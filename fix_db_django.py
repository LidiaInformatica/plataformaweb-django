#!/usr/bin/env python
"""
Management command para arreglar la base de datos
"""
import os
import sys
import django
from django.conf import settings
from django.core.management import execute_from_command_line

# Configurar Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'plataformaweb.settings')
django.setup()

from django.db import connection

def fix_database():
    """Arreglar la base de datos añadiendo la columna faltante"""
    try:
        with connection.cursor() as cursor:
            # Verificar si la columna existe
            cursor.execute("PRAGMA table_info(core_perfilusuario)")
            columns = [row[1] for row in cursor.fetchall()]
            print(f"Columnas actuales: {columns}")
            
            if 'cargo_directiva' not in columns:
                print("Añadiendo columna cargo_directiva...")
                cursor.execute("""
                    ALTER TABLE core_perfilusuario 
                    ADD COLUMN cargo_directiva VARCHAR(20)
                """)
                print("Columna añadida exitosamente")
            else:
                print("La columna cargo_directiva ya existe")
            
            # Verificar nuevamente
            cursor.execute("PRAGMA table_info(core_perfilusuario)")
            columns_final = [row[1] for row in cursor.fetchall()]
            print(f"Columnas finales: {columns_final}")
            
        return True
        
    except Exception as e:
        print(f"Error: {e}")
        return False

if __name__ == "__main__":
    if fix_database():
        print("Base de datos arreglada exitosamente")
        # Marcar la migración como aplicada
        try:
            from django.db.migrations.recorder import MigrationRecorder
            recorder = MigrationRecorder(connection)
            recorder.record_applied('core', '0002_add_cargo_directiva')
            print("Migración marcada como aplicada")
        except Exception as e:
            print(f"Error marcando migración: {e}")
    else:
        print("Error al arreglar la base de datos")
