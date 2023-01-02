#from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect
from django.contrib import messages
from login import bd 
from .forms import NuevoClienteForm, BuscarClienteForm, BuscarFechaForm
from .tables import ClienteTabla, ClienteTablaCompleta, Horas
from datetime import datetime
from django.urls import reverse
busqueda_cliente =""
clientes_g = ""
def main_cliente(request):
    return render(request, "main_cliente.html")

def mostrar_clientes(request):

    cursor = bd.ConnectionBD().get_conexion().cursor()
    clientes = [] 
    cursor.execute("SELECT dni, nombre, apellidos, telefono FROM cliente")
    
    clientes = [ {'dni':fila[0], 'nombre':fila[1], 'apellido':fila[2], 'telefono':fila[3]} for fila in  cursor.fetchall()]
    return render(request,"mostrar_clientes.html", {"clientes": clientes})

def mostrar_citas(request):

    cursor = bd.ConnectionBD().get_conexion().cursor()
    clientes = [] 
    cursor.execute("SELECT fechahora, cita.dni, nombre, apellidos FROM cita LEFT JOIN cliente on cita.dni = cliente.dni")
    
    citas = [ {'fecha':fila[0],'dni':fila[1], 'nombre':fila[2], 'apellido':fila[3]} for fila in  cursor.fetchall()]

    return render(request,"mostrar_citas.html", {"citas": citas})


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
            fecha = form.cleaned_data["date"].strftime("%d/%m/%y")
            
            try:
                print("Buscando fecha: ", fecha)
                cursor = bd.ConnectionBD().get_conexion().cursor()
                horas = [] 

                sql = "SELECT fechahora FROM cita WHERE disponibilidad = 'Y' AND TO_CHAR(fechahora, 'DD/MM/YY' ) LIKE '{0}'".format(str(fecha))
                print(sql)
                
                cursor.execute(sql)
                
                horas = [ {'fecha':fila[0],'hora':fila[0].strftime("%H:%M")} for fila in  cursor.fetchall()]
                
                return render(request,"buscar_fecha.html", {"form":form , "horas": horas})
            except:
                error_message="ERROR: Datos de fecha incorrectos"
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
    

def modificar_cliente(request, pk):
    if request.method == 'POST':
        form = NuevoClienteForm(request.POST)
        if form.is_valid():
            print(form.cleaned_data)
            nombre = form.cleaned_data["nombre"]
            apellidos = form.cleaned_data["apellidos"]
            direccion = form.cleaned_data["direccion"]
            telefono = form.cleaned_data["telefono"]
            dni = form.cleaned_data["dni"]
            cuenta_bancaria = form.cleaned_data["cuenta_banco"]
                
            print("Modificando cliente: ", nombre, apellidos)
            cursor = bd.ConnectionBD().get_conexion().cursor()

            sql = "UPDATE cliente SET "
            if (dni != '') :sql += "dni='{0}'".format(str(dni))
            if (nombre != '') :sql += ", nombre='{0}'".format(str(nombre))
            if (apellidos != '') :sql += ", apellidos='{0}'".format(str(apellidos))
            if (direccion != '') :sql += ", direccion='{0}'".format(str(direccion))
            if (telefono != '') :sql += ", telefono='{0}'".format(str(telefono))
            if (cuenta_bancaria != '') :sql += ", cuentabancaria='{0}'".format(str(cuenta_bancaria))
            sql += "WHERE dni='{0}'".format( str(pk))
            print(sql)

            cursor.execute(sql)
            bd.ConnectionBD().get_conexion().commit()
            
            messages.success(request, 'Cliente modificado correctamente')
            
            # si se ha conectado bien a la BD, lo redireccionamos  a la url del menú principal de la aplicación
            return redirect("clientes:mostrar_clientes")
            
    valores_iniciales = {'dni':pk}
    
    sql = "SELECT dni, nombre, apellidos, telefono, direccion, cuentabancaria FROM cliente WHERE dni = '{0}'".format(str(pk))
    try:
        cursor = bd.ConnectionBD().get_conexion().cursor()
        cursor.execute(sql)
        cliente = cursor.fetchall()[0]
        if (cliente[1]!=''): valores_iniciales['nombre']=cliente[1]
        if (cliente[2]!=''): valores_iniciales['apellidos']=cliente[2]
        if (cliente[3]!=''): valores_iniciales['telefono']=cliente[3]
        if (cliente[4]!=''): valores_iniciales['direccion']=cliente[4]

        if (cliente[5]!=''): valores_iniciales['cuenta_banco']=cliente[5]

        form = NuevoClienteForm(initial=valores_iniciales)
        return render(request, "modificar_cliente.html", {"form": form})
    except:
        form = NuevoClienteForm(initial={'dni':pk})
        error_message="ERROR: No se han podido cargar los datos iniciales"
        return render(request,"modificar_cliente.html", {"form": form, "error_message": error_message})
    
            
