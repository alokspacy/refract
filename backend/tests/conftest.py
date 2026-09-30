import os
import sys

# Ensure backend root and project root are in sys.path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")))
sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))

import shutil
import tempfile
import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from unittest.mock import MagicMock
from app.core.config import settings
from app.core.dependencies import get_db, get_storage
from app.core.security import create_access_token, hash_password
from app.db.database import Base
from app.main import app as fastapi_app
from app.models.user import User
from app.storage.local import LocalStorageProvider
import app.workers.tasks as worker_tasks

# Use in-memory SQLite database for testing
TEST_DATABASE_URL = "sqlite:///:memory:"
test_engine = create_engine(
    TEST_DATABASE_URL,
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=test_engine)


@pytest.fixture(autouse=True)
def mock_celery_task(monkeypatch):
    """Mock Celery task dispatch so tests run instantly without external brokers."""
    mock_dispatch = MagicMock(return_value=MagicMock(id="mock-task-id"))
    monkeypatch.setattr(worker_tasks.process_document_job, "delay", mock_dispatch)
    monkeypatch.setattr(worker_tasks.process_document_job, "apply_async", mock_dispatch)
    monkeypatch.setattr(worker_tasks.analyze_document_job, "delay", mock_dispatch)
    monkeypatch.setattr(worker_tasks.analyze_document_job, "apply_async", mock_dispatch)
    monkeypatch.setattr(worker_tasks.generate_variant_job, "delay", mock_dispatch)
    monkeypatch.setattr(worker_tasks.generate_variant_job, "apply_async", mock_dispatch)
    yield mock_dispatch


@pytest.fixture(scope="session", autouse=True)
def setup_test_db():
    Base.metadata.create_all(bind=test_engine)
    yield
    Base.metadata.drop_all(bind=test_engine)


@pytest.fixture
def db_session():
    connection = test_engine.connect()
    transaction = connection.begin()
    session = TestingSessionLocal(bind=connection)

    yield session

    session.close()
    transaction.rollback()
    connection.close()


@pytest.fixture
def temp_storage():
    temp_dir = tempfile.mkdtemp()
    provider = LocalStorageProvider(base_path=temp_dir)
    yield provider
    shutil.rmtree(temp_dir, ignore_errors=True)


@pytest.fixture
def client(db_session, temp_storage):
    def override_get_db():
        try:
            yield db_session
        finally:
            pass

    def override_get_storage():
        return temp_storage

    fastapi_app.dependency_overrides[get_db] = override_get_db
    fastapi_app.dependency_overrides[get_storage] = override_get_storage

    with TestClient(fastapi_app) as test_client:
        yield test_client

    fastapi_app.dependency_overrides.clear()


@pytest.fixture
def test_user(db_session) -> User:
    user = User(
        email="teacher1@school.edu",
        password_hash=hash_password("TeacherSecurePass123!"),
        name="Teacher Jane",
        role="teacher",
        is_active=True
    )
    db_session.add(user)
    db_session.commit()
    db_session.refresh(user)
    return user


@pytest.fixture
def test_user_token(test_user: User) -> str:
    return create_access_token(
        subject=test_user.id,
        extra_claims={"email": test_user.email, "role": test_user.role}
    )


@pytest.fixture
def auth_headers(test_user_token: str):
    return {"Authorization": f"Bearer {test_user_token}"}


@pytest.fixture
def another_user(db_session) -> User:
    user = User(
        email="teacher2@school.edu",
        password_hash=hash_password("AnotherPass123!"),
        name="Teacher Bob",
        role="teacher",
        is_active=True
    )
    db_session.add(user)
    db_session.commit()
    db_session.refresh(user)
    return user


@pytest.fixture
def another_auth_headers(another_user: User):
    token = create_access_token(
        subject=another_user.id,
        extra_claims={"email": another_user.email, "role": another_user.role}
    )
    return {"Authorization": f"Bearer {token}"}
