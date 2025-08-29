#!/usr/bin/env python
"""
Script para vincular usuarios con apoderados REALES existentes en la base de datos
NO CREA DATOS FICTICIOS - Solo vincula datos existentes
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

def vincular_usuarios_con_apoderados_reales():
    print(" VINCULANDO USUARIOS CON APODERADOS REALES EXISTENTES")
    print("=" * 70)
    
    # Primero mostrar qué datos reales tenemos
    print("\n DATOS REALES EXISTENTES:")
    print("-" * 40)
    
    print(" Usuarios:")
    usuarios = User.objects.all()
    for user in usuarios:
        print(f"   {user.username} | {user.get_full_name()} | {user.email}")
    
    print("\nApoderados:")
    apoderados = Apoderado.objects.all()
    for apoderado in apoderados:
        usuario_str = f"Usuario: {apoderado.usuario.username}" if apoderado.usuario else "SIN USUARIO"
        print(f"   👨‍👩‍👧‍👦 RUT: {apoderado.rut} | {apoderado.nombre_completo()} | {usuario_str}")
    
    print("\n Estudiantes:")
    estudiantes = Estudiante.objects.all()
    for estudiante in estudiantes:
        print(f"    RUT: {estudiante.rut} | {estudiante.nombre} {estudiante.apellido_paterno} | Apoderado: {estudiante.apoderado.rut}")
    
    # Estrategia de vinculación
    print("\n ESTRATEGIA DE VINCULACIÓN:")
    print("-" * 40)
    
    usuarios_apoderado = ['apoderado1', 'apoderado2', 'apoderado3']
    vinculaciones_realizadas = 0
    
    for username in usuarios_apoderado:
        try:
            usuario = User.objects.get(username=username)
            print(f"\n Procesando usuario: {username}")
            
            # Verificar si ya tiene apoderado vinculado
            try:
                apoderado_existente = Apoderado.objects.get(usuario=usuario)
                print(f"    Ya tiene apoderado vinculado: {apoderado_existente.nombre_completo()}")
                continue
            except Apoderado.DoesNotExist:
                pass
            
            # Buscar apoderado sin usuario vinculado
            apoderados_sin_usuario = Apoderado.objects.filter(usuario__isnull=True)
            
            if apoderados_sin_usuario.exists():
                # Vincular el primer apoderado disponible
                apoderado_disponible = apoderados_sin_usuario.first()
                apoderado_disponible.usuario = usuario
                apoderado_disponible.save()
                
                print(f"    VINCULADO con apoderado: {apoderado_disponible.nombre_completo()} (RUT: {apoderado_disponible.rut})")
                vinculaciones_realizadas += 1
            else:
                # Si no hay apoderados sin usuario, buscar por email
                try:
                    apoderado_por_email = Apoderado.objects.get(email=usuario.email)
                    if not apoderado_por_email.usuario:
                        apoderado_por_email.usuario = usuario
                        apoderado_por_email.save()
                        print(f"    VINCULADO por email con: {apoderado_por_email.nombre_completo()}")
                        vinculaciones_realizadas += 1
                    else:
                        print(f"     Apoderado con email {usuario.email} ya tiene usuario vinculado")
                except Apoderado.DoesNotExist:
                    print(f"     No se encontró apoderado disponible para vincular")
                    print(f"    Solución: El usuario {username} funcionará con dashboard básico")
        
        except User.DoesNotExist:
            print(f"    Usuario {username} no existe")
    
    print(f"\n RESUMEN:")
    print(f" Vinculaciones realizadas: {vinculaciones_realizadas}")
    
    # Mostrar estado final
    print("\n ESTADO FINAL DE VINCULACIONES:")
    print("-" * 40)
    
    for user in usuarios:
        try:
            apoderado = Apoderado.objects.get(usuario=user)
            print(f" {user.username:12} -> {apoderado.nombre_completo()} (RUT: {apoderado.rut})")
        except Apoderado.DoesNotExist:
            print(f"  {user.username:12} -> SIN APODERADO (usará dashboard básico)")
    
    print("\n RESULTADO:")
    print(" El sistema ahora puede manejar usuarios con y sin apoderados reales")
    print(" Los usuarios sin apoderado verán un dashboard básico")
    print(" Los usuarios con apoderado verán sus datos completos")

if __name__ == '__main__':
    try:
        vincular_usuarios_con_apoderados_reales()
    except Exception as e:
        print(f" Error: {e}")
        import traceback
        traceback.print_exc()
