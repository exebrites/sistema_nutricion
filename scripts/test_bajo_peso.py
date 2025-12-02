import os
import sys

# Asegurar que la carpeta `sistema_nutricion` está en sys.path
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

from experto.rules import ClasificacionIMC
from experto.facts import Paciente


def test_bajo_peso():
    """Prueba la nueva regla bajo_peso con IMC 17.5"""
    engine = ClasificacionIMC()
    engine.reset()
    engine.declare(Paciente(imc=17.5))
    engine.run()
    
    print("=== TEST: Regla Bajo Peso (IMC 17.5) ===")
    print(f"Resultado: {engine.resultado}")
    print(f"Regla disparada: {engine.triggered_rule}")
    print()


def test_normal():
    """Prueba la regla normal con IMC 22"""
    engine = ClasificacionIMC()
    engine.reset()
    engine.declare(Paciente(imc=22.0))
    engine.run()
    
    print("=== TEST: Regla Normal (IMC 22) ===")
    print(f"Resultado: {engine.resultado}")
    print(f"Regla disparada: {engine.triggered_rule}")
    print()


def test_sobrepeso():
    """Prueba la regla sobrepeso con IMC 27"""
    engine = ClasificacionIMC()
    engine.reset()
    engine.declare(Paciente(imc=27.0))
    engine.run()
    
    print("=== TEST: Regla Sobrepeso (IMC 27) ===")
    print(f"Resultado: {engine.resultado}")
    print(f"Regla disparada: {engine.triggered_rule}")
    print()


def test_obesidad_grado_I():
    """Prueba la regla obesidad I con IMC 32"""
    engine = ClasificacionIMC()
    engine.reset()
    engine.declare(Paciente(imc=32.0))
    engine.run()
    
    print("=== TEST: Regla Obesidad Grado I (IMC 32) ===")
    print(f"Resultado: {engine.resultado}")
    print(f"Regla disparada: {engine.triggered_rule}")
    print()


if __name__ == '__main__':
    test_bajo_peso()
    test_normal()
    test_sobrepeso()
    test_obesidad_grado_I()
    print("✓ Todos los tests completados.")
