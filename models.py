from sqlalchemy import Column, Integer, String, ForeignKey
from database import Base


# Database model for movies
class MovieDB(Base):
    __tablename__ = "movies"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(200), nullable=False)
    year = Column(Integer, nullable=False)
    genre = Column(String(100), nullable=False)


# Database model for reviews
class ReviewDB(Base):
    __tablename__ = "reviews"

    id = Column(Integer, primary_key=True, index=True)
    movie_id = Column(Integer, ForeignKey("movies.id"), nullable=False)
    rating = Column(Integer, nullable=False)
    comment = Column(String(500), nullable=False)