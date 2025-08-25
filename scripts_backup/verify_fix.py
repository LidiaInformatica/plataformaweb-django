#!/usr/bin/env python
import os
import sys
import django
import sqlite3
from datetime import datetime

# Configurar Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'plataformaweb.settings')

def test_database():
    """Probar la base de datos directamente"""
    try:
        conn = sqlite3.connect('db.sqlite3')
        cursor = conn.cursor()
        
        # Verificar tabla y columnas
        cursor.execute("PRAGMA table_info(core_perfilusuario)")
        columns = [row[1] for row in cursor.fetchall()]
        
        result = {
            'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            'table_exists': 'core_perfilusuario' in [t[0] for t in cursor.execute("SELECT name FROM sqlite_master WHERE type='table'").fetchall()],
            'columns': columns,
            'cargo_directiva_exists': 'cargo_directiva' in columns,
            'total_columns': len(columns)
        }
        
        conn.close()
        return result
        
    except Exception as e:
        return {'error': str(e)}

def test_django_model():
    """Probar el modelo Django"""
    try:
        django.setup()
        from core.models import PerfilUsuario
        
        count = PerfilUsuario.objects.count()
        return {'django_model_works': True, 'profile_count': count}
        
    except Exception as e:
        return {'django_model_works': False, 'error': str(e)}

# Ejecutar pruebas
db_result = test_database()
django_result = test_django_model()

# Escribir resultados
with open('test_results.txt', 'w', encoding='utf-8') as f:
    f.write("=== RESULTADOS DE PRUEBA ===\n\n")
    f.write("Base de datos SQLite:\n")
    for key, value in db_result.items():
        f.write(f"  {key}: {value}\n")
    
    f.write("\nModelo Django:\n")
    for key, value in django_result.items():
        f.write(f"  {key}: {value}\n")
    
    if db_result.get('cargo_directiva_exists') and django_result.get('django_model_works'):
        f.write("\n✅ TODO FUNCIONANDO CORRECTAMENTE\n")
        f.write("El servidor debería iniciarse sin errores.\n")
    else:
        f.write("\n❌ PROBLEMAS DETECTADOS\n")
        f.write("Revise los errores arriba.\n")

print("Resultados guardados en test_results.txt")
