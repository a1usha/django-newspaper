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
    taskSubmitRedirect,
    updateArticleOrder,
    ArticleTaskCreateView,
    ArticleTaskDeleteView,
    ArticleTaskUpdateView,
    ImageTaskCreateView,
    ImageTaskDeleteView,
    ImageTaskUpdateView,
    ImageTaskSubmitView,
    TextTaskCreateView,
    TextTaskDeleteView,
    TextTaskUpdateView,
    TextTaskSubmitView,
    AdTaskCreateView,
    AdTaskDeleteView,
    AdTaskUpdateView,
    AdTaskSubmitView,
    TypoTaskCreateView,
    TypoTaskDeleteView,
    TypoTaskUpdateView
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

    path("newspaper/<int:newspaper_id>/newarticletask/", ArticleTaskCreateView.as_view(), name='articletask-create'),
    path("newspaper/<int:newspaper_id>/articletask/<int:pk>/delete", ArticleTaskDeleteView.as_view(), name='articletask-delete'),
    path("newspaper/<int:newspaper_id>/articletask/<int:pk>/update", ArticleTaskUpdateView.as_view(), name='articletask-update'),

    path("articletask/<int:articletask_id>/subtask/<int:pk>/submit", views.taskSubmitRedirect, name="subtask-submit"),

    path("newspaper/<int:newspaper_id>/articletask/<int:articletask_id>/newimagetask", ImageTaskCreateView.as_view(), name='imagetask-create'),
    path("articletask/<int:articletask_id>/imagetask/<int:pk>/submit", ImageTaskSubmitView.as_view(), name='imagetask-submit'),
    path("newspaper/<int:newspaper_id>/articletask/<int:articletask_id>/imagetask/<int:pk>/delete", ImageTaskDeleteView.as_view(), name='imagetask-delete'),
    path("newspaper/<int:newspaper_id>/articletask/<int:articletask_id>/imagetask/<int:pk>/update", ImageTaskUpdateView.as_view(), name='imagetask-update'),

    path("newspaper/<int:newspaper_id>/articletask/<int:articletask_id>/newtexttask", TextTaskCreateView.as_view(), name='texttask-create'),
    path("articletask/<int:articletask_id>/texttask/<int:pk>/submit", TextTaskSubmitView.as_view(), name='texttask-submit'),
    path("newspaper/<int:newspaper_id>/articletask/<int:articletask_id>/texttask/<int:pk>/delete", TextTaskDeleteView.as_view(), name='texttask-delete'),
    path("newspaper/<int:newspaper_id>/articletask/<int:articletask_id>/texttask/<int:pk>/update", TextTaskUpdateView.as_view(), name='texttask-update'),

    path("newspaper/<int:newspaper_id>/articletask/<int:articletask_id>/newadtask", AdTaskCreateView.as_view(), name='adtask-create'),
    path("articletask/<int:articletask_id>/adtask/<int:pk>/submit", AdTaskSubmitView.as_view(), name='adtask-submit'),
    path("newspaper/<int:newspaper_id>/articletask/<int:articletask_id>/adtask/<int:pk>/delete", AdTaskDeleteView.as_view(), name='adtask-delete'),
    path("newspaper/<int:newspaper_id>/articletask/<int:articletask_id>/adtask/<int:pk>/update", AdTaskUpdateView.as_view(), name='adtask-update'),

    path("newspaper/<int:newspaper_id>/articletask/<int:articletask_id>/newtypotask", TypoTaskCreateView.as_view(), name='typotask-create'),
    path("newspaper/<int:newspaper_id>/articletask/<int:articletask_id>/typotask/<int:pk>/delete", TypoTaskDeleteView.as_view(), name='typotask-delete'),
    path("newspaper/<int:newspaper_id>/articletask/<int:articletask_id>/typotask/<int:pk>/update", TypoTaskUpdateView.as_view(), name='typotask-update'),

    path("newspaper/ajax/article_order", updateArticleOrder, name='article-order-update')
]
