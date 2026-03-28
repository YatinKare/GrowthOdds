from typing import Generator
from sqlmodel import create_engine, Session, SQLModel
from .models import CompanyInfo, Experiment
import os

# Database file location
# Assuming the file is named database.db in the backend/db folder
DB_PATH = "db/database.db"
sqlite_url = f"sqlite:///{DB_PATH}"

# For SQLite, we set check_same_thread to False
engine = create_engine(sqlite_url, connect_args={"check_same_thread": False})

def create_db_and_tables():
    SQLModel.metadata.create_all(engine)

def get_db() -> Generator[Session, None, None]:
    with Session(engine) as session:
        yield session
