from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db import transaction
from datetime import datetime, timedelta
from django.utils import timezone
from .models import Actividad, TipoActividad
from .forms import ActividadForm, TipoActividadForm
from estudiantes.models import Curso
from core.notificaciones import ServicioNotificaciones
import logging

logger = logging.getLogger('actividades.views')

@login_required
def lista_actividades(request):
    """Vista para mostrar la lista de actividades"""
    logger.debug("Cargando lista de actividades")
    
    # Obtener filtros de la URL
    tipo_filtro = request.GET.get('tipo', '')
    curso_filtro = request.GET.get('curso', '')
    fecha_inicio = request.GET.get('fecha_inicio', '')
    fecha_fin = request.GET.get('fecha_fin', '')
    
    # Obtener actividades reales de la base de datos
    actividades = Actividad.objects.all().order_by('-fecha_creacion')
    
    # Aplicar filtros
    if tipo_filtro:
        actividades = actividades.filter(tipo__nombre__icontains=tipo_filtro)
    
    if curso_filtro:
        actividades = actividades.filter(cursos_asignados__nombre__icontains=curso_filtro)
    
    if fecha_inicio:
        actividades = actividades.filter(fecha_inicio__gte=fecha_inicio)
    
    if fecha_fin:
        actividades = actividades.filter(fecha_fin__lte=fecha_fin)
    
    # Obtener tipos de actividad y cursos para los filtros
    tipos_actividad = TipoActividad.objects.all()
    cursos = Curso.objects.all()
    
    logger.debug(f"Encontradas {actividades.count()} actividades")
    
    context = {
        'actividades': actividades,
        'tipos_actividad': tipos_actividad,
        'cursos': cursos,
        'filtros': {
            'tipo': tipo_filtro,
            'curso': curso_filtro,
            'fecha_inicio': fecha_inicio,
            'fecha_fin': fecha_fin,
        }
    }
    
    return render(request, 'actividades/lista.html', context)

@login_required
def crear_actividad(request):
    """Vista para crear una nueva actividad"""
    logger.debug("Accediendo al formulario de crear actividad")
    
    if request.method == 'POST':
        form = ActividadForm(request.POST)
        if form.is_valid():
            try:
                with transaction.atomic():
                    actividad = form.save()
                    logger.info(f"Nueva actividad creada: {actividad.nombre}")
                    
                    #  ENVIAR NOTIFICACIÓN AUTOMÁTICA POR EMAIL
                    try:
                        notificacion_enviada = ServicioNotificaciones.enviar_notificacion_nueva_actividad(actividad)
                        if notificacion_enviada:
                            messages.success(request, f' Actividad "{actividad.nombre}" creada exitosamente. Notificación enviada por email.')
                        else:
                            messages.warning(request, f' Actividad "{actividad.nombre}" creada exitosamente. ⚠️ Error al enviar notificación por email.')
                    except Exception as e:
                        logger.error(f"Error al enviar notificación: {str(e)}")
                        messages.success(request, f' Actividad "{actividad.nombre}" creada exitosamente. ⚠️ Notificación no enviada.')
                    
                    return redirect('actividades:lista')
            except Exception as e:
                logger.error(f"Error al crear actividad: {str(e)}")
                messages.error(request, 'Error al crear la actividad. Intente nuevamente.')
        else:
            logger.warning(f"Formulario de actividad inválido: {form.errors}")
            messages.error(request, 'Por favor corrija los errores en el formulario.')
    else:
        form = ActividadForm()
    
    return render(request, 'actividades/form.html', {
        'form': form,
        'titulo': 'Nueva Actividad',
        'boton_texto': 'Crear Actividad',
        'tipos_actividad': TipoActividad.objects.all()
    })

@login_required
def editar_actividad(request, pk):
    """Vista para editar una actividad existente"""
    actividad = get_object_or_404(Actividad, pk=pk)
    logger.debug(f"Editando actividad: {actividad.nombre}")
    
    if request.method == 'POST':
        form = ActividadForm(request.POST, instance=actividad)
        if form.is_valid():
            try:
                with transaction.atomic():
                    actividad = form.save()
                    logger.info(f"Actividad actualizada: {actividad.nombre}")
                    messages.success(request, f'Actividad "{actividad.nombre}" actualizada exitosamente.')
                    return redirect('actividades:lista')
            except Exception as e:
                logger.error(f"Error al actualizar actividad: {str(e)}")
                messages.error(request, 'Error al actualizar la actividad. Intente nuevamente.')
        else:
            logger.warning(f"Formulario de actividad inválido: {form.errors}")
            messages.error(request, 'Por favor corrija los errores en el formulario.')
    else:
        form = ActividadForm(instance=actividad)
    
    return render(request, 'actividades/form.html', {
        'form': form,
        'actividad': actividad,
        'titulo': 'Editar Actividad',
        'boton_texto': 'Actualizar Actividad',
        'tipos_actividad': TipoActividad.objects.all()
    })

@login_required
def ver_actividad(request, pk):
    """Vista para ver los detalles de una actividad"""
    actividad = get_object_or_404(Actividad, pk=pk)
    logger.debug(f"Viendo detalles de actividad: {actividad.nombre}")
    
    return render(request, 'actividades/detalle.html', {
        'actividad': actividad
    })

@login_required
def eliminar_actividad(request, pk):
    """Vista para eliminar una actividad"""
    actividad = get_object_or_404(Actividad, pk=pk)
    logger.debug(f"Solicitando eliminación de actividad: {actividad.nombre}")
    
    if request.method == 'POST':
        try:
            nombre_actividad = actividad.nombre
            actividad.delete()
            logger.info(f"Actividad eliminada: {nombre_actividad}")
            messages.success(request, f'Actividad "{nombre_actividad}" eliminada exitosamente.')
            return redirect('actividades:lista')
        except Exception as e:
            logger.error(f"Error al eliminar actividad: {str(e)}")
            messages.error(request, 'Error al eliminar la actividad. Intente nuevamente.')
    
    return render(request, 'actividades/confirmar_eliminar.html', {
        'actividad': actividad
    })

@login_required
def exportar_actividades(request):
    """Vista para exportar actividades"""
    # Simular exportación
    return render(request, 'actividades/exportar.html', {
        'mensaje': 'Funcionalidad de exportación simulada. En producción se generaría un archivo Excel o CSV.'
    })
