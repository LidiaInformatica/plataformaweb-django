#!/usr/bin/env python
"""
Script para crear registros Apoderado para usuarios apoderado1, apoderado2, apoderado3
"""

import os
import sys
import django

# Configurar Django
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'plataformaweb.settings')
django.setup()

from django.contrib.auth.models import User
from estudiantes.models import Apoderado

def crear_apoderados():
    """Crea registros Apoderado para usuarios apoderado1, apoderado2, apoderado3"""
    
    print("🏗️  CREANDO REGISTROS APODERADO")
    print("=" * 60)
    
    usuarios_apoderado = [
        {
            'username': 'apoderado1',
            'rut': 'apoderado1',
            'nombre': 'Alejandro',
            'apellido_paterno': 'Palacios',
            'apellido_materno': 'González',
            'telefono': '+56 9 1111 1111',
            'direccion': 'Calle Ejemplo 123, Santiago'
        },
        {
            'username': 'apoderado2',
            'rut': 'apoderado2',
            'nombre': 'Lidia',
            'apellido_paterno': 'Inostroza',
            'apellido_materno': 'Yañez',
            'telefono': '+56 9 2222 2222',
            'direccion': 'Avenida Principal 456, Santiago'
        },
        {
            'username': 'apoderado3',
            'rut': 'apoderado3',
            'nombre': 'María',
            'apellido_paterno': 'Teresa',
            'apellido_materno': 'Yañez',
            'telefono': '+56 9 3333 3333',
            'direccion': 'Pasaje Los Aromos 789, Santiago'
        }
    ]
    
    creados = 0
    actualizados = 0
    errores = 0
    
    for datos in usuarios_apoderado:
        try:
            # Buscar el usuario
            usuario = User.objects.get(username=datos['username'])
            print(f"\n👤 Procesando usuario: {datos['username']}")
            
            # Verificar si ya tiene apoderado
            apoderado, creado = Apoderado.objects.get_or_create(
                usuario=usuario,
                defaults={
                    'rut': datos['rut'],
                    'nombre': datos['nombre'],
                    'apellido_paterno': datos['apellido_paterno'],
                    'apellido_materno': datos['apellido_materno'],
                    'telefono': datos['telefono'],
                    'email': usuario.email,
                    'direccion': datos['direccion']
                }
            )
            
            if creado:
                print(f"   ✅ Apoderado creado: {apoderado.nombre_completo()}")
                creados += 1
            else:
                # Actualizar datos si ya existe
                apoderado.nombre = datos['nombre']
                apoderado.apellido_paterno = datos['apellido_paterno']
                apoderado.apellido_materno = datos['apellido_materno']
                apoderado.telefono = datos['telefono']
                apoderado.email = usuario.email
                apoderado.direccion = datos['direccion']
                apoderado.save()
                print(f"   🔄 Apoderado actualizado: {apoderado.nombre_completo()}")
                actualizados += 1
                
        except User.DoesNotExist:
            print(f"   ❌ Usuario {datos['username']} no encontrado")
            errores += 1
        except Exception as e:
            print(f"   ❌ Error procesando {datos['username']}: {e}")
            errores += 1
    
    print("\n" + "=" * 60)
    print("📊 RESUMEN:")
    print(f"✅ Apoderados creados: {creados}")
    print(f"🔄 Apoderados actualizados: {actualizados}")
    print(f"❌ Errores: {errores}")
    
    # Mostrar estado final
    print("\n📋 ESTADO FINAL DE APODERADOS:")
    print("-" * 40)
    
    for datos in usuarios_apoderado:
        try:
            usuario = User.objects.get(username=datos['username'])
            try:
                apoderado = Apoderado.objects.get(usuario=usuario)
                print(f"✅ {usuario.username:12} | {apoderado.nombre_completo():25} | {apoderado.email}")
            except Apoderado.DoesNotExist:
                print(f"❌ {usuario.username:12} | SIN APODERADO")
        except User.DoesNotExist:
            print(f"❌ {datos['username']:12} | USUARIO NO EXISTE")

if __name__ == '__main__':
    try:
        crear_apoderados()
        print("\n🎉 Proceso completado!")
        print("📝 Los usuarios apoderado1, apoderado2, apoderado3 ahora tienen registros Apoderado.")
        print("📝 Esto debería resolver el error 'Apoderado matching query does not exist'.")
    except Exception as e:
        print(f"❌ Error durante el proceso: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
