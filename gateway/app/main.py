import logging
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import httpx
from pydantic import BaseModel

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)
logger = logging.getLogger("api_gateway")

app = FastAPI(title="NexusForge API Gateway", version="0.1.0")

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, specify the allowed origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class ServiceResponse(BaseModel):
    message: str


@app.get("/health", response_model=ServiceResponse)
async def health_check():
    """Health check endpoint for the API Gateway"""
    return {"message": "API Gateway is healthy"}


@app.get("/services/health", response_model=ServiceResponse)
async def services_health():
    """Check health of all dependent services"""
    services = {"text_to_text": "http://text_to_text:8000/health"}

    results = {}
    all_healthy = True

    async with httpx.AsyncClient(timeout=5.0) as client:
        for service_name, health_url in services.items():
            try:
                response = await client.get(health_url)
                if response.status_code == 200:
                    results[service_name] = "healthy"
                else:
                    results[service_name] = (
                        f"unhealthy (status: {response.status_code})"
                    )
                    all_healthy = False
            except Exception as e:
                results[service_name] = f"error ({str(e)})"
                all_healthy = False

    if all_healthy:
        return {"message": "All services are healthy"}
    else:
        raise HTTPException(
            status_code=503, detail=f"Service health check failed: {results}"
        )


# Placeholder for future routes that will be added for text-to-text endpoints
