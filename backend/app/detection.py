"""
detection.py

Motor de análisis de riesgo. Contiene:

  1. Un conjunto de reglas por expresiones regulares para los patrones
     estructurados (CUIT/CUIL, CBU, credenciales, email) — cubre la
     parte de "reglas configurables y expresiones regulares" descripta
     en el marco conceptual.

  2. Un punto de extensión explícito (`analizar_con_nlp`) para que
     Denise sume la capa de NLP/NER con spaCy (nombres propios,
     organizaciones, referencias implícitas a datos comerciales) sin
     tener que tocar el resto del backend: solo se completa esa
     función y se llama desde `analizar_texto`.

Este archivo es intencionalmente el punto de partida más simple
posible: reglas regex + una función de scoring. La idea es que Denise
lo extienda directamente acá (agregando patrones a REGLAS, o
completando `analizar_con_nlp`) en lugar de reescribir el módulo.
"""

import re
from dataclasses import dataclass
from typing import Optional


@dataclass
class ResultadoAnalisis:
    nivel_riesgo: str  # "bajo" | "medio" | "alto" | "critico"
    tipo_dato_detectado: Optional[str]
    fragmento_detectado: Optional[str]
    mensaje_contextual: Optional[str]


@dataclass
class Regla:
    tipo: str
    patron: re.Pattern
    nivel: str
    mensaje: str


REGLAS: list[Regla] = [
    Regla(
        tipo="CUIT/CUIL",
        patron=re.compile(r"\b\d{2}-?\d{8}-?\d\b"),
        nivel="alto",
        mensaje=(
            "El CUIT/CUIL es un identificador personal protegido por la Ley 25.326. "
            "Enviarlo a una IA externa lo expone fuera del control de la empresa."
        ),
    ),
    Regla(
        tipo="CBU",
        patron=re.compile(r"\b\d{22}\b"),
        nivel="alto",
        mensaje="Detectamos un CBU en el texto: es información financiera sensible de un cliente o de la empresa.",
    ),
    Regla(
        tipo="Credencial o token",
        patron=re.compile(r"(api[_-]?key|token|password|contrase[ñn]a|secret)\s*[:=]\s*\S+", re.IGNORECASE),
        nivel="critico",
        mensaje="El texto parece incluir una credencial o clave de acceso, lo que puede comprometer sistemas de la empresa.",
    ),
    Regla(
        tipo="Correo electrónico",
        patron=re.compile(r"[\w.+-]+@[\w-]+\.[a-zA-Z]{2,}"),
        nivel="medio",
        mensaje="Detectamos una dirección de correo electrónico, posible dato personal de un cliente o proveedor.",
    ),
]


def _extraer_fragmento(texto: str, match: re.Match) -> str:
    inicio = max(0, match.start() - 20)
    fin = min(len(texto), match.end() + 10)
    prefijo = "…" if inicio > 0 else ""
    sufijo = "…" if fin < len(texto) else ""
    return f"{prefijo}{texto[inicio:fin]}{sufijo}"


def analizar_con_reglas(texto: str) -> Optional[ResultadoAnalisis]:
    for regla in REGLAS:
        match = regla.patron.search(texto)
        if match:
            return ResultadoAnalisis(
                nivel_riesgo=regla.nivel,
                tipo_dato_detectado=regla.tipo,
                fragmento_detectado=_extraer_fragmento(texto, match),
                mensaje_contextual=regla.mensaje,
            )
    return None


def analizar_con_nlp(texto: str) -> Optional[ResultadoAnalisis]:
    """
    PUNTO DE EXTENSIÓN PARA DENISE.

    Acá va la capa de NLP/NER con spaCy: detección de nombres propios,
    organizaciones, código propietario y demás casos que no se resuelven
    con un patrón fijo. Por ahora no hace nada (devuelve None), para que
    `analizar_texto` caiga siempre en las reglas por regex.

    Sugerencia de forma de implementación, para no romper el contrato:

        import spacy
        _nlp = spacy.load("es_core_news_sm")

        def analizar_con_nlp(texto: str) -> Optional[ResultadoAnalisis]:
            doc = _nlp(texto)
            for ent in doc.ents:
                if ent.label_ in ("PER", "ORG"):
                    return ResultadoAnalisis(
                        nivel_riesgo="medio",
                        tipo_dato_detectado=f"Entidad detectada ({ent.label_})",
                        fragmento_detectado=ent.text,
                        mensaje_contextual="...",
                    )
            return None
    """
    return None


def analizar_texto(texto: str) -> ResultadoAnalisis:
    """
    Punto de entrada único del motor de análisis. Primero intenta con
    las reglas estructuradas (más precisas y baratas); si no matchean,
    delega en la capa de NLP. Si tampoco encuentra nada, el riesgo es
    bajo y se permite el envío automáticamente.
    """
    resultado = analizar_con_reglas(texto)
    if resultado:
        return resultado

    resultado = analizar_con_nlp(texto)
    if resultado:
        return resultado

    return ResultadoAnalisis(
        nivel_riesgo="bajo",
        tipo_dato_detectado=None,
        fragmento_detectado=None,
        mensaje_contextual=None,
    )
