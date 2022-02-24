from django.contrib.auth.views import LoginView
from django.contrib.auth.mixins import LoginRequiredMixin

from django.http import HttpResponse
from django.views.generic.detail import DetailView
from django.views.generic.list import ListView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy

from .models import *

# Create your views here.


class CustomLoginView(LoginView):
    template_name = "login.html"
    fields = "__all__"
    redirect_authenticated_user = True

    def get_success_url(self):
        return reverse_lazy("index")

class Index(ListView):
    model = Secret
    context_object_name = "secrets"


class SecretDetail(DetailView):
    model = Secret
    context_object_name = "secret"

class SecretCreate(CreateView):
    model = Secret
    fields = ["key", "passwd"]
    success_url = reverse_lazy("index")

class SecretUpdate(UpdateView):
    model = Secret
    fields = ["key", "passwd"]
    success_url = reverse_lazy("index")

class SecretDelete(DeleteView):
    model = Secret
    context_object_name = "secret"
    success_url = reverse_lazy("index")
