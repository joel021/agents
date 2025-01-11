import pytest

import mongomock
from mongoengine import connect

from agents.__main__ import app
from agents.db.status import Status

@pytest.fixture
def client():
    app.testing = True
    with app.test_client() as client:
        yield client

@pytest.fixture(scope="module")
def before_all():

    connect('mongoenginetest', host='mongodb://localhost', mongo_client_class=mongomock.MongoClient)
    yield
    #tear down

def test_epic_controller(client, before_all):
    payload = {
        "title": "Epic Test",
        "status": str(Status.TODO),
        "description": "Description",
        "summary": "Description",
        "stories": []
    }
    response = client.post('/epic', json=payload)
    assert response.status_code == 201
    data = response.get_json()
    assert data["title"] == payload["title"]
    assert data["description"] == payload["description"]
