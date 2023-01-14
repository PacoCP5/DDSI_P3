from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib import messages

from login import bd 
from .forms import *

import cx_Oracle

def menu_rh(request):
    if request.method == 'POST':
        keys_request_POST = request.POST.keys()
        
        if 'alta_contrato-btn' in keys_request_POST:
            return redirect("rh:alta_contrato")
        elif 'baja_contrato-btn' in keys_request_POST:
            return redirect("rh:baja_contrato")
        elif 'agendar_entrevista-btn' in keys_request_POST:
            return redirect("rh:agendar_entrevista")
        elif 'consultar_contrato-btn' in keys_request_POST:
            return redirect("rh:consultar_contrato")
        elif 'modificar_contrato-btn' in keys_request_POST:
            return redirect("rh:modificar_contrato")
        
    return render(request, 'menu_rh.html')

def alta_contrato(request):
    form = ContratoForm(request.POST)
    if request.method == 'POST':
        if form.is_valid():
            dni = form.cleaned_data["dni"]
            nombre = form.cleaned_data["nombre"]
            apellidos = form.cleaned_data["apellidos"]
            fecha_nacimiento = form.cleaned_data["fecha_nacimiento"]
            telefono = form.cleaned_data["telefono"]
            sueldo = form.cleaned_data["sueldo"]
            cuenta_bancaria = form.cleaned_data["cuenta_bancaria"]
            duracion_contrato = form.cleaned_data["duracion_contrato"]  
            try:
                with bd.ConnectionBD().get_conexion().cursor() as cursor:
                    # Comprobamos si el DNI ya existe
                    sql = "SELECT * FROM CONTRATO WHERE DNI = '{0}'".format(str(dni))
                    cursor.execute(sql)
                    
                    if cursor.fetchone() is not None:
                        messages.error(request, '[ERROR] Ya existe un contrato asociado al DNI ingresado')
                        return render(request,"alta_contrato.html", {"form": form})
                    else:                        
                        sql = "INSERT INTO CONTRATO VALUES ('{0}', '{1}', '{2}', TO_DATE('{3}','YYYY-DD-MM'), '{4}', '{5}', '{6}', '{7}')".format(str(dni), str(nombre), str(apellidos), str(fecha_nacimiento), str(telefono), str(sueldo), str(cuenta_bancaria), str(duracion_contrato))
                        cursor.execute(sql)
                        bd.ConnectionBD().get_conexion().commit()
                        messages.success(request, '[INFO] Contrato guardado correctamente')
            except:
                messages.error(request, '[ERROR] Fallo al guardar el contrato')
                return render(request,"alta_contrato.html", {"form": form})
                
    return render(request, 'alta_contrato.html',{'form':form})


def baja_contrato(request):
    form = DNIForm(request.POST)
    if request.method == 'POST':
        if form.is_valid():
            dni = form.cleaned_data["dni"]

            try:
                with bd.ConnectionBD().get_conexion().cursor() as cursor:
                    # Comprobamos si el DNI existe
                    sql = "SELECT * FROM CONTRATO WHERE DNI = '{0}'".format(str(dni))
                    cursor.execute(sql)
                    
                    if cursor.fetchone() is None:
                        messages.error(request, '[ERROR] No existe un contrato asociado al DNI ingresado')
                        return render(request,"baja_contrato.html", {"form": form})
                    else:                        
                        sql = "DELETE FROM CONTRATO WHERE DNI = '{0}'".format(str(dni))
                        cursor.execute(sql)
                        bd.ConnectionBD().get_conexion().commit()
                        messages.success(request, '[INFO] Contrato eliminado correctamente')
            except:
                messages.error(request, '[ERROR] Fallo al eliminar el contrato')
                return render(request,"baja_contrato.html", {"form": form})
            
    return render(request, 'baja_contrato.html',{'form':form})

