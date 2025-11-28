from datetime import datetime
from motor_inferencia import MotorAlimentos, Alimento 
from random import choice
if __name__ == "__main__":
 
    engine = MotorAlimentos()
    engine.reset()

    engine.declare(Alimento(
        nombre="Galletitas",
        calorias=300,
        proteinas=4,
        grasas=15,
        carbohidratos=40,
        sodio=750,
        fecha_vencimiento=datetime(2025, 1, 30),
        stock=2,
        fibra=1
    ))

    engine.run()

# Be cautious because light is blinking-yellow
