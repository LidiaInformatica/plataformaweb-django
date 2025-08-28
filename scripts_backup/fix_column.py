import sqlite3
import os

def add_missing_column():
    """Añadir la columna cargo_directiva directamente a SQLite"""
    
    db_path = 'db.sqlite3'
    
    if not os.path.exists(db_path):
        print(" La base de datos no existe")
        return False
    
    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        # Verificar si la tabla existe
        cursor.execute("""
            SELECT name FROM sqlite_master 
            WHERE type='table' AND name='core_perfilusuario'
        """)
        
        if not cursor.fetchone():
            print(" La tabla core_perfilusuario no existe")
            conn.close()
            return False
        
        # Verificar columnas actuales
        cursor.execute("PRAGMA table_info(core_perfilusuario)")
        columns = [row[1] for row in cursor.fetchall()]
        print(f" Columnas actuales: {columns}")
        
        if 'cargo_directiva' in columns:
            print(" La columna cargo_directiva ya existe")
            conn.close()
            return True
        
        # Añadir la columna
        print(" Añadiendo columna cargo_directiva...")
        cursor.execute("""
            ALTER TABLE core_perfilusuario 
            ADD COLUMN cargo_directiva VARCHAR(20) DEFAULT NULL
        """)
        
        conn.commit()
        print(" Columna añadida exitosamente")
        
        # Verificar que se añadió
        cursor.execute("PRAGMA table_info(core_perfilusuario)")
        columns_final = [row[1] for row in cursor.fetchall()]
        print(f" Columnas finales: {columns_final}")
        
        conn.close()
        return True
        
    except Exception as e:
        print(f" Error: {e}")
        return False

if __name__ == "__main__":
    print(" Arreglando base de datos...")
    if add_missing_column():
        print(" Base de datos arreglada. Reinicie el servidor.")
    else:
        print(" Error al arreglar la base de datos")
