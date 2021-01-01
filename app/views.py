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

from .models import Newspaper, Article
from django.contrib.auth.models import User


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
    

def index(request):
    return render(request, 'app/index.html')


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