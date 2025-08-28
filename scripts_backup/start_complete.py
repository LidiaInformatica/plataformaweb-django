#!/usr/bin/env python
"""
Script de inicio completo que verifica todo antes de iniciar el servidor
"""
import os
import sys
import subprocess

def run_command(command, description):
    """Ejecutar comando y mostrar resultado"""
    print(f" {description}...")
    try:
        result = subprocess.run(command, shell=True, capture_output=True, text=True)
        if result.returncode == 0:
            print(f" {description} - OK")
            if result.stdout.strip():
                print(f"   {result.stdout.strip()}")
            return True
        else:
            print(f" {description} - ERROR")
            if result.stderr.strip():
                print(f"   {result.stderr.strip()}")
            return False
    except Exception as e:
        print(f" {description} - EXCEPCIÓN: {e}")
        return False

def main():
    print(" INICIANDO SISTEMA DJANGO")
    print("=" * 40)
    
    # 1. Verificar Pillow
    if not run_command('python -c "import PIL; print(f\'Pillow {PIL.__version__} instalado\')"', "Verificar Pillow"):
        print("Instalando Pillow...")
        run_command("python -m pip install Pillow", "Instalar Pillow")
    
    # 2. Aplicar migraciones
    run_command("python manage.py migrate", "Aplicar migraciones")
    
    # 3. Ejecutar script de emergencia
    run_command("python apply_migration.py", "Aplicar migración cargo_directiva")
    
    # 4. Crear usuario admin
    run_command("python crear_admin.py", "Crear usuario admin")
    
    # 5. Verificar sistema
    if run_command("python manage.py check", "Verificar sistema"):
        print("\n SISTEMA LISTO")
        print("Credenciales de acceso:")
        print("  Usuario: admin")
        print("  Contraseña: admin123")
        print("  URL: http://127.0.0.1:8000")
        print("\nPara iniciar el servidor ejecute:")
        print("  python manage.py runserver")
    else:
        print("\n HAY ERRORES EN EL SISTEMA")
        print("Revise los mensajes anteriores")

if __name__ == "__main__":
    main()
