from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils import timezone
from django.db.models import Sum
from django.http import HttpResponseForbidden

# Modelos
from cuotas.models import PagoCuota, CuotaEstudiante
from actividades.models import Actividad
from estudiantes.models import Apoderado, Estudiante
from core.models import Notificacion, PerfilUsuario
from .decorators import grupo_requerido

# Logging
import logging

logger = logging.getLogger(__name__)

from functools import wraps

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


def grupo_requerido(nombre_grupo):
    def decorator(view_func):
        @wraps(view_func)
        def wrapper(request, *args, **kwargs):
            if not request.user.groups.filter(name=nombre_grupo).exists():
                messages.error(request, f'Acceso denegado. Se requiere pertenecer al grupo {nombre_grupo}')
                return HttpResponseForbidden('Acceso denegado')
            return view_func(request, *args, **kwargs)

        return wrapper

    return decorator


@login_required
def dashboard(request):
    """Dashboard principal que redirige según el grupo del usuario"""
    logger.debug(f"Usuario {request.user} accediendo al dashboard principal")
    try:
        perfil = PerfilUsuario.objects.get(usuario=request.user)
        logger.info(f"Perfil encontrado: {perfil.tipo_perfil}")

        if perfil.tipo_perfil == 'directiva':
            return redirect('core:dashboard_directiva')
        elif perfil.tipo_perfil == 'apoderado':
            return redirect('core:dashboard_apoderado')
        elif perfil.tipo_perfil == 'administrador':
            context = _get_admin_dashboard_context()
            return render(request, 'core/dashboard.html', context)
        else:
            messages.error(request, "Tipo de perfil no reconocido.")
            return redirect('accounts:login')
    except PerfilUsuario.DoesNotExist:
        if request.user.is_superuser:
            context = _get_admin_dashboard_context()
            return render(request, 'core/dashboard.html', context)
        else:
            return redirect('core:error_apoderado')


def _get_admin_dashboard_context():
    """Helper function para obtener contexto del dashboard admin"""
    recaudacion_total = PagoCuota.objects.filter(
        cuota__estado='pagado'
    ).aggregate(Sum('monto'))['monto__sum'] or 0

    ultimos_pagos = PagoCuota.objects.select_related(
        'cuota__estudiante',
        'cuota__actividad'
    ).order_by('-fecha_pago')[:10]

    mes_actual = timezone.now().strftime('%B %Y')
    mes_actual_es = MESES_ES[mes_actual.split()[0]] + ' ' + mes_actual.split()[1]

    return {
        'mes_actual': mes_actual_es,
        'recaudacion_total': recaudacion_total,
        'cuotas_pendientes': CuotaEstudiante.objects.filter(estado='pendiente').count(),
        'actividades_activas': Actividad.objects.filter(estado='activa').count(),
        'total_estudiantes': Estudiante.objects.count(),
        'notificaciones_no_leidas': Notificacion.objects.filter(leida=False).count(),
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
        'notificaciones_automaticas': Notificacion.objects.filter(
            tipo__in=['recordatorio', 'nueva_cuota']
        ).order_by('-fecha_envio')[:10]
    }


@login_required
@grupo_requerido('Apoderado')
def dashboard_apoderado(request):
    try:
        perfil = PerfilUsuario.objects.filter(usuario=request.user, tipo_perfil='apoderado').first()
        if not perfil:
            messages.error(request, "No tiene un perfil de apoderado configurado")
            return redirect('core:error_apoderado')

        apoderado = Apoderado.objects.filter(usuario=request.user).first()
        if not apoderado:
            messages.error(request, "No tiene un apoderado asociado")
            return redirect('core:error_apoderado')

        estudiantes = Estudiante.objects.filter(apoderado=apoderado)
        if not estudiantes.exists():
            return render(request, 'core/dashboard_apoderado.html', {
                'mensaje': "No tiene estudiantes asociados a su perfil.",
                'perfil': perfil,
                'estudiantes_info': [],
                'notificaciones_estudiante': [],
            })

        estudiantes_info = []
        for estudiante in estudiantes:
            cuotas = CuotaEstudiante.objects.filter(estudiante=estudiante)
            actividades_asignadas = Actividad.objects.filter(cursos_asignados=estudiante.curso)
            pagos_estudiante = PagoCuota.objects.filter(cuota__estudiante=estudiante).order_by('-fecha_pago')
            # Usa el campo correcto: monto_total
            total_pendiente = cuotas.filter(estado='pendiente').aggregate(Sum('monto_total'))['monto_total__sum'] or 0
            total_pagado = cuotas.filter(estado='pagado').aggregate(Sum('monto_total'))['monto_total__sum'] or 0
            estudiantes_info.append({
                'estudiante': estudiante,
                'actividades_asignadas': actividades_asignadas,
                'cuotas_pendientes': cuotas.filter(estado='pendiente').count(),
                'cuotas_pagadas': cuotas.filter(estado='pagado').count(),
                'total_pendiente': total_pendiente,
                'total_pagado': total_pagado,
                'pagos_estudiante': pagos_estudiante,
            })

        notificaciones_estudiante = Notificacion.objects.filter(usuario_registra=request.user).order_by('-fecha_envio')

        context = {
            'perfil': perfil,
            'estudiantes_info': estudiantes_info,
            'notificaciones_estudiante': notificaciones_estudiante,
        }
        return render(request, 'core/dashboard_apoderado.html', context)

    except Exception as e:
        import traceback
        print(traceback.format_exc())
        messages.error(request, "Ocurrió un error al cargar el dashboard")
        return redirect('core:error_apoderado')

