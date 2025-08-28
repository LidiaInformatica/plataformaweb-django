# Configuración y validación del entorno Docker

Este documento registra la configuración reproducible del entorno Docker utilizado para el despliegue y validación funcional del sistema escolar digital del Colegio Adventista Talcahuano Centro.

---

## 1. Requisitos del entorno

- **Sistema operativo:** Windows 10/11
- **Docker Desktop:** instalado y operativo
- **Ubicación del proyecto:** `C:\platformweb-django`
- **Base de datos:** `db.sqlite3` con datos reales funcionales

---

## 2. Archivos involucrados

- `Dockerfile` — define la imagen base del sistema
- `docker-compose.yml` — orquesta los servicios y puertos
- `.env` — variables de entorno (SMTP, DEBUG, etc.)
- `db.sqlite3` — base de datos funcional incluida

---

## 3. Comandos ejecutados

### Construcción de imagen

```powershell
docker build -t platformweb-django .


Ejecución del contenedor
powershell
docker-compose up --build

Validación manual del servidor
powershell
python manage.py runserver
