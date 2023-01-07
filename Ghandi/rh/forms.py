from django import forms

class ContratoForm(forms.Form):
    dni = forms.CharField(label="DNI",widget=forms.TextInput(attrs={'placeholder': "Introduce DNI del empleado"}))
    nombre = forms.CharField(label="Nombre",widget=forms.TextInput(attrs={'placeholder': "Nombre del empleado"}))
    apellidos = forms.CharField(label="Apellidos",widget=forms.TextInput(attrs={'placeholder': "Apellidos"}))
    fecha_nacimiento = forms.DateField(label="FechaNacimiento", widget=forms.TextInput(attrs={'placeholder': "Fecha de nacimiento (DD/MM/YYYY)"}))
    telefono = forms.CharField(label="Telefono", widget=forms.TextInput(attrs={'placeholder': "Telefono"}))
    cuenta_bancaria = forms.CharField(label="CuentaBancaria",widget=forms.TextInput(attrs={'placeholder': "CuentaBancaria"}))
    sueldo = forms.FloatField(label="Sueldo", widget=forms.TextInput(attrs={'placeholder': "Sueldo"}))
    duracion_contrato = forms.CharField(label="Duracion",widget=forms.TextInput(attrs={'placeholder': "Durancion del contrato"}))

class DNIForm(forms.Form):
    dni = forms.CharField(label="DNI",widget=forms.TextInput(attrs={'placeholder': "Introduce DNI del empleado"}))

class EntrevistaForm(forms.Form):
    dni = forms.CharField(label="DNI",widget=forms.TextInput(attrs={'placeholder': "Introduce DNI del empleado"}))
    nombre = forms.CharField(label="Nombre",widget=forms.TextInput(attrs={'placeholder': "Nombre"}))
    apellidos = forms.CharField(label="Apellidos",widget=forms.TextInput(attrs={'placeholder': "Apellidos"}))
    fecha = forms.DateField(label="Fecha", widget=forms.TextInput(attrs={'placeholder': "Fecha de la entrevista (DD/MM/YYYY)"}))
    hora = forms.CharField(label="Hora",widget=forms.TextInput(attrs={'placeholder': "Hora (HH:MM)"}))

class ModificaForm(forms.Form):
    dni = forms.CharField(label="DNI",widget=forms.TextInput(attrs={'placeholder': "Introduce DNI del empleado a modificar"}))
    nombre = forms.CharField(label="Nombre",widget=forms.TextInput(attrs={'placeholder': "Nombre nuevo"}))
    apellidos = forms.CharField(label="Apellidos",widget=forms.TextInput(attrs={'placeholder': "Apellidos nuevos"}))
    fecha_nacimiento = forms.DateField(label="FechaNacimiento", widget=forms.TextInput(attrs={'placeholder': "Fecha de nacimiento (DD/MM/YYYY)"}))
    telefono = forms.CharField(label="Telefono", widget=forms.TextInput(attrs={'placeholder': "Telefono"}))
    cuenta_bancaria = forms.CharField(label="CuentaBancaria",widget=forms.TextInput(attrs={'placeholder': "CuentaBancaria"}))
    sueldo = forms.FloatField(label="Sueldo", widget=forms.TextInput(attrs={'placeholder': "Sueldo"}))
    duracion_contrato = forms.CharField(label="Duracion",widget=forms.TextInput(attrs={'placeholder': "Durancion del contrato"}))