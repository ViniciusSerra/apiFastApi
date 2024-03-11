from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

DB_CONNECTION_STRING = 'mysql+pymysql://user:password@127.0.0.1:3306/anyForm'

engine = create_engine(
    DB_CONNECTION_STRING,pool_pre_ping=True
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()