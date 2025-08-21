# syntax=docker/dockerfile:1
FROM python:3.12
WORKDIR /app
COPY . /app
RUN pip install --upgrade pip && pip install -r requirements.txt

# Comando para iniciar el servidor Django
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]

