from typing import List, Optional

from pydantic import BaseModel


class BlogBase(BaseModel):
    title: str
    body: str
    user_id: int


class Blog(BlogBase):
    class Config:
        orm_mode = True


class User(BaseModel):
    name: str
    surname: str
    email: str
    password: str


class UserInDB(User):
    hashed_password: str


class ShowBlog(BaseModel):
    title: str
    body: str

    class Config:
        orm_mode = True


class ShowUser(BaseModel):
    name: str
    surname: str
    email: str
    blogs: List[ShowBlog] = []

    class Config:
        orm_mode = True


class Login(BaseModel):
    user_name: str
    password: str


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    name: Optional[str] = None
