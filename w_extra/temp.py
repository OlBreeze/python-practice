# models.py
from django.db import models
from django.contrib.auth.models import User


# 1. Task Manager



# 2. E-commerce
class Product(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    stock = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)


class Cart(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)


class Order(models.Model):
    STATUS_CHOICES = [
        ('processing', 'У процесі'),
        ('shipped', 'Відправлений'),
        ('delivered', 'Доставлений'),
    ]
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='processing')
    created_at = models.DateTimeField(auto_now_add=True)
    total_price = models.DecimalField(max_digits=10, decimal_places=2)


class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.IntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=2)


# 3. Movie Collection
class Genre(models.Model):
    name = models.CharField(max_length=100)


class Movie(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    genres = models.ManyToManyField(Genre)
    rating = models.FloatField(default=0)
    release_date = models.DateField()
    created_at = models.DateTimeField(auto_now_add=True)


class Review(models.Model):
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.TextField()
    rating = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)


# 4. Blog Platform
class Post(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class Tag(models.Model):
    name = models.CharField(max_length=50)
    posts = models.ManyToManyField(Post, related_name='tags')


class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)


# 5. Server Monitoring
class Server(models.Model):
    STATUS_CHOICES = [
        ('online', 'Увімкнений'),
        ('offline', 'Вимкнений'),
    ]
    name = models.CharField(max_length=200)
    ip_address = models.GenericIPAddressField()
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='online')
    created_at = models.DateTimeField(auto_now_add=True)


class ServerMetric(models.Model):
    server = models.ForeignKey(Server, on_delete=models.CASCADE)
    cpu_usage = models.FloatField()
    memory_usage = models.FloatField()
    disk_usage = models.FloatField()
    timestamp = models.DateTimeField(auto_now_add=True)


class Alert(models.Model):
    server = models.ForeignKey(Server, on_delete=models.CASCADE)
    message = models.TextField()
    is_critical = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)


# 6. Book Library
class Book(models.Model):
    title = models.CharField(max_length=200)
    author = models.CharField(max_length=200)
    genre = models.CharField(max_length=100)
    isbn = models.CharField(max_length=13, unique=True)
    available = models.BooleanField(default=True)


class Rental(models.Model):
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    rented_at = models.DateTimeField(auto_now_add=True)
    return_date = models.DateTimeField()
    returned = models.BooleanField(default=False)


