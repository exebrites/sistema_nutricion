from .facts import Nutricion
from .rules import BaseConocimientoNutricional

def evaluar_nutricion(data):
    # 1. Instanciamos la Base de Conocimiento (que incluye el motor por herencia)
    engine = BaseConocimientoNutricional()
    
    # 2. Reseteo y carga de hechos
    engine.reset()
    engine.declare(Nutricion(**data))
    
    # 3. Ejecución
    engine.run()
    
    # 4. Extracción de resultados (usando el método del padre)
    return engine.obtener_reporte()

# --- PRUEBA ---
# if __name__ == "__main__":
#     datos_alimento = {
#         "calorias": 120,
#         "grasas": 5,
#         "grasas_saturadas": 2,
#         "sodio": 150,
#         "azucar": 10,
#         "carbohidratos": 30,
#         "proteinas": 20,
#         "fibra": 6,
#         "vitaminas": True
#     }

#     resultado = evaluar_nutricion(datos_alimento)
#     import json
#     print(json.dumps(resultado, indent=4, ensure_ascii=False))