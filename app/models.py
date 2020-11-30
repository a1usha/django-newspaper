from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User

class Newspaper(models.Model):
    title = models.CharField(max_length=100)
    date_posted = models.DateField(default=timezone.now)
    # If the User gets deleted, the newspaper also deletes
    # Foreign key provides many-to-one relationship (User can have many newspapers created)
    author = models.ForeignKey(User, on_delete=models.CASCADE) 

    def __str__(self):
        return "'{}' created by {}".format(self.title, self.author)


class Article(models.Model):
    title = models.CharField(max_length=100)
    content = models.TextField()
    author = models.CharField(max_length=50)
    date_created = models.DateField(default=timezone.now)
    newspaper = models.ForeignKey(Newspaper, on_delete=models.CASCADE)

    def __str__(self):
        return "'{}' written by {}".format(self.title, self.author)


