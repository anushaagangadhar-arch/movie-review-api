Movie Review API

A RESTful backend API built using Python, FastAPI, PostgreSQL, and SQLAlchemy to manage movies and their reviews.

Live Project

- Live API: https://movie-review-api-88ke.onrender.com
- Swagger API Documentation: https://movie-review-api-88ke.onrender.com/docs
- GitHub Repository: https://github.com/anushaagangadhar-arch/movie-review-api

Features

Movie Management

- Create, view, update, and delete movies
- Prevent duplicate movie entries
- Search movies by title
- Filter movies by release year and genre
- Pagination and sorting

Review Management

- Create, view, update, and delete reviews
- Validate review ratings and movie details
- Calculate total reviews and average ratings
- Prevent deletion of movies that have existing reviews

Testing

- Automated testing using pytest
- 57 tests passed in the latest full test run

Technologies Used

- Python
- FastAPI
- PostgreSQL
- SQLAlchemy
- Pydantic
- Pytest
- Uvicorn
- Git and GitHub
- Render

Project Structure

movie-review-api/
├── .venv/
├── main.py
├── database.py
├── test_main.py
├── requirements.txt
├── .gitignore
└── README.md

Installation and Setup

1. Clone the repository

git clone https://github.com/anushaagangadhar-arch/movie-review-api.git
cd movie-review-api

2. Create a virtual environment

python -m venv .venv

3. Activate the virtual environment

Windows PowerShell:

.\.venv\Scripts\Activate.ps1

4. Install dependencies

python -m pip install -r requirements.txt

5. Configure environment variables

Create a ".env" file in the project root directory.

Add your PostgreSQL connection URL:

DATABASE_URL=your_postgresql_connection_url

Replace the placeholder with your own database connection URL.

Security: Never upload your ".env" file or database credentials to GitHub.

6. Start the API

python -m uvicorn main:app --reload

7. Open API documentation

Visit:

http://127.0.0.1:8000/docs

Running Tests

Run the automated test suite:

python -m pytest

Latest full test result: 57 passed.

Deployment

The API is deployed using Render.

Live documentation:

https://movie-review-api-88ke.onrender.com/docs

Future Improvements

- Database migrations using Alembic
- User registration and login
- JWT authentication and authorization
- Role-based access control
- Improved logging and monitoring
- Additional automated integration tests

Author

Backend Development Projects