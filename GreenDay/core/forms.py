from django import forms
from .models import Cliente

class PerfilForm(forms.ModelForm):
    class Meta:
        model = Cliente
        fields = ['nombre', 'apellido', 'telefono', 'direccion']  # ajusta según tus campos
