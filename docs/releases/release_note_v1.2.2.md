Release Note — v1.2.2

Fecha: 27 de agosto de 2025  
Responsable: Lidia Andrea Inostroza Yañez  
Contexto: Validación reproducible del sistema escolar digital mediante entorno Docker y pruebas automatizadas con `pytest`.

---

## Objetivos alcanzados

- Entorno dockerizado funcional y reproducible
- Integración de `pytest` como herramienta de validación técnica
- Segmentación institucional validada en modelos y formularios
- Evidencia técnica documentada en `docs/`

---

## Pruebas automatizadas

- Configuración:
  Archivo `pytest.ini` agregado para parametrización reproducible

- Tests ejecutados:  
  - `tests/core/test_model_perfilusuario.py`  
    Valida segmentación institucional por tipo de usuario

- Resultado: 
Todos los tests pasaron exitosamente en entorno local y contenedor

---

## Dockerización

- Archivo agregado: `docker-compose.yml`  
  Define servicios para entorno reproducible

- Validación:
  Documentada en `docs/docker_setup.md`  
  Incluye comandos, dependencias y pasos de ejecución

---

## Documentación técnica

- `docs/tests/tests_validacion.md`  
  Evidencia de ejecución de pruebas automatizadas

- `docs/docker_setup.md`  
  Validación del entorno dockerizado

---

## Tag creado

```bash
git tag -a v1.2.2 -m "Versión reproducible con Docker y pruebas automatizadas validadas"
