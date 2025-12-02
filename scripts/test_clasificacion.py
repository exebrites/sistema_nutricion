import os
import sys

# Asegurar que la carpeta `sistema_nutricion` está en sys.path
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

from experto.rules import BaseConocimientoNutricional
from experto.facts import Nutricion


def test_ultraprocesado():
    """Prueba la regla ultraprocesado con valores altos"""
    engine = BaseConocimientoNutricional()
    engine.reset()
    engine.declare(Nutricion(
        nombre="Snack ultraprocesado",
        sodio=700,
        grasas_saturadas=20,
        azucar=30,
        calorias=350
    ))
    engine.run()
    
    print("=== TEST: Regla Ultraprocesado ===")
    print(f"Clasificación: {engine.clasificacion}")
    print(f"Riesgos: {engine.riesgos}")
    print(f"Advertencias: {engine.advertencias}")
    print()


def test_poco_saludable():
    """Prueba la regla poco_saludable (sin cumplir ultraprocesado)"""
    engine = BaseConocimientoNutricional()
    engine.reset()
    engine.declare(Nutricion(
        nombre="Galletas",
        sodio=350,
        grasas_saturadas=8,
        azucar=18,
        calorias=200
    ))
    engine.run()
    
    print("=== TEST: Regla Poco Saludable ===")
    print(f"Clasificación: {engine.clasificacion}")
    print(f"Riesgos: {engine.riesgos}")
    print(f"Advertencias: {engine.advertencias}")
    print()


def test_saludable():
    """Prueba la regla saludable"""
    engine = BaseConocimientoNutricional()
    engine.reset()
    engine.declare(Nutricion(
        nombre="Manzana",
        sodio=100,
        grasas=2,
        calorias=80,
        proteinas=10,
        fibra=3,
        vitaminas=True
    ))
    engine.run()
    
    print("=== TEST: Regla Saludable ===")
    print(f"Clasificación: {engine.clasificacion}")
    print(f"Beneficios: {engine.beneficios}")
    print()


if __name__ == '__main__':
    test_ultraprocesado()
    test_poco_saludable()
    test_saludable()
    print("✓ Todos los tests de clasificación completados.")
