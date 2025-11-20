from datetime import datetime
from typing import List

from ninja import Schema


class GenreIn(Schema):
    name: str


class GenreOut(Schema):
    id: int
    name: str


class MovieIn(Schema):
    title: str
    description: str
    genre_ids: List[int]
    rating: float
    release_date: datetime


class MovieOut(Schema):
    id: int
    title: str
    description: str
    rating: float
    release_date: datetime


class ReviewIn(Schema):
    text: str
    rating: int


class ReviewOut(Schema):
    id: int
    movie_id: int
    text: str
    rating: int
