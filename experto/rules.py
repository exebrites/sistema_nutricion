from experta import Rule, P, AS, OR
from .facts import Nutricion  # Importamos los hechos
from .engine_base import MotorBase # Importamos el motor base

class BaseConocimientoNutricional(MotorBase):
    """
    Aquí residen EXCLUSIVAMENTE las reglas de negocio.
    Hereda la capacidad de almacenar resultados del MotorBase.
    """

    # ---------------- RIESGOS ---------------- #
    @Rule(Nutricion(sodio=P(lambda x: x > 700)))
    def riesgo_sodio(self):
        self.agregar_riesgo("Alto contenido de sodio: limitar en hipertensos.")

    @Rule(Nutricion(grasas_saturadas=P(lambda g: g > 10)))
    def riesgo_grasas(self):
        self.agregar_riesgo("Alto en grasas saturadas: riesgo cardiovascular.")

    @Rule(Nutricion(azucar=P(lambda a: a > 20)))
    def riesgo_azucar(self):
        self.agregar_riesgo("Exceso de azúcar: evitar en diabéticos.")

    # ---------------- ADVERTENCIAS ---------------- #
    @Rule(Nutricion(calorias=P(lambda c: c >= 300)))
    def advertencia_calorias(self):
        self.agregar_advertencia("Alimento calórico: moderar porciones.")

    @Rule(Nutricion(grasas_totales=P(lambda g: g > 20)))
    def advertencia_grasas_totales(self):
        self.agregar_advertencia("Contiene mucha grasa total.")

    @Rule(Nutricion(carbohidratos=P(lambda c: c > 40)))
    def advertencia_carbohidratos(self):
        self.agregar_advertencia("Alto en carbohidratos: balancear con proteínas.")

    # ---------------- BENEFICIOS ---------------- #
    @Rule(Nutricion(proteinas=P(lambda p: p >= 15)))
    def beneficio_proteina(self):
        self.agregar_beneficio("Buena fuente de proteínas.")

    @Rule(Nutricion(fibra=P(lambda f: f >= 5)))
    def beneficio_fibra(self):
        self.agregar_beneficio("Alto en fibra: ayuda a la digestión.")

    @Rule(Nutricion(vitaminas=True))
    def beneficio_vitaminas(self):
        self.agregar_beneficio("Contiene vitaminas esenciales.")

    # ---------------- CLASIFICACIÓN ---------------- #
    @Rule(Nutricion(calorias=P(lambda c: c < 150),
                    grasas=P(lambda g: g < 8),
                    sodio=P(lambda s: s < 200),
                    proteinas=P(lambda p: p > 5)))
    def clasificacion_saludable(self):
        self.set_clasificacion("Saludable")

    @Rule(OR(
        Nutricion(calorias=P(lambda c: c >= 150)),
        Nutricion(grasas=P(lambda g: g >= 15)),
        Nutricion(sodio=P(lambda s: s >= 400))
    ))
    def clasificacion_no_saludable(self):
        self.set_clasificacion("Poco saludable")

    # Regla por defecto (baja prioridad o catch-all)
    @Rule(AS.f << Nutricion())
    def clasificacion_default(self, f):
        # La lógica de "si no existe clasificacion, pon neutro" 
        # ya la manejamos en el método obtener_reporte o set_clasificacion del padre,
        # pero aquí podemos forzar un cálculo si es necesario.
        pass