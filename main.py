from fastapi import FastAPI,Depends, HTTPException, Query
from pydantic import BaseModel, ConfigDict, Field, field_validator
from sqlalchemy import func
from sqlalchemy.orm import Session

from database import Base,engine, SessionLocal
from database import get_db
from models import MovieDB, ReviewDB

app = FastAPI(title="Movie Review API")




# Request model: data sent by the user
class Movie(BaseModel):
    title: str = Field(min_length=2)
    year: int =Field(ge=1888, le=2100)
    genre: str =Field(min_length=2)

    @field_validator("title","genre")
    @classmethod
    def reject_blank_text(cls,value:str) -> str:
        value = value.strip()
        if not value:
            raise ValueError("this field cannot be empty")
        return value
    # Request model for reviews
class Review(BaseModel):
    movie_id: int = Field(gt=0)
    rating: int = Field(ge=1, le=10)
    comment: str = Field(min_length=1, max_length=500)

    @field_validator("comment")
    @classmethod
    def reject_blank_comment(cls, value: str) -> str:
        value = value.strip()
        if not value:
            raise ValueError("Comment cannot be empty")
        return value


# Response model: data returned by the API
class MovieResponse(Movie):
    id: int

    model_config = ConfigDict(from_attributes=True)


# Create and close database sessions
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# HOME
@app.get("/")
def home():
    return {"message": "Movie Review API is running!"}


# READ: Get all movies
@app.get("/movies", response_model=list[MovieResponse])
def get_movies(
    skip: int = Query(default=0, ge=0),
    limit: int =Query(default=10, ge=1, le=100),
    sort_order: str = Query(default="asc",pattern="^(asc|desc)$"),
    db: Session = Depends(get_db)
):
    query = db.query(MovieDB) 

    if sort_order =="desc":
        query = query.order_by(MovieDB.year.desc())
    else:
        query = query.order_by(MovieDB.year.asc())

    movies = query.offset(skip).limit(limit).all()

    return movies

    movies = (
        db.query(MovieDB)
        .order_by(MovieDB.id.asc())
        .offset(skip)
        .limit(limit)
        .all()
    )
    return movies
# Create a movie and prevent duplicates
@app.post("/movies", response_model=MovieResponse, status_code=201)
def create_movie(movie: Movie, db: Session = Depends(get_db)):
    existing_movie = (
        db.query(MovieDB)
        .filter(
            MovieDB.title.ilike(movie.title.strip()),
            MovieDB.year == movie.year
        )
        .first()
    )

    if existing_movie is not None:
        raise HTTPException(
            status_code=409,
            detail="This movie already exists"
        )

    new_movie = MovieDB(
        title=movie.title,
        year=movie.year,
        genre=movie.genre
    )

    db.add(new_movie)
    db.commit()
    db.refresh(new_movie)

    return new_movie
# Search movies by title
# Search movies by title with pagination and sorting
@app.get("/movies/search", response_model=list[MovieResponse])
def search_movies(
    title: str,
    skip: int = Query(default=0, ge=0),
    limit: int = Query(default=10, ge=1, le=100),
    sort_order: str = Query(default="asc", pattern="^(asc|desc)$"),
    db: Session = Depends(get_db)
):
    query = db.query(MovieDB).filter(
        MovieDB.title.ilike(f"%{title.strip()}%")
    )

    if sort_order == "desc":
        query = query.order_by(MovieDB.year.desc())
    else:
        query = query.order_by(MovieDB.year.asc())

    movies = query.offset(skip).limit(limit).all()

    return movies


# Filter movies by release year
# Filter movies by release year
@app.get("/movies/year/{year}", response_model=list[MovieResponse])
def get_movies_by_year(
    year: int,
    skip: int = Query(default=0, ge=0),
    limit: int = Query(default=10, ge=1, le=100),
    sort_order: str = Query(default="asc", pattern="^(asc|desc)$"),
    db: Session = Depends(get_db)
):
    query = db.query(MovieDB).filter(
        MovieDB.year == year
    )

    if sort_order == "desc":
        query = query.order_by(MovieDB.year.desc())
    else:
        query = query.order_by(MovieDB.year.asc())

    movies = query.offset(skip).limit(limit).all()

    return movies
