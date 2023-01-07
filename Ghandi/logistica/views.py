from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect
from .forms import HacerPedidoForm, StockForm, AlmacenarForm, DisponibilidadForm, AsignarForm, AltaProductoForm
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
            return redirect("logistica:asignar_jaula")
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
            print(cantidad)
            if (',' not in str(cantidad) and '.' not in str(cantidad)):
                cantidad = str(cantidad) + '.0'  
            print(cantidad)          
            if ',' in str(cantidad):
                cant_split = (str(cantidad)).split(',')
                cantidad = cant_split[0] + '.' + cant_split[1]
            print(cantidad)
            try:
                a = float(str(cantidad))
            except:
                error_message="ERROR: Cantidad en Formato Incorrecto"
                return render(request,"hacerpedido.html", {"form": form, "error_message": error_message})
        
            print(fecha)
            cantidad_split = str(fecha).split('-')
            if len(cantidad_split) != 3 or len(cantidad_split[0]) != 4 or len(cantidad_split[1]) != 2 or len(cantidad_split[2]) != 2:
                error_message="ERROR: Fecha en Formato Incorrecto"
                return render(request,"hacerpedido.html", {"form": form, "error_message": error_message})
            print(str(pagado))
            if (str(pagado) not in ['S','N']) and str(pagado) != '' and str(pagado) != 'None':
                error_message="ERROR: El atributo Pagado debe ser 'S' (sí) o 'N' (no)"
                return render(request,"hacerpedido.html", {"form": form, "error_message": error_message})
            elif (pagado == 'None' or pagado == ''):
                pagado = 'N'

            try:
                cursor = bd.ConnectionBD().get_conexion().cursor()
                
                if str(idpedido) == 'None':
                    sql = "SELECT idpedido FROM pedido"
                    cursor.execute(sql)
                    print("cursor funciona2")
                    pedidos = []
                    pedidos = [ {'idpedido':fila[0]} for fila in  cursor.fetchall()]
                    ids = []
                    for pedido in pedidos:
                        ids.append(int(pedido['idpedido']))
                    print(ids)
                    ids.sort(reverse=True)
                    print(ids)
                    idpedido = ids[0]+1
                else:
                    sql = "SELECT idpedido FROM pedido WHERE idpedido={0}".format(str(idpedido))
                    cursor.execute(sql)
                    print("cursor funciona2")
                    pedidos = []
                    pedidos = [ {'idpedido':fila[0]} for fila in  cursor.fetchall()]

                    if pedidos != []:
                        error_message="ERROR: Ya existe un Pedido con ese idPedido"
                        return render(request,"hacerpedido.html", {"form": form, "error_message": error_message})
                
                sql = "SELECT idproducto FROM producto WHERE idproducto={0}".format(str(idproducto))
                cursor.execute(sql)
                print("cursor funciona2")
                productos = []
                productos = [ {'idproducto':fila[0]} for fila in  cursor.fetchall()]

                if productos == []:
                    error_message="ERROR: Ese Producto no está registrado, debes darlo de alta primero"
                    return render(request,"hacerpedido.html", {"form": form, "error_message": error_message})
            
                print("cursor funciona4")
                sql = "INSERT INTO PEDIDO VALUES ({0}, {1}, TO_DATE('{2}','YYYY-DD-MM'), '{3}', {4})".format(str(idpedido), str(cantidad), str(fecha), str(pagado), str(idproducto)) 
                print(sql)
                cursor = bd.ConnectionBD().get_conexion().cursor()
                cursor.execute(sql)

                print("llego casi commit")
                bd.ConnectionBD().get_conexion().commit()
                
                messages.success(request, '    Producto Registrado con Éxito')
                
                return redirect("logistica:hacer_pedido")
            except:
                error_message="ERROR: El SGBD no ha aceptado la operación"
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
                if productos == []:
                    error_message="ERROR: El Producto no existe"
                    return render(request,"consultarstock.html", {"form": StockForm, "error_message": error_message})
                
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

            if (',' not in str(cantidad) and '.' not in str(cantidad)):
                cantidad = str(cantidad) + '.0'            
            if ',' in str(cantidad):
                cant_split = str(cantidad).split(',')
                cantidad = cant_split[0] + '.' + cant_split[1]

            try:
                cursor = bd.ConnectionBD().get_conexion().cursor()
                print("cursor funciona")
                sql = "SELECT cantidad FROM producto WHERE idproducto='{0}'".format(str(idproducto))
                cursor.execute(sql)
                print("cursor funciona2")
                productos = []
                productos = [ {'cantidad':fila[0]} for fila in  cursor.fetchall()]
                
                print("cursor funciona3")
                if productos == []:
                    error_message="ERROR: El Producto no existe"
                    return render(request,"almacenarproducto.html", {"form": AlmacenarForm, "error_message": error_message})
                print("cursor funciona4")
                old_cantidad = str(productos[0]['cantidad'])
                print(old_cantidad)
                print(cantidad)
                print(old_cantidad + '+' + str(cantidad))
                sql = "UPDATE producto SET cantidad = {0}+{1} WHERE idproducto={2}".format(str(old_cantidad), str(cantidad), str(idproducto))
                print(sql)
                cursor = bd.ConnectionBD().get_conexion().cursor()
                cursor.execute(sql)

                print("llego casi commit")
                bd.ConnectionBD().get_conexion().commit()
                
                messages.success(request, '    Pedido Realizado con Éxito')
                
                return redirect("logistica:almacenar_producto")
            except:
                error_message="ERROR: El SGBD no ha aceptado la operación"
                return render(request,"almacenarproducto.html", {"form": AlmacenarForm, "error_message": error_message})
        else:
            error_message="[ERROR] Fallo en los datos introducidos"
            return render(request,"almacenarproducto.html",{'form':AlmacenarForm, 'error_message':error_message})
    return render(request,"almacenarproducto.html", {"form": AlmacenarForm()})


