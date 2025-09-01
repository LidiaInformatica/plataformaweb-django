# Control de Ramas

## Rama: testing/waterfall-rf-validation

### Información General
- **Propósito**: Validación de requerimientos funcionales
- **Estado**: En progreso
- **Fecha Creación**: 01/09/2025
- **Responsable**: Equipo Testing

### Commits Principales
- Configuración Docker para testing
- Tests RF-01 y RF-02
- Documentación actualizada
- Fixes en cuotas
- Archivos técnicos
- Reglas de ignorado

### Enlaces
- **Pull Request**: [Ver en GitHub](https://github.com/LidiaInformatica/plataformaweb-django/pull/new/testing/waterfall-rf-validation)
- **Base**: master
- **Target**: testing/waterfall-rf-validation

### Tests Implementados
- RF-01: `test_registro_cuotas_por_actividad.py`
- RF-02: `test_ciclo1_calculo_estado_pago.py`, `test_ciclo2_segmentacion_apoderado.py`

Branch: testing/waterfall-rf-validation
Commits: 3 nuevos commits
Archivos principales modificados:
- core/management/commands/configurar_usuarios.py (nuevo)
- core/management/commands/reorganizar_perfiles.py (nuevo)
- docker-compose.yml (actualizado)
- .gitignore (actualizado)