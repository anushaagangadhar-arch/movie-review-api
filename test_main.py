from fastapi.testclient import TestClient
from main import app

client = TestClient(app)


def test_home():
    response = client.get("/")
    assert response.status_code == 200


def test_movies_requires_login():
    response = client.get("/movies")
    assert response.status_code == 401


def test_movie_not_found():
    response = client.get("/movies/999999")
    assert response.status_code == 404


def test_review_not_found():
    response = client.get("/reviews/999999")
    assert response.status_code == 404


def test_invalid_movie_data():
    response = client.post(
        "/movies",
        json={
            "title": "",
            "year": 2000,
            "genre": "Action"
        }
    )
    assert response.status_code in [401, 422]