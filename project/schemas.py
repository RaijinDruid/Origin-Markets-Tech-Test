from pydantic import BaseModel
from typing import List, Optional

class Bond(BaseModel):
    id: int

class UserBase(BaseModel):
    email:str

class UserCreate(UserBase):
    password: str

class User(UserBase):
    id: int
    bonds: List[Bond] = []
    
    class Config:
        orm_mode = True

class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    username: Optional[str] = None