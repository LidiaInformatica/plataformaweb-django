import sqlite3

# Conectar a la base de datos
conn = sqlite3.connect('db.sqlite3')
cursor = conn.cursor()

try:
    # Verificar columnas actuales
    cursor.execute("PRAGMA table_info(core_perfilusuario)")
    columns = [row[1] for row in cursor.fetchall()]
    print("Columnas actuales:", columns)
    
    # Añadir columna si no existe
    if 'cargo_directiva' not in columns:
        cursor.execute("ALTER TABLE core_perfilusuario ADD COLUMN cargo_directiva VARCHAR(20)")
        conn.commit()
        print("Columna cargo_directiva añadida exitosamente")
    else:
        print("La columna ya existe")
    
    # Verificar columnas finales
    cursor.execute("PRAGMA table_info(core_perfilusuario)")
    columns_final = [row[1] for row in cursor.fetchall()]
    print("Columnas finales:", columns_final)
    
except Exception as e:
    print(f"Error: {e}")
finally:
    conn.close()
