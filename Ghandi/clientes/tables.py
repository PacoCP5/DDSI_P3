import django_tables2 as tables



class ClienteTabla(tables.Table):

    dni =   tables.Column()
    nombre = tables.Column()
    apellido = tables.Column()
    telefono = tables.Column()

    class Meta:
        attrs = {'class': 'paleblue','width':'250px'}
    


class ClienteTablaCompleta(tables.Table):
    dni =   tables.Column()
    nombre = tables.Column()
    apellido = tables.Column()
    telefono = tables.Column()
    cuenta = tables.Column()
    direccion = tables.Column()
    delete = tables.LinkColumn('clientes:confirmar_borrado', args=[dni], attrs={
    'a': {'class': 'btn'}
    })
    class Meta:
        attrs = {'class': 'paleblue','width':'550px'}

class Horas(tables.Table):
    fecha = tables.Column()
    hora = tables.Column()
    class Meta:
        attrs = {'class': 'paleblue','width':'250px'}