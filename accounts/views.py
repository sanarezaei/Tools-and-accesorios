from django.shortcuts import render
from django.views.generic import CreateView
from django.urls import reverse_lazy
from django.contrib.auth.views import LoginView
from django.contrib.auth import authenticate, login
from django.http import HttpResponseRedirect

from .forms import UserCreationForm, AuthenticationForm, SignupForm

class SignUpView(CreateView):
    form_class = UserCreationForm
    success_url = reverse_lazy('login')
    template_name = "registration/signup.html"
    
    
class PhoneNumberLoginView(LoginView):
    template_name = 'registration/login.html'
    authentication_form = AuthenticationForm
    
    def form_valid(self, form):
        phone_number = forms.cleaned_data.get("phone_number")
        password = forms.cleaned_data.get("password")
        user = authenticate(self.request, phone_number=phone_number, password=password)
        
        if user is not None:
            login(self.request, user)
            return HttpResponseRedirect(self.get_success_url())
        return self.form_invalid(form)


class SignUpView(CreateView):
    form_class = SignupForm
    template_name = "registration/signup.html"
    success_url = reverse_lazy("login")
