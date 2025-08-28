# registrar_pago_benjamin.py
import os
import django
from datetime import datetime

# Configurar Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'plataformaweb.settings')
django.setup()

from estudiantes.models import Estudiante
from actividades.models import Actividad
from cuotas.models import CuotaEstudiante, PagoCuota
from core.notificaciones import ServicioNotificaciones
from django.contrib.auth.models import User

def registrar_pago_benjamin():
    """Registra un pago para Benjamín y envía notificación a Lidia"""
    
    print(" Buscando a Benjamín en la base de datos...")
    
    # Buscar a Benjamín
    try:
        benjamin = Estudiante.objects.get(rut='22497710-7')
        print(f" Benjamín encontrado: {benjamin.nombre} {benjamin.apellido_paterno}")
    except Estudiante.DoesNotExist:
        print(" Benjamín no encontrado")
        return
    
    # Buscar una actividad
    try:
        actividad = Actividad.objects.first()
        print(f" Actividad encontrada: {actividad.nombre}")
    except:
        print(" No hay actividades disponibles")
        return
    
    # Buscar al usuario Lidia
    try:
        lidia = User.objects.get(email='lidia.inostroza18@gmail.com')
        print(f" Usuario Lidia encontrado: {lidia.username}")
    except User.DoesNotExist:
        print(" Usuario Lidia no encontrado")
        return
    
    # Crear una cuota para Benjamín si no existe
    cuota, created = CuotaEstudiante.objects.get_or_create(
        estudiante=benjamin,
        actividad=actividad,
        defaults={
            'monto_total': actividad.monto_por_estudiante,
            'monto_pagado': 0,
            'estado': 'pendiente',
            'fecha_vencimiento': actividad.fecha_fin
        }
    )
    
    if created:
        print(f" Nueva cuota creada para {benjamin.nombre}: ${actividad.monto_por_estudiante}")
    else:
        print(f" Cuota existente encontrada: ${cuota.monto_total}")
    
    # Registrar el pago
    pago = PagoCuota.objects.create(
        cuota=cuota,
        monto=actividad.monto_por_estudiante,
        metodo_pago='transferencia',
        comprobante='COMP-BENJAMIN-001',
        observacion='Pago registrado automáticamente para prueba de notificaciones'
    )
    
    print(f" Pago registrado: ${pago.monto} por {pago.metodo_pago}")
    
    # Actualizar la cuota
    cuota.monto_pagado = actividad.monto_por_estudiante
    cuota.estado = 'pagado'
    cuota.save()
    
    print(" Cuota marcada como pagada")
    
    # Enviar notificación
    servicio = ServicioNotificaciones()
    
    try:
        # Usar el método de recordatorio de pago con los parámetros correctos
        resultado = servicio.enviar_recordatorio_pago(cuota, 'lidia.inostroza18@gmail.com')
        
        if resultado:
            print(f" Notificación enviada exitosamente")
            print(f" Email enviado a: lidia.inostroza18@gmail.com")
            print(f" Cuota notificada: ${cuota.monto_total}")
        else:
            print(" Error al enviar la notificación")
        
    except Exception as e:
        print(f" Error al enviar notificación: {str(e)}")
    
    print("\n ¡Proceso completado! Revisa tu email y el dashboard.")

if __name__ == "__main__":
    registrar_pago_benjamin()
