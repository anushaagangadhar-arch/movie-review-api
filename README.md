Movie Review API

A backend REST API for managing movies, users, and movie reviews.

Built using FastAPI, PostgreSQL, SQLAlchemy, JWT authentication, and Alembic.

Features

- User registration
- Secure password hashing
- User login with JWT authentication
- Protected API endpoints
- Movie CRUD operations
- Prevent duplicate movies
- Search movies by title
- Filter movies by release year
- Filter movies by genre
- Pagination
- Sorting
- Create, read, update, and delete reviews
- Movie rating calculation
- Movie details with average rating and review count
- Input validation
- Proper HTTP error handling
- Automated API tests
- PostgreSQL database
- Alembic database migrations
- Swagger API documentation
- Deployed using Render

Technologies

- Python
- FastAPI
- PostgreSQL
- SQLAlchemy
- Pydantic
- JWT
- pwdlib
- Alembic
- pytest
- Render
- GitHub

API Endpoints

Authentication

Method| Endpoint| Description
POST| "/register"| Register a new user
POST| "/login"| Login and receive JWT token

Movies

Method| Endpoint| Description
GET| "/movies"| Get movies with pagination and sorting
POST| "/movies"| Create a movie
GET| "/movies/{movie_id}"| Get a movie
PUT| "/movies/{movie_id}"| Update a movie
DELETE| "/movies/{movie_id}"| Delete a movie
GET| "/movies/search"| Search movies by title
GET| "/movies/year/{year}"| Filter movies by year
GET| "/movies/genre/{genre}"| Filter movies by genre
GET| "/movies/{movie_id}/rating"| Get movie rating
GET| "/movies/{movie_id}/details"| Get movie details and rating

Reviews

Method| Endpoint| Description
POST| "/reviews"| Create a review
GET| "/reviews"| Get reviews
GET| "/reviews/{review_id}"| Get one review
PUT| "/reviews/{review_id}"| Update a review
DELETE| "/reviews/{review_id}"| Delete a review

Authentication

Protected endpoints require a JWT access token.

1. Register using "/register".
2. Login using "/login".
3. Copy the returned "access_token".
4. Click Authorize in Swagger.
5. Enter the token.
6. Access protected endpoints.

Run Locally

Clone the repository and enter the project directory:

git clone https://github.com/anushaagangadhar-arch/movie-review-api.git
cd movie-review-api

Create and activate a virtual environment:

python -m venv .venv

Windows PowerShell:

.venv\Scripts\Activate.ps1

Install dependencies:

pip install -r requirements.txt

Create a ".env" file and configure:

DATABASE_URL=your_postgresql_database_url
SECRET_KEY=your_secret_key

Run the API:

python -m uvicorn main:app --reload

Open Swagger:

http://127.0.0.1:8000/docs

Run Tests

Run:

pytest -q

Current test result:

5 passed

Database Migrations

Alembic is used for database migrations.

Check the current migration:

alembic current

Apply migrations:

alembic upgrade head

Deployment

The API is deployed using Render with a PostgreSQL database.

The application uses environment variables for sensitive configuration such as:

- "DATABASE_URL"
- "SECRET_KEY"

Sensitive values are not stored in GitHub.

Project Structure

movie-review-api/
│
├── main.py
├── database.py
├── models.py
├── schemas.py
├── security.py
├── init_db.py
├── test_main.py
├── requirements.txt
├── alembic.ini
├── migration/
├── .env
└── .gitignore

Learning Outcomes

This project demonstrates practical backend development concepts including:

- REST API development
- Authentication and authorization
- Password security
- JWT tokens
- Database design
- SQLAlchemy ORM
- PostgreSQL
- Data validation
- Pagination and sorting
- Error handling
- Automated testing
- Database migrations
- Cloud deployment
- Git and GitHub