from fastapi.testclient import TestClient


def test_user_registration(client: TestClient):
    payload = {
        "email": "newteacher@school.edu",
        "password": "Password123!",
        "name": "New Teacher",
        "role": "teacher"
    }
    response = client.post("/auth/register", json=payload)
    assert response.status_code == 201
    data = response.json()
    assert "access_token" in data
    assert data["token_type"] == "bearer"
    assert data["user"]["email"] == "newteacher@school.edu"
    assert data["user"]["name"] == "New Teacher"
    assert data["user"]["role"] == "teacher"


def test_duplicate_email_registration_fails(client: TestClient, test_user):
    payload = {
        "email": test_user.email,
        "password": "SomeOtherPassword123!",
        "name": "Duplicate User",
        "role": "teacher"
    }
    response = client.post("/auth/register", json=payload)
    assert response.status_code == 400
    data = response.json()
    assert data["error"]["code"] == "EMAIL_ALREADY_EXISTS"


def test_user_login_success(client: TestClient, test_user):
    payload = {
        "email": "teacher1@school.edu",
        "password": "TeacherSecurePass123!"
    }
    response = client.post("/auth/login", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert "access_token" in data
    assert data["user"]["id"] == test_user.id


def test_user_login_invalid_password_fails(client: TestClient, test_user):
    payload = {
        "email": "teacher1@school.edu",
        "password": "WrongPassword!"
    }
    response = client.post("/auth/login", json=payload)
    assert response.status_code == 401
    data = response.json()
    assert data["error"]["code"] == "INVALID_CREDENTIALS"


def test_get_current_user_me(client: TestClient, test_user, auth_headers):
    response = client.get("/auth/me", headers=auth_headers)
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == test_user.id
    assert data["email"] == test_user.email


def test_get_current_user_unauthorized(client: TestClient):
    response = client.get("/auth/me")
    assert response.status_code == 401
    data = response.json()
    assert data["error"]["code"] in ["UNAUTHORIZED", "INVALID_TOKEN"]
