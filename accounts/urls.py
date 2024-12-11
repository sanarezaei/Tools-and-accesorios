from django.urls import path
from .views import SignUpView, PhoneNumberLoginView, otp_verification_view, LogoutView

urlpatterns = [
    path('signup/', SignUpView.as_view(), name="signup"),
    path('login/', PhoneNumberLoginView.as_view(), name="login"),
    path('logout/', LogoutView.as_view(), name="logout"),
    path('otp/', otp_verification_view, name="otp_verification"), 
    
]
