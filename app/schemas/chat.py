from pydantic import BaseModel, Field, NonNegativeFloat


class ChatRequest(BaseModel):
    prompt: str
    system: str | None = None
    max_history: int = Field(ge=5)
    temperature: NonNegativeFloat


class ChatResponse(BaseModel):
    answer: str
