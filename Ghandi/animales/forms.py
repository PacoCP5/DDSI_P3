from django import forms

class AltaAnimalForm(forms.Form):
    idAnimal = forms.CharField(label="ID del Animal",widget=forms.TextInput(attrs={'placeholder': "Introduce el ID del animal"}))
    dni_duenio = forms.CharField(label="DNI del dueño",widget=forms.TextInput(attrs={'placeholder': "Introduce el DNI del dueño del animal"}))
    tipo = forms.CharField(label="Tipo",widget=forms.TextInput(attrs={'placeholder': "Introduce el tipo del animal"}))
    especie = forms.CharField(label="Especie",widget=forms.TextInput(attrs={'placeholder': "Introduce la especie del animal"}))
    
class IDAnimalForm(forms.Form):
    idAnimal = forms.CharField(label="ID del animal",widget=forms.TextInput(attrs={'placeholder': "Introduce el ID del animal"}))

class BuscarAnimalForm(forms.Form):
    idAnimal = forms.CharField(label="ID del animal",widget=forms.TextInput(attrs={'placeholder': "Introduce el ID del animal"}), required=False)
    dni = forms.CharField(label="DNI del dueño",widget=forms.TextInput(attrs={'placeholder': "Introduce el DNI del dueño del animal"}), required=False)
    tipo = forms.CharField(label="Tipo",widget=forms.TextInput(attrs={'placeholder': "Introduce el tipo del animal"}), required = False)
    especie = forms.CharField(label="Especie",widget=forms.TextInput(attrs={'placeholder': "Introduce la especie del animal"}), required = False)
    
class ModificarAnimalForm(forms.Form):
    idAnimal_antiguo = forms.CharField(label="ID del animal a modificar",widget=forms.TextInput(attrs={'placeholder': "Introduce el ID del animal"}))
    idAnimal_nuevo = forms.CharField(label="ID nuevo del animal",widget=forms.TextInput(attrs={'placeholder': "Introduce el ID del animal"}), required=False)
    dni_duenio = forms.CharField(label="DNI del dueño",widget=forms.TextInput(attrs={'placeholder': "Introduce el DNI del dueño del animal"}), required=False)
    tipo = forms.CharField(label="tipo",widget=forms.TextInput(attrs={'placeholder': "Introduce el tipo del animal"}), required = False)
    especie = forms.CharField(label="especie",widget=forms.TextInput(attrs={'placeholder': "Introduce la especie del animal"}), required = False)
    