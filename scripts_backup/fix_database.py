#!/usr/bin/env python
"""
Script para arreglar la base de datos añadiendo la columna cargo_directiva
"""
import sqlite3
import os

# Ruta a la base de datos
db_path = 'db.sqlite3'

def fix_database():
    if not os.path.exists(db_path):
        print(f"Error: No se encuentra la base de datos en {db_path}")
        return False
    
    try:
        # Conectar a la base de datos
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        # Verificar si la tabla existe
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='core_perfilusuario'")
        table_exists = cursor.fetchone()
        
        if not table_exists:
            print("La tabla core_perfilusuario no existe")
            conn.close()
            return False
        
        # Verificar si la columna ya existe
        cursor.execute("PRAGMA table_info(core_perfilusuario)")
        columns = [row[1] for row in cursor.fetchall()]
        print(f"Columnas actuales: {columns}")
        
        if 'cargo_directiva' not in columns:
            print("Añadiendo columna cargo_directiva...")
            cursor.execute("""
                ALTER TABLE core_perfilusuario 
                ADD COLUMN cargo_directiva VARCHAR(20) NULL
            """)
            print("Columna añadida exitosamente")
        else:
            print("La columna cargo_directiva ya existe")
        
        # Confirmar cambios
        conn.commit()
        
        # Verificar la estructura final
        cursor.execute("PRAGMA table_info(core_perfilusuario)")
        columns_final = [row[1] for row in cursor.fetchall()]
        print(f"Columnas finales: {columns_final}")
        
        conn.close()
        return True
        
    except Exception as e:
        print(f"Error: {e}")
        return False

if __name__ == "__main__":
    if fix_database():
        print("Base de datos arreglada exitosamente")
    else:
        print("Error al arreglar la base de datos")
