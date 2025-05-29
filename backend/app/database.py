import os
from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker
# from dotenv import load_dotenv

# load_dotenv()

# DATABASE_URL = os.getenv("DATABASE_URL")

DATABASE_URL='postgresql://postgres:bcorji@localhost:5432/taskmanager'

print("Database URL:", DATABASE_URL)  # for debugging purposes
if not DATABASE_URL:
    raise ValueError("DATABASE_URL environment variable is not set.")

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

def create_tables():
    from .models import User, Project, Task
    Base.metadata.create_all(bind=engine)
