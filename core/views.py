from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from datetime import datetime, timedelta
from django.db.models import Sum
from django.contrib import messages

from cuotas.models import PagoCuota as Pago
from actividades.models import Actividad
from estudiantes.models import Estudiante
from core.models import Notificacion
from cuotas.models import CuotaEstudiante

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
    recaudacion_total = sum(pago.monto for pago in Pago.objects.filter(cuota__estado='pagado'))
    cuotas_pendientes = Pago.objects.filter(cuota__estado='pendiente').count()
    actividades_activas = Actividad.objects.filter(estado='activa').count()
    total_estudiantes = Estudiante.objects.count()
    notificaciones_no_leidas = Notificacion.objects.filter(leida=False).count()

    ultimos_pagos = Pago.objects.select_related('cuota__estudiante', 'cuota__actividad').order_by('-fecha_pago')[:10]
    notificaciones_automaticas = Notificacion.objects.filter(tipo__in=['recordatorio', 'nueva_cuota']).order_by('-fecha_envio')[:10]

    context = {
        'mes_actual': 'Agosto 2025',
        'recaudacion_total': recaudacion_total,
        'cuotas_pendientes': cuotas_pendientes,
        'actividades_activas': actividades_activas,
        'total_estudiantes': total_estudiantes,
        'notificaciones_no_leidas': notificaciones_no_leidas,
        'ultimos_pagos': [
            {
                'estudiante': str(pago.cuota.estudiante),
                'actividad': pago.cuota.actividad.nombre,
                'monto': pago.monto,
                'fecha': pago.fecha_pago,
                'estado': pago.cuota.estado,
            }
            for pago in ultimos_pagos
        ],
        'notificaciones_automaticas': [
            {
                'tipo': notif.tipo,
                'mensaje': notif.mensaje,
                'estudiante': str(notif.estudiante) if notif.estudiante else 'Sin estudiante',
                'fecha_envio': notif.fecha_envio,
                'estado': notif.estado,
            }
            for notif in notificaciones_automaticas
        ],
        'mensajes_alertas': [],
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
    
@login_required
def dashboard_directiva(request):
    # Validación de perfil
    perfil = getattr(request.user, 'perfilusuario', None)
    if not perfil or perfil.tipo_perfil != 'directiva':
        messages.warning(request, 'Acceso restringido al panel de la directiva.')
        return redirect('core:dashboard')

    # Datos financieros
    cuotas = CuotaEstudiante.objects.all()
    total_cuotas = cuotas.count()
    total_pagado = sum(c.monto_pagado for c in cuotas)
    cuotas_vencidas = cuotas.filter(estado='vencido').count()
    pagos_pendientes = cuotas.filter(estado='pendiente').count()

    # Actividades institucionales
    actividades = Actividad.objects.select_related('responsable').all()

    # Estudiantes registrados
    estudiantes = Estudiante.objects.select_related('apoderado').all()

    # Notificaciones enviadas
    notificaciones_raw = Notificacion.objects.select_related('estudiante').all()
    notificaciones = []
    for notif in notificaciones_raw:
        estudiante = notif.estudiante
        notificaciones.append({
            'fecha': notif.fecha_creacion,
            'mensaje': notif.mensaje,
            'estado': notif.estado,
            'nombre': estudiante.nombre if estudiante else 'Sin nombre',
            'rut': estudiante.rut if estudiante else 'Sin RUT',
            'numero': estudiante.id if estudiante else 'No asignado',
        })

    context = {
        'total_cuotas': total_cuotas,
        'total_pagado': total_pagado,
        'cuotas_vencidas': cuotas_vencidas,
        'pagos_pendientes': pagos_pendientes,
        'actividades': actividades,
        'estudiantes': estudiantes,
        'notificaciones': notificaciones,
    }

    return render(request, 'core/dashboard_directiva.html', context)

@login_required
def vista_apoderado(request):
    """Vista exclusiva para Apoderados"""
    if not request.user.groups.filter(name='Apoderado').exists():
        messages.warning(request, 'No tiene permisos para acceder al panel de apoderado.')
        return redirect('core:dashboard')

    from cuotas.models import CuotaEstudiante, PagoCuota
    from actividades.models import Actividad
    from core.models import Notificacion

    hoy = timezone.now().date()
    mes_en = hoy.strftime('%B')
    mes_es = MESES_ES.get(mes_en, mes_en)

    cuotas_apoderado = CuotaEstudiante.objects.filter(apoderado_email=request.user.email)
    pagos_apoderado = PagoCuota.objects.filter(cuota__apoderado_email=request.user.email)

    recaudacion_total = pagos_apoderado.aggregate(total=Sum('monto'))['total'] or 0
    cuotas_pendientes = cuotas_apoderado.filter(estado='pendiente').count()
    actividades_activas = Actividad.objects.count()

    ultimos_pagos = pagos_apoderado.select_related('cuota__actividad').order_by('-fecha_pago')[:5]

    pagos_formateados = []
    for pago in ultimos_pagos:
        pagos_formateados.append({
            'actividad': pago.cuota.actividad.nombre,
            'monto': pago.monto,
            'fecha': pago.fecha_pago.date(),
            'estado': pago.cuota.estado
        })

    notificaciones = Notificacion.objects.filter(
        apoderado_email=request.user.email
    ).order_by('-fecha_creacion')[:10]

    total_no_leidas = notificaciones.filter(leida=False).count()

    notificaciones_automaticas = []
    for notif in notificaciones:
        notificaciones_automaticas.append({
            'titulo': notif.titulo,
            'mensaje': notif.mensaje[:100] + '...' if len(notif.mensaje) > 100 else notif.mensaje,
            'fecha_envio': notif.fecha_creacion.date(),
            'tipo': notif.get_tipo_display(),
            'estado': notif.estado
        })

    context = {
        'recaudacion_total': recaudacion_total,
        'cuotas_pendientes': cuotas_pendientes,
        'actividades_activas': actividades_activas,
        'ultimos_pagos': pagos_formateados,
        'mes_actual': f"{mes_es} de {hoy.year}",
        'notificaciones_automaticas': notificaciones_automaticas,
        'notificaciones_no_leidas': total_no_leidas,
    }

    return render(request, 'core/vista_apoderado.html', context)

def redireccion_post_login(request):
    perfil = getattr(request.user, 'perfilusuario', None)
    if perfil and perfil.tipo_perfil == 'directiva':
        return redirect('core:dashboard_directiva')
    elif perfil and perfil.tipo_perfil == 'apoderado':
        return redirect('core:vista_apoderado')
    else:
        return redirect('core:dashboard')


