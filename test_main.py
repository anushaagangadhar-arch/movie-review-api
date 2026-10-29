from fastapi.testclient import TestClient
from main import app 
import uuid

client = TestClient(app)


def test_homepage():
    response = client.get("/")

    assert response.status_code == 200
def test_get_movies():
    response = client.get("/movies")

    assert response.status_code == 200
    assert isinstance(response.json(), list)

def test_get_movie_by_id():
    response = client.get("/movies/3")

    assert response.status_code == 200
    assert response.json()["id"] == 3

def test_get_movie_not_found():
    response = client.get("/movies/999999")

    assert response.status_code == 404
def test_create_movie():
    movie_data = {
        "title": "Automated Test Movie October 24",
        "year": 2025,
        "genre": "Drama"
    }

    response = client.post("/movies", json=movie_data)

    if response.status_code == 409:
        # This movie already exists from an earlier run.
        existing = client.get(
            "/movies/search",
            params={"title": movie_data["title"]}
        )
        assert existing.status_code == 200
        assert any(
            movie["title"] == movie_data["title"]
            and movie["year"] == movie_data["year"]
            for movie in existing.json()
        )
    else:
        assert response.status_code == 201
        assert response.json()["title"] == movie_data["title"]
        assert response.json()["year"] == 2025
        assert response.json()["genre"] == "Drama"
        assert "id" in response.json()

def test_duplicate_movie():
    movie_data = {
        "title": "Automated Test Movie October 24",
        "year": 2025,
        "genre": "Drama"
    }

    first_response = client.post("/movies", json=movie_data)
    assert first_response.status_code in (201, 409)

    second_response = client.post("/movies", json=movie_data)
    assert second_response.status_code == 409

def test_create_movie_invalid_year():
    movie_data = {
        "title": "Invalid Year Test",
        "year": 1800,
        "genre": "Drama"
    }

    response = client.post("/movies", json=movie_data)

    assert response.status_code == 422

def test_create_movie_blank_title():
    movie_data = {
        "title": "   ",
        "year": 2025,
        "genre": "Drama"
    }

    response = client.post("/movies", json=movie_data)

    assert response.status_code == 422
def test_create_movie_blank_genre():
    movie_data = {
        "title": "Blank Genre Test",
        "year": 2025,
        "genre": "   "
    }

    response = client.post("/movies", json=movie_data)

    assert response.status_code == 422
def test_create_review_invalid_rating():
    review_data = {
        "movie_id": 3,
        "rating": 11,
        "comment": "A great movie"
    }

    response = client.post("/reviews", json=review_data)

    assert response.status_code == 422
def test_create_review_zero_rating():
    review_data = {
        "movie_id": 3,
        "rating": 0,
        "comment": "A good movie"
    }

    response = client.post("/reviews", json=review_data)

    assert response.status_code == 422
def test_create_review_movie_not_found():
    review_data = {
        "movie_id": 999999,
        "rating": 8,
        "comment": "A good movie"
    }

    response = client.post("/reviews", json=review_data)

    assert response.status_code == 404
def test_get_review_not_found():
    response = client.get("/reviews/999999")

    assert response.status_code == 404
def test_create_review_blank_comment():
    review_data = {
        "movie_id": 3,
        "rating": 8,
        "comment": ""
    }

    response = client.post("/reviews", json=review_data)

    assert response.status_code == 422
def test_create_review():
    review_data = {
        "movie_id": 3,
        "rating": 8,
        "comment": "A very good movie"
    }

    response = client.post("/reviews", json=review_data)

    assert response.status_code == 201
    assert response.json()["movie_id"] == 3
    assert response.json()["rating"] == 8
    assert response.json()["comment"] == "A very good movie"
    assert "id" in response.json()
