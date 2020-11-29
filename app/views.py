from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.http import HttpResponse
from django.views.generic import TemplateView, DetailView
from django.contrib.auth.mixins import LoginRequiredMixin

from .models import Newspaper, Article


def loginView(request):
    if request.method == "POST":
        email = request.POST["login"]
        password = request.POST["password"]
        user = authenticate(request, username=email, password=password)
        if user is not None:
            login(request, user)
            return redirect("app:editor")
        else:
            return HttpResponse("Bad login or pass")
    else:
        return HttpResponse("")


class EditorView(LoginRequiredMixin, TemplateView):
    login_url = "/auth/"
    template_name = "app/editor.html"

    def get_context_data(self, **kwargs):
        context = super(EditorView, self).get_context_data(**kwargs)
        context['articles'] = Newspaper.objects.first().article_set.all()
        return context
    

def index(request):
    if request.user.is_authenticated:
        return redirect("app:editor")
    else:
        return redirect("app:auth")


def auth(request):
    if not request.user.is_authenticated:
        return render(request, "app/signin.html", context={'title': 'login'})
    else:
        return redirect("app:editor")


# Page for editor.js package testing and development
def editorjs_example(request):
    if request.user.is_authenticated:
        return render(request, 'editorjs_example.html')
    else:
        return redirect("app:auth")
