from django.core.management.base import BaseCommand
from django.db import connection

class Command(BaseCommand):
    help = 'Arregla la base de datos añadiendo la columna cargo_directiva'

    def handle(self, *args, **options):
        try:
            with connection.cursor() as cursor:
                # Verificar si la columna existe
                cursor.execute("PRAGMA table_info(core_perfilusuario)")
                columns = [row[1] for row in cursor.fetchall()]
                self.stdout.write(f"Columnas actuales: {columns}")
                
                if 'cargo_directiva' not in columns:
                    self.stdout.write("Añadiendo columna cargo_directiva...")
                    cursor.execute("""
                        ALTER TABLE core_perfilusuario 
                        ADD COLUMN cargo_directiva VARCHAR(20)
                    """)
                    self.stdout.write(
                        self.style.SUCCESS('Columna cargo_directiva añadida exitosamente')
                    )
                else:
                    self.stdout.write(
                        self.style.WARNING('La columna cargo_directiva ya existe')
                    )
                
                # Verificar nuevamente
                cursor.execute("PRAGMA table_info(core_perfilusuario)")
                columns_final = [row[1] for row in cursor.fetchall()]
                self.stdout.write(f"Columnas finales: {columns_final}")
                
        except Exception as e:
            self.stdout.write(
                self.style.ERROR(f'Error: {e}')
            )
