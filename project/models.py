from sqlalchemy import Column, Integer, String, ForeignKey
from flask_sqlalchemy import SQLAlchemy
from project.database import Base
from sqlalchemy.orm import relationship

class User(Base):
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True)
    email = Column(String, nullable = False, unique=True)
    password = Column(String, nullable=False)

    bonds = relationship("Bond", back_populates="owner")

class Bond(Base):
    __tablename__ = "bonds"

    id = Column(Integer, primary_key=True)
    email = Column(String, nullable = False, unique=True)
    password = Column(String, nullable=False)
    user_id = Column(Integer, ForeignKey("users.id"))

    owner = relationship("User", back_populates="bonds")