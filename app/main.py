
from fastapi.params import *
from fastapi import FastAPI
import psycopg2
from   psycopg2.extras import RealDictCursor
import time 
from . import models
from .database import engine, get_db
from .routers import post, user, auth

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

app.include_router(post.router)
app.include_router(user.router)
app.include_router(auth.router)