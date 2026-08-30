"""
store.py

Registro de eventos en memoria. Alcanza para desarrollo y para las
simulaciones de la Etapa 4; queda aislado en este módulo justamente
para que reemplazarlo por una base de datos real (SQLite/Postgres) el
día de mañana implique tocar solo este archivo, no los endpoints.
"""

import itertools
import uuid
from datetime import datetime, timezone
from typing import Optional

from .schemas import Evento

_eventos: dict[str, Evento] = {}
_contador = itertools.count(1)


def crear_evento(
    usuario_id: str,
    ia_destino: str,
    nivel_riesgo: str,
    tipo_dato_detectado: Optional[str],
    mensaje_contextual: Optional[str],
) -> Evento:
    evento = Evento(
        id=f"evt-{next(_contador)}-{uuid.uuid4().hex[:6]}",
        usuario_id=usuario_id,
        ia_destino=ia_destino,
        nivel_riesgo=nivel_riesgo,
        tipo_dato_detectado=tipo_dato_detectado,
        mensaje_contextual=mensaje_contextual,
        accion="permitido_automatico" if nivel_riesgo == "bajo" else None,
        timestamp=datetime.now(timezone.utc),
    )
    _eventos[evento.id] = evento
    return evento


def actualizar_accion(evento_id: str, accion: str) -> Optional[Evento]:
    evento = _eventos.get(evento_id)
    if not evento:
        return None
    evento.accion = accion
    return evento


def listar_eventos(
    usuario_id: Optional[str] = None,
    ia_destino: Optional[str] = None,
    nivel_riesgo: Optional[str] = None,
) -> list[Evento]:
    eventos = list(_eventos.values())
    if usuario_id:
        eventos = [e for e in eventos if e.usuario_id == usuario_id]
    if ia_destino:
        eventos = [e for e in eventos if e.ia_destino == ia_destino]
    if nivel_riesgo:
        eventos = [e for e in eventos if e.nivel_riesgo == nivel_riesgo]
    return sorted(eventos, key=lambda e: e.timestamp, reverse=True)
