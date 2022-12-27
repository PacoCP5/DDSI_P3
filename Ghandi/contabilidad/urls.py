from django.urls import path, include
from . import views

app_name = 'contabilidad'

urlpatterns = [
    path('contabilidad/', views.menu_contabilidad, name='menu_contabilidad'),
    path('contabilidad/emitir_factura', views.emitir_factura, name='emitir_factura'),
    path('contabilidad/pagar_factura', views.pagar_factura, name='pagar_factura'),
    path('contabilidad/ingreso_salarios', views.ingreso_salarios, name='ingreso_salarios'),
    path('contabilidad/pago_pedidos', views.pago_pedidos, name='pago_pedidos'),
    path('contabilidad/pedidos_pendientes', views.pedidos_pendientes, name='pedidos_pendientes')
]
