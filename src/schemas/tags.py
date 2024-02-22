from datetime import datetime
from typing import List, Optional
from pydantic import BaseModel, Field

from src.schemas.users import UserResponse


class TagSchema(BaseModel):
    name: str = Field(max_length=25)


class TagUpdateSchema(TagSchema):
    completed: bool


class TagResponse(BaseModel):
    id: int = 1
    name: str
    created_at: datetime | None
    updated_at: datetime | None
    user: UserResponse | None

    class Config:
        from_attributes = True
