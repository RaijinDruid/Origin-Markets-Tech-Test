from .models import User, Bond
from .database import get_db
from . import security
from .schemas import UserCreate, BondCreate
import requests

db = next(get_db())


def create_user(user: UserCreate):
    user.password = security.get_password_hash(user.password)
    new_user = User(**user.dict())
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user


def get_user(id: int):
    return db.query(User).filter(User.id == id).first()


def get_users():
    return db.query(User).all()


def get_user_by_email(email: str):
    return db.query(User).filter(User.email == email).first()


def authenticate_user(email: str, password: str):
    user = get_user_by_email(email=email)
    if not user:
        return False
    if not security.verify_password(password, user.password):
        return False
    return user


def create_bond(bond: BondCreate, user_id: int, legal_name: str):
    new_bond = Bond(**bond.dict(), user_id=user_id, legal_name=legal_name)
    db.add(new_bond)
    db.commit()
    db.refresh(new_bond)
    return new_bond


def get_legal_name(lei: str):
    response = requests.get(f"https://leilookup.gleif.org/api/v2/leirecords?lei={lei}")
    data = response.json()

    if not response.status_code == 200 or not data[0]['Entity']['LegalName']['$']:
        return False

    return data[0]['Entity']['LegalName']['$']
