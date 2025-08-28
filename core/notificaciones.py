"""
Servicio de notificaciones por email
Sistema para enviar notificaciones automáticas a apoderados y administradores
"""
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.template import TemplateDoesNotExist
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
            destinatario = email_admin or settings.ADMIN_EMAIL

            contexto = {
                'actividad': actividad,
                'fecha_actual': timezone.now().strftime('%d/%m/%Y %H:%M'),
                'url_actividad': f"http://127.0.0.1:8000/actividades/{actividad.id}/",
                'nombre_institucion': 'Colegio Adventista Talcahuano Centro'
            }

            try:
                contenido_html = render_to_string('emails/nueva_actividad.html', contexto)
                contenido_texto = render_to_string('emails/nueva_actividad.txt', contexto)
            except TemplateDoesNotExist as e:
                logger.warning(f"Plantilla no encontrada: {str(e)}")
                contenido_texto = f"Nueva actividad creada: {actividad.nombre}"
                contenido_html = None

            resultado = send_mail(
                subject=f'Nueva Actividad Creada: {actividad.nombre}',
                message=contenido_texto,
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[destinatario],
                html_message=contenido_html,
                fail_silently=False
            )

            from core.models import Notificacion
            estado = 'enviada' if resultado else 'fallida'

            Notificacion.objects.create(
                tipo='nueva_actividad',
                titulo=f'Nueva Actividad Creada: {actividad.nombre}',
                mensaje=contenido_texto,
                apoderado_email=destinatario,
                apoderado_nombre='Administrador',
                estado=estado,
                fecha_creacion=timezone.now(),
                actividad_id=actividad.id,
                error_envio=None if resultado else 'Error al enviar email'
            )

            return resultado

        except Exception as e:
            logger.error(f"Error en envío de notificación: {str(e)}")
            from core.models import Notificacion
            Notificacion.objects.create(
                tipo='nueva_actividad',
                titulo=f'Nueva Actividad Creada: {actividad.nombre}',
                mensaje=f'Error al enviar: {str(e)}',
                apoderado_email=destinatario,
                apoderado_nombre='Administrador',
                estado='fallida',
                fecha_creacion=timezone.now(),
                actividad_id=actividad.id,
                error_envio=str(e)
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

            try:
                contenido_html = render_to_string('emails/recordatorio_pago.html', contexto)
                contenido_texto = render_to_string('emails/recordatorio_pago.txt', contexto)
            except TemplateDoesNotExist as e:
                logger.warning(f"Plantilla no encontrada: {str(e)}")
                contenido_texto = f"Recordatorio de pago pendiente para actividad {cuota.actividad.nombre}"
                contenido_html = None

            resultado = send_mail(
                subject=f'Recordatorio de Pago - {cuota.actividad.nombre}',
                message=contenido_texto,
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[email_apoderado],
                html_message=contenido_html,
                fail_silently=False
            )

            return resultado

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
        Envía un email de prueba y registra la notificación en la base de datos
        """
        try:
            destinatario = settings.ADMIN_EMAIL
            fecha_actual = timezone.now().strftime('%d/%m/%Y %H:%M')

            mensaje = f"""
¡Hola desde el Sistema de Gestión Escolar!

Este es un email de prueba enviado el {fecha_actual}.

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

            from core.models import Notificacion
            Notificacion.objects.create(
                tipo='demo',
                titulo='Email de prueba enviado',
                mensaje=mensaje,
                apoderado_email=destinatario,
                apoderado_nombre='Administrador',
                estado='enviada' if resultado else 'fallida',
                fecha_creacion=timezone.now(),
                error_envio=None if resultado else 'Error al enviar email de prueba'
            )

            return resultado

        except Exception as e:
            logger.error(f"Error en email de prueba: {str(e)}")
            return False

