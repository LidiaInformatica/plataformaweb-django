from django.core.management.base import BaseCommand
from django.contrib.auth.models import User, Group
from core.models import PerfilUsuario

class Command(BaseCommand):
    help = 'Configura los usuarios del sistema con sus perfiles y grupos'

    def handle(self, *args, **kwargs):
        self.stdout.write("Configurando usuarios del admin de Django...")
        self.stdout.write("=" * 60)
        
        # Configuración específica de usuarios
        configuraciones = [
            {
                'username': 'Lidia',
                'tipo_perfil': 'administrador',
                'grupos': [],
                'is_superuser': True
            },
            # ...resto de las configuraciones...
        ]

        # Resto del código existente pero usando self.stdout.write en lugar de print
        # ...

        self.stdout.write(self.style.SUCCESS("\nConfiguración completada exitosamente!"))