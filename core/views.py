from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from datetime import datetime, timedelta
from django.db.models import Sum
from django.contrib import messages

from cuotas.models import PagoCuota as Pago
from actividades.models import Actividad
from core.models import Notificacion, PerfilUsuario
from cuotas.models import CuotaEstudiante
from estudiantes.models import Apoderado, Estudiante
from cuotas.models import PagoCuota
from django.http import HttpResponseForbidden
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required

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
    """Vista del perfil de usuario con datos reales"""
    try:
        perfil = PerfilUsuario.objects.get(usuario=request.user)
        perfil_data = {
            'nombre': request.user.get_full_name(),
            'tipo': perfil.get_tipo_perfil_display(),
            'rut': perfil.rut,
            'telefono': perfil.telefono,
            'email': request.user.email,
            'cargo_directiva': perfil.get_cargo_directiva_display() if perfil.cargo_directiva else None
        }
    except PerfilUsuario.DoesNotExist:
        # Si no tiene perfil, mostrar datos básicos del usuario
        perfil_data = {
            'nombre': request.user.get_full_name(),
            'tipo': 'Sin perfil configurado',
            'rut': request.user.username,
            'telefono': '',
            'email': request.user.email,
            'cargo_directiva': None
        }
        messages.warning(request, 'Su perfil no está completamente configurado.')
    
    return render(request, 'core/perfil.html', {'perfil': perfil_data})

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
    try:
        perfil = PerfilUsuario.objects.get(usuario=request.user)
        if perfil.tipo_perfil != 'directiva':
            messages.warning(request, 'Acceso restringido al panel de la directiva.')
            return redirect('core:dashboard')
    except PerfilUsuario.DoesNotExist:
        messages.warning(request, 'No tiene un perfil configurado. Acceso denegado.')
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
def dashboard_apoderado(request):
    """Dashboard para apoderados - Versión simplificada y segura"""
    usuario = request.user
    correo_apoderado = usuario.email
    
    # Buscar apoderados por email (manejo seguro de múltiples resultados)
    apoderados_usuario = Apoderado.objects.filter(email=correo_apoderado)
    
    # Buscar estudiantes relacionados con estos apoderados
    estudiantes_relacionados = Estudiante.objects.filter(apoderado__in=apoderados_usuario)
    
    if estudiantes_relacionados.exists():
        # Usuario con hijos/estudiantes reales
        todos_los_estudiantes = list(estudiantes_relacionados)
        
        # Información básica de los hijos
        info_hijos = []
        for estudiante in todos_los_estudiantes:
            info_hijos.append({
                'nombre_completo': f"{estudiante.nombre} {estudiante.apellido_paterno} {estudiante.apellido_materno}",
                'rut': estudiante.rut,
                'curso': str(estudiante.curso),
                'vinculo': estudiante.get_vinculo_apoderado_display() if hasattr(estudiante, 'get_vinculo_apoderado_display') else estudiante.vinculo_apoderado
            })
        
        # Datos básicos de cuotas y pagos
        cuotas = CuotaEstudiante.objects.filter(apoderado_email=correo_apoderado)
        cuotas_pagadas = cuotas.filter(estado='pagado')
        cuotas_pendientes = cuotas.filter(estado='pendiente')
        
        total_pagado = sum(pago.monto for pago in Pago.objects.filter(cuota__apoderado_email=correo_apoderado))
        total_pendiente = sum(cuota.monto for cuota in cuotas_pendientes)
        
        # Notificaciones
        notificaciones = Notificacion.objects.filter(apoderado_email=correo_apoderado)
        
        context = {
            'usuario': usuario,
            'apoderados': apoderados_usuario,
            'estudiantes': todos_los_estudiantes,
            'info_hijos': info_hijos,
            'total_hijos': len(todos_los_estudiantes),
            'cuotas_pagadas': cuotas_pagadas.count(),
            'cuotas_pendientes': cuotas_pendientes.count(),
            'total_pagado': total_pagado,
            'total_pendiente': total_pendiente,
            'notificaciones_estudiante': notificaciones,
            'tiene_datos_completos': True,
            'mensaje_bienvenida': f'Bienvenida {usuario.get_full_name()}, apoderada de {len(todos_los_estudiantes)} estudiante(s)'
        }
    else:
        # Usuario sin estudiantes - dashboard básico
        context = {
            'usuario': usuario,
            'apoderados': None,
            'estudiantes': [],
            'info_hijos': [],
            'total_hijos': 0,
            'cuotas_pagadas': 0,
            'cuotas_pendientes': 0,
            'total_pagado': 0,
            'total_pendiente': 0,
            'notificaciones_estudiante': [],
            'tiene_datos_completos': False,
            'mensaje_bienvenida': f'Bienvenido(a) {usuario.get_full_name()}',
            'mensaje_info': 'No se encontraron estudiantes asociados a su perfil de apoderado.'
        }

    return render(request, 'core/dashboard_apoderado.html', context)

    return render(request, 'core/dashboard_apoderado.html', context)

def redireccion_post_login(request):
    """Redirección inteligente basada en el perfil del usuario"""
    try:
        perfil = PerfilUsuario.objects.get(usuario=request.user)
        
        # Redirigir según tipo de perfil
        if perfil.tipo_perfil == 'directiva':
            messages.info(request, f'Bienvenido al panel de directiva.')
            return redirect('core:dashboard_directiva')
        elif perfil.tipo_perfil == 'apoderado':
            messages.info(request, f'Bienvenido al panel de apoderados.')
            return redirect('core:dashboard_apoderado')
        elif perfil.tipo_perfil == 'administrador':
            messages.info(request, f'Bienvenido al panel de administración.')
            return redirect('core:dashboard')
        else:
            messages.warning(request, f'Tipo de perfil no reconocido: {perfil.tipo_perfil}')
            return redirect('core:dashboard')
            
    except PerfilUsuario.DoesNotExist:
        # Si no tiene perfil, verificar si es superusuario
        if request.user.is_superuser:
            messages.info(request, 'Bienvenido, administrador.')
            return redirect('core:dashboard')
        else:
            messages.warning(request, 'Su perfil no está configurado correctamente. Contacte al administrador.')
            return redirect('accounts:crear_perfil')


def error_apoderado(request):
    return render(request, 'error_apoderado.html', {'mensaje': 'No se encontró el perfil Apoderado asociado.'})
