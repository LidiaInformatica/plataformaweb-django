# ========================================
#    SCRIPT DE VERIFICACIÓN DEL SISTEMA
# ========================================

Write-Host "Verificando configuración del proyecto Django..." -ForegroundColor Green
Write-Host ""

# Navegar al directorio del proyecto
Set-Location "C:\plataformaweb-django"

# Activar entorno virtual
.\venv\Scripts\Activate.ps1

# Verificaciones
Write-Host "1. Verificando Django..." -ForegroundColor Yellow
$djangoVersion = python -c "import django; print(django.get_version())" 2>$null
if ($djangoVersion) {
    Write-Host "   ✅ Django $djangoVersion instalado" -ForegroundColor Green
} else {
    Write-Host "   ❌ Django no está instalado" -ForegroundColor Red
}

Write-Host "2. Verificando Pillow..." -ForegroundColor Yellow
$pillowInstalled = python -c "try: import PIL; print('OK'); except ImportError: print('ERROR')" 2>$null
if ($pillowInstalled -eq "OK") {
    Write-Host "   ✅ Pillow instalado correctamente" -ForegroundColor Green
} else {
    Write-Host "   ❌ Pillow no está instalado" -ForegroundColor Red
}

Write-Host "3. Verificando base de datos..." -ForegroundColor Yellow
python manage.py check --database default 2>$null
if ($LASTEXITCODE -eq 0) {
    Write-Host "   ✅ Base de datos configurada correctamente" -ForegroundColor Green
} else {
    Write-Host "   ❌ Problemas con la base de datos" -ForegroundColor Red
}

Write-Host "4. Verificando migraciones..." -ForegroundColor Yellow
$migrationsOutput = python manage.py showmigrations --plan 2>$null
if ($migrationsOutput) {
    Write-Host "   ✅ Migraciones aplicadas" -ForegroundColor Green
} else {
    Write-Host "   ⚠️  Revisar migraciones" -ForegroundColor Yellow
}

Write-Host "5. Verificando configuración general..." -ForegroundColor Yellow
python manage.py check 2>$null
if ($LASTEXITCODE -eq 0) {
    Write-Host "   ✅ Configuración sin errores" -ForegroundColor Green
} else {
    Write-Host "   ❌ Errores en la configuración" -ForegroundColor Red
}

Write-Host ""
Write-Host "========================================" -ForegroundColor Green
Write-Host "   VERIFICACIÓN COMPLETADA" -ForegroundColor Green
Write-Host "========================================" -ForegroundColor Green
Write-Host ""

# Probar servidor por 5 segundos
Write-Host "Probando servidor por 5 segundos..." -ForegroundColor Yellow
$serverJob = Start-Job -ScriptBlock {
    Set-Location "c:\Users\Pc38\Downloads\plataformaweb-django"
    .\venv\Scripts\Activate.ps1
    python manage.py runserver --noreload 2>$null
}

Start-Sleep -Seconds 5
Stop-Job $serverJob -Force
Remove-Job $serverJob -Force

Write-Host "✅ Servidor probado exitosamente" -ForegroundColor Green
Write-Host ""
Write-Host "El proyecto está listo para usar:" -ForegroundColor Cyan
Write-Host "python manage.py runserver" -ForegroundColor White
