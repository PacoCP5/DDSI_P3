from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect
from .forms import *
from django.contrib import messages
from login import bd

import cx_Oracle

def index(request):
    return HttpResponse("Hello, World!")

def menu_logistica(request):
    if request.method == 'POST':
        keys_request_POST = request.POST.keys()
        if 'hacerpedido-btn' in keys_request_POST:
            return HttpResponseRedirect("hacer_pedido")
        elif 'consultarstock-btn' in keys_request_POST:
            return HttpResponseRedirect("consultar_stock")
        elif 'almacenarproducto-btn' in keys_request_POST:
            return HttpResponseRedirect("almacenar_producto")
        elif 'asignarjaula-btn' in keys_request_POST:
            return HttpResponseRedirect("asingar_jaula")
        elif 'consultardisponibilidadjaulas-btn' in keys_request_POST:
            return HttpResponseRedirect("consultar_disponibilidad_jaulas")
        elif 'vaciarjaula-btn' in keys_request_POST:
            return HttpResponseRedirect("vaciar_jaula")
        elif 'altaproductoalmacen-btn' in keys_request_POST:
            return HttpResponseRedirect("alta_producto_almacen")
        elif 'atras-btn' in keys_request_POST:
            return logout(request)
    return render(request, 'menu_logistica.html')

def logout(request):
    return HttpResponseRedirect("/menu")

def hacer_pedido(request):
    #form = HacerPedidoForm()
    if request.method == 'POST':
        form = HacerPedidoForm(request.POST)
        if form.is_valid():
            print("HOLA")
            idpedido = form.cleaned_data["idpedido"]
            cantidad = form.cleaned_data["cantidad"]
            fecha = form.cleaned_data["fecha"]
            pagado = form.cleaned_data["pagado"]
            idproducto = form.cleaned_data["idproducto"]

            if '.' in str(cantidad):
                cant_split = str(cantidad).split('.')
                cantidad = cant_split[0] + ',' + cant_split[1]

            try:
                cursor = bd.ConnectionBD().get_conexion().cursor()
                print("cursor funciona")
                sql = "INSERT INTO PEDIDO VALUES ('{0}', '{1}', TO_DATE('{2}','YYYY-DD-MM'), '{3}', '{4}');".format(str(idpedido), str(cantidad), str(fecha), str(pagado), str(idproducto))
                cursor.execute(sql)
                print("llego casi commit")
                bd.ConnectionBD().get_conexion().commit()
                
                messages.success(request, 'Pedido Realizado')
                
                return HttpResponseRedirect('/menu/logistica')
            except:
                messages.error(request, '[ERROR] Fallo al hacer el pedido')
                error_message="ERROR: No se puede insertar en la tabla"
                return render(request,"hacerpedido.html", {"form": form, "error_message": error_message})
        else:
            error_message="[ERROR] Fallo en los datos introducidos"
            return render(request,"hacerpedido.html",{'form':form, 'error_message':error_message})
    return render(request,"hacerpedido.html", {"form": HacerPedidoForm()})

def consultar_stock(request):
    form = StockForm()
    if request.method == 'POST':
        form = StockForm(request.POST)
        if form.is_valid():
            idproducto = form.cleaned_data["idproducto"]
            nombreproducto = form.cleaned_data["nombreproducto"]

            try:
                with bd.get_conexion().cursor() as cursor:
                    if idproducto != "" and nombreproducto != "":
                        sql = "SELECT * FROM Producto WHERE idproducto='{0}' AND nombre='{1}'".format(str(idproducto),str(nombreproducto))
                    elif idproducto == "":
                        sql = "SELECT * FROM Producto WHERE nombre='{0}'".format(str(nombreproducto))
                    else:
                        sql = "SELECT * FROM Producto WHERE idproducto='{0}'".format(str(idproducto))
                    print(sql)
                    cursor.execute(sql)
                    cursor.commit()
                
                messages.success(request, 'Pedido Realizado')
                
                return HttpResponseRedirect('/menu/logistica')
            except:
                messages.error(request, '[ERROR] Fallo al hacer el pedido')
                error_message="ERROR: No se puede insertar en la tabla"
                return render(request,"hacerpedido.html", {"form": form, "error_message": error_message})
        else:
            error_message="[ERROR] Fallo en los datos introducidos"
            return render(request,"hacerpedido.html",{'form':form, 'error_message':error_message})
    return render(request,"hacerpedido.html", {"form": form})
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