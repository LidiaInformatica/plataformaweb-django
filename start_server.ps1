# ========================================
#    SCRIPT SIMPLE PARA INICIAR SERVIDOR
# ========================================

# Navegar al directorio del proyecto
Set-Location "c:\Users\Pc38\Downloads\plataformaweb-django"

# Activar entorno virtual
.\venv\Scripts\Activate.ps1

# Iniciar servidor
Write-Host "Iniciando servidor Django en http://127.0.0.1:8000..." -ForegroundColor Green
Write-Host "Presiona Ctrl+C para detener el servidor" -ForegroundColor Yellow
python manage.py runserver
