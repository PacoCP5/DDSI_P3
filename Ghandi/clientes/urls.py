from django.urls import path, include
from . import views

urlpatterns = [
    path('clientes/', views.index, name='index'),
]
