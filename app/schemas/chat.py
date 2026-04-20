from pydantic import BaseModel


class ChatRequest(BaseModel):
    prompt: str
    system: str
    max_history: int
    temperature: float


class ChatResponse(BaseModel):
    answer: str
