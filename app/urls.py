from django.urls import path
from . import views

app_name = "app"
urlpatterns = [
    path("", views.index, name="index"),
    path("editor/", views.EditorView.as_view(), name='app-editor'),
]
