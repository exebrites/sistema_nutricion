from django.contrib import admin

from nutricion.models import Alimento, Antropometria, Dieta, DietaAlimento, HabitoAlimentario, MotivoConsulta, Paciente, Sintoma

# Register your models here.
admin.site.register(Alimento)
admin.site.register(Dieta)
admin.site.register(DietaAlimento)
admin.site.register(Paciente)
admin.site.register(Antropometria)
admin.site.register(MotivoConsulta)
admin.site.register(Sintoma)
admin.site.register(HabitoAlimentario)
