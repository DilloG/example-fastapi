from datetime import datetime
from typing import Optional, ClassVar
from pydantic import BaseModel, EmailStr, conint


# User Section ----------------

class UserCreate(BaseModel):
    email: EmailStr
    password: str

class UserOut(BaseModel):
    id: int
    email: EmailStr
    created_at: datetime

class UserLogin(BaseModel):
    email: EmailStr
    password: str

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    id: Optional[str] = None

# POST -----------

class PostBase(BaseModel):
    title: str
    content: str
    published: int = 1

class PostCreate(PostBase):
    pass

# Response model
class Post(PostBase):
    id: int
    created_at: datetime
    owner_id: int
    owner: UserOut
    
class Vote(BaseModel):
    post_id: int
    dir: int

class PostOut(BaseModel):
    Post: Post
    votes: int