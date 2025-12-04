from django import forms
from .models import Alimento
from .system_experto import validar_alimento
from datetime import datetime


class AlimentoForm(forms.ModelForm):
    fecha_vencimiento = forms.DateField(
        required=False,
        widget=forms.DateInput(attrs={'type': 'date', 'class': 'form-control'})
    )
    class Meta:
        model = Alimento
        fields = "__all__"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs.update({'class': 'form-control'})

    def clean(self):
        cleaned = super().clean()

        # Manejar la fecha_vencimiento de forma segura
        fecha_vencimiento = cleaned.get("fecha_vencimiento")
        if fecha_vencimiento:
            # Si hay fecha, combinar con tiempo mínimo
            fecha_vencimiento_combinada = datetime.combine(
                fecha_vencimiento, datetime.min.time()
            )
        else:
            # Si no hay fecha, usar None o un valor por defecto
            fecha_vencimiento_combinada = None

        data = {
            "nombre": cleaned.get("nombre", ""),
            "calorias": cleaned.get("calorias", 0),
            "proteinas": cleaned.get("proteinas", 0),
            "grasas": cleaned.get("grasas", 0),
            "carbohidratos": cleaned.get("carbohidratos", 0),
            "sodio": cleaned.get("sodio", 0),
            "stock": cleaned.get("stock", 0),
            "fecha_vencimiento": fecha_vencimiento_combinada,
        }

        resultado = validar_alimento(data)
        
        # ERRORES → bloquean el guardado
        if resultado["errores"]:
            for e in resultado["errores"]:
                self.add_error(None, e)
        
        # Guardamos advertencias e info para mostrarlas en la vista
        self.advertencias = resultado["advertencias"]
        self.info = resultado["info"]

        return cleaned
