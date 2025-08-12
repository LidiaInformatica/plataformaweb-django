# Script para mover proyecto a C:\
Write-Host "Moviendo proyecto de Descargas a C:\" -ForegroundColor Green

$origenPath = "C:\Users\Pc38\Downloads\plataformaweb-django"
$destinoPath = "C:\plataformaweb-django"

# Verificar que existe el proyecto original
if (!(Test-Path $origenPath)) {
    Write-Host "No se encuentra el proyecto en: $origenPath" -ForegroundColor Red
    exit 1
}

# Crear directorio destino
Write-Host "Creando directorio destino..." -ForegroundColor Yellow
if (!(Test-Path $destinoPath)) {
    New-Item -ItemType Directory -Path $destinoPath -Force | Out-Null
    Write-Host "Directorio creado: $destinoPath" -ForegroundColor Green
} else {
    Write-Host "El directorio ya existe: $destinoPath" -ForegroundColor Yellow
}

# Copiar archivos usando xcopy
Write-Host "Copiando archivos..." -ForegroundColor Yellow
$comando = "xcopy `"$origenPath`" `"$destinoPath`" /E /H /C /I /Y"
Invoke-Expression $comando

if ($LASTEXITCODE -eq 0) {
    Write-Host "Archivos copiados exitosamente" -ForegroundColor Green
} else {
    Write-Host "Error al copiar archivos" -ForegroundColor Red
    exit 1
}

# Verificar archivos importantes
$archivosImportantes = @("manage.py", "requirements.txt", "db.sqlite3")
foreach ($archivo in $archivosImportantes) {
    if (Test-Path "$destinoPath\$archivo") {
        Write-Host "$archivo - OK" -ForegroundColor Green
    } else {
        Write-Host "$archivo - FALTA" -ForegroundColor Red
    }
}

Write-Host ""
Write-Host "MIGRACION COMPLETADA" -ForegroundColor Green
Write-Host ""
Write-Host "Proximos pasos:" -ForegroundColor Cyan
Write-Host "1. cd C:\plataformaweb-django" -ForegroundColor White
Write-Host "2. .\venv\Scripts\Activate.ps1" -ForegroundColor White
Write-Host "3. python manage.py runserver" -ForegroundColor White
