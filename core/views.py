from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from datetime import datetime, timedelta
from django.db.models import Sum
# Traducción manual de meses al español
MESES_ES = {
    'January': 'Enero',
    'February': 'Febrero',
    'March': 'Marzo',
    'April': 'Abril',
    'May': 'Mayo',
    'June': 'Junio',
    'July': 'Julio',
    'August': 'Agosto',
    'September': 'Septiembre',
    'October': 'Octubre',
    'November': 'Noviembre',
    'December': 'Diciembre',
}

@login_required
def dashboard(request):
    # Obtener datos reales de la base de datos
    from cuotas.models import CuotaEstudiante, PagoCuota
    from estudiantes.models import Estudiante
    from actividades.models import Actividad
    
    hoy = timezone.now().date()
    
    # Calcular estadísticas reales
    total_cuotas = CuotaEstudiante.objects.all()
    recaudacion_total = total_cuotas.aggregate(total=Sum('monto_pagado'))['total'] or 0
    cuotas_pendientes = total_cuotas.filter(estado='pendiente').count()
    actividades_activas = Actividad.objects.count()
    total_estudiantes = Estudiante.objects.count()
    
    # Obtener últimos pagos reales
    pagos_recientes = PagoCuota.objects.select_related(
        'cuota__estudiante', 'cuota__actividad'
    ).order_by('-fecha_pago')[:5]
    
    ultimos_pagos = []
    for pago in pagos_recientes:
        ultimos_pagos.append({
            'estudiante': f"{pago.cuota.estudiante.nombre} {pago.cuota.estudiante.apellido_paterno} {pago.cuota.estudiante.apellido_materno}",
            'actividad': pago.cuota.actividad.nombre,
            'monto': pago.monto,
            'fecha': pago.fecha_pago.date(),
            'estado': pago.cuota.estado  # ✅ Usar el estado real de la cuota
        })
    
    # RF-08: Visualizar mensajes y alertas en bandeja por perfil
    mensajes_alertas = [
        {
            'tipo': 'info',
            'titulo': 'Sistema Actualizado',
            'mensaje': f'Se han registrado {pagos_recientes.count()} pagos recientes.',
            'fecha': hoy,
            'icono': 'fas fa-info-circle',
            'color': 'info'
        },
        {
            'tipo': 'alerta',
            'titulo': 'Cuotas Pendientes',
            'mensaje': f'Hay {cuotas_pendientes} cuotas pendientes de pago.',
            'fecha': hoy,
            'icono': 'fas fa-exclamation-triangle',
            'color': 'warning'
        }
    ]
    
    # RF-06: Notificaciones automáticas REALES
    from core.models import Notificacion
    notificaciones_recientes = Notificacion.objects.filter(
        estado='enviada'
    ).order_by('-fecha_creacion')[:10]
    
    # Contar notificaciones no leídas para el usuario actual
    total_no_leidas = Notificacion.objects.filter(
    apoderado_email=request.user.email,
    leida=False
    ).count()
    
    notificaciones_automaticas = []
    for notif in notificaciones_recientes:
        notificaciones_automaticas.append({
            'titulo': notif.titulo,
            'mensaje': notif.mensaje[:100] + '...' if len(notif.mensaje) > 100 else notif.mensaje,
            'estudiante': notif.estudiante_nombre,
            'apoderado': notif.apoderado_nombre,
            'email': notif.apoderado_email,
            'telefono': notif.apoderado_telefono,
            'fecha_envio': notif.fecha_creacion.date(),
            'tipo': notif.get_tipo_display(),
            'estado': notif.estado
        })

    hoy = timezone.now().date()
    mes_en = hoy.strftime('%B')
    mes_es = MESES_ES.get(mes_en, mes_en)
    context = {
        'recaudacion_total': recaudacion_total,
        'cuotas_pendientes': cuotas_pendientes,
        'actividades_activas': actividades_activas,
        'total_estudiantes': total_estudiantes,
        'ultimos_pagos': ultimos_pagos,
        'mes_actual': f"{mes_es} de {hoy.year}",
        'mensajes_alertas': mensajes_alertas,
        'notificaciones_automaticas': notificaciones_automaticas,
        'notificaciones_no_leidas': total_no_leidas,
    }
    
    return render(request, 'core/dashboard.html', context)

