import pytest
from django.contrib.auth import get_user_model
from core.models import PerfilUsuario

@pytest.mark.django_db
def test_user_str():
    User = get_user_model()
    user = User.objects.create_user(username="lidia", password="admin123", first_name="Lidia", last_name="Inostroza")
    
    perfil = PerfilUsuario.objects.create(
        usuario=user,
        tipo_perfil="administrador",
        rut="12345678-9",
        telefono="987654321"
    )
    
    assert perfil.usuario.username == "lidia"
    assert str(perfil) == "Lidia Inostroza - Administrador del Sistema"



