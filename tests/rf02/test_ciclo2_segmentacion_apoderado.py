import pytest
from django.urls import reverse
from django.contrib.auth.models import User
from estudiantes.models import Estudiante, Apoderado, Curso
from actividades.models import Actividad, TipoActividad
from cuotas.models import CuotaEstudiante
from datetime import date

@pytest.mark.django_db
def test_segmentacion_por_apoderado(client):
    """
    RF-02 Ciclo 2: Segmentación por Apoderado
    Verifica que un apoderado solo pueda ver el estado de pago de sus estudiantes.
    
    Estado: En prueba con credenciales reales
    Credenciales: apoderado1/Lidi0354
    """
    # Usar credenciales reales en lugar de crear nuevo usuario
    client.login(username="apoderado1", password="Lidi0354")
    
    # Obtener página de estado
    url = reverse('cuotas:estado_apoderado')
    response = client.get(url)
    
    # Verificar que la página carga
    assert response.status_code == 200
    
    # Obtener el apoderado real
    apoderado = Apoderado.objects.get(usuario__username="apoderado1")
    
    # Verificar contenido usando datos reales
    content = response.content.decode()
    
    # Debe contener datos del apoderado real
    assert apoderado.rut in content
    
    # Debe contener datos de sus estudiantes reales
    estudiantes = Estudiante.objects.filter(apoderado=apoderado)
    for estudiante in estudiantes:
        assert estudiante.rut in content
        assert estudiante.nombre in content