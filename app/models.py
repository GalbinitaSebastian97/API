from typing import Text
from sqlalchemy.sql.sqltypes import TIMESTAMP
from .database import Base
from sqlalchemy import Column, Integer, String, Boolean
from sqlalchemy.sql.expression import text

# create all of the models !!Read the documnetation!!


class Post(Base):
    __tablename__ = "posts"

    id = Column(Integer, primary_key = True, nullable = False)
    title = Column(String, nullable = False)
    content = Column(String, nullable = False)
    # If you want the default to reflect into the database you have to use server_default=<string>
    published = Column(Boolean, server_default = 'TRUE', nullable = False )
    created_at = Column(TIMESTAMP(timezone = True), nullable = False, server_default = text('now()'))

#Creating User functionality
class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key = True, nullable = False)
    email = Column(String, nullable = False, unique = True)
    password = Column(String, nullable = False)
    created_at = Column(TIMESTAMP(timezone = True), nullable = False, server_default = text('now()'))

