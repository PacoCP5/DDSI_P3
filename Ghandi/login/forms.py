from django import forms

class LoginBDForm(forms.Form):
   username = forms.CharField(
                  label="Nombre de Usuario",
                  widget=forms.TextInput(attrs={'placeholder': "Introduce nombre de usuario"}))
   password = forms.CharField(
                  label="Contraseña",
                  widget=forms.TextInput(attrs={'placeholder': "Introduce contraseña"}))

