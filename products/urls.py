from django.urls import path

from .views import ProductListView, ProductCreateView, ProductDetailView, CommentListView, CommentCreateView

app_name = "products"

urlpatterns = [
    # Product
    path("", ProductListView.as_view(), name="product_list"),
    path("create/", ProductCreateView.as_view(), name="product_create"), 
    path("<int:pk>/", ProductDetailView.as_view(), name="product_detail"),
    path("<int:pk>/comments/", CommentListView.as_view(), name="comment_list"),
    path("<int:pk>/comments/new/", CommentCreateView.as_view(), name="comment_form"),
]