# Filter movies by genre
@app.get("/movies/genre/{genre}", response_model=list[MovieResponse])
def get_movies_by_genre(genre: str, db: Session = Depends(get_db)):
    return (
        db.query(MovieDB)
        .filter(MovieDB.genre.ilike(genre.strip()))
        .order_by(MovieDB.id.asc())
        .all()
    )

# Get one movie by ID
@app.get("/movies/{movie_id}", response_model=MovieResponse)
def get_movie(movie_id: int, db: Session = Depends(get_db)):
    movie = (
        db.query(MovieDB)
        .filter(MovieDB.id == movie_id)
        .first()
    )

    if movie is None:
        raise HTTPException(
            status_code=404,
            detail=f"Movie with ID {movie_id} not found"
        )

    return movie

# Update a movie
@app.put("/movies/{movie_id}", response_model=MovieResponse)
def update_movie(
    movie_id: int,
    movie: Movie,
    db: Session = Depends(get_db)
):
    existing_movie = (
        db.query(MovieDB)
        .filter(MovieDB.id == movie_id)
        .first()
    )

    if existing_movie is None:
        raise HTTPException(
            status_code=404,
            detail=f"Movie with ID {movie_id} not found"
        )

    duplicate_movie = (
    db.query(MovieDB)
    .filter(
        MovieDB.title.ilike(movie.title.strip()),
        MovieDB.year == movie.year,
        MovieDB.id != movie_id
    )
    .first()
)

    if duplicate_movie is not None:
      raise HTTPException(
        status_code=409,
        detail="Another movie with this title and year already exists"
    )

    existing_movie.title = movie.title
    existing_movie.year = movie.year
    existing_movie.genre = movie.genre

    db.commit()
    db.refresh(existing_movie)

    return existing_movie


# Get movies by release year
@app.get("/movies/year/{year}", response_model=list[MovieResponse])
def get_movies_by_year(
    year: int,
    skip: int = Query(default=0, ge=0),
    limit: int = Query(default=10, ge=1, le=100),
    sort_order: str = Query(default="asc", pattern="^(asc|desc)$"),
    db: Session = Depends(get_db)
):
    query = db.query(MovieDB).filter(
        MovieDB.year == year
    )

    if sort_order == "desc":
        query = query.order_by(MovieDB.id.desc())
    else:
        query = query.order_by(MovieDB.id.asc())

    movies = query.offset(skip).limit(limit).all()

    return movies

# Get movies by genre
@app.get("/movies/genre/{genre}", response_model=list[MovieResponse])
def get_movies_by_genre(
    genre: str,
    skip: int = Query(default=0, ge=0),
    limit: int = Query(default=10, ge=1, le=100),
    sort_order: str = Query(default="asc", pattern="^(asc|desc)$"),
    db: Session = Depends(get_db)
):
    query = db.query(MovieDB).filter(
        MovieDB.genre.ilike(genre.strip())
    )

    if sort_order == "desc":
        query = query.order_by(MovieDB.year.desc())
    else:
        query = query.order_by(MovieDB.year.asc())

    movies = query.offset(skip).limit(limit).all()

    return movies


# READ: Get one movie by ID
@app.get("/movies/{movie_id}", response_model=MovieResponse)
def get_movie(movie_id: int, db: Session = Depends(get_db)):
    movie = (
        db.query(MovieDB)
        .filter(MovieDB.id == movie_id)
        .first()
    )

    if movie is None:
        raise HTTPException(
            status_code=404,
            detail="Movie not found"
        )

    return movie


# DELETE: Delete a movie
@app.delete("/movies/{movie_id}")
def delete_movie(movie_id: int, db: Session = Depends(get_db)):
    movie = (
        db.query(MovieDB)
        .filter(MovieDB.id == movie_id)
        .first()
    )

    if movie is None:
        raise HTTPException(
            status_code=404,
            detail="Movie not found"
        )
    existing_reviews = (
        db.query(ReviewDB)
        .filter(ReviewDB.movie_id == movie_id)
        .first()
    )

    if existing_reviews is not None:
        raise HTTPException(
            status_code=409,
            detail="Cannot delete this movie because it has existing reviews"
        )

    db.delete(movie)
    db.commit()

    return {"message": "Movie deleted successfully"}

