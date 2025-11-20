from ninja import Router
from django.shortcuts import get_object_or_404
from typing import List
from .models import *
from .schemas import *

router = Router()


@router.get("/books", response=List[BookOut])
def list_books(request, title: str = None, author: str = None, genre: str = None):
    books = Book.objects.all()
    if title:
        books = books.filter(title__icontains=title)
    if author:
        books = books.filter(author__icontains=author)
    if genre:
        books = books.filter(genre__icontains=genre)
    return books


@router.post("/books", response=BookOut)
def create_book(request, payload: BookIn):
    book = Book.objects.create(**payload.dict())
    return book


@router.get("/books/{book_id}", response=BookOut)
def get_book(request, book_id: int):
    return get_object_or_404(Book, id=book_id)


@router.put("/books/{book_id}", response=BookOut)
def update_book(request, book_id: int, payload: BookIn):
    book = get_object_or_404(Book, id=book_id)
    for attr, value in payload.dict().items():
        setattr(book, attr, value)
    book.save()
    return book


@router.delete("/books/{book_id}")
def delete_book(request, book_id: int):
    book = get_object_or_404(Book, id=book_id)
    book.delete()
    return {"success": True}


@router.post("/rentals", response=RentalOut)
def rent_book(request, payload: RentalIn):
    book = get_object_or_404(Book, id=payload.book_id)
    if not book.available:
        return {"error": "Книга недоступна"}

    rental = Rental.objects.create(book=book, user=request.user, return_date=payload.return_date)
    book.available = False
    book.save()
    return rental


@router.put("/rentals/{rental_id}/return")
def return_book(request, rental_id: int):
    rental = get_object_or_404(Rental, id=rental_id, user=request.user)
    rental.returned = True
    rental.save()
    rental.book.available = True
    rental.book.save()
    return {"success": True}
