from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib import messages

from login import bd 

from .forms import IngresoSalariosForm

import cx_Oracle
bd = 0

def menu_contabilidad(request):
    if request.method == 'POST':
        keys_request_POST = request.POST.keys()
        
        if 'emitir-factura-btn' in keys_request_POST:
            return redirect("contabilidad:emitir_factura")
        elif 'pagar-factura-btn' in keys_request_POST:
            return redirect("contabilidad:pagar_factura")
        elif 'ingreso-salarios-btn' in keys_request_POST:
            return redirect("contabilidad:ingreso_salarios")
        elif 'pago-pedidos-btn' in keys_request_POST:
            return redirect("contabilidad:pago_pedidos")
        elif 'pedidos-pendientes-btn' in keys_request_POST:
            return redirect("contabilidad:pedidos_pendientes")
        
    return render(request, 'menu_contabilidad.html')

def emitir_factura(request):
    return render(request, 'emitir_factura.html')

def pagar_factura(request):
    return render(request, 'pagar_factura.html')

def ingreso_salarios(request):
    if request.method == 'POST':
        form = IngresoSalariosForm(request.POST)
        if form.is_valid():
            dni=form.cleaned_data["dni"]
            print(dni)
            
    return render(request, 'ingreso_salarios.html')

def pago_pedidos(request):
    return render(request, 'pago_pedidos.html')

def pedidos_pendientes(request):
    return render(request, 'pedidos_pendientes.html')
