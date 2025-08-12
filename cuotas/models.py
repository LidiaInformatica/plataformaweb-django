from django.db import models
from estudiantes.models import Estudiante
from actividades.models import Actividad

class CuotaEstudiante(models.Model):
    ESTADO_CHOICES = [
        ('pendiente', 'Pendiente'),
        ('pagado', 'Pagado'),
        ('vencido', 'Vencido'),
        ('exento', 'Exento'),
    ]
    
    estudiante = models.ForeignKey(Estudiante, on_delete=models.CASCADE)
    actividad = models.ForeignKey(Actividad, on_delete=models.CASCADE)
    monto_total = models.DecimalField(max_digits=10, decimal_places=0)
    monto_pagado = models.DecimalField(max_digits=10, decimal_places=0, default=0)
    estado = models.CharField(max_length=20, choices=ESTADO_CHOICES, default='pendiente')
    fecha_vencimiento = models.DateField()
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.estudiante} - {self.actividad}"
    
    def saldo_pendiente(self):
        return self.monto_total - self.monto_pagado

class PagoCuota(models.Model):
    METODO_PAGO_CHOICES = [
        ('efectivo', 'Efectivo'),
        ('transferencia', 'Transferencia'),
        ('cheque', 'Cheque'),
        ('tarjeta', 'Tarjeta'),
    ]
    
    cuota = models.ForeignKey(CuotaEstudiante, on_delete=models.CASCADE)
    monto = models.DecimalField(max_digits=10, decimal_places=0)
    metodo_pago = models.CharField(max_length=20, choices=METODO_PAGO_CHOICES)
    fecha_pago = models.DateTimeField(auto_now_add=True)
    observacion = models.TextField(blank=True)
    comprobante = models.CharField(max_length=100, blank=True)
    
    def __str__(self):
        return f"Pago {self.monto} - {self.cuota}"
