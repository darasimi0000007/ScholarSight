from sqlalchemy import create_engine
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv
import os

load_dotenv()

database_url = os.getenv("DATABASE_URL", "sqlite:///./StudentDetails.db").split(",")
database_url = database_url[0]


engine = create_engine(database_url, connect_args={"check_same_thread": False} if database_url.startswith("sqlite") else {})



SessionLocal = sessionmaker(bind=engine, autocommit=False, autoflush=False)

Base = declarative_base()


#calling the student details database
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()