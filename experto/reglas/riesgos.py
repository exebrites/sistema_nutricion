# reglas/riesgos.py
from experta import *
from experto.motor import Nutricion, MotorNutricional


@Rule(Nutricion(sodio=P(lambda x: x > 700)))
def riesgo_sodio(self):
    self.riesgos.append(
        "Alto contenido de sodio: limitar consumo, especialmente en hipertensos."
    )


@Rule(Nutricion(grasas_saturadas=P(lambda g: g > 10)))
def riesgo_grasas_saturadas(self):
    self.riesgos.append("Alto en grasas saturadas: riesgo cardiovascular.")


@Rule(Nutricion(azucar=P(lambda a: a > 20)))
def riesgo_azucar(self):
    self.riesgos.append("Exceso de azúcar: evitar en dietas para diabéticos.")
