from django.contrib.auth.forms import UserCreationForm, UserChangeForm, AuthenticationForm
from django.contrib.auth import get_user_model
from django import forms

class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = get_user_model()
        fields = ("phone_number",)
        

class CustomUserChangeForm(UserChangeForm):
    class Meta:
        model = get_user_model()
        fields = ("phone_number",)
        
    
class PhoneNumberLoginForm(forms.Form):
    phone_number = forms.CharField(label="Phone Number", max_length=15)
    password = forms.CharField(label="Password", widget=forms.PasswordInput)        


class SignupForm(forms.ModelForm):
    password1 = forms.CharField(label="Password", widget=forms.PasswordInput)
    password2 = forms.CharField(label= "Confirm Password", widget=forms.PasswordInput)
    
    class Meta:
        model = get_user_model()
        fields = ("phone_number", "username", "email")
        
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
    