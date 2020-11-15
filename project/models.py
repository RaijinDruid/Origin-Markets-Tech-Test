from sqlalchemy import Column, Integer, String
from flask_sqlalchemy import SQLAlchemy
from project.database import Base

class User(Base):
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True)
    email = Column(String, nullable = False)
    password = Column(String, nullable=False)