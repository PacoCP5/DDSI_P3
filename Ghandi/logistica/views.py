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
            return redirect("logistica:hacer_pedido")
        elif 'consultarstock-btn' in keys_request_POST:
            return redirect("logistica:consultar_stock")
        elif 'almacenarproducto-btn' in keys_request_POST:
            return redirect("logistica:almacenar_producto")
        elif 'asignarjaula-btn' in keys_request_POST:
            return redirect("logistica:asingar_jaula")
        elif 'consultardisponibilidadjaulas-btn' in keys_request_POST:
            return redirect("logistica:consultar_disponibilidad_jaulas")
        elif 'vaciarjaula-btn' in keys_request_POST:
            return redirect("logistica:vaciar_jaula")
        elif 'altaproductoalmacen-btn' in keys_request_POST:
            return redirect("logistica:alta_producto_almacen")
    return render(request, 'menu_logistica.html')

def logout(request):
    return HttpResponseRedirect("/menu")

def hacer_pedido(request):
    #form = HacerPedidoForm()
    if request.method == 'POST':
        form = HacerPedidoForm(request.POST)
        if form.is_valid():
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
                sql = "INSERT INTO PEDIDO VALUES ('{0}', '{1}', TO_DATE('{2}','YYYY-DD-MM'), '{3}', '{4}')".format(str(idpedido), str(cantidad), str(fecha), str(pagado), str(idproducto))
                cursor.execute(sql)
                print("llego casi commit")
                bd.ConnectionBD().get_conexion().commit()
                
                messages.success(request, 'Pedido Realizado')
                
                return redirect("logistica:hacer_pedido")
            except:
                error_message="ERROR: No se puede insertar en la tabla"
                return render(request,"hacerpedido.html", {"form": form, "error_message": error_message})
        else:
            error_message="[ERROR] Fallo en los datos introducidos"
            return render(request,"hacerpedido.html",{'form':form, 'error_message':error_message})
    return render(request,"hacerpedido.html", {"form": HacerPedidoForm()})

def consultar_stock(request):
    #form = StockForm()
    if request.method == 'POST':
        keys_request_POST = request.POST.keys()
        if 'consulta1' in keys_request_POST:
            form = StockForm(request.POST)
            if form.is_valid():
                idproducto = form.cleaned_data["idproducto"]
                nombreproducto = form.cleaned_data["nombreproducto"]

                cursor = bd.ConnectionBD().get_conexion().cursor()
                sql = "SELECT * FROM Producto WHERE idproducto='{0}' OR nombre='{1}'".format(str(idproducto),str(nombreproducto).upper())
                print(sql)
                cursor.execute(sql)
                productos = []
                productos = [ {'idproducto':fila[0], 'nombre':fila[1], 'cantidad':fila[2]} for fila in  cursor.fetchall()]
                
                return render(request,'consultarstock.html', {"form": StockForm(), "productos": productos})
            else:
                error_message="[ERROR] Fallo en los datos introducidos"
                return render(request,"hacerpedido.html",{'form':form, 'error_message':error_message})
        elif 'consulta2' in keys_request_POST:
            cursor = bd.ConnectionBD().get_conexion().cursor()
            sql = "SELECT * FROM Producto"
            print(sql)
            cursor.execute(sql)
            productos = []
            productos = [ {'idproducto':fila[0], 'nombre':fila[1], 'cantidad':fila[2]} for fila in  cursor.fetchall()]
            
            return render(request,'consultarstock.html', {"form": StockForm(), "productos": productos})
        
    return render(request,"consultarstock.html", {"form": StockForm()})

def almacenar_producto(request):
    if request.method == 'POST':
        form = AlmacenarForm(request.POST)
        if form.is_valid():
            idproducto = form.cleaned_data["idproducto"]
            cantidad = form.cleaned_data["cantidad"]
            
            if '.' in str(cantidad):
                cant_split = str(cantidad).split('.')
                cantidad = cant_split[0] + ',' + cant_split[1]

            try:
                cursor = bd.ConnectionBD().get_conexion().cursor()
                print("cursor funciona")
                sql = "SELECT cantidad FROM producto WHERE idproducto='{0}'".format(str(idproducto))
                cursor.execute(sql)

                productos = []
                productos = [ {'cantidad':fila[0]} for fila in  cursor.fetchall()]

                if productos == []:
                    error_message="ERROR: El Producto no existe"
                    return render(request,"almacenarproducto.html", {"form": AlmacenarForm, "error_message": error_message})
        
                sql = "UPDATE producto SET cantidad = '{0}'+'{1}' WHERE idproducto='{3}'".format(str(productos[0]), str(cantidad), str(idproducto))
                cursor.execute(sql)

                print("llego casi commit")
                bd.ConnectionBD().get_conexion().commit()
                
                messages.success(request, 'Pedido Realizado')
                
                return redirect("logistica:almacenar_producto")
            except:
                error_message="ERROR: No se puede insertar en la tabla"
                return render(request,"almacenarproducto.html", {"form": AlmacenarForm, "error_message": error_message})
        else:
            error_message="[ERROR] Fallo en los datos introducidos"
            return render(request,"almacenarproducto.html",{'form':AlmacenarForm, 'error_message':error_message})
    return render(request,"almacenarproducto.html", {"form": AlmacenarForm()})


def asignar_jaula(request):
    return HttpResponse("Hello, World!")

def consultar_disponibilidad_jaulas(request):
    if request.method == 'POST':
        keys_request_POST = request.POST.keys()
        if 'consulta1' in keys_request_POST:
            form = DisponibilidadForm(request.POST)
            if form.is_valid():
                idjaula = form.cleaned_data["idjaula"]

                cursor = bd.ConnectionBD().get_conexion().cursor()
                sql = "SELECT * FROM Jaula WHERE idjaula='{0}'".format(str(idjaula))
                print(sql)
                cursor.execute(sql)
                jaulas = []
                jaulas = [ {'idjaula':fila[0], 'idanimal':fila[1], 'tamano':fila[2]} for fila in  cursor.fetchall()]
                
                return render(request,'consultardisponibilidadjaulas.html', {"form": DisponibilidadForm(), "jaulas": jaulas})
            else:
                error_message="[ERROR] Fallo en los datos introducidos"
                return render(request,"consultardisponibilidadjaulas.html",{'form':form, 'error_message':error_message})
        elif 'consulta2' in keys_request_POST:
            cursor = bd.ConnectionBD().get_conexion().cursor()
            sql = "SELECT * FROM jaula"
            print(sql)
            cursor.execute(sql)
            jaulas = []
            jaulas = [ {'idjaula':fila[0], 'idanimal':fila[1], 'tamano':fila[2]} for fila in  cursor.fetchall()]
            
            return render(request,'consultardisponibilidadjaulas.html', {"form": DisponibilidadForm(), "jaulas": jaulas})
        
    return render(request,"consultardisponibilidadjaulas.html", {"form": DisponibilidadForm()})

def vaciar_jaula(request):
    return HttpResponse("Hello, World!")

def alta_producto_almacen(request):
    return HttpResponse("Hello, World!")

def menu_general(request):
    return HttpResponseRedirect("login")