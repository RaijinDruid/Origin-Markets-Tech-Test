from pydantic import BaseModel
from typing import List, Optional


class BondCreate(BaseModel):
    isin: str
    size: int
    currency: str
    maturity: str
    lei: str


class Bond(BondCreate):
    id: int
    legal_name: str
    user_id: int

    class Config:
        orm_mode = True


class UserBase(BaseModel):
    email: str


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