def asignar_jaula(request):
    if request.method == 'POST':
        form = AsignarForm(request.POST)
        if form.is_valid():
            idjaula = form.cleaned_data["idjaula"]
            idanimal = form.cleaned_data["idanimal"]

            try:
                cursor = bd.ConnectionBD().get_conexion().cursor()
                print("cursor funciona")
                sql = "SELECT idanimal FROM animal WHERE idanimal='{0}'".format(str(idanimal))
                cursor.execute(sql)
                
                animal = []
                animal = [ {'idjaula':fila[0]} for fila in  cursor.fetchall()]
                
                if animal == []:
                    error_message="ERROR: El Animal no existe"
                    return render(request,"asignarjaula.html", {"form": AsignarForm(), "error_message": error_message})
            
                sql = "SELECT idjaula FROM jaula WHERE idanimal='{0}'".format(str(idanimal))
                cursor.execute(sql)
                
                animal = []
                animal = [ {'idjaula':fila[0]} for fila in  cursor.fetchall()]
                
                if animal != []:
                    error_message="ERROR: El Animal ya estaba asignado a otra Jaula. Vacíala primero"
                    return render(request,"asignarjaula.html", {"form": AsignarForm(), "error_message": error_message})
            
                sql = "SELECT idanimal FROM jaula WHERE idjaula='{0}'".format(str(idjaula))
                cursor.execute(sql)
                
                animal = []
                animal = [ {'idanimal':fila[0]} for fila in  cursor.fetchall()]
                print(animal[0]['idanimal'])
                if str(animal[0]['idanimal']) != 'None':
                    error_message="ERROR: La Jaula no está vacía"
                    return render(request,"asignarjaula.html", {"form": AsignarForm(), "error_message": error_message})
            
                sql = "UPDATE jaula SET idanimal = {0} WHERE idjaula={1}".format(str(idanimal), str(idjaula))
                print(sql)
                cursor = bd.ConnectionBD().get_conexion().cursor()
                cursor.execute(sql)

                print("llego casi commit")
                bd.ConnectionBD().get_conexion().commit()
                
                messages.success(request, '    Animal asignado con Éxito')
                
                return redirect("logistica:asignar_jaula")
            except:
                error_message="ERROR: La Jaula no existe"
                return render(request,"asignarjaula.html", {"form": AsignarForm(), "error_message": error_message})
        else:
            error_message="[ERROR] Fallo en los datos introducidos"
            return render(request,"asignarjaula.html",{'form':AsignarForm(), 'error_message':error_message})
    return render(request,"asignarjaula.html", {"form": AsignarForm()})


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
                if jaulas == []:
                    error_message="ERROR: La Jaula no existe"
                    return render(request,"consultardisponibilidadjaulas.html", {"form": DisponibilidadForm(), "error_message": error_message})
                
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
    if request.method == 'POST':
        form = DisponibilidadForm(request.POST)
        if form.is_valid():
            idjaula = form.cleaned_data["idjaula"]

            try:
                cursor = bd.ConnectionBD().get_conexion().cursor()
                print("cursor funciona")
                sql = "SELECT idanimal FROM jaula WHERE idjaula='{0}'".format(str(idjaula))
                cursor.execute(sql)
                
                animal = []
                animal = [ {'idanimal':fila[0]} for fila in  cursor.fetchall()]
                
                if str(animal[0]['idanimal']) == 'None':
                    error_message="ERROR: La Jaula ya estaba Vacía"
                    return render(request,"vaciarjaula.html", {"form": DisponibilidadForm(), "error_message": error_message})
            
                sql = "UPDATE jaula SET idanimal = '' WHERE idjaula={0}".format(str(idjaula))
                print(sql)
                cursor = bd.ConnectionBD().get_conexion().cursor()
                cursor.execute(sql)

                print("llego casi commit")
                bd.ConnectionBD().get_conexion().commit()
                
                messages.success(request, '    Jaula vaciada con Éxito')
                
                return redirect("logistica:vaciar_jaula")
            except:
                error_message="ERROR: La Jaula no existe"
                return render(request,"vaciarjaula.html", {"form": DisponibilidadForm(), "error_message": error_message})
        else:
            error_message="[ERROR] Fallo en los datos introducidos"
            return render(request,"vaciarjaula.html",{'form':DisponibilidadForm(), 'error_message':error_message})
    return render(request,"vaciarjaula.html", {"form": DisponibilidadForm()})



