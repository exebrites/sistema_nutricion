from experta import Fact, Field

class Nutricion(Fact):
    """
    Modelo de datos para los alimentos.
    Define la estructura de la información que entra al sistema.
    """
    pass
class Validacion(Fact):
    """
    Datos para validar la integridad del alimento 
    (stock, nombre, fecha, etc.)
    """
    pass

class Paciente(Fact):
    """Hecho que contiene datos antropométricos simples del paciente adulto."""
    imc = Field(float, mandatory=True)
    pass