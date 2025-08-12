from django import forms
from .models import Actividad, TipoActividad
from estudiantes.models import Curso

class ActividadForm(forms.ModelForm):
    """Formulario para crear y editar actividades"""
    
    class Meta:
        model = Actividad
        fields = ['nombre', 'descripcion', 'tipo', 'fecha_inicio', 'fecha_fin', 
                 'monto_por_estudiante', 'cursos_asignados', 'estado']
        widgets = {
            'nombre': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Ej: Gala de 4° Medio'
            }),
            'descripcion': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'Descripción de la actividad'
            }),
            'tipo': forms.Select(attrs={
                'class': 'form-select'
            }),
            'fecha_inicio': forms.DateInput(attrs={
                'class': 'form-control',
                'type': 'date'
            }),
            'fecha_fin': forms.DateInput(attrs={
                'class': 'form-control',
                'type': 'date'
            }),
            'monto_por_estudiante': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': 'Monto en pesos (sin decimales)'
            }),
            'cursos_asignados': forms.CheckboxSelectMultiple(attrs={
                'class': 'form-check-input'
            }),
            'estado': forms.Select(attrs={
                'class': 'form-select'
            })
        }
        labels = {
            'nombre': 'Nombre de la Actividad',
            'descripcion': 'Descripción',
            'tipo': 'Tipo de Actividad',
            'fecha_inicio': 'Fecha de Inicio',
            'fecha_fin': 'Fecha de Vencimiento (Límite para Pago)',
            'monto_por_estudiante': 'Monto por Estudiante',
            'cursos_asignados': 'Cursos Participantes',
            'estado': 'Estado de la Actividad'
        }

    def clean(self):
        cleaned_data = super().clean()
        fecha_inicio = cleaned_data.get('fecha_inicio')
        fecha_fin = cleaned_data.get('fecha_fin')
        
        if fecha_inicio and fecha_fin:
            if fecha_fin < fecha_inicio:
                raise forms.ValidationError(
                    'La fecha de vencimiento no puede ser anterior a la fecha de inicio.'
                )
        
        return cleaned_data

class TipoActividadForm(forms.ModelForm):
    """Formulario para crear tipos de actividad"""
    
    class Meta:
        model = TipoActividad
        fields = ['nombre', 'descripcion']
        widgets = {
            'nombre': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Ej: Evento, Gira, Material Escolar'
            }),
            'descripcion': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 2,
                'placeholder': 'Descripción opcional del tipo de actividad'
            })
        }
        labels = {
            'nombre': 'Nombre del Tipo',
            'descripcion': 'Descripción'
        }
