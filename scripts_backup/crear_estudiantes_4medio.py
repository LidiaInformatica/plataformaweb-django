#!/usr/bin/env python
"""
Script para crear 25 estudiantes para 4° Medio
Para demostración del sistema escolar
"""

import os
import sys
import django
from datetime import date
import random

# Configurar Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'plataformaweb.settings')
django.setup()

from estudiantes.models import Estudiante, Apoderado, Curso

# Datos realistas para estudiantes chilenos de 4° Medio
ESTUDIANTES_DATA = [
    # Nombre, Apellido Paterno, Apellido Materno, RUT (sin DV), Nombre Apoderado, Apellido Apoderado, RUT Apoderado
    ("Matías", "González", "Pérez", "21234567", "Carmen", "Pérez", "15123456"),
    ("Valentina", "Rodríguez", "Silva", "21345678", "Roberto", "Silva", "14234567"),
    ("Sebastián", "Martínez", "López", "21456789", "María", "López", "16345678"),
    ("Isidora", "Hernández", "Castro", "21567890", "Juan", "Castro", "15456789"),
    ("Diego", "Fernández", "Morales", "21678901", "Patricia", "Morales", "17567890"),
    ("Antonia", "Silva", "Rojas", "21789012", "Carlos", "Rojas", "16678901"),
    ("Joaquín", "Vargas", "Muñoz", "21890123", "Elena", "Muñoz", "18789012"),
    ("Emilia", "Contreras", "Torres", "21901234", "Luis", "Torres", "17890123"),
    ("Tomás", "Sepúlveda", "Flores", "22012345", "Andrea", "Flores", "19901234"),
    ("Sofía", "Moreno", "Herrera", "22123456", "Pedro", "Herrera", "18012345"),
    ("Nicolás", "Jiménez", "Soto", "22234567", "Claudia", "Soto", "20123456"),
    ("Catalina", "Ruiz", "Aguilar", "22345678", "Miguel", "Aguilar", "19234567"),
    ("Francisco", "Espinoza", "Vega", "22456789", "Soledad", "Vega", "21345678"),
    ("Amanda", "Tapia", "Ramos", "22567890", "Sergio", "Ramos", "20456789"),
    ("Benjamín", "Cortés", "Mendoza", "22678901", "Mónica", "Mendoza", "22567890"),
    ("Javiera", "Sandoval", "Guerrero", "22789012", "Andrés", "Guerrero", "21678901"),
    ("Cristóbal", "Cáceres", "Peña", "22890123", "Gloria", "Peña", "23789012"),
    ("Fernanda", "Santander", "Bravo", "22901234", "Raúl", "Bravo", "22890123"),
    ("Ignacio", "Reyes", "Campos", "23012345", "Isabel", "Campos", "24901234"),
    ("Maite", "Parra", "Núñez", "23123456", "Fernando", "Núñez", "23012345"),
    ("Alonso", "Carrasco", "Escobar", "23234567", "Beatriz", "Escobar", "25123456"),
    ("Constanza", "Valenzuela", "Ortega", "23345678", "Gonzalo", "Ortega", "24234567"),
    ("Maximiliano", "Araya", "Paredes", "23456789", "Paulina", "Paredes", "26345678"),
    ("Renata", "Figueroa", "Medina", "23567890", "Rodrigo", "Medina", "25456789"),
    ("Lucas", "Saavedra", "Garrido", "23678901", "Veronica", "Garrido", "27567890"),
]

def calcular_dv(rut):
    """Calcula el dígito verificador de un RUT chileno"""
    suma = 0
    multiplicador = 2
    
    for digito in reversed(str(rut)):
        suma += int(digito) * multiplicador
        multiplicador += 1
        if multiplicador == 8:
            multiplicador = 2
    
    resto = suma % 11
    dv = 11 - resto
    
    if dv == 11:
        return "0"
    elif dv == 10:
        return "K"
    else:
        return str(dv)

def crear_estudiantes():
    """Crear 25 estudiantes para 4° Medio"""
    print("🏫 Creando 25 estudiantes para 4° Medio...")
    
    # Obtener el curso de 4° Medio
    try:
        curso_4medio = Curso.objects.get(nombre="4° Medio")
        print(f"✅ Curso encontrado: {curso_4medio.nombre}")
    except Curso.DoesNotExist:
        print("❌ Error: No se encontró el curso '4° Medio'")
        return
    
    estudiantes_creados = 0
    apoderados_creados = 0
    
    for datos in ESTUDIANTES_DATA:
        nombre_est, apellido_p_est, apellido_m_est, rut_est_sin_dv, nombre_apo, apellido_apo, rut_apo_sin_dv = datos
        
        # Calcular dígitos verificadores
        dv_estudiante = calcular_dv(rut_est_sin_dv)
        dv_apoderado = calcular_dv(rut_apo_sin_dv)
        
        rut_estudiante = f"{rut_est_sin_dv}-{dv_estudiante}"
        rut_apoderado = f"{rut_apo_sin_dv}-{dv_apoderado}"
        
        try:
            # Verificar si ya existe el apoderado
            apoderado, creado_apo = Apoderado.objects.get_or_create(
                rut=rut_apoderado,
                defaults={
                    'nombre': nombre_apo,
                    'apellido_paterno': apellido_apo,
                    'apellido_materno': 'Avilés',  # Apellido común
                    'telefono': f'+569{random.randint(10000000, 99999999)}',
                    'email': f'{nombre_apo.lower()}.{apellido_apo.lower()}@email.com',
                    'direccion': f'Calle {random.choice(["Los Aromos", "Las Heras", "San Martín", "O\'Higgins", "Freire"])} {random.randint(100, 999)}, Talcahuano'
                }
            )
            
            if creado_apo:
                apoderados_creados += 1
                print(f"  👨‍👩‍👧‍👦 Apoderado creado: {apoderado.nombre} {apoderado.apellido_paterno}")
            
            # Crear el estudiante
            estudiante, creado_est = Estudiante.objects.get_or_create(
                rut=rut_estudiante,
                defaults={
                    'nombre': nombre_est,
                    'apellido_paterno': apellido_p_est,
                    'apellido_materno': apellido_m_est,
                    'fecha_nacimiento': date(2007, random.randint(1, 12), random.randint(1, 28)),  # Nacidos en 2007
                    'curso': curso_4medio,
                    'apoderado': apoderado,
                    'vinculo_apoderado': 'hijo',
                    'activo': True
                }
            )
            
            if creado_est:
                estudiantes_creados += 1
                print(f"  🎓 Estudiante creado: {estudiante.nombre} {estudiante.apellido_paterno} (RUT: {rut_estudiante})")
            else:
                print(f"  ⚠️  Estudiante ya existe: {rut_estudiante}")
                
        except Exception as e:
            print(f"  ❌ Error creando estudiante {nombre_est}: {str(e)}")
    
    print(f"\n🎉 Proceso completado:")
    print(f"  📊 Estudiantes creados: {estudiantes_creados}")
    print(f"  👨‍👩‍👧‍👦 Apoderados creados: {apoderados_creados}")
    print(f"  📚 Total estudiantes en 4° Medio: {Estudiante.objects.filter(curso=curso_4medio).count()}")

if __name__ == "__main__":
    crear_estudiantes()
