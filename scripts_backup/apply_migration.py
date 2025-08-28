#!/usr/bin/env python
"""
Script para aplicar la migración faltante usando Django ORM
"""
import os
import sys
import django

# Configurar Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'plataformaweb.settings')
django.setup()

from django.db import connection, transaction
from django.db.migrations.recorder import MigrationRecorder

def apply_migration():
    """Aplicar la migración de cargo_directiva manualmente"""
    
    print("🔧 Aplicando migración de cargo_directiva...")
    
    try:
        with connection.cursor() as cursor:
            # 1. Verificar si la columna existe
            cursor.execute("PRAGMA table_info(core_perfilusuario)")
            columns = [row[1] for row in cursor.fetchall()]
            print(f"Columnas actuales: {columns}")
            
            # 2. Añadir columna si no existe
            if 'cargo_directiva' not in columns:
                print("Añadiendo columna cargo_directiva...")
                cursor.execute("""
                    ALTER TABLE core_perfilusuario 
                    ADD COLUMN cargo_directiva VARCHAR(20) DEFAULT NULL
                """)
                print(" Columna añadida")
            else:
                print(" Columna ya existe")
            
            # 3. Marcar migración como aplicada
            recorder = MigrationRecorder(connection)
            if not recorder.migration_qs.filter(app='core', name='0002_add_cargo_directiva').exists():
                recorder.record_applied('core', '0002_add_cargo_directiva')
                print(" Migración marcada como aplicada")
            else:
                print(" Migración ya estaba marcada")
            
            # 4. Verificar que todo está OK
            cursor.execute("PRAGMA table_info(core_perfilusuario)")
            final_columns = [row[1] for row in cursor.fetchall()]
            print(f"Columnas finales: {final_columns}")
            
            if 'cargo_directiva' in final_columns:
                print(" ÉXITO: La columna cargo_directiva está disponible")
                return True
            else:
                print(" ERROR: La columna no se añadió correctamente")
                return False
                
    except Exception as e:
        print(f" Error: {e}")
        return False

if __name__ == "__main__":
    if apply_migration():
        print("\n MIGRACIÓN APLICADA EXITOSAMENTE")
        print("El servidor ya debería funcionar correctamente")
        print("Ejecute: python manage.py runserver")
    else:
        print("\n ERROR AL APLICAR LA MIGRACIÓN")
        sys.exit(1)
