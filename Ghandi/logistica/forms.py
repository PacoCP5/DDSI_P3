from django import forms

class HacerPedidoForm(forms.Form):
    idpedido = forms.IntegerField(label="idPedido", widget=forms.TextInput(attrs={'placeholder': "idPedido"}))
    cantidad = forms.FloatField(label="Cantidad", widget=forms.TextInput(attrs={'placeholder': "Cantidad"}))
    fecha = forms.DateField(label="Fecha", widget=forms.TextInput(attrs={'placeholder': "Fecha (DD/MM/YYYY)"}))
    pagado = forms.CharField(label="Pagado", max_length=1, widget=forms.TextInput(attrs={'placeholder': "Pagado (S/N)"}))
    idproducto = forms.CharField(label="idProducto", widget=forms.TextInput(attrs={'placeholder': "idProducto"}))