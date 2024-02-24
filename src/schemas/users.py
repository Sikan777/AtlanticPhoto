import datetime
from typing import Optional
from pydantic import BaseModel, EmailStr, Field
from typing import Optional
from src.entity.models import Role
from datetime import datetime


from src.entity.models import Role
# Here are some shemas for responce and validation information


class UserSchema(BaseModel):
    username: str = Field(min_length=3, max_length=50)
    email: EmailStr
    password: str = Field(min_length=6, max_length=8)


class TokenSchema(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = "bearer"


class UserResponse(BaseModel):
    id: int = 1
    username: str
    email: EmailStr
    avatar: str | None
    role: Role  # 21.02.2024 Богдан
    created_at: datetime
    picture_count: Optional[int]

    class Config:
        from_attributes = True


# Цей код визначає модель Pydantic для представлення спрощених даних користувача, включаючи їх повне ім'я, електронну пошту, URL або шлях до аватару, кількість зображень, які належать користувачеві, а також дату та час їх створення.
class AnotherUsers(BaseModel):
    username: str
    email: EmailStr
    avatar: str
    picture_count: Optional[int]
    created_at: datetime


class UserUpdate(BaseModel):
    username: str
    email: EmailStr
    password: str
