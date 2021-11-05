from typing import Optional
from pydantic import BaseModel,EmailStr
from datetime import datetime

#Create models for each different requests
class PostBase(BaseModel):
    title: str
    content: str
    published : bool = True

class PostCreate(PostBase):
    pass

class PostUpdate(PostBase):
    pass

class UserCreate(BaseModel):
    email: EmailStr
    password: str

class UserOut(BaseModel):
    id: int
    email: EmailStr
    created_at: datetime

    class Config:
        orm_mode = True

class UserLogin(BaseModel):
    email: EmailStr
    password: str
# Tackle the response
# Sending specific fields to the users
class Post(PostBase):
    id: int
    created_at: datetime
    owner_id: int
    owner: UserOut
    #necessary Convert a sqlalchemy ointo a pydentic model

    class Config:
        orm_mode = True

# Schema for the Access Token
class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    id: Optional[str] = None

    

