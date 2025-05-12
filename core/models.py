from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any

class Message(BaseModel):
    role: str = Field(..., description="The role of the message sender (e.g., 'user', 'assistant')")
    content: str = Field(..., description="The content of the message")

class ChatRequest(BaseModel):
    messages: List[Message] = Field(..., description="List of messages in the conversation")
    model: str = Field(..., description="The model to use for generation")
    temperature: float = Field(0.7, description="Controls randomness in generation (0.0 to 1.0)")
    system: Optional[str] = Field(None, description="Optional system prompt for context")

class ChatResponse(BaseModel):
    response: str = Field(..., description="The text response from the model")
    model: str = Field(..., description="The model used for generation")
    usage: Dict[str, Any] = Field(default_factory=dict, description="Usage statistics")