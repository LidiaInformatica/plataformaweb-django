import os, django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'plataformaweb.settings')
django.setup()

from django.contrib.auth.models import User, Group
from core.models import PerfilUsuario

print(" CONFIGURANDO USUARIO APODERADO2")
print("=" * 50)

# Buscar o crear usuario apoderado2
try:
    user = User.objects.get(username='apoderado2')
    print(f" Usuario encontrado: {user.username}")
except User.DoesNotExist:
    print(" Usuario apoderado2 no existe, creándolo...")
    user = User.objects.create_user(
        username='apoderado2',
        email='lidia.inostroza18@gmail.com',
        first_name='Lidia',
        last_name='Inostroza Yañez',
        password='Lidi0354'
    )
    print(f"Usuario creado: {user.username}")

# Configurar contraseña
user.set_password('Lidi0354')
user.is_active = True
user.save()
print(f" Contraseña configurada: Lidi0354")

# Verificar/crear perfil
try:
    perfil = PerfilUsuario.objects.get(usuario=user)
    print(f" Perfil existe: {perfil.get_tipo_perfil_display()}")
except PerfilUsuario.DoesNotExist:
    perfil = PerfilUsuario.objects.create(
        usuario=user,
        tipo_perfil='apoderado',
        rut='apoderado2',
        telefono=''
    )
    print(f" Perfil creado: {perfil.get_tipo_perfil_display()}")

# Configurar grupo
grupo_apoderado, created = Group.objects.get_or_create(name='Apoderado')
user.groups.clear()
user.groups.add(grupo_apoderado)
print(f" Grupo asignado: {grupo_apoderado.name}")

print(f"\n CONFIGURACIÓN COMPLETADA:")
print(f"Username: apoderado2")
print(f"Password: Lidi0354")
print(f"Email: {user.email}")
print(f"Perfil: {perfil.get_tipo_perfil_display()}")
print(f"Activo: {user.is_active}")

# Verificar login
if user.check_password('Lidi0354'):
    print(" Credenciales verificadas - Login debería funcionar")
else:
    print(" Error en credenciales")
