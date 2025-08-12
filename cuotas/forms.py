from django import forms
from .models import PagoCuota
import re

class PagoCuotaForm(forms.ModelForm):
    class Meta:
        model = PagoCuota
        fields = ['monto', 'metodo_pago', 'observacion', 'comprobante']
        widgets = {
            'monto': forms.NumberInput(attrs={
                'class': 'form-control',
                'id': 'id_monto',
                'placeholder': 'Ingrese el monto',
                'min': '1',
                'required': True
            }),
            'metodo_pago': forms.Select(attrs={
                'class': 'form-select',
                'required': True
            }),
            'observacion': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 2,
                'placeholder': 'Observaciones adicionales (opcional)'
            }),
            'comprobante': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Número de comprobante (opcional)'
            }),
        }
        labels = {
            'monto': 'Monto a Pagar *',
            'metodo_pago': 'Método de Pago *',
            'observacion': 'Observaciones',
            'comprobante': 'N° Comprobante',
        }

    def clean_monto(self):
        monto = self.cleaned_data.get('monto')
        if not monto:
            raise forms.ValidationError('El monto es obligatorio.')
        if monto <= 0:
            raise forms.ValidationError('El monto debe ser mayor a cero.')
        if monto > 1000000:
            raise forms.ValidationError('El monto no puede ser mayor a $1.000.000.')
        return monto

    def clean_comprobante(self):
        comprobante = self.cleaned_data.get('comprobante')
        if comprobante and len(comprobante) < 3:
            raise forms.ValidationError('El número de comprobante debe tener al menos 3 caracteres.')
        return comprobante

    def clean(self):
        cleaned_data = super().clean()
        metodo_pago = cleaned_data.get('metodo_pago')
        comprobante = cleaned_data.get('comprobante')

        if metodo_pago in ['transferencia', 'cheque'] and not comprobante:
            raise forms.ValidationError('El comprobante es obligatorio para transferencias y cheques.')

        return cleaned_data

class FiltroAvanzadoForm(forms.Form):
    estudiante = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Nombre del estudiante'
        }),
        label='Estudiante'
    )

    rut = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': '12.345.678-9'
        }),
        label='RUT'
    )

    actividad = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Nombre de la actividad'
        }),
        label='Actividad'
    )

    estado = forms.ChoiceField(
        required=False,
        choices=[
            ('', 'Todos los estados'),
            ('pagado', 'Pagado'),
            ('pendiente', 'Pendiente'),
            ('parcial', 'Parcial'),
            ('vencido', 'Vencido'),
        ],
        widget=forms.Select(attrs={
            'class': 'form-control'
        }),
        label='Estado'
    )

    def clean_rut(self):
        rut = self.cleaned_data.get('rut')
        if rut:
            rut_pattern = r'^\d{1,2}\.\d{3}\.\d{3}-[\dkK]$'
            if not re.match(rut_pattern, rut):
                raise forms.ValidationError('Formato de RUT inválido. Use: 12.345.678-9')
        return rut

