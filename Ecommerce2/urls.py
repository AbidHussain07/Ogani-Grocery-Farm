"""
URL configuration for Ecommerce2 project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.urls import path , include
from Core.views import *

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', home ,name = "Homepage"),
    
    path('category/', category_view ,name = "Category_view"),
    path('category/<cid>/', product_view ,name = "Product_view"),
    path('product/<pid>/', product_detail ,name = "Product_detail"),
    path('blog/', blog_view , name ="Blog"),
    path('contact/', contact_view , name ="Contact"),
    
    path('search/', search_view , name ="Search"),
    
    path('user/', include("Accounts.urls")),
    
    path('add-to-cart/', add_to_cart , name="Add-to-cart"),
    path('cart/', cart_items , name="Cart"),
    
    
    path('delete-from-cart/', delete_item_from_cart , name="delete-from-cart"),
    path('update-cart/', update_cart , name="update-cart"),
    
    path('checkout/', checkout_view , name="check-out"),
    path('order-placed/', after_order_placed , name="order-placed"),
    
    path('dashboard/', customer_dashboard , name="dashboard"),
    path('order-view/<id>', order_view , name="order-view"),
    path('update-address/', update_address , name="update-address"),
    
    path('wishlist/', wishlist_view , name="wishlist"),
    path('add-to-wishlist/', add_to_wishlist , name="add-to-wishlist"),
    path('remove-from-wishlist/', remove_wishlist , name="remove-from-wishlist"),
    
    
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL , document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL , document_root=settings.STATIC_ROOT)
    
urlpatterns += staticfiles_urlpatterns()