def agendar_entrevista(request):
    form = EntrevistaForm(request.POST)
    if request.method == 'POST':
        if form.is_valid():
            dni = form.cleaned_data["dni"]
            nombre = form.cleaned_data["nombre"]
            apellidos = form.cleaned_data["apellidos"]
            fecha = form.cleaned_data["fecha"]
            hora = form.cleaned_data["hora"]
 
            try:
                with bd.ConnectionBD().get_conexion().cursor() as cursor:
                    # Comprobamos si el DNI ya existe
                    sql = "SELECT * FROM ENTREVISTA WHERE DNI = '{0}'".format(str(dni))
                    cursor.execute(sql)
                    
                    if cursor.fetchone() is not None:
                        messages.error(request, '[ERROR] Ya existe una entrevista asociada al DNI ingresado')
                        return render(request,"agendar_entrevista.html", {"form": form})
                    else:                        
                        sql = "INSERT INTO ENTREVISTA VALUES ('{0}', '{1}', '{2}', TO_DATE('{3}','YYYY-DD-MM'), '{4}')".format(str(dni), str(nombre), str(apellidos), str(fecha), str(hora))
                        cursor.execute(sql)
                        bd.ConnectionBD().get_conexion().commit()
                        messages.success(request, '[INFO] Entrevista guardada correctamente')
            except:
                messages.error(request, '[ERROR] Fallo al guardar la entrevista')
                return render(request,"agendar_entrevista.html", {"form": form})
            
    return render(request, 'agendar_entrevista.html',{'form':form})

def consultar_contrato(request):
    form = DNIForm(request.POST)
    
    cursor = bd.ConnectionBD().get_conexion().cursor()
    if request.method == 'POST':
        if form.is_valid():
            dni = form.cleaned_data["dni"]
            sql = "SELECT * FROM CONTRATO WHERE DNI = '{0}'".format(str(dni))
            cursor.execute(sql)
            
            consulta = cursor.fetchone()
            if consulta is not None:    
                contrato = []
                sql = "SELECT * FROM CONTRATO WHERE DNI = '{0}'".format(str(dni))
                cursor.execute(sql)
                contrato = [ {'dni':fila[0], 'nombre':fila[1], 'apellidos':fila[2], 'fecha_nacimiento':fila[3], 'telefono':fila[4], 'cuenta_bancaria':fila[5], 'sueldo':fila[6], 'duracion_contrato':fila[7]} for fila in  cursor.fetchall()]
                return render(request,"mostrar_contrato.html", {"contrato": contrato})     
            else:
                messages.error(request, '[ERROR] No existe un contrato con el DNI ingresado')
                return render(request,"consultar_contrato.html", {"form": form})

    return render(request, 'consultar_contrato.html',{'form':form})

def modificar_contrato(request):
    form = ModificaForm(request.POST)
    
    cursor = bd.ConnectionBD().get_conexion().cursor()
    if request.method == 'POST':
        if form.is_valid():
            dni = form.cleaned_data["dni"]
            nombre = form.cleaned_data["nombre"]
            apellidos = form.cleaned_data["apellidos"]
            fecha_nacimiento = form.cleaned_data["fecha_nacimiento"]
            telefono = form.cleaned_data["telefono"]
            sueldo = form.cleaned_data["sueldo"]
            cuenta_bancaria = form.cleaned_data["cuenta_bancaria"]
            duracion_contrato = form.cleaned_data["duracion_contrato"] 

            try:
                sql = "SELECT * FROM CONTRATO WHERE DNI = '{0}'".format(str(dni))
                cursor.execute(sql)
                consulta = cursor.fetchone()

                if consulta is not None:    
                    sql = "UPDATE CONTRATO SET NOMBRE='{1}', APELLIDOS='{2}',FECHA_NACIM=TO_DATE('{3}','YYYY-DD-MM'),TELEFONO='{4}',SUELDO='{5}',CUENTABANCARIA='{6}',DURACION='{7}' WHERE DNI = '{0}'".format(str(dni), str(nombre), str(apellidos), str(fecha_nacimiento), str(telefono), str(sueldo), str(cuenta_bancaria), str(duracion_contrato))
                    cursor.execute(sql)
                    bd.ConnectionBD().get_conexion().commit()
                    messages.success(request, '[INFO] Contrato modificado correctamente')
                else:
                    messages.error(request, '[ERROR] No existe un contrato con el ID ingresado')
                    return render(request,"modificar_contrato.html", {"form": form})
            except:
                messages.error(request, '[ERROR] Fallo al modificar el contrato')
                return render(request,"modificar_contrato.html", {"form": form})
    
    return render(request, 'modificar_contrato.html',{'form':form})
