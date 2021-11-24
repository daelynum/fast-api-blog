from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from .database import Base


class Blog(Base):
    __tablename__ = 'blogs'
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String)
    body = Column(String)
    user_id = Column(Integer, ForeignKey('registered_users.id'), nullable=False)

    creator = relationship("Users", back_populates="blogs")


class Users(Base):
    __tablename__ = 'registered_users'

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    surname = Column(String)
    email = Column(String, unique=True)
    password = Column(String)

    blogs = relationship('Blog', back_populates='creator')
