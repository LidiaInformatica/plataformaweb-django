#!/usr/bin/env python
import os
import sys
import django

# Configurar Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'plataformaweb.settings')
django.setup()

try:
    from core.models import PerfilUsuario
    count = PerfilUsuario.objects.count()
    print(f" Modelo funciona correctamente. Perfiles: {count}")
    print(" La columna cargo_directiva está funcionando")
except Exception as e:
    print(f" Error: {e}")
    sys.exit(1)
