from ninja import Router
from django.shortcuts import get_object_or_404
from .models import *
from .schemas import *

router = Router()

@router.get("/movies", response=List[MovieOut])
def list_movies(request, genre: str = None, rating: float = None):
    movies = Movie.objects.all()
    if genre:
        movies = movies.filter(genres__name=genre)
    if rating:
        movies = movies.filter(rating__gte=rating)
    return movies

@router.post("/movies", response=MovieOut)
def create_movie(request, payload: MovieIn):
    genre_ids = payload.dict().pop('genre_ids')
    movie = Movie.objects.create(**payload.dict())
    movie.genres.set(genre_ids)
    return movie

@router.get("/movies/{movie_id}", response=MovieOut)
def get_movie(request, movie_id: int):
    return get_object_or_404(Movie, id=movie_id)

@router.put("/movies/{movie_id}", response=MovieOut)
def update_movie(request, movie_id: int, payload: MovieIn):
    movie = get_object_or_404(Movie, id=movie_id)
    genre_ids = payload.dict().pop('genre_ids')
    for attr, value in payload.dict().items():
        setattr(movie, attr, value)
    movie.save()
    movie.genres.set(genre_ids)
    return movie

@router.delete("/movies/{movie_id}")
def delete_movie(request, movie_id: int):
    movie = get_object_or_404(Movie, id=movie_id)
    movie.delete()
    return {"success": True}

@router.get("/movies/search/{title}")
def search_movies(request, title: str):
    movies = Movie.objects.filter(title__icontains=title)
    return [MovieOut.from_orm(m) for m in movies]

@router.post("/movies/{movie_id}/reviews", response=ReviewOut)
def add_review(request, movie_id: int, payload: ReviewIn):
    movie = get_object_or_404(Movie, id=movie_id)
    review = Review.objects.create(movie=movie, user=request.user, **payload.dict())
    return review

@router.post("/genres", response=GenreOut)
def create_genre(request, payload: GenreIn):
    genre = Genre.objects.create(**payload.dict())
    return genre