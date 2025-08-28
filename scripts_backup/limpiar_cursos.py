#!/usr/bin/env python
"""
Script para limpiar cursos duplicados y mantener solo el sistema educativo chileno estándar
"""
import os
import sys
import django

# Configurar Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'plataformaweb.settings')
django.setup()

from estudiantes.models import Curso

def limpiar_cursos_duplicados():
    """Limpiar cursos duplicados y mantener solo el sistema educativo chileno"""
    print("=== Analizando cursos en la base de datos ===")
    
    # Obtener todos los cursos
    todos_cursos = Curso.objects.all().order_by('nombre')
    print(f"Total de cursos encontrados: {todos_cursos.count()}")
    
    print("\n--- Lista actual de cursos ---")
    for curso in todos_cursos:
        print(f"ID: {curso.id}, Nombre: {curso.nombre}, Nivel: {curso.nivel}, Año: {curso.año}")
    
    # Cursos válidos del sistema educativo chileno
    cursos_validos = [
        'Pre Kinder', 'Kinder',
        '1° Básico', '2° Básico', '3° Básico', '4° Básico', 
        '5° Básico', '6° Básico', '7° Básico', '8° Básico',
        '1° Medio', '2° Medio', '3° Medio', '4° Medio'
    ]
    
    # Identificar cursos a eliminar (duplicados o no válidos)
    cursos_a_eliminar = []
    for curso in todos_cursos:
        if curso.nombre not in cursos_validos:
            cursos_a_eliminar.append(curso)
    
    print(f"\n=== Cursos a eliminar: {len(cursos_a_eliminar)} ===")
    for curso in cursos_a_eliminar:
        print(f"- {curso.nombre} (ID: {curso.id})")
    
    if cursos_a_eliminar:
        respuesta = input(f"\n¿Eliminar {len(cursos_a_eliminar)} cursos duplicados/no válidos? (s/n): ")
        if respuesta.lower() == 's':
            for curso in cursos_a_eliminar:
                print(f"Eliminando: {curso.nombre}")
                curso.delete()
            print(f" {len(cursos_a_eliminar)} cursos eliminados")
        else:
            print(" Operación cancelada")
    else:
        print(" No hay cursos duplicados para eliminar")
    
    # Mostrar estado final
    cursos_finales = Curso.objects.all().order_by('nombre')
    print(f"\n=== Estado final ===")
    print(f"Total de cursos: {cursos_finales.count()}")
    print("\n--- Cursos válidos ---")
    for curso in cursos_finales:
        print(f" {curso.nombre} ({curso.nivel})")

def main():
    try:
        limpiar_cursos_duplicados()
    except Exception as e:
        print(f" Error: {str(e)}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()
