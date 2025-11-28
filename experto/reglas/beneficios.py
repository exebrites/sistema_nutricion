# reglas/beneficios.py
from experta import *
from experto.motor import Nutricion


@Rule(Nutricion(proteinas=P(lambda p: p >= 15)))
def beneficio_proteina(self):
    self.beneficios.append("Buena fuente de proteínas.")


@Rule(Nutricion(fibra=P(lambda f: f >= 5)))
def beneficio_fibra(self):
    self.beneficios.append("Alto en fibra: ayuda a la digestión.")


@Rule(Nutricion(vitaminas=P(lambda v: v is True)))
def beneficio_vitaminas(self):
    self.beneficios.append("Contiene vitaminas esenciales.")
