from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.urls import reverse
from .forms import CustomUserCreationForm, CustomAuthenticationForm, PerfilUsuarioForm, CambiarPasswordForm
from core.models import PerfilUsuario

def login_view(request):
    """Vista de inicio de sesión"""
    if request.user.is_authenticated:
        user = request.user
        # Redirección según grupo si ya está logueado
        if user.groups.filter(name='Apoderado').exists():
            return redirect('core:vista_apoderado')
        elif user.groups.filter(name__in=['Presidenta', 'Tesorera', 'Secretaria']).exists():
            return redirect('core:dashboard_directiva')
        elif user.is_superuser:
            return redirect('core:dashboard')
        else:
            return redirect('accounts:perfil')

    if request.method == 'POST':
        form = CustomAuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)

            if user is not None:
                login(request, user)
                messages.success(request, f'¡Bienvenido, {user.get_full_name()}!')

                # Verificar si tiene perfil
                try:
                    perfil = PerfilUsuario.objects.get(usuario=user)

                    # Redirección según grupo
                    if user.groups.filter(name='Apoderado').exists():
                        return redirect('core:vista_apoderado')
                    elif user.groups.filter(name__in=['Presidenta', 'Tesorera', 'Secretaria']).exists():
                        return redirect('core:dashboard_directiva')
                    elif user.is_superuser:
                        return redirect('core:dashboard')
                    else:
                        messages.warning(request, 'Su cuenta no tiene un grupo válido asignado. Contacte al administrador.')
                        return redirect('accounts:perfil')

                except PerfilUsuario.DoesNotExist:
                    messages.warning(request, 'Debe completar su perfil para continuar.')
                    return redirect('accounts:crear_perfil')
            else:
                messages.error(request, 'RUT o contraseña incorrectos.')
    else:
        form = CustomAuthenticationForm()

    return render(request, 'accounts/login.html', {'form': form})

def register_view(request):
    """Vista de registro de usuario"""
    if request.user.is_authenticated:
        return redirect('core:dashboard')
    
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            messages.success(request, 'Cuenta creada exitosamente. Ahora complete su perfil.')
            login(request, user)
            return redirect('accounts:crear_perfil')
        else:
            messages.error(request, 'Por favor corrija los errores en el formulario.')
    else:
        form = CustomUserCreationForm()
    
    return render(request, 'accounts/register.html', {'form': form})

@login_required
def crear_perfil_view(request):
    """Vista para crear perfil de usuario"""
    # Verificar si ya tiene perfil
    try:
        perfil = PerfilUsuario.objects.get(usuario=request.user)
        messages.info(request, 'Ya tiene un perfil creado.')
        return redirect('core:dashboard')
    except PerfilUsuario.DoesNotExist:
        pass
    
    if request.method == 'POST':
        form = PerfilUsuarioForm(request.POST)
        if form.is_valid():
            perfil = form.save(commit=False)
            perfil.usuario = request.user
            perfil.rut = request.user.username  # El username es el RUT
            perfil.save()
            
            messages.success(request, 'Perfil creado exitosamente. ¡Bienvenido al sistema!')
            return redirect('core:dashboard')
        else:
            messages.error(request, 'Por favor corrija los errores en el formulario.')
    else:
        form = PerfilUsuarioForm()
    
    return render(request, 'accounts/crear_perfil.html', {'form': form})

@login_required
def perfil_view(request):
    """Vista del perfil de usuario"""
    try:
        perfil = PerfilUsuario.objects.get(usuario=request.user)
    except PerfilUsuario.DoesNotExist:
        messages.warning(request, 'Debe completar su perfil para continuar.')
        return redirect('accounts:crear_perfil')
    
    if request.method == 'POST':
        form = PerfilUsuarioForm(request.POST, instance=perfil)
        if form.is_valid():
            form.save()
            messages.success(request, 'Perfil actualizado exitosamente.')
            return redirect('accounts:perfil')
        else:
            messages.error(request, 'Por favor corrija los errores en el formulario.')
    else:
        form = PerfilUsuarioForm(instance=perfil)
    
    context = {
        'perfil': perfil,
        'form': form
    }
    
    return render(request, 'accounts/perfil.html', context)

@login_required
def cambiar_password_view(request):
    """Vista para cambiar contraseña"""
    if request.method == 'POST':
        form = CambiarPasswordForm(request.user, request.POST)
        if form.is_valid():
            password_nueva = form.cleaned_data['password_nueva']
            request.user.set_password(password_nueva)
            request.user.save()
            
            messages.success(request, 'Contraseña cambiada exitosamente. Inicie sesión nuevamente.')
            logout(request)
            return redirect('accounts:login')
        else:
            messages.error(request, 'Por favor corrija los errores en el formulario.')
    else:
        form = CambiarPasswordForm(request.user)
    
    return render(request, 'accounts/cambiar_password.html', {'form': form})

def logout_view(request):
    """Vista de cierre de sesión"""
    if request.user.is_authenticated:
        nombre = request.user.get_full_name()
        logout(request)
        messages.success(request, f'Sesión cerrada exitosamente. ¡Hasta pronto, {nombre}!')
    
    return redirect('accounts:login')
