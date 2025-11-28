from experta import *
from datetime import datetime, timedelta


class Alimento(Fact):
    """Datos de un alimento."""
    pass


class MotorAlimentos(KnowledgeEngine):

    # --- Clasificación por calorías ---
    @Rule(Alimento(calorias=P(lambda c: c < 100)))
    def bajo_en_calorias(self):
        print("→ Clasificación: Bajo en calorías")

    @Rule(Alimento(calorias=P(lambda c: 100 <= c < 250)))
    def moderado_en_calorias(self):
        print("→ Clasificación: Moderado en calorías")

    @Rule(Alimento(calorias=P(lambda c: c >= 250)))
    def alto_en_calorias(self):
        print("→ Clasificación: Alto en calorías")

    # --- Clasificación por macronutrientes ---
    @Rule(Alimento(proteinas=P(lambda p: p > 15)))
    def rico_en_proteinas(self):
        print("→ Clasificación: Rico en proteínas")

    @Rule(Alimento(grasas=P(lambda g: g > 20)))
    def alto_en_grasas(self):
        print("→ Clasificación: Alto en grasas")

    @Rule(Alimento(carbohidratos=P(lambda c: c > 30)))
    def alto_en_carbohidratos(self):
        print("→ Clasificación: Alto en carbohidratos")

    # --- Detección de alimentos próximos a vencer ---
    @Rule(Alimento(fecha_vencimiento=P(lambda f: (f - datetime.now()).days <= 3)))
    def proximo_a_vencer(self):
        print("⚠ Advertencia: El alimento está próximo a vencer")

    # --- Alimento vencido ---
    @Rule(Alimento(fecha_vencimiento=P(lambda f: f < datetime.now())))
    def vencido(self):
        print("❌ ALERTA: El alimento está vencido")

    # --- Control de stock ---
    @Rule(Alimento(stock=P(lambda s: s == 0)))
    def sin_stock(self):
        print("⚠ Sin stock disponible")

    @Rule(Alimento(stock=P(lambda s: 0 < s <= 5)))
    def stock_bajo(self):
        print("⚠ Stock bajo, considerar reponer")

    # --- Sugerencias nutricionales ---
    @Rule(Alimento(sodio=P(lambda s: s > 600)))
    def alto_en_sodio(self):
        print("⚠ Sugerencia: Alto en sodio, limitar consumo")

    @Rule(Alimento(grasas=P(lambda g: g > 20),
                   proteinas=P(lambda p: p < 10)))
    def no_saludable(self):
        print("⚠ Sugerencia: Alto en grasas y bajo en proteínas. No es saludable.")

    @Rule(Alimento(fibra=P(lambda f: f > 5)))
    def bueno_para_digestion(self):
        print("→ Recomendación: Bueno para la digestión")
