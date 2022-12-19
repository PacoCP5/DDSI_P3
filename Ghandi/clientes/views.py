#from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect
from django.contrib import messages



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



def menu(request):
    return render(request, 'menu.html')

