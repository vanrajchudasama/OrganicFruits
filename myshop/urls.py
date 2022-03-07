from django.urls import path
from . import views
from django.contrib.auth import views as auth_views


urlpatterns = [
    path('', views.home, name='home'),
    path('product-details/<slug:slug>/', views.product_detail, name='product_detail'),
    path('<slug:slug>/product-reviews/<int:id>/', views.product_reviews_list, name='product_reviews'),
    path('<slug:slug>/product-reviews-form/<int:id>/', views.product_reviews_form, name='product_reviews_form'),
]