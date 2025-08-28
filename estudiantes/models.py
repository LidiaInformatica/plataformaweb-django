from django.db import models
from django.contrib.auth.models import User

class Curso(models.Model):
    nombre = models.CharField(max_length=50)
    nivel = models.CharField(max_length=20)
    año = models.IntegerField()
    
    def __str__(self):
        return f"{self.nombre} - {self.año}"

class Apoderado(models.Model):
    usuario = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True)
    rut = models.CharField(max_length=12, unique=True)
    nombre = models.CharField(max_length=100)
    apellido_paterno = models.CharField(max_length=50)
    apellido_materno = models.CharField(max_length=50)
    telefono = models.CharField(max_length=15)
    email = models.EmailField()
    direccion = models.TextField(blank=True)
    fecha_registro = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.nombre} {self.apellido_paterno} {self.apellido_materno}"
    
    def nombre_completo(self):
        return f"{self.nombre} {self.apellido_paterno} {self.apellido_materno}"

class Estudiante(models.Model):
    VINCULO_CHOICES = [
        ('hijo', 'Hijo/a'),
        ('padre', 'Padre'),
        ('madre', 'Madre'),
        ('abuelo', 'Abuelo/a'),
        ('tio', 'Tío/a'),
        ('tutor', 'Tutor Legal'),
        ('otro', 'Otro'),
    ]
        
    rut = models.CharField(max_length=12, unique=True)
    nombre = models.CharField(max_length=100)
    apellido_paterno = models.CharField(max_length=50)
    apellido_materno = models.CharField(max_length=50)
    fecha_nacimiento = models.DateField()
    curso = models.ForeignKey(Curso, on_delete=models.CASCADE)
    apoderado = models.ForeignKey(Apoderado, on_delete=models.CASCADE)
    vinculo_apoderado = models.CharField(max_length=20, choices=VINCULO_CHOICES)
    fecha_registro = models.DateTimeField(auto_now_add=True)
    activo = models.BooleanField(default=True)
    
    def __str__(self):
        return f"{self.nombre} {self.apellido_paterno} {self.apellido_materno}"
    
    def nombre_completo(self):
        return f"{self.nombre} {self.apellido_paterno} {self.apellido_materno}"
