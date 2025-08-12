@echo off
echo ========================================
echo    COLEGIO ADVENTISTA TALCAHUANO CENTRO
echo    INICIANDO PROYECTO DJANGO
echo ========================================

echo.
echo 1. Navegando al directorio del proyecto...
cd /d "c:\Users\Pc38\Downloads\plataformaweb-django"

echo.
echo 2. Activando entorno virtual...
call .\venv\Scripts\activate.bat

echo.
echo 3. Creando usuario de acceso rapido...
python -c "import django,os; os.environ.setdefault('DJANGO_SETTINGS_MODULE','plataformaweb.settings'); django.setup(); from django.contrib.auth.models import User; u,created=User.objects.get_or_create(username='admin'); u.set_password('123'); u.is_superuser=True; u.is_staff=True; u.save(); print('Usuario: admin | Contraseña: 123')"

echo.
echo 4. Aplicando migraciones...
python manage.py migrate

echo.
echo ========================================
echo    PROYECTO LISTO PARA USAR
echo ========================================
echo.
echo 🎯 CREDENCIALES DE ACCESO:
echo Usuario: admin
echo Contraseña: 123
echo.
echo 🌐 ENLACES:
echo Principal: http://127.0.0.1:8000
echo Admin: http://127.0.0.1:8000/admin
echo.
echo Para iniciar servidor:
echo python manage.py runserver
echo.
pause
