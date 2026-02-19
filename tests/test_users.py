import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.main import app
from app.db.database import Base, get_db

SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread": False},
)

TestingSessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine,
)

from app.db.models import User

Base.metadata.create_all(bind=engine)


def override_get_db():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()


app.dependency_overrides[get_db] = override_get_db

client = TestClient(app)

def test_create_user_success():
    response = client.post(
        "/users/",
        json={
            "username": "testuser",
            "email": "test@example.com",
            "first_name": "Test",
            "last_name": "User",
            "role": "admin",
            "active": True
        },
    )

    assert response.status_code == 201
    data = response.json()
    assert data["username"] == "testuser"
    assert data["email"] == "test@example.com"

def test_create_user_duplicate_username():
    client.post(
        "/users/",
        json={
            "username": "duplicate",
            "email": "dup1@example.com",
            "first_name": "Dup",
            "last_name": "User",
            "role": "admin",
            "active": True
        },
    )

    response = client.post(
        "/users/",
        json={
            "username": "duplicate",
            "email": "dup2@example.com",
            "first_name": "Dup",
            "last_name": "User",
            "role": "admin",
            "active": True
        },
    )

    assert response.status_code == 409

def test_get_user_by_id():
    create_response = client.post(
        "/users/",
        json={
            "username": "getuser",
            "email": "get@example.com",
            "first_name": "Get",
            "last_name": "User",
            "role": "user",
            "active": True
        },
    )

    user_id = create_response.json()["id"]

    response = client.get(f"/users/{user_id}")

    assert response.status_code == 200
    assert response.json()["id"] == user_id

def test_patch_user():
    create_response = client.post(
        "/users/",
        json={
            "username": "patchuser",
            "email": "patch@example.com",
            "first_name": "Patch",
            "last_name": "User",
            "role": "user",
            "active": True
        },
    )

    user_id = create_response.json()["id"]

    response = client.patch(
        f"/users/{user_id}",
        json={"first_name": "Updated"}
    )

    assert response.status_code == 200
    assert response.json()["first_name"] == "Updated"

def test_delete_user():
    create_response = client.post(
        "/users/",
        json={
            "username": "deleteuser",
            "email": "delete@example.com",
            "first_name": "Delete",
            "last_name": "User",
            "role": "user",
            "active": True
        },
    )

    user_id = create_response.json()["id"]

    response = client.delete(f"/users/{user_id}")

    assert response.status_code == 204

def test_create_user_invalid_role(client):

    response = client.post(
        "/users/",
        json={
            "username": "invalidrole",
            "email": "invalid@latam.com",
            "role": "superadmin"  # rol inválido
        }
    )

    assert response.status_code == 422

def test_create_user_invalid_email(client):

    response = client.post(
        "/users/",
        json={
            "username": "bademail",
            "email": "not-an-email",
            "role": "admin"
        }
    )

    assert response.status_code == 422

def test_get_user_not_found(client):

    response = client.get("/users/9999")

    assert response.status_code == 404


def test_list_users(client):

    # Crear usuario
    client.post(
        "/users/",
        json={
            "username": "listuser",
            "email": "list@latam.com",
            "role": "admin"
        }
    )

    response = client.get("/users/")

    assert response.status_code == 200
    assert isinstance(response.json(), list)
    assert len(response.json()) >= 1


import os

@pytest.fixture(scope="session", autouse=True)
def cleanup():
    yield
    if os.path.exists("test.db"):
        os.remove("test.db")

