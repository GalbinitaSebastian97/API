from pydantic import BaseModel

#Create models for each different requests
class PostBase(BaseModel):
    title: str
    content: str
    published : bool = True

class PostCreate(PostBase):
    pass

class PostUpdate(PostBase):
    pass


