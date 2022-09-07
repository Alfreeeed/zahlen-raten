import pytest
from app import app as create_app

@pytest.fixture()
def app():
    app = create_app
    app.config.update({
        "TESTING": True
    })

    yield app

@pytest.fixture()
def client(app):
    return app.test_client()

@pytest.fixture()
def runner(app):
    return app.test_cli_runner()

def test_create_user(client):
    response = client.get("/", data={
        "username": "Test User"
    })
    assert response.status_code == 200

def test_root_page(client):
    response = client.get("/")
    assert response.status_code == 200