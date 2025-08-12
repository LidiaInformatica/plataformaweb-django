"""
Vistas para el panel de notificaciones
"""
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from .models import Notificacion
import logging

logger = logging.getLogger('core.notificaciones')

@login_required
def panel_notificaciones(request):
    """Vista para mostrar el panel de notificaciones"""
    notificaciones = Notificacion.objects.all().order_by('-fecha_creacion')[:20]
    
    context = {
        'notificaciones': notificaciones,
        'total_pendientes': notificaciones.filter(estado='pendiente').count(),
        'total_enviadas': notificaciones.filter(estado='enviada').count(),
        'total_fallidas': notificaciones.filter(estado='fallida').count(),
    }
    
    return render(request, 'core/notificaciones.html', context)
