# reglas/advertencias.py
from experta import *
from experto.motor import Nutricion


@Rule(Nutricion(calorias=P(lambda c: c >= 300)))
def advertencia_calorias(self):
    self.advertencias.append("Alimento calórico: moderar porciones.")


@Rule(Nutricion(grasas_totales=P(lambda g: g > 20)))
def advertencia_grasas(self):
    self.advertencias.append("Contiene mucha grasa total.")


@Rule(Nutricion(carbohidratos=P(lambda c: c > 40)))
def advertencia_carbohidratos(self):
    self.advertencias.append(
        "Alto en carbohidratos: considerar balancear con proteínas."
    )
