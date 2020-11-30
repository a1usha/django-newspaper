from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.http import HttpResponse
from django.views.generic import TemplateView, DetailView
from django.contrib.auth.mixins import LoginRequiredMixin

from .models import Newspaper, Article
from django.contrib.auth.models import User


class EditorView(LoginRequiredMixin, TemplateView):
    login_url = 'login'
    template_name = "app/editor.html"

    def get_context_data(self, **kwargs):
        context = super(EditorView, self).get_context_data(**kwargs)
        user_id = self.request.user.id
        user = User.objects.get(id=user_id)
        newspaper = user.newspaper_set.first()
        if newspaper != None:
            context['articles'] = newspaper.article_set.all()
        return context
    
@login_required
def index(request):
    return redirect('app:app-editor')
