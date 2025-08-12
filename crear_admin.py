#!/usr/bin/env python
"""
Script para crear usuario admin con contraseña admin123
"""
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'plataformaweb.settings')
django.setup()

from django.contrib.auth.models import User

try:
    # Crear o actualizar usuario admin
    user, created = User.objects.get_or_create(
        username='admin',
        defaults={
            'email': 'admin@ejemplo.com',
            'first_name': 'Administrador',
            'last_name': 'Sistema',
            'is_staff': True,
            'is_superuser': True,
        }
    )
    
    # Establecer contraseña
    user.set_password('admin123')
    user.save()
    
    action = "creado" if created else "actualizado"
    print(f"✅ Usuario admin {action} exitosamente")
    print("   Username: admin")
    print("   Password: admin123")
    print("   Email: admin@ejemplo.com")
    
except Exception as e:
    print(f"❌ Error: {e}")
