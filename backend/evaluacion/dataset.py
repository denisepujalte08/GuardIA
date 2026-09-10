"""
dataset.py

Dataset sintético de evaluación del motor de detección (Etapa 4).
Cada caso indica el texto de prueba, la categoria general definida en
el plan de trabajo (seguro / sospechoso / critico) y el nivel de riesgo
exacto que debería devolver `analizar_texto()` segun el diseño del
motor (bajo / medio / alto / critico).

No son casos reales: son textos sintéticos construidos para cubrir
cada tipo de patron que el motor debe reconocer.
"""

from dataclasses import dataclass


@dataclass
class CasoPrueba:
    texto: str
    categoria: str  # "seguro" | "sospechoso" | "critico"
    nivel_esperado: str  # "bajo" | "medio" | "alto" | "critico"
    tipo_esperado: str | None = None  # tipo_dato_detectado esperado, o None si nivel_esperado == "bajo"


DATASET: list[CasoPrueba] = [
    # --- Seguros: texto genérico, sin datos sensibles (nivel esperado: bajo) ---
    CasoPrueba("Necesito ayuda para escribir una función en Python que ordene una lista", "seguro", "bajo"),
    CasoPrueba("¿Cuál es la capital de Francia?", "seguro", "bajo"),
    CasoPrueba("Resumime este artículo sobre historia argentina", "seguro", "bajo"),
    CasoPrueba("Dame ideas para un cumpleaños sorpresa", "seguro", "bajo"),
    CasoPrueba("Explicame qué es la fotosíntesis", "seguro", "bajo"),
    CasoPrueba("Ayudame a traducir esta frase al inglés", "seguro", "bajo"),
    CasoPrueba("def ordenar_lista(numeros): return sorted(numeros)", "seguro", "bajo"),
    CasoPrueba("¿Qué diferencia hay entre un array y una lista enlazada?", "seguro", "bajo"),
    CasoPrueba("Escribime un poema corto sobre el otoño", "seguro", "bajo"),
    CasoPrueba("Necesito una receta de pastel de papas", "seguro", "bajo"),
    CasoPrueba("Cómo instalar Docker en Windows", "seguro", "bajo"),
    CasoPrueba("Dame un resumen de las reglas del ajedrez", "seguro", "bajo"),
    # --- Sospechosos: nombres propios / organizaciones en texto libre (nivel esperado: medio, via NLP) ---
    CasoPrueba("Envié el presupuesto a Juan Perez", "sospechoso", "medio", "Nombre de persona"),
    CasoPrueba("Hablé con María Gómez sobre el contrato", "sospechoso", "medio", "Nombre de persona"),
    CasoPrueba("El cliente se llama Carlos Fernandez", "sospechoso", "medio", "Nombre de persona"),
    CasoPrueba("Trabajo en Acindar desde hace 3 años", "sospechoso", "medio", "Nombre de organización"),
    CasoPrueba("La reunión es con Roberto Sánchez", "sospechoso", "medio", "Nombre de persona"),
    CasoPrueba("Contactate con Laura Martinez para coordinar", "sospechoso", "medio", "Nombre de persona"),
    CasoPrueba("El proveedor es Molinos Río de la Plata", "sospechoso", "medio", "Nombre de organización"),
    CasoPrueba("Le mandé el mensaje a Diego Ramirez", "sospechoso", "medio", "Nombre de persona"),
    CasoPrueba("La empresa Techint aprobó el presupuesto", "sospechoso", "medio", "Nombre de organización"),
    CasoPrueba("Coordiná con Ana Lopez la entrega", "sospechoso", "medio", "Nombre de persona"),
    CasoPrueba("El gerente es Pablo Torres", "sospechoso", "medio", "Nombre de persona"),
    CasoPrueba("Trabajamos con Mercado Libre en este proyecto", "sospechoso", "medio", "Nombre de organización"),
    # --- Críticos: datos con formato fijo, regex (nivel esperado: alto o critico) ---
    CasoPrueba("Mi CUIT es 20-38456712-4", "critico", "critico", "CUIT/CUIL"),
    CasoPrueba("El CBU es 2850590940090418135201", "critico", "critico", "CBU"),
    CasoPrueba("La api_key: sk-12345abcde", "critico", "critico", "Credencial o token"),
    CasoPrueba("Mi contraseña: SuperSecreta123", "critico", "critico", "Credencial o token"),
    CasoPrueba("Mi DNI es 30123456", "critico", "alto", "DNI"),
    CasoPrueba("Mi DNI es 30.123.456", "critico", "alto", "DNI"),
    CasoPrueba("Llamame al 3624 456789", "critico", "alto", "Teléfono"),
    CasoPrueba("Mandale un mail a cliente@empresa.com", "critico", "alto", "Correo electrónico"),
    CasoPrueba(
        "def calcular(cliente): return cliente.total  # parte del sistema interno",
        "critico",
        "alto",
        "Código o información propietaria",
    ),
    CasoPrueba("Mi CUIL es 27-30123456-5", "critico", "critico", "CUIT/CUIL"),
    CasoPrueba("El teléfono de la oficina es 011 4444-5555", "critico", "alto", "Teléfono"),
    CasoPrueba("token: abcdef123456", "critico", "critico", "Credencial o token"),
]
