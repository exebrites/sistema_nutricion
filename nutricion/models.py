from django.db import models

# Create your models here.


class Alimento(models.Model):
    nombre = models.CharField(max_length=50)
    calorias = models.IntegerField()
    proteinas = models.IntegerField()
    grasas = models.IntegerField()
    carbohidratos = models.IntegerField()
    sodio = models.IntegerField()
    fecha_vencimiento = models.DateField()
    stock = models.IntegerField()

    def __str__(self):
        return self.nombre
    def to_dict(self):
        return {
            'id': self.id,
            'nombre': self.nombre,
            'calorias': self.calorias,
            'proteinas': self.proteinas,
            'grasas': self.grasas,
            'carbohidratos': self.carbohidratos,
            'sodio': self.sodio,
            'stock': self.stock,
            'fecha_vencimiento': str(self.fecha_vencimiento) if self.fecha_vencimiento else None
        }

class Dieta(models.Model):
    nombre = models.CharField(max_length=100)
    descripcion = models.TextField(blank=True)
    alimentos = models.ManyToManyField(
        'Alimento',
        through='DietaAlimento',
        related_name='dietas'
    )
    creada = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.nombre


class DietaAlimento(models.Model):
    dieta = models.ForeignKey(Dieta, on_delete=models.CASCADE)
    alimento = models.ForeignKey(Alimento, on_delete=models.CASCADE)
    cantidad = models.FloatField(default=100.0, help_text='Cantidad en gramos')
    unidad = models.CharField(max_length=20, default='g')

    class Meta:
        unique_together = ('dieta', 'alimento')

    def __str__(self):
        return f"{self.cantidad}{self.unidad} de {self.alimento.nombre} en {self.dieta.nombre}"
# ...existing code...
