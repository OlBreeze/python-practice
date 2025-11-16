from django.contrib import admin
from .models import Author, Book, Review

@admin.register(Author)
class AuthorAdmin(admin.ModelAdmin):
    list_display = ['name']
    search_fields = ['name']

@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = ['title', 'author', 'published_year']
    list_filter = ['published_year', 'author']
    search_fields = ['title']

@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ['book', 'rating', 'created']
    list_filter = ['rating', 'created']