import requests
import logging
from typing import Dict, Any, Optional, List

logger = logging.getLogger(__name__)

class OllamaClient:
    def __init__(self, base_url: str = "http://ollama:11434"):
        self.base_url = base_url
        logger.info(f"Initialized Ollama client with base URL: {base_url}")

    def generate(self, 
                 model: str, 
                 prompt: str, 
                 system: Optional[str] = None,
                 temperature: float = 0.7,
                 **payload_params) -> Dict[Any, Any]:
        """
        Generate a response from an Ollama model.
        
        Args:
            model: The name of the model to use
            prompt: The prompt to send to the model
            system: Optional system prompt for context
            temperature: Controls randomness (0.0 to 1.0)
            
        Returns:
            The model's response as a dictionary
        """
        url = f"{self.base_url}/api/generate"
        
        payload = {
            "model": model,
            "prompt": prompt,
            "temperature": temperature,
            **payload_params,
        }
        
        if system:
            payload["system"] = system
            
        try:
            logger.debug(f"Sending request to Ollama with model: {model}")
            response = requests.post(url, json=payload)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            logger.error(f"Error calling Ollama API: {str(e)}")
            raise
    
    def list_models(self) -> List[Dict[str, Any]]:
        """List all available models on the Ollama server"""
        url = f"{self.base_url}/api/tags"
        
        try:
            response = requests.get(url)
            response.raise_for_status()
            return response.json().get("models", [])
        except requests.exceptions.RequestException as e:
            logger.error(f"Error listing Ollama models: {str(e)}")
            raise