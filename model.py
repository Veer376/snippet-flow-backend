# filepath: c:\Users\aryav\projects\snippet-flow2\backend\model.py
# filepath: c:\Users\aryav\projects\snippet-flow2\backend\main.py
# Get database URL from environment variable
import os
from dotenv import load_dotenv
from sqlalchemy import create_engine, Column, Integer, String, Boolean, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship 

load_dotenv()
DATABASE_URL = os.environ.get('DATABASE_URL')

# Create a SQLAlchemy engine
engine = create_engine(DATABASE_URL)

# Base class for declarative models
Base = declarative_base()

class Snippet(Base):
    __tablename__ = 'snippets'
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    text = Column(String, nullable=False)
    author = Column(String)
    hasEmbedding = Column(Boolean, default=False)
    interactions = relationship("UserSnippetInteraction", backref="snippet")

class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    username = Column(String, unique=True, nullable=False, index=True)
    password = Column(String, nullable=False)
    interactions = relationship("UserSnippetInteraction", backref="user")

# User-Snippet interaction model
# This model will store the interactions between users and snippets.
class UserSnippetInteraction(Base):
    __tablename__ = 'usi'
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    snippet_id = Column(Integer, ForeignKey('snippets.id'), nullable=False)
    rating = Column(Integer, default=0)  # +1 for like, -1 for dislike, 0 neutral

# Base.metadata.drop_all(bind=engine)
Base.metadata.create_all(bind=engine)
