from django.shortcuts import render
from django.views.generic import CreateView
from django.urls import reverse_lazy
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.auth import authenticate, login
from django.http import HttpResponseRedirect
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.detail import DetailView
from django.shortcuts import get_object_or_404
from django.views.generic.edit import FormView, UpdateView
from django.contrib.auth import update_session_auth_hash
from django.views.generic import ListView, DeleteView

from .forms import UserCreationForm, SignupForm, OTPVerificationForm, ProfileUpdateForm, PasswordUpdateForm, AddressForm
from .models import OTP, CustomUser, Address
      
class LoginView(LoginView):
    template_name = 'registration/login.html'
    
    def form_valid(self, form):
        phone_number = form.cleaned_data.get("phone_number")
        password = form.cleaned_data.get("password")
        user = authenticate(self.request, phone_number=phone_number, password=password)
        
        if user is not None:
            login(self.request, user)
            return HttpResponseRedirect(self.get_success_url())
        return self.form_invalid(form)


class SignUpView(CreateView):
    form_class = SignupForm
    template_name = "registration/signup.html"
    success_url = reverse_lazy("login")


def otp_verification_view(request):
    if request.method == 'POST':
        form = OTPVerificationForm(request.POST)
        if form.is_valid():
            otp_input = form.cleaned_data.get("otp")
            try:
                otp_obj = OTP.objects.get(otp_code=otp_input, user=request.user)
                if otp_obj.is_valid():
                    request.user.is_active = True
                    request.user.save()
                    otp_obj.delete()
                    messages.success(request, "Your account is activated:)")
                    return redirect("home")
            except OTP.DoesNotExist:
                messages.error(request, "OTP invalid. Please try again.")
    else:
        form = OTPVerificationForm()
    return render(request, "accounts/otp_verification.html", context={"form": form})

def register_view(request):
    if request.method == "POST":
        user = CustomUser.objects.create_user(
            phone_number=request.POST["phone_number"],
            username=request.POST[""],
            email=request.POST["email"],
            password=request.POST["password"],
            is_active = False
        ) 
        print("user")
        messages.info(request, "An OTP has been sent to your phone.")
        return redirect("otp_verification") 
    return render(request, "register/signup.html")


class ProfileView(LoginRequiredMixin, DetailView):
    template_name = 'accounts/profile.html'
    model = CustomUser
    context_object_name = "user"
    
    def get_object(self):
        return get_object_or_404(CustomUser, pk=self.request.user.pk)


class ProfileUpdateView(LoginRequiredMixin, UpdateView):
    model = CustomUser
    template_name = 'accounts/profile_update.html'
    form_class = ProfileUpdateForm
    success_url = reverse_lazy("accounts:profile")
    
    def get_object(self):
        return self.request.user


class PasswordUpdateView(LoginRequiredMixin, FormView):
    template_name = 'accounts/password_update.html'
    form_class = PasswordUpdateForm
    success_url = reverse_lazy("accounts:profile")
    
    def get_object(self):
        return self.request.user
    
    def form_invalid(self, form):
        user = self.request.user
        current_password = form.cleaned_date.get("current_password") 
        new_password = form.cleaned_date.get("new_password") 
        
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

