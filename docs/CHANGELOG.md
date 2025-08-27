# CHANGELOG

Registro de cambios técnicos del sistema escolar digital — Colegio Adventista Talcahuano Centro

---

## v1.1.1 - Base de datos funcional integrada (21-08-2025)
- Se reemplaza `db.sqlite3` por versión con datos reales desde entorno original
- El dashboard muestra estudiantes, pagos, actividades y notificaciones
- Se actualiza `README.md` con comandos reproducibles y credenciales reales
- Validación funcional completa en entorno Docker
- Sistema listo para revisión académica sin necesidad de poblamiento manual

## v1.1.0 - Dockerización inicial y estructura funcional (15-08-2025)
- Se configura `Dockerfile` para entorno reproducible
- Se corrige acceso local (`localhost:8000`) en `README.md`
- Se agregan dependencias faltantes (`django-extensions==4.1`) en `requirements.txt`
- Validación funcional con `docker build` y `docker run`
- Acceso operativo con credenciales reales (`Lidia / admin123`)

## v1.0.0 - Versión local no dockerizada (10-08-2025)
- Sistema funcional en entorno virtual local (`venv`)
- Login operativo con credenciales de prueba
- Base de datos vacía (`db.sqlite3`) sin datos reales
- README inicial sin instrucciones reproducibles
- No se incluía Docker ni control de versiones completo

## v1.2.0 - Módulo de Notificaciones y mejoras defendibles (22-08-2025)
-Se corrige cálculo del mes en español en dashboard.html usando locale.setlocale y strftime('%B')
-Se eliminan modelos duplicados y scripts huérfanos tras auditoría manual (core/models.py, core/scripts/)
-Se valida configuración SMTP en entorno dockerizado y envío real desde shell Django
-Se crea vista protegida para enviar notificaciones manuales a apoderados vinculados (enviar_notificacion_manual.html)
-Se agregan filtros personalizados en templatetags/form_filters.py para mejorar la visualización de formularios
-Se mejora la estética y usabilidad de vistas (base.html, lista.html, dashboard.css)
-Se documenta cada avance en release_note_v1.2.0.md y README.md, con evidencia técnica y visual

## v1.2.1 – Segmentación institucional validada (26-08-2025)
- Validación de segmentación funcional para perfiles “admin” y “directiva” (énfasis en presidenta)
- Acceso diferenciado a vistas protegidas según grupo institucional
- Lectura de notificaciones automáticas habilitada para presidenta
- Corrección de trazabilidad en modelo `Notificacion` (`estudiante` como ForeignKey)
- Eliminación de notificaciones huérfanas y ajuste de lógica `leida=True`
- Estado RF-03 y RF-06: validados; RF-09: avance parcial con presidenta funcional
- Documentado en release_note_v1.2.1.md con evidencia técnica

## v2025.08.26 – Consolidación y preparación de auditoría de Apoderado (26-08-2025)
- Diagnóstico y documentación de acceso a `python manage.py shell` en Windows y Docker
- Procedimiento estandarizado para iniciar contenedor detenido y acceder a shell interna
- Auditoría de datos: diferenciados datos reales vs. de prueba; marcaje de temporales/fixtures para eliminación controlada
- Dashboard institucional: ajustes de tamaño, reordenamiento de bloques e incremento de prioridad de indicadores financieros
- Notificaciones automáticas: incorporadas columnas “Estudiante” y “Fecha de envío” para trazabilidad
- Creación de vista/dashboard para perfil de Apoderado (acceso aún bloqueado por falta de vínculo `Apoderado → User`)
- Pendientes: 
  - Confirmar OneToOne/FK y migrar datos con log
  - Aplicar segmentación por rol en rutas/menús y ocultación de componentes fuera de alcance
  - Verificar acceso restringido de Apoderado autenticado
  - Eliminar datos temporales con evidencia

