from django.urls import path
from . import views

app_name = "app"
urlpatterns = [
    path("", views.index, name="index"),
    path("auth", views.auth, name="auth"),
    path("auth/login", views.loginView, name="login"),
    path("editor", views.EditorView.as_view(), name="editor"),
    path("test", views.editorjs_example, name="test")
]
