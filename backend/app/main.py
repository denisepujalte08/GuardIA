"""
main.py

Expone los 3 endpoints definidos en el contrato de comunicación:

    POST  /analizar        -> usado por la extensión (service worker)
    PATCH /eventos/{id}    -> usado por la extensión, para registrar
                              la acción elegida por el usuario en el modal
    GET   /eventos         -> usado por el dashboard (listado + métricas)

Para correrlo localmente:

    cd backend
    python -m venv .venv && source .venv/bin/activate
    pip install -r requirements.txt
    uvicorn app.main:app --reload --port 8000

Documentación interactiva disponible en http://localhost:8000/docs
"""

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware

from . import store
from .detection import analizar_texto
from .schemas import (
    ActualizarAccionRequest,
    AnalizarRequest,
    AnalizarResponse,
    Evento,
    EventosResponse,
)

app = FastAPI(
    title="DLP PyME - Backend de Análisis",
    description="Motor de análisis y registro de eventos del sistema de prevención de fuga de datos por IA.",
    version="0.1.0",
)

# Durante el desarrollo, la extensión y el dashboard corren en orígenes
# distintos al del backend. Se habilita CORS abierto solo para este
# entorno; en producción conviene restringirlo a los orígenes reales.
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/", tags=["salud"])
def salud():
    return {"status": "ok", "servicio": "dlp-pyme-backend"}


@app.post("/analizar", response_model=AnalizarResponse, tags=["analisis"])
def analizar(request: AnalizarRequest):
    resultado = analizar_texto(request.texto)

    evento = store.crear_evento(
        usuario_id=request.usuario_id,
        ia_destino=request.ia_destino,
        nivel_riesgo=resultado.nivel_riesgo,
        tipo_dato_detectado=resultado.tipo_dato_detectado,
        mensaje_contextual=resultado.mensaje_contextual,
    )

    return AnalizarResponse(
        evento_id=evento.id,
        nivel_riesgo=resultado.nivel_riesgo,
        tipo_dato_detectado=resultado.tipo_dato_detectado,
        fragmento_detectado=resultado.fragmento_detectado,
        mensaje_contextual=resultado.mensaje_contextual,
    )


@app.patch("/eventos/{evento_id}", response_model=Evento, tags=["eventos"])
def actualizar_accion(evento_id: str, request: ActualizarAccionRequest):
    evento = store.actualizar_accion(evento_id, request.accion)
    if not evento:
        raise HTTPException(status_code=404, detail="Evento no encontrado")
    return evento


@app.get("/eventos", response_model=EventosResponse, tags=["eventos"])
def listar_eventos(usuario_id: str | None = None, ia_destino: str | None = None, nivel_riesgo: str | None = None):
    eventos = store.listar_eventos(usuario_id=usuario_id, ia_destino=ia_destino, nivel_riesgo=nivel_riesgo)
    return EventosResponse(eventos=eventos, total=len(eventos))
