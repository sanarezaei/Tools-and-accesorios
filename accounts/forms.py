from django.contrib.auth.forms import  UserChangeForm, AuthenticationForm
from django.contrib.auth import get_user_model
from django import forms
from django.core.exceptions import ValidationError

from .models import CustomUser, Address


class CustomUserChangeForm(UserChangeForm):
    class Meta:
        model = get_user_model()
        fields = ("phone_number",)
        
    
class PhoneNumberLoginForm(forms.Form):
    phone_number = forms.CharField(label="Phone Number", max_length=15)
    password = forms.CharField(label="Password", widget=forms.PasswordInput)        


class SignupForm(forms.ModelForm):
    password1 = forms.CharField(label="Password", widget=forms.PasswordInput)
    password2 = forms.CharField(label="Confirm Password", widget=forms.PasswordInput)
    
    class Meta:
        model = get_user_model()
        fields = ("phone_number", "username", "email")
    
    def clean_username(self):
        username = self.cleaned_data.get('username')
        if CustomUser.objects.filter(username=username).exists():
            raise ValidationError("A user with this username already exists.")
        return username
       
    def clean_password2(self): 
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Password don't match.")
        return password2
    
    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user 


class OTPVerificationForm(forms.Form):
    otp = forms.CharField(max_length=6, label="Enter OTP")
    

class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = ["phone_number", "username", ]


class PasswordUpdateForm(forms.Form):
    current_password = forms.CharField(widget=forms.PasswordInput, label="Current Password") 
    new_password = forms.CharField(widget=forms.PasswordInput, label="New Password")
    confirm_password = forms.CharField(widget=forms.PasswordInput, label="Confirm Password")
    
    def clean(self):
        cleaned_data = super().clean()
        new_password = cleaned_data.get("new_password")
        confirm_password = cleaned_data.get("confirm_password")
        
        if new_password != confirm_password:
            raise forms.ValidationError("The new password do not match.")
        return cleaned_data


class AddressForm(forms.ModelForm):
    class Meta:
        model = Address
        fields = ["first_name", "last_name", "province", "city", "postal_code", "address"]
