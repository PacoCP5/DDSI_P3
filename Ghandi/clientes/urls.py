from django.urls import path, include
from . import views
app_name = 'clientes'
urlpatterns = [
    path('clientes/', views.menu_cliente, name='menu_clientes'),
    path('clientes/alta', views.alta_cliente, name='alta_cliente'),
]
