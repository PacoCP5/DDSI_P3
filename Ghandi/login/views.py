#from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect
from django.contrib import messages

from .forms import LoginBDForm

import cx_Oracle

class Singleton(type):
    _instances = {}
    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(Singleton, cls).__call__(*args, **kwargs)
        return cls._instances[cls]

class BD(metaclass=Singleton):
    def get_conexion(self):
        return self.conexion

    def establecer_conexion(self, username, passwd):
        self.conexion = cx_Oracle.connect(user=username, password=passwd,
                                        dsn="oracle0.ugr.es:1521/practbd.oracle0.ugr.es",
                                        encoding="UTF-8")

    def cerrar_conexion(self):
        self.conexion.close()

def index(request):
    return render(request, "base.html")

def login(request):
    if request.method == 'POST':
        form = LoginBDForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data["username"]
            password = form.cleaned_data["password"]
            try:
                BD().establecer_conexion(username, password)
                return redirect("login:menu")
            except:
                error_message="[ERROR] Credenciales de Usuario y/o Contraseña incorrectas para la conexión a la BD de Oracle"
                return render(request,"login.html", {"form": form, "error_message": error_message})
    return render(request,"login.html", {"form": LoginBDForm()})

def menu(request):
    if request.method == 'POST':
        keys_request_POST = request.POST.keys()
            # Obtengo las claves del diccionario request.POST, que por ejemplo tiene el valor:
            # <QueryDict: {'csrfmiddlewaretoken': ['CHNZtCiLbU'], 'clientes-btn': ['']}> 
            # Me quedo con las claves para coger "clientes-btn", que es la que me interesa 
            # coger (según el boton que pulse y se escoja hacer una acción u otra)
        if 'clientes-btn' in keys_request_POST:
            return HttpResponseRedirect("clientes")
        elif 'contabilidad-btn' in keys_request_POST:
            return HttpResponseRedirect("contabilidad")
        elif 'logistica-btn' in keys_request_POST:
            return HttpResponseRedirect("logistica")
        elif 'animales-btn' in keys_request_POST:
            return HttpResponseRedirect("animales")
        elif 'rh-btn' in keys_request_POST:
            return HttpResponseRedirect("rh")
        elif 'cerrar-btn' in keys_request_POST:
            return logout(request)
    return render(request, 'menu.html')

def logout(request):
    BD().cerrar_conexion()
    return HttpResponseRedirect("/")
