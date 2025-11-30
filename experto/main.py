from .facts import Nutricion, Paciente
from .rules import BaseConocimientoNutricional, ClasificacionIMC

def evaluar_nutricion(data,modo="completo"):
    if modo not in ["validacion","nutricion"]:
        raise ValueError("Modo inválido. Use 'validacion' o 'nutricion'.")
    # 1. Instanciamos la Base de Conocimiento (que incluye el motor por herencia)
    engine = BaseConocimientoNutricional()
    
    # 2. Reseteo y carga de hechos
    engine.reset()
    engine.declare(Nutricion(**data))
    
    # 3. Ejecución
    engine.run()
    if modo =="validacion":
        return engine.obtener_reporte_validacion()
    if modo =="nutricion":
        return engine.obtener_reporte()
    # 4. Extracción de resultados (usando el método del padre)
    

class DiagnosticoPES:
    """Clase para manejar diagnósticos de sobrepeso y obesidad basados en IMC."""
    
    def clasificar_imc(imc_valor):
        engine = ClasificacionIMC()
        engine.reset()
        engine.declare(Paciente(imc=imc_valor))
        engine.run()
        return engine.resultado, engine.triggered_rule # Return both results and triggered rule