@login_required
def perfil_usuario(request):
    # Simular perfil de usuario (RF-03: Acceder al sistema con sesión segmentada)
    perfil_simulado = {
        'nombre': 'Juan Pérez González',
        'tipo': 'Apoderado',  # o 'Directiva'
        'rut': '12.345.678-9',
        'telefono': '+56 9 8765 4321',
        'email': 'juan.perez@email.com'
    }
    
    return render(request, 'core/perfil.html', {'perfil': perfil_simulado})

@login_required
def bandeja_mensajes(request):
    """RF-08: Visualizar mensajes y alertas en bandeja por perfil"""
    import logging
    logger = logging.getLogger(__name__)
    
    logger.debug(f"Usuario accediendo a bandeja de mensajes: {request.user.username}")
    
    try:
        # Obtener notificaciones REALES de la base de datos
        from core.models import Notificacion
        
        # Filtrar por usuario si es apoderado, o mostrar todas si es staff
        if request.user.is_staff:
            # Personal del colegio ve todas las notificaciones
            notificaciones = Notificacion.objects.all().order_by('-fecha_creacion')
            tipo_usuario = 'directiva'
            logger.debug(f"Usuario staff - mostrando {notificaciones.count()} notificaciones")
        else:
            # Apoderados ven sus notificaciones (buscar por email del usuario)
            notificaciones = Notificacion.objects.filter(
                apoderado_email=request.user.email
            ).order_by('-fecha_creacion')
            tipo_usuario = 'apoderado'
            logger.debug(f"Usuario apoderado - mostrando {notificaciones.count()} notificaciones")
        
        # Convertir a formato para template
        mensajes = []
        for notif in notificaciones:
            # Determinar tipo basado en el contenido
            if 'recordatorio' in notif.mensaje.lower():
                tipo_msg = 'recordatorio'
                prioridad = 'alta'
            elif 'pago confirmado' in notif.mensaje.lower():
                tipo_msg = 'confirmacion'
                prioridad = 'baja'
            elif 'nueva actividad' in notif.mensaje.lower():
                tipo_msg = 'informativo'
                prioridad = 'media'
            else:
                tipo_msg = 'informativo'
                prioridad = 'media'
            
            mensajes.append({
                'id': notif.id,
                'tipo': tipo_msg,
                'titulo': notif.tipo.replace('_', ' ').title(),
                'mensaje': notif.mensaje,
                'fecha': notif.fecha_creacion,
                'leido': notif.leido,
                'prioridad': prioridad,
                'apoderado_nombre': notif.apoderado_nombre,
                'apoderado_email': notif.apoderado_email,
                'usuario_registra': notif.usuario_registra
            })
        
        # Contar mensajes no leídos
        mensajes_no_leidos = len([m for m in mensajes if not m['leido']])
        logger.debug(f"Mensajes no leídos: {mensajes_no_leidos}")
        
        context = {
            'mensajes': mensajes,
            'mensajes_no_leidos': mensajes_no_leidos,
            'tipo_usuario': tipo_usuario
        }
        
        logger.debug("Bandeja de mensajes cargada exitosamente")
        return render(request, 'core/bandeja_mensajes.html', context)
        
    except Exception as e:
        logger.error(f"Error en bandeja_mensajes: {str(e)}")
        logger.exception("Traceback completo:")
        
        # Fallback a datos simulados en caso de error
        mensajes = [
            {
                'id': 999,
                'tipo': 'error',
                'titulo': 'Error del Sistema',
                'mensaje': f'Ocurrió un error al cargar los mensajes: {str(e)}',
                'fecha': timezone.now(),
                'leido': False,
                'prioridad': 'alta'
            }
        ]
        
        context = {
            'mensajes': mensajes,
            'mensajes_no_leidos': 1,
            'tipo_usuario': 'apoderado'
        }
        
        return render(request, 'core/bandeja_mensajes.html', context)
