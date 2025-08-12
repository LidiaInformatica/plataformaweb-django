# Plataforma Web Escolar

Sistema de gestión escolar desarrollado en Django para el control de estudiantes, actividades y cuotas de pago.

## ✅ PROYECTO CONFIGURADO Y LISTO PARA USAR

### 🚀 Inicio Rápido

Para iniciar el proyecto, ejecuta uno de estos comandos:

```powershell
# Opción 1: Script automático (recomendado)
.\iniciar_servidor.ps1

# Opción 2: Comandos manuales
cd "c:\Users\Pc38\Downloads\plataformaweb-django"
.\venv\Scripts\Activate.ps1
python manage.py runserver
```

Luego abre tu navegador en: **http://127.0.0.1:8000**

### 📋 Scripts Disponibles

- **`iniciar_servidor.ps1`** - Configuración completa y automática
- **`start_server.ps1`** - Inicio rápido del servidor
- **`crear_superusuario.ps1`** - Crear usuario administrador
- **`verificar_sistema.ps1`** - Verificar que todo funcione correctamente

### 🛠️ Tecnologías

- **Django 4.2.7** ✅ Instalado
- **Pillow** ✅ Instalado
- **python-decouple** ✅ Instalado
- **SQLite** ✅ Base de datos configurada

## Características Principales

### 🏫 Gestión Institucional
- Dashboard con resumen mensual de recaudación
- Segmentación de perfiles (Apoderado/Directiva)
- Sistema de mensajes y configuración

### 👥 Gestión de Estudiantes
- Registro de estudiantes y apoderados
- Control de vínculos familiares
- Información de contacto y cursos

### 📅 Gestión de Actividades
- Registro de actividades escolares
- Asignación por cursos y fechas
- Control de montos por estudiante
- Filtros avanzados y exportación

### 💰 Gestión de Cuotas
- Vinculación estudiante-actividad
- Registro de pagos con validación
- Estados de pago (Pendiente/Pagado/Vencido)
- Historial de transacciones

## Estructura del Proyecto

