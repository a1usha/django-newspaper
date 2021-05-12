from django.contrib import admin
from .models import Newspaper, Article, ArticleTask, ImageTask, TextTask, AdTask, TypoTask, BaseTask

admin.site.register(Newspaper)
admin.site.register(Article)
admin.site.register(ArticleTask)
admin.site.register(ImageTask)
admin.site.register(TextTask)
admin.site.register(AdTask)
admin.site.register(TypoTask)
admin.site.register(BaseTask)