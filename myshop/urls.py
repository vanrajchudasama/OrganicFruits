from django.urls import path
from . import views
from django.contrib.auth import views as auth_views


urlpatterns = [
    path('', views.home, name='home'),
    path('product-details/<slug:slug>/', views.product_detail, name='product_detail'),
]