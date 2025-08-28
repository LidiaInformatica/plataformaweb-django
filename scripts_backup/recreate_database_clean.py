#!/usr/bin/env python
"""
Script para recrear la base de datos completa
"""
import os
import shutil

def recreate_database():
    """Recrear la base de datos desde cero"""
    
    print(" RECREANDO BASE DE DATOS COMPLETA")
    print("=" * 40)
    
    # 1. Hacer backup
    if os.path.exists('db.sqlite3'):
        timestamp = __import__('datetime').datetime.now().strftime('%Y%m%d_%H%M%S')
        backup_name = f'db_backup_{timestamp}.sqlite3'
        shutil.copy2('db.sqlite3', backup_name)
        print(f" Backup creado: {backup_name}")
        
        # Eliminar base de datos actual
        os.remove('db.sqlite3')
        print(" Base de datos actual eliminada")
    
    print("\n INSTRUCCIONES:")
    print("1. Ejecute: python manage.py migrate")
    print("2. Ejecute: python manage.py createsuperuser")
    print("3. Use username: admin, password: admin123")
    print("4. Ejecute: python manage.py runserver")
    
    return True

if __name__ == "__main__":
    recreate_database()
