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
    azucares_totales = models.IntegerField(default=0)
    fibra_alimentaria = models.IntegerField(default=0)
    agua_humedad = models.IntegerField(default=0)
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

class Paciente(models.Model):
    nombre = models.CharField(max_length=50)
    apellido = models.CharField(max_length=50)
    fecha_nacimiento = models.DateField()
    sexo = models.CharField(max_length=1, choices=[('M','Masculino'),('F','Femenino')])
    direccion_residencial = models.CharField(max_length=200)
    numero_telefono = models.CharField(max_length=20)
    edad = models.IntegerField()
    def __str__(self):
        return self.nombre
    #calcular edad 
    def calcular_edad(self):
        from datetime import date
        today = date.today()
        edad = today.year - self.fecha_nacimiento.year - ((today.month, today.day) < (self.fecha_nacimiento.month, self.fecha_nacimiento.day))
        return edad

class Antropometria(models.Model):
    paciente = models.ForeignKey(Paciente, on_delete=models.CASCADE)
    fecha_medicion = models.DateField()
    peso_corporal = models.FloatField(help_text='Peso en kg')
    altura = models.FloatField(help_text='Altura en cm')
    imc = models.FloatField(help_text='Índice de Masa Corporal', blank=True, null=True)
    perimetro_abdominal = models.FloatField(help_text='Perímetro abdominal en cm')
    circunferencia_abdominal = models.FloatField(help_text='Circunferencia abdominal en cm')
    pliegue_cutaneo_tricipital = models.FloatField(help_text='Pliegue cutánea triicipital en mm')
    pliegue_cutaneo_subescapular = models.FloatField(help_text='Pliegue cutánea subescapular en mm')
    pliegue_cutaneo_bicipital = models.FloatField(help_text='Pliegue cutánea bicipital en mm')
    pliegue_cutaneo_suprailiaco = models.FloatField(help_text='Pliegue cutánea suprailiaco en mm')
    circunferencia_cadera = models.FloatField(help_text='Circunferencia de la cadera en cm')
    perimetro_cefalico = models.FloatField(help_text='Perímetro cefálico en cm')

    def save(self, *args, **kwargs):
        if self.altura > 0:
            altura_metros = self.altura / 100
            self.imc = self.peso / (altura_metros ** 2)
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Antropometría de {self.paciente.nombre} el {self.fecha_medicion}"
    
class MotivoConsulta(models.Model):
    paciente = models.ForeignKey(Paciente, on_delete=models.CASCADE)
    fecha_consulta = models.DateField()
    motivo = models.TextField()
    objetivos_peso = models.CharField(max_length=200, choices=[
        ('P', 'Pérdida de peso'),
        ('M', 'Mantenimiento del peso actual'),
        ('A', 'Aumento de peso'),
        ('O', 'Otro')
    ], help_text='Objetivos de peso')
    condiciones_patologicas = models.CharField(max_length=200, choices=[
        ('D', 'Diabetes'),
        ('H', 'Hipertensión'),
        ('C', 'Colesterol'),
        ('O', 'Otra')
    ], help_text='Condiciones patológicas')
    rendimiento_deficiencias = models.TextField(help_text='Rendimiento y deficiencias')

    restricciones_alimentarias = models.CharField(max_length=200, choices=[
        ('A', 'Alergias'),
        ('I', 'Intolerancias alimentarias')
    ], help_text='Restricciones alimentarias')
    
    def __str__(self):
        
        return f"Motivo de consulta de {self.paciente.nombre} el {self.fecha_consulta}"
    
class Sintoma(models.Model):
    nombre = models.CharField(max_length=100)
    descripcion = models.TextField(blank=True)

    def __str__(self):
        return self.nombre