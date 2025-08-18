import sqlite3
import os
import sys

def emergency_fix():
    """Solución de emergencia para el problema de cargo_directiva"""
    
    print("🚨 SOLUCIÓN DE EMERGENCIA PARA CARGO_DIRECTIVA")
    print("=" * 50)
    
    # 1. Verificar que existe la base de datos
    if not os.path.exists('db.sqlite3'):
        print("❌ No se encontró db.sqlite3")
        return False
    
    conn = sqlite3.connect('db.sqlite3')
    cursor = conn.cursor()
    
    try:
        # 2. Verificar tabla
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='core_perfilusuario'")
        if not cursor.fetchone():
            print("❌ Tabla core_perfilusuario no existe")
            return False
        
        # 3. Verificar columnas actuales
        cursor.execute("PRAGMA table_info(core_perfilusuario)")
        columns = [row[1] for row in cursor.fetchall()]
        print(f"📋 Columnas actuales: {', '.join(columns)}")
        
        # 4. Añadir columna si no existe
        if 'cargo_directiva' not in columns:
            print("➕ Añadiendo columna cargo_directiva...")
            cursor.execute("ALTER TABLE core_perfilusuario ADD COLUMN cargo_directiva VARCHAR(20)")
            conn.commit()
            print("✅ Columna añadida")
        else:
            print("✅ Columna ya existe")
        
        # 5. Verificar nuevamente
        cursor.execute("PRAGMA table_info(core_perfilusuario)")
        new_columns = [row[1] for row in cursor.fetchall()]
        print(f"📋 Columnas finales: {', '.join(new_columns)}")
        
        # 6. Marcar migración como aplicada
        print("📝 Marcando migración como aplicada...")
        
        # Verificar si existe la tabla de migraciones
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='django_migrations'")
        if cursor.fetchone():
            # Insertar registro de migración si no existe
            cursor.execute("""
                INSERT OR IGNORE INTO django_migrations (app, name, applied)
                VALUES ('core', '0002_add_cargo_directiva', datetime('now'))
            """)
            conn.commit()
            print("✅ Migración marcada como aplicada")
        
        return True
        
    except sqlite3.OperationalError as e:
        if "duplicate column name" in str(e):
            print("✅ La columna ya existe (duplicate column)")
            return True
        else:
            print(f"❌ Error SQL: {e}")
            return False
    except Exception as e:
        print(f"❌ Error: {e}")
        return False
    finally:
        conn.close()

if __name__ == "__main__":
    if emergency_fix():
        print("\n🎉 PROBLEMA RESUELTO")
        print("Ahora puedes iniciar el servidor:")
        print("python manage.py runserver")
    else:
        print("\n❌ ERROR: No se pudo resolver el problema")
        sys.exit(1)
