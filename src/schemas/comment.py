from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Field

from src.schemas.users import UserResponse


class CommentCreate(BaseModel):
    comment: str = Field(min_length=3, max_length=255)


class CommentUpdate(BaseModel):
    pass


class CommentResponse(BaseModel):
    id: int
    comment: str
    created_at: Optional[datetime]
    updated_at: Optional[datetime]
    user: Optional[UserResponse]

    class Config:
        from_attributes = True