def test_update_review():
    review_data = {
        "movie_id": 3,
        "rating": 9,
        "comment": "Updated review comment"
    }

    create_response = client.post("/reviews", json=review_data)
    assert create_response.status_code == 201

    review_id = create_response.json()["id"]

    updated_data = {
        "movie_id": 3,
        "rating": 7,
        "comment": "This review has been updated"
    }

    response = client.put(
        f"/reviews/{review_id}",
        json=updated_data
    )

    assert response.status_code == 200
    assert response.json()["rating"] == 7
    assert response.json()["comment"] == "This review has been updated"
def test_delete_review():
    review_data = {
        "movie_id": 3,
        "rating": 8,
        "comment": "Review to be deleted"
    }

    create_response = client.post("/reviews", json=review_data)
    assert create_response.status_code == 201

    review_id = create_response.json()["id"]

    delete_response = client.delete(f"/reviews/{review_id}")
    assert delete_response.status_code == 200

    get_response = client.get(f"/reviews/{review_id}")
    assert get_response.status_code == 404
def test_create_review_comment_too_long():
    review_data = {
        "movie_id": 3,
        "rating": 8,
        "comment": "A" * 501
    }

    response = client.post("/reviews", json=review_data)

    assert response.status_code == 422
def test_create_review_whitespace_comment():
    review_data = {
        "movie_id": 3,
        "rating": 8,
        "comment": "   "
    }

    response = client.post("/reviews", json=review_data)

    assert response.status_code == 422
def test_create_movie_whitespace_title():
    movie_data = {
        "title": "   ",
        "year": 2025,
        "genre": "Drama"
    }

    response = client.post("/movies", json=movie_data)

    assert response.status_code == 422
def test_create_movie_whitespace_genre():
    movie_data = {
        "title": "Valid Test Movie",
        "year": 2025,
        "genre": "   "
    }

    response = client.post("/movies", json=movie_data)

    assert response.status_code == 422
def test_create_review_max_rating():
    review_data = {
        "movie_id": 3,
        "rating": 10,
        "comment": "Excellent movie"
    }

    response = client.post("/reviews", json=review_data)

    assert response.status_code == 201
    assert response.json()["rating"] == 10
def test_create_review_min_rating():
    review_data = {
        "movie_id": 3,
        "rating": 1,
        "comment": "Not a good movie"
    }

    response = client.post("/reviews", json=review_data)

    assert response.status_code == 201
    assert response.json()["rating"] == 1
def test_create_movie_invalid_future_year():
    movie_data = {
        "title": "Future Movie Test",
        "year": 2101,
        "genre": "Drama"
    }

    response = client.post("/movies", json=movie_data)

    assert response.status_code == 422
def test_create_movie_invalid_past_year():
    movie_data = {
        "title": "Ancient Movie Test",
        "year": 1887,
        "genre": "Drama"
    }

    response = client.post("/movies", json=movie_data)

    assert response.status_code == 422
def test_create_movie_short_title():
    movie_data = {
        "title": "A",
        "year": 2025,
        "genre": "Drama"
    }

    response = client.post("/movies", json=movie_data)

    assert response.status_code == 422
def test_create_movie_short_genre():
    movie_data = {
        "title": "Short Genre Test",
        "year": 2025,
        "genre": "A"
    }

    response = client.post("/movies", json=movie_data)

    assert response.status_code == 422
def test_create_review_invalid_movie_id():
    review_data = {
        "movie_id": 0,
        "rating": 8,
        "comment": "A good movie"
    }

    response = client.post("/reviews", json=review_data)

    assert response.status_code == 422
def test_create_review_negative_movie_id():
    review_data = {
        "movie_id": -1,
        "rating": 8,
        "comment": "A good movie"
    }

    response = client.post("/reviews", json=review_data)

    assert response.status_code == 422
def test_create_review_max_comment_length():
    review_data = {
        "movie_id": 3,
        "rating": 8,
        "comment": "A" * 500
    }

    response = client.post("/reviews", json=review_data)

    assert response.status_code == 201
    assert len(response.json()["comment"]) == 500
