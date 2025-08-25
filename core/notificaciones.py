"""
Servicio de notificaciones por email
Sistema para enviar notificaciones automáticas a apoderados y administradores
"""
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.utils import timezone
from django.conf import settings
import logging

logger = logging.getLogger('core.notificaciones')

class ServicioNotificaciones:
    """Servicio centralizado para el envío de notificaciones por email"""
    
    @staticmethod
    def enviar_notificacion_nueva_actividad(actividad, email_admin=None):
        """
        Envía notificación cuando se crea una nueva actividad
        """
        try:
            # Email del administrador (por defecto el tuyo)
            destinatario = email_admin or settings.ADMIN_EMAIL
            
            # Crear el contexto para el template
            contexto = {
                'actividad': actividad,
                'fecha_actual': timezone.now().strftime('%d/%m/%Y %H:%M'),
                'url_actividad': f"http://127.0.0.1:8000/actividades/{actividad.id}/",
                'nombre_institucion': 'Colegio Adventista Talcahuano Centro'
            }
            
            # Generar el contenido HTML del email
            contenido_html = render_to_string('emails/nueva_actividad.html', contexto)
            contenido_texto = render_to_string('emails/nueva_actividad.txt', contexto)
            
            # Enviar el email
            resultado = send_mail(
                subject=f'Nueva Actividad Creada: {actividad.nombre}',
                message=contenido_texto,
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[destinatario],
                html_message=contenido_html,
                fail_silently=False
            )
            
            if resultado:
                logger.info(f"Notificación enviada exitosamente a {destinatario} para actividad {actividad.nombre}")
                
                # Guardar registro de la notificación
                from core.models import Notificacion
                notificacion = Notificacion.objects.create(
                    tipo='nueva_actividad',
                    titulo=f'Nueva Actividad Creada: {actividad.nombre}',
                    mensaje=contenido_texto,
                    email_destinatario=destinatario,
                    nombre_destinatario='Administrador',
                    estado='enviada',
                    fecha_envio=timezone.now(),
                    actividad_id=actividad.id
                )
                
                return True
            else:
                logger.error(f"Error al enviar notificación a {destinatario}")
                return False
                
        except Exception as e:
            logger.error(f"Error en envío de notificación: {str(e)}")
            
            # Guardar registro del error
            from core.models import Notificacion
            Notificacion.objects.create(
                tipo='nueva_actividad',
                titulo=f'Nueva Actividad Creada: {actividad.nombre}',
                mensaje=f'Error al enviar: {str(e)}',
                email_destinatario=destinatario,
                nombre_destinatario='Administrador',
                estado='fallida',
                error_envio=str(e),
                actividad_id=actividad.id
            )
            return False
    
    @staticmethod
    def enviar_recordatorio_pago(cuota, email_apoderado):
        """
        Envía recordatorio de pago a un apoderado
        """
        try:
            contexto = {
                'cuota': cuota,
                'estudiante': cuota.estudiante,
                'actividad': cuota.actividad,
                'fecha_vencimiento': cuota.fecha_vencimiento.strftime('%d/%m/%Y'),
                'monto_pendiente': cuota.saldo_pendiente(),
                'url_pago': f"http://127.0.0.1:8000/cuotas/{cuota.id}/",
            }
            
            contenido_html = render_to_string('emails/recordatorio_pago.html', contexto)
            contenido_texto = render_to_string('emails/recordatorio_pago.txt', contexto)
            
            resultado = send_mail(
                subject=f'Recordatorio de Pago - {cuota.actividad.nombre}',
                message=contenido_texto,
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[email_apoderado],
                html_message=contenido_html,
                fail_silently=False
            )
            
            if resultado:
                logger.info(f"Recordatorio de pago enviado a {email_apoderado}")
                return True
            else:
                logger.error(f"Error al enviar recordatorio a {email_apoderado}")
                return False
                
        except Exception as e:
            logger.error(f"Error en envío de recordatorio: {str(e)}")
            return False
    
    @staticmethod
    def crear_notificacion(tipo, titulo, mensaje, apoderado_email, datos_adicionales=None):
        """
        Crea una notificación en la base de datos sin enviar correo
        """
        from core.models import Notificacion, User

        try:
            usuario = User.objects.filter(email=apoderado_email).first()
            if not usuario:
                return None

            notificacion = Notificacion.objects.create(
                usuario_registra=usuario,
                apoderado_nombre=datos_adicionales.get('usuario', 'Desconocido'),
                apoderado_email=apoderado_email,
                titulo=titulo,
                mensaje=mensaje,
                tipo=tipo,
                estado='pendiente',
                fecha_creacion=timezone.now()
            )
            return notificacion

        except Exception as e:
            logger.error(f"Error al crear notificación: {str(e)}")
            return None
    
    @staticmethod
    def probar_notificacion_demo():
        """
        Envía un email de prueba para demostrar el funcionamiento
        """
        try:
            destinatario = settings.ADMIN_EMAIL
            
            contexto = {
                'fecha_actual': timezone.now().strftime('%d/%m/%Y %H:%M'),
                'mensaje_demo': 'Este es un email de prueba del sistema de notificaciones.',
                'funcionalidades': [
                    'Notificaciones automáticas al crear actividades',
                    'Recordatorios de pago a apoderados',
                    'Confirmaciones de pagos recibidos',
                    'Alertas de actividades vencidas'
                ]
            }
            
            # Para la demo, usaremos un template simple
            mensaje = f"""
¡Hola desde el Sistema de Gestión Escolar!

Este es un email de prueba enviado el {contexto['fecha_actual']}.

Funcionalidades implementadas:
• Notificaciones automáticas al crear actividades
• Recordatorios de pago a apoderados  
• Confirmaciones de pagos recibidos
• Alertas de actividades vencidas

El sistema está funcionando correctamente.

---
Colegio Adventista Talcahuano Centro
Sistema de Gestión Escolar
            """
            
            resultado = send_mail(
                subject='🎉 Sistema de Notificaciones - FUNCIONANDO',
                message=mensaje,
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[destinatario],
                fail_silently=False
            )
            
            if resultado:
                logger.info(f"Email de prueba enviado exitosamente a {destinatario}")
                return True
            else:
                logger.error(f"Error al enviar email de prueba")
                return False
                
        except Exception as e:
            logger.error(f"Error en email de prueba: {str(e)}")
            return False
