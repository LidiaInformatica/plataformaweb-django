import pytest
from django.urls import reverse
from estudiantes.models import Apoderado, Estudiante, Curso
from core.models import Notificacion

@pytest.mark.django_db
def test_notificaciones_apoderado_segmentado(client, django_user_model):
    # Crear usuario y apoderado
    user = django_user_model.objects.create_user(username="apoderado_test", password="1234")
    apoderado = Apoderado.objects.create(
        usuario=user,
        nombre="Lidia",
        apellido_paterno="Inostroza",
        apellido_materno="Yañez",
        rut="12345678-9",
        telefono="123456789",
        email="apoderado@test.com"
    )

    # Crear curso y estudiante vinculado
    curso = Curso.objects.create(nombre="5° Básico", nivel="Básica", año=2023)
    estudiante = Estudiante.objects.create(
        nombre="Juanito",
        apellido_paterno="Pérez",
        apellido_materno="Gómez",
        rut="11111111-1",
        curso=curso,
        apoderado=apoderado,
        vinculo_apoderado="hijo",
        fecha_nacimiento="2010-01-01",
        activo=True
    )

    # Crear notificación vinculada al estudiante
    Notificacion.objects.create(
        estudiante=estudiante,
        mensaje="Prueba de notificación",
        titulo="Recordatorio",
        usuario_registra=user
    )

    # Login y acceso al dashboard
    client.login(username="apoderado_test", password="1234")
    response = client.get(reverse("core:dashboard_apoderado"))
    html = response.content.decode("utf-8")

    # Validaciones
    assert response.status_code == 200
    assert "Juanito" in html
    assert "Prueba de notificación" in html
    assert "Recordatorio" in html



