"""Testing Registration Routes"""
import pytest

from application.database import User
from application import init_app, db

@pytest.fixture(name="app")
def create_app():
    """create a new test app"""
    new_app = init_app()
    new_app.config.update({
        "TESTING": True,
        "WTF_CSRF_ENABLED": False
    })

    with new_app.app_context():
        db.session.remove()
        db.drop_all()
        db.create_all()
        yield new_app
        db.session.remove()
        db.drop_all()


@pytest.fixture(name="client")
def create_client(app):
    """initialize a fixture test client for flask unit testing"""
    return app.test_client()


def test_user_invalid_login(client):
    """test invalid user login"""
    response = client.post("/login", data={
        "email": "steve@123.com",
        "password": "123456",
    }, follow_redirects=True)

    assert response.request.path == "/login"
    assert response.status_code == 200
    assert b"User Not Found" in response.data
    assert b"Login" in response.data


def test_user_login(client, app):
    """test valid login"""
    with app.app_context():
        user = User.create('steve@123.com', '123456')
        db.session.add(user)  # pylint: disable=no-member
        db.session.commit()  # pylint: disable=no-member

    response = client.post("/login", data={
        "email": "steve@123.com",
        "password": "123456",
    }, follow_redirects=True)

    assert response.request.path == "/dashboard"
    assert response.status_code == 200
    assert b"Welcome" in response.data
    assert b"Your user ID is" in response.data


def test_user_invalid_passwd(client, app):
    """test invalid passwd"""
    with app.app_context():
        user = User.create('steve@123.com', '123456')
        db.session.add(user)  # pylint: disable=no-member
        db.session.commit()  # pylint: disable=no-member

    response = client.post("/login", data={
        "email": "steve@123.com",
        "password": "2345",
    }, follow_redirects=True)

    assert response.request.path == "/login"
    assert response.status_code == 200
    assert b"Password Incorrect" in response.data
    assert b"Login" in response.data


def test_user_logout(client, app):
    """test login then logout"""
    with app.app_context():
        user = User.create('steve@123.com', '123456')
        db.session.add(user)  # pylint: disable=no-member
        db.session.commit()  # pylint: disable=no-member

    response = client.post("/login", data={
        "email": "steve@123.com",
        "password": "123456",
    }, follow_redirects=True)
    assert response.request.path == "/dashboard"
    assert response.status_code == 200
    assert b"Welcome" in response.data
    assert b"Your user ID is" in response.data

    response = client.get("/logout", follow_redirects=True)
    assert response.request.path == "/"
    assert response.status_code == 200
    assert b"Login" in response.data
    assert b"Register" in response.data


def test_user_access_no_credential(client):
    """test access without credential"""
    response = client.get("/dashboard", follow_redirects=True)
    assert response.request.path == "/login"
    assert response.status_code == 200
    assert b"Login" in response.data
    assert b"Register" in response.data
