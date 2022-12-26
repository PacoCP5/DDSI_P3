#from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect
from django.contrib import messages
from login import bd 
from .forms import NuevoClienteForm, BuscarClienteForm, BuscarFechaForm




def main_cliente(request):
    return render(request, "main_cliente.html")

def mostrar_clientes(request):
    print("Estoy")
    cursor = bd.ConnectionBD().get_conexion().cursor()
    clientes = [] 
    cursor.execute("SELECT dni, nombre, apellidos, telefono FROM cliente")
    
    clientes = [ {'dni':fila[0], 'nombre':fila[1], 'apellido':fila[2], 'telefono':fila[3]} for fila in  cursor.fetchall()]
    print(clientes)
    return render(request,"mostrar_clientes.html", {"clientes": clientes})


def buscar_clientes(request):
    if request.method == 'POST':
        
        form = BuscarClienteForm(request.POST)
        if form.is_valid():
            nombre = form.cleaned_data["nombre"]
            apellidos = form.cleaned_data["apellidos"]
            dni = form.cleaned_data["dni"]
            
            try:
                print("Buscando cliente: ", dni)
                cursor = bd.ConnectionBD().get_conexion().cursor()
                print("Buscando cliente: ", dni)
                clientes = [] 
                sql = "SELECT dni, nombre, apellidos, telefono, direccion, cuentabancaria FROM cliente WHERE dni = '{0}'".format(str(dni))
                print(sql)
                if (nombre != ""):
                    sql +="AND nombre = '{0}'".format(str(nombre))
                if (apellidos != ""):
                    sql +="AND apellidos = '{0}'".format(str(apellidos))
                cursor.execute(sql)
                print(sql)
                clientes = [ {'dni':fila[0], 'nombre':fila[1], 'apellido':fila[2], 'telefono':fila[3], 'direccion':fila[4], 'cuenta':fila[5]} for fila in  cursor.fetchall()]
                print(clientes)
                return render(request,"buscar_clientes.html", {"form":form , "clientes": clientes})
            except:
                error_message="ERROR: Datos del cliente incorrectos"
                return render(request,"buscar_clientes.html", {"form": form, "error_message": error_message})
    return render(request, "buscar_clientes.html", {"form": BuscarClienteForm(), "clientes":[]})


def buscar_fecha(request):
    if request.method == 'POST':
        
        form = BuscarFechaForm(request.POST)
        if form.is_valid():
            fecha = form.cleaned_data["date"]
            
            try:
                print("Buscando fecha: ", fecha)
                cursor = bd.ConnectionBD().get_conexion().cursor()
                clientes = [] 
                sql = "SELECT fechahora FROM cita WHERE disponibilidad = 'Y' AND DATE(fechahora) = '{0}'".format(str(fecha))
                print(sql)
                
                cursor.execute(sql)
                print(sql)
                horas = [ {'hora':fila[0].split(" ")[1].split(',')[0]} for fila in  cursor.fetchall()]
                print(horas)
                return render(request,"buscar_fecha.html", {"form":form , "horas": horas})
            except:
                error_message="ERROR: Datos del cliente incorrectos"
                return render(request,"buscar_fecha.html", {"form": form, "error_message": error_message})
    return render(request, "buscar_fecha.html", {"form": BuscarFechaForm(), "horas":[]})


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
                cursor = bd.ConnectionBD().get_conexion().cursor()
                sql = "INSERT INTO cliente(dni, nombre, apellidos, telefono) VALUES ('{0}', '{1}', '{2}', '{3}')".format(str(dni),str(nombre), str(apellidos), str(telefono))
                cursor.execute(sql)
                bd.ConnectionBD().get_conexion().commit()
                
                messages.success(request, 'Cliente añadido correctamente')
                
                # si se ha conectado bien a la BD, lo redireccionamos  a la url del menú principal de la aplicación
                return redirect("cliente:alta_cliente")
            except:
                 error_message="ERROR: Datos del cliente incorrectos"
                 return render(request,"alta_cliente.html", {"form": form, "error_message": error_message})

    return render(request, "alta_cliente.html", {"form": NuevoClienteForm()})
    
def menu_cliente(request):
    if request.method == 'POST':
        keys_request_POST = request.POST.keys()
        
        if 'alta-cliente-btn' in keys_request_POST:
            return redirect("clientes:alta_cliente")
        elif 'mostrar-clientes-btn' in keys_request_POST:
            return redirect("clientes:mostrar_clientes")
        elif 'buscar-clientes-btn' in keys_request_POST:
            return redirect("clientes:buscar_clientes")
        elif 'buscar-fecha-btn' in keys_request_POST:
            return redirect("clientes:buscar_fecha")
    
    return render(request, 'menu_cliente.html')

