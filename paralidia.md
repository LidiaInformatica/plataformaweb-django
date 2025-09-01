- Detener y limpiar contenedores anteriores
docker compose down --volumes --remove-orphans

- Reconstruir la imagen
docker compose build

- Levantar el contenedor
docker compose up -d

- Verificar que todo este corriendo correctamente
docker ps
docker inspect plataformaweb-django

- Entrar a la shell del contenedor
docker exec -it plataformaweb-django bash

- Ejecutar comandos Django sin entrar a la Shell
docker exec -it plataformaweb-django python manage.py migrate
docker exec -it plataformaweb-django python manage.py createsuperuser

- Ver logs del contenedor
docker logs -f plataformaweb-django

- Mostrar logs en tiempo real
docker compose logs -f plataformaweb-django

- Reconstruir la imagen
docker compose build
docker compose up -d --force-recreate

- Validar sqlite desde el contenedor dentro de la shell
sqlite3 db.sqlite3
- Ver todas las tablas
.tables
- Ver estructura de una tabla
.schema ej: estudiantes_estudiante


- Detener Docker Compose
docker-compose down

- Activar entorno Virtual Local
venv/Scripts/activate.bat


- Levantar ambiente virtual desde Local

- Clonar el repositorio
git clone https://github.com/LidiaInformatica/plataformaweb-django.git
cd plataformaweb-django

-Crear entorno virtual local
python -m venv venv
venv\Scripts\activate 
pip install -r requirements.txt








