# scripts/cargar_sintomas.py
import os
import django
import sys

# Configurar Django
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'sistema_nutricion.settings')
django.setup()

from nutricion.models import Sintoma

def cargar_sintomas():
    """Carga 10 síntomas de ejemplo en la base de datos"""
    
    sintomas_data = [
        {
            'nombre': 'Fatiga',
            'descripcion': 'Cansancio extremo y falta de energía'
        },
        {
            'nombre': 'Dolor de cabeza',
            'descripcion': 'Malestar o dolor en la cabeza o cuello'
        },
        {
            'nombre': 'Náuseas',
            'descripcion': 'Sensación de malestar estomacal con ganas de vomitar'
        },
        {
            'nombre': 'Mareos',
            'descripcion': 'Pérdida del equilibrio y sensación de vértigo'
        },
        {
            'nombre': 'Dolor abdominal',
            'descripcion': 'Molestia o dolor en la zona del abdomen'
        },
        {
            'nombre': 'Fiebre',
            'descripcion': 'Aumento de la temperatura corporal por encima de lo normal'
        },
        {
            'nombre': 'Tos persistente',
            'descripcion': 'Tos que dura más de lo normal y puede ser seca o con flemas'
        },
        {
            'nombre': 'Dificultad para respirar',
            'descripcion': 'Sensación de falta de aire o respiración entrecortada'
        },
        {
            'nombre': 'Pérdida de apetito',
            'descripcion': 'Falta de interés por la comida o reducción del hambre'
        },
        {
            'nombre': 'Insomnio',
            'descripcion': 'Dificultad para conciliar el sueño o mantenerlo'
        }
    ]
    
    sintomas_creados = []
    
    for dato in sintomas_data:
        # Verificar si el síntoma ya existe
        if not Sintoma.objects.filter(nombre=dato['nombre']).exists():
            sintoma = Sintoma.objects.create(
                nombre=dato['nombre'],
                descripcion=dato['descripcion']
            )
            sintomas_creados.append(sintoma)
            print(f"[OK] Sintoma creado: {sintoma.nombre}")
        else:
            print(f"[WARN] Sintoma ya existe: {dato['nombre']}")
    
    print(f"\n[SUCCESS] Se crearon {len(sintomas_creados)} sintomas nuevos")
    return sintomas_creados

if __name__ == '__main__':
    cargar_sintomas()