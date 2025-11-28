from experta import *
from datetime import datetime


class Nutricion(Fact):
    """Datos nutricionales del alimento."""
    pass


class MotorNutricional(KnowledgeEngine):

    def __init__(self):
        super().__init__()
        self.riesgos = []
        self.advertencias = []
        self.beneficios = []
        self.clasificacion = None

    # ---------------- RULES: RIESGOS ---------------- #

    @Rule(Nutricion(sodio=P(lambda x: x > 700)))
    def riesgo_sodio(self):
        self.riesgos.append(
            "Alto contenido de sodio: limitar consumo, especialmente en hipertensos.")

    @Rule(Nutricion(grasas_saturadas=P(lambda g: g > 10)))
    def riesgo_grasas_saturadas(self):
        self.riesgos.append("Alto en grasas saturadas: riesgo cardiovascular.")

    @Rule(Nutricion(azucar=P(lambda a: a > 20)))
    def riesgo_azucar(self):
        self.riesgos.append(
            "Exceso de azúcar: evitar en dietas para diabéticos.")

    # ---------------- RULES: ADVERTENCIAS ---------------- #

    @Rule(Nutricion(calorias=P(lambda c: c >= 300)))
    def advertencia_calorias(self):
        self.advertencias.append("Alimento calórico: moderar porciones.")

    @Rule(Nutricion(grasas_totales=P(lambda g: g > 20)))
    def advertencia_grasas(self):
        self.advertencias.append("Contiene mucha grasa total.")

    @Rule(Nutricion(carbohidratos=P(lambda c: c > 40)))
    def advertencia_carbohidratos(self):
        self.advertencias.append(
            "Alto en carbohidratos: considerar balancear con proteínas.")

    # ---------------- RULES: BENEFICIOS ---------------- #

    @Rule(Nutricion(proteinas=P(lambda p: p >= 15)))
    def beneficio_proteina(self):
        self.beneficios.append("Buena fuente de proteínas.")

    @Rule(Nutricion(fibra=P(lambda f: f >= 5)))
    def beneficio_fibra(self):
        self.beneficios.append("Alto en fibra: ayuda a la digestión.")

    @Rule(Nutricion(vitaminas=P(lambda v: v == True)))
    def beneficio_vitaminas(self):
        self.beneficios.append("Contiene vitaminas esenciales.")

    # ---------------- CLASIFICACIÓN FINAL ---------------- #

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


def evaluar_nutricion(data):
    engine = MotorNutricional()
    engine.reset()
    engine.declare(Nutricion(**data))
    engine.run()

    return {
        "riesgos": engine.riesgos,
        "advertencias": engine.advertencias,
        "beneficios": engine.beneficios,
        "clasificacion": engine.clasificacion,
    }
