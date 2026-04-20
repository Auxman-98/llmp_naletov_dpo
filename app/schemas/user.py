from pydantic import BaseModel, EmailStr

from .core.config import settings


class UserPublic(BaseModel):
    id: int
    email: EmailStr
    role: str


settings.model_config = {"from_attributes": True}
