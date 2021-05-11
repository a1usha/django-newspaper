from django.db import models
from django.db.models.base import Model
from django.db.models.deletion import CASCADE
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
    # content = RichTextField(config_name='custom_ckeditor', blank=True, null=True)
    content = RichTextUploadingField(config_name='custom_ckeditor', blank=True, null=True)
    author = models.CharField(max_length=50)
    date_created = models.DateField(default=timezone.now)
    newspaper = models.ForeignKey(Newspaper, on_delete=models.CASCADE)
    order = models.IntegerField(default=1000, null=True)

    class Meta:
        ordering = ['order']

    def __str__(self):
        return "'{}' written by {}".format(self.title, self.author)



class ArticleTask(models.Model):
    date_created = models.DateField(default=timezone.now)
    title = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)
    newspaper = models.ForeignKey(Newspaper, on_delete=models.CASCADE, default=0)

    STATUS_CHOISES = (
        ('in progress', 'in progress'),
        ('archived', 'archived'),
    )

    status = models.CharField(max_length=100, choices=STATUS_CHOISES, default='in progress')

    def __str__(self):
        return "'{}' article task owned by {}".format(self.title, self.newspaper.author)


class BaseTask(models.Model):
    articletask = models.ForeignKey(ArticleTask, on_delete=CASCADE)
    title = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)

    STATUS_CHOISES = (
        ('in progress', 'in progress'),
        ('awaiting review', 'awaiting review'),
        ('confirmed', 'confirmed'),
    )

    status = models.CharField(max_length=100, choices=STATUS_CHOISES, default='in progress')

    class Meta:
        abstract=True

    def __str__(self):
        return "'{}' subtask owned by {} and assigned to {}".format(self.title, self.newspaper.author, self.assignee)


class ImageTask(BaseTask):
    assignee = models.ForeignKey(User, on_delete=models.CASCADE, limit_choices_to={'groups__name': "Illustrator"})
    image = models.ImageField(default='default.jpg', upload_to='profile_pics')


class TextTask(BaseTask):
    assignee = models.ForeignKey(User, on_delete=models.CASCADE, limit_choices_to={'groups__name': "Author"})
    article_title = models.CharField(max_length=100, blank=True)
    content = RichTextUploadingField(config_name='custom_ckeditor', blank=True, null=True)
    author = models.CharField(max_length=50)
    date_created = models.DateField(default=timezone.now)


class AdTask(BaseTask):
    assignee = models.ForeignKey(User, on_delete=models.CASCADE, limit_choices_to={'groups__name': "Advertisement designer"})
    ad_title = models.CharField(max_length=100, blank=True)
    content = RichTextUploadingField(config_name='custom_ckeditor', blank=True, null=True)


class TypoTask(BaseTask):
    assignee = models.ForeignKey(User, on_delete=models.CASCADE, limit_choices_to={'groups__name': "Head of typography"})
