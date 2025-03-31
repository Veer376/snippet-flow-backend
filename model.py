# filepath: c:\Users\aryav\projects\snippet-flow2\backend\model.py
# filepath: c:\Users\aryav\projects\snippet-flow2\backend\main.py
# Get database URL from environment variable
import os
from dotenv import load_dotenv
from sqlalchemy import create_engine, Column, Integer, String, Boolean, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship 
from database import Base, es_client


class Snippet(Base):
    __tablename__ = 'snippet'
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    text = Column(String, nullable=False)
    author = Column(String)
    interactions = relationship("UserSnippetInteraction", back_populates="snippet")
    snippet_embedding = relationship("SnippetEmbedding", back_populates="snippet")

class User(Base):
    __tablename__ = 'user'
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    email = Column(String, unique=True, nullable=False, index=True)
    password = Column(String, nullable=False)
    interactions = relationship("UserSnippetInteraction", back_populates="user")

class UserSnippetInteraction(Base):
    __tablename__ = 'usi'
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey('user.id'), nullable=False)
    snippet_id = Column(Integer, ForeignKey('snippet.id'), nullable=False)
    rating = Column(Integer, default=0)  # +1 for like, -1 for dislike, 0 neutral
    user = relationship("User", back_populates="interactions")
    snippet = relationship("Snippet", back_populates="interactions")

"""
elasticsearch: 

snippet_embedding {
    "snippet_id" : 1,
    "embedding" : [0.1, 0.2, 0.3, ...]
    "text" : "this is the snippet" # we need this to avoid making one extra query to the postgres.
}
"""
response = es_client.indices.create(
    index="snippet_embedding",
    body={
        "mappings": {
            "dynamic": False,
            "properties": {
                "snippet_id": {"type": "integer"},
                "embedding": {"type": "dense_vector", "dims": 768},
                "snippet": {
                    "properties": {
                        "text": {"type": "text"},
                        "author": {"type": "text"}
                    }
                }
            }
        }
    }
)

