import os
from dotenv import load_dotenv
from sqlalchemy import create_engine, text
from models import Base
from sqlalchemy.orm import sessionmaker

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")
print("DATABASE_URL:", DATABASE_URL)

engine = create_engine(DATABASE_URL)

def test_connection():
    with engine.connect() as connection:
        result = connection.execute(text("SELECT 1"))
        print("Conexión OK:", result.scalar())

def create_tables():
    Base.metadata.create_all(bind=engine)
    print("Tablas creadas")

SessionLocal = sessionmaker(bind=engine)