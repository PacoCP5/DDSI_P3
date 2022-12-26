from django.urls import path, include
from . import views
app_name = 'logistica'
urlpatterns = [
    #path('menu/', include(('login.urls', 'ghandi'), namespace='rh')),
    path('logistica/', views.menu_logistica, name='menu_logistica'),
    path('logistica/hacer_pedido', views.hacer_pedido, name='hacer_pedido'),
    path('logistica/consultar_stock', views.consultar_stock, name='consultar_stock'),
    path('logistica/almacenar_producto', views.almacenar_producto, name='almacenar_producto'),
    path('logistica/asignar_jaula', views.asignar_jaula, name='asignar_jaula'),
    path('logistica/consultar_disponibilidad_jaulas', views.consultar_disponibilidad_jaulas, name='consultar_disponibilidad_jaulas'),
    path('logistica/vaciar_jaula', views.vaciar_jaula, name='vaciar_jaula'),
    path('logistica/alta_producto_almacen', views.alta_producto_almacen, name='alta_producto_almacen'),
]
