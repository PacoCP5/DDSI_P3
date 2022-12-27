from django import forms

class IngresoSalariosForm(forms.Form):
    dni = forms.CharField(label="DNI",widget=forms.TextInput(attrs={'placeholder': "Introduce DNI del trabajador"}))
    