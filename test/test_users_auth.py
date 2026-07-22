from pathlib import Path
import sys
from uuid import uuid4

from fastapi.testclient import TestClient

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

import crud.users as crud_users
import main
from crud.database import get_session
from models.users import UserInDB
from utils.security import create_access_token


def override_session():
    yield object()


def test_login_returns_bearer_token(monkeypatch):
    main.init_db = lambda: None
    main.app.dependency_overrides[get_session] = override_session

    user = UserInDB(id=uuid4(), email="user@example.com", password="hashed-password")
    monkeypatch.setattr(
        crud_users, "authenticate_user", lambda db, email, password: user
    )

    client = TestClient(main.app)
    response = client.post(
        "/login",
        data={"username": "user@example.com", "password": "secret"},
    )

    assert response.status_code == 200
    payload = response.json()
    assert payload["token_type"] == "bearer"
    assert payload["access_token"]


def test_me_returns_current_user(monkeypatch):
    main.init_db = lambda: None
    main.app.dependency_overrides[get_session] = override_session

    user = UserInDB(id=uuid4(), email="user@example.com", password="hashed-password")
    token = create_access_token({"sub": str(user.id)})
    monkeypatch.setattr(crud_users, "get_user_by_id", lambda db, user_id: user)

    client = TestClient(main.app)
    response = client.get(
        "/me",
        headers={"Authorization": f"Bearer {token}"},
    )

    assert response.status_code == 200
    assert response.json() == {"id": str(user.id), "email": "user@example.com"}
