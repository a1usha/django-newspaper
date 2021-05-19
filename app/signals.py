from django.db.models.signals import post_save, post_delete, pre_save
from django.dispatch import receiver
from .models import AdTask, ArticleTask, Article, BaseTask, ImageTask, Newspaper, TextTask

TEXT_CONTENT_HEADER = '<p>-!!!- Text content written by {} -!!!-<p>'
AD_CONTENT_HEADER = '<p>-!!!- Advertisement "{}" written by {} -!!!-<p>'
IMAGE_CONTENT_HEADER = '<p>-!!!- Image taken by {} -!!!-<p>'
BOTTOM_DELIMETER = '<p>-!!!- +++ -!!!-<p>'


# Create article with articletask creation
@receiver(post_save, sender=ArticleTask)
def create_article(instance, created, **kwargs):
    if created:
        Article.objects.create(
            articletask=instance, 
            newspaper=instance.newspaper)


# Вставить в статью контент текстовой подзадачи после перевода ее в статус confirmed
@receiver(post_save, sender=TextTask)
def populate_article_with_text(instance, **kwargs):
    if instance.status == 'confirmed':
        # Если босс принимает задачу, то вставляем содержимое в статью
        article = Article.objects.get(articletask=instance.articletask)
        article.title = instance.article_title
        article.author = instance.author
        article.date_created = instance.date_created
    
        article.content += TEXT_CONTENT_HEADER.format(instance.assignee)
        article.content += instance.content
        article.content += BOTTOM_DELIMETER
        article.save()


@receiver(post_delete, sender=TextTask)
def remove_text_content_from_article(instance, **kwargs):
    article = Article.objects.get(articletask=instance.articletask)

    article.title = ""
    article.author = ""

    if instance.content and article.content:
        article.content = article.content.replace(TEXT_CONTENT_HEADER.format(instance.assignee), '')
        article.content = article.content.replace(instance.content, '')
        article.content = article.content.replace(BOTTOM_DELIMETER, '')
    article.save()


# Удалить старый текст перед сохранением и добавлением нового (избежать дублирование)
@receiver(pre_save, sender=TextTask)
def remove_old_text_before_save(instance, **kwargs):
    article = Article.objects.get(articletask=instance.articletask)
    prev_content = instance.tracker.previous('content')
    if prev_content and article.content:
        article.content = article.content.replace(TEXT_CONTENT_HEADER.format(instance.assignee), '')
        article.content = article.content.replace(prev_content, '')
        article.content = article.content.replace(BOTTOM_DELIMETER, '')
        article.save()




@receiver(post_save, sender=AdTask)
def populate_article_with_ad(instance, **kwargs):
    if instance.status == 'confirmed':
        article = Article.objects.get(articletask=instance.articletask)
        article.content += AD_CONTENT_HEADER.format(instance.ad_title, instance.assignee)
        article.content += instance.content
        article.content += BOTTOM_DELIMETER
        article.save()


@receiver(post_delete, sender=AdTask)
def remove_ad_content_from_article(instance, **kwargs):
    article = Article.objects.get(articletask=instance.articletask)
    if instance.content and article.content:
        article.content = article.content.replace(AD_CONTENT_HEADER.format(instance.ad_title, instance.assignee), '')
        article.content = article.content.replace(instance.content, '')
        article.content = article.content.replace(BOTTOM_DELIMETER, '')
        article.save()


@receiver(pre_save, sender=AdTask)
def remove_old_ad_before_save(instance, **kwargs):
    article = Article.objects.get(articletask=instance.articletask)
    prev_content = instance.tracker.previous('content')
    if prev_content and article.content:
        article.content = article.content.replace(AD_CONTENT_HEADER.format(instance.ad_title, instance.assignee), '')
        article.content = article.content.replace(instance.content, '')
        article.content = article.content.replace(BOTTOM_DELIMETER, '')
        article.save()




@receiver(post_save, sender=ImageTask)
def populate_article_with_image(instance, **kwargs):
    article = Article.objects.get(articletask=instance.articletask)
    if instance.status == 'confirmed':
        article.content += IMAGE_CONTENT_HEADER.format(instance.assignee)
        article.content += instance.image
        article.content += BOTTOM_DELIMETER
        article.save()


@receiver(post_delete, sender=ImageTask)
def remove_image_content_from_article(instance, **kwargs):
    article = Article.objects.get(articletask=instance.articletask)
    article.content = article.content.replace(IMAGE_CONTENT_HEADER.format(instance.assignee), '')
    article.content = article.content.replace(instance.image, '')
    article.content = article.content.replace(BOTTOM_DELIMETER, '')
    article.save()


@receiver(pre_save, sender=ImageTask)
def remove_old_image_before_save(instance, **kwargs):
    article = Article.objects.get(articletask=instance.articletask)
    prev_content = instance.tracker.previous('image')
    if prev_content and article.content:
        article.content = article.content.replace(IMAGE_CONTENT_HEADER.format(instance.assignee), '')
        article.content = article.content.replace(instance.image, '')
        article.content = article.content.replace(BOTTOM_DELIMETER, '')
        article.save()