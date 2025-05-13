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

@app.get("/api/v1/ping", response_model=ServiceResponse)
async def forward_ping():
    """Forward the ping request to the text-to-text service"""
    async with httpx.AsyncClient(timeout=5.0) as client:
        try:
            # Use the correct service name 'text_to_text'
            response = await client.get("http://text_to_text:8000/ping")
            response.raise_for_status()
            # Return the JSON response from the service
            return response.json()
        except httpx.RequestError as e:
            logger.error(f"Error forwarding ping request: {e.request.url} - {e}")
            raise HTTPException(status_code=503, detail=f"Text-to-text service unavailable: {str(e)}")
        except httpx.HTTPStatusError as e:
            logger.error(f"Error forwarding ping request, status {e.response.status_code}: {e.response.text}")
            raise HTTPException(status_code=e.response.status_code, detail=e.response.text)
        except Exception as e:
            logger.error(f"Unexpected error forwarding ping request: {str(e)}")
            raise HTTPException(status_code=500, detail=f"Internal server error forwarding ping: {str(e)}")


@app.get("/api/v1/models")
async def forward_list_models():
    """Forward the list models request to the text-to-text service"""
    async with httpx.AsyncClient(timeout=30.0) as client:
        try:
            response = await client.get("http://text_to_text:8000/models")
            response.raise_for_status()
            return response.json()
        except Exception as e:
            logger.error(f"Error forwarding list models request: {str(e)}")
            raise HTTPException(status_code=500, detail=f"Error listing models: {str(e)}")

@app.post("/api/v1/simple-prompt")
async def forward_simple_prompt(prompt: str):
    """Forward a simple prompt to the text-to-text service"""
    async with httpx.AsyncClient(timeout=150.0) as client:
        try:
            response = await client.post(
                "http://text_to_text:8000/simple-prompt",
                params={"prompt": prompt}
            )
            response.raise_for_status()
            return response.json()
        except Exception as e:
            logger.error(f"Error forwarding simple prompt: {str(e)}")
            raise HTTPException(status_code=500, detail=f"Error processing prompt: {str(e)}")