**Autora:** Lidia Andrea Inostroza Yáñez  
**Proyecto:** Sistema de Gestión Digital de Cuotas Escolares  
**Avance actual:** 95% de requerimientos funcionales implementados  
**Versión del repositorio:** `v1.2.3` — rama `segmentacion-admin-directiva-validada`

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

| Fase       | Estado      | % Avance |
|------------|-------------|----------|
| Análisis   | Completado  | 100%     |
| Diseño     | Completado  | 100%     |
| Desarrollo | Completado  | 95%      |
| Testing    | En progreso | 25%      |
| Cierre     | Pendiente   | 0%       |

---

## Requerimientos funcionales desarrollados

| Código  | Descripción                                         | Estado                        | Nivel de Cumplimiento |
|---------|-----------------------------------------------------|-------------------------------|----------------------|
| RF-01   | Registrar cuotas escolares por actividad           | Completado                    | 100%                 |
| RF-02   | Visualizar estado de pago por alumno               | Completado                    | 100%                 |
| RF-03   | Acceder con sesión segmentada                      | Completado                    | 100%                 |
| RF-04   | Filtrar actividad por nombre/RUT/curso             | Completado                    | 100%                 |
| RF-05   | Exportar información PDF/Excel                     | Implementado parcialmente     | 70%                  |
| RF-06   | Notificaciones automáticas                         | Completado                    | 100%                 |
| RF-07   | Validar campos obligatorios                        | Completado                    | 100%                 |
| RF-08   | Visualizar mensajes y alertas                      | Completado                    | 100%                 |
| RF-09   | Crear alumno y apoderado desde la plataforma       | Implementado parcialmente     | 85%                  |

---

## Avances Técnicos Destacados

### Segmentación de Perfiles Institucionales - COMPLETADO
- **Sistema de perfiles unificado** mediante modelo `PerfilUsuario`
- **Redirección automática** post-login según tipo de perfil
- **Dashboards diferenciados** para administrador, directiva y apoderado
- **Datos reales integrados** - eliminación completa de datos ficticios
- **Resolución de conflictos** de email entre roles

### Módulo de Notificaciones - COMPLETADO
- **Configuración SMTP funcional** con Gmail
- **Envío de notificaciones automáticas** a apoderados
- **Bandeja de mensajes personalizada** por perfil
- **Vista protegida** para envío manual de notificaciones
- **Trazabilidad completa** con fecha de envío y estado de lectura

### Sistema de Autenticación - COMPLETADO
- **Login segmentado** con redirección automática
- **Perfiles institucionales** validados: administrador, directiva (presidenta/secretaria/tesorera), apoderado
- **Base de datos real** con estudiantes Benjamin Santa Cruz Inostroza y Vicente Navarrete Inostroza
- **Múltiples hijos por apoderado** correctamente gestionados

### Validación y Testing - EN DESARROLLO
- **Scripts de verificación** automatizados
- **Configuración Docker** reproducible
- **Pytest integrado** para validación de modelos
- **Auditoría de datos** reales vs ficticios

---

## Dockerización del entorno

Requisitos previos
•	Docker y Docker Compose instalados (en Windows, Docker Desktop ya los incluye)
•	Proyecto clonado en: C:\plataformaweb-django

## Levantar el sistema

Desde la raíz del proyecto

docker compose up -d --build

•	Construye la imagen plataformaweb-django-web
•	Levanta el contenedor plataformaweb en segundo plano
•	Expone el sistema en http://localhost:8000
 
Acceso a la plataforma

Plataforma: http://localhost:8000
•	Usuario Admin: Lidia / Contraseña: admin123
•	Usuario Apoderado: apoderado3 / Contraseña: Lidi0354
Panel Admin: http://localhost:8000/admin

Entrar al contenedor en modo interactivo
docker exec -it plataformaweb bash
•	Acceso al shell del contenedor


Base de datos funcional incluida

Este repositorio incluye el archivo db.sqlite3 con datos reales del sistema escolar digital validados para defensa de título:

