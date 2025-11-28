from .facts import Nutricion
from .rules import BaseConocimientoNutricional

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