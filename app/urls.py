from django.urls import path
from . import views
from .views import (
    EditorDetailView, 
    EditorCreateView,
    EditorUpdateView,
    EditorDeleteView,
    ArticleCreateView
)

app_name = "app"
urlpatterns = [
    path("", views.index, name="index"),
    path("newspaper/<int:pk>/", EditorDetailView.as_view(), name='editor'),
    path("newspaper/new/", EditorCreateView.as_view(), name='editor-create'),
    path("newspaper/<int:pk>/update/", EditorUpdateView.as_view(), name='editor-update'),
    path("newspaper/<int:pk>/delete/", EditorDeleteView.as_view(), name='editor-delete'),
    path("newspaper/<int:newspaper_id>/newarticle/", ArticleCreateView.as_view(), name='article-create'),
]
