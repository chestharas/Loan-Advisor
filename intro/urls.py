from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='intro-index'),
]
