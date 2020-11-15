import project.schemas
from sqlalchemy.orm import Session
from .models import User
from .database import get_db
from .util import serialize_data
from . import schemas, security

db = next(get_db())
def create_user(user: schemas.UserCreate):
    user.password = security.get_password_hash(user.password)
    new_user = User(**user.dict())
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return serialize_data(new_user, schemas.User)

def get_users():
    users = db.query(User).all()
    return serialize_data(users, schemas.User)

def get_user_by_email(email: str):
    user = db.query(User).filter(User.email == email).first()
    if user:
        return serialize_data(user, schemas.User)
    return False

def authenticate_user(email: str, password: str):
    user = get_user_by_email(db, email=email)
    if not user:
        return False
    if not verify_password(password, user.hashed_password):
        return False
    return user