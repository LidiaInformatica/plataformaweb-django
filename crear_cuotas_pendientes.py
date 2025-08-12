#!/usr/bin/env python
"""
Script para crear cuotas pendientes para probar el sistema de notificaciones
"""
import os
import sys
import django

# Configurar Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'plataformaweb.settings')
django.setup()

from cuotas.models import CuotaEstudiante
from estudiantes.models import Estudiante
from actividades.models import Actividad
from datetime import date

def main():
    print("=== Creando cuotas pendientes ===")
    
    # Obtener las actividades que creamos
    try:
        actividad1 = Actividad.objects.get(nombre="Matrícula 2026")
        actividad2 = Actividad.objects.get(nombre="Materiales Escolares Agosto")
        actividad3 = Actividad.objects.get(nombre="Excursión Pedagógica")
        print("✓ Actividades encontradas")
    except Actividad.DoesNotExist as e:
        print(f"❌ Error: No se encontró una actividad: {e}")
        return
    
    # Obtener todos los estudiantes
    estudiantes = Estudiante.objects.all()
    print(f"✓ Total estudiantes: {estudiantes.count()}")
    
    if estudiantes.count() == 0:
        print("❌ No hay estudiantes en la base de datos")
        return
    
    # Crear cuotas pendientes para cada estudiante
    print("\n--- Creando cuotas de matrícula ---")
    for estudiante in estudiantes:
        # Verificar si ya existe una cuota para esta actividad
        if not CuotaEstudiante.objects.filter(estudiante=estudiante, actividad=actividad1).exists():
            CuotaEstudiante.objects.create(
                estudiante=estudiante,
                actividad=actividad1,
                monto_total=actividad1.monto_por_estudiante,
                monto_pagado=0,
                estado='pendiente',
                fecha_vencimiento=date(2025, 8, 31)
            )
            print(f"✓ Cuota matrícula creada para {estudiante.nombre}")
        else:
            print(f"⚠ Cuota matrícula ya existe para {estudiante.nombre}")
    
    # Crear cuotas de materiales escolares para todos
    print("\n--- Creando cuotas de materiales escolares ---")
    for estudiante in estudiantes:
        if not CuotaEstudiante.objects.filter(estudiante=estudiante, actividad=actividad2).exists():
            CuotaEstudiante.objects.create(
                estudiante=estudiante,
                actividad=actividad2,
                monto_total=actividad2.monto_por_estudiante,
                monto_pagado=0,
                estado='pendiente',
                fecha_vencimiento=date(2025, 8, 25)
            )
            print(f"✓ Cuota materiales creada para {estudiante.nombre}")
        else:
            print(f"⚠ Cuota materiales ya existe para {estudiante.nombre}")
    
    # Crear cuotas de excursión solo para algunos estudiantes (para variar)
    print("\n--- Creando cuotas de excursión ---")
    estudiantes_excursion = estudiantes[:4]  # Solo los primeros 4
    for estudiante in estudiantes_excursion:
        if not CuotaEstudiante.objects.filter(estudiante=estudiante, actividad=actividad3).exists():
            CuotaEstudiante.objects.create(
                estudiante=estudiante,
                actividad=actividad3,
                monto_total=actividad3.monto_por_estudiante,
                monto_pagado=0,
                estado='pendiente',
                fecha_vencimiento=date(2025, 8, 20)
            )
            print(f"✓ Cuota excursión creada para {estudiante.nombre}")
        else:
            print(f"⚠ Cuota excursión ya existe para {estudiante.nombre}")
    
    # Verificar cuántas cuotas pendientes tenemos
    print("\n=== RESUMEN ===")
    cuotas_pendientes = CuotaEstudiante.objects.filter(estado='pendiente')
    print(f"Total cuotas pendientes: {cuotas_pendientes.count()}")
    
    # Mostrar resumen por actividad
    for actividad in [actividad1, actividad2, actividad3]:
        count = CuotaEstudiante.objects.filter(actividad=actividad, estado='pendiente').count()
        total_monto = sum(c.monto_total for c in CuotaEstudiante.objects.filter(actividad=actividad, estado='pendiente'))
        print(f"• {actividad.nombre}: {count} cuotas pendientes (${total_monto:,.0f} total)")
    
    print("\n✅ Proceso completado. Ya puedes probar el registro de pagos y las notificaciones.")

if __name__ == "__main__":
    main()
