from django.urls import path, include
from . import views
app_name = 'rh'
urlpatterns = [
    path('rh/', views.menu_rh, name='menu_rh'),
    path('rh/alta_contrato', views.alta_contrato, name='alta_contrato'),
    path('rh/baja_contrato', views.baja_contrato, name='baja_contrato'),
    path('rh/agendar_entrevista', views.agendar_entrevista, name='agendar_entrevista'),
    path('rh/consultar_contrato', views.consultar_contrato, name='consultar_contrato'),
    path('rh/modificar_contrato', views.modificar_contrato, name='modificar_contrato')
]
