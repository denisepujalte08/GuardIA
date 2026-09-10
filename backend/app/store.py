"""
store.py

Registro de eventos persistido en SQLite. Reemplaza el store en memoria
original (un diccionario en RAM, que perdía todos los eventos cada vez
que el proceso se reiniciaba, por ejemplo con `uvicorn --reload`).

La interfaz pública (`crear_evento`, `actualizar_accion`,
`listar_eventos`) es exactamente la misma que antes, así que `main.py`
no necesita cambios: solo cambió cómo se guardan los datos puertas
adentro de este módulo.
"""

import sqlite3
import uuid
from datetime import datetime, timezone
from pathlib import Path
from typing import Optional

from .schemas import Evento

_DB_PATH = Path(__file__).resolve().parent.parent / "dlp.db"


def _conectar() -> sqlite3.Connection:
    conn = sqlite3.connect(_DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def _crear_tabla() -> None:
    with _conectar() as conn:
        conn.execute(
            """
            CREATE TABLE IF NOT EXISTS eventos (
                id TEXT PRIMARY KEY,
                usuario_id TEXT NOT NULL,
                ia_destino TEXT NOT NULL,
                nivel_riesgo TEXT NOT NULL,
                tipo_dato_detectado TEXT,
                mensaje_contextual TEXT,
                accion TEXT,
                perfil TEXT,
                condicion TEXT,
                timestamp TEXT NOT NULL
            )
            """
        )


_crear_tabla()


def _fila_a_evento(fila: sqlite3.Row) -> Evento:
    return Evento(
        id=fila["id"],
        usuario_id=fila["usuario_id"],
        ia_destino=fila["ia_destino"],
        nivel_riesgo=fila["nivel_riesgo"],
        tipo_dato_detectado=fila["tipo_dato_detectado"],
        mensaje_contextual=fila["mensaje_contextual"],
        accion=fila["accion"],
        perfil=fila["perfil"],
        condicion=fila["condicion"],
        timestamp=datetime.fromisoformat(fila["timestamp"]),
    )


def crear_evento(
    usuario_id: str,
    ia_destino: str,
    nivel_riesgo: str,
    tipo_dato_detectado: Optional[str],
    mensaje_contextual: Optional[str],
    perfil: Optional[str] = None,
    condicion: Optional[str] = None,
) -> Evento:
    evento = Evento(
        id=f"evt-{uuid.uuid4().hex[:10]}",
        usuario_id=usuario_id,
        ia_destino=ia_destino,
        nivel_riesgo=nivel_riesgo,
        tipo_dato_detectado=tipo_dato_detectado,
        mensaje_contextual=mensaje_contextual,
        accion="permitido_automatico" if nivel_riesgo == "bajo" else None,
        perfil=perfil,
        condicion=condicion,
        timestamp=datetime.now(timezone.utc),
    )
    with _conectar() as conn:
        conn.execute(
            """
            INSERT INTO eventos
                (id, usuario_id, ia_destino, nivel_riesgo, tipo_dato_detectado,
                 mensaje_contextual, accion, perfil, condicion, timestamp)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """,
            (
                evento.id,
                evento.usuario_id,
                evento.ia_destino,
                evento.nivel_riesgo,
                evento.tipo_dato_detectado,
                evento.mensaje_contextual,
                evento.accion,
                evento.perfil,
                evento.condicion,
                evento.timestamp.isoformat(),
            ),
        )
    return evento


def actualizar_accion(evento_id: str, accion: str) -> Optional[Evento]:
    with _conectar() as conn:
        conn.execute("UPDATE eventos SET accion = ? WHERE id = ?", (accion, evento_id))
        fila = conn.execute("SELECT * FROM eventos WHERE id = ?", (evento_id,)).fetchone()
    return _fila_a_evento(fila) if fila else None


def listar_eventos(
    usuario_id: Optional[str] = None,
    ia_destino: Optional[str] = None,
    nivel_riesgo: Optional[str] = None,
    perfil: Optional[str] = None,
    condicion: Optional[str] = None,
) -> list[Evento]:
    condiciones = []
    parametros: list[str] = []
    if usuario_id:
        condiciones.append("usuario_id = ?")
        parametros.append(usuario_id)
    if ia_destino:
        condiciones.append("ia_destino = ?")
        parametros.append(ia_destino)
    if nivel_riesgo:
        condiciones.append("nivel_riesgo = ?")
        parametros.append(nivel_riesgo)
    if perfil:
        condiciones.append("perfil = ?")
        parametros.append(perfil)
    if condicion:
        condiciones.append("condicion = ?")
        parametros.append(condicion)

    consulta = "SELECT * FROM eventos"
    if condiciones:
        consulta += " WHERE " + " AND ".join(condiciones)
    consulta += " ORDER BY timestamp DESC"

    with _conectar() as conn:
        filas = conn.execute(consulta, parametros).fetchall()
    return [_fila_a_evento(fila) for fila in filas]
