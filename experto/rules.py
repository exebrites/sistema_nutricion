from datetime import datetime
from experta import Rule, P,OR, AS
from .facts import Nutricion, Validacion  # Importamos Validacion
from .engine_base import MotorBase

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
        self.agregar_advertencia(
            "Alto en carbohidratos: balancear con proteínas.")

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


class ReglasValidacion(MotorBase):
    """
    Motor dedicado a validar la integridad de los datos 
    (fechas, stock, nombres, límites extremos).
    """

    # ---------------- VALIDACIONES DE ERROR ---------------- #
    @Rule(Validacion(calorias=P(lambda c: c <= 0)))
    def calorias_invalidas(self):
        self.agregar_error("Las calorías deben ser mayores a 0.")

    @Rule(Validacion(nombre=P(lambda n: len(n.strip()) == 0)))
    def nombre_vacio(self):
        self.agregar_error("El nombre no puede estar vacío.")

    @Rule(Validacion(fecha_vencimiento=P(lambda f: f < datetime.now())))
    def alimento_vencido(self):
        self.agregar_error("El alimento está vencido.")

    @Rule(Validacion(stock=P(lambda s: s < 0)))
    def stock_negativo(self):
        self.agregar_error("El stock no puede ser negativo.")

    # ---------------- ADVERTENCIAS ---------------- #
    # Nota: Usamos Validacion(), no Nutricion() aquí

    @Rule(Validacion(sodio=P(lambda s: s > 600)))
    def alto_en_sodio(self):
        self.agregar_advertencia("Alto en sodio (Validación).")

    @Rule(Validacion(grasas=P(lambda g: g > 20)))
    def grasas_altas(self):
        self.agregar_advertencia("Contenido de grasas elevado.")

    @Rule(Validacion(stock=P(lambda s: 0 <= s <= 3)))
    def stock_bajo(self):
        self.agregar_advertencia("Stock bajo, reponer pronto.")

    # ---------------- INFO ---------------- #
    @Rule(Validacion(calorias=P(lambda c: c < 100)))
    def bajo_calorias(self):
        self.agregar_info("Producto bajo en calorías.")

    @Rule(Validacion(calorias=P(lambda c: c >= 250)))
    def alto_calorias(self):
        self.agregar_info("Producto alto en calorías.")