def test_create_review_missing_comment():
    review_data = {
        "movie_id": 3,
        "rating": 8
    }

    response = client.post("/reviews", json=review_data)

    assert response.status_code == 422
def test_create_review_missing_rating():
    review_data = {
        "movie_id": 3,
        "comment": "A good movie"
    }

    response = client.post("/reviews", json=review_data)

    assert response.status_code == 422
def test_create_review_missing_movie_id():
    review_data = {
        "rating": 8,
        "comment": "A good movie"
    }

    response = client.post("/reviews", json=review_data)

    assert response.status_code == 422
def test_update_review_missing_comment():
    review_data = {
        "movie_id": 3,
        "rating": 8,
        "comment": "Original review"
    }

    create_response = client.post("/reviews", json=review_data)
    assert create_response.status_code == 201

    review_id = create_response.json()["id"]

    updated_data = {
        "movie_id": 3,
        "rating": 9
    }

    response = client.put(
        f"/reviews/{review_id}",
        json=updated_data
    )

    assert response.status_code == 422
def test_update_review_invalid_rating():
    review_data = {
        "movie_id": 3,
        "rating": 8,
        "comment": "Original review"
    }

    create_response = client.post("/reviews", json=review_data)
    assert create_response.status_code == 201

    review_id = create_response.json()["id"]

    updated_data = {
        "movie_id": 3,
        "rating": 11,
        "comment": "Updated review"
    }

    response = client.put(
        f"/reviews/{review_id}",
        json=updated_data
    )

    assert response.status_code == 422
def test_update_review_zero_rating():
    review_data = {
        "movie_id": 3,
        "rating": 8,
        "comment": "Original review"
    }

    create_response = client.post("/reviews", json=review_data)
    assert create_response.status_code == 201

    review_id = create_response.json()["id"]

    updated_data = {
        "movie_id": 3,
        "rating": 0,
        "comment": "Updated review"
    }

    response = client.put(
        f"/reviews/{review_id}",
        json=updated_data
    )

    assert response.status_code == 422
def test_update_review_whitespace_comment():
    review_data = {
        "movie_id": 3,
        "rating": 8,
        "comment": "Original review"
    }

    create_response = client.post("/reviews", json=review_data)
    assert create_response.status_code == 201

    review_id = create_response.json()["id"]

    updated_data = {
        "movie_id": 3,
        "rating": 8,
        "comment": "   "
    }

    response = client.put(
        f"/reviews/{review_id}",
        json=updated_data
    )

    assert response.status_code == 422
def test_update_review_missing_rating():
    review_data = {
        "movie_id": 3,
        "rating": 8,
        "comment": "Original review"
    }
    create_response = client.post("/reviews", json=review_data)
    assert create_response.status_code == 201
    review_id = create_response.json()["id"]

    updated_data = {
        "movie_id": 3,
        "comment": "Updated review"
    }
    response = client.put(f"/reviews/{review_id}", json=updated_data)
    assert response.status_code == 422
def test_update_review_not_found():
    updated_data = {
        "movie_id": 3,
        "rating": 8,
        "comment": "Updated review"
    }

    response = client.put("/reviews/999999", json=updated_data)
    assert response.status_code == 404
def test_update_review_min_rating():
    review_data = {
        "movie_id": 3,
        "rating": 8,
        "comment": "Original review"
    }
    create_response = client.post("/reviews", json=review_data)
    assert create_response.status_code == 201
    review_id = create_response.json()["id"]

    updated_data = {
        "movie_id": 3,
        "rating": 1,
        "comment": "Updated review"
    }
    response = client.put(f"/reviews/{review_id}", json=updated_data)
    assert response.status_code == 200
    assert response.json()["rating"] == 1
