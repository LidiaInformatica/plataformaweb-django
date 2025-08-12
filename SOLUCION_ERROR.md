# SOLUCIÓN DEFINITIVA PARA EL ERROR DE cargo_directiva

## Problema
Error: `sqlite3.OperationalError: no such column: core_perfilusuario.cargo_directiva`

## Solución Paso a Paso

### 1. Detener el servidor
```powershell
# Presionar Ctrl+C en la terminal del servidor
# O ejecutar:
taskkill /f /im python.exe
```

### 2. Aplicar solución de emergencia
```powershell
python apply_migration.py
```

### 3. Si el paso 2 no funciona, recrear base de datos
```powershell
python recreate_database_clean.py
python manage.py migrate
python crear_admin.py
```

### 4. Verificar que todo está bien
```powershell
python manage.py check
python manage.py showmigrations
```

### 5. Iniciar servidor
```powershell
python manage.py runserver
```

### 6. Probar login
- URL: http://127.0.0.1:8000
- Usuario: admin
- Contraseña: admin123

## Scripts disponibles para solucionar:

1. **apply_migration.py** - Aplica la migración usando Django ORM
2. **emergency_fix.py** - Solución de emergencia con SQLite directo
3. **recreate_database_clean.py** - Recrea la base de datos desde cero
4. **crear_admin.py** - Crea usuario admin con contraseña admin123

## Si nada funciona:

```powershell
# Eliminar base de datos y empezar de cero
del db.sqlite3
python manage.py migrate
python crear_admin.py
python manage.py runserver
```

El problema es que la columna `cargo_directiva` no existe físicamente en la base de datos aunque está definida en el modelo Django.
