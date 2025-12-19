from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# We use SQLite for this assignment as it requires no extra installation.
# In a real production app (like CredResolve), we would switch this URL to PostgreSQL.
SQLALCHEMY_DATABASE_URL = "sqlite:///./expenses.db"

# Create the engine that manages the connection
engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)

# Create a Session factory
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# The base class for our models
Base = declarative_base()

# Dependency: This helper function gives us a database session when we need it,
# and closes it automatically when we are done.
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()