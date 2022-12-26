from django import forms
from bootstrap_datepicker_plus.widgets import DatePickerInput


class NuevoClienteForm(forms.Form):
   nombre = forms.CharField(
                  label="Nombre",
                  widget=forms.TextInput(attrs={'placeholder': "Introduce nombre del cliente"}))
   apellidos = forms.CharField(
                  label="Apellidos",
                  widget=forms.TextInput(attrs={'placeholder': "Introduce apellidos del cliente"}))
   telefono = forms.CharField(label="Telefono",widget=forms.TextInput(attrs={'placeholder': "Introduce telefono del cliente"}), required=False)
   direccion = forms.CharField(label="Direccion",widget=forms.TextInput(attrs={'placeholder': "Introduce direccion del cliente"}), required=False)
   dni = forms.CharField(label="DNI",widget=forms.TextInput(attrs={'placeholder': "Introduce DNI del cliente"}))
   cuenta_banco = forms.CharField(label="Cuenta Banco",widget=forms.TextInput(attrs={'placeholder': "Introduce cuenta del banco del cliente"}), required=False)

class BuscarClienteForm(  forms.Form):
   nombre = forms.CharField(
                  label="Nombre",
                  widget=forms.TextInput(attrs={'placeholder': "Introduce nombre del cliente"}), required=False)
   apellidos = forms.CharField(
                  label="Apellidos",
                  widget=forms.TextInput(attrs={'placeholder': "Introduce apellidos del cliente"}), required=False)
   dni = forms.CharField(label="DNI",widget=forms.TextInput(attrs={'placeholder': "Introduce DNI del cliente"}))


class BuscarFechaForm(forms.Form):
   date = forms.DateField(widget = DatePickerInput())

            
   