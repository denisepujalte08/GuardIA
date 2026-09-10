"""
correr_evaluacion.py

Corre el dataset sintético (dataset.py) contra el motor de deteccion
real y calcula las metricas de la Etapa 4: precision, recall, tasa de
falsos positivos/negativos y tiempo de respuesta promedio.

Uso (desde backend/, con el venv activado):

    python -m evaluacion.correr_evaluacion

Genera un resumen por consola y guarda el detalle en
evaluacion/resultados.json para el informe final.
"""

import json
import time
from pathlib import Path

from app.detection import analizar_texto
from evaluacion.dataset import DATASET

NIVELES_POSITIVOS = {"medio", "alto", "critico"}  # "hay algo sensible"


def evaluar() -> dict:
    detalle = []
    tiempos = []

    verdaderos_positivos = 0
    falsos_positivos = 0
    verdaderos_negativos = 0
    falsos_negativos = 0
    coincidencia_exacta_nivel = 0
    coincidencia_exacta_tipo = 0

    for caso in DATASET:
        inicio = time.perf_counter()
        resultado = analizar_texto(caso.texto)
        duracion_ms = (time.perf_counter() - inicio) * 1000
        tiempos.append(duracion_ms)

        esperado_positivo = caso.nivel_esperado in NIVELES_POSITIVOS
        obtenido_positivo = resultado.nivel_riesgo in NIVELES_POSITIVOS

        if esperado_positivo and obtenido_positivo:
            verdaderos_positivos += 1
        elif esperado_positivo and not obtenido_positivo:
            falsos_negativos += 1
        elif not esperado_positivo and obtenido_positivo:
            falsos_positivos += 1
        else:
            verdaderos_negativos += 1

        nivel_ok = resultado.nivel_riesgo == caso.nivel_esperado
        tipo_ok = resultado.tipo_dato_detectado == caso.tipo_esperado
        if nivel_ok:
            coincidencia_exacta_nivel += 1
        if tipo_ok:
            coincidencia_exacta_tipo += 1

        detalle.append(
            {
                "texto": caso.texto,
                "categoria": caso.categoria,
                "nivel_esperado": caso.nivel_esperado,
                "nivel_obtenido": resultado.nivel_riesgo,
                "tipo_esperado": caso.tipo_esperado,
                "tipo_obtenido": resultado.tipo_dato_detectado,
                "nivel_correcto": nivel_ok,
                "tipo_correcto": tipo_ok,
                "tiempo_ms": round(duracion_ms, 3),
            }
        )

    total = len(DATASET)
    precision = verdaderos_positivos / (verdaderos_positivos + falsos_positivos) if (verdaderos_positivos + falsos_positivos) else 0.0
    recall = verdaderos_positivos / (verdaderos_positivos + falsos_negativos) if (verdaderos_positivos + falsos_negativos) else 0.0
    f1 = 2 * precision * recall / (precision + recall) if (precision + recall) else 0.0

    resumen = {
        "total_casos": total,
        "accuracy_nivel_exacto": coincidencia_exacta_nivel / total,
        "accuracy_tipo_exacto": coincidencia_exacta_tipo / total,
        "deteccion_binaria": {
            "verdaderos_positivos": verdaderos_positivos,
            "falsos_positivos": falsos_positivos,
            "verdaderos_negativos": verdaderos_negativos,
            "falsos_negativos": falsos_negativos,
            "precision": precision,
            "recall": recall,
            "f1_score": f1,
        },
        "tiempo_respuesta_ms": {
            "promedio": sum(tiempos) / len(tiempos),
            "maximo": max(tiempos),
            "minimo": min(tiempos),
        },
    }

    return {"resumen": resumen, "detalle": detalle}


def imprimir_resumen(resultado: dict) -> None:
    r = resultado["resumen"]
    print(f"Total de casos evaluados: {r['total_casos']}")
    print(f"Accuracy (nivel de riesgo exacto):  {r['accuracy_nivel_exacto']:.1%}")
    print(f"Accuracy (tipo de dato exacto):     {r['accuracy_tipo_exacto']:.1%}")
    print()
    db = r["deteccion_binaria"]
    print("Deteccion binaria (¿hay algo sensible o no?):")
    print(f"  Verdaderos positivos: {db['verdaderos_positivos']}")
    print(f"  Falsos positivos:     {db['falsos_positivos']}")
    print(f"  Verdaderos negativos: {db['verdaderos_negativos']}")
    print(f"  Falsos negativos:     {db['falsos_negativos']}")
    print(f"  Precision: {db['precision']:.1%}")
    print(f"  Recall:    {db['recall']:.1%}")
    print(f"  F1-score:  {db['f1_score']:.1%}")
    print()
    t = r["tiempo_respuesta_ms"]
    print(f"Tiempo de respuesta: promedio {t['promedio']:.2f} ms, min {t['minimo']:.2f} ms, max {t['maximo']:.2f} ms")
    print()
    print("Casos donde el motor no coincidio con lo esperado:")
    fallos = [d for d in resultado["detalle"] if not d["nivel_correcto"]]
    if not fallos:
        print("  (ninguno)")
    for d in fallos:
        print(f"  - \"{d['texto']}\" -> esperado: {d['nivel_esperado']}, obtenido: {d['nivel_obtenido']}")


if __name__ == "__main__":
    resultado = evaluar()
    imprimir_resumen(resultado)

    salida = Path(__file__).parent / "resultados.json"
    salida.write_text(json.dumps(resultado, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"\nDetalle completo guardado en {salida}")
