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

## Próxima versión: v1.1.2 (pendiente)
- Corrección de advertencia en módulo `Notificación`
- Validación de envío automático y visualización en dashboard
- Documentación técnica en release note y `README.md`
