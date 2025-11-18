from django.contrib import admin
from django.urls import path
from bookstore1 import views

urlpatterns = [
    path('admin/', admin.site.urls),

    # LOGIN
    path("", views.login_page, name="login_page"),
    path("home/", views.home, name="home"),
    # CRUD
    path('crud/', views.crud, name='crud'),
    path('delete/<int:id>/', views.delete_book, name='delete_book'),

    # CART
    path('cart/', views.cart_page, name='cart'),
    path('add_to_cart/<int:book_id>/', views.add_to_cart, name='add_to_cart'),
    # PURCHASE MANAGEMENT - Admin
    path("delete-purchase/<int:index>/", views.delete_purchase, name="delete_purchase"),
    path("delete-purchase/<int:index>/", views.delete_purchase, name="delete_purchase"),
    path('remove_from_cart/<int:index>/', views.remove_from_cart, name='remove_from_cart'),
    
]
