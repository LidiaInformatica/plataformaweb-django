from estudiantes.models import Apoderado, Estudiante
from core.models import Notificacion
import pytest

@pytest.mark.django_db
def test_notificaciones_apoderado(client, django_user_model):
    user = django_user_model.objects.create_user(username="apoderado_test", password="1234")
    apoderado = Apoderado.objects.create(user=user)
    estudiante = Estudiante.objects.create(apoderado=apoderado, nombre="Juanito")
    Notificacion.objects.create(estudiante=estudiante, mensaje="Prueba")

    client.login(username="apoderado_test", password="1234")
    response = client.get("/dashboard/apoderado/")
    assert "Prueba" in response.content.decode()
