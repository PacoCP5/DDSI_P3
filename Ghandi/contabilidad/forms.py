from django import forms

class IngresoSalariosForm(forms.Form):
    dni = forms.CharField(label="DNI",widget=forms.TextInput(attrs={'placeholder': "Introduce DNI del trabajador"}))
    
class FacturaForm(forms.Form):
    idfactura = forms.CharField(label="idFactura",widget=forms.TextInput(attrs={'placeholder': "Introduce ID de la factura"}))
    dni = forms.CharField(label="DNI",widget=forms.TextInput(attrs={'placeholder': "Introduce DNI del cliente"}))
    cantidad = forms.CharField(label="Cantidad",widget=forms.TextInput(attrs={'placeholder': "Introduce cantidad"}))

class PagoFacturaForm(forms.Form):
    idfactura = forms.CharField(label="idFactura",widget=forms.TextInput(attrs={'placeholder': "Introduce ID de la factura"}))

class PagoPedidoForm(forms.Form):
    idpedido = forms.CharField(label="idPedido",widget=forms.TextInput(attrs={'placeholder': "Introduce ID del pedido"}))
