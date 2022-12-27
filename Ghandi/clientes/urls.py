from django.urls import path, include
from . import views
app_name = 'clientes'
urlpatterns = [
    path('clientes/', views.menu_cliente, name='menu_clientes'),
    path('clientes/alta', views.alta_cliente, name='alta_cliente'),
     path('clientes/view', views.mostrar_clientes, name='mostrar_clientes'),
    path('clientes/search', views.buscar_clientes, name='buscar_clientes'),
    path('clientes/searchdate', views.buscar_fecha, name='buscar_fecha'),
    path('clientes/search/confirm/<str:pk>', views.confirmar_borrado_cliente, name="confirmar_borrado")

]
