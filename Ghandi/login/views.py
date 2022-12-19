#from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect
from django.contrib import messages

from .forms import LoginBDForm

import cx_Oracle

# Create your views here.
bd = 0 # Variable global para gestionar la conexión a través de todas las funciones
       
def establecer_conexion(username, passwd):
    # se define aquí el atributo que almacena la conexión con la BD de Oracle
    return cx_Oracle.connect( user=username, 
                              password=passwd,
                              dsn="oracle0.ugr.es:1521/practbd.oracle0.ugr.es",
                              encoding="UTF-8")

def cerrar_conexion():
    bd.close()

def index(request):
    return render(request, "base.html")

def login(request):
    if request.method == 'POST':
        form = LoginBDForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data["username"]
            password = form.cleaned_data["password"]
            try:
                global bd # para poder usar la variable global, ha de invocarse
                
                bd = establecer_conexion(username, password)
                # si se ha conectado bien a la BD, lo redireccionamos  a la url del menú principal de la aplicación
                return redirect("menu")
            except:
                 error_message="ERROR: Credenciales de usuario y contraseña incorrectas para la conexión a la base de datos de Oracle"
                 return render(request,"login.html", {"form": form, "error_message": error_message})

    # si no se ha hecho un post o hay errores en los campos del form, se presenta de nuevo el formulario vacío para rellenarlo
    return render(request,"login.html", {"form": LoginBDForm()})

def menu(request):
    return render(request, 'menu.html')



def logout(request):
    cerrar_conexion()
    return redirect("index")
