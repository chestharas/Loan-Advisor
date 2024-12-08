from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='auth-index'),
    path('signup/', views.signup, name='auth-signup'),
    path('sign-in/', views.sign_in, name='auth-sign-in'),
    path('verify/', views.verify_otp, name='auth-verify'),
    path('get-otp/', views.generate_otp, name='auth-get-otp'), 
    path('create-password/', views.create_password, name='auth-create-password'),
]