@login_required
@grupo_requerido('Directiva')
def dashboard_directiva(request):
    """Vista del dashboard para directiva"""
    try:
        context = {
            'total_estudiantes': Estudiante.objects.count(),
            'total_cuotas': CuotaEstudiante.objects.count(),
            'cuotas_pendientes': CuotaEstudiante.objects.filter(estado='pendiente'),
            'cuotas_pagadas': CuotaEstudiante.objects.filter(estado='pagado'),
            'estudiantes_recientes': Estudiante.objects.all().order_by('-fecha_registro')[:5],
            'actividades': Actividad.objects.all(),
            'recaudacion_total': PagoCuota.objects.filter(
                cuota__estado='pagado'
            ).aggregate(Sum('monto'))['monto__sum'] or 0,
            'notificaciones': Notificacion.objects.all().order_by('-fecha_creacion')[:5]
        }
        return render(request, 'core/dashboard_directiva.html', context)

    except Exception as e:
        logger.error(f"Error en dashboard_directiva: {str(e)}")
        messages.error(request, "Ocurrió un error al cargar el dashboard")
        return redirect('core:error_apoderado')


@login_required
def perfil_usuario(request):
    """Vista del perfil de usuario"""
    try:
        perfil = PerfilUsuario.objects.get(usuario=request.user)
        context = {
            'perfil': {
                'nombre': request.user.get_full_name() or request.user.username,
                'tipo': perfil.get_tipo_perfil_display(),
                'rut': perfil.rut,
                'email': request.user.email,
                'telefono': perfil.telefono if hasattr(perfil, 'telefono') else None,
                'cargo_directiva': perfil.get_cargo_directiva_display() if hasattr(perfil, 'cargo_directiva') else None
            }
        }
        return render(request, 'core/perfil.html', context)
    except PerfilUsuario.DoesNotExist:
        logger.warning(f"Perfil no encontrado para usuario {request.user}")
        messages.error(request, 'Perfil no encontrado')
        return redirect('core:dashboard')


@login_required
def redireccion_post_login(request):
    """Redirección inteligente post-login"""
    try:
        perfil = PerfilUsuario.objects.get(usuario=request.user)
        if perfil.tipo_perfil == 'directiva':
            messages.success(request, 'Bienvenido al panel de directiva.')
            return redirect('core:dashboard_directiva')
        elif perfil.tipo_perfil == 'apoderado':
            messages.success(request, 'Bienvenido al panel de apoderados.')
            return redirect('core:dashboard_apoderado')
        elif perfil.tipo_perfil == 'administrador':
            messages.success(request, 'Bienvenido al panel de administración.')
            return redirect('core:dashboard')
    except PerfilUsuario.DoesNotExist:
        if request.user.is_superuser:
            messages.success(request, 'Bienvenido, administrador.')
            return redirect('core:dashboard')
        messages.warning(request, 'Perfil no configurado. Contacte al administrador.')
        return redirect('accounts:crear_perfil')


@login_required
def error_apoderado(request):
    """Vista de error para perfil no encontrado"""
    return render(request, 'core/error_apoderado.html', {
        'mensaje': 'No tiene permiso para acceder a esta sección.'
    })


@login_required
def bandeja_mensajes(request):
    """Vista de bandeja de mensajes"""
    try:
        if request.user.is_staff:
            notificaciones = Notificacion.objects.all().order_by('-fecha_creacion')
            tipo_usuario = 'directiva'
        else:
            notificaciones = Notificacion.objects.filter(
                destinatario=request.user
            ).order_by('-fecha_creacion')
            tipo_usuario = 'apoderado'

        context = {
            'mensajes': notificaciones,
            'mensajes_no_leidos': notificaciones.filter(leida=False).count(),
            'tipo_usuario': tipo_usuario
        }
        return render(request, 'core/bandeja_mensajes.html', context)

    except Exception as e:
        logger.error(f"Error en bandeja_mensajes: {str(e)}")
        messages.error(request, "Error al cargar los mensajes")
        return redirect('core:dashboard')