from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import Base
from os import getenv
from dotenv import load_dotenv

load_dotenv('.env')
DATABASE_URL = getenv('DATABASE_URL')

engine = create_engine(
    DATABASE_URL,
    echo=False,
    pool_size=10,
    max_overflow=20,
    pool_pre_ping=True
)

Base.metadata.drop_all(bind=engine)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def create_tables():
    Base.metadata.create_all(bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
