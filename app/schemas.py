'''
    schemas: Pydantic Models
    Pre-defined fields for user request
    Pre-defined fields for server response
'''

from pydantic import BaseModel, EmailStr
from pydantic.types import conint
from datetime import datetime
from typing import Optional

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

## Base class
class PostBase(BaseModel):
    title: str
    content: str
    published: bool = True

## Base class for creating posts
class PostCreate(PostBase):
    pass

## Required structure of a Post inheriting from PostBase(title, content, published)
class Post(PostBase):
    id: int
    created_at: datetime
    owner_id: int
    owner: UserOut
    ## (=) config value
    ## (:) type declaration
    class Config:
        orm_mode = True

class PostOut(BaseModel):
    Post: Post
    votes: int

    class Config:
        orm_mode = True

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenPayload(BaseModel):
    id: Optional[str] = None

class Vote(BaseModel):
    post_id: int
    dir: conint(le=1)   ## Less than 1