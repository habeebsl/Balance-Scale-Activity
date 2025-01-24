from sqlalchemy import create_engine, StaticPool
from sqlalchemy.orm import sessionmaker
from database import Base

TEST_DATABASE_URL = "sqlite:///:memory:"

test_engine = create_engine(
    TEST_DATABASE_URL, 
    connect_args={"check_same_thread": False},
    poolclass=StaticPool 
)

TestingSessionLocal = sessionmaker(
    autocommit=False, 
    autoflush=False, 
    bind=test_engine,
    expire_on_commit=False
)

def override_get_db():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()