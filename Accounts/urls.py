from django.urls import path
from Accounts import views

urlpatterns = [
    path('register/', views.register_view, name='register'),
    path('login/', views.login_view, name='login'),
    path('log-out/', views.logout_view, name='log-out'),
]

