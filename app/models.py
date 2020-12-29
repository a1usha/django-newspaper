from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.urls import reverse

from ckeditor.fields import RichTextField
from ckeditor_uploader.fields import RichTextUploadingField


class Newspaper(models.Model):
    title = models.CharField(max_length=100)
    date_posted = models.DateField(default=timezone.now)

    COLUMN_CHOISES = (
        ('2', 2),
        ('3', 3),
        ('4', 4),
        ('5', 5),
    )

    columns = models.CharField(max_length=1, choices=COLUMN_CHOISES, default=3)

    FORMAT_CHOISES = {
        ('broadsheet', 'Broadsheet - 600 x 750 mm (23.5" x 29.5")'),
        ('berliner', 'Berliner - 315 x 470 mm (12.4" x 18.5")'),
        ('tabloid', 'Tabloid - 280 x 430 mm (11.0" x 16.9")')
    }

    page_size = models.CharField(max_length=100, choices=FORMAT_CHOISES, default='berliner')

    # If the User gets deleted, the newspaper also deletes
    # Foreign key provides many-to-one relationship (User can have many newspapers created)
    author = models.ForeignKey(User, on_delete=models.CASCADE) 

    def __str__(self):
        return "'{}' created by {}".format(self.title, self.author)

    def get_absolute_url(self):
        return reverse('profile')
        # return reverse('editor', kwargs={'pk': self.pk})
    


class Article(models.Model):
    title = models.CharField(max_length=100)
    # content = models.TextField()
    # content = RichTextField(config_name='custom_ckeditor', blank=True, null=True)
    content = RichTextUploadingField(config_name='custom_ckeditor', blank=True, null=True)
    author = models.CharField(max_length=50)
    date_created = models.DateField(default=timezone.now)
    newspaper = models.ForeignKey(Newspaper, on_delete=models.CASCADE)

    def __str__(self):
        return "'{}' written by {}".format(self.title, self.author)


