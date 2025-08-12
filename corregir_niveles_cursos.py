#!/usr/bin/env python
"""
Script para corregir los niveles de los cursos del sistema educativo chileno
"""
import os
import sys
import django

# Configurar Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'plataformaweb.settings')
django.setup()

from estudiantes.models import Curso

def corregir_niveles_cursos():
    """Corregir los niveles de los cursos para que sean consistentes"""
    print("=== Corrigiendo niveles de cursos ===")
    
    # Mapeo de correcciones
    correcciones = {
        'Pre Kinder': 'Parvularia',
        'Kinder': 'Parvularia',
        '1° Básico': '1° Básico',
        '2° Básico': '2° Básico', 
        '3° Básico': '3° Básico',
        '4° Básico': '4° Básico',
        '5° Básico': '5° Básico',
        '6° Básico': '6° Básico',
        '7° Básico': '7° Básico',
        '8° Básico': '8° Básico',
        '1° Medio': '1° Medio',
        '2° Medio': '2° Medio',
        '3° Medio': '3° Medio',
        '4° Medio': '4° Medio'
    }
    
    cursos_corregidos = 0
    for curso in Curso.objects.all():
        if curso.nombre in correcciones:
            nuevo_nivel = correcciones[curso.nombre]
            if curso.nivel != nuevo_nivel:
                print(f"Corrigiendo {curso.nombre}: {curso.nivel} → {nuevo_nivel}")
                curso.nivel = nuevo_nivel
                curso.save()
                cursos_corregidos += 1
    
    print(f"\n✅ {cursos_corregidos} cursos corregidos")
    
    # Mostrar estado final
    print("\n=== Estado final de cursos ===")
    for curso in Curso.objects.all().order_by('id'):
        print(f"✓ {curso.nombre} - Nivel: {curso.nivel}")

def main():
    try:
        corregir_niveles_cursos()
    except Exception as e:
        print(f"❌ Error: {str(e)}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()
