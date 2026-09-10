"""
exportar_simulacion.py

Exporta los eventos de simulacion (los que tienen perfil/condicion no
nulos) del backend local a un archivo JSON, para poder combinar los
resultados de Denise y Zaira -- cada una corre esto contra su propio
backend local y despues juntan los dos archivos.

Uso (desde backend/, con el venv activado y el backend NO hace falta
que este corriendo -- lee directo de dlp.db):

    python -m evaluacion.exportar_simulacion [nombre_opcional]

Genera evaluacion/simulacion_<nombre_opcional_o_fecha>.json
"""

import json
import sys
from datetime import datetime
from pathlib import Path

from app import store


def exportar(nombre: str | None = None) -> Path:
    eventos = store.listar_eventos()
    eventos_simulacion = [e for e in eventos if e.perfil is not None and e.condicion is not None]

    if not eventos_simulacion:
        print("No hay eventos de simulacion (perfil/condicion) en la base local.")
        print("Recorda correr las 18 combinaciones antes de exportar.")
        sys.exit(1)

    sufijo = nombre or datetime.now().strftime("%Y%m%d_%H%M%S")
    salida = Path(__file__).parent / f"simulacion_{sufijo}.json"

    datos = [
        {
            "id": e.id,
            "usuario_id": e.usuario_id,
            "ia_destino": e.ia_destino,
            "nivel_riesgo": e.nivel_riesgo,
            "tipo_dato_detectado": e.tipo_dato_detectado,
            "accion": e.accion,
            "perfil": e.perfil,
            "condicion": e.condicion,
            "timestamp": e.timestamp.isoformat(),
        }
        for e in eventos_simulacion
    ]

    salida.write_text(json.dumps(datos, ensure_ascii=False, indent=2), encoding="utf-8")

    print(f"Exportados {len(datos)} eventos de simulacion a {salida}")
    usuarios = sorted({d["usuario_id"] for d in datos})
    print(f"usuario_id encontrados: {usuarios}")
    return salida


if __name__ == "__main__":
    nombre_arg = sys.argv[1] if len(sys.argv) > 1 else None
    exportar(nombre_arg)
