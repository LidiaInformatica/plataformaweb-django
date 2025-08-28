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
  
v1.2.2 – Validación reproducible con Docker y Pytest (27-08-2025)
Se configura docker-compose.yml para ejecución automatizada del sistema escolar digital
Se valida el entorno Docker con python manage.py runserver en contenedor activo
Se ejecuta pytest en entorno dockerizado, confirmando test funcional test_user_str
Se registra evidencia técnica en docs/tests_validacion.md y log reproducible en docs/evidencias/est_model_perfilusuario.log
Se documenta la configuración del entorno en docs/docker_setup.md
Se consolida commit técnico con trazabilidad completa (v1.2.2)
Estado RF-07 y RF-08: validados en entorno reproducible
Pendiente: integración de pytest como servicio en docker-compose.yml para automatización continua

## [2025-08-27] Segmentación institucional dockerizada
- Commit: `6d71443`
- Redirección por perfil validada
- Datos reales en dashboard de Apoderado
- Imagen Docker reproducible
- Evidencia técnica documentada

## [2025-08-27] Imagen Docker reconstruida post-segmentación
- Basada en commit `6d71443`
- Incluye correcciones de redirección y datos reales
- Validada en entorno dockerizado


