Movie Review API

A REST API built using Python, FastAPI, and PostgreSQL to manage movies and their reviews.

Features

- Create, view, update, and delete movies
- Search movies by title
- Filter movies by release year and genre
- Pagination and sorting
- Create, view, update, and delete reviews
- Validate movie details and review ratings
- Calculate total reviews and average ratings
- Automated testing using pytest

Technologies Used

- Python
- FastAPI
- PostgreSQL
- SQLAlchemy
- Pydantic
- Pytest

Project Structure

movie-review-api/
├── main.py
├── database.py
├── test_main.py
├── requirements.txt
└── README.md

Installation and Setup

1. Create a virtual environment

python -m venv .venv

2. Activate the virtual environment

.\.venv\Scripts\Activate.ps1

3. Install dependencies

python -m pip install -r requirements.txt

4. Configure PostgreSQL

Install PostgreSQL and create a database named "movie_db".

Configure the database connection with your own credentials. Never publish database passwords in your source code or GitHub repository.

5. Start the API

python -m uvicorn main:app --reload

6. Open API documentation

Open this URL in your browser:

http://127.0.0.1:8000/docs

Running Tests

Run the following command in the project terminal:

python -m pytest test_main.py -v

The latest full test run completed with 57 passing tests.

Future Improvements

- Deploy the API online
- Add authentication and authorization
- Improve database configuration and security
- Add more automated tests