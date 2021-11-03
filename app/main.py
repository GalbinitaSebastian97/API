from fastapi import FastAPI, Response, status, HTTPException, Depends
from fastapi.params import *
from pydantic import BaseModel
from random import randrange
import psycopg2
from psycopg2.extras import RealDictCursor
import time 
from . import models, schemas
from .database import engine, get_db
from sqlalchemy.orm  import Session

# create all of the models !!Read the documnetation!!
models.Base.metadata.create_all(bind = engine)

app = FastAPI()

while True:

    try:
        conn = psycopg2.connect( host = 'localhost',database = 'fastapi',user = 'postgres',password = '1234', 
                                cursor_factory= RealDictCursor)
        cursor = conn.cursor()
        print("Database connection was successful.")
        break
    except Exception as error:
        print("Connection to database failde")
        print("Error:",error)
        time.sleep(2)

@app.get("/posts") 
def get_posts(db:Session = Depends(get_db)):
    # cursor.execute("SELECT * FROM posts")
    # posts = cursor.fetchall()
    posts = db.query(models.Post).all()
    return {"data":posts}

@app.post("/posts",status_code = status.HTTP_201_CREATED)
def create_post(post: schemas.PostCreate,db:Session = Depends(get_db) ): # giving access to the databse
    #cursor.execute("INSERT INTO posts (title, content, published) VALUES (%s,%s,%s) RETURNING *",
                    #(post.title,post.content,post.published))
    #new_post = cursor.fetchone()
    #conn.commit() # push the changes to the database
    # **post.dict() same as title = post.title, content = post.content, published = post.published
    new_post = models.Post(**post.dict())
    db.add(new_post)
    db.commit()
    # RETURNING *
    db.refresh(new_post)
    return {"data": new_post}

@app.get("/posts/{id}")
def get_post(id:int,db:Session = Depends(get_db)):
    #cursor.execute("SELECT * FROM posts WHERE id= %s",(str(id)))
    #post = cursor.fetchone()
    post = db.query(models.Post).filter(models.Post.id == id).first()
    if not post:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail = f"post with id: {id} was not found")
        #response.status_code = status.HTTP_404_NOT_FOUND
        #return {'message':'post with id {} was not found'.format(id)}
    return {"post_detail":post}
    
@app.delete("/posts/{id}",status_code = status.HTTP_204_NO_CONTENT)
def delete_post(id: int,db:Session = Depends(get_db)):
    #cursor.execute("DELETE FROM posts WHERE id = %s RETURNING *",(str(id),))
    #deleted_post = cursor.fetchone()
    #conn.commit()
    deleted_post = db.query(models.Post).filter(models.Post.id == id)

    if deleted_post.first() == None:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND,detail = "post with id {} not found".format(id))
    deleted_post.delete(synchronize_session= False)
    db.commit()
    return Response(status_code = status.HTTP_204_NO_CONTENT)

@app.put("/posts/{id}",status_code = status.HTTP_201_CREATED)
def update_post(id: int,post: schemas.PostCreate,db:Session = Depends(get_db)):
    #cursor.execute("UPDATE posts SET title = %s, content = %s, published = %s WHERE id = %s RETURNING ",
                    #(post.title,post.content,post.published,str(id)))
    #updated_post = cursor.fetchone()
    #conn.commit()
    updated_post = db.query(models.Post).filter(models.Post.id == id)

    if updated_post == None:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND,detail = "post with id {} not found".format(id))
    
    updated_post.update(post.dict(),synchronize_session = False)
    db.commit()
    return {"data":updated_post.first()}