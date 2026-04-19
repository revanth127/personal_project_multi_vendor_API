import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.main import app
from app.database import get_db
from app.models import Base
from app.config import settings

engine = create_engine(
    settings.DATABASE_URL_TEST,
    connect_args={"check_same_thread": False}  # required for SQLite
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


@pytest.fixture(scope="session", autouse=True)
def setup_database():
    """Create tables once for the whole test session, drop after."""
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    yield
    Base.metadata.drop_all(bind=engine)


@pytest.fixture
def db_session():
    """Fresh, isolated DB session per test — rolls back after each test."""
    connection = engine.connect()
    transaction = connection.begin()
    db = TestingSessionLocal(bind=connection)

    yield db

    db.close()
    transaction.rollback()  # wipe all changes after each test
    connection.close()


@pytest.fixture
def client(db_session):
    """Test client wired to the isolated test DB session."""
    def override_get_db():
        yield db_session

    app.dependency_overrides[get_db] = override_get_db
    yield TestClient(app)
    app.dependency_overrides.clear() 