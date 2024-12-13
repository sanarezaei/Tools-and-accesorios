from django.urls import path
from django.contrib.auth.views import LogoutView

from .views import SignUpView, LoginView, otp_verification_view, ProfileView, ProfileUpdateView, PasswordUpdateView, AddressCreateView, AddressListView, AddressUpdateView, AddressDeleteView

app_name = "accounts"

urlpatterns = [
    path('signup/', SignUpView.as_view(), name="signup"),
    path('login/', LoginView.as_view(), name="login"),
    path('logout/', LogoutView.as_view(), name="logout"),
    path('otp/', otp_verification_view, name="otp_verification"),    
    path('profile/', ProfileView.as_view(), name="profile"),
    path('profile/update/', ProfileUpdateView.as_view(), name="profile_update"),
    path('profile/password/', PasswordUpdateView.as_view(), name="password_update"),
    # addresses
    path('', AddressListView.as_view(), name="address_list"),
    path('create/', AddressCreateView.as_view(), name="address_create"),
    path('<int:pk>/update/', AddressUpdateView.as_view(), name="address_update"),
    path('<int:pk>/delete/', AddressDeleteView.as_view(), name="address_delete"),
]
