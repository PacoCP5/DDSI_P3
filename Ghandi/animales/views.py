from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect
from .forms import *
from django.contrib import messages
from login import bd
import numpy as np

#import oracledb

#def index(request):
#    return HttpResponse("Hello, World!")

def logout(request):
    return HttpResponseRedirect("/menu")

def menu_animales(request):
    if request.method == 'POST':
        keys_request_POST = request.POST.keys()
        # Estos son los nombres asociados a los botones del html
        if 'alta_animal-btn' in keys_request_POST:
            return redirect("animales:alta_animal")
        elif 'baja_animal-btn' in keys_request_POST:
            return redirect("animales:baja_animal")
        elif 'consultar_todos_animales-btn' in keys_request_POST:
            return redirect("animales:consultar_todos_animales")
        elif 'buscar_animales-btn' in keys_request_POST:
            return redirect("animales:buscar_animales")
        elif 'modificar_animales-btn' in keys_request_POST:
            return redirect("animales:modificar_animales")
        elif 'notificar_vacunas-btn' in keys_request_POST:
            return redirect("animales:notificar_vacunas")
        elif 'atras-btn' in keys_request_POST:
            return logout(request)
    return render(request, 'menu_animales.html')    

def obtener_ids():
    cursor = bd.ConnectionBD().get_conexion().cursor()
    cursor.execute("SELECT IDANIMAL FROM ANIMAL")
    ids = [ fila[0] for fila in cursor.fetchall()]
    return ids

def obtener_dnis():
    cursor = bd.ConnectionBD().get_conexion().cursor()
    cursor.execute("SELECT DNI FROM CLIENTE")
    dnis = [ fila[0] for fila in cursor.fetchall()]
    return dnis

def alta_animal(request):
    if request.method == 'POST':
        form = AltaAnimalForm(request.POST)
        if form.is_valid():
            id_animal = form.cleaned_data["idAnimal"]
            dni_duenio = form.cleaned_data["dni_duenio"]
            tipo = form.cleaned_data["tipo"]
            especie = form.cleaned_data["especie"]

            # Comprobamos si el ID no es repetido

            existe = False
            ids = obtener_ids()
            for id in ids: 
                if(id == id_animal): 
                    existe = True
                    break

            if(existe == True): 
                error_message="ERROR: Ya existe un animal con ese ID."
                messages.error(request, error_message)

            else:

                # Comprobamos si el dueño está dado de alta            
                existe = False
                dnis = obtener_dnis()
                for dni in dnis: 
                    if(dni == dni_duenio): 
                        existe = True
                        break

                if(existe == False): 
                    error_message="ERROR: El DNI introducido no se corresponde con ningún cliente dado de alta."
                    messages.error(request, error_message)

                else:

                    try:
                        
                        print("Dando de alta el animal con ID: ", id_animal)
                        cursor = bd.ConnectionBD().get_conexion().cursor()
                        sql = "INSERT INTO animal(idanimal, dni, tipo, especie) VALUES ('{0}', '{1}', '{2}', '{3}')".format(str(id_animal),str(dni_duenio), str(tipo), str(especie))
                        print(sql)
                        cursor.execute(sql)
                        bd.ConnectionBD().get_conexion().commit()
                        
                        messages.success(request, 'Animal añadido correctamente')
                        return redirect("animales:alta_animal")
                    except:
                        error_message="ERROR: Datos del animal incorrectos"
                        return render(request,"alta_animal.html", {"form": form, "error_message": error_message})

    return render(request, "alta_animal.html", {"form": AltaAnimalForm()})

def baja_animal(request):
    if request.method == 'POST':
        form = IDAnimalForm(request.POST)
        if form.is_valid():
            id_animal = form.cleaned_data["idAnimal"]

            # Comprobamos si el ID existe

            existe = False
            ids = obtener_ids()
            for id in ids: 
                if(id == id_animal): 
                    existe = True
                    break

            if(existe == False): 
                error_message="ERROR: NO existe un animal con ese ID."
                messages.error(request, error_message)

            else:
                try: 
                    print("Dando de baja el animal con ID: ", id_animal)
                    cursor = bd.ConnectionBD().get_conexion().cursor()
                    
                    cursor.execute("UPDATE JAULA SET IDANIMAL = null WHERE IDANIMAL = '{}'".format(str(id_animal)))
                    print("Jaula liberada correctamente")
                    bd.ConnectionBD().get_conexion().commit()

                    sql = "DELETE FROM animal WHERE idanimal = '{}'".format(str(id_animal))
                    print(sql)
                    cursor2 = bd.ConnectionBD().get_conexion().cursor()
                    cursor2.execute(sql)

                    bd.ConnectionBD().get_conexion().commit()
                    messages.success(request, 'Animal borrado correctamente')
                    return redirect("animales:baja_animal")
                except:
                   error_message="ERROR: ID del Animal incorrecto."
                   return render(request,"baja_animal.html", {"form": form, "error_message": error_message})

    return render(request, "baja_animal.html", {"form": IDAnimalForm()})

