from django.urls import path
from .views import *
from . import views

urlpatterns = [
    path('register/customer/', views.register_customer, name='register_customer'),
    path('register/showproducer/', views.register_showproducer, name='register_showproducer'),
    path('login/', views.login_view, name='login_view'),
    path('login/admin', views.admin_login, name='admin_login'),
    path('test/', protected_view, name='protected_view')
]