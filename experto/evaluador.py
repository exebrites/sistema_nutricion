# evaluador.py
from experto.motor import MotorNutricional, Nutricion, cargar_reglas


def evaluar_nutricion(data):
    engine = MotorNutricional()
    cargar_reglas(engine)

    engine.reset()
    engine.declare(Nutricion(**data))
    engine.run()

    return {
        "riesgos": engine.riesgos,
        "advertencias": engine.advertencias,
        "beneficios": engine.beneficios,
        "clasificacion": engine.clasificacion,
    }
