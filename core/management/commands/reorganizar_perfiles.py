from django.core.management.base import BaseCommand
from django.contrib.auth.models import Group, User

class Command(BaseCommand):
    help = 'Reorganiza los grupos y perfiles de usuario manteniendo claves específicas'

    def handle(self, *args, **kwargs):
        # Configuración de usuarios con sus claves
        usuarios_config = {
            'Directiva': {
                'usuarios': [
                    {'username': 'Presidenta', 'password': 'directiva2025'},
                    {'username': 'Secretaria', 'password': 'directiva2025'},
                    {'username': 'Tesorera', 'password': 'directiva2025'}
                ]
            },
            'Apoderado': {
                'usuarios': [
                    {'username': 'apoderado1', 'password': 'Lidi0354'},
                    {'username': 'apoderado2', 'password': 'Lidi0354'},
                    {'username': 'apoderado3', 'password': 'Lidi0354'}
                ]
            }
        }

        for grupo_nombre, config in usuarios_config.items():
            grupo, creado = Group.objects.get_or_create(name=grupo_nombre)
            self.stdout.write(f"Grupo {grupo_nombre}: {'creado' if creado else 'existente'}")

            for user_data in config['usuarios']:
                usuario = User.objects.filter(username=user_data['username']).first()
                if usuario:
                    usuario.set_password(user_data['password'])
                    usuario.save()
                    usuario.groups.add(grupo)
                    self.stdout.write(f"Usuario {user_data['username']} actualizado en {grupo_nombre}")

        # Eliminar grupos obsoletos
        grupos_obsoletos = ['Presidenta', 'Tesorera', 'Secretaria']
        for grupo in grupos_obsoletos:
            Group.objects.filter(name=grupo).delete()

        self.stdout.write(self.style.SUCCESS('Reorganización completada con contraseñas actualizadas'))