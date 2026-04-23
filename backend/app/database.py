from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker
from sqlalchemy.pool import NullPool
import os

DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://masroufi_dev:masroufi_dev_password@localhost:5432/masroufi_db")

engine = create_engine(
    DATABASE_URL,
    poolclass=NullPool if os.getenv("ENVIRONMENT") == "test" else None,
    echo=os.getenv("ENVIRONMENT") == "development"
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
