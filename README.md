# Plataforma Web Escolar - Colegio Adventista Talcahuano Centro

**Autora:** Lidia Andrea Inostroza Yáñez  
**Proyecto:** Sistema de Gestión Digital de Cuotas Escolares  
**Avance actual:** 68% de requerimientos funcionales implementados  
**Versión del repositorio:** v1.0 + rama `avance-60porciento`

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

| Fase         | Estado | % Avance |
|--------------|--------|----------|
| Análisis     | ✅     | 100%     |
| Diseño       | ✅     | 100%     |
| Desarrollo   | ⚠️     | 69%      |
| Testing      | ⏳     | 0%       |
| Cierre       | ⏳     | 0%       |

---

## Requerimientos funcionales desarrollados

| Código | Descripción                                     | Estado     |
|--------|-------------------------------------------------|------------|
| RF-01  | Registrar cuotas escolares por actividad        | ✅         |
| RF-02  | Visualizar estado de pago por alumno            | ✅         |
| RF-03  | Acceder con sesión segmentada                   | ⚠️ Parcial |
| RF-04  | Filtrar actividad por nombre/RUT/curso          | ✅         |
| RF-05  | Exportar información PDF/Excel                  | ⚠️ Parcial |
| RF-06  | Notificaciones automáticas                      | ⚠️ Parcial |
| RF-07  | Validar campos obligatorios                     | ✅         |
| RF-08  | Visualizar mensajes y alertas                   | ⚠️ Parcial |
| RF-09  | Crear alumno y apoderado desde la plataforma    | ⚠️ Parcial |

---

### Dockerización del entorno

El sistema está dockerizado para garantizar reproducibilidad y trazabilidad.

### Requisitos

- Docker instalado en Windows
- Proyecto ubicado en `C:\plataformaweb-django`

### Comandos

```powershell
docker build -t plataformaweb-django .
docker run -p 8000:8000 plataformaweb-django

Acceso  
http://localhost:8000/

Usuario: Lidia 
Contraseña: admin123

http://localhost:8000/admin

Superusuario: Lidia
Contraseña: admin123

---Validación funcional---
El sistema se ejecuta correctamente en entorno Docker
El login funciona con credenciales reales
Se accede al dashboard y al módulo de pagos
Se han realizado pruebas manuales de flujo

---Estructura del Proyecto---

plataformaweb-django/
├── core/
├── estudiantes/
├── actividades/
├── cuotas/
├── accounts/
├── templates/
├── Dockerfile
├── requirements.txt
└── README.md

---Control de versiones---

Rama principal: main
Rama de avance: avance-60porciento
Versión actual: v1.0
Próxima versión: v1.1 (con testing y cierre)

---Documentación técnica---
Arquitectura: patrón MVT (Model-View-Template)
Base de datos: SQLite
Backend: Django 4.2.7 / Python 3.13
Frontend: Bootstrap 5.3 + JavaScript
Notificaciones: Gmail SMTP (en desarrollo)

---

## Historial de versiones

| Versión | Fecha | Descripción | Rama asociada |
|---------|-------|-------------|----------------|
| v1.0 | 2025-08-10 | Versión inicial con funcionalidades básicas | `main` |
| v1.1 | 2025-08-21 | Dockerización reproducible, corrección de dependencias, validación funcional y mejora en documentación | `avance-60porciento` |


