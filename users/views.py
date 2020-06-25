from django.core.mail import send_mail
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic import CreateView

from .forms import CreationForm

class SignUp(CreateView):
    form_class = CreationForm
    success_url = '/auth/login/'
    template_name = 'signup.html'

    def form_valid(self, form):
        email = form.cleaned_data['email']
        send_msg(email)
        return super().form_valid(form)

def send_msg(email):
    send_mail(
        'Successful registration', 'Sup, welcome to Yatubah', 'yatube@yatube.com', [email], fail_silently=False,
        )