from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()

# Books model

class Book(models.Model):
    title = models.CharField(max_length=255)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    collaborators = models.ManyToManyField(User, related_name='collaborating_books')
    created_at = models.DateTimeField(auto_now_add=True)


# Book section/subsections model
class BookSection(models.Model):
    title = models.CharField(max_length=255)
    content = models.TextField()
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    parent_section = models.ForeignKey('self', null=True, blank=True, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
