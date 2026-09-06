import pytest
from fastapi.testclient import TestClient
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from src.api.core.settings import settings
from src.api.core.database import Base
from src.api.main import app
from src.dependencies.database import get_db
import numpy as np

test_engine = create_engine(settings.test_database_url)

test_session_local = sessionmaker(bind=test_engine, autoflush=False, autocommit=False)

def override_get_db():
    db = test_session_local()

    try:
        yield db

    finally:
        db.close()

class DummyModel():
    def predict(self, X):
        return np.array([1])
    def predict_proba(self, X):
        return np.array([[0.1, 0.9]])

@pytest.fixture
def client():

    Base.metadata.drop_all(bind=test_engine)
    Base.metadata.create_all(bind=test_engine)

    app.dependency_overrides[get_db] = override_get_db
    app.state.model = DummyModel

    yield TestClient(app)

    app.dependency_overrides.clear()

   
    