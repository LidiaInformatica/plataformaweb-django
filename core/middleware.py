from django.shortcuts import redirect
from django.urls import reverse, NoReverseMatch
from django.contrib import messages
from .models import PerfilUsuario

class PerfilMiddleware:
    """
    Middleware para manejar perfiles de usuario y redirecciones según el tipo de perfil
    """
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # URLs que no requieren autenticación
        public_urls = [
            '/admin/',
            '/static/',
            '/media/',
        ]
        
        # Intentar obtener URLs dinámicas de forma segura
        try:
            public_urls.extend([
                reverse('accounts:login'),
                reverse('accounts:register'),
            ])
        except NoReverseMatch:
            # Si las URLs no existen, las ignoramos
            pass
        
        # Verificar si la URL actual es pública
        is_public_url = any(request.path.startswith(url) for url in public_urls)
        
        if request.user.is_authenticated and not is_public_url:
            try:
                # Verificar si el usuario tiene perfil
                perfil = PerfilUsuario.objects.get(usuario=request.user)
                request.perfil = perfil
                
                # Verificar permisos según el tipo de perfil
                if not self._tiene_permiso(request, perfil):
                    try:
                        return redirect('core:dashboard')
                    except NoReverseMatch:
                        # Si la URL del dashboard no existe, permitir continuar
                        pass
                    
            except PerfilUsuario.DoesNotExist:
                # Si no tiene perfil, redirigir a crear perfil
                try:
                    crear_perfil_url = reverse('accounts:crear_perfil')
                    if request.path != crear_perfil_url:
                        return redirect('accounts:crear_perfil')
                except NoReverseMatch:
                    # Si la URL no existe, permitir continuar
                    pass
        
        elif not request.user.is_authenticated and not is_public_url:
            # Si no está autenticado y trata de acceder a URL privada
            try:
                return redirect('accounts:login')
            except NoReverseMatch:
                # Si la URL de login no existe, redirigir al admin
                return redirect('/admin/login/')

        response = self.get_response(request)
        return response
    
    def _tiene_permiso(self, request, perfil):
        """
        Verificar permisos según el tipo de perfil
        """
        # URLs solo para directiva
        directiva_urls = [
            '/estudiantes/',
            '/actividades/',
        ]
        
        # URLs solo para apoderados
        apoderado_urls = [
            '/cuotas/estado-apoderado/',
        ]
        
        # Si es directiva, puede acceder a todo
        if perfil.tipo_perfil == 'directiva':
            return True
        
        # Si es apoderado, verificar restricciones
        if perfil.tipo_perfil == 'apoderado':
            # Los apoderados no pueden acceder a ciertas URLs
            for url in directiva_urls:
                if request.path.startswith(url) and 'lista' in request.path:
                    return False
            return True
        
        return True
