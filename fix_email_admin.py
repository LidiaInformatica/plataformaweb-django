import os, django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'plataformaweb.settings')
django.setup()

from django.contrib.auth.models import User

# Cambiar email del usuario admin
try:
    user = User.objects.get(username='Lidia')
    print(f"Usuario admin encontrado: {user.username}")
    print(f"Email actual: {user.email}")
    
    # Cambiar a email institucional
    user.email = "admin@colegiocementerioriente.cl"
    user.save()
    
    print(f"Email cambiado a: {user.email}")
    print("✅ Conflicto de email resuelto")
    
except User.DoesNotExist:
    print("❌ Usuario 'Lidia' no encontrado")

print("\n🎯 Ahora el login de apoderado2 debería funcionar sin conflictos")