def alta_producto_almacen(request):
    if request.method == 'POST':
        form = AltaProductoForm(request.POST)
        if form.is_valid():
            idproducto = form.cleaned_data["idproducto"]
            nombreproducto = form.cleaned_data["nombreproducto"]
            print(idproducto)
            try:
                cursor = bd.ConnectionBD().get_conexion().cursor()
                
                if str(idproducto) == 'None':
                    sql = "SELECT idproducto FROM producto"
                    cursor.execute(sql)
                    print("cursor funciona2")
                    productos = []
                    productos = [ {'idproducto':fila[0]} for fila in  cursor.fetchall()]
                    ids = []
                    for producto in productos:
                        print(int(producto['idproducto']))
                        ids.append(int(producto['idproducto']))
                    print(ids)
                    ids.sort(reverse=True)
                    print(ids)
                    idproducto = ids[0]+1
                else:
                    sql = "SELECT idproducto FROM producto WHERE idproducto={0}".format(str(idproducto))
                    cursor.execute(sql)
                    print("cursor funciona2")
                    productos = []
                    productos = [ {'idproducto':fila[0]} for fila in  cursor.fetchall()]

                    if productos != []:
                        error_message="ERROR: Ya existe un Producto con ese idProducto"
                        return render(request,"altaproducto.html", {"form": AltaProductoForm(), "error_message": error_message})
                
                print("cursor funciona4")
                sql = "INSERT INTO producto(idproducto, nombre,cantidad) VALUES ({0},'{1}',0.0)".format(str(idproducto),str(nombreproducto))
                print(sql)
                cursor = bd.ConnectionBD().get_conexion().cursor()
                cursor.execute(sql)

                print("llego casi commit")
                bd.ConnectionBD().get_conexion().commit()
                
                messages.success(request, '    Producto Registrado con Éxito')
                
                return redirect("logistica:alta_producto_almacen")
            except:
                error_message="ERROR: El SGBD no ha aceptado la operación"
                return render(request,"altaproducto.html", {"form": AltaProductoForm(), "error_message": error_message})
        else:
            error_message="[ERROR] Fallo en los datos introducidos"
            return render(request,"altaproducto.html",{'form':AltaProductoForm(), 'error_message':error_message})
    return render(request,"altaproducto.html", {"form": AltaProductoForm()})


def menu_general(request):
    return HttpResponseRedirect("login")