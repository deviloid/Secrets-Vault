from django import forms
from django.contrib.auth.views import LoginView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
from django.http import JsonResponse
from django.shortcuts import redirect
from django.views import View
from django.views.generic.detail import DetailView
from django.views.generic.list import ListView
from django.views.generic.edit import CreateView, UpdateView, DeleteView, FormView
from django.urls import reverse_lazy

from passlib.hash import pbkdf2_sha256

from .models import *

# Create your views here.


class CustomLoginView(LoginView):
    template_name = "login.html"
    fields = "__all__"
    redirect_authenticated_user = True

    def get_success_url(self):
        return reverse_lazy("index")


class RegisterPage(FormView):
    template_name = "register.html"
    form_class = UserCreationForm
    success_url = reverse_lazy("index")

    def form_valid(self, form):
        user = form.save()
        if user is not None:
            login(self.request, user)
        return super(RegisterPage, self).form_valid(form)

    def get(self, *args, **kwargs):
        if self.request.user.is_authenticated:
            return redirect("index")
        return super(RegisterPage, self).get(*args, **kwargs)


class Index(LoginRequiredMixin, ListView):
    model = Secret
    context_object_name = "secrets"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["secrets"] = context["secrets"].filter(user=self.request.user)
        return context


class SecretDetail(LoginRequiredMixin, DetailView):
    model = Secret
    context_object_name = "secret"


class CreateSecretForm(forms.ModelForm):
    class Meta:
        model = Secret
        fields = ["key", "passwd", "encrypted", "passwd_hashed"]
        widgets = {"passwd_hashed": forms.HiddenInput()}

    def clean(self):
        if self.cleaned_data["encrypted"] == True:
            passwd = self.cleaned_data["passwd"]
            self.cleaned_data["passwd_hashed"] = pbkdf2_sha256.encrypt(passwd)


class SecretCreate(LoginRequiredMixin, CreateView):
    template_name = "secret/secret_form.html"
    form_class = CreateSecretForm
    success_url = reverse_lazy("index")

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super(SecretCreate, self).form_valid(form)


class SecretUpdate(LoginRequiredMixin, UpdateView):
    model = Secret
    form_class = CreateSecretForm
    success_url = reverse_lazy("index")


class SecretDelete(LoginRequiredMixin, DeleteView):
    model = Secret
    context_object_name = "secret"
    success_url = reverse_lazy("index")


class getPasswd(LoginRequiredMixin, View):
    def get(self, *args, **kwargs):
        pk = self.request.GET.get("pk")
        if self.request.method == "GET":
            passwd = Secret.objects.get(id=pk).passwd
            hash = Secret.objects.get(id=pk).passwd_hashed
        data = {
            "passwd": passwd,
            "passwd_hash": hash
        }
        return JsonResponse(data)