def test_update_review_max_rating():
    review_data = {
        "movie_id": 3,
        "rating": 8,
        "comment": "Original review"
    }
    create_response = client.post("/reviews", json=review_data)
    assert create_response.status_code == 201
    review_id = create_response.json()["id"]

    updated_data = {
        "movie_id": 3,
        "rating": 10,
        "comment": "Updated review"
    }
    response = client.put(f"/reviews/{review_id}", json=updated_data)
    assert response.status_code == 200
    assert response.json()["rating"] == 10
def test_update_review_comment_too_long():
    review_data = {
        "movie_id": 3,
        "rating": 8,
        "comment": "Original review"
    }
    create_response = client.post("/reviews", json=review_data)
    assert create_response.status_code == 201
    review_id = create_response.json()["id"]

    updated_data = {
        "movie_id": 3,
        "rating": 8,
        "comment": "A" * 501
    }
    response = client.put(f"/reviews/{review_id}", json=updated_data)
    assert response.status_code == 422
def test_update_review_negative_rating():
    review_data = {
        "movie_id": 3,
        "rating": 8,
        "comment": "Original review"
    }
    create_response = client.post("/reviews", json=review_data)
    assert create_response.status_code == 201
    review_id = create_response.json()["id"]

    updated_data = {
        "movie_id": 3,
        "rating": -1,
        "comment": "Updated review"
    }
    response = client.put(f"/reviews/{review_id}", json=updated_data)
    assert response.status_code == 422
def test_update_review_missing_movie_id():
    review_data = {
        "movie_id": 3,
        "rating": 8,
        "comment": "Original review"
    }
    create_response = client.post("/reviews", json=review_data)
    assert create_response.status_code == 201
    review_id = create_response.json()["id"]

    updated_data = {
        "rating": 8,
        "comment": "Updated review"
    }
    response = client.put(f"/reviews/{review_id}", json=updated_data)
    assert response.status_code == 422
def test_update_review_invalid_movie_id():
    review_data = {
        "movie_id": 3,
        "rating": 8,
        "comment": "Original review"
    }
    create_response = client.post("/reviews", json=review_data)
    assert create_response.status_code == 201
    review_id = create_response.json()["id"]

    updated_data = {
        "movie_id": 0,
        "rating": 8,
        "comment": "Updated review"
    }
    response = client.put(f"/reviews/{review_id}", json=updated_data)
    assert response.status_code == 422
def test_delete_review_not_found():
    response = client.delete("/reviews/999999")
    assert response.status_code == 404
def test_delete_review_then_get():
    review_data = {
        "movie_id": 3,
        "rating": 8,
        "comment": "Review to delete"
    }
    create_response = client.post("/reviews", json=review_data)
    assert create_response.status_code == 201
    review_id = create_response.json()["id"]

    delete_response = client.delete(f"/reviews/{review_id}")
    assert delete_response.status_code == 200

    get_response = client.get(f"/reviews/{review_id}")
    assert get_response.status_code == 404
def test_delete_review_twice():
    review_data = {
        "movie_id": 3,
        "rating": 7,
        "comment": "Review to delete twice"
    }
    create_response = client.post("/reviews", json=review_data)
    assert create_response.status_code == 201
    review_id = create_response.json()["id"]

    first_response = client.delete(f"/reviews/{review_id}")
    assert first_response.status_code == 200

    second_response = client.delete(f"/reviews/{review_id}")
    assert second_response.status_code == 404
def test_delete_movie_not_found():
    response = client.delete("/movies/999999")
    assert response.status_code == 404
def test_delete_movie_then_get():
    movie_data = {
        "title": "Movie To Delete",
        "year": 2020,
        "genre": "Drama"
    }
    create_response = client.post("/movies", json=movie_data)
    assert create_response.status_code == 201
    movie_id = create_response.json()["id"]

    delete_response = client.delete(f"/movies/{movie_id}")
    assert delete_response.status_code == 200

    get_response = client.get(f"/movies/{movie_id}")
    assert get_response.status_code == 404
