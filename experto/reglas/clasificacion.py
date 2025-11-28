# reglas/clasificacion.py
from experta import *
from experto.motor import Nutricion


@Rule(Nutricion(calorias=P(lambda c: c < 150),
                grasas_totales=P(lambda g: g < 8),
                sodio=P(lambda s: s < 200),
                proteinas=P(lambda p: p > 5)))
def clasificacion_saludable(self):
    self.clasificacion = "Saludable"


@Rule(OR(
    Nutricion(calorias=P(lambda c: c >= 150)),
    Nutricion(grasas_totales=P(lambda g: g >= 15)),
    Nutricion(sodio=P(lambda s: s >= 400))
))
def clasificacion_no_saludable(self):
    self.clasificacion = "Poco saludable"


@Rule(AS.f << Nutricion())
def clasificacion_default(self, f):
    if not self.clasificacion:
        self.clasificacion = "Neutro"
