from django.urls import path
from . import views
from .views import (
    EditorDetailView, 
    EditorCreateView,
    EditorUpdateView,
    EditorDeleteView,
    ArticleCreateView,
    ArticleUpdateView,
    ArticleDeleteView,
)

app_name = "app"
urlpatterns = [
    path("", views.index, name="index"),
    path("newspaper/<int:pk>/", EditorDetailView.as_view(), name='editor'),
    path("newspaper/new/", EditorCreateView.as_view(), name='editor-create'),
    path("newspaper/<int:pk>/update/", EditorUpdateView.as_view(), name='editor-update'),
    path("newspaper/<int:pk>/delete/", EditorDeleteView.as_view(), name='editor-delete'),
    path("newspaper/<int:newspaper_id>/newarticle/", ArticleCreateView.as_view(), name='article-create'),
    path("newspaper/<int:newspaper_id>/article/<int:pk>/update", ArticleUpdateView.as_view(), name='article-update'),
    path("newspaper/<int:newspaper_id>/article/<int:pk>/delete", ArticleDeleteView.as_view(), name='article-delete'),
]
