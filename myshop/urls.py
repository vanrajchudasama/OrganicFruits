from django.urls import path
from . import views
from django.contrib.auth import views as auth_views


urlpatterns = [
    path('', views.home, name='home'),
    path('product-details/<slug:slug>/', views.product_detail, name='product_detail'),
    path('<slug:slug>/product-reviews/<int:id>/', views.product_reviews_list, name='product_reviews'),
    path('<slug:slug>/product-reviews-form/<int:id>/', views.product_reviews_form, name='product_reviews_form'),
    path('cart/<slug:slug>/<int:id>/', views.add_to_cart, name='my_cart'),
    path('cart/', views.go_to_cart, name='cart'),
    path('cart/item/delete/<int:id>', views.delete_cart_item, name='delete_cart_item'),
    path('cart/item/change', views.change_cart_item, name='change_cart_item'),

]