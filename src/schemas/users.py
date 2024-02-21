from datetime import date
from pydantic import BaseModel, EmailStr, Field 

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

    class Config:
        from_attributes = True
        
class UserProfileResponse(BaseModel):
    username: str
    photoloadedcount: int = 0  #additional task 1
    class Config:
        from_attributes = True
    
        
        