def consultar_todos_animales(request, url = None):
    cursor = bd.ConnectionBD().get_conexion().cursor()
    animales = [] 
    cursor.execute("SELECT * FROM ANIMAL")
    
    animales = [ {'id_animal':fila[0], 'dni':fila[1], 'tipo':fila[2], 'especie':fila[3]} for fila in  cursor.fetchall()]
    print(animales)
    return render(request,"consultar_todos_animales.html", {"animales": animales})

def buscar_animales(request):
    if request.method == 'POST':
        form = BuscarAnimalForm(request.POST)
        if form.is_valid():
            
            id_animal = form.cleaned_data["idAnimal"]
            dni_duenio = form.cleaned_data["dni"]
            tipo = form.cleaned_data["tipo"]
            especie = form.cleaned_data["especie"]

            #attrs = ['idAnimal','dni','tipo','especie']
            values = [id_animal, dni_duenio, tipo, especie]
            empty = []

            for i, s in enumerate(values): 
                empty.append(1 if s == "" else 0)

            print("HHHHHH ", empty)

            # Si el usuario no mete ningún valor, mostramos todos los animales.
            print(min(empty))
            if (min(empty) == 1): 
                cursor = bd.ConnectionBD().get_conexion().cursor()
                animales = [] 
                cursor.execute("SELECT * FROM ANIMAL")
                
                animales = [ {'id_animal':fila[0], 'dni':fila[1], 'tipo':fila[2], 'especie':fila[3]} for fila in  cursor.fetchall()]
                print(animales)
                return render(request,"consultar_todos_animales.html", {"animales": animales})

            else: 
                try:
                    print("Consultando animales: ")
                    cursor = bd.ConnectionBD().get_conexion().cursor()
                    primero = True

                    sql = "SELECT * FROM animal WHERE "
                    if (id_animal != ""):
                        sql += "idanimal='{0}'".format(str(id_animal))
                        primero = False

                    if (dni_duenio != ''): 
                        if(primero == False):
                            sql += " and dni='{0}'".format(str(dni_duenio))
                        else:
                            sql += "dni='{0}'".format(str(dni_duenio))
                            primero = False

                    if (tipo != ''): 
                        if(primero == False):
                            sql += " and tipo='{0}'".format(str(tipo))
                        else:
                            sql += "tipo='{0}'".format(str(tipo))
                            primero = False
                    
                    if (especie != ''):
                        if(primero == False):
                            sql += " and especie='{0}'".format(str(especie))
                        else: 
                            sql += "especie='{0}'".format(str(especie))

                    #sql += ";"
                    print(sql)
                    cursor.execute(sql)
                    bd.ConnectionBD().get_conexion().commit()
                                        
                    # si se ha conectado bien a la BD, lo redireccionamos  a la url del menú principal de la aplicación
                    animales = [ {'id_animal':fila[0], 'dni':fila[1], 'tipo':fila[2], 'especie':fila[3]} for fila in  cursor.fetchall()]
                    print(animales)
                    print(bool(animales))
                    if (bool(animales) == False): 
                        messages.error(request, 'No existe ningún animal con esos datos')
                        return render(request, "buscar_animales.html", {"form": BuscarAnimalForm()})
                    else:
                        messages.success(request, 'Animal consultado correctamente')
                        return render(request,"consultar_todos_animales.html", {"animales": animales})
                    
                except:
                    error_message="ERROR: Datos del animal incorrectos"
                    return render(request,"buscar_animales.html", {"form": form, "error_message": error_message})
    return render(request, "buscar_animales.html", {"form": BuscarAnimalForm(), "animales":[]})

