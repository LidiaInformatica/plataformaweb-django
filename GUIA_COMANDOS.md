# Guía de Comandos Django - Plataforma Web

## ✅ CONFIGURACIÓN COMPLETADA EXITOSAMENTE

### 🚀 Comandos rápidos para usar el proyecto

#### Para iniciar el proyecto (uso diario):
```powershell
# Opción 1: Usar script automático
.\iniciar_servidor.ps1

# Opción 2: Comandos manuales
cd "c:\Users\Pc38\Downloads\plataformaweb-django"
.\venv\Scripts\Activate.ps1
python manage.py runserver
```

#### Para iniciar solo el servidor:
```powershell
.\start_server.ps1
```

#### Para crear superusuario:
```powershell
.\crear_superusuario.ps1
```

### 🔧 Comandos técnicos

#### Gestión de base de datos:
```powershell
# Crear migraciones
python manage.py makemigrations

# Aplicar migraciones
python manage.py migrate

# Ver estado de migraciones
python manage.py showmigrations
```

#### Gestión de usuarios:
```powershell
# Crear superusuario
python manage.py createsuperuser

# Cambiar contraseña de usuario
python manage.py changepassword <username>
```

#### Gestión del servidor:
```powershell
# Iniciar servidor
python manage.py runserver

# Iniciar servidor en puerto específico
python manage.py runserver 8080

# Iniciar servidor sin auto-reload
python manage.py runserver --noreload
```

### 🌐 URLs importantes

- **Aplicación principal:** http://127.0.0.1:8000
- **Panel de administración:** http://127.0.0.1:8000/admin
- **Cuentas de usuario:** http://127.0.0.1:8000/accounts/
- **Estudiantes:** http://127.0.0.1:8000/estudiantes/
- **Actividades:** http://127.0.0.1:8000/actividades/
- **Cuotas:** http://127.0.0.1:8000/cuotas/

### 🛠️ Tecnologías utilizadas

- **Django 4.2.7** - Framework web
- **Pillow** - Procesamiento de imágenes
- **python-decouple** - Configuración de variables
- **SQLite** - Base de datos (por defecto)

### 📁 Estructura del proyecto

```
plataformaweb-django/
├── manage.py
├── requirements.txt
├── iniciar_servidor.ps1
├── start_server.ps1
├── crear_superusuario.ps1
├── db.sqlite3
├── venv/
├── plataformaweb/
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
├── core/
├── accounts/
├── estudiantes/
├── actividades/
├── cuotas/
├── templates/
└── static/
```

### 🔍 Solución de problemas

#### Problema: Error de importación Django
```powershell
# Solución: Activar entorno virtual
.\venv\Scripts\Activate.ps1
```

#### Problema: Error con Pillow
```powershell
# Solución: Instalar Pillow
pip install Pillow
```

#### Problema: Error de migraciones
```powershell
# Solución: Aplicar migraciones
python manage.py migrate
```

### 🎯 Pasos siguientes

1. **Crear superusuario**: `.\crear_superusuario.ps1`
2. **Acceder al admin**: http://127.0.0.1:8000/admin
3. **Configurar datos iniciales** en el panel de administración
4. **Personalizar templates** en la carpeta `templates/`
5. **Agregar archivos estáticos** en la carpeta `static/`

### 📞 Comandos útiles adicionales

```powershell
# Ver versión de Django
python -c "import django; print(django.get_version())"

# Verificar configuración
python manage.py check

# Crear app nueva
python manage.py startapp nombre_app

# Recopilar archivos estáticos
python manage.py collectstatic

# Abrir shell de Django
python manage.py shell
```

---
**Proyecto configurado exitosamente el 7 de agosto de 2025**
