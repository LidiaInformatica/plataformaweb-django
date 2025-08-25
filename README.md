
**Autora:** Lidia Andrea Inostroza Yáñez  
**Proyecto:** Sistema de Gestión Digital de Cuotas Escolares  
**Avance actual:** 77% de requerimientos funcionales implementados  
**Versión del repositorio:** `v1.2.0` — rama `avance-60porciento` extendida

---

## Contexto del Proyecto

Este sistema responde a una necesidad concreta del Colegio Adventista Talcahuano Centro: digitalizar la gestión de cuotas escolares voluntarias por curso. Actualmente, esta gestión se realiza de forma informal, lo que genera problemas de trazabilidad, transparencia y sobrecarga operativa.

---

## Objetivo General

Diseñar y desarrollar una plataforma web modular que permita:

- Registrar pagos voluntarios por actividad  
- Visualizar estado de cuotas por estudiante  
- Generar reportes exportables  
- Enviar notificaciones automáticas  
- Segmentar vistas por perfil institucional  

---

## Cronograma y avance por fases

| Fase       | Estado   | % Avance |
|------------|----------|----------|
| Análisis   | ✅       | 100%     |
| Diseño     | ✅       | 100%     |
| Desarrollo | ✅       | 77%      |
| Testing    | ⏳       | 0%       |
| Cierre     | ⏳       | 0%       |

---

## Requerimientos funcionales desarrollados

| Código  | Descripción                                         | Estado   |
|---------|-----------------------------------------------------|----------|
| RF-01   | Registrar cuotas escolares por actividad            | ✅       |
| RF-02   | Visualizar estado de pago por alumno                | ✅       |
| RF-03   | Acceder con sesión segmentada                       | ⚠️ Parcial |
| RF-04   | Filtrar actividad por nombre/RUT/curso              | ✅       |
| RF-05   | Exportar información PDF/Excel                      | ⚠️ Parcial |
| RF-06   | Notificaciones automáticas                          | ✅       |
| RF-07   | Validar campos obligatorios                         | ✅       |
| RF-08   | Visualizar mensajes y alertas                       | ✅       |
| RF-09   | Crear alumno y apoderado desde la plataforma        | ⚠️ Parcial |

---

## Módulo de Notificaciones — Avance técnico

El módulo pasó de estar en desarrollo parcial a estar funcional y validado. Se realizaron las siguientes mejoras:

- Configuración SMTP funcional con Gmail  
- Validación de envío real desde el shell de Django  
- Creación de vista protegida con formulario validado (`enviar_notificacion_manual.html`)  
- Integración de botón estilizado en el dashboard (`dashboard.html`, `dashboard.css`)  
- Corrección de lógica `leida=True` para evitar falsos positivos  
- Localización del mes en español con `locale.setlocale(locale.LC_TIME, 'es_ES.UTF-8')`  
- Eliminación de modelos duplicados y scripts huérfanos (`core/models.py`, `core/scripts/`)  
- Ajuste de configuración SMTP y prefijo de asunto (`settings.py`)  
- Documentación técnica y evidencia reproducible

---

## Dockerización del entorno

**Requisitos:**

- Docker instalado en Windows  
- Proyecto ubicado en `C:\plataformaweb-django`  

**Comandos:**

```powershell
docker build -t plataformaweb-django .
docker run -p 8000:8000 plataformaweb-django

- Acceso
Plataforma: http://localhost:8000/

Usuario: Lidia / Contraseña: admin123
Admin: http://localhost:8000/admin

- Base de datos funcional incluida
Este repositorio incluye el archivo db.sqlite3 con datos reales del sistema escolar digital. Esto permite:

Acceder al dashboard con datos funcionales
Validar el login y flujo de pagos
Visualizar estudiantes, actividades y notificaciones

No es necesario ejecutar scripts de poblamiento. Solo aplicar migraciones si se reconstruye desde cero.

- Validación funcional

El sistema se ejecuta correctamente en entorno Docker
Login funcional con credenciales reales
Acceso al dashboard y módulo de pagos
Pruebas manuales de flujo completadas
Envío de correos reales validado desde el shell
Evidencias técnicas y visuales documentadas

- Estructura del Proyecto

plaintext
plataformaweb-django/
├── core/             # Dashboard y perfiles institucionales
├── estudiantes/      # Gestión de estudiantes y apoderados
├── actividades/      # Registro y control de actividades escolares
├── cuotas/           # Módulo de pagos y estado de cuotas
├── accounts/         # Autenticación y perfiles segmentados
├── templates/        # Plantillas HTML
│   ├── base.html
│   ├── core/
│   ├── estudiantes/
│   ├── actividades/
│   └── cuotas/
├── static/           # Archivos estáticos
│   ├── css/
│   └── js/
├── scripts/          # Scripts de automatización y prueba
│   ├── iniciar_servidor.ps1
│   ├── crear_superusuario.ps1
│   ├── verificar_sistema.ps1
│   └── crear_usuarios_prueba.py
├── Dockerfile        # Dockerización del entorno
├── requirements.txt  # Dependencias del proyecto
└── README.md         # Documentación técnica


- Control de versione

Versión	Fecha	    Descripción                                                         	    Rama asociada
v1.0	2025-08-10	Versión inicial con funcionalidades básicas	                                main
v1.1.0	2025-08-15	Dockerización reproducible y validación	                                    avance-60porciento
v1.1.1	2025-08-21	Base de datos funcional, mejoras SMTP y documentación técnica defendible    avance-60porciento
v1.2.0	2025-08-24	Corrección de notificaciones, mejoras estéticas y validación SMTP en Docker	avance-60porciento

-Documentación técnica
Arquitectura: patrón MVT (Model-View-Template)
Base de datos: SQLite
Backend: Django 4.2.7 / Python 3.13
Frontend: Bootstrap 5.3 + JavaScript
Notificaciones: Gmail SMTP (validado)
>>>>>>> avance-60porciento
