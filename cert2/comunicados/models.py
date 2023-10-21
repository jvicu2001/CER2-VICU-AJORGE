from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save

# Create your models here.
class Entidad(models.Model):
    id = models.BigAutoField(primary_key=True)
    nombre = models.CharField(max_length=100)
    logo = models.ImageField(upload_to='logos', null=True, blank=True)

    def __str__(self):
        return self.nombre
    
    class Meta:
        verbose_name_plural = "Entidades"
    
class Comunicado(models.Model):
    TIPO_CHOICES = [
        ("S", "Suspensión de actividades"),
        ("C", "Suspensión de clase"),
        ("I", "Información")
    ]

    id = models.BigAutoField(primary_key=True)
    titulo = models.CharField(max_length=100)
    detalle = models.CharField(max_length=1000)
    detalle_corto = models.CharField(max_length=100)
    tipo = models.CharField(max_length=1, choices=TIPO_CHOICES)
    entidad = models.ForeignKey(Entidad, on_delete=models.CASCADE)
    visible = models.BooleanField(default=True)
    fecha_publicacion = models.DateTimeField(auto_now_add=True) # Darle la fecha actual, ya que se crea cuando se publica
    fecha_expiracion = models.DateTimeField(null=True, blank=True)
    publicado_por = models.ForeignKey(User, on_delete=models.CASCADE)

    # Ya que se tiene a User como ForeignKey dos veces, se debe especificar el related_name
    modificado_por = models.ForeignKey(User, on_delete=models.CASCADE, related_name="modificado_por", null=True, blank=True) 

    def __str__(self):
        return self.titulo
    
# Modelo extension usuario, para relacionarlo con modelo Entidad
class AdminEntidad(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    entidad = models.ForeignKey(Entidad, on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return self.user.username