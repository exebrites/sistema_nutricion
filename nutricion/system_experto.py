from experta import *
from datetime import datetime


class Validacion(Fact):
    """Fact con datos del alimento."""
    pass


class MotorValidacion(KnowledgeEngine):

    def __init__(self):
        super().__init__()
        self.errores = []
        self.advertencias = []
        self.info = []

    # ---------------- VALIDACIONES DE ERROR ---------------- #

    @Rule(Validacion(calorias=P(lambda c: c <= 0)))
    def calorias_invalidas(self):
        self.errores.append("Las calorías deben ser mayores a 0.")

    @Rule(Validacion(nombre=P(lambda n: len(n.strip()) == 0)))
    def nombre_vacio(self):
        self.errores.append("El nombre no puede estar vacío.")

    @Rule(Validacion(fecha_vencimiento=P(lambda f: f < datetime.now())))
    def alimento_vencido(self):
        self.errores.append("El alimento está vencido.")

    @Rule(Validacion(stock=P(lambda s: s < 0)))
    def stock_negativo(self):
        self.errores.append("El stock no puede ser negativo.")

    # ---------------- ADVERTENCIAS ---------------- #

    @Rule(Validacion(sodio=P(lambda s: s > 600)))
    def alto_en_sodio(self):
        self.advertencias.append("Alto en sodio.")

    @Rule(Validacion(grasas=P(lambda g: g > 20)))
    def grasas_altas(self):
        self.advertencias.append("Contenido de grasas elevado.")

    @Rule(Validacion(stock=P(lambda s: 0 <= s <= 3)))
    def stock_bajo(self):
        self.advertencias.append("Stock bajo.")

    # ---------------- INFO / CLASIFICACIONES ---------------- #

    @Rule(Validacion(calorias=P(lambda c: c < 100)))
    def bajo_calorias(self):
        self.info.append("Bajo en calorías.")

    @Rule(Validacion(calorias=P(lambda c: c >= 250)))
    def alto_calorias(self):
        self.info.append("Alto en calorías.")


def validar_alimento(data):
    """
    Recibe un dict desde Django Forms y devuelve las listas:
    errores, advertencias, info.
    """

    engine = MotorValidacion()
    engine.reset()
    engine.declare(Validacion(**data))
    engine.run()

    return {
        "errores": engine.errores,
        "advertencias": engine.advertencias,
        "info": engine.info
    }
