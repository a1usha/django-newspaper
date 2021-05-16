from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import ArticleTask, Article

# Create article with articletask creation
@receiver(post_save, sender=ArticleTask)
def create_article(sender, instance, created, **kwargs):
    print('Someone created articletask')
    print(sender)
    print(instance.newspaper)
    print(created)