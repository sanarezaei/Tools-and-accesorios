from django.urls import path, include
from django.contrib.auth.views import LogoutView

from .views import (SignUpView, CustomLoginView, ProfileView, ProfileUpdateView,
                    PasswordUpdateView, AddressCreateView, AddressListView,
                    AddressUpdateView, AddressDeleteView, OTPVerificationView)

app_name = "accounts"

urlpatterns = [
    path('signup/', SignUpView.as_view(), name="signup"),
    path('login/', CustomLoginView.as_view(), name="login"),
    path('logout/', LogoutView.as_view(), name="logout"),
    path('otp-verify/', OTPVerificationView.as_view(), name="otp_verification"),
    # profile    
    path('profile/', ProfileView.as_view(), name="profile"),
    path('profile/update/', ProfileUpdateView.as_view(), name="profile_update"),
    path('profile/password/', PasswordUpdateView.as_view(), name="password_update"),
    # addresses
    path('addresses/', AddressListView.as_view(), name="address_list"),
    path('addresses/create/', AddressCreateView.as_view(), name="address_create"),
    path('addresses/<int:pk>/update/', AddressUpdateView.as_view(), name="address_update"),
    path('addresses/<int:pk>/delete/', AddressDeleteView.as_view(), name="address_delete"),
]
