from django.db import models
from estudiantes.models import Curso

class TipoActividad(models.Model):
    nombre = models.CharField(max_length=100)
    descripcion = models.TextField(blank=True)
    
    def __str__(self):
        return self.nombre

class Actividad(models.Model):
    ESTADO_CHOICES = [
        ('planificada', 'Planificada'),
        ('activa', 'Activa'),
        ('finalizada', 'Finalizada'),
        ('cancelada', 'Cancelada'),
    ]
    
    nombre = models.CharField(max_length=200)
    descripcion = models.TextField()
    tipo = models.ForeignKey(TipoActividad, on_delete=models.CASCADE)
    fecha_inicio = models.DateField()
    fecha_fin = models.DateField()
    monto_por_estudiante = models.DecimalField(max_digits=10, decimal_places=0)
    cursos_asignados = models.ManyToManyField(Curso)
    estado = models.CharField(max_length=20, choices=ESTADO_CHOICES, default='planificada')
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.nombre
    
    def total_estudiantes(self):
        # Simular conteo de estudiantes
        return sum([25, 28, 30, 27, 26][:len(self.cursos_asignados.all())])
    
    def recaudacion_esperada(self):
        return self.monto_por_estudiante * self.total_estudiantes()
