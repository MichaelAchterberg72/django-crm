from django.shortcuts import render, redirect
from django.urls import reverse
from django.http import HttpResponse
from django.contrib.auth.forms import UserCreationForm
from django.views import generic
from .forms import CustomUserCreationForm

class SignupView(generic.CreateView):
    template_name = 'registration/signup.html'
    form_class = CustomUserCreationForm

    def get_success_url(self):
        return redirect(reverse('Login'))
