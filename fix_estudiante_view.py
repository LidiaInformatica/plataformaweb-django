#!/usr/bin/env python
"""
Script para arreglar la vista de crear estudiante
"""
import os
import django

# Configurar Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'plataformaweb.settings')
django.setup()

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.db import transaction
from estudiantes.models import Estudiante, Apoderado, Curso
from estudiantes.forms import EstudianteForm, ApoderadoForm
import logging

logger = logging.getLogger(__name__)

# La nueva función corregida
nueva_funcion = '''@login_required
def crear_estudiante(request):
    """Vista para crear un nuevo estudiante"""
    logger.debug(" Accediendo a formulario de creación de estudiante")
    
    if request.method == 'POST':
        logger.debug(f" Datos POST recibidos: {dict(request.POST)}")
        
        # Obtener RUT del apoderado del POST
        rut_apoderado = request.POST.get('rut')  # RUT del apoderado en el formulario
        apoderado_existente = None
        
        logger.info(f" Verificando RUT del apoderado: {rut_apoderado}")
        
        # Verificar si ya existe un apoderado con este RUT
        if rut_apoderado:
            try:
                apoderado_existente = Apoderado.objects.get(rut=rut_apoderado)
                logger.info(f" Apoderado existente encontrado: {apoderado_existente.nombre}")
            except Apoderado.DoesNotExist:
                logger.info(f" No existe apoderado con RUT {rut_apoderado}")
        
        # Validar formulario de estudiante
        estudiante_form = EstudianteForm(request.POST)
        
        if estudiante_form.is_valid():
            logger.debug(" Formulario de estudiante válido")
            
            try:
                with transaction.atomic():
                    # Decidir qué hacer con el apoderado
                    if apoderado_existente:
                        # Reutilizar apoderado existente
                        apoderado = apoderado_existente
                        logger.info(f" Reutilizando apoderado: {apoderado.nombre}")
                    else:
                        # Crear nuevo apoderado
                        apoderado_form = ApoderadoForm(request.POST)
                        if not apoderado_form.is_valid():
                            logger.error(f" Formulario de apoderado inválido: {apoderado_form.errors}")
                            messages.error(request, 'Por favor corrija los errores en los datos del apoderado.')
                            return render(request, 'estudiantes/form.html', {
                                'estudiante_form': estudiante_form,
                                'apoderado_form': apoderado_form,
                                'titulo': 'Nuevo Estudiante'
                            })
                        
                        apoderado = apoderado_form.save()
                        logger.debug(f" Nuevo apoderado creado: {apoderado.nombre}")
                    
                    # Crear estudiante
                    estudiante = estudiante_form.save(commit=False)
                    estudiante.apoderado = apoderado
                    estudiante.save()
                    
                    logger.debug(f" Estudiante creado: {estudiante.nombre}")
                    
                    # Contar hijos del apoderado
                    total_hijos = Estudiante.objects.filter(apoderado=apoderado).count()
                    
                    if apoderado_existente:
                        messages.success(request, f' {estudiante.nombre} registrado como hijo #{total_hijos} de {apoderado.nombre}')
                        logger.info(f" Hijo #{total_hijos} agregado a {apoderado.nombre}")
                    else:
                        messages.success(request, f' Estudiante {estudiante.nombre} y apoderado {apoderado.nombre} creados')
                        logger.info(f" Nuevo estudiante y apoderado creados")
                    
                    return redirect('estudiantes:lista')
                    
            except Exception as e:
                logger.error(f" Error al crear estudiante: {str(e)}", exc_info=True)
                messages.error(request, f'Error al crear el estudiante: {str(e)}')
        else:
            logger.error(" Formulario de estudiante inválido")
            logger.error(f"Errores estudiante: {estudiante_form.errors}")
            
        # Si llegamos aquí, mostrar formulario con errores
        if 'apoderado_form' not in locals():
            apoderado_form = ApoderadoForm(request.POST)
        
    else:
        logger.info(" Cargando formulario GET")
        estudiante_form = EstudianteForm()
        apoderado_form = ApoderadoForm()
    
    context = {
        'estudiante_form': estudiante_form,
        'apoderado_form': apoderado_form,
        'titulo': 'Nuevo Estudiante'
    }
    
    return render(request, 'estudiantes/form.html', context)'''

print("Nueva función lista para reemplazar en estudiantes/views.py")
print("\nCopia este contenido y reemplaza la función crear_estudiante manualmente.")
print("\nO puedo intentar hacer el reemplazo automáticamente si me das permiso.")
