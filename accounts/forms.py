from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from core.models import PerfilUsuario
import re

class CustomAuthenticationForm(AuthenticationForm):
    username = forms.CharField(
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'RUT o Usuario (ej: colegio, admin)',
            'autofocus': True
        }),
        label='RUT / Usuario'
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Contraseña'
        }),
        label='Contraseña'
    )
    
    def clean_username(self):
        username = self.cleaned_data.get('username')
        if username:
            # Si parece ser un RUT (contiene puntos o guiones), limpiar formato
            if '.' in username or '-' in username:
                username = re.sub(r'[.-]', '', username)
                # Validar formato de RUT solo si parece ser un RUT
                if not re.match(r'^\d{7,8}[0-9kK]$', username):
                    raise forms.ValidationError('Formato de RUT inválido.')
            # Si no parece ser un RUT, permitir cualquier username válido
            # (para usuarios como "admin", "colegio", etc.)
        return username

class CustomUserCreationForm(UserCreationForm):
    first_name = forms.CharField(
        max_length=30,
        required=True,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Nombres'
        }),
        label='Nombres'
    )
    last_name = forms.CharField(
        max_length=30,
        required=True,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Apellidos'
        }),
        label='Apellidos'
    )
    email = forms.EmailField(
        required=True,
        widget=forms.EmailInput(attrs={
            'class': 'form-control',
            'placeholder': 'correo@ejemplo.com'
        }),
        label='Email'
    )
    username = forms.CharField(
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'RUT sin puntos ni guión'
        }),
        label='RUT',
        help_text='Ingrese su RUT sin puntos ni guión (ej: 12345678k)'
    )
    password1 = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Contraseña'
        }),
        label='Contraseña'
    )
    password2 = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Confirmar contraseña'
        }),
        label='Confirmar Contraseña'
    )

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'password1', 'password2')

    def clean_username(self):
        username = self.cleaned_data.get('username')
        if username:
            # Limpiar RUT
            username = re.sub(r'[.-]', '', username)
            # Validar formato
            if not re.match(r'^\d{7,8}[0-9kK]$', username):
                raise forms.ValidationError('Formato de RUT inválido. Use formato: 12345678k')
            # Verificar si ya existe
            if User.objects.filter(username=username).exists():
                raise forms.ValidationError('Este RUT ya está registrado.')
        return username

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError('Este email ya está registrado.')
        return email

class PerfilUsuarioForm(forms.ModelForm):
    telefono = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': '+56 9 1234 5678'
        }),
        label='Teléfono'
    )
    
    cargo_directiva = forms.ChoiceField(
        choices=[('', 'Seleccione un cargo')] + PerfilUsuario.CARGO_DIRECTIVA_CHOICES,
        required=False,
        widget=forms.Select(attrs={
            'class': 'form-control',
            'id': 'id_cargo_directiva'
        }),
        label='Cargo en la Directiva'
    )
    
    class Meta:
        model = PerfilUsuario
        fields = ['tipo_perfil', 'cargo_directiva', 'telefono']
        widgets = {
            'tipo_perfil': forms.Select(attrs={
                'class': 'form-control',
                'id': 'id_tipo_perfil',
                'onchange': 'toggleCargoDirectiva()'
            }),
        }
        labels = {
            'tipo_perfil': 'Tipo de Perfil',
            'telefono': 'Teléfono'
        }

    def clean_telefono(self):
        telefono = self.cleaned_data.get('telefono')
        if telefono:
            # Validar formato básico de teléfono chileno
            telefono_limpio = re.sub(r'[^\d+]', '', telefono)
            if not re.match(r'^\+?56\d{8,9}$', telefono_limpio):
                raise forms.ValidationError('Formato de teléfono inválido. Use: +56 9 1234 5678')
        return telefono
    
    def clean(self):
        cleaned_data = super().clean()
        tipo_perfil = cleaned_data.get('tipo_perfil')
        cargo_directiva = cleaned_data.get('cargo_directiva')
        
        # Si es directiva, el cargo es obligatorio
        if tipo_perfil == 'directiva' and not cargo_directiva:
            raise forms.ValidationError('Debe seleccionar un cargo para la directiva.')
        
        # Si no es directiva, limpiar el cargo
        if tipo_perfil != 'directiva':
            cleaned_data['cargo_directiva'] = None
        
        return cleaned_data

class CambiarPasswordForm(forms.Form):
    password_actual = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Contraseña actual'
        }),
        label='Contraseña Actual'
    )
    password_nueva = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Nueva contraseña'
        }),
        label='Nueva Contraseña',
        min_length=8
    )
    password_confirmacion = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Confirmar nueva contraseña'
        }),
        label='Confirmar Nueva Contraseña'
    )

    def __init__(self, user, *args, **kwargs):
        self.user = user
        super().__init__(*args, **kwargs)

    def clean_password_actual(self):
        password_actual = self.cleaned_data.get('password_actual')
        if not self.user.check_password(password_actual):
            raise forms.ValidationError('La contraseña actual es incorrecta.')
        return password_actual

    def clean(self):
        cleaned_data = super().clean()
        password_nueva = cleaned_data.get('password_nueva')
        password_confirmacion = cleaned_data.get('password_confirmacion')

        if password_nueva and password_confirmacion:
            if password_nueva != password_confirmacion:
                raise forms.ValidationError('Las contraseñas no coinciden.')

        return cleaned_data
