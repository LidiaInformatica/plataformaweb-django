#!/usr/bin/env python
"""
Script para recrear la base de datos completamente
"""
import os
import shutil
import sqlite3

# Hacer backup de la base de datos actual
if os.path.exists('db.sqlite3'):
    shutil.copy2('db.sqlite3', 'db_backup.sqlite3')
    print("Backup de la base de datos creado: db_backup.sqlite3")

# Eliminar la base de datos actual
if os.path.exists('db.sqlite3'):
    os.remove('db.sqlite3')
    print("Base de datos actual eliminada")

print("Ahora ejecute: python manage.py migrate")
print("Luego: python manage.py createsuperuser")