# 7. Student Course Management
class Course(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField()
    credits = models.IntegerField()


class Student(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    student_id = models.CharField(max_length=20, unique=True)
    courses = models.ManyToManyField(Course, through='Enrollment')


class Enrollment(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    enrolled_at = models.DateTimeField(auto_now_add=True)


class Grade(models.Model):
    enrollment = models.ForeignKey(Enrollment, on_delete=models.CASCADE)
    grade = models.FloatField()
    exam_date = models.DateTimeField()


# schemas.py
from ninja import Schema
from datetime import datetime
from typing import Optional, List


# 1. Task Manager Schemas



# 2. E-commerce Schemas
class ProductIn(Schema):
    name: str
    description: str
    price: float
    stock: int


class ProductOut(Schema):
    id: int
    name: str
    description: str
    price: float
    stock: int


class CartIn(Schema):
    product_id: int
    quantity: int


class CartOut(Schema):
    id: int
    product_id: int
    quantity: int


class OrderOut(Schema):
    id: int
    status: str
    created_at: datetime
    total_price: float


# 3. Movie Collection Schemas
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


# 4. Blog Schemas
class PostIn(Schema):
    title: str
    content: str


class PostOut(Schema):
    id: int
    title: str
    content: str
    created_at: datetime


class TagIn(Schema):
    name: str


class TagOut(Schema):
    id: int
    name: str


class CommentIn(Schema):
    text: str


class CommentOut(Schema):
    id: int
    post_id: int
    text: str
    created_at: datetime


# 5. Server Monitoring Schemas
class ServerIn(Schema):
    name: str
    ip_address: str
    status: str


class ServerOut(Schema):
    id: int
    name: str
    ip_address: str
    status: str


class MetricIn(Schema):
    cpu_usage: float
    memory_usage: float
    disk_usage: float


class MetricOut(Schema):
    id: int
    server_id: int
    cpu_usage: float
    memory_usage: float
    disk_usage: float
    timestamp: datetime


# 6. Book Library Schemas
class BookIn(Schema):
    title: str
    author: str
    genre: str
    isbn: str


class BookOut(Schema):
    id: int
    title: str
    author: str
    genre: str
    isbn: str
    available: bool


class RentalIn(Schema):
    book_id: int
    return_date: datetime


class RentalOut(Schema):
    id: int
    book_id: int
    rented_at: datetime
    return_date: datetime
    returned: bool


# 7. Student Course Management Schemas
class CourseIn(Schema):
    name: str
    description: str
    credits: int


class CourseOut(Schema):
    id: int
    name: str
    description: str
    credits: int


class StudentIn(Schema):
    student_id: str


class StudentOut(Schema):
    id: int
    student_id: str


class GradeIn(Schema):
    enrollment_id: int
    grade: float
    exam_date: datetime


class GradeOut(Schema):
    id: int
    enrollment_id: int
    grade: float
    exam_date: datetime


# api.py
from ninja import NinjaAPI
from ninja.security import django_auth
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404
from typing import List
from .models import *
from .schemas import *

api = NinjaAPI()


# Декоратор для аутентифікації
def authenticated(func):
    return api.operation(auth=django_auth)(func)



# ============= 2. E-COMMERCE API =============
@api.get("/products", response=List[ProductOut])
def list_products(request):
    return Product.objects.all()


@api.post("/products", response=ProductOut, auth=django_auth)
def create_product(request, payload: ProductIn):
    product = Product.objects.create(**payload.dict())
    return product


@api.get("/products/{product_id}", response=ProductOut)
def get_product(request, product_id: int):
    return get_object_or_404(Product, id=product_id)


@api.put("/products/{product_id}", response=ProductOut, auth=django_auth)
def update_product(request, product_id: int, payload: ProductIn):
    product = get_object_or_404(Product, id=product_id)
    for attr, value in payload.dict().items():
        setattr(product, attr, value)
    product.save()
    return product


@api.delete("/products/{product_id}", auth=django_auth)
def delete_product(request, product_id: int):
    product = get_object_or_404(Product, id=product_id)
    product.delete()
    return {"success": True}


@api.post("/cart", response=CartOut, auth=django_auth)
def add_to_cart(request, payload: CartIn):
    cart = Cart.objects.create(user=request.user, **payload.dict())
    return cart


@api.delete("/cart/{cart_id}", auth=django_auth)
def remove_from_cart(request, cart_id: int):
    cart = get_object_or_404(Cart, id=cart_id, user=request.user)
    cart.delete()
    return {"success": True}


@api.post("/orders", response=OrderOut, auth=django_auth)
def create_order(request):
    cart_items = Cart.objects.filter(user=request.user)
    total = sum(item.product.price * item.quantity for item in cart_items)
    order = Order.objects.create(user=request.user, total_price=total)
    for item in cart_items:
        OrderItem.objects.create(
            order=order,
            product=item.product,
            quantity=item.quantity,
            price=item.product.price
        )
    cart_items.delete()
    return order


@api.get("/orders", response=List[OrderOut], auth=django_auth)
def list_orders(request):
    return Order.objects.filter(user=request.user)


@api.put("/orders/{order_id}/status", response=OrderOut, auth=django_auth)
def update_order_status(request, order_id: int, status: str):
    order = get_object_or_404(Order, id=order_id)
    order.status = status
    order.save()
    return order


# ============= 3. MOVIE COLLECTION API =============
@api.get("/movies", response=List[MovieOut])
def list_movies(request, genre: str = None, rating: float = None):
    movies = Movie.objects.all()
    if genre:
        movies = movies.filter(genres__name=genre)
    if rating:
        movies = movies.filter(rating__gte=rating)
    return movies


@api.post("/movies", response=MovieOut, auth=django_auth)
def create_movie(request, payload: MovieIn):
    genre_ids = payload.dict().pop('genre_ids')
    movie = Movie.objects.create(**payload.dict())
    movie.genres.set(genre_ids)
    return movie


@api.get("/movies/{movie_id}", response=MovieOut)
def get_movie(request, movie_id: int):
    return get_object_or_404(Movie, id=movie_id)


@api.put("/movies/{movie_id}", response=MovieOut, auth=django_auth)
def update_movie(request, movie_id: int, payload: MovieIn):
    movie = get_object_or_404(Movie, id=movie_id)
    genre_ids = payload.dict().pop('genre_ids')
    for attr, value in payload.dict().items():
        setattr(movie, attr, value)
    movie.save()
    movie.genres.set(genre_ids)
    return movie


@api.delete("/movies/{movie_id}", auth=django_auth)
def delete_movie(request, movie_id: int):
    movie = get_object_or_404(Movie, id=movie_id)
    movie.delete()
    return {"success": True}


@api.get("/movies/search/{title}")
def search_movies(request, title: str):
    movies = Movie.objects.filter(title__icontains=title)
    return [MovieOut.from_orm(m) for m in movies]


@api.post("/movies/{movie_id}/reviews", response=ReviewOut, auth=django_auth)
def add_review(request, movie_id: int, payload: ReviewIn):
    movie = get_object_or_404(Movie, id=movie_id)
    review = Review.objects.create(
        movie=movie,
        user=request.user,
        **payload.dict()
    )
    return review


@api.post("/genres", response=GenreOut, auth=django_auth)
def create_genre(request, payload: GenreIn):
    genre = Genre.objects.create(**payload.dict())
    return genre


# ============= 4. BLOG PLATFORM API =============
@api.get("/posts", response=List[PostOut])
def list_posts(request):
    return Post.objects.all()


@api.post("/posts", response=PostOut, auth=django_auth)
def create_post(request, payload: PostIn):
    post = Post.objects.create(user=request.user, **payload.dict())
    return post


@api.get("/posts/{post_id}", response=PostOut)
def get_post(request, post_id: int):
    return get_object_or_404(Post, id=post_id)


@api.put("/posts/{post_id}", response=PostOut, auth=django_auth)
def update_post(request, post_id: int, payload: PostIn):
    post = get_object_or_404(Post, id=post_id, user=request.user)
    for attr, value in payload.dict().items():
        setattr(post, attr, value)
    post.save()
    return post


@api.delete("/posts/{post_id}", auth=django_auth)
def delete_post(request, post_id: int):
    post = get_object_or_404(Post, id=post_id, user=request.user)
    post.delete()
    return {"success": True}


@api.post("/posts/{post_id}/comments", response=CommentOut, auth=django_auth)
def add_comment(request, post_id: int, payload: CommentIn):
    post = get_object_or_404(Post, id=post_id)
    comment = Comment.objects.create(
        post=post,
        user=request.user,
        **payload.dict()
    )
    return comment


@api.post("/tags", response=TagOut, auth=django_auth)
def create_tag(request, payload: TagIn):
    tag = Tag.objects.create(**payload.dict())
    return tag


@api.post("/posts/{post_id}/tags/{tag_id}", auth=django_auth)
def add_tag_to_post(request, post_id: int, tag_id: int):
    post = get_object_or_404(Post, id=post_id)
    tag = get_object_or_404(Tag, id=tag_id)
    tag.posts.add(post)
    return {"success": True}


# ============= 5. SERVER MONITORING API =============
@api.get("/servers", response=List[ServerOut], auth=django_auth)
def list_servers(request):
    return Server.objects.all()


@api.post("/servers", response=ServerOut, auth=django_auth)
def create_server(request, payload: ServerIn):
    server = Server.objects.create(**payload.dict())
    return server


@api.get("/servers/{server_id}", response=ServerOut, auth=django_auth)
def get_server(request, server_id: int):
    return get_object_or_404(Server, id=server_id)


@api.put("/servers/{server_id}", response=ServerOut, auth=django_auth)
def update_server(request, server_id: int, payload: ServerIn):
    server = get_object_or_404(Server, id=server_id)
    for attr, value in payload.dict().items():
        setattr(server, attr, value)
    server.save()
    return server


@api.delete("/servers/{server_id}", auth=django_auth)
def delete_server(request, server_id: int):
    server = get_object_or_404(Server, id=server_id)
    server.delete()
    return {"success": True}


@api.post("/servers/{server_id}/metrics", response=MetricOut, auth=django_auth)
def add_metric(request, server_id: int, payload: MetricIn):
    server = get_object_or_404(Server, id=server_id)
    metric = ServerMetric.objects.create(server=server, **payload.dict())

    # Перевірка критичних значень
    if metric.cpu_usage > 90 or metric.memory_usage > 90:
        Alert.objects.create(
            server=server,
            message=f"Критичне навантаження на сервер {server.name}",
            is_critical=True
        )

    return metric


@api.get("/servers/{server_id}/metrics", response=List[MetricOut], auth=django_auth)
def get_metrics(request, server_id: int):
    return ServerMetric.objects.filter(server_id=server_id)


# ============= 6. BOOK LIBRARY API =============
@api.get("/books", response=List[BookOut])
def list_books(request, title: str = None, author: str = None, genre: str = None):
    books = Book.objects.all()
    if title:
        books = books.filter(title__icontains=title)
    if author:
        books = books.filter(author__icontains=author)
    if genre:
        books = books.filter(genre__icontains=genre)
    return books


@api.post("/books", response=BookOut, auth=django_auth)
def create_book(request, payload: BookIn):
    book = Book.objects.create(**payload.dict())
    return book


@api.get("/books/{book_id}", response=BookOut)
def get_book(request, book_id: int):
    return get_object_or_404(Book, id=book_id)


@api.put("/books/{book_id}", response=BookOut, auth=django_auth)
def update_book(request, book_id: int, payload: BookIn):
    book = get_object_or_404(Book, id=book_id)
    for attr, value in payload.dict().items():
        setattr(book, attr, value)
    book.save()
    return book


@api.delete("/books/{book_id}", auth=django_auth)
def delete_book(request, book_id: int):
    book = get_object_or_404(Book, id=book_id)
    book.delete()
    return {"success": True}


@api.post("/rentals", response=RentalOut, auth=django_auth)
def rent_book(request, payload: RentalIn):
    book = get_object_or_404(Book, id=payload.book_id)
    if not book.available:
        return {"error": "Книга недоступна"}

    rental = Rental.objects.create(
        book=book,
        user=request.user,
        return_date=payload.return_date
    )
    book.available = False
    book.save()
    return rental


@api.put("/rentals/{rental_id}/return", auth=django_auth)
def return_book(request, rental_id: int):
    rental = get_object_or_404(Rental, id=rental_id, user=request.user)
    rental.returned = True
    rental.save()
    rental.book.available = True
    rental.book.save()
    return {"success": True}


# ============= 7. STUDENT COURSE MANAGEMENT API =============
@api.get("/courses", response=List[CourseOut])
def list_courses(request):
    return Course.objects.all()


@api.post("/courses", response=CourseOut, auth=django_auth)
def create_course(request, payload: CourseIn):
    course = Course.objects.create(**payload.dict())
    return course


@api.get("/courses/{course_id}", response=CourseOut)
def get_course(request, course_id: int):
    return get_object_or_404(Course, id=course_id)


@api.put("/courses/{course_id}", response=CourseOut, auth=django_auth)
def update_course(request, course_id: int, payload: CourseIn):
    course = get_object_or_404(Course, id=course_id)
    for attr, value in payload.dict().items():
        setattr(course, attr, value)
    course.save()
    return course


@api.delete("/courses/{course_id}", auth=django_auth)
def delete_course(request, course_id: int):
    course = get_object_or_404(Course, id=course_id)
    course.delete()
    return {"success": True}


@api.get("/students", response=List[StudentOut], auth=django_auth)
def list_students(request):
    return Student.objects.all()


@api.post("/students", response=StudentOut, auth=django_auth)
def create_student(request, payload: StudentIn):
    student = Student.objects.create(user=request.user, **payload.dict())
    return student


@api.post("/enrollments", auth=django_auth)
def enroll_student(request, student_id: int, course_id: int):
    student = get_object_or_404(Student, id=student_id)
    course = get_object_or_404(Course, id=course_id)
    enrollment = Enrollment.objects.create(student=student, course=course)
    return {"success": True, "enrollment_id": enrollment.id}


@api.post("/grades", response=GradeOut, auth=django_auth)
def add_grade(request, payload: GradeIn):
    grade = Grade.objects.create(**payload.dict())
    return grade


@api.get("/courses/{course_id}/average", auth=django_auth)
def get_course_average(request, course_id: int):
    enrollments = Enrollment.objects.filter(course_id=course_id)
    grades = Grade.objects.filter(enrollment__in=enrollments)
    if grades.exists():
        avg = sum(g.grade for g in grades) / len(grades)
        return {"course_id": course_id, "average_grade": avg}
    return {"course_id": course_id, "average_grade": 0}


# urls.py (додати в основний urls.py проекту)
"""
from django.urls import path
from .api import api

urlpatterns = [
    path("api/", api.urls),
]
"""

# settings.py (додати в INSTALLED_APPS)
"""
INSTALLED_APPS = [
    ...
    'ninja',
    'your_app_name',
]
"""