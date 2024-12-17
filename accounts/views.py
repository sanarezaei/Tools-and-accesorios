from django.shortcuts import render, get_object_or_404
from django.views.generic import CreateView, ListView, DeleteView
from django.views.generic.detail import DetailView
from django.views.generic.edit import FormView, UpdateView
from django.contrib import messages
from django.contrib.auth import authenticate, login, update_session_auth_hash
from django.contrib.auth.views import LoginView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseRedirect
from django.urls import reverse_lazy

from .forms import SignupForm, OTPVerificationForm, ProfileUpdateForm, PasswordUpdateForm, AddressForm
from .models import OTP, CustomUser, Address

import random
   
class CustomLoginView(LoginView):
    template_name = 'registration/login.html'


class SignUpView(FormView):
    form_class = SignupForm
    template_name = "accounts/signup.html"
    success_url = reverse_lazy("accounts:otp_verification")

    def form_valid(self, form):
        cd = form.cleaned_data
        
        # Save user info and send otp 
        self.request.session['signup_data'] = {
            'phone_number': cd.get('phone_number'),
            'username': cd.get('username'), 
            'email': cd.get('email'), 
            'password': cd.get('password1') # password1
            }
        return super().form_valid(form)
 

class OTPVerificationView(FormView):
    form_class = OTPVerificationForm
    template_name = "accounts/otp_verification.html"
    success_url = reverse_lazy("home")
    
    def get_signup_data(self):
        return self.request.session.get('signup_data', {})
    
    def get(self, request, *args, **kwargs):    
        # Get user phone_number for send otp code
        signup_data = self.get_signup_data()
        print("Signup Data:", signup_data)
        
        if signup_data:
            phone_number = signup_data.get('phone_number')
            if phone_number:
                run_code = str(random.randint(10000, 999999))
                otp, created = OTP.objects.get_or_create(phone_number=phone_number, defaults={'otp_code': run_code})
                print("Generated OTP Code:", run_code)
            else:
                print("Phone number not found in signup data.")
        else:
            print("Sign up data is empty")
        return super().get(request, *args, **kwargs)
    
    def form_valid(self, form):
        signup_data = self.get_signup_data()
           
        if not signup_data:
            form.add_error(None, "Signup data is empty.")
            return super().form_invalid(form)
        
        if signup_data:
            # Find otp and check exists
            phone_number = signup_data.get("phone_number")
            entered_code = form.cleaned_data.get("otp")
            otp = OTP.objects.filter(phone_number=phone_number, otp_code=entered_code)
            
            user = CustomUser.objects.create(
                phone_number=signup_data.get('phone_number'), 
                username=signup_data.get('username'),
                email=signup_data.get('email'),
                )
            user.set_password(signup_data.get('password'))
            user.save()
            
            otp.delete()
            self.request.session.flush()
            login(self.request, user)
        else:
            return super().form_invalid(form)
         
        return super().form_valid(form)


class ProfileView(LoginRequiredMixin, DetailView):
    template_name = 'accounts/profile.html'
    model = CustomUser
    context_object_name = "user"
    
    def get_object(self, queryset=None):
        return get_object_or_404(CustomUser, pk=self.request.user.pk)


class ProfileUpdateView(LoginRequiredMixin, UpdateView):
    model = CustomUser
    template_name = 'accounts/profile_update.html'
    form_class = ProfileUpdateForm
    success_url = reverse_lazy("accounts:profile")
    
    def get_object(self, queryset=None):
        return self.request.user


class PasswordUpdateView(LoginRequiredMixin, FormView):
    template_name = 'accounts/password_update.html'
    form_class = PasswordUpdateForm
    success_url = reverse_lazy("accounts:profile")
    
    def get_object(self, queryset=None):
        return self.request.user
    
    def form_valid(self, form):
        user = self.request.user
        cd = form.cleaned_data
        current_password = cd.get("current_password") 
        new_password = cd.get("new_password") 
        
        if not user.check_password(current_password):
            form.add_error("current_password", "Current password is incorrect.")
            return self.form_invalid(form)
        
        user.set_password(new_password)
        user.save()
        
        update_session_auth_hash(self.request, user)
        return super().form_valid(form)


class AddressListView(ListView):
    model = Address
    template_name = "accounts/address_list.html"
    context_object_name = "addresses"
    
    def get_queryset(self):
        return Address.objects.filter(user=self.request.user)


class AddressCreateView(CreateView):
    model = Address
    form_class = AddressForm
    template_name = "accounts/address_form.html"
    success_url = reverse_lazy("accounts:address_list")
    
    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)


class AddressUpdateView(UpdateView):
    model = Address
    form_class = AddressForm
    template_name = "accounts/address_form.html"
    success_url = reverse_lazy("accounts:address_list")
    

class AddressDeleteView(DeleteView):
    model = Address
    template_name = "accounts/address_confirm_delete.html"
    success_url = reverse_lazy("accounts:address_list")

