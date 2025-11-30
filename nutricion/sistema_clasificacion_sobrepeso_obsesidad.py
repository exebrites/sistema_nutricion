
# -------------------------------
# SISTEMA EXPERTO - CLASIFICACIÓN IMC ADULTOS
# -------------------------------

from experta import *

# -----------------------------------------
# 1) Definición del hecho (input del paciente)
# -----------------------------------------
class Paciente(Fact):
    """Hecho que contiene datos antropométricos simples del paciente adulto."""
    imc = Field(float, mandatory=True)

# -----------------------------------------
# 2) Motor del sistema experto
# -----------------------------------------
class ClasificacionIMC(KnowledgeEngine):

    def __init__(self):
        super().__init__()
        self.resultado = None
        self.triggered_rule = None # New attribute to store the triggered rule details

    @DefFacts()
    def _initial_action(self):
        yield Fact(start=True)

    # Normal
    @Rule(Paciente(imc=P(lambda x: x < 25)))
    def normal(self):
        self.resultado = "IMC Normal (<25)"
        self.triggered_rule = {
            "rule_name": "normal",
            "classification": self.resultado,
            "condition": "imc < 25"
        }
        print("Clasificación: IMC Normal (<25)")

    # Sobrepeso
    @Rule(Paciente(imc=P(lambda x: 25 <= x < 30)))
    def sobrepeso(self):
        self.resultado = "Sobrepeso (25–29.9)"
        self.triggered_rule = {
            "rule_name": "sobrepeso",
            "classification": self.resultado,
            "condition": "25 <= imc < 30"
        }
        print("Clasificación: Sobrepeso (25–29.9)")

    # Obesidad grado I
    @Rule(Paciente(imc=P(lambda x: 30 <= x < 35)))
    def obesidad_I(self):
        self.resultado = "Obesidad grado I (30–34.9)"
        self.triggered_rule = {
            "rule_name": "obesidad_I",
            "classification": self.resultado,
            "condition": "30 <= imc < 35"
        }
        print("Clasificación: Obesidad grado I (30–34.9)")

    # Obesidad grado II
    @Rule(Paciente(imc=P(lambda x: 35 <= x < 40)))
    def obesidad_II(self):
        self.resultado = "Obesidad grado II (35–39.9)"
        self.triggered_rule = {
            "rule_name": "obesidad_II",
            "classification": self.resultado,
            "condition": "35 <= imc < 40"
        }
        print("Clasificación: Obesidad grado II (35–39.9)")

    # Obesidad grado III
    @Rule(Paciente(imc=P(lambda x: x >= 40)))
    def obesidad_III(self):
        self.resultado = "Obesidad grado III (≥40)"
        self.triggered_rule = {
            "rule_name": "obesidad_III",
            "classification": self.resultado,
            "condition": "imc >= 40"
        }
        print("Clasificación: Obesidad grado III (≥40)")

# -----------------------------------------
# 3) Ejecución del sistema experto
# -----------------------------------------
def clasificar_imc(imc_valor):
    engine = ClasificacionIMC()
    engine.reset()
    engine.declare(Paciente(imc=imc_valor))
    engine.run()
    return engine.resultado, engine.triggered_rule # Return both results and triggered rule

# -----------------------------------------
# 4) Ejemplo de prueba
# -----------------------------------------
print("=== EJEMPLO ===")
resultado, regla_activada = clasificar_imc(39.0) # Changed 39 to 39.0
print("Resultado devuelto por el motor:", resultado)
print("Regla activada:", regla_activada)
