# ========================================
#    SCRIPT PARA CREAR SUPERUSUARIO
# ========================================

Write-Host "Creando superusuario para Django..." -ForegroundColor Green

# Navegar al directorio del proyecto
Set-Location "C:\plataformaweb-django"

# Activar entorno virtual
.\venv\Scripts\Activate.ps1

# Crear superusuario
Write-Host "Ingresa los datos para el superusuario:" -ForegroundColor Yellow
python manage.py createsuperuser

Write-Host ""
Write-Host "========================================" -ForegroundColor Green
Write-Host "   SUPERUSUARIO CREADO EXITOSAMENTE" -ForegroundColor Green
Write-Host "========================================" -ForegroundColor Green
Write-Host ""
Write-Host "Ahora puedes:" -ForegroundColor Cyan
Write-Host "1. Iniciar el servidor: python manage.py runserver" -ForegroundColor White
Write-Host "2. Acceder al admin en: http://127.0.0.1:8000/admin" -ForegroundColor White
Write-Host ""
