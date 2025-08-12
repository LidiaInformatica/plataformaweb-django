#!/usr/bin/env python
"""
Script para crear tipos de actividad y cursos básicos
"""
import os
import sys
import django

# Configurar Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'plataformaweb.settings')
django.setup()

from actividades.models import TipoActividad
from estudiantes.models import Curso

def crear_tipos_actividad():
    """Crear tipos de actividad básicos"""
    tipos = [
        {
            'nombre': 'Evento',
            'descripcion': 'Ceremonias, galas, graduaciones y eventos especiales'
        },
        {
            'nombre': 'Gira Educativa',
            'descripcion': 'Viajes de estudio y giras educativas'
        },
        {
            'nombre': 'Material Escolar',
            'descripcion': 'Uniformes, útiles escolares y materiales educativos'
        },
        {
            'nombre': 'Extracurricular',
            'descripcion': 'Actividades deportivas, artísticas y extracurriculares'
        },
        {
            'nombre': 'Seguro',
            'descripcion': 'Seguros escolares y de accidentes'
        },
        {
            'nombre': 'Cuota Anual',
            'descripcion': 'Cuotas anuales del centro de padres y apoderados'
        }
    ]
    
    print("=== Creando Tipos de Actividad ===")
    for tipo_data in tipos:
        tipo, created = TipoActividad.objects.get_or_create(
            nombre=tipo_data['nombre'],
            defaults={'descripcion': tipo_data['descripcion']}
        )
        if created:
            print(f"✓ Creado: {tipo.nombre}")
        else:
            print(f"- Ya existe: {tipo.nombre}")

def crear_cursos():
    """Crear cursos básicos del sistema educativo chileno si no existen"""
    cursos_chilenos = [
        # Educación Parvularia
        ('Pre Kinder', 'Parvularia', 2025),
        ('Kinder', 'Parvularia', 2025),
        
        # Educación Básica
        ('1° Básico', '1° Básico', 2025),
        ('2° Básico', '2° Básico', 2025),
        ('3° Básico', '3° Básico', 2025),
        ('4° Básico', '4° Básico', 2025),
        ('5° Básico', '5° Básico', 2025),
        ('6° Básico', '6° Básico', 2025),
        ('7° Básico', '7° Básico', 2025),
        ('8° Básico', '8° Básico', 2025),
        
        # Educación Media
        ('1° Medio', '1° Medio', 2025),
        ('2° Medio', '2° Medio', 2025),
        ('3° Medio', '3° Medio', 2025),
        ('4° Medio', '4° Medio', 2025),
    ]
    
    print("\n=== Creando Cursos del Sistema Educativo Chileno ===")
    for curso_nombre, nivel, año in cursos_chilenos:
        curso, created = Curso.objects.get_or_create(
            nombre=curso_nombre,
            defaults={
                'nivel': nivel,
                'año': año
            }
        )
        if created:
            print(f"✓ Creado: {curso.nombre}")
        else:
            print(f"- Ya existe: {curso.nombre}")

def main():
    print("=== Inicializando datos para el módulo de actividades ===\n")
    
    try:
        crear_tipos_actividad()
        crear_cursos()
        
        print(f"\n✅ Inicialización completada:")
        print(f"   - Tipos de actividad: {TipoActividad.objects.count()}")
        print(f"   - Cursos disponibles: {Curso.objects.count()}")
        print(f"\n🎯 Ya puede crear actividades en: http://127.0.0.1:8000/actividades/crear/")
        
    except Exception as e:
        print(f"❌ Error: {str(e)}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()