def confirmar_borrado_cliente(request, pk):
    if request.method == 'POST':
        keys_request_POST = request.POST.keys()
        
        if 'borrar-btn' in keys_request_POST:
            print("aqui")
            try:
                print("Borrando cliente: ", pk)
                cursor = bd.ConnectionBD().get_conexion().cursor()

                sql = "DELETE FROM CLIENTE WHERE DNI LIKE '{0}'".format(str(pk))
                print(sql)
                
                cursor.execute(sql)
                bd.ConnectionBD().get_conexion().commit()
                return redirect("clientes:mostrar_clientes")
            except:
                error_message="ERROR: Borrado incorrecto"
                return render(request,"confirmacion_borrado.html", {'dni': pk, "error_message": error_message})

            return redirect("clientes:alta_cliente")
        elif 'cancelar-btn' in keys_request_POST:
            return redirect("clientes:mostrar_clientes")
    return render(request, 'confirmacion_borrado.html', {'dni': pk})

def confirmar_liberacion_cita(request, pk):
    if request.method == 'POST':
        keys_request_POST = request.POST.keys()
        
        if 'liberar-btn' in keys_request_POST:
            print("aqui")
            try:
                print("Liberando: ", pk)
                cursor = bd.ConnectionBD().get_conexion().cursor()
                horas = [] 
                
                fecha = datetime.strptime(pk, '%Y-%m-%d %H:%M:%S').strftime("%d/%m/%y")
                hora =  datetime.strptime(pk, '%Y-%m-%d %H:%M:%S').strftime("%H:%M")
                print(fecha, hora)
                sql = "UPDATE CITA SET DNI=NULL, DISPONIBILIDAD='Y' WHERE TO_CHAR(fechahora, 'DD/MM/YY' ) LIKE '{0}' AND TO_CHAR(fechahora, 'HH24:MI') LIKE '{1}' ".format(fecha, hora)
                print(sql)
                
                cursor.execute(sql)
                bd.ConnectionBD().get_conexion().commit()
                return redirect("clientes:mostrar_citas")
            except:
                error_message="ERROR: Liberación incorrecto"
                return render(request,"confirmacion_liberacion.html", {'info': pk, "error_message": error_message})

            return redirect("clientes:alta_cliente")
        elif 'cancelar-btn' in keys_request_POST:
            return redirect("clientes:mostrar_citas")
    return render(request, 'confirmacion_liberacion.html', {'info': pk})

    
        
def reservar_cita(request, pk):
    cursor = bd.ConnectionBD().get_conexion().cursor()
    clientes = [] 
    cursor.execute("SELECT dni, nombre, apellidos, telefono FROM cliente")
    
    clientes = [ {'dni':fila[0], 'nombre':fila[1], 'apellido':fila[2], 'telefono':fila[3]} for fila in  cursor.fetchall()]
    return render(request,"reserva_cita.html", {"clientes": clientes, "fecha":pk})
      
def asignar_cliente(request, pk, fecha):
    try:
        print("Asignando: ", fecha, " a: ", pk)
        cursor = bd.ConnectionBD().get_conexion().cursor()
        
        f = datetime.strptime(fecha, '%Y-%m-%d %H:%M:%S').strftime("%d/%m/%y")
        h =  datetime.strptime(fecha, '%Y-%m-%d %H:%M:%S').strftime("%H:%M")
        print(f, h)
        sql = "UPDATE CITA SET DNI='{0}', DISPONIBILIDAD='N' WHERE TO_CHAR(fechahora, 'DD/MM/YY' ) LIKE '{1}' AND TO_CHAR(fechahora, 'HH24:MI') LIKE '{2}' ".format(pk, f, h)
        print(sql)
        
        cursor.execute(sql)
        bd.ConnectionBD().get_conexion().commit()
        return redirect("clientes:mostrar_citas")
    except:
        error_message="ERROR: Asignación incorrecta incorrecto"
        return redirect(reverse("clientes:reservar_cita", kwargs={ 'pk': fecha }))

            


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
        elif 'mostrar-citas-btn' in keys_request_POST:
            return redirect("clientes:mostrar_citas")
        elif 'modificar-cliente-btn' in keys_request_POST:
            return redirect("clientes:modificar_cliente")
    
    return render(request, 'menu_cliente.html')

