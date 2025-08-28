#!/usr/bin/env python
import os
import django
from django.conf import settings

# Configurar Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'plataformaweb.settings')
django.setup()

from django.contrib.auth.models import User

# Establecer contraseña para admin
try:
    user = User.objects.get(username='admin')
    user.set_password('admin123')
    user.save()
    print("Contraseña establecida para 'admin': admin123")
except User.DoesNotExist:
    print(" Usuario admin no encontrado")

# Crear usuarios de prueba rápidos
users_data = [
    {'username': 'test1', 'password': '123456', 'email': 'test1@talcahuanocentro.cl'},
    {'username': 'test2', 'password': '123456', 'email': 'test2@talcahuanocentro.cl'},
    {'username': 'directivo', 'password': '123456', 'email': 'directivo@talcahuanocentro.cl'},
]

for user_data in users_data:
    user, created = User.objects.get_or_create(
        username=user_data['username'],
        defaults={
            'email': user_data['email'],
            'first_name': f"Usuario {user_data['username']}",
        }
    )
    if created:
        user.set_password(user_data['password'])
        user.save()
        print(f" Usuario creado: {user_data['username']} / {user_data['password']}")
    else:
        print(f"  Usuario ya existe: {user_data['username']}")

print("\n CREDENCIALES LISTAS:")
print("Admin: admin / admin123")
print("Test1: test1 / 123456")
print("Test2: test2 / 123456")
print("Directivo: directivo / 123456")
