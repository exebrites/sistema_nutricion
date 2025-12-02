# load_alimentos.py
import os
import django
import random
import sys
from datetime import date, timedelta

# Configurar Django
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'sistema_nutricion.settings')
django.setup()

from nutricion.models import Alimento

def crear_alimentos():
    # Lista de nombres de alimentos realistas
    nombres_alimentos = [
        "Manzana", "Plátano", "Naranja", "Pera", "Uva", "Fresa", "Kiwi", "Mango", 
        "Piña", "Sandía", "Melón", "Zanahoria", "Brócoli", "Espinaca", "Lechuga",
        "Tomate", "Pepino", "Cebolla", "Ajo", "Pimiento", "Papa", "Batata", 
        "Arroz Integral", "Arroz Blanco", "Quinoa", "Avena", "Pan Integral",
        "Pan Blanco", "Pasta Integral", "Pasta Regular", "Lentejas", "Garbanzos",
        "Frijoles Negros", "Soja", "Tofu", "Pechuga de Pollo", "Muslo de Pollo",
        "Salmón", "Atún", "Trucha", "Camarón", "Huevo", "Leche Entera", 
        "Leche Desnatada", "Yogur Natural", "Queso Cheddar", "Queso Mozzarella",
        "Mantequilla", "Aceite de Oliva", "Aguacate", "Almendra", "Nuez",
        "Cacahuete", "Pistacho", "Semillas de Chía", "Semillas de Lino",
        "Chocolate Negro", "Miel", "Azúcar", "Sal", "Pimienta", "Canela",
        "Café", "Té Verde", "Zumo de Naranja", "Agua", "Refresco", "Cerveza",
        "Vino Tinto", "Pizza", "Hamburguesa", "Hot Dog", "Ensalada César",
        "Sopa de Tomate", "Sándwich de Pavo", "Tortilla", "Puré de Papa",
        "Pescado Frito", "Pollo Asado", "Cerdo a la Plancha", "Ternera",
        "Cordero", "Cangrejo", "Mejillón", "Almeja", "Calamares", "Anchoa",
        "Sardina", "Caballa", "Bacalao", "Merluza", "Rape", "Lubina",
        "Dorada", "Langosta", "Langostino", "Pulpo", "Centollo", "Bogavante"
    ]
    
    alimentos_creados = 0
    
    for i in range(100):
        # Seleccionar nombre aleatorio
        nombre = random.choice(nombres_alimentos)
        
        # Generar valores nutricionales realistas
        calorias = random.randint(50, 500)
        proteinas = random.randint(1, 40)
        grasas = random.randint(1, 30)
        carbohidratos = random.randint(5, 80)
        sodio = random.randint(0, 500)
        stock = random.randint(10, 200)
        
        # Generar fecha de vencimiento (entre 30 y 365 días desde hoy)
        dias_vencimiento = random.randint(30, 365)
        fecha_vencimiento = date.today() + timedelta(days=dias_vencimiento)
        
        try:
            # Crear el alimento
            alimento = Alimento(
                nombre=f"{nombre} #{i+1}",
                calorias=calorias,
                proteinas=proteinas,
                grasas=grasas,
                carbohidratos=carbohidratos,
                sodio=sodio,
                fecha_vencimiento=fecha_vencimiento,
                stock=stock
            )
            alimento.save()
            alimentos_creados += 1
            print(f"✅ Creado: {alimento.nombre}")
            
        except Exception as e:
            print(f"❌ Error creando alimento: {e}")
    
    print(f"\n🎉 ¡Se crearon {alimentos_creados} alimentos exitosamente!")

if __name__ == "__main__":
    crear_alimentos()