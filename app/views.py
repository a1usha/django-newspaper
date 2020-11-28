from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.http import HttpResponse
from django.views.generic import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin


def loginView(request):
    if request.method == "POST":
        email = request.POST["login"]
        password = request.POST["password"]
        user = authenticate(request, username=email, password=password)
        if user is not None:
            login(request, user)
            return redirect("app:editor")
            # return HttpResponse("123")
            # Redirect to a success page.
        else:
            return HttpResponse("Bad login or pass")
    else:
        return HttpResponse("")


# class EditorView(TemplateView):
#     template_name = 'editor.html'


class EditorView(LoginRequiredMixin, TemplateView):
    login_url = "/auth/"
    template_name = "app/editor.html"


# @login_required(login_url='/')
# def editor(request):
#     # if not request.user.is_authenticated:
#     # return redirect('app:index')
#     # else:
#     return render(request, 'editor.html')


def index(request):
    if request.user.is_authenticated:
        return redirect("app:editor")
    else:
        return redirect("app:auth")


# class AuthView(TemplateView):
#     template_name = 'signin.html'

def auth(request):
    if not request.user.is_authenticated:
        return render(request, "app/signin.html")
    else:
        return redirect("app:editor")


# Page for editor.js package testing and development
def editorjs_example(request):
    if request.user.is_authenticated:
        return render(request, 'editorjs_example.html')
    else:
        return redirect("app:auth")
