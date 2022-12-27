from django.urls import path, include
from . import views
app_name = 'clientes'
urlpatterns = [
    path('clientes/', views.menu_cliente, name='menu_clientes'),
    path('clientes/alta', views.alta_cliente, name='alta_cliente'),
    
    path('clientes/view', views.mostrar_clientes, name='mostrar_clientes'),
    path('clientes/viewdates', views.mostrar_citas, name='mostrar_citas'),
    path('clientes/search', views.buscar_clientes, name='buscar_clientes'),
    path('clientes/searchdate', views.buscar_fecha, name='buscar_fecha'),
    path('clientes/searchdate/confirm/<str:pk>', views.confirmar_liberacion_cita, name="confirmar_liberacion"),
    path('clientes/searchdate/reserve/<str:pk>', views.reservar_cita, name="reservar_cita"),
    path('clientes/searchdate/reserve/client/<str:pk>_<str:fecha>', views.asignar_cliente, name="asignar_cliente"),

    path('clientes/search/confirm/<str:pk>', views.confirmar_borrado_cliente, name="confirmar_borrado"),
    path('clientes/search/modify/<str:pk>', views.modificar_cliente, name='modificar_cliente'),
]
