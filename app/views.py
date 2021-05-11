from typing import Text
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, reverse, get_object_or_404
from django.contrib.auth import authenticate, login
from django.http import JsonResponse
import json

from django.views.generic import (
    DetailView,
    CreateView,
    UpdateView,
    DeleteView
)

from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin

from .models import *
from django.contrib.auth.models import Group, User


# Diplay newspaper
class EditorDetailView(PermissionRequiredMixin, DetailView):
    model = Newspaper
    template_name = "app/editor.html"

    # Check if it is a user's newspaper
    def has_permission(self):
        newspaper = self.get_object()
        return self.request.user == newspaper.author


# Create newspaper
class EditorCreateView(LoginRequiredMixin, CreateView):
    model = Newspaper
    fields = ['title', 'page_size', 'columns']

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)


# Edit newspaper parameters
class EditorUpdateView(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    model = Newspaper
    fields = ['title', 'page_size', 'columns']

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('app:editor', kwargs={'pk': self.get_object().id})

    # Check if it is a user's newspaper
    def has_permission(self):
        newspaper = self.get_object()
        return self.request.user == newspaper.author


# Delete newspaper
class EditorDeleteView(LoginRequiredMixin, PermissionRequiredMixin, DeleteView):
    model = Newspaper

    def get_success_url(self):
        return reverse('profile')

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

    # Check if it is a user's newspaper
    def has_permission(self):
        newspaper = self.get_object()
        return self.request.user == newspaper.author


# Create article
class ArticleCreateView(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    model = Article
    fields = ['title', 'content', 'author', 'date_created']

    # Function to take newspaper by id from URL
    def dispatch(self, request, *args, **kwargs):
        """
        Overridden so we can make sure the `newspaper` instance exists
        before going any further.
        """
        self.newspaper = get_object_or_404(Newspaper, pk=kwargs['newspaper_id'])
        return super().dispatch(request, *args, **kwargs)

    def get_success_url(self):
        if self.request.POST.get('to_profile'):
            return reverse('profile')
        elif self.request.POST.get('to_editor'):
            return reverse('app:editor', kwargs={'pk': self.newspaper.id})

    def form_valid(self, form):
        form.instance.newspaper = self.newspaper
        return super().form_valid(form)

    # Check if it is a user's newspaper
    def has_permission(self):
        return self.request.user == self.newspaper.author


# Edit article
class ArticleUpdateView(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    model = Article
    fields = ['title', 'content', 'author', 'date_created']

    # Function to take newspaper by id from URL
    def dispatch(self, request, *args, **kwargs):
        """
        Overridden so we can make sure the `newspaper` instance exists
        before going any further.
        """
        self.newspaper = get_object_or_404(Newspaper, pk=kwargs['newspaper_id'])
        return super().dispatch(request, *args, **kwargs)

    def get_success_url(self):
        return reverse('app:editor', kwargs={'pk': self.newspaper.id})

    def form_valid(self, form):
        form.instance.newspaper = self.newspaper
        return super().form_valid(form)

    # Check if it is a user's newspaper
    def has_permission(self):
        return self.request.user == self.newspaper.author


# Delete article
class ArticleDeleteView(LoginRequiredMixin, PermissionRequiredMixin, DeleteView):
    model = Article

    # Function to take newspaper by id from URL
    def dispatch(self, request, *args, **kwargs):
        """
        Overridden so we can make sure the `newspaper` instance exists
        before going any further.
        """
        self.newspaper = get_object_or_404(Newspaper, pk=kwargs['newspaper_id'])
        return super().dispatch(request, *args, **kwargs)

    def get_success_url(self):
        return reverse('app:editor', kwargs={'pk': self.newspaper.id})

    def form_valid(self, form):
        form.instance.newspaper = self.newspaper
        return super().form_valid(form)

    # Check if it is a user's newspaper
    def has_permission(self):
        return self.request.user == self.newspaper.author
    

# Create task for article
class ArticleTaskCreateView(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    model = ArticleTask
    fields = ['title', 'description']
    
    # Function to take newspaper by id from URL
    def dispatch(self, request, *args, **kwargs):
        """
        Overridden so we can make sure the `newspaper` instance exists
        before going any further.
        """
        self.newspaper = get_object_or_404(Newspaper, pk=kwargs['newspaper_id'])
        return super().dispatch(request, *args, **kwargs)

    def get_success_url(self):
        return reverse('profile')

    def form_valid(self, form):
        form.instance.newspaper = self.newspaper
        return super().form_valid(form)

    # Check if it is a user's newspaper
    def has_permission(self):
        print(self.request.user.groups.filter(name='Copy editor').exists())
        return self.request.user == self.newspaper.author and isUserInGroup(self.request.user, 'Copy editor')



# Delete existing article task
class ArticleTaskDeleteView(LoginRequiredMixin, PermissionRequiredMixin, DeleteView):
    model = ArticleTask

    # Function to take newspaper by id from URL
    def dispatch(self, request, *args, **kwargs):
        """
        Overridden so we can make sure the `newspaper` instance exists
        before going any further.
        """
        self.newspaper = get_object_or_404(Newspaper, pk=kwargs['newspaper_id'])
        return super().dispatch(request, *args, **kwargs)

    def get_success_url(self):
        return reverse('profile')

    def form_valid(self, form):
        form.instance.newspaper = self.newspaper
        return super().form_valid(form)

    # Check if it is a user's newspaper
    def has_permission(self):
        print(self.request.user.groups.filter(name='Copy editor').exists())
        return self.request.user == self.newspaper.author and isUserInGroup(self.request.user, 'Copy editor')



# Update existing article task == change status to archived
class ArticleTaskUpdateView(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    model = ArticleTask
    fields = ['status']

    # Function to take newspaper by id from URL
    def dispatch(self, request, *args, **kwargs):
        """
        Overridden so we can make sure the `newspaper` instance exists
        before going any further.
        """
        self.newspaper = get_object_or_404(Newspaper, pk=kwargs['newspaper_id'])
        return super().dispatch(request, *args, **kwargs)

    def get_success_url(self):
        return reverse('profile')

    def form_valid(self, form):
        form.instance.newspaper = self.newspaper
        return super().form_valid(form)

    # Check if it is a user's newspaper
    def has_permission(self):
        print(self.request.user.groups.filter(name='Copy editor').exists())
        return self.request.user == self.newspaper.author and isUserInGroup(self.request.user, 'Copy editor')


class SubtaskView(LoginRequiredMixin, PermissionRequiredMixin):
    # Function to take newspaper by id from URL
    def dispatch(self, request, *args, **kwargs):
        """
        Overridden so we can make sure the `newspaper` instance exists
        before going any further.
        """
        self.articletask = get_object_or_404(ArticleTask, pk=kwargs['articletask_id'])
        return super().dispatch(request, *args, **kwargs)

    def get_success_url(self):
        return reverse('profile')

    def form_valid(self, form):
        form.instance.articletask = self.articletask
        return super().form_valid(form)

    # Check if it is a user's newspaper
    def has_permission(self):
        print(self.request.user.groups.filter(name='Copy editor').exists())
        return self.request.user == self.articletask.newspaper.author and isUserInGroup(self.request.user, 'Copy editor')


# Create new image subtask in existing article task
class ImageTaskCreateView(SubtaskView, CreateView):
    model = ImageTask
    fields = ['title', 'description', 'assignee']


# Delete existing image subtask from article task
class ImageTaskDeleteView(SubtaskView, DeleteView):
    model = ImageTask


# Update existing image subtask in article task
class ImageTaskUpdateView(SubtaskView, UpdateView):
    model = ImageTask
    fields = ['status']



# Create new text task in existing article task 
class TextTaskCreateView(SubtaskView, CreateView):
    model = TextTask
    fields = ['title', 'description', 'assignee']


# Delete existing text subtask from article task
class TextTaskDeleteView(SubtaskView, DeleteView):
    model = TextTask


# Update existing text subtask in article task
class TextTaskUpdateView(SubtaskView, UpdateView):
    model = TextTask
    fields = ['status']



# Create new ad subtask in existing article task
class AdTaskCreateView(SubtaskView, CreateView):
    model = AdTask
    fields = ['title', 'description', 'assignee']


# Delete existing ad subtask from article task
class AdTaskDeleteView(SubtaskView, DeleteView):
    model = AdTask


# Update existing ad subtask in article task
class AdTaskUpdateView(SubtaskView, UpdateView):
    model = AdTask
    fields = ['status']



# Create new typo subtask in existing article task
class TypoTaskCreateView(SubtaskView, CreateView):
    model = TypoTask
    fields = ['title', 'description', 'assignee']


# Delete existing typo subtask from article task
class TypoTaskDeleteView(SubtaskView, DeleteView):
    model = TypoTask


# Update existing typo subtask in article subtask
class TypoTaskUpdateView(SubtaskView, UpdateView):
    model = TypoTask
    fields = ['status']



def index(request):
    return render(request, 'app/index.html')


def isUserInGroup(user, groupname):
    return user.groups.filter(name=groupname).exists()


# Update order of articles using ajax
def updateArticleOrder(request):
    # request should be ajax and method should be POST.
    if request.is_ajax and request.method == "POST":
        
        orders = json.loads(request.POST.get('orders'))

        for article_id in orders:
            article = Article.objects.filter(pk=article_id).update(order=orders[article_id])
            
        return JsonResponse({"ok": ""}, status=200)

    # some error occured
    return JsonResponse({"error": ""}, status=400)