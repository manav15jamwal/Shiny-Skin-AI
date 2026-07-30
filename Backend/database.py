from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker,declarative_base
from dotenv import load_dotenv
import os
load_dotenv()

DB = os.getenv("DB_URL")

engine = create_engine(url=DB,connect_args={"check_same_thread":False})

SessionLocal = sessionmaker(
    autoflush=False,
    autocommit = False,
    bind = engine
)

def get_db():
    db = SessionLocal()
    
    try:
        yield db
    finally:
        db.close

Base = declarative_base()