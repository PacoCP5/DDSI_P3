from django.urls import path, include
from . import views
app_name = 'animales'
urlpatterns = [
    path('animales/', views.menu_animales, name='menu_animales'),
    path('animales/alta_animal', views.alta_animal, name='alta_animal'),
    path('animales/baja_animal', views.baja_animal, name='baja_animal'),
    #path('animales/consultar_todos_animales', views.consultar_todos_animales, name='consultar_todos_animales'),
    path('animales/buscar_animales', views.buscar_animales, name='buscar_animales'),
    path('animales/modificar_animales', views.modificar_animales, name='modificar_animales'),    
    path('animales/notificar_vacunas', views.notificar_vacunas, name='notificar_vacunas'),
]