from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('login/', views.login, name='login'),
    path('menu/', views.menu, name='menu'),
    path('menu/logout/',views.logout, name='logout')
]
