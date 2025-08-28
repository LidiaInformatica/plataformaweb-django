import sqlite3
import os

def recreate_table():
    """Recrear la tabla con todas las columnas necesarias"""
    
    if not os.path.exists('db.sqlite3'):
        print("No hay base de datos")
        return
    
    conn = sqlite3.connect('db.sqlite3')
    cursor = conn.cursor()
    
    try:
        # Obtener datos existentes
        cursor.execute("SELECT id, usuario_id, tipo_perfil, rut, telefono, fecha_creacion FROM core_perfilusuario")
        existing_data = cursor.fetchall()
        print(f"Respaldando {len(existing_data)} registros")
        
        # Eliminar tabla existente
        cursor.execute("DROP TABLE core_perfilusuario")
        
        # Crear tabla nueva con todas las columnas
        cursor.execute("""
            CREATE TABLE core_perfilusuario (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                usuario_id INTEGER NOT NULL UNIQUE,
                tipo_perfil VARCHAR(20) NOT NULL,
                cargo_directiva VARCHAR(20) NULL,
                rut VARCHAR(12) NOT NULL UNIQUE,
                telefono VARCHAR(15) NOT NULL,
                fecha_creacion DATETIME NOT NULL,
                FOREIGN KEY (usuario_id) REFERENCES auth_user (id)
            )
        """)
        
        # Restaurar datos
        for record in existing_data:
            cursor.execute("""
                INSERT INTO core_perfilusuario 
                (id, usuario_id, tipo_perfil, cargo_directiva, rut, telefono, fecha_creacion)
                VALUES (?, ?, ?, NULL, ?, ?, ?)
            """, record)
        
        conn.commit()
        print(" Tabla recreada exitosamente")
        
        # Verificar
        cursor.execute("PRAGMA table_info(core_perfilusuario)")
        columns = [row[1] for row in cursor.fetchall()]
        print(f"Columnas: {columns}")
        
    except Exception as e:
        print(f"Error: {e}")
        conn.rollback()
    finally:
        conn.close()

if __name__ == "__main__":
    recreate_table()
