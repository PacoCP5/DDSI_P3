from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib import messages

from login import bd 

from .forms import IngresoSalariosForm, FacturaForm, PagoPedidoForm, PagoFacturaForm

import cx_Oracle

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
    form = FacturaForm(request.POST)
    if request.method == 'POST':
        if form.is_valid():
            idfactura=form.cleaned_data["idfactura"]
            dni=form.cleaned_data["dni"]
            cantidad=form.cleaned_data["cantidad"]       
            try:
                with bd.ConnectionBD().get_conexion().cursor() as cursor:
                    # Comprobamos si el id de la factura ya existe
                    sql = "SELECT * FROM FACTURA WHERE IDFACTURA = '{0}'".format(str(idfactura))
                    cursor.execute(sql)
                    
                    if cursor.fetchone() is not None:
                        messages.error(request, '[ERROR] Ya existe una factura con el ID ingresado')
                        return render(request,"emitir_factura.html", {"form": form})
                    else:
                        # Comprobamos si el dni existe
                        sql = "SELECT * FROM CLIENTE WHERE DNI = '{0}'".format(str(dni))
                        cursor.execute(sql)
                        
                        if cursor.fetchone() is None:
                            messages.error(request, '[ERROR] No existe un cliente con el DNI ingresado')
                            return render(request,"emitir_factura.html", {"form": form})
                        else:
                            sql = "INSERT INTO FACTURA VALUES ('{0}','{1}',{2},'N')".format(str(idfactura), str(dni), str(cantidad))
                            cursor.execute(sql)
                            bd.ConnectionBD().get_conexion().commit()
                            messages.success(request, '[INFO] Factura emitida correctamente')
            except:
                messages.error(request, '[ERROR] Fallo al emitir la factura')
                return render(request,"emitir_factura.html", {"form": form})
            
    return render(request, 'emitir_factura.html',{'form':form})

def pagar_factura(request):
    form = PagoFacturaForm(request.POST)
    
    cursor = bd.ConnectionBD().get_conexion().cursor()
    if request.method == 'POST':
        if form.is_valid():
            idfactura=form.cleaned_data["idfactura"]
            sql = "SELECT PAGADO FROM FACTURA WHERE IDFACTURA = '{0}'".format(str(idfactura))
            cursor.execute(sql)
            
            consulta = cursor.fetchone()
            if consulta is not None:    
                pagado = consulta[0]
                                
                if pagado != 'S':
                    sql = "UPDATE FACTURA SET PAGADO = 'S' WHERE IDFACTURA = '{0}'".format(str(idfactura))
                    cursor.execute(sql)
                    bd.ConnectionBD().get_conexion().commit()
                    messages.success(request, '[INFO] Factura pagada correctamente')
                else:
                    messages.error(request, '[ERROR] La factura ya ha sido pagada')
                    return render(request,"pagar_factura.html", {"form": form})
            else:
                messages.error(request, '[ERROR] No existe una factura con el ID ingresado')
                return render(request,"pagar_factura.html", {"form": form})
    
    return render(request, 'pagar_factura.html',{'form':form})

def ingreso_salarios(request):
    form = IngresoSalariosForm(request.POST)
    dni=None
    sueldo=None
    if request.method == 'POST':
        if form.is_valid():
            dni=form.cleaned_data["dni"]
            
            try:
                with bd.ConnectionBD().get_conexion().cursor() as cursor:
                    sql = "SELECT SUELDO FROM CONTRATO WHERE DNI = '{0}'".format(str(dni))
                    
                    cursor.execute(sql)
                    sueldo = cursor.fetchone()

                    if sueldo is None:
                        messages.error(request, '[ERROR] No existe un contrato con el DNI ingresado')
                        return render(request,"ingreso_salarios.html", {"form": form})
                    else:
                        sueldo=sueldo[0]
            
            except:
                messages.error(request, '[ERROR] Fallo al consultar el DNI')
                return render(request,"ingreso_salarios.html", {"form": form})

    return render(request, 'ingreso_salarios.html',{'form':form, "dni": dni, "sueldo": sueldo})

def pago_pedidos(request):
    form = PagoPedidoForm(request.POST)
    
    cursor = bd.ConnectionBD().get_conexion().cursor()
    if request.method == 'POST':
        if form.is_valid():
            idpedido=form.cleaned_data["idpedido"]
            sql = "SELECT PAGADO FROM PEDIDO WHERE IDPEDIDO = '{0}'".format(str(idpedido))
            cursor.execute(sql)
            
            consulta = cursor.fetchone()
            if consulta is not None:    
                pagado = consulta[0]
                                
                if pagado != 'S':
                    sql = "UPDATE PEDIDO SET PAGADO = 'S' WHERE IDPEDIDO = '{0}'".format(str(idpedido))
                    cursor.execute(sql)
                    bd.ConnectionBD().get_conexion().commit()
                    messages.success(request, '[INFO] Pedido pagado correctamente')
                else:
                    messages.error(request, '[ERROR] El pedido ya ha sido pagado')
                    return render(request,"pagar_pedidos.html", {"form": form})
            else:
                messages.error(request, '[ERROR] No existe un pedido con el ID ingresado')
                return render(request,"pagar_pedidos.html", {"form": form})
    
    return render(request, 'pagar_pedidos.html',{'form':form})

def pedidos_pendientes(request):
    
    try:
        cursor= bd.ConnectionBD().get_conexion().cursor()
        pedidos=[]
        sql = "SELECT idpedido, cantidad, fecha, idproducto FROM pedido WHERE pagado='N'"
        cursor.execute(sql)
        pedidos = [ { 'idpedido' : fila[0], 'cantidad' : fila[1], 'fecha' : fila[2], 'idproducto' : fila[3]} for fila in cursor.fetchall() ]
    except:
        messages.error(request, '[ERROR] Fallo al consultar los pedidos pendientes')
        return render(request,"pedidos_pendientes.html")
    
    return render(request, 'pedidos_pendientes.html', {"pedidos": pedidos})
