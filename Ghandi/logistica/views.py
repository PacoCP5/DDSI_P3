from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect



# Create your views here.

def index(request):
    return HttpResponse("Hello, World!")

def menu_logistica(request):
    return render(request, "menu_logistica.html")

def hacer_pedido(request):
    return HttpResponse("Hello, World!")

def consultar_stock(request):
    return HttpResponse("Hello, World!")

def almacenar_producto(request):
    return HttpResponse("Hello, World!")

def asignar_jaula(request):
    return HttpResponse("Hello, World!")

def consultar_disponibilidad_jaulas(request):
    return HttpResponse("Hello, World!")

def vaciar_jaula(request):
    return HttpResponse("Hello, World!")

def alta_producto_almacen(request):
    return HttpResponse("Hello, World!")

def menu_general(request):
    return HttpResponseRedirect("login")