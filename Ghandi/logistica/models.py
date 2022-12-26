from django.db import models

class Animal(models.Model):
    idanimal = models.IntegerField(max_length=9, primary_key=True)

    def __str__(self):
        return self.idanimal
        
class Jaula(models.Model):
    idjaula = models.IntegerField(max_length=9, primary_key=True)
    idanimal = models.ForeignKey(Animal, on_delete=models.DO_NOTHING, default=None)
    tamanio = models.CharField(max_length=9)

    def __str__(self):
        return self.idjaula

class Producto(models.Model):
    idproducto = models.IntegerField(max_length=9, primary_key=True)
    nombre = models.CharField(max_length=50)
    cantidad = models.FloatField(max_length=10)

    def __str__(self):
        return self.idproducto

class Pedido(models.Model):
    idpedido = models.IntegerField(max_length=9, primary_key=True)
    cantidad = models.FloatField(max_length=9)
    fecha = models.DateField()
    pagado = models.CharField(max_length=1)
    idproducto = models.ForeignKey(Producto, on_delete=models.DO_NOTHING, default=None)

    def __str__(self):
        return self.idpedido