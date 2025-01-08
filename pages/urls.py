from django.urls import path 

from .views import HomePageView, AboutUsPageView

app_name = "pages"

urlpatterns = [
    path('', HomePageView.as_view(), name="home"),
    path('aboutus/', AboutUsPageView.as_view(), name="aboutus"), 
]
