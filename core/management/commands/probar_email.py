"""
Comando personalizado para probar el sistema de notificaciones
"""
from django.core.management.base import BaseCommand
from core.notificaciones import ServicioNotificaciones

class Command(BaseCommand):
    help = 'Envía un email de prueba para demostrar el sistema de notificaciones'
    
    def handle(self, *args, **options):
        self.stdout.write(' Enviando email de prueba...')
        
        try:
            resultado = ServicioNotificaciones.probar_notificacion_demo()
            
            if resultado:
                self.stdout.write(
                    self.style.SUCCESS(' Email de prueba enviado exitosamente!')
                )
                self.stdout.write(' Revisa tu bandeja de entrada: lidia.inostroza18@gmail.com')
            else:
                self.stdout.write(
                    self.style.ERROR(' Error al enviar el email de prueba')
                )
                
        except Exception as e:
            self.stdout.write(
                self.style.ERROR(f' Error: {str(e)}')
            )
