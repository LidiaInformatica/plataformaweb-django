FROM python:3.12

ENV PYTHONUNBUFFERED 1
ENV DJANGO_SETTINGS_MODULE=plataformaweb.settings

WORKDIR /app

COPY requirements.txt /app/
RUN pip install --no-cache-dir -r requirements.txt

# Instalar dependencias de testing
RUN pip install --no-cache-dir pytest pytest-django pytest-cov

COPY . /app/

# Crear directorios necesarios
RUN mkdir -p /app/tests /app/docs/evidencias-RF01 /app/docs/evidencias-RF02

# Permisos para los directorios
RUN chmod -R 755 /app/tests /app/docs