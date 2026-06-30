from pydantic import BaseModel, Field, NonNegativeFloat
from datetime import datetime


class ChatRequest(BaseModel):
    prompt: str
    system: str | None = None
    max_history: int = Field(ge=5)
    temperature: NonNegativeFloat


class ChatResponse(BaseModel):
    answer: str


class ChatMessageOut(BaseModel):
    id: int
    role: str
    content: str
    created_at: datetime


class ChatHistory(BaseModel):
    items: list[ChatMessageOut]
