# scripts/cargar_habitos_alimentarios.py
import os
import django
import sys

# Configurar Django
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'sistema_nutricion.settings')
django.setup()

from nutricion.models import HabitoAlimentario

def cargar_habitos_alimentarios():
    """Carga 10 hábitos alimentarios de ejemplo en la base de datos"""
    
    habitos_data = [
        {
            'nombre': 'Dieta mediterránea',
            'descripcion': 'Alto consumo de frutas, verduras, pescado y aceite de oliva'
        },
        {
            'nombre': 'Vegetarianismo',
            'descripcion': 'Exclusión de carnes y pescados, consumo de vegetales, lácteos y huevos'
        },
        {
            'nombre': 'Veganismo',
            'descripcion': 'Exclusión total de productos de origen animal'
        },
        {
            'nombre': 'Dieta baja en carbohidratos',
            'descripcion': 'Reducción del consumo de azúcares y harinas'
        },
        {
            'nombre': 'Alimentación intuitiva',
            'descripcion': 'Comer según las señales de hambre y saciedad del cuerpo'
        },
        {
            'nombre': 'Ayuno intermitente',
            'descripcion': 'Ciclos entre periodos de alimentación y ayuno'
        },
        {
            'nombre': 'Dieta alta en proteínas',
            'descripcion': 'Enfoque en consumo de carnes, huevos y legumbres'
        },
        {
            'nombre': 'Alimentación emocional',
            'descripcion': 'Tendencia a comer en respuesta a emociones más que a hambre física'
        },
        {
            'nombre': 'Comida rápida frecuente',
            'descripcion': 'Consumo regular de alimentos procesados y comida chatarra'
        },
        {
            'nombre': 'Alimentación consciente',
            'descripcion': 'Atención plena durante las comidas, masticación lenta'
        }
    ]
    
    habitos_creados = []
    
    for dato in habitos_data:
        # Verificar si el hábito ya existe
        if not HabitoAlimentario.objects.filter(nombre=dato['nombre']).exists():
            habito = HabitoAlimentario.objects.create(
                nombre=dato['nombre'],
                descripcion=dato['descripcion']
            )
            habitos_creados.append(habito)
            print(f"[OK] Habito creado: {habito.nombre}")
        else:
            print(f"[WARN] Habito ya existe: {dato['nombre']}")
    
    print(f"\n[SUCCESS] Se crearon {len(habitos_creados)} habitos nuevos")
    return habitos_creados

if __name__ == '__main__':
    cargar_habitos_alimentarios()