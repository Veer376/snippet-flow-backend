import os
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

DATABASE_URL = os.getenv('DATABASE_URL', "postgresql://username:password@postgres:5432/snippet-flow-db")

# Create a SQLAlchemy engine
engine = create_engine(
    DATABASE_URL,
    pool_size = 100,
    max_overflow = 200,
    pool_timeout = 30,
)

# Create a session factory
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base class for declarative models
Base = declarative_base()
