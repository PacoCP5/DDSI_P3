from django.urls import path, include
from . import views
app_name = 'login'
urlpatterns = [
    path('', views.index, name='index_login'),
    path('login/', views.login, name='login'),
    path('menu/', views.menu, name="menu"),
    path('logout/',views.logout, name="logout")
]
