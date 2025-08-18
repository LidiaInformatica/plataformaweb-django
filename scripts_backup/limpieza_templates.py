import os

# Carpeta de templates
TEMPLATES_DIR = "templates"
BACKUP_DIR = "templates_backup"

# Lista de templates usados (de tus vistas y extends)
templates_usados = [
    "accounts/login.html",
    "accounts/register.html",
    "accounts/crear_perfil.html",
    "accounts/perfil.html",
    "accounts/cambiar_password.html",
    "actividades/lista.html",
    "actividades/form.html",
    "actividades/detalle.html",
    "actividades/confirmar_eliminar.html",
    "actividades/exportar.html",
    "core/dashboard.html",
    "core/perfil.html",
    "core/bandeja_mensajes.html",
    "cuotas/lista_pagos.html",
    "cuotas/registrar_pago.html",
    "cuotas/historial_actividad.html",
    "cuotas/estado_apoderado.html",
    "estudiantes/lista.html",
    "estudiantes/form.html",
    "estudiantes/detalle.html",
    "estudiantes/confirmar_eliminar.html",
    "base.html"  # si lo tenés como base común
]

# Crear carpeta de respaldo si no existe
if not os.path.exists(BACKUP_DIR):
    os.makedirs(BACKUP_DIR)

# Buscar todos los templates
candidatos = []
for root, dirs, files in os.walk(TEMPLATES_DIR):
    for file in files:
        if file.endswith(".html"):
            rel_path = os.path.relpath(os.path.join(root, file), TEMPLATES_DIR).replace("\\", "/")
            if rel_path not in templates_usados:
                candidatos.append(rel_path)

# Mostrar candidatos
print("\n📋 Templates candidatos a respaldo:")
for c in candidatos:
    print(f" - {c}")

# Preguntar si querés respaldarlos
confirmar = input("\n¿Deseás respaldarlos ahora? (s/n): ").lower()
if confirmar == "s":
    for c in candidatos:
        origen = os.path.join(TEMPLATES_DIR, c)
        destino = os.path.join(BACKUP_DIR, os.path.basename(c))
        os.rename(origen, destino)
    print(f"\n✅ Archivos movidos a {BACKUP_DIR}")
else:
    print("\n❌ No se movió ningún archivo.")
# Fin del script