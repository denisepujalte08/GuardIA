"""
schemas.py

Formaliza como modelos Pydantic el contrato ya consolidado en el marco
conceptual entre la extensión, el backend y el dashboard. Cualquier
cambio a este contrato debería discutirse en conjunto (Zaira y Denise)
porque impacta a los tres componentes.
"""

from datetime import datetime
from typing import Literal, Optional

from pydantic import BaseModel, Field

NivelRiesgo = Literal["bajo", "medio", "alto", "critico"]
Accion = Literal["permitido_automatico", "editar", "cancelar", "continuar"]

# Campos opcionales usados solo durante las simulaciones de la Etapa 4
# (ver docs/diseno_simulacion_etapa4.md). En uso real de la extensión
# quedan en null.
Perfil = Literal["cuidadoso", "apurado", "esceptico"]
Condicion = Literal["contextual", "generico"]


class AnalizarRequest(BaseModel):
    texto: str = Field(..., min_length=1, description="Texto capturado por el content script antes del envío")
    usuario_id: str
    ia_destino: Literal["chatgpt", "gemini", "claude"]
    perfil: Optional[Perfil] = None
    condicion: Optional[Condicion] = None


class AnalizarResponse(BaseModel):
    evento_id: str
    nivel_riesgo: NivelRiesgo
    tipo_dato_detectado: Optional[str] = None
    fragmento_detectado: Optional[str] = None
    mensaje_contextual: Optional[str] = None


class ActualizarAccionRequest(BaseModel):
    accion: Accion


class Evento(BaseModel):
    id: str
    usuario_id: str
    ia_destino: str
    nivel_riesgo: NivelRiesgo
    tipo_dato_detectado: Optional[str] = None
    mensaje_contextual: Optional[str] = None
    accion: Optional[Accion] = None
    perfil: Optional[Perfil] = None
    condicion: Optional[Condicion] = None
    timestamp: datetime


class EventosResponse(BaseModel):
    eventos: list[Evento]
    total: int
