from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.paginator import Paginator
from django.http import JsonResponse
from .models import Notificacion
from .notificaciones import ServicioNotificaciones
from django.db.models import Q
import logging

logger = logging.getLogger(__name__)

@login_required
def lista_notificaciones(request):
    """Vista para listar todas las notificaciones del usuario"""
    try:
        notificaciones = Notificacion.objects.filter(
            Q(apoderado_email=request.user.email) |
            Q(usuario_registra=request.user)
        ).order_by('-fecha_creacion')

        paginator = Paginator(notificaciones, 10)
        page = request.GET.get('page')
        notificaciones_page = paginator.get_page(page)

        notificaciones_no_leidas = notificaciones.filter(leida=False)
        if notificaciones_no_leidas.exists():
            logger.info(f"Marcadas {notificaciones_no_leidas.count()} notificaciones como leídas para {request.user.email}")

        context = {
            'notificaciones': notificaciones_page,
            'total_notificaciones': notificaciones.count(),
        }

        return render(request, 'core/notificaciones/lista.html', context)

    except Exception as e:
        logger.error(f"Error al listar notificaciones para {request.user.email}: {str(e)}")
        messages.error(request, 'Error al cargar las notificaciones.')
        return redirect('core:dashboard')

@login_required
def detalle_notificacion(request, notificacion_id):
    """Vista para ver el detalle de una notificación específica"""
    try:
        notificacion = get_object_or_404(
            Notificacion,
            Q(id=notificacion_id) & (
                Q(apoderado_email=request.user.email) |
                Q(usuario_registra=request.user)
            )
        )

        if notificacion.leida is False:
            notificacion.leida = True
            notificacion.save()
            logger.info(f"Notificación {notificacion_id} marcada como leída por {request.user.email}")

        context = {
            'notificacion': notificacion,
        }

        return render(request, 'core/notificaciones/detalle.html', context)

    except Exception as e:
        logger.error(f"Error al mostrar detalle de notificación {notificacion_id}: {str(e)}")
        messages.error(request, 'Error al cargar la notificación.')
        return redirect('notificaciones:lista')

@login_required
def marcar_leida(request, notificacion_id):
    """Vista AJAX para marcar una notificación como leída"""
    if request.method == 'POST':
        try:
            notificacion = get_object_or_404(
                Notificacion,
                Q(id=notificacion_id) & (
                    Q(apoderado_email=request.user.email) |
                    Q(usuario_registra=request.user)
                )
            )

            notificacion.estado = 'leido'
            notificacion.save()

            logger.info(f"Notificación {notificacion_id} marcada como leída por {request.user.email}")

            return JsonResponse({
                'success': True,
                'message': 'Notificación marcada como leída'
            })

        except Exception as e:
            logger.error(f"Error al marcar notificación {notificacion_id} como leída: {str(e)}")
            return JsonResponse({
                'success': False,
                'message': 'Error al marcar la notificación como leída'
            })

    return JsonResponse({'success': False, 'message': 'Método no permitido'})

@login_required
def test_notificacion(request):
    """Vista para probar el sistema de notificaciones (solo para desarrollo)"""
    try:
        if request.method == 'POST':
            servicio = ServicioNotificaciones()

            notificacion = servicio.crear_notificacion(
                tipo='prueba',
                titulo='Notificación de Prueba',
                mensaje='Esta es una notificación de prueba del sistema.',
                apoderado_email=request.user.email,
                datos_adicionales={
                    'usuario': request.user.username,
                    'fecha_test': 'Ahora'
                }
            )

            if notificacion:
                messages.success(request, 'Notificación de prueba enviada correctamente.')
                logger.info(f"Notificación de prueba enviada a {request.user.email}")
            else:
                messages.error(request, 'Error al enviar notificación de prueba.')

            return redirect('notificaciones:lista')

        return render(request, 'core/notificaciones/test.html')

    except Exception as e:
        logger.error(f"Error en test de notificaciones: {str(e)}")
        messages.error(request, 'Error al realizar la prueba de notificaciones.')
        return redirect('notificaciones:lista')

@login_required
def lista_automaticas(request):
    """Vista para listar todas las notificaciones automáticas del sistema"""
    try:
        notificaciones = Notificacion.objects.filter(
            tipo__in=['recordatorio', 'nueva_cuota', 'sistema']
        ).order_by('-fecha_envio')

        paginator = Paginator(notificaciones, 15)
        page = request.GET.get('page')
        notificaciones_page = paginator.get_page(page)

        context = {
            'notificaciones': notificaciones_page,
            'total': notificaciones.count(),
        }

        return render(request, 'core/notificaciones/lista_automaticas.html', context)

    except Exception as e:
        logger.error(f"Error al listar notificaciones automáticas: {str(e)}")
        messages.error(request, 'Error al cargar las notificaciones automáticas.')
        return redirect('core:dashboard')

