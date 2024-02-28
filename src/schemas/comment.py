from datetime import datetime
from typing import Optional
from src.entity.models import Comment
from pydantic import BaseModel, Field

from src.schemas.users import UserResponse


# add images
class CommentBase(BaseModel):
    comment: str = Field(..., max_length=255)


class CommentCreate(CommentBase):
    pass


class CommentUpdate(CommentBase):
    pass


class CommentResponse(BaseModel):
    id: int
    comment: str
    created_at: Optional[datetime]
    updated_at: Optional[datetime]
    user: Optional[UserResponse]

    class Config:
        from_attributes = True
