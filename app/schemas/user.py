from pydantic import BaseModel, EmailStr

from app.core.config import Settings


class UserPublic(BaseModel):
    id: int
    email: EmailStr
    role: str


Settings.model_config = {"from_attributes": True}
