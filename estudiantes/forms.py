from django import forms
from django.contrib.auth.models import Group
from .models import Estudiante, Apoderado, Curso

class EstudianteForm(forms.ModelForm):
    class Meta:
        model = Estudiante
        fields = [
            'rut', 'nombre', 'apellido_paterno', 'apellido_materno',
            'fecha_nacimiento', 'curso', 'apoderado', 'vinculo_apoderado'
        ]
        widgets = {
            'rut': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Ej: 12.345.678-9'
            }),
            'nombre': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Nombre del estudiante'
            }),
            'apellido_paterno': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Apellido paterno'
            }),
            'apellido_materno': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Apellido materno'
            }),
            'fecha_nacimiento': forms.DateInput(attrs={
                'class': 'form-control',
                'type': 'date'
            }),
            'curso': forms.Select(attrs={
                'class': 'form-select'
            }),
            'apoderado': forms.Select(attrs={
                'class': 'form-select'
            }),
            'vinculo_apoderado': forms.Select(attrs={
                'class': 'form-select'
            }),
        }

    def clean_apoderado(self):
        apoderado = self.cleaned_data['apoderado']
        if not hasattr(apoderado, 'usuario'):
            raise forms.ValidationError("El apoderado no tiene un usuario vinculado.")
        if not apoderado.usuario.groups.filter(name='Apoderados').exists():
            raise forms.ValidationError("El usuario vinculado al apoderado no pertenece al grupo 'Apoderados'.")
        return apoderado

class ApoderadoForm(forms.ModelForm):
    class Meta:
        model = Apoderado
        fields = [
            'rut', 'nombre', 'apellido_paterno', 'apellido_materno',
            'telefono', 'email', 'direccion'
        ]
        widgets = {
            'rut': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Ej: 12.345.678-9'
            }),
            'nombre': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Nombre del apoderado'
            }),
            'apellido_paterno': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Apellido paterno'
            }),
            'apellido_materno': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Apellido materno'
            }),
            'telefono': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': '+56 9 1234 5678'
            }),
            'email': forms.EmailInput(attrs={
                'class': 'form-control',
                'placeholder': 'apoderado@email.com'
            }),
            'direccion': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'Dirección completa'
            }),
        }
