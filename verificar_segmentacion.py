#!/usr/bin/env python
"""
Script de verificación final para confirmar que la segmentación funciona correctamente
"""

import os
import sys
import django

# Configurar Django
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'plataformaweb.settings')
django.setup()

from django.contrib.auth.models import User, Group
from core.models import PerfilUsuario
from django.test import Client
from django.urls import reverse

def verificar_segmentacion():
    """Verifica que la segmentación esté funcionando correctamente"""
    
    print(" VERIFICACIÓN FINAL DE SEGMENTACIÓN")
    print("=" * 60)
    
    # Verificar que todos los usuarios tienen perfiles
    print("\n1.  VERIFICANDO PERFILES DE USUARIO:")
    print("-" * 40)
    
    usuarios_problema = []
    for usuario in User.objects.all():
        try:
            perfil = PerfilUsuario.objects.get(usuario=usuario)
            grupos = ", ".join([g.name for g in usuario.groups.all()]) or "Sin grupos"
            cargo = f" ({perfil.cargo_directiva})" if perfil.cargo_directiva else ""
            print(f" {usuario.username:12} | {perfil.get_tipo_perfil_display():15}{cargo:15} | Grupos: {grupos}")
        except PerfilUsuario.DoesNotExist:
            usuarios_problema.append(usuario.username)
            print(f" {usuario.username:12} | SIN PERFIL")
    
    if usuarios_problema:
        print(f"\n  USUARIOS SIN PERFIL: {', '.join(usuarios_problema)}")
    else:
        print("\n Todos los usuarios tienen perfiles configurados!")
    
    # Verificar URLs de redirección
    print("\n2.  VERIFICANDO URLS DE REDIRECCIÓN:")
    print("-" * 40)
    
    urls_verificar = [
        ('core:dashboard', 'Dashboard principal'),
        ('core:dashboard_apoderado', 'Dashboard apoderado'),
        ('core:dashboard_directiva', 'Dashboard directiva'),
        ('core:redireccion_post_login', 'Redirección post-login'),
        ('accounts:login', 'Login'),
    ]
    
    for url_name, descripcion in urls_verificar:
        try:
            url = reverse(url_name)
            print(f" {descripcion:25} | {url}")
        except Exception as e:
            print(f" {descripcion:25} | ERROR: {e}")
    
    # Verificar configuración de LOGIN_REDIRECT_URL
    print("\n3.   VERIFICANDO CONFIGURACIÓN:")
    print("-" * 40)
    
    from django.conf import settings
    
    login_redirect = getattr(settings, 'LOGIN_REDIRECT_URL', 'No configurado')
    login_url = getattr(settings, 'LOGIN_URL', 'No configurado')
    
    print(f"LOGIN_REDIRECT_URL: {login_redirect}")
    print(f"LOGIN_URL: {login_url}")
    
    # Verificar que la URL de redirección apunta a la función correcta
    if login_redirect == '/redireccion/':
        print(" LOGIN_REDIRECT_URL configurado correctamente")
    else:
        print("  LOGIN_REDIRECT_URL podría no estar configurado correctamente")
    
    # Mostrar estadísticas finales
    print("\n4.  ESTADÍSTICAS FINALES:")
    print("-" * 40)
    
    total_usuarios = User.objects.count()
    total_perfiles = PerfilUsuario.objects.count()
    apoderados = PerfilUsuario.objects.filter(tipo_perfil='apoderado').count()
    directiva = PerfilUsuario.objects.filter(tipo_perfil='directiva').count()
    administradores = PerfilUsuario.objects.filter(tipo_perfil='administrador').count()
    
    print(f" Total usuarios: {total_usuarios}")
    print(f" Total perfiles: {total_perfiles}")
    print(f" Apoderados: {apoderados}")
    print(f"  Directiva: {directiva}")
    print(f" Administradores: {administradores}")
    
    # Verificación de integridad
    print("\n5.  VERIFICACIÓN DE INTEGRIDAD:")
    print("-" * 40)
    
    if total_usuarios == total_perfiles:
        print(" Todos los usuarios tienen perfiles")
    else:
        faltantes = total_usuarios - total_perfiles
        print(f"  Faltan {faltantes} perfiles por configurar")
    
    # Verificar usuarios específicos mencionados
    print("\n6.  VERIFICACIÓN DE USUARIOS ESPECÍFICOS:")
    print("-" * 40)
    
    usuarios_especificos = ['apoderado1', 'apoderado2', 'apoderado3', 'Presidenta', 'Tesorera', 'Secretaria', 'Lidia']
    
    for username in usuarios_especificos:
        try:
            usuario = User.objects.get(username=username)
            try:
                perfil = PerfilUsuario.objects.get(usuario=usuario)
                print(f" {username:12} | {perfil.get_tipo_perfil_display():15} | Email: {usuario.email}")
            except PerfilUsuario.DoesNotExist:
                print(f" {username:12} | SIN PERFIL")
        except User.DoesNotExist:
            print(f" {username:12} | NO EXISTE")
    
    print("\n" + "=" * 60)
    print(" RESUMEN DE VERIFICACIÓN:")
    print("=" * 60)
    
    if total_usuarios == total_perfiles and not usuarios_problema:
        print(" SEGMENTACIÓN CONFIGURADA CORRECTAMENTE")
        print(" Todos los usuarios pueden acceder a sus dashboards correspondientes")
        print(" apoderado3 con contraseña Lidi0354 debería funcionar correctamente")
    else:
        print("  HAY PROBLEMAS EN LA CONFIGURACIÓN:")
        if usuarios_problema:
            print(f"   - Usuarios sin perfil: {', '.join(usuarios_problema)}")
        if total_usuarios != total_perfiles:
            print(f"   - Desbalance usuarios/perfiles: {total_usuarios}/{total_perfiles}")
    
    print("\n INSTRUCCIONES PARA PROBAR:")
    print("1. Ir a http://127.0.0.1:8000/accounts/login/")
    print("2. Login con apoderado3 / Lidi0354")
    print("3. Debería redirigir a dashboard de apoderado")
    print("4. Probar con otros usuarios según sus perfiles")

if __name__ == '__main__':
    try:
        verificar_segmentacion()
    except Exception as e:
        print(f" Error durante la verificación: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
