from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.db import transaction
from .models import Estudiante, Apoderado, Curso
from .forms import EstudianteForm, ApoderadoForm
import logging

logger = logging.getLogger(__name__)

@login_required
def lista_estudiantes(request):
    """Vista para mostrar la lista de estudiantes reales"""
    logger.debug("Cargando lista de estudiantes")
    
    try:
        estudiantes = Estudiante.objects.select_related('curso', 'apoderado').all()
        logger.debug(f"Encontrados {estudiantes.count()} estudiantes")
        
        # Calcular estadísticas
        total_estudiantes = estudiantes.count()
        cursos_activos = Curso.objects.count()
        apoderados_count = Apoderado.objects.count()
        estudiantes_activos = estudiantes.filter(activo=True).count()
        
        context = {
            'estudiantes': estudiantes,
            'total_estudiantes': total_estudiantes,
            'cursos_activos': cursos_activos,
            'apoderados_count': apoderados_count,
            'estudiantes_activos': estudiantes_activos,
        }
        
        return render(request, 'estudiantes/lista.html', context)
        
    except Exception as e:
        logger.error(f"Error al cargar lista de estudiantes: {str(e)}")
        messages.error(request, f"Error al cargar los estudiantes: {str(e)}")
        return render(request, 'estudiantes/lista.html', {'estudiantes': []})

@login_required
def crear_estudiante(request):
    """Vista para crear un nuevo estudiante"""
    logger.debug(" Accediendo a formulario de creación de estudiante")
    
    if request.method == 'POST':
        logger.debug(f" Datos POST recibidos: {dict(request.POST)}")

        #  Buscar o crear el apoderado ANTES de validar estudiante
        rut_apoderado = request.POST.get('apoderado-rut')
        apoderado_existente = None
        apoderado = None

        if rut_apoderado:
            try:
                apoderado_existente = Apoderado.objects.get(rut=rut_apoderado)
                apoderado = apoderado_existente
                logger.info(f" Apoderado existente encontrado: {apoderado.nombre} (RUT: {rut_apoderado})")
            except Apoderado.DoesNotExist:
                logger.info(f" No existe apoderado con RUT {rut_apoderado}, creando uno nuevo desde datos POST")
                apoderado_form_temp = ApoderadoForm(request.POST, prefix='apoderado')
                if apoderado_form_temp.is_valid():
                    apoderado = apoderado_form_temp.save()
                    logger.debug(f" Nuevo apoderado creado: {apoderado.nombre}")
                else:
                    logger.error(f" Formulario de apoderado inválido: {apoderado_form_temp.errors}")
                    messages.error(request, 'Por favor corrija los errores en los datos del apoderado.')
                    return render(request, 'estudiantes/form.html', {
                        'estudiante_form': EstudianteForm(prefix='estudiante'),
                        'apoderado_form': apoderado_form_temp,
                        'titulo': 'Nuevo Estudiante'
                    })

        #  Clonar POST e inyectar el ID del apoderado para que EstudianteForm lo reciba
        post_modificado = request.POST.copy()
        if apoderado:
            post_modificado[f'estudiante-apoderado'] = apoderado.id

        #  Crear formularios con prefijo
        estudiante_form = EstudianteForm(post_modificado, prefix='estudiante')
        apoderado_form = ApoderadoForm(request.POST, prefix='apoderado')

        logger.debug(f" Formulario estudiante válido: {estudiante_form.is_valid()}")

        if estudiante_form.is_valid():
            logger.debug(" Formulario de estudiante válido")
            try:
                with transaction.atomic():
                    estudiante = estudiante_form.save(commit=False)
                    estudiante.apoderado = apoderado
                    estudiante.save()

                    logger.debug(f" Estudiante creado: {estudiante.nombre} - Apoderado: {apoderado.nombre}")
                    
                    total_hijos = Estudiante.objects.filter(apoderado=apoderado).count()
                    
                    if apoderado_existente:
                        messages.success(request, f' {estudiante.nombre} registrado como hijo #{total_hijos} de {apoderado.nombre}')
                        logger.info(f" Hijo #{total_hijos} agregado a {apoderado.nombre}")
                    else:
                        messages.success(request, f' Estudiante {estudiante.nombre} y apoderado {apoderado.nombre} creados exitosamente')
                        logger.info(f" Nuevo estudiante y apoderado creados")
                    
                    return redirect('estudiantes:lista')
                    
            except Exception as e:
                logger.error(f" Error al crear estudiante: {str(e)}", exc_info=True)
                messages.error(request, f'Error al crear el estudiante: {str(e)}')
        else:
            logger.error(" Formulario de estudiante inválido")
            logger.error(f"Errores estudiante: {estudiante_form.errors}")
            
    else:
        logger.info(" Cargando formulario GET")
        estudiante_form = EstudianteForm(prefix='estudiante')
        apoderado_form = ApoderadoForm(prefix='apoderado')
    
    context = {
        'estudiante_form': estudiante_form,
        'apoderado_form': apoderado_form,
        'titulo': 'Nuevo Estudiante'
    }
    
    return render(request, 'estudiantes/form.html', context)