def test_delete_movie_twice():
    movie_data = {
        "title": f"Update Test{uuid.uuid4().hex[:8]}",
        "year": 2026,
        "genre": "Drama"
    }
    create_response = client.post("/movies", json=movie_data)
    assert create_response.status_code == 201
    movie_id = create_response.json()["id"]

    first_response = client.delete(f"/movies/{movie_id}")
    assert first_response.status_code == 200

    second_response = client.delete(f"/movies/{movie_id}")
    assert second_response.status_code == 404
def test_update_movie():
    movie_data = {
        "title": f"update test {uuid.uuid4().hex[:8]}",
        "year": 2026,
        "genre": "Drama"
    }
    create_response = client.post("/movies", json=movie_data)
    print("CREATE STATUS:", create_response.status_code)
    print("CREATE RESPONSE:", create_response.text)
    assert create_response.status_code == 201
    movie_id = create_response.json()["id"]

    updated_data = {
        "title": f"Updated Movie {uuid.uuid4().hex[:8]}",
        "year": 2022,
        "genre": "Comedy"
    }
    response = client.put(f"/movies/{movie_id}", json=updated_data)
    print("UPDATE STATUS:",response.status_code)
    print("UPDATE BODY:",response.json())

    assert response.status_code == 200
    assert response.json()["title"] == updated_data["title"]
    assert response.json()["year"] == 2022
    assert response.json()["genre"] == "Comedy"
def test_update_movie_not_found():
    updated_data = {
        "title": "Updated Movie",
        "year": 2022,
        "genre": "Comedy"
    }
    response = client.put("/movies/999999", json=updated_data)
    assert response.status_code == 404
def test_update_movie_invalid_year():
    movie_data = {
        "title": f"invalid year test {uuid.uuid4().hex[:8]}",
        "year": 2020,
        "genre": "Drama"
    }
    create_response = client.post("/movies", json=movie_data)
    assert create_response.status_code == 201
    movie_id = create_response.json()["id"]

    updated_data = {
        "title": "Updated Movie",
        "year": 2200,
        "genre": "Comedy"
    }
    response = client.put(f"/movies/{movie_id}", json=updated_data)
    assert response.status_code == 422
def test_update_movie_blank_title():
    movie_data = {
        "title": f"blank genre test {uuid.uuid4().hex[:8]}",
        "year": 2025,
        "genre": "Drama"
    }
    create_response = client.post("/movies", json=movie_data)
    assert create_response.status_code == 201
    movie_id = create_response.json()["id"]

    updated_data = {
        "title": "   ",
        "year": 2022,
        "genre": "Comedy"
    }
    response = client.put(f"/movies/{movie_id}", json=updated_data)
    assert response.status_code == 422
def test_update_movie_blank_genre():
    movie_data = {
        "title": f"blank genre test {uuid.uuid4().hex[:8]}",
        "year": 2020,
        "genre": "Drama"
    }
    create_response = client.post("/movies", json=movie_data)
    assert create_response.status_code == 201
    movie_id = create_response.json()["id"]

    updated_data = {
        "title": f"Updated Movie {uuid.uuid4().hex[:8]}",
        "year": 2022,
        "genre": ""
    }
    response = client.put(f"/movies/{movie_id}", json=updated_data)
    assert response.status_code == 422
def test_update_movie_short_title():
    movie_data = {
        "title": f"short title test {uuid.uuid4().hex[:8]}",
        "year": 2024,
        "genre": "Drama"
    }
    create_response = client.post("/movies", json=movie_data)
    assert create_response.status_code == 201
    movie_id = create_response.json()["id"]

    updated_data = {
        "title": "A",
        "year": 2022,
        "genre": "Comedy"
    }
    response = client.put(f"/movies/{movie_id}", json=updated_data)
    assert response.status_code == 422
    assert "detail" in response.json()
