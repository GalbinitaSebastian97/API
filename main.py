from fastapi import FastAPI, Response, status, HTTPException
from fastapi.params import *
from pydantic import BaseModel
from random import randrange

app = FastAPI()

class Post(BaseModel):
    title: str
    content: str
    published : bool = True
    rating: Optional[int] = None

my_posts = [{"title":"title post one","content": "content of post 1","id":1},
            {"title":"title post two","content": "content of post 2","id":2}]

def find_post(id):
    for p in my_posts:
        if p['id'] == id:
            return p
@app.get("/") #->root path
async def root():
    return {"message":"Hello world !! !!"}

@app.get("/posts")
def get_posts():
    return {"data":my_posts}

@app.post("/posts",status_code = status.HTTP_201_CREATED)
def create_post(post:Post):
    post_dict = post.dict()
    post_dict['id'] = randrange(1,10000000)
    my_posts.append(post_dict)
    print(my_posts)
    return {"data":my_posts}

@app.get("/posts/{id}")
def get_posts(id:int,response: Response):
    print(id)
    post = find_post(int(id))
    if not post:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail = "post with id: {id} was not found")
        #response.status_code = status.HTTP_404_NOT_FOUND
        #return {'message':'post with id {} was not found'.format(id)}
    return {"post_detail":post}