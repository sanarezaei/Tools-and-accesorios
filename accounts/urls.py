from django.urls import path

from .views import SignUpView, PhoneNumberLoginView

urlpatterns = [
    path('signup/', SignUpView.as_view(), name="signup"),
    path('login/', PhoneNumberLoginView.as_view(), name="login"),
]
