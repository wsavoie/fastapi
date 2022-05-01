from datetime import datetime
from typing import Optional
from pydantic import BaseModel, EmailStr, conint



class UserBase(BaseModel):
    email: EmailStr

class UserCreate(UserBase):
    password: str

class UserResponse(UserBase):
    id: int
    created_at: datetime
    class Config:
        orm_mode = True

class UserLogin(UserBase):
    password: str

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    username: Optional[str] = None

class PostBase(BaseModel):
    title: str
    content: str
    published: bool = True


    
class PostCreate(PostBase):
    pass

class PostResponse(PostBase):
    id: int
    created_at: datetime
    user_id: int
    user: UserResponse
    class Config:
        orm_mode = True

class PostOut(BaseModel):
    Post: PostResponse
    votes: int
    # score: int cannot get this to work coalesce is buggy and second argument doesn't process correctly when viewing outputted sql statemetn

class VoteBase(BaseModel):
    post_id: int
    direction: conint(le=1,ge=-1)

class VoteCreate(VoteBase):
    pass

class VoteResponse(VoteBase):
    # total_votes: int
    user_id: int
    class Config:
        orm_mode = True