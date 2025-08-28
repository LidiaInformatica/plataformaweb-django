#!/usr/bin/env python
"""
Script para verificar datos REALES existentes en la base de datos
"""

import os
import sys
import django

# Configurar Django
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'plataformaweb.settings')
django.setup()

from estudiantes.models import Apoderado, Estudiante
from django.contrib.auth.models import User

def verificar_datos_reales():
    print(" VERIFICANDO DATOS REALES EN LA BASE DE DATOS")
    print("=" * 60)
    
    print("\n USUARIOS EXISTENTES:")
    print("-" * 40)
    usuarios = User.objects.all()
    for user in usuarios:
        print(f" {user.username:12} | {user.get_full_name():25} | {user.email}")
    
    print(f"\nTotal usuarios: {usuarios.count()}")
    
    print("\n APODERADOS EXISTENTES:")
    print("-" * 40)
    apoderados = Apoderado.objects.all()
    for apoderado in apoderados:
        usuario_vinculado = apoderado.usuario.username if apoderado.usuario else "Sin usuario"
        print(f" RUT: {apoderado.rut:12} | {apoderado.nombre_completo():25} | Usuario: {usuario_vinculado}")
    
    print(f"\nTotal apoderados: {apoderados.count()}")
    
    print("\n ESTUDIANTES EXISTENTES:")
    print("-" * 40)
    estudiantes = Estudiante.objects.all()
    for estudiante in estudiantes:
        apoderado_nombre = estudiante.apoderado.nombre_completo() if estudiante.apoderado else "Sin apoderado"
        print(f" RUT: {estudiante.rut:12} | {estudiante.nombre} {estudiante.apellido_paterno:15} | Apoderado: {apoderado_nombre}")
    
    print(f"\nTotal estudiantes: {estudiantes.count()}")
    
    print("\n RELACIONES USUARIO-APODERADO:")
    print("-" * 40)
    for user in usuarios:
        try:
            apoderado = Apoderado.objects.get(usuario=user)
            print(f" {user.username:12} -> Apoderado: {apoderado.nombre_completo()}")
        except Apoderado.DoesNotExist:
            print(f" {user.username:12} -> SIN APODERADO VINCULADO")
    
    # Buscar apoderados sin usuario vinculado
    print("\n APODERADOS SIN USUARIO:")
    print("-" * 40)
    apoderados_sin_usuario = Apoderado.objects.filter(usuario__isnull=True)
    for apoderado in apoderados_sin_usuario:
        print(f"  {apoderado.rut:12} | {apoderado.nombre_completo()} | SIN USUARIO")
    
    if apoderados_sin_usuario.count() == 0:
        print(" Todos los apoderados tienen usuario vinculado")

if __name__ == '__main__':
    try:
        verificar_datos_reales()
    except Exception as e:
        print(f" Error: {e}")
        import traceback
        traceback.print_exc()
