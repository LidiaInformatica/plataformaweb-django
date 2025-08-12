# ========================================
#    SCRIPT PARA INICIAR PROYECTO DJANGO
# ========================================

Write-Host "Iniciando proyecto Django..." -ForegroundColor Green

# 1. Navegar al directorio del proyecto
Set-Location "C:\plataformaweb-django"

# 2. Verificar si existe el entorno virtual
if (!(Test-Path ".\venv")) {
    Write-Host "Creando entorno virtual..." -ForegroundColor Yellow
    python -m venv venv
}

# 3. Activar entorno virtual
Write-Host "Activando entorno virtual..." -ForegroundColor Yellow
.\venv\Scripts\Activate.ps1

# 4. Verificar e instalar dependencias si no están instaladas
Write-Host "Verificando instalación de Django..." -ForegroundColor Yellow
$djangoInstalled = python -c "try: import django; print('True'); except ImportError: print('False')" 2>$null

if ($djangoInstalled -eq "False") {
    Write-Host "Instalando Django..." -ForegroundColor Yellow
    pip install Django==4.2.7
    pip install python-decouple==3.8
}

Write-Host "Verificando instalación de Pillow..." -ForegroundColor Yellow
$pillowInstalled = python -c "try: import PIL; print('True'); except ImportError: print('False')" 2>$null

if ($pillowInstalled -eq "False") {
    Write-Host "Instalando Pillow para soporte de imágenes..." -ForegroundColor Yellow
    pip install Pillow
}

# 5. Crear y aplicar migraciones
Write-Host "Creando migraciones personalizadas..." -ForegroundColor Yellow
python manage.py makemigrations core --noinput 2>$null
python manage.py makemigrations estudiantes --noinput 2>$null
python manage.py makemigrations actividades --noinput 2>$null
python manage.py makemigrations cuotas --noinput 2>$null
python manage.py makemigrations accounts --noinput 2>$null

Write-Host "Aplicando migraciones..." -ForegroundColor Yellow
python manage.py migrate

# 6. Crear usuarios de prueba
Write-Host "Creando usuarios de prueba..." -ForegroundColor Yellow
python crear_usuarios_rapido.py 2>$null

# 7. Mensaje de información
Write-Host "========================================" -ForegroundColor Green
Write-Host "   COLEGIO ADVENTISTA TALCAHUANO CENTRO" -ForegroundColor Green
Write-Host "   PROYECTO DJANGO CONFIGURADO" -ForegroundColor Green
Write-Host "========================================" -ForegroundColor Green
Write-Host ""
Write-Host "🎯 CREDENCIALES QUE FUNCIONAN:" -ForegroundColor Cyan
Write-Host "Usuario: colegio" -ForegroundColor White
Write-Host "Contraseña: 123" -ForegroundColor White
Write-Host ""
Write-Host "🌐 ENLACES DIRECTOS:" -ForegroundColor Cyan
Write-Host "Sistema Principal: http://127.0.0.1:8000" -ForegroundColor White
Write-Host "Panel Admin: http://127.0.0.1:8000/admin" -ForegroundColor White
Write-Host "Login: http://127.0.0.1:8000/accounts/login/" -ForegroundColor White
Write-Host ""
Write-Host "Para iniciar el servidor ejecuta:" -ForegroundColor Cyan
Write-Host "python manage.py runserver" -ForegroundColor White
Write-Host ""

# 8. Preguntar si quiere iniciar el servidor
$iniciarServidor = Read-Host "¿Quieres iniciar el servidor ahora? (s/n)"
if ($iniciarServidor -eq "s" -or $iniciarServidor -eq "S" -or $iniciarServidor -eq "si" -or $iniciarServidor -eq "Si") {
    Write-Host "Iniciando servidor en http://127.0.0.1:8000..." -ForegroundColor Green
    Write-Host "Usa las credenciales mostradas arriba para acceder" -ForegroundColor Yellow
    python manage.py runserver
}