@login_required 
def buscar_apoderado_ajax(request):
    """Vista AJAX para buscar apoderado por RUT y autocompletar datos"""
    if request.method == 'GET':
        rut = request.GET.get('rut', '').strip()
        
        if rut:
            try:
                apoderado = Apoderado.objects.get(rut=rut)
                # Contar cuántos hijos tiene
                hijos = Estudiante.objects.filter(apoderado=apoderado)
                
                data = {
                    'encontrado': True,
                    'apoderado': {
                        'nombre': apoderado.nombre,
                        'apellido_paterno': apoderado.apellido_paterno,
                        'apellido_materno': apoderado.apellido_materno,
                        'telefono': apoderado.telefono,
                        'email': apoderado.email,
                        'direccion': apoderado.direccion,
                    },
                    'hijos': [
                        {
                            'nombre': f"{h.nombre} {h.apellido_paterno}",
                            'curso': str(h.curso)
                        } for h in hijos
                    ],
                    'total_hijos': hijos.count()
                }
                logger.info(f" Apoderado encontrado: {apoderado.nombre} con {hijos.count()} hijo(s)")
                
            except Apoderado.DoesNotExist:
                data = {
                    'encontrado': False,
                    'mensaje': 'No se encontró apoderado con este RUT'
                }
                logger.info(f" No se encontró apoderado con RUT: {rut}")
                
        else:
            data = {
                'encontrado': False,
                'mensaje': 'RUT no proporcionado'
            }
            
        return JsonResponse(data)
    
    return JsonResponse({'error': 'Método no permitido'})

@login_required
def editar_estudiante(request, pk):
    """Vista para editar un estudiante existente"""
    estudiante = get_object_or_404(Estudiante, pk=pk)
    apoderado = estudiante.apoderado
    
    logger.debug(f"Editando estudiante: {estudiante.nombre}")
    
    if request.method == 'POST':
        estudiante_form = EstudianteForm(request.POST, instance=estudiante)
        apoderado_form = ApoderadoForm(request.POST, instance=apoderado)
        
        if estudiante_form.is_valid() and apoderado_form.is_valid():
            try:
                with transaction.atomic():
                    apoderado_form.save()
                    estudiante_form.save()
                    
                    logger.debug(f"Estudiante actualizado: {estudiante.nombre}")
                    messages.success(request, f'Estudiante {estudiante.nombre} actualizado exitosamente')
                    return redirect('estudiantes:lista')
                    
            except Exception as e:
                logger.error(f"Error al actualizar estudiante: {str(e)}")
                messages.error(request, f'Error al actualizar el estudiante: {str(e)}')
    else:
        estudiante_form = EstudianteForm(instance=estudiante)
        apoderado_form = ApoderadoForm(instance=apoderado)
    
    context = {
        'estudiante_form': estudiante_form,
        'apoderado_form': apoderado_form,
        'estudiante': estudiante,
        'titulo': f'Editar Estudiante - {estudiante.nombre}'
    }
    
    return render(request, 'estudiantes/form.html', context)

@login_required
def ver_estudiante(request, pk):
    """Vista para ver detalles de un estudiante"""
    estudiante = get_object_or_404(Estudiante, pk=pk)
    logger.debug(f"Viendo detalles de estudiante: {estudiante.nombre}")
    
    context = {
        'estudiante': estudiante,
    }
    
    return render(request, 'estudiantes/detalle.html', context)

@login_required
def eliminar_estudiante(request, pk):
    """Vista para eliminar un estudiante"""
    estudiante = get_object_or_404(Estudiante, pk=pk)
    
    if request.method == 'POST':
        nombre = estudiante.nombre
        try:
            estudiante.delete()
            logger.debug(f"Estudiante eliminado: {nombre}")
            messages.success(request, f'Estudiante {nombre} eliminado exitosamente')
        except Exception as e:
            logger.error(f"Error al eliminar estudiante: {str(e)}")
            messages.error(request, f'Error al eliminar el estudiante: {str(e)}')
        
        return redirect('estudiantes:lista')
    
    context = {
        'estudiante': estudiante,
    }
    
    return render(request, 'estudiantes/confirmar_eliminar.html', context)
