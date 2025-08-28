#!/usr/bin/env python
"""
Script para corregir directamente los datos del estudiante desde la base de datos
"""
import os
import sys
import django

# Configurar Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'plataformaweb.settings')
django.setup()

from estudiantes.models import Estudiante, Apoderado
from datetime import date

def main():
    print("=== Corrigiendo datos del estudiante ===")
    
    try:
        # Buscar el estudiante con RUT 175403221 (el que aparece en la imagen)
        estudiante = Estudiante.objects.filter(rut="175403221").first()
        
        if estudiante:
            print(f"✓ Encontrado estudiante: {estudiante.nombre} {estudiante.apellido_paterno}")
            print(f"  RUT actual: {estudiante.rut}")
            print(f"  Apoderado: {estudiante.apoderado.nombre}")
            
            # Corregir datos del estudiante (Benjamin)
            estudiante.nombre = "Benjamin Ezequiel"
            estudiante.apellido_paterno = "Santa Cruz"
            estudiante.apellido_materno = "Inostroza"
            estudiante.rut = "22497710-7"
            estudiante.fecha_nacimiento = date(2007, 8, 31)
            estudiante.vinculo_apoderado = "hijo"
            estudiante.save()
            
            print("\n Datos del estudiante corregidos:")
            print(f"   Nombre: {estudiante.nombre} {estudiante.apellido_paterno} {estudiante.apellido_materno}")
            print(f"   RUT: {estudiante.rut}")
            print(f"   Fecha nacimiento: {estudiante.fecha_nacimiento}")
            print(f"   Vínculo: {estudiante.get_vinculo_apoderado_display()}")
            print(f"   Apoderado: {estudiante.apoderado.nombre} {estudiante.apoderado.apellido_paterno}")
            
        else:
            print(" No se encontró el estudiante con RUT 175403221")
            
            # Mostrar todos los estudiantes para debug
            print("\n--- Todos los estudiantes en la base de datos ---")
            for est in Estudiante.objects.all():
                print(f"ID: {est.id}, RUT: {est.rut}, Nombre: {est.nombre} {est.apellido_paterno}")
            
    except Exception as e:
        print(f" Error: {str(e)}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()
