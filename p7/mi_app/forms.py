from django import forms

from .models import Libro,Autor,Prestamo

class AutorForm(forms.ModelForm):

    class Meta:
        model = Autor
        fields = '__all__'

class LibroForm(forms.ModelForm):

    class Meta:
        model = Libro
        fields = '__all__'

class PrestamoForm(forms.ModelForm):

    class Meta:
        model = Prestamo
        fields = ('libro',)

