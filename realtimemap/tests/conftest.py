import pytest
from fastapi.testclient import TestClient

from database.helper import db_helper
from main import app
from models import BaseSqlModel


@pytest.fixture(scope="session", autouse=True)
def setup_db():
    BaseSqlModel.metadata.drop_all(bind=db_helper.sync_engine)
    BaseSqlModel.metadata.create_all(bind=db_helper.sync_engine)


@pytest.fixture
def client():
    with TestClient(app=app) as client:
        yield client
