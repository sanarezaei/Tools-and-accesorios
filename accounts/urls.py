from django.urls import path
from django.contrib.auth.views import LogoutView

from .views import SignUpView, LoginView, otp_verification_view, ProfileView

app_name = "accounts"

urlpatterns = [
    path('signup/', SignUpView.as_view(), name="signup"),
    path('login/', LoginView.as_view(), name="login"),
    path('logout/', LogoutView.as_view(), name="logout"),
    path('otp/', otp_verification_view, name="otp_verification"),    
    path('profile/', ProfileView.as_view(), name="profile"),
]
