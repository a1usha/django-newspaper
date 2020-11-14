from django.contrib.auth import authenticate, login
from django.http import HttpResponse
from django.views.generic import ListView, TemplateView


def auth(request):
    username = request.POST["username"]
    password = request.POST["password"]
    user = authenticate(request, username=username, password=password)
    if user is not None:
        login(request, user)
        # Redirect to a success page.
    else:
        return HttpResponse("Bad login or pass")


class IndexView(TemplateView):
    template_name = "signin.html"
