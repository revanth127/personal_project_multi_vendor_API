import pytest
from fastapi.testclient import TestClient 
from app.main import app
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.database import get_db
from app.models import Base
from app.config import settings

sql_database_url =settings.DATABASE_URL_TEST

engine = create_engine(sql_database_url)
TestingSessionLocal = sessionmaker(autocommit=False,autoflush=False,bind=engine)


def ovveride_get_db():
    db=TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()

app.dependency_overrides[get_db] = ovveride_get_db

@pytest.fixture(scope='module')
def client():
    Base.metadata.create_all(bind=engine)
    yield TestClient(app)
    Base.metadata.drop_all(bind=engine)