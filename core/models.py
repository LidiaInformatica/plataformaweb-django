from django.db import models
from django.contrib.auth.models import User

class PerfilUsuario(models.Model):
    TIPO_PERFIL_CHOICES = [
        ('administrador', 'Administrador del Sistema'),
        ('directiva', 'Directiva (Presidenta/Tesorera/Secretaria)'),
        ('apoderado', 'Apoderado'),
    ]
    
    CARGO_DIRECTIVA_CHOICES = [
        ('presidenta', 'Presidenta'),
        ('tesorera', 'Tesorera'),
        ('secretaria', 'Secretaria'),
    ]
    
    usuario = models.OneToOneField(User, on_delete=models.CASCADE)
    tipo_perfil = models.CharField(max_length=20, choices=TIPO_PERFIL_CHOICES)
    cargo_directiva = models.CharField(
        max_length=20, 
        choices=CARGO_DIRECTIVA_CHOICES, 
        blank=True, 
        null=True,
        help_text="Solo para miembros de la directiva"
    )
    rut = models.CharField(max_length=12, unique=True)
    telefono = models.CharField(max_length=15, blank=True)
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.usuario.get_full_name()} - {self.get_tipo_perfil_display()}"

class Mensaje(models.Model):
    TIPO_MENSAJE_CHOICES = [
        ('info', 'Información'),
        ('alerta', 'Alerta'),
        ('urgente', 'Urgente'),
    ]
    
    titulo = models.CharField(max_length=200)
    contenido = models.TextField()
    tipo = models.CharField(max_length=20, choices=TIPO_MENSAJE_CHOICES, default='info')
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    activo = models.BooleanField(default=True)
    
    def __str__(self):
        return self.titulo

class ConfiguracionSistema(models.Model):
    nombre_institucion = models.CharField(max_length=200, default='Colegio Adventista Talcahuano Centro')
    telefono_contacto = models.CharField(max_length=15, blank=True)
    email_contacto = models.EmailField(blank=True)
    direccion_institucion = models.TextField(blank=True)
    
    def __str__(self):
        return self.nombre_institucion

class Notificacion(models.Model):
    TIPO_NOTIFICACION_CHOICES = [
        ('nueva_actividad', 'Nueva Actividad Creada'),
        ('recordatorio_pago', 'Recordatorio de Pago'),
        ('pago_recibido', 'Pago Recibido'),
        ('actividad_vencida', 'Actividad Vencida'),
        ('sistema', 'Notificación del Sistema'),
    ]
    
    ESTADO_CHOICES = [
        ('pendiente', 'Pendiente'),
        ('enviada', 'Enviada'),
        ('fallida', 'Fallida'),
    ]
    
    tipo = models.CharField(max_length=30, choices=TIPO_NOTIFICACION_CHOICES)
    titulo = models.CharField(max_length=200)
    mensaje = models.TextField()
    email_destinatario = models.EmailField()
    nombre_destinatario = models.CharField(max_length=100)
    estado = models.CharField(max_length=20, choices=ESTADO_CHOICES, default='pendiente')
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    fecha_envio = models.DateTimeField(null=True, blank=True)
    error_envio = models.TextField(blank=True)
    
    # Campos para referenciar objetos relacionados
    actividad_id = models.IntegerField(null=True, blank=True)
    estudiante_id = models.IntegerField(null=True, blank=True)
    
    def __str__(self):
        return f"{self.get_tipo_display()} - {self.email_destinatario}"
    
    class Meta:
        ordering = ['-fecha_creacion']
    direccion = models.CharField(max_length=300, blank=True)
    telefono = models.CharField(max_length=15, blank=True)
    email = models.EmailField(blank=True)
    logo = models.ImageField(upload_to='logos/', blank=True, null=True)
    
    class Meta:
        verbose_name = 'Configuración del Sistema'
        verbose_name_plural = 'Configuraciones del Sistema'
    
    def __str__(self):
        return self.nombre_institucion

class Notificacion(models.Model):
    TIPO_NOTIFICACION_CHOICES = [
        ('pago_confirmado', 'Pago Confirmado'),
        ('pago_parcial', 'Pago Parcial'),
        ('recordatorio', 'Recordatorio de Pago'),
        ('cuota_vencida', 'Cuota Vencida'),
        ('nueva_cuota', 'Nueva Cuota Asignada'),
    ]
    
    ESTADOS = [
        ('enviada', 'Enviada'),
        ('pendiente', 'Pendiente'),
        ('fallida', 'Fallida'),
    ]
    
    # Usuario que registra (admin/directiva)
    usuario_registra = models.ForeignKey(User, on_delete=models.CASCADE, related_name='notificaciones_registradas')
    
    # Información del apoderado destinatario
    apoderado_nombre = models.CharField(max_length=200)
    apoderado_email = models.EmailField()
    apoderado_telefono = models.CharField(max_length=15, blank=True)
    apoderado_rut = models.CharField(max_length=12, blank=True)
    
    titulo = models.CharField(max_length=200)
    mensaje = models.TextField()
    tipo = models.CharField(max_length=20, choices=TIPO_NOTIFICACION_CHOICES)
    
    # Campos adicionales para pagos
    estudiante_nombre = models.CharField(max_length=200, blank=True)
    actividad_nombre = models.CharField(max_length=200, blank=True)
    monto = models.DecimalField(max_digits=10, decimal_places=0, null=True, blank=True)
    metodo_pago = models.CharField(max_length=50, blank=True)
    
    leida = models.BooleanField(default=False)
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    fecha_envio = models.DateTimeField(null=True, blank=True)
    estado = models.CharField(max_length=10, choices=ESTADOS, default='enviada')
    
    class Meta:
        ordering = ['-fecha_creacion']
        verbose_name = 'Notificación'
        verbose_name_plural = 'Notificaciones'
    
    def __str__(self):
        return f"{self.titulo} - Para: {self.apoderado_nombre}"
    
    def marcar_como_enviada(self):
        """Marca la notificación como enviada"""
        from django.utils import timezone
        self.estado = 'enviada'
        self.fecha_envio = timezone.now()
        self.save()
