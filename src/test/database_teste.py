from sqlalchemy import create_engine
from src.config.database import DB_CONNECTION_STRING
from loguru import logger


def test_database_connection():
    try:
        # Create a SQLAlchemy engine to establish a connection to the database
        engine = create_engine(DB_CONNECTION_STRING)

        # Attempt to connect to the database
        with engine.connect() as connection:
            # Check if the connection is alive
            if connection:
                logger.info("Database connection successful!")
            else:
                logger.error("Database connection failed!")
        return True
    except Exception as e:
        logger.error(f"Error connecting to database: {e}")
        return False

