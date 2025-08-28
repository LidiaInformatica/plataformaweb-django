import os, django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'plataformaweb.settings')
django.setup()

from django.contrib.auth.models import User

print("=== VERIFICANDO USUARIOS ===")
usuarios = User.objects.all()
for user in usuarios:
    print(f"Usuario: {user.username:15} | Email: {user.email:30} | Activo: {user.is_active}")

print(f"\nTotal usuarios: {usuarios.count()}")

# Verificar específicamente apoderado2
print("\n=== VERIFICANDO APODERADO2 ===")
try:
    user = User.objects.get(username='apoderado2')
    print(f" Usuario encontrado: {user.username}")
    print(f"Email: {user.email}")
    print(f"Nombre completo: {user.get_full_name()}")
    print(f"Activo: {user.is_active}")
    
    # Probar contraseña
    if user.check_password('Lidi0354'):
        print(" Contraseña Lidi0354 es CORRECTA")
    else:
        print(" Contraseña Lidi0354 es INCORRECTA")
        print(" Configurando contraseña...")
        user.set_password('Lidi0354')
        user.save()
        print(" Contraseña configurada a Lidi0354")
        
except User.DoesNotExist:
    print(" Usuario apoderado2 NO EXISTE")
    print("Usuarios existentes:")
    for u in User.objects.all():
        print(f"  - {u.username}")
