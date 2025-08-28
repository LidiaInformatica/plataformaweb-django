import os, django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'plataformaweb.settings')
django.setup()

from django.contrib.auth.models import User
from estudiantes.models import Apoderado, Estudiante
from core.models import PerfilUsuario

print("=== DATOS REALES EN LA BASE DE DATOS ===")

print("\n👥 USUARIOS:")
for user in User.objects.all():
    print(f"{user.username} | {user.get_full_name()} | {user.email}")

print("\n👤 APODERADOS:")
for apoderado in Apoderado.objects.all():
    print(f"RUT: {apoderado.rut} | {apoderado.nombre_completo()} | Email: {apoderado.email}")

print("\n👶 ESTUDIANTES:")
for estudiante in Estudiante.objects.all():
    print(f"RUT: {estudiante.rut} | {estudiante.nombre} {estudiante.apellido_paterno} | Apoderado RUT: {estudiante.apoderado.rut}")

print("\n🔍 CONFLICTO DE EMAILS:")
email_problema = "lidia.inostroza18@gmail.com"
apoderados_conflicto = Apoderado.objects.filter(email=email_problema)
print(f"Apoderados con email {email_problema}: {apoderados_conflicto.count()}")
for ap in apoderados_conflicto:
    estudiantes = Estudiante.objects.filter(apoderado=ap)
    hijos = [f"{e.nombre} {e.apellido_paterno}" for e in estudiantes]
    print(f"  - {ap.rut} | {ap.nombre_completo()} | Hijos: {', '.join(hijos)}")
