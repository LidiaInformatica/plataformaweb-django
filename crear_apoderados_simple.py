import os
import sys
import django

# Configurar Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'plataformaweb.settings')
django.setup()

from django.contrib.auth.models import User
from estudiantes.models import Apoderado

print("🔍 CREANDO APODERADOS FALTANTES...")

# Crear apoderados para cada usuario
usuarios_apoderado = ['apoderado1', 'apoderado2', 'apoderado3']

for username in usuarios_apoderado:
    try:
        user = User.objects.get(username=username)
        apoderado, created = Apoderado.objects.get_or_create(
            usuario=user,
            defaults={
                'rut': username,
                'nombre': username.title(),
                'apellido_paterno': 'Apellido',
                'apellido_materno': 'Materno',
                'telefono': '+56 9 0000 0000',
                'email': user.email,
                'direccion': 'Dirección ejemplo'
            }
        )
        if created:
            print(f"✅ Apoderado creado para {username}")
        else:
            print(f"👍 Apoderado ya existe para {username}")
    except User.DoesNotExist:
        print(f"❌ Usuario {username} no existe")

print("✅ Proceso completado!")
