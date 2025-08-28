#!/usr/bin/env python
"""
Script para configurar específicamente los usuarios de admin que aparecen en la imagen
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

def configurar_usuarios_admin():
    """Configura específicamente los usuarios visibles en el admin"""
    
    print("🔧 Configurando usuarios del admin de Django...")
    print("=" * 60)
    
    # Configuración específica de usuarios
    configuraciones = [
        {
            'username': 'Lidia',
            'tipo_perfil': 'administrador',
            'grupos': [],
            'is_superuser': True
        },
        {
            'username': 'Presidenta',
            'tipo_perfil': 'directiva',
            'cargo_directiva': 'presidenta',
            'grupos': ['Presidenta']
        },
        {
            'username': 'Secretaria',
            'tipo_perfil': 'directiva',
            'cargo_directiva': 'secretaria',
            'grupos': ['Secretaria']
        },
        {
            'username': 'Tesorera',
            'tipo_perfil': 'directiva',
            'cargo_directiva': 'tesorera',
            'grupos': ['Tesorera']
        },
        {
            'username': 'apoderado1',
            'tipo_perfil': 'apoderado',
            'grupos': ['Apoderado']
        },
        {
            'username': 'apoderado2',
            'tipo_perfil': 'apoderado',
            'grupos': ['Apoderado']
        },
        {
            'username': 'apoderado3',
            'tipo_perfil': 'apoderado',
            'grupos': ['Apoderado']
        }
    ]
    
    # Crear grupos si no existen
    grupos_requeridos = ['Apoderado', 'Presidenta', 'Secretaria', 'Tesorera']
    for grupo_nombre in grupos_requeridos:
        grupo, creado = Group.objects.get_or_create(name=grupo_nombre)
        if creado:
            print(f"✅ Grupo creado: {grupo_nombre}")
        else:
            print(f"👍 Grupo ya existe: {grupo_nombre}")
    
    print("\n" + "=" * 60)
    
    # Configurar cada usuario
    for config in configuraciones:
        username = config['username']
        
        try:
            usuario = User.objects.get(username=username)
            print(f"\n👤 Configurando usuario: {username}")
            
            # Configurar superusuario si es necesario
            if config.get('is_superuser'):
                usuario.is_superuser = True
                usuario.is_staff = True
                usuario.save()
                print(f"   🔑 Configurado como superusuario")
            
            # Crear o actualizar perfil
            perfil, creado = PerfilUsuario.objects.get_or_create(
                usuario=usuario,
                defaults={
                    'tipo_perfil': config['tipo_perfil'],
                    'cargo_directiva': config.get('cargo_directiva'),
                    'rut': username,
                    'telefono': ''
                }
            )
            
            if not creado:
                # Actualizar perfil existente
                perfil.tipo_perfil = config['tipo_perfil']
                if 'cargo_directiva' in config:
                    perfil.cargo_directiva = config['cargo_directiva']
                perfil.save()
                print(f"   🔄 Perfil actualizado: {config['tipo_perfil']}")
            else:
                print(f"   ✅ Perfil creado: {config['tipo_perfil']}")
            
            # Configurar grupos
            usuario.groups.clear()  # Limpiar grupos existentes
            for grupo_nombre in config.get('grupos', []):
                grupo = Group.objects.get(name=grupo_nombre)
                usuario.groups.add(grupo)
                print(f"   📋 Agregado al grupo: {grupo_nombre}")
            
            print(f"   ✅ Usuario {username} configurado correctamente")
            
        except User.DoesNotExist:
            print(f"   ❌ Usuario {username} no encontrado en la base de datos")
    
    print("\n" + "=" * 60)
    print("📊 CONFIGURACIÓN COMPLETADA")
    print("=" * 60)
    
    # Mostrar estado final
    print("\n📋 ESTADO FINAL DE USUARIOS:")
    for config in configuraciones:
        try:
            usuario = User.objects.get(username=config['username'])
            try:
                perfil = PerfilUsuario.objects.get(usuario=usuario)
                tipo_display = perfil.get_tipo_perfil_display()
                cargo = f" ({perfil.cargo_directiva})" if perfil.cargo_directiva else ""
            except PerfilUsuario.DoesNotExist:
                tipo_display = "SIN PERFIL"
                cargo = ""
            
            grupos = ", ".join([g.name for g in usuario.groups.all()])
            print(f"👤 {config['username']:12} | {tipo_display:15}{cargo:15} | Grupos: {grupos}")
        except User.DoesNotExist:
            print(f"❌ {config['username']:12} | NO EXISTE")

if __name__ == '__main__':
    try:
        configurar_usuarios_admin()
        print("\n🎉 Configuración completada exitosamente!")
        print("📝 Todos los usuarios deberían poder acceder a sus dashboards correspondientes.")
    except Exception as e:
        print(f"❌ Error durante la configuración: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
