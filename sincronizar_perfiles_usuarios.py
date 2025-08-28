#!/usr/bin/env python
"""
Script para sincronizar usuarios existentes con perfiles PerfilUsuario
Corrige la segmentación de perfiles para usuarios creados en admin de Django
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

def sincronizar_perfiles():
    """Sincroniza todos los usuarios existentes con sus perfiles"""
    
    print("🔄 Iniciando sincronización de perfiles de usuario...")
    print("=" * 60)
    
    # Mapeo de grupos a tipos de perfil
    mapeo_grupos = {
        'Apoderado': 'apoderado',
        'Presidenta': 'directiva',
        'Tesorera': 'directiva', 
        'Secretaria': 'directiva'
    }
    
    # Mapeo de grupos a cargos de directiva
    mapeo_cargos = {
        'Presidenta': 'presidenta',
        'Tesorera': 'tesorera',
        'Secretaria': 'secretaria'
    }
    
    usuarios_procesados = 0
    perfiles_creados = 0
    perfiles_actualizados = 0
    
    # Procesar todos los usuarios
    for usuario in User.objects.all():
        usuarios_procesados += 1
        
        print(f"\n👤 Procesando usuario: {usuario.username} ({usuario.get_full_name()})")
        
        # Verificar si ya tiene perfil
        perfil_existe = PerfilUsuario.objects.filter(usuario=usuario).first()
        
        # Determinar tipo de perfil basado en grupos
        tipo_perfil = None
        cargo_directiva = None
        
        # Verificar si es superusuario
        if usuario.is_superuser:
            tipo_perfil = 'administrador'
            print(f"   🔑 Es superusuario -> Tipo: administrador")
        else:
            # Verificar grupos del usuario
            grupos_usuario = usuario.groups.all()
            print(f"   📋 Grupos: {[g.name for g in grupos_usuario]}")
            
            for grupo in grupos_usuario:
                if grupo.name in mapeo_grupos:
                    tipo_perfil = mapeo_grupos[grupo.name]
                    if grupo.name in mapeo_cargos:
                        cargo_directiva = mapeo_cargos[grupo.name]
                    break
        
        # Si no se encontró tipo de perfil, asignar por defecto según email
        if not tipo_perfil:
            if 'apoderado' in usuario.username.lower():
                tipo_perfil = 'apoderado'
                print(f"   🔍 Detectado por username -> Tipo: apoderado")
            elif any(cargo in usuario.username.lower() for cargo in ['presidenta', 'tesorera', 'secretaria']):
                tipo_perfil = 'directiva'
                print(f"   🔍 Detectado por username -> Tipo: directiva")
            else:
                tipo_perfil = 'apoderado'  # Por defecto
                print(f"   ⚠️  Asignado por defecto -> Tipo: apoderado")
        
        # Crear o actualizar perfil
        if perfil_existe:
            # Actualizar perfil existente
            perfil_existe.tipo_perfil = tipo_perfil
            if cargo_directiva:
                perfil_existe.cargo_directiva = cargo_directiva
            perfil_existe.save()
            perfiles_actualizados += 1
            print(f"   ✅ Perfil actualizado: {tipo_perfil}" + (f" ({cargo_directiva})" if cargo_directiva else ""))
        else:
            # Crear nuevo perfil
            perfil = PerfilUsuario.objects.create(
                usuario=usuario,
                tipo_perfil=tipo_perfil,
                cargo_directiva=cargo_directiva,
                rut=usuario.username,  # El username es el RUT
                telefono=""  # Se puede completar después
            )
            perfiles_creados += 1
            print(f"   ✅ Perfil creado: {tipo_perfil}" + (f" ({cargo_directiva})" if cargo_directiva else ""))
    
    print("\n" + "=" * 60)
    print("📊 RESUMEN DE SINCRONIZACIÓN:")
    print(f"👥 Usuarios procesados: {usuarios_procesados}")
    print(f"➕ Perfiles creados: {perfiles_creados}")
    print(f"🔄 Perfiles actualizados: {perfiles_actualizados}")
    print("✅ Sincronización completada exitosamente!")

def verificar_grupos():
    """Verifica que los grupos necesarios existan"""
    print("\n🔍 Verificando grupos necesarios...")
    
    grupos_requeridos = ['Apoderado', 'Presidenta', 'Tesorera', 'Secretaria']
    
    for grupo_nombre in grupos_requeridos:
        grupo, creado = Group.objects.get_or_create(name=grupo_nombre)
        if creado:
            print(f"   ➕ Grupo creado: {grupo_nombre}")
        else:
            print(f"   ✅ Grupo existe: {grupo_nombre}")

def mostrar_estado_final():
    """Muestra el estado final de todos los perfiles"""
    print("\n" + "=" * 60)
    print("📋 ESTADO FINAL DE PERFILES:")
    print("=" * 60)
    
    for perfil in PerfilUsuario.objects.all().order_by('tipo_perfil', 'usuario__username'):
        cargo = f" ({perfil.cargo_directiva})" if perfil.cargo_directiva else ""
        grupos = ", ".join([g.name for g in perfil.usuario.groups.all()])
        print(f"👤 {perfil.usuario.username:12} | {perfil.usuario.get_full_name():25} | {perfil.get_tipo_perfil_display():15}{cargo:15} | Grupos: {grupos}")

if __name__ == '__main__':
    try:
        verificar_grupos()
        sincronizar_perfiles()
        mostrar_estado_final()
    except Exception as e:
        print(f"❌ Error durante la sincronización: {e}")
        sys.exit(1)
