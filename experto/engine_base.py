from experta import KnowledgeEngine


class MotorBase(KnowledgeEngine):
    """
    Esta clase maneja el estado de la inferencia y los contenedores de resultados.
    NO contiene reglas de negocio, solo lógica de gestión.
    """

    def __init__(self):
        super().__init__()
        # Inicializamos los contenedores de resultados
        self.riesgos = []
        self.advertencias = []
        self.beneficios = []
        self.clasificacion = None
        # --- Listas de Validación (NUEVAS) ---
        self.errores = []
        self.info = []
        #-- sobrepeso/obesidad   
        self.resultado = None
        self.triggered_rule = None # New attribute to store the triggered rule details

    # Métodos para agregar resultados


    def agregar_riesgo(self, mensaje):
        self.riesgos.append(mensaje)

    def agregar_advertencia(self, mensaje):
        self.advertencias.append(mensaje)

    def agregar_beneficio(self, mensaje):
        self.beneficios.append(mensaje)

    def set_clasificacion(self, tipo):
        # Solo asignamos si no tiene una clasificación previa (o según tu lógica)
        if self.clasificacion is None or tipo != "Neutro":
            self.clasificacion = tipo
    # --- NUEVOS MÉTODOS ---

    def agregar_error(self, mensaje):
        self.errores.append(mensaje)

    def agregar_info(self, mensaje):
        self.info.append(mensaje)

    #sobrepeso/obesidad
    def set_resultado(self, resultado):
        self.resultado = resultado

    def set_triggered_rule(self, triggered_rule):
        self.triggered_rule = triggered_rule

    def obtener_reporte_validacion(self):
        """Retorna solo lo relevante para validación"""
        return {
            "errores": self.errores,
            "advertencias": self.advertencias,
            "info": self.info,
            "es_valido": len(self.errores) == 0  # Un flag útil
        }

    def obtener_reporte(self):
        """Devuelve un diccionario limpio con los resultados."""
        return {
            "riesgos": self.riesgos,
            "advertencias": self.advertencias,
            "beneficios": self.beneficios,
            "clasificacion": self.clasificacion or "Neutro"
        }
