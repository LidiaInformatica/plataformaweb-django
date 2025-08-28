#!/usr/bin/env python
"""
Script para corregir los datos del estudiante y crear el registro correcto
"""
import os
import sys
import django

# Configurar Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'plataformaweb.settings')
django.setup()

from estudiantes.models import Estudiante, Apoderado, Curso
from datetime import date

def main():
    print("=== Corrigiendo datos del estudiante ===")
    
    try:
        # Buscar el estudiante creado incorrectamente
        estudiante_incorrecto = Estudiante.objects.filter(nombre="Lidia").first()
        
        if estudiante_incorrecto:
            print(f"Encontrado estudiante incorrecto: {estudiante_incorrecto}")
            
            # Guardar referencia al apoderado
            apoderado = estudiante_incorrecto.apoderado
            print(f"Apoderado: {apoderado}")
            
            # Actualizar datos del apoderado (la mamá)
            apoderado.nombre = "Lidia Andrea"
            apoderado.apellido_paterno = "Inostroza" 
            apoderado.apellido_materno = "Yañez"
            apoderado.rut = "17540322-1"  # RUT de la mamá
            apoderado.save()
            print(" Datos del apoderado (mamá) actualizados")
            
            # Actualizar datos del estudiante (el hijo)
            estudiante_incorrecto.nombre = "Benjamin Ezequiel"
            estudiante_incorrecto.apellido_paterno = "Santa Cruz"
            estudiante_incorrecto.apellido_materno = "Inostroza"
            estudiante_incorrecto.rut = "22497710-7"  # RUT del hijo
            estudiante_incorrecto.fecha_nacimiento = date(2007, 8, 31)
            estudiante_incorrecto.vinculo_apoderado = "hijo"
            estudiante_incorrecto.save()
            print(" Datos del estudiante (hijo) actualizados")
            
            print(f"\n Corrección completada:")
            print(f"   Estudiante: {estudiante_incorrecto.nombre} {estudiante_incorrecto.apellido_paterno}")
            print(f"   Apoderado: {apoderado.nombre} {apoderado.apellido_paterno}")
            print(f"   Relación: {estudiante_incorrecto.get_vinculo_apoderado_display()}")
            
        else:
            print(" No se encontró el estudiante a corregir")
            
    except Exception as e:
        print(f" Error al corregir datos: {str(e)}")

if __name__ == "__main__":
    main()
