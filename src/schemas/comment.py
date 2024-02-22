from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Field

from src.schemas.users import UserResponse


class CommentBase(BaseModel):
    content: str = Field(..., max_length=255)


class CommentCreate(CommentBase):
    pass


class CommentUpdate(CommentBase):
    pass


class CommentResponse(BaseModel):
    id: int
    content: str
    created_at: Optional[datetime]
    updated_at: Optional[datetime]
    user: Optional[UserResponse]

    class Config:
        orm_mode = True
