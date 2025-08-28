# ========================================
#    SCRIPT PARA MOVER PROYECTO A C:\
# ========================================

Write-Host "Moviendo proyecto de Descargas a C:\" -ForegroundColor Green
Write-Host ""

$origenPath = "C:\Users\Pc38\Downloads\plataformaweb-django"
$destinoPath = "C:\plataformaweb-django"

# 1. Verificar que existe el proyecto original
if (!(Test-Path $origenPath)) {
    Write-Host " No se encuentra el proyecto en: $origenPath" -ForegroundColor Red
    exit 1
}

# 2. Crear directorio destino
Write-Host " Creando directorio destino..." -ForegroundColor Yellow
if (!(Test-Path $destinoPath)) {
    New-Item -ItemType Directory -Path $destinoPath -Force | Out-Null
    Write-Host " Directorio creado: $destinoPath" -ForegroundColor Green
} else {
    Write-Host "  El directorio ya existe: $destinoPath" -ForegroundColor Yellow
}

# 3. Copiar archivos
Write-Host " Copiando archivos..." -ForegroundColor Yellow
try {
    # Usar robocopy para una copia más robusta
    robocopy $origenPath $destinoPath /E /Z /MT:8 /R:3 /W:1 /TBD /NP /NDL
    Write-Host " Archivos copiados exitosamente" -ForegroundColor Green
} catch {
    Write-Host " Error al copiar archivos: $_" -ForegroundColor Red
    exit 1
}

# 4. Verificar que se copiaron los archivos importantes
$archivosImportantes = @("manage.py", "requirements.txt", "db.sqlite3")
foreach ($archivo in $archivosImportantes) {
    if (Test-Path "$destinoPath\$archivo") {
        Write-Host " $archivo - OK" -ForegroundColor Green
    } else {
        Write-Host " $archivo - FALTA" -ForegroundColor Red
    }
}

Write-Host ""
Write-Host " MIGRACIÓN COMPLETADA" -ForegroundColor Green
Write-Host ""
Write-Host "Próximos pasos:" -ForegroundColor Cyan
Write-Host "1. Navegar a la nueva ubicación: cd C:\plataformaweb-django" -ForegroundColor White
Write-Host "2. Activar entorno virtual: .\venv\Scripts\Activate.ps1" -ForegroundColor White
Write-Host "3. Probar el servidor: python manage.py runserver" -ForegroundColor White
Write-Host ""
Write-Host "Opcional: Eliminar carpeta original después de verificar que todo funciona" -ForegroundColor Yellow
