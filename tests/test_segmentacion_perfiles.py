import pytest
from django.urls import reverse
from django.contrib.auth.models import User, Group
from core.models import PerfilUsuario

@pytest.mark.django_db
@pytest.mark.parametrize("username,password,tipo_perfil,expected_url", [
    ("apoderado1", "Lidi0354", "apoderado", "/dashboard/apoderado/"),
    ("apoderado2", "Lidi0354", "apoderado", "/dashboard/apoderado/"),
    ("apoderado3", "Lidi0354", "apoderado", "/dashboard/apoderado/"),
    ("presidenta", "directiva2025", "directiva", "/dashboard/directiva/"),
    ("secretaria", "directiva2025", "directiva", "/dashboard/directiva/"),
    ("tesorera", "directiva2025", "directiva", "/dashboard/directiva/"),
    ("Lidia", "admin123", "admin", "/dashboard/admin/"),
])
def test_redireccion_por_perfil(client, username, password, tipo_perfil, expected_url):
    user = User.objects.create_user(username=username, password=password)
    PerfilUsuario.objects.create(usuario=user, tipo_perfil=tipo_perfil)

    # Opcional: asociar grupo si lo usas en tus vistas
    group, _ = Group.objects.get_or_create(name=tipo_perfil)
    user.groups.add(group)

    response = client.post(reverse("login"), {
        "username": username,
        "password": password
    })

    assert response.status_code == 302
    assert response.url == expected_url



