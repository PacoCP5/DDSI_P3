from django import forms

class HacerPedidoForm(forms.Form):
    idpedido = forms.IntegerField(label="idPedido", widget=forms.TextInput(attrs={'placeholder': "idPedido"}))
    cantidad = forms.FloatField(label="Cantidad", widget=forms.TextInput(attrs={'placeholder': "Cantidad"}))
    fecha = forms.DateField(label="Fecha", widget=forms.TextInput(attrs={'placeholder': "Fecha (DD/MM/YYYY)"}))
    pagado = forms.CharField(label="Pagado", max_length=1, widget=forms.TextInput(attrs={'placeholder': "Pagado (S/N)"}))
    idproducto = forms.CharField(label="idProducto", widget=forms.TextInput(attrs={'placeholder': "idProducto"}))

class StockForm(forms.Form):
    idproducto = forms.IntegerField(label="idProducto", required=False, widget=forms.TextInput(attrs={'placeholder': "idProducto"}))
    nombreproducto = forms.CharField(label="Nombre Producto", required=False, widget=forms.TextInput(attrs={'placeholder': "Nombre"}))

class DisponibilidadForm(forms.Form):
    idjaula = forms.IntegerField(label="idJaula", required=False, widget=forms.TextInput(attrs={'placeholder': "idJaula"}))
    
class AsignarForm(forms.Form):
    idjaula = forms.IntegerField(label="idJaula", widget=forms.TextInput(attrs={'placeholder': "idJaula"}))
    idanimal = forms.IntegerField(label="idAnimal", widget=forms.TextInput(attrs={'placeholder': "idAnimal"}))

class AlmacenarForm(forms.Form):
    idproducto = forms.IntegerField(label="idProducto", widget=forms.TextInput(attrs={'placeholder': "idProducto"}))
    cantidad = forms.CharField(label="Cantidad", widget=forms.TextInput(attrs={'placeholder': "Cantidad"}))

class AltaProductoForm(forms.Form):
    idproducto = forms.IntegerField(label="idProducto", required=False, widget=forms.TextInput(attrs={'placeholder': "idProducto (Opcional)"}))
    nombreproducto = forms.CharField(label="Nombre Producto", widget=forms.TextInput(attrs={'placeholder': "Nombre"}))
