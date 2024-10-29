from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import declarative_base


base = declarative_base()

class User(base):
    __tablename__ = 'user'
    id = Column(Integer, primary_key=True)
    username = Column(String, nullable=False)
    password = Column(String, nullable=True)
    is_ban = Column(Integer, nullable=True)
    is_admin = Column(Integer, nullable=True)
    password_limit = Column(Integer, nullable=True)


