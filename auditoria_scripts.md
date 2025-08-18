import os
import shutil
from datetime import datetime

# Configuración
BASE_DIR = os.getcwd()
BACKUP_DIR = os.path.join(BASE_DIR, 'scripts_backup')
LOG_FILE = os.path.join(BASE_DIR, 'auditoría_scripts.md')

# Crear carpeta de respaldo si no existe
os.makedirs(BACKUP_DIR, exist_ok=True)

# Archivos protegidos que no se deben mover
PROTEGIDOS = ['manage.py', 'settings.py', 'urls.py', 'wsgi.py', 'asgi.py']

# Función para detectar si un script está referenciado
def esta_referenciado(nombre_archivo, contenido_global):
    return nombre_archivo.replace('.py', '') in contenido_global

# Cargar contenido global de archivos clave
contenido_global = ''
for archivo in ['urls.py', 'views.py', 'settings.py']:
    ruta = os.path.join(BASE_DIR, archivo)
    if os.path.exists(ruta):
        with open(ruta, 'r', encoding='utf-8') as f:
            contenido_global += f.read()

# Auditoría
movidos = []
for archivo in os.listdir(BASE_DIR):
    if archivo.endswith('.py') and archivo not in PROTEGIDOS:
        if not esta_referenciado(archivo, contenido_global):
            origen = os.path.join(BASE_DIR, archivo)
            destino = os.path.join(BACKUP_DIR, archivo)
            shutil.move(origen, destino)
            movidos.append(archivo)

# Documentar auditoría
with open(LOG_FILE, 'a', encoding='utf-8') as log:
    log.write(f"\n### Auditoría {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
    for archivo in movidos:
        log.write(f"- `{archivo}` movido a `scripts_backup/`\n")

print(f"{len(movidos)} archivos movidos. Revisa auditoría_scripts.md para detalles.")