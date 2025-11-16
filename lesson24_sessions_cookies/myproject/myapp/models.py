from django.db import models

class Author(models.Model):
    name = models.CharField(max_length=200)

class Book(models.Model):
    author = models.ForeignKey(Author, related_name='books', on_delete=models.CASCADE)
    title = models.CharField(max_length=300)
    # published_at = models.DateField(null=True, blank=True)
    published_year = models.IntegerField()

    def __str__(self):
        return self.title

    class Meta:
        indexes = [
            models.Index(fields=['author']),
            models.Index(fields=['published_year']),
        ]


class Review(models.Model):
    book = models.ForeignKey(Book, related_name='reviews', on_delete=models.CASCADE)
    # rating = models.PositiveSmallIntegerField()
    rating = models.IntegerField(choices=[(i, i) for i in range(1, 6)])

    comment = models.TextField(blank=True)
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        indexes = [
            models.Index(fields=['rating']),
            models.Index(fields=['created']),
        ]
