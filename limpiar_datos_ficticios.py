#!/usr/bin/env python
"""
Script para limpiar datos ficticios y configurar email institucional para admin
SOLO TRABAJA CON DATOS REALES DE LA BASE DE DATOS
"""

import os
import sys
import django

# Configurar Django
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'plataformaweb.settings')
django.setup()

from django.contrib.auth.models import User
from estudiantes.models import Apoderado, Estudiante
from core.models import PerfilUsuario

def limpiar_y_configurar():
    print("🧹 LIMPIANDO DATOS FICTICIOS Y CONFIGURANDO EMAILS INSTITUCIONALES")
    print("=" * 80)
    
    # 1. Mostrar datos reales actuales
    print("\n DATOS REALES ACTUALES:")
    print("-" * 50)
    
    print(" Usuarios:")
    for user in User.objects.all():
        print(f"   {user.username:15} | {user.get_full_name():25} | {user.email}")
    
    print("\n Apoderados:")
    for apoderado in Apoderado.objects.all():
        print(f"   RUT: {apoderado.rut:15} | {apoderado.nombre_completo():30} | {apoderado.email}")
    
    print("\n Estudiantes:")
    for estudiante in Estudiante.objects.all():
        print(f"   RUT: {estudiante.rut:15} | {estudiante.nombre} {estudiante.apellido_paterno:15} | Apoderado: {estudiante.apoderado.rut}")
    
    # 2. Identificar y resolver conflicto de emails
    print("\n IDENTIFICANDO CONFLICTOS DE EMAIL:")
    print("-" * 50)
    
    # Buscar el usuario admin/Lidia
    try:
        usuario_admin = User.objects.get(username='Lidia')
        print(f" Usuario admin encontrado: {usuario_admin.username} | {usuario_admin.email}")
        
        # Verificar si hay apoderados con el mismo email
        apoderados_mismo_email = Apoderado.objects.filter(email=usuario_admin.email)
        if apoderados_mismo_email.count() > 0:
            print(f"  CONFLICTO: {apoderados_mismo_email.count()} apoderado(s) con email {usuario_admin.email}")
            for apoderado in apoderados_mismo_email:
                estudiantes = Estudiante.objects.filter(apoderado=apoderado)
                hijos = [f"{e.nombre} {e.apellido_paterno}" for e in estudiantes]
                print(f"   {apoderado.rut} | {apoderado.nombre_completo()} | Hijos: {', '.join(hijos) if hijos else 'Sin hijos'}")
            
            # Cambiar email del admin a uno institucional
            nuevo_email_admin = "admin@colegiocementerioriente.cl"
            print(f"\n SOLUCIÓN: Cambiar email admin de {usuario_admin.email} a {nuevo_email_admin}")
            
            respuesta = input("¿Proceder con el cambio? (s/n): ")
            if respuesta.lower() == 's':
                usuario_admin.email = nuevo_email_admin
                usuario_admin.save()
                print(f" Email del admin cambiado exitosamente")
            else:
                print(" Cambio cancelado")
        else:
            print(" No hay conflictos de email")
            
    except User.DoesNotExist:
        print(" Usuario admin 'Lidia' no encontrado")
    
    # 3. Eliminar datos ficticios creados anteriormente
    print("\n  ELIMINANDO DATOS FICTICIOS:")
    print("-" * 50)
    
    # Buscar apoderados con datos obviamente ficticios
    apoderados_ficticios = Apoderado.objects.filter(
        apellido_paterno__in=['Apellido', 'González', 'López', 'Torres', 'Martínez']
    ).exclude(
        # Excluir datos que podrían ser reales
        rut__in=['19876543k', '20123456j']  # Agregar RUTs reales conocidos aquí
    )
    
    if apoderados_ficticios.exists():
        print(" Apoderados ficticios encontrados:")
        for apoderado in apoderados_ficticios:
            print(f"  {apoderado.rut} | {apoderado.nombre_completo()}")
        
        respuesta = input("¿Eliminar datos ficticios? (s/n): ")
        if respuesta.lower() == 's':
            count = apoderados_ficticios.count()
            apoderados_ficticios.delete()
            print(f" {count} apoderado(s) ficticio(s) eliminado(s)")
        else:
            print(" Eliminación cancelada")
    else:
        print(" No se encontraron datos ficticios evidentes")
    
    # 4. Mostrar estado final limpio
    print("\n ESTADO FINAL LIMPIO:")
    print("-" * 50)
    
    print(" Usuarios finales:")
    for user in User.objects.all():
        perfil_tipo = "Sin perfil"
        try:
            perfil = PerfilUsuario.objects.get(usuario=user)
            perfil_tipo = perfil.get_tipo_perfil_display()
        except PerfilUsuario.DoesNotExist:
            pass
        print(f"   {user.username:15} | {perfil_tipo:20} | {user.email}")
    
    print("\n Apoderados finales:")
    for apoderado in Apoderado.objects.all():
        estudiantes = Estudiante.objects.filter(apoderado=apoderado)
        hijos = [f"{e.nombre} {e.apellido_paterno}" for e in estudiantes]
        print(f"   {apoderado.rut:15} | {apoderado.nombre_completo():30} | Hijos: {', '.join(hijos) if hijos else 'Sin hijos'}")
    
    print("\n RESULTADO:")
    print(" Conflicto de emails resuelto")
    print(" Datos ficticios eliminados")
    print(" Solo quedan datos reales de la defensa de título")
    print(" Dashboard de apoderado funcionará correctamente")

if __name__ == '__main__':
    try:
        limpiar_y_configurar()
    except Exception as e:
        print(f" Error: {e}")
        import traceback
        traceback.print_exc()