- Estudiantes reales: Benjamin Santa Cruz Inostroza, Vicente Navarrete Inostroza
- Apoderado real: Lidia Inostroza (vinculada a ambos estudiantes)
- Actividades escolares con cuotas y pagos registrados
- Notificaciones automáticas funcionales
- Perfiles institucionales completos
- No es necesario ejecutar scripts de poblamiento. Sistema listo para demostración académica.

Validación funcional

- Sistema ejecutándose correctamente en entorno Docker
- Login funcional con credenciales reales para los tres perfiles
- Dashboards diferenciados mostrando datos específicos por rol
- Módulo de pagos y cuotas operativo
- Notificaciones automáticas validadas
- Exportación básica implementada
- Evidencias técnicas documentadas




Estructura del Proyecto

plataformaweb-django/
├── core/             # Dashboard y perfiles institucionales
├── estudiantes/      # Gestión de estudiantes y apoderados
├── actividades/      # Registro y control de actividades escolares
├── cuotas/           # Módulo de pagos y estado de cuotas
├── accounts/         # Autenticación y perfiles segmentados
├── templates/        # Plantillas HTML por módulo
├── static/           # Archivos estáticos (CSS, JS, imágenes)
├── scripts/          # Scripts de automatización y verificación
├── docs/             # Documentación técnica y evidencias
├── Dockerfile        # Configuración de contenedor
├── docker-compose.yml # Orquestación de servicios
├── requirements.txt  # Dependencias Python
└── pytest.ini       # Configuración de testing


Control de versiones

Versión	Fecha	    Descripción	Rama asociada
v1.0	2025-08-10	Versión inicial con funcionalidades básicas	main
v1.1.0	2025-08-15	Dockerización reproducible y validación	avance-60porciento
v1.1.1	2025-08-21	Base de datos funcional integrada	avance-60porciento
v1.2.0	2025-08-24	Módulo de notificaciones completado	avance-60porciento
v1.2.1	2025-08-26	Segmentación institucional validada	avance-60porciento
v1.2.2	2025-08-27	Validación reproducible con Docker y Pytest	avance-60porciento
v1.2.3	2025-08-28	Cierre funcional de segmentación - datos reales         
                    únicamente	segmentacion-admin-directiva-validada



Scripts de Verificación y Mantenimiento

- verificar_segmentacion.py - Confirma integridad del sistema de perfiles
- verificar_datos_reales.py - Audita datos reales vs ficticios
- sincronizar_perfiles_usuarios.py - Mantiene consistencia Usuario-Perfil
- limpiar_datos_ficticios.py - Elimina datos temporales no necesarios
- configurar_usuarios_admin.py - Configura usuarios administrativos





Estado Final para Defensa de Título

Sistema completamente funcional con segmentación de perfiles validada:

-Administrador: Dashboard completo con acceso a toda la información institucional
-Directiva: Dashboard institucional con funciones específicas por cargo (presidenta/secretaria/tesorera)
-Apoderado: Dashboard personalizado con información de hijos, cuotas y actividades
-Datos reales verificados para demostración académica sin contenido ficticio.

Arquitectura técnica defendible con documentación completa y evidencia de funcionamiento.

-Merge técnico: segmentacion-admin-directiva-validada → master

El 28 de agosto de 2025 se realizó el merge definitivo desde la rama segmentacion-admin-directiva-validada hacia master, consolidando:

- Segmentación completa de perfiles institucionales
- Eliminación total de datos ficticios
- Sistema de autenticación robusto con datos reales
- Dashboards funcionales para los tres tipos de usuario
- Base de datos lista para defensa académica

Este merge marca el cierre técnico del desarrollo y la preparación final para defensa de título.

Documentación técnica

-Arquitectura: Patrón MVT (Model-View-Template)
-Base de datos: SQLite con datos reales del colegio
-Backend: Django 5.2.5 / Python 3.13
-Frontend: Bootstrap 5.3 + JavaScript personalizado
-Notificaciones: Gmail SMTP validado en producción
-Testing: Pytest + Django TestCase
-Containerización: Docker + docker-compose


