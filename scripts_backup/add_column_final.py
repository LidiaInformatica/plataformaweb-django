#!/usr/bin/env python
"""
Script final para añadir la columna cargo_directiva
"""
import sqlite3
import os
import sys

def main():
    db_path = 'db.sqlite3'
    
    if not os.path.exists(db_path):
        print(" Base de datos no encontrada")
        return False
    
    try:
        # Conectar a SQLite
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        # Verificar tabla
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='core_perfilusuario'")
        if not cursor.fetchone():
            print(" Tabla core_perfilusuario no encontrada")
            return False
        
        # Obtener columnas actuales
        cursor.execute("PRAGMA table_info(core_perfilusuario)")
        columns = [row[1] for row in cursor.fetchall()]
        
        print(f"Columnas actuales: {', '.join(columns)}")
        
        # Verificar si la columna existe
        if 'cargo_directiva' in columns:
            print(" La columna cargo_directiva ya existe")
            return True
        
        # Añadir la columna
        print("Añadiendo columna cargo_directiva...")
        cursor.execute("ALTER TABLE core_perfilusuario ADD COLUMN cargo_directiva VARCHAR(20)")
        conn.commit()
        
        # Verificar que se añadió
        cursor.execute("PRAGMA table_info(core_perfilusuario)")
        columns_new = [row[1] for row in cursor.fetchall()]
        
        if 'cargo_directiva' in columns_new:
            print(" Columna añadida exitosamente")
            print(f"Nuevas columnas: {', '.join(columns_new)}")
            return True
        else:
            print(" Error: columna no se añadió")
            return False
            
    except sqlite3.OperationalError as e:
        if "duplicate column name" in str(e):
            print(" La columna ya existe (duplicate column)")
            return True
        else:
            print(f" Error SQL: {e}")
            return False
    except Exception as e:
        print(f" Error: {e}")
        return False
    finally:
        conn.close()

if __name__ == "__main__":
    print(" Añadiendo columna cargo_directiva...")
    success = main()
    if success:
        print(" Listo. Ahora descomente el campo en models.py")
        sys.exit(0)
    else:
        print(" Error al añadir la columna")
        sys.exit(1)
