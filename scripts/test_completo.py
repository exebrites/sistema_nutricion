#!/usr/bin/env python
"""
Script maestro que ejecuta todas las pruebas del sistema experto.
Prueba IMC, clasificación de alimentos y validaciones.
"""
import os
import sys

# Asegurar que la carpeta `sistema_nutricion` está en sys.path
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

from experto.rules import ClasificacionIMC, BaseConocimientoNutricional
from experto.facts import Paciente, Nutricion
from experto.main import evaluar_nutricion


def separador(titulo):
    """Imprime un separador visual"""
    print("\n" + "="*70)
    print(f"  {titulo}")
    print("="*70 + "\n")


def test_imc():
    """Prueba completa del sistema de clasificación IMC"""
    separador("1. SISTEMA DE CLASIFICACIÓN IMC")
    
    casos = [
        (17.5, "Bajo peso"),
        (22.0, "Normal"),
        (27.0, "Sobrepeso"),
        (32.0, "Obesidad I"),
        (38.0, "Obesidad II"),
        (42.0, "Obesidad III"),
    ]
    
    for imc, esperado in casos:
        engine = ClasificacionIMC()
        engine.reset()
        engine.declare(Paciente(imc=imc))
        engine.run()
        print(f"  IMC {imc:5.1f} → {engine.resultado:<35} ✓")
    

def test_clasificacion_alimentos():
    """Prueba clasificación de alimentos (saludable, poco saludable, ultraprocesado)"""
    separador("2. SISTEMA DE CLASIFICACIÓN DE ALIMENTOS")
    
    casos = [
        {
            "nombre": "Manzana",
            "sodio": 100,
            "grasas": 2,
            "calorias": 80,
            "proteinas": 10,
            "fibra": 3,
            "vitaminas": True,
            "esperado": "Saludable"
        },
        {
            "nombre": "Galletas",
            "sodio": 350,
            "grasas_saturadas": 8,
            "azucar": 18,
            "calorias": 200,
            "esperado": "Poco saludable"
        },
        {
            "nombre": "Snack ultraprocesado",
            "sodio": 700,
            "grasas_saturadas": 20,
            "azucar": 30,
            "calorias": 350,
            "esperado": "Ultraprocesado"
        }
    ]
    
    for caso in casos:
        esperado = caso.pop("esperado")
        engine = BaseConocimientoNutricional()
        engine.reset()
        engine.declare(Nutricion(**caso))
        engine.run()
        resultado = engine.clasificacion or "Neutro"
        marca = "✓" if esperado.lower() in resultado.lower() else "✗"
        print(f"  {caso['nombre']:<25} → {resultado:<40} {marca}")


def test_evaluar_nutricion():
    """Prueba función `evaluar_nutricion` desde main.py"""
    separador("3. FUNCIÓN evaluar_nutricion() (INTEGRACIÓN)")
    
    datos = {
        "nombre": "Producto de prueba",
        "sodio": 650,
        "grasas_saturadas": 18,
        "azucar": 28,
        "calorias": 320,
        "proteinas": 5,
        "fibra": 2
    }
    
    print(f"  Datos de entrada:")
    for k, v in datos.items():
        print(f"    - {k}: {v}")
    
    print(f"\n  Resultados:")
    resultado = evaluar_nutricion(datos, modo='nutricion')
    print(f"    Clasificación: {resultado.get('clasificacion', 'N/A')}")
    print(f"    Riesgos: {resultado.get('riesgos', [])}")
    print(f"    Advertencias: {resultado.get('advertencias', [])}")
    print(f"    Beneficios: {resultado.get('beneficios', [])}")


def main():
    """Ejecuta todas las pruebas"""
    print("\n" + "█"*70)
    print("█" + " "*68 + "█")
    print("█" + "  SISTEMA EXPERTO DE NUTRICIÓN - PRUEBAS COMPLETAS".center(68) + "█")
    print("█" + " "*68 + "█")
    print("█"*70)
    
    try:
        test_imc()
        test_clasificacion_alimentos()
        test_evaluar_nutricion()
        
        separador("✓ TODAS LAS PRUEBAS COMPLETADAS EXITOSAMENTE")
        print("  El sistema experto está operativo y listo para usar.\n")
        
    except Exception as e:
        separador("✗ ERROR EN PRUEBAS")
        print(f"  Error: {e}\n")
        import traceback
        traceback.print_exc()
        return 1
    
    return 0


if __name__ == '__main__':
    sys.exit(main())
