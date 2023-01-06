'''
    models: SQLAlchemy Models
    This file defines the structure of the table created by sqlalchemy
'''

from .database import Base
from sqlalchemy.orm import relationship
from sqlalchemy.sql.expression import text
from sqlalchemy import Boolean, Column, Integer, String, TIMESTAMP, ForeignKey

class Post(Base):

    __tablename__ = "posts"
    id = Column(Integer, primary_key=True, nullable=False, index=True)
    title = Column(String(length=100), nullable=False)
    content = Column(String(length=200), nullable=False)
    published = Column(Boolean, server_default='1', nullable=False)
    created_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text('now()'))
    ## Foreign Key -> users.id
    ## CASCADE -> delete the related post if users.id is deleted
    owner_id = Column(Integer, ForeignKey(column="users.id", ondelete="CASCADE"), nullable=False)
    owner = relationship("User")    ## Forming a relationship with the User model

class User(Base):

    __tablename__ = "users"
    id = Column(Integer, primary_key=True, nullable=False, index=True)
    email = Column(String(length=30), nullable=False, unique=True)
    password = Column(String(length=60), nullable=False)
    created_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text('now()'))

class Vote(Base):
    __tablename__ = "votes"

    ## Composite keys
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), primary_key=True)
    post_id = Column(Integer, ForeignKey("posts.id", ondelete="CASCADE"), primary_key=True)