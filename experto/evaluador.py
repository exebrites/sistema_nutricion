# evaluador.py
from experto.motor import MotorNutricional, Nutricion, cargar_reglas


def evaluar_nutricion(data, modo="completo"):
    engine = MotorNutricional()
    cargar_reglas(engine)

    engine.reset()
    engine.declare(Nutricion(**data))
    engine.run()
    # Resultado general
    resultado = {
        "errores": engine.errores,
        "advertencias_validacion": engine.advertencias_validacion,
        "info": engine.info,
        "riesgos": engine.riesgos,
        "advertencias_nutricionales": engine.advertencias_nutricionales,
        "beneficios": engine.beneficios,
        "clasificacion": engine.clasificacion,
    }
    # ---- FILTRADOS POR MODO ---- #

    if modo == "crud":
        return {
            "errores": engine.errores,
            "advertencias": engine.advertencias_validacion,
            "info": engine.info,       # si querés se puede remover
        }

    if modo == "nutricional":
        return {
            "riesgos": engine.riesgos,
            "advertencias": engine.advertencias_nutricionales,
            "beneficios": engine.beneficios,
            "clasificacion": engine.clasificacion,
        }

    return resultado   # modo completo
