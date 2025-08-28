#!/usr/bin/env python
"""
Script para corregir el curso de Benjamín Santa Cruz
De 8° Básico a 4° Medio
"""
import os
import sys
import django

# Configurar Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'plataformaweb.settings')
django.setup()

from estudiantes.models import Estudiante, Curso

def main():
    print(" Corrigiendo curso de Benjamín Santa Cruz...")
    
    try:
        # Buscar a Benjamín
        benjamin = Estudiante.objects.filter(
            nombre__icontains='Benjamin',
            apellido_paterno__icontains='Santa Cruz'
        ).first()
        
        if not benjamin:
            print(" No se encontró a Benjamín Santa Cruz")
            return
            
        print(f" Benjamín encontrado: {benjamin.nombre} {benjamin.apellido_paterno}")
        print(f" Curso actual: {benjamin.curso}")
        
        # Buscar o crear 4° Medio
        curso_4to_medio, created = Curso.objects.get_or_create(
            nombre='4° Medio',
            defaults={
                'nivel': '4° Medio',
                'descripcion': 'Cuarto año de Educación Media'
            }
        )
        
        if created:
            print(f" Curso '4° Medio' creado")
        else:
            print(f" Curso '4° Medio' ya existe")
            
        # Actualizar curso de Benjamín
        curso_anterior = benjamin.curso
        benjamin.curso = curso_4to_medio
        benjamin.save()
        
        print(f" Curso actualizado:")
        print(f"   Anterior: {curso_anterior}")
        print(f"   Nuevo: {benjamin.curso}")
        print(f" ¡Benjamín ahora está en 4° Medio!")
        
    except Exception as e:
        print(f" Error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == '__main__':
    main()
