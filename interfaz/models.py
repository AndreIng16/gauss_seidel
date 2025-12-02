from django.db import models

class SistemaEcuaciones(models.Model):
    nombre = models.CharField(max_length=200, default="Sistema sin nombre")
    ecuaciones = models.TextField()
    valores_iniciales = models.CharField(max_length=200)
    tolerancia = models.FloatField()
    max_iteraciones = models.IntegerField()
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-fecha_creacion']
    
    def __str__(self):
        return f"{self.nombre} - {self.fecha_creacion.strftime('%Y-%m-%d %H:%M')}"


class Solucion(models.Model):
    sistema = models.OneToOneField(SistemaEcuaciones, on_delete=models.CASCADE)
    solucion = models.TextField()
    variables = models.CharField(max_length=200)
    convergio = models.BooleanField(default=True)
    iteraciones_usadas = models.IntegerField()
    
    def __str__(self):
        return f"Solución de {self.sistema.nombre}"


class Iteracion(models.Model):
    sistema = models.ForeignKey(SistemaEcuaciones, on_delete=models.CASCADE, related_name='iteraciones')
    numero = models.IntegerField()
    valores = models.TextField()
    errores = models.TextField()
    
    class Meta:
        ordering = ['numero']
    
    def __str__(self):
        return f"Iteración {self.numero}"