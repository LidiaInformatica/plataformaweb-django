import pytest
from django.urls import reverse
from django.contrib.auth.models import User
from estudiantes.models import Apoderado, Estudiante, Curso
from datetime import date

@pytest.mark.django_db
def test_segmentacion_por_apoderado(client):
    user = User.objects.create_user(username="apoderado2", password="Lidi0354")
    apoderado = Apoderado.objects.create(usuario=user, nombre="Apoderado Dos", rut="2-7")
    curso = Curso.objects.create(nombre="4° Medio", nivel="Enseñanza Media", año=2025)
    estudiante = Estudiante.objects.create(
        nombre="Hijo Uno",
        apellido_paterno="Apellido",
        apellido_materno="Apellido",
        rut="11.111.111-1",
        apoderado=apoderado,
        curso=curso,
        fecha_nacimiento=date(2010, 5, 1)
    )

    assert client.login(username="apoderado2", password="Lidi0354")

    url = reverse('cuotas:estado_apoderado')
    response = client.get(url)
    assert response.status_code == 200