# motor.py
from experta import KnowledgeEngine, Fact
from importlib import import_module
import pkgutil


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


def cargar_reglas(engine, paquete="experto.reglas"):
    """
    Carga automática de todas las reglas
    definidas en el paquete experto/reglas/
    """
    for _, modulo, _ in pkgutil.iter_modules(import_module(paquete).__path__):
        import_module(f"{paquete}.{modulo}")
