# filepath: c:\Users\aryav\projects\snippet-flow2\backend\model.py
# filepath: c:\Users\aryav\projects\snippet-flow2\backend\main.py
# Get database URL from environment variable
import os
from dotenv import load_dotenv
from sqlalchemy import create_engine, Column, Integer, String, Boolean, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship 
from pgvector.sqlalchemy import Vector
from database import Base

class Snippets(Base):
    __tablename__ = 'snippets'
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    text = Column(String, nullable=False)
    author = Column(String)
    hasEmbedding = Column(Boolean, default=False)
    interactions = relationship("UserSnippetInteraction", back_populates="snippet")
    snippet_embeddings = relationship("SnippetEmbeddings", back_populates="snippet")

class SnippetEmbeddings(Base):
    __tablename__ = 'snippet_embeddings'
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    snippet_id = Column(Integer, ForeignKey('snippets.id'), nullable=False)
    embedding = Column(Vector, nullable=False)
    snippet = relationship("Snippets", back_populates="snippet_embeddings")

class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    username = Column(String, unique=True, nullable=False, index=True)
    password = Column(String, nullable=False)
    interactions = relationship("UserSnippetInteraction", back_populates="user")

class UserSnippetInteraction(Base):
    __tablename__ = 'usi'
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    snippet_id = Column(Integer, ForeignKey('snippets.id'), nullable=False)
    rating = Column(Integer, default=0)  # +1 for like, -1 for dislike, 0 neutral
    user = relationship("User", back_populates="interactions")
    snippet = relationship("Snippets", back_populates="interactions")

