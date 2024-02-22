from typing import Optional
from datetime import date, datetime
from pydantic import BaseModel, Field
from src.schemas.users import UserResponse


# Here are some shemas for validation of input information


class ImageSchema(BaseModel):
    description: str = Field(min_length=3, max_length=150)
    # image: str = Field(min_length=3, max_length=255)


class ImageUpdateSchema(ImageSchema):
    pass


class ImageResponse(BaseModel):
    id: int = 1
    description: str
    image: str
    created_at: datetime | None  # for user
    updated_at: datetime | None
    user: UserResponse | None

    # add tags and comments
    class Config:
        from_attributes = True