# POST: Create a review
@app.post("/reviews",status_code=201)
def create_review(review: Review, db: Session = Depends(get_db)):
    movie = db.query(MovieDB).filter(
        MovieDB.id == review.movie_id
    ).first()

    if movie is None:
        raise HTTPException(
            status_code=404,
            detail="Movie not found"
        )

    new_review = ReviewDB(
        movie_id=review.movie_id,
        rating=review.rating,
        comment=review.comment
    )

    db.add(new_review)
    db.commit()
    db.refresh(new_review)

    return new_review
# GET: Retrieve all reviews
@app.get("/reviews")
def get_reviews(
    skip: int = Query(default=0, ge=0),
    limit: int = Query(default=10, ge=1, le=100),
    sort_order: str = Query(default="asc", pattern="^(asc|desc)$"),
    db: Session = Depends(get_db)
):
    query = db.query(ReviewDB)

    if sort_order == "desc":
        query = query.order_by(ReviewDB.id.desc())
    else:
        query = query.order_by(ReviewDB.id.asc())

    reviews = query.offset(skip).limit(limit).all()

    return reviews

# GET: Retrieve one review by ID
@app.get("/reviews/{review_id}")
def get_review(review_id: int, db: Session = Depends(get_db)):
    review = db.query(ReviewDB).filter(
        ReviewDB.id == review_id
    ).first()

    if review is None:
        raise HTTPException(
            status_code=404,
            detail="Review not found"
        )

    return review
# PUT: Update an existing review
@app.put("/reviews/{review_id}")
def update_review(
    review_id: int,
    review_data: Review,
    db: Session = Depends(get_db)
):
    review = db.query(ReviewDB).filter(
        ReviewDB.id == review_id
    ).first()

    if review is None:
        raise HTTPException(
            status_code=404,
            detail="Review not found"
        )

    movie = db.query(MovieDB).filter(
        MovieDB.id == review_data.movie_id
    ).first()

    if movie is None:
        raise HTTPException(
            status_code=404,
            detail="Movie not found"
        )

    review.movie_id = review_data.movie_id
    review.rating = review_data.rating
    review.comment = review_data.comment

    db.commit()
    db.refresh(review)

    return review

# DELETE: Delete a review
@app.delete("/reviews/{review_id}")
def delete_review(review_id: int, db: Session = Depends(get_db)):
    review = db.query(ReviewDB).filter(
        ReviewDB.id == review_id
    ).first()

    if review is None:
        raise HTTPException(
            status_code=404,
            detail="Review not found"
        )

    db.delete(review)
    db.commit()

    return {"message": "Review deleted successfully"}

from sqlalchemy import func

@app.get("/movies/{movie_id}/rating")
def get_movie_rating(
    movie_id: int,
    db: Session = Depends(get_db)
):
    # Check whether the movie exists
    movie = db.query(MovieDB).filter(
        MovieDB.id == movie_id
    ).first()

    if movie is None:
        raise HTTPException(
            status_code=404,
            detail="Movie not found"
        )

    # Calculate the average rating and number of reviews
    result = db.query(
        func.avg(ReviewDB.rating),
        func.count(ReviewDB.id)
    ).filter(
        ReviewDB.movie_id == movie_id
    ).first()

    average_rating = result[0]
    total_reviews = result[1]

    return {
        "movie_id": movie_id,
        "movie_title": movie.title,
        "average_rating": (
    f"{float(average_rating):.1f}"
    if average_rating is not None
    else None
),
        "total_reviews": total_reviews
    }

@app.get("/movies/{movie_id}/details")
def get_movie_details(
    movie_id: int,
    db: Session = Depends(get_db)
):
    # Find the movie
    movie = db.query(MovieDB).filter(
        MovieDB.id == movie_id
    ).first()

    if movie is None:
        raise HTTPException(
            status_code=404,
            detail="Movie not found"
        )

    # Calculate average rating and total reviews
    result = db.query(
        func.avg(ReviewDB.rating),
        func.count(ReviewDB.id)
    ).filter(
        ReviewDB.movie_id == movie_id
    ).first()

    average_rating = result[0]
    total_reviews = result[1]

    return {
        "id": movie.id,
        "title": movie.title,
        "year": movie.year,
        "genre": movie.genre,
        "average_rating": (
            f"{float(average_rating):.1f}"
            if average_rating is not None
            else None
        ),
        "total_reviews": total_reviews
    }