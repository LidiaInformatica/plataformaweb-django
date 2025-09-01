# Plataforma de Gestión Digital de Cuotas Escolares
## Fase: Testing & Quality Assurance - Metodología Waterfall

### Estado de Avance por Fases
| Fase       | Estado      | % Avance | Observaciones |
|------------|-------------|----------|---------------|
| Análisis   | Completado  | 100%     | Documentación validada |
| Diseño     | Completado  | 100%     | Arquitectura implementada |
| Desarrollo | Completado  | 95%*     | *Sujeto a validación por testing |
| Testing    | En progreso | 25%      | Ciclos de prueba en ejecución |
| Cierre     | Pendiente   | 0%       | Pendiente validación final |

### Validación de Requerimientos Funcionales
| Código | Descripción                                  | Avance (%) | Evidencia / Test                                    | Estado   |
|--------|----------------------------------------------|------------|-----------------------------------------------------|----------|
| RF-01  | Registrar cuotas escolares por actividad     | 100%       | test_registro_basico.py, test_validacion_monto.py, test_simulacion_completa.py, docs/evidencias-RF01/ | PASSED   |
| RF-02  | Visualizar estado de pago por alumno         | 50%        | test_ciclo1_calculo_estado_pago.py, test_ciclo2_segmentacion_apoderado.py | CICLO 2 - FAILED |
| RF-03  | Acceder con sesión segmentada               | En Testing | | |
| RF-04  | Filtrar actividad por nombre/RUT/curso      | En Testing | | |
| RF-05  | Exportar información PDF/Excel              | Pendiente  | | |
| RF-06  | Notificaciones automáticas                  | En Testing | | |
| RF-07  | Validar campos obligatorios                 | Pendiente  | | |
| RF-08  | Visualizar mensajes y alertas               | En Testing | | |
| RF-09  | Crear alumno y apoderado desde plataforma   | Pendiente  | | |

### Estructura de Testing
```
tests/
├── rf01/                           # Tests RF-01
│   ├── test_registro_basico.py
│   ├── test_validacion_monto.py
│   └── test_simulacion_completa.py
├── rf02/                           # Tests RF-02
│   ├── test_ciclo1_calculo_estado_pago.py
│   └── test_ciclo2_segmentacion_apoderado.py
└── ...

docs/
├── evidencias-RF01/               # Evidencias técnicas RF-01
├── evidencias-RF02/               # Evidencias técnicas RF-02
│   ├── test_rf02_ciclo1.log
│   └── test_rf02_ciclo2.log
└── ...
```

### Control de Versiones - Testing
| Rama                            | Propósito                    | Estado    |
|--------------------------------|------------------------------|-----------|
| testing-waterfall-rf-validation | Validación de RFs por ciclos| Activa    |
| main                           | Código base estable          | Estable   |

### Notas Técnicas
- Testing basado en ciclos de validación
- Evidencias documentadas por requerimiento funcional
- Uso de pytest para automatización
- Entorno Docker reproducible