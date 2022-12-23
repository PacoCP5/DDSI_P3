#from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect
from django.contrib import messages
from login.views import bd 
from .forms import NuevoClienteForm
import cx_Oracle



def main_cliente(request):
    return render(request, "main_cliente.html")

def alta_cliente(request):
    if request.method == 'POST':
        form = NuevoClienteForm(request.POST)
        if form.is_valid():
            nombre = form.cleaned_data["nombre"]
            apellidos = form.cleaned_data["apellidos"]
            direccion = form.cleaned_data["direccion"]
            telefono = form.cleaned_data["telefono"]
            dni = form.cleaned_data["dni"]
            cuenta_bancaria = form.cleaned_data["cuenta_banco"]
            try:
                
                print("Dando de alta cliente: ", nombre, apellidos)
                cursor = bd.cursor()
                sql = "INSERT INTO cliente(dni, nombre, apellidos, telefono) VALUES ('{0}', '{1}', '{2}', '{3}')".format(str(dni),str(nombre), str(apellidos), str(telefono))
                cursor.execute(sql)
                bd.commit()
                
                messages.success(request, 'Cliente añadido correctamente')
                
                # si se ha conectado bien a la BD, lo redireccionamos  a la url del menú principal de la aplicación
                return redirect("cliente:")
            except:
                 error_message="ERROR: Datos del cliente incorrectos"
                 return render(request,"alta_cliente.html", {"form": form, "error_message": error_message})

    return render(request, "alta_cliente.html", {"form": NuevoClienteForm()})
    
def menu_cliente(request):
    if request.method == 'POST':
        keys_request_POST = request.POST.keys()
        
        if 'alta-cliente-btn' in keys_request_POST:
            return redirect("clientes:alta_cliente")
    return render(request, 'menu_clientes.html')

