# core/context_processors.py
from .models import Notificacion

def notificaciones_context(request):
    """
    Context processor para incluir el conteo de notificaciones no leídas
    en todas las plantillas
    """
    if request.user.is_authenticated:
        notificaciones_no_leidas = Notificacion.objects.filter(
            apoderado_email=request.user.email,
            estado__in=['enviado', 'visto']
        ).count()
        
        return {
            'notificaciones_no_leidas': notificaciones_no_leidas
        }
    
    return {
        'notificaciones_no_leidas': 0
    }