\`\`\`
plataformaweb/
├── core/                   # App principal - Dashboard y perfiles
├── estudiantes/           # Gestión de estudiantes y apoderados
├── actividades/          # Gestión de actividades escolares
├── cuotas/              # Gestión de cuotas y pagos
├── templates/           # Plantillas HTML
│   ├── base.html       # Plantilla base
│   ├── core/           # Templates del core
│   ├── estudiantes/    # Templates de estudiantes
│   ├── actividades/    # Templates de actividades
│   └── cuotas/         # Templates de cuotas
├── static/             # Archivos estáticos
│   ├── css/           # Estilos CSS
│   └── js/            # Scripts JavaScript
└── plataformaweb/     # Configuración del proyecto
\`\`\`

## Tecnologías Utilizadas

- **Backend**: Django 4.2.7
- **Base de Datos**: SQLite3
- **Frontend**: Bootstrap 5.1.3
- **Iconos**: Font Awesome 6.0.0
- **Estilos**: CSS personalizado

## Instalación y Configuración

### Prerrequisitos
- Python 3.8 o superior
- pip (gestor de paquetes de Python)

### Pasos de Instalación

1. **Clonar el repositorio**
\`\`\`bash
git clone <url-del-repositorio>
cd plataformaweb
\`\`\`

2. **Crear entorno virtual**
\`\`\`bash
python -m venv venv
source venv/bin/activate  # En Windows: venv\Scripts\activate
\`\`\`

3. **Instalar dependencias**
\`\`\`bash
pip install -r requirements.txt
\`\`\`

4. **Configurar base de datos**
\`\`\`bash
python manage.py makemigrations
python manage.py migrate
\`\`\`

5. **Crear superusuario**
\`\`\`bash
python manage.py createsuperuser
\`\`\`

6. **Crear usuarios de prueba (opcional)**
\`\`\`bash
python scripts/crear_usuarios_prueba.py
\`\`\`

7. **Ejecutar servidor de desarrollo**
\`\`\`bash
python manage.py runserver
\`\`\`

8. **Acceder a la aplicación**
- Aplicación: http://127.0.0.1:8000/
- Login: http://127.0.0.1:8000/accounts/login/
- Admin: http://127.0.0.1:8000/admin/

### Usuarios de Prueba
- **Administrador**: Lidia | Contraseña: 'admin123'
- **Apoderado**: RUT `12345678k` | Contraseña: `password123`
- **Directiva**: RUT `98765432j` | Contraseña: `password123`

## Funcionalidades Implementadas

### ✅ Dashboard (Core)
- **RF-08**: Resumen mensual con métricas clave y bandeja de mensajes por perfil
- Últimos pagos registrados con estados
- Accesos rápidos a funciones principales
- **RF-03**: Perfil de usuario con segmentación (Apoderado/Directiva)

### ✅ Estudiantes
- Lista completa con información de estudiantes y apoderados
- Datos de vínculos familiares y contacto
- Estadísticas generales del sistema

### ✅ Actividades
- **RF-09**: Lista con filtros avanzados por tipo, curso y fechas
- Información detallada de fechas, montos y cursos asignados
- Estados de actividades (Activa/Planificada/Finalizada)
- **RF-05**: Simulación de exportación en PDF y Excel

### ✅ Cuotas y Pagos
- **RF-01**: Registro de cuotas escolares por actividad
- **RF-02**: Visualización del estado de pago por apoderado
- **RF-04**: Filtros avanzados por nombre, RUT y actividad
- **RF-07**: Formulario con validación completa de campos obligatorios
- **RF-09**: Historial detallado de cuotas por actividad específica
- Estados de pago y control de saldos pendientes

### ✅ Sistema de Notificaciones
- **RF-06**: Notificaciones automáticas de nuevas cuotas y pagos pendientes
- **RF-08**: Bandeja de mensajes y alertas segmentada por perfil
- Configuración personalizable de notificaciones
- Alertas de vencimiento y recordatorios automáticos

### ✅ Exportación de Datos
- **RF-05**: Exportación simulada en formatos PDF y Excel
- Reportes por actividad y estado de pagos
- Filtros aplicables a las exportaciones

### ✅ Sistema de Autenticación
- **Login/Logout**: Sistema completo de inicio y cierre de sesión
- **Registro de usuarios**: Formulario de registro con validación de RUT
- **Perfiles de usuario**: Segmentación Apoderado/Directiva
- **Middleware de perfiles**: Control de acceso según tipo de usuario
- **Cambio de contraseña**: Funcionalidad segura de cambio de contraseña
- **Validación de formularios**: Validación completa de RUT y datos

## Características Técnicas

### Formateo de Moneda
- Formato chileno sin decimales
- Separador de miles con punto
- Símbolo peso ($) precediendo el valor
- Ejemplo: $15.000

### Validación de Formularios
- Campos obligatorios marcados
- Validación de montos positivos
- Mensajes de error contextuales
- Alertas de éxito/error

### Diseño Responsivo
- Compatible con dispositivos móviles
- Interfaz adaptativa con Bootstrap
- Navegación optimizada para touch

### Datos Simulados
- Sistema funcional con datos de prueba
- Estudiantes, actividades y pagos simulados
- Métricas realistas para demostración

## Próximas Funcionalidades

- [ ] Sistema de autenticación real
- [ ] Exportación real a Excel/CSV
- [ ] Reportes avanzados
- [ ] Notificaciones por email
- [ ] API REST
- [ ] Integración con sistemas de pago

## Contribución

1. Fork el proyecto
2. Crear rama para nueva funcionalidad (`git checkout -b feature/nueva-funcionalidad`)
3. Commit los cambios (`git commit -am 'Agregar nueva funcionalidad'`)
4. Push a la rama (`git push origin feature/nueva-funcionalidad`)
5. Crear Pull Request

