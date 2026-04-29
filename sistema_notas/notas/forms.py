from django import forms
from .models import DetalleNota

class NotaForm(forms.ModelForm):
    class Meta:
        model = DetalleNota
        fields = ['tipo', 'valor']