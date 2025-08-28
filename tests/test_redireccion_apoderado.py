import pytest
from django.contrib.auth.models import Group
from core.models import PerfilUsuario

@pytest.mark.django_db
def test_redireccion_apoderado(client, django_user_model):
    apoderado_group = Group.objects.create(name='Apoderado')
    user = django_user_model.objects.create_user(username='apoderado2', password='test123')
    user.groups.add(apoderado_group)

    # Crear perfil asociado
    PerfilUsuario.objects.create(usuario=user, rut='apoderado2', tipo_perfil='apoderado')

    response = client.post('/accounts/login/', {'username': 'apoderado2', 'password': 'test123'})
    assert response.status_code == 302
    assert response.url == '/dashboard/apoderado/'



