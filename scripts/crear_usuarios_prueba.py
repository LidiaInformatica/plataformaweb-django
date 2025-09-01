#!/usr/bin/env python
"""
Script para crear usuarios de prueba en el sistema
"""
import os
import sys
import django

# Configurar Django
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'plataformaweb.settings')
django.setup()

from django.contrib.auth.models import User
from core.models import PerfilUsuario

def crear_usuarios_prueba():
    """Crear usuarios de prueba para el sistema"""
    
    usuarios_prueba = [
        {
            'username': '12345678k',
            'first_name': 'Juan Carlos',
            'last_name': 'Pérez González',
            'email': 'juan.perez@email.com',
            'password': 'password123',
            'tipo_perfil': 'apoderado',
            'telefono': '+56 9 8765 4321'
        },
        {
            'username': '98765432j',
            'first_name': 'María Elena',
            'last_name': 'Rodríguez Silva',
            'email': 'maria.rodriguez@email.com',
            'password': 'password123',
            'tipo_perfil': 'directiva',
            'telefono': '+56 9 7654 3210'
        },
        {
            'username': '11223344k',
            'first_name': 'Carlos Alberto',
            'last_name': 'González López',
            'email': 'carlos.gonzalez@email.com',
            'password': 'password123',
            'tipo_perfil': 'apoderado',
            'telefono': '+56 9 6543 2109'
        },
        {
            'username': '55667788j',
            'first_name': 'Ana Patricia',
            'last_name': 'Martínez Torres',
            'email': 'ana.martinez@email.com',
            'password': 'password123',
            'tipo_perfil': 'directiva',
            'telefono': '+56 9 5432 1098'
        }
    ]
    
    print("Creando usuarios de prueba...")
    
    for datos_usuario in usuarios_prueba:
        # Verificar si el usuario ya existe
        if User.objects.filter(username=datos_usuario['username']).exists():
            print(f"Usuario {datos_usuario['username']} ya existe")
            continue
        
        try:
            # Crear usuario
            usuario = User.objects.create_user(
                username=datos_usuario['username'],
                first_name=datos_usuario['first_name'],
                last_name=datos_usuario['last_name'],
                email=datos_usuario['email'],
                password=datos_usuario['password']
            )
            
            # Crear perfil
            perfil = PerfilUsuario.objects.create(
                usuario=usuario,
                tipo_perfil=datos_usuario['tipo_perfil'],
                rut=datos_usuario['username'],
                telefono=datos_usuario['telefono']
            )
            
            print(f"Usuario creado: {usuario.get_full_name()} ({perfil.get_tipo_perfil_display()})")
            
        except Exception as e:
            print(f"Error creando usuario {datos_usuario['username']}: {e}")
    
    print("\nUsuarios de prueba creados:")
    print("=" * 50)
    print("RUT: 12345678k | Contraseña: password123 | Tipo: Apoderado")
    print("RUT: 98765432j | Contraseña: password123 | Tipo: Directiva")
    print("RUT: 11223344k | Contraseña: password123 | Tipo: Apoderado")
    print("RUT: 55667788j | Contraseña: password123 | Tipo: Directiva")
    print("=" * 50)

if __name__ == '__main__':
    crear_usuarios_prueba()
