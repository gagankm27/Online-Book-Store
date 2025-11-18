from django.contrib import admin
from django.urls import path
from bookstore1 import views

urlpatterns = [
    path("admin/", admin.site.urls),  # Django admin panel

    path("", views.login_page, name="login"),  # User login page
    path('admin_login/', views.admin_login_page, name='admin_login'),  # Admin login page

    path("home/", views.home, name="home"),  # Home page
    path("crud/", views.crud, name="crud"),  # CRUD page to manage books

    path('add_to_cart/<int:id>/', views.add_to_cart, name='add_to_cart'),  # Add book to cart
    path('cart/', views.cart_page, name='cart'),  # View cart
    path('remove_from_cart/<int:index>/', views.remove_from_cart, name='remove_from_cart'),  # Remove item from cart

    path("checkout/", views.checkout, name="checkout"),  # Checkout and save purchase to CSV
    path("delete-purchase/<int:index>/", views.delete_purchase, name="delete_purchase"),  # Delete purchase entry

    path('delete/<int:id>/', views.delete_book, name='delete_book'),  # Delete book from CRUD
]
