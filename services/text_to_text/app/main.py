import logging
import requests
from typing import List, Dict, Any, Optional

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from nexusforge_core.logging_config import configure_logging, get_logger
from nexusforge_core.models import Message, ChatRequest, ChatResponse
from nexusforge_core.llm_client import OllamaClient

# Configure logging
configure_logging(level=logging.INFO)
logger = get_logger("text_to_text_service")

app = FastAPI(title="Text-to-Text Service", version="0.1.0")

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, specify the allowed origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

OLLAMA_API_URL = "http://ollama:11434/api"


class ServiceResponse(BaseModel):
    message: str


class Message(BaseModel):
    role: str
    content: str


class ChatRequest(BaseModel):
    messages: List[Message]
    model: str = "llama3"
    temperature: float = 0.7
    system: Optional[str] = None


class ChatResponse(BaseModel):
    response: str
    model: str
    usage: Dict[str, Any] = {}


@app.get("/health", response_model=ServiceResponse)
async def health_check():
    """Health check endpoint for the text-to-text service"""
    try:
        # Check if Ollama service is reachable
        response = requests.get(f"{OLLAMA_API_URL}/tags", timeout=5)
        if response.status_code == 200:
            return {"message": "Text-to-text service is healthy"}
        else:
            logger.error(f"Ollama health check failed: {response.status_code}")
            raise HTTPException(
                status_code=503, detail="Ollama service is not available"
            )
    except Exception as e:
        logger.error(f"Ollama health check failed: {str(e)}")
        raise HTTPException(
            status_code=503, detail=f"Ollama service is not available: {str(e)}"
        )


@app.post("/chat", response_model=ChatResponse)
async def chat(request: ChatRequest):
    """Basic endpoint for chat interaction with an LLM"""

    logger.info(f"Chat request received for model: {request.model}")

    # Convert messages to the format expected by Ollama
    formatted_messages = []
    for msg in request.messages:
        formatted_messages.append({"role": msg.role, "content": msg.content})

    # Prepare the request payload
    payload = {
        "model": request.model,
        "messages": formatted_messages,
        "temperature": request.temperature,
    }

    if request.system:
        payload["system"] = request.system

    try:
        # Send the request to Ollama
        response = requests.post(f"{OLLAMA_API_URL}/chat", json=payload, timeout=60)
        response.raise_for_status()
        data = response.json()

        # Extract the response from Ollama
        return {
            "response": data["message"]["content"],
            "model": request.model,
            "usage": data.get("usage", {}),
        }
    except Exception as e:
        logger.error(f"Error calling Ollama API: {str(e)}")
        raise HTTPException(
            status_code=500, detail=f"Error generating response: {str(e)}"
        )

@app.get("/models", response_model=dict)
async def list_models():
    """List all available models from Ollama"""
    try:
        logger.info("Requesting model list from Ollama")
        models = ollama_client.list_models()
        return {"models": models}
    except Exception as e:
        logger.error(f"Error listing models from Ollama: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error listing models: {str(e)}")

        
@app.post("/simple-prompt", response_model=dict)
async def simple_prompt(prompt: str):
    """Send a simple prompt to Ollama and return the response"""
    try:
        logger.info(f"Sending simple prompt to Ollama: {prompt}")
        response = ollama_client.generate(
            model="tinyllama",  # Using tinyllama as specified in the roadmap
            prompt=prompt,
            temperature=0.7
        )
        return {"response": response}
    except Exception as e:
        logger.error(f"Error sending prompt to Ollama: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error generating response: {str(e)}")

@app.get("/ping", response_model=ServiceResponse)
async def ping():
    """Simple ping endpoint to test service availability"""
    return {"message": "pong"}
