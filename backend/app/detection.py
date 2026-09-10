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

import spacy

_nlp = spacy.load("es_core_news_sm")


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
        nivel="critico",
        mensaje=(
            "El CUIT/CUIL es un identificador personal protegido por la Ley 25.326. "
            "Enviarlo a una IA externa lo expone fuera del control de la empresa."
        ),
    ),
    Regla(
        tipo="CBU",
        patron=re.compile(r"\b\d{22}\b"),
        nivel="critico",
        mensaje="Detectamos un CBU en el texto: es información financiera sensible de un cliente o de la empresa.",
    ),
    Regla(
        tipo="Credencial o token",
        patron=re.compile(
            r"\b(api[_-]?key|token|password|contrase[ñn]a|clave|secret|credencial(?:es)?)\b"
            r"\s*(?:es|son|[:=])?\s*\S+",
            re.IGNORECASE,
        ),
        nivel="critico",
        mensaje="El texto parece incluir una credencial o clave de acceso, lo que puede comprometer sistemas de la empresa.",
    ),
    Regla(
        tipo="DNI",
        patron=re.compile(r"\b\d{1,2}[.\s]\d{3}[.\s]\d{3}\b|\b\d{7,8}\b"),
        nivel="alto",
        mensaje="Detectamos un DNI en el texto: es un dato personal protegido por la Ley 25.326.",
    ),
    Regla(
        tipo="Teléfono",
        patron=re.compile(r"\b(?:\+?54[\s.-]?)?(?:9[\s.-]?)?\d{2,4}[\s.-]\d{3,4}[\s.-]?\d{3,4}\b|\b\d{10}\b"),
        nivel="alto",
        mensaje="Detectamos un número de teléfono en el texto: puede tratarse de un dato personal de un cliente o proveedor.",
    ),
    Regla(
        tipo="Correo electrónico",
        patron=re.compile(r"[\w.+-]+@[\w-]+\.[a-zA-Z]{2,}"),
        nivel="alto",
        mensaje="Detectamos una dirección de correo electrónico, posible dato personal de un cliente o proveedor.",
    ),
]


TERMINOS_PROPIETARIOS = [
    "sistema interno",
    "proyecto confidencial",
    # Lista de ejemplo. En una PyME real, se completaría con los nombres
    # propios de sus sistemas, productos o proyectos internos.
]

_PATRON_CODIGO = re.compile(r"\b(def|function|class|const|var|let|import)\b|[{};]")
_PATRON_TERMINO_PROPIETARIO = re.compile(
    r"\b(" + "|".join(re.escape(t) for t in TERMINOS_PROPIETARIOS) + r")\b",
    re.IGNORECASE,
)


def analizar_codigo_propietario(texto: str) -> Optional[ResultadoAnalisis]:
    """
    Detecta código fuente combinado con una referencia a un término propio
    de la empresa (configurable en TERMINOS_PROPIETARIOS). Exigir ambas
    señales a la vez evita marcar como riesgo cualquier código genérico
    (por ejemplo, un ejercicio de programación sin nada sensible).
    """
    match_termino = _PATRON_TERMINO_PROPIETARIO.search(texto)
    if _PATRON_CODIGO.search(texto) and match_termino:
        return ResultadoAnalisis(
            nivel_riesgo="alto",
            tipo_dato_detectado="Código o información propietaria",
            fragmento_detectado=match_termino.group(0),
            mensaje_contextual=(
                "El texto parece contener código junto con una referencia a un sistema o "
                "proyecto interno de la empresa. Compartir código propietario con una IA "
                "externa puede exponer lógica de negocio o secretos comerciales."
            ),
        )
    return None


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


_ETIQUETAS_ENTIDAD = {
    "PER": (
        "Nombre de persona",
        "Detectamos el nombre de una persona en el texto. Puede tratarse de un dato personal "
        "de un cliente, empleado o proveedor; compartirlo con una IA externa puede exponer "
        "información protegida por la Ley 25.326.",
    ),
    "ORG": (
        "Nombre de organización",
        "Detectamos el nombre de una organización o empresa en el texto. Puede tratarse de un "
        "dato comercial sensible (un cliente, proveedor o competidor); conviene revisar si es "
        "necesario incluirlo antes de enviarlo a una IA externa.",
    ),
}


def analizar_con_nlp(texto: str) -> Optional[ResultadoAnalisis]:
    """
    Detección de entidades nombradas (NER) con spaCy: cubre nombres propios y
    organizaciones que no siguen un patrón fijo y por eso no son capturables
    con expresiones regulares. Solo se ejecuta cuando `analizar_con_reglas`
    no encontró nada, según el orden definido en `analizar_texto`.
    """
    doc = _nlp(texto)
    for ent in doc.ents:
        if ent.label_ in _ETIQUETAS_ENTIDAD:
            tipo, mensaje = _ETIQUETAS_ENTIDAD[ent.label_]
            return ResultadoAnalisis(
                nivel_riesgo="medio",
                tipo_dato_detectado=tipo,
                fragmento_detectado=ent.text,
                mensaje_contextual=mensaje,
            )
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

    resultado = analizar_codigo_propietario(texto)
    if resultado:
        return resultado

    if _PATRON_CODIGO.search(texto):
        # Es código sin ningún término propietario: no se manda a la capa
        # de NLP, que no es confiable con sintaxis de código (spaCy puede
        # confundir identificadores de código con nombres de organización).
        return ResultadoAnalisis(
            nivel_riesgo="bajo",
            tipo_dato_detectado=None,
            fragmento_detectado=None,
            mensaje_contextual=None,
        )

    resultado = analizar_con_nlp(texto)
    if resultado:
        return resultado

    return ResultadoAnalisis(
        nivel_riesgo="bajo",
        tipo_dato_detectado=None,
        fragmento_detectado=None,
        mensaje_contextual=None,
    )