def modificar_animales(request):
    if request.method == 'POST':
        form = ModificarAnimalForm(request.POST)
        if form.is_valid():
            id_animal_antiguo = form.cleaned_data["idAnimal_antiguo"]
            id_animal_nuevo = form.cleaned_data["idAnimal_nuevo"]
            dni_duenio = form.cleaned_data["dni_duenio"]
            tipo = form.cleaned_data["tipo"]
            especie = form.cleaned_data["especie"]

            # Comprobamos si el ID está dado de alta

            existe = False
            ids = obtener_ids()
            for id in ids: 
                if(id == id_animal_antiguo): 
                    existe = True
                    break

            if(existe == False): 
                error_message="ERROR: No existe un animal con ese ID."
                messages.error(request, error_message)

            else:
 
                try:
                    
                    print("Modificando el animal con ID: ", id_animal_antiguo)
                    cursor = bd.ConnectionBD().get_conexion().cursor()
                    
                    primero = True

                    sql = "UPDATE animal SET "
                    if (id_animal_nuevo != ''):
                        sql += "idanimal='{0}'".format(str(id_animal_nuevo))
                        primero = False

                    if (dni_duenio != ''): 
                        if(primero == False):
                            sql += ", dni='{0}'".format(str(dni_duenio))
                        else:
                            sql += "dni='{0}'".format(str(dni_duenio))
                            primero = False

                    if (tipo != ''): 
                        if(primero == False):
                            sql += ", tipo='{0}'".format(str(tipo))
                        else:
                            sql += "tipo='{0}'".format(str(tipo))
                            primero = False

                    if (especie != ''):
                        if(primero == False):
                            sql += ", especie='{0}'".format(str(especie))
                        else: 
                            sql += "especie='{0}'".format(str(especie))

                    sql += " WHERE idanimal='{0}'".format( str(id_animal_antiguo))
                    print(sql)
                    cursor.execute(sql)
                    print("AAAAAAAAA")
                    bd.ConnectionBD().get_conexion().commit()
                    
                    messages.success(request, 'Animal modificado correctamente')
                    
                    # si se ha conectado bien a la BD, lo redireccionamos  a la url del menú principal de la aplicación
                    return redirect("animales:modificar_animales")
                except:
                    messages.error(request, 'Error al añadir el animal: el DNI del dueño no es válido')
                    error_message="ERROR: Datos del animal incorrectos"
                    return render(request,"modificar_animales.html", {"form": form, "error_message": error_message})

    return render(request, "modificar_animales.html", {"form": ModificarAnimalForm()})

def notificar_vacunas(request):
    if request.method == 'POST':
        form = IDAnimalForm(request.POST)
        if form.is_valid():
            id_animal = form.cleaned_data["idAnimal"]

            # Comprobamos si el ID existe

            existe = False
            ids = obtener_ids()
            for id in ids: 
                if(id == id_animal): 
                    existe = True
                    break

            if(existe == False): 
                error_message="ERROR: NO existe un animal con ese ID."
                messages.error(request, error_message)

            else:
                try: 

                    print("Obteniendo el dueño del animal con ID: ", id_animal)
                    cursor = bd.ConnectionBD().get_conexion().cursor()
                    cursor.execute("SELECT dni FROM ANIMAL WHERE idanimal = '{}'".format(str(id_animal)))

                    # obtenemos el dni asociado al animal
                    dni = [fila[0] for fila in  cursor.fetchall()][0]
                    print(dni)

                    # obtenemos los datos del dueño asociado
                    cursor.execute("SELECT dni, nombre, apellidos, telefono FROM CLIENTE WHERE dni = '{}'".format(str(dni)))
                    duenio = [ {'nombre':fila[1], 'apellido':fila[2], 'telefono':fila[3]} for fila in cursor.fetchall()][0]

                    print(duenio)

                    msg = "Notificación realizada correctamente. Se ha enviado un mensaje recordatorio sobre la vacuna al telefono {}. \
                        Este número pertenece a {} {}, con DNI {} y dueño del animal con ID {}.".format(duenio['telefono'], duenio['nombre'], duenio['apellido'], dni, id_animal)
                    messages.success(request, msg)
                    
                    # si se ha conectado bien a la BD, lo redireccionamos  a la url del menú principal de la aplicación
                    return redirect("animales:notificar_vacunas")

                except:
                        error_message="ERROR: ID del Animal incorrecto."
                        return render(request,"notificar_vacunas.html", {"form": form, "error_message": error_message})

    return render(request, "notificar_vacunas.html", {"form": IDAnimalForm()})