### RF-02 Ciclo 2: Segmentación por Apoderado

**Estado**: Fallido
**Razón**: Se identificaron múltiples mejoras necesarias:

1. Autenticación incorrecta del apoderado
2. Falta de restricción en vistas por rol
3. Ausencia de segmentación de información

**Plan de Mejoras (Ciclo 3)**:

1. Implementar middleware de autenticación específico para apoderados
2. Crear decoradores de permisos por rol
3. Segmentar información por apoderado
4. Implementar notificaciones en tiempo real


class ApoderadoAuthMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if request.user.is_authenticated:
            try:
                request.apoderado = Apoderado.objects.get(usuario=request.user)
            except Apoderado.DoesNotExist:
                request.apoderado = None
        return self.get_response(request)


from functools import wraps
from django.shortcuts import redirect
from django.contrib import messages

def apoderado_required(view_func):
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        if not hasattr(request, 'apoderado') or request.apoderado is None:
            messages.error(request, 'Acceso permitido solo para apoderados.')
            return redirect('core:dashboard')
        return view_func(request, *args, **kwargs)
    return wrapper


from core.decorators import apoderado_required

@apoderado_required
def estado_pago_apoderado(request):
    """Vista segmentada para apoderados"""
    estudiantes = Estudiante.objects.filter(apoderado=request.apoderado)
    cuotas = CuotaEstudiante.objects.filter(estudiante__in=estudiantes)
    
    context = {
        'estudiantes': estudiantes,
        'cuotas': cuotas,
        'total_pendiente': cuotas.filter(estado='pendiente').aggregate(Sum('monto_total'))['monto_total__sum'] or 0,
    }
    return render(request, 'cuotas/estado_apoderado.html', context)

3. Plan de Implementación (Ciclo 3)
Implementar autenticación robusta
Agregar middleware de apoderados
Crear decoradores de permisos
Modificar vistas para usar segmentación
Implementar notificaciones en tiempo real
Actualizar templates para mostrar solo información relevante