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

# Tackle the response
# Sending specific fields to the users
class Post(PostBase):
    created_at: datetime
    #necessary Convert a sqlalchemy ointo a pydentic model
    class Config:
        orm_mode = True


class UserCreate(BaseModel):
    email: EmailStr
    password: str

class UserOut(BaseModel):
    id: int
    email: EmailStr
    created_at: datetime

    class Config:
        orm_mode = True