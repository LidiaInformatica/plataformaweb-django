"""
Vistas para el panel de notificaciones
"""
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from .models import Notificacion
from core.forms import NotificacionManualForm
from core.models import Notificacion
from django.core.mail import send_mail
from django.shortcuts import redirect
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
    
    return render(request, 'core/', context)


@login_required
def enviar_notificacion_manual(request):
    if request.method == 'POST':
        form = NotificacionManualForm(request.POST)
        if form.is_valid():
            apoderado = form.cleaned_data['apoderado']
            asunto = form.cleaned_data['asunto']
            mensaje = form.cleaned_data['mensaje']

            # Envío por correo
            send_mail(
                subject=asunto,
                message=mensaje,
                from_email='notificaciones@colegio.cl',
                recipient_list=[apoderado.email],
                fail_silently=False,
            )

            # Registro en base de datos
            Notificacion.objects.create(
                usuario_registra=request.user,
                apoderado_nombre=apoderado.nombre_completo,  # o apoderado.__str__() si no tienes ese campo
                apoderado_email=apoderado.email,
                titulo=asunto,
                mensaje=mensaje,
                tipo='recordatorio',  # ← puedes parametrizarlo luego
                leida=False
            )

            return redirect('/notificaciones/')
    else:
        form = NotificacionManualForm()

    return render(request, 'core/enviar_notificacion_manual.html', {'form': form})
