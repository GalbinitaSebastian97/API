from .. import models, schemas,oauth2
from fastapi import  Response, status, HTTPException, Depends, APIRouter
from ..database import get_db
from sqlalchemy.orm import Session
from typing import List

router = APIRouter(
    prefix = "/posts",
    tags = ['Posts'] # group the in the docs root/docs
)

@router.get("/", response_model= List[schemas.Post]) 
def get_posts(
    db:Session = Depends(get_db), 
    current_user: int = Depends(oauth2.get_current_user), 
    limit: int = 10,
    skip:int = 0 #helpfull for pagination
    ):
    # cursor.execute("SELECT * FROM posts")
    # posts = cursor.fetchall()
    #For all users
    post = db.query(models.Post).limit(limit).offset(skip).all()
    
    # Posts for users that ale logged in
    # post = db.query(models.Post).filter(models.Post.owner_id == current_user.id).all()  
    return post

@router.post("/",status_code = status.HTTP_201_CREATED, response_model = schemas.Post)
def create_post(post: schemas.PostCreate,db:Session = Depends(get_db), current_user:int = Depends(oauth2.get_current_user)): # gives access to the databse
    #cursor.execute("INSERT INTO posts (title, content, published) VALUES (%s,%s,%s) RETURNING *",
                    #(post.title,post.content,post.published))
    #new_post = cursor.fetchone()
    #conn.commit() # push the changes to the database
    # **post.dict() same as title = post.title, content = post.content, published = post.published
    
    new_post = models.Post(owner_id = current_user.id,**post.dict())
    db.add(new_post)
    db.commit()
    # RETURNING *
    db.refresh(new_post)
    return new_post

@router.get("/{id}",response_model = schemas.Post)
def get_post(id:int,db:Session = Depends(get_db),current_user:int = Depends(oauth2.get_current_user)):
    #cursor.execute("SELECT * FROM posts WHERE id= %s",(str(id)))
    #post = cursor.fetchone()
    post = db.query(models.Post).filter(models.Post.id == id).first()
    if not post:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail = f"post with id: {id} was not found")
        #response.status_code = status.HTTP_404_NOT_FOUND
        #return {'message':'post with id {} was not found'.format(id)}
    return post
    
@router.delete("/{id}",status_code = status.HTTP_204_NO_CONTENT)
def delete_post(id: int,db:Session = Depends(get_db),current_user:int = Depends(oauth2.get_current_user)):

    deleted_post = db.query(models.Post).filter(models.Post.id == id)
    post = deleted_post.first()

    if deleted_post.first() == None:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND,detail = "post with id {} not found".format(id))

    if post.owner_id != current_user.id:
        raise HTTPException(status_code = status.HTTP_403_FORBIDDEN, detail = "Not authorized tp perform requested action")

    deleted_post.delete(synchronize_session= False)
    db.commit()
    return Response(status_code = status.HTTP_204_NO_CONTENT)

@router.put("/{id}",status_code = status.HTTP_201_CREATED,response_model = schemas.Post)
def update_post(id: int,updated_post: schemas.PostCreate,db:Session = Depends(get_db),current_user:int = Depends(oauth2.get_current_user)):
    
    post_query = db.query(models.Post).filter(models.Post.id == id)
    post = post_query.first()
    if post == None:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND,detail = "post with id {} not found".format(id))

    if post.owner_id != current_user.id:
        raise HTTPException(status_code = status.HTTP_403_FORBIDDEN, detail = "Not authorized tp perform requested action")

    post_query.update(updated_post.dict(),synchronize_session = False)
    db.commit()
    return post_query.first()