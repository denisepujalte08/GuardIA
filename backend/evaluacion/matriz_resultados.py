"""
matriz_resultados.py

Combina los archivos simulacion_*.json (uno por integrante) y calcula
la matriz de resultados de usabilidad de la Etapa 4:

  - Tasa de aceptación de alertas (¿cuántas veces se eligió "continuar"
    cuando estaba disponible?) por perfil y por condicion.
  - Distribución de acciones (editar/cancelar/continuar) por perfil,
    condicion y nivel de riesgo.
  - Comparación directa contextual vs. generico por perfil.

Uso (desde backend/, con el venv activado):

    python -m evaluacion.matriz_resultados

Lee todos los archivos evaluacion/simulacion_*.json que encuentre y
guarda el resumen en evaluacion/matriz_resultados.json.
"""

import json
from collections import defaultdict
from pathlib import Path

CARPETA = Path(__file__).parent


def cargar_eventos() -> list[dict]:
    eventos = []
    for archivo in sorted(CARPETA.glob("simulacion_*.json")):
        datos = json.loads(archivo.read_text(encoding="utf-8"))
        for d in datos:
            d["_origen"] = archivo.stem
            eventos.append(d)
    return eventos


def calcular_matriz(eventos: list[dict]) -> dict:
    # Tasa de aceptación de alertas = continuar / total, por perfil y condicion
    # (solo tiene sentido en nivel "medio", donde "continuar" está disponible
    # en ambas condiciones; en alto/critico esa opción está deshabilitada).
    conteo_accion = defaultdict(lambda: defaultdict(int))
    conteo_total = defaultdict(int)

    for e in eventos:
        clave = (e["perfil"], e["condicion"], e["nivel_riesgo"])
        conteo_accion[clave][e["accion"]] += 1
        conteo_total[clave] += 1

    matriz = []
    for (perfil, condicion, nivel), total in sorted(conteo_total.items()):
        acciones = conteo_accion[(perfil, condicion, nivel)]
        matriz.append(
            {
                "perfil": perfil,
                "condicion": condicion,
                "nivel_riesgo": nivel,
                "total_casos": total,
                "editar": acciones.get("editar", 0),
                "cancelar": acciones.get("cancelar", 0),
                "continuar": acciones.get("continuar", 0),
                "tasa_continuar": round(acciones.get("continuar", 0) / total, 2) if total else 0.0,
            }
        )

    # Comparación agregada contextual vs. generico, por perfil (todos los niveles)
    comparacion = defaultdict(lambda: defaultdict(lambda: defaultdict(int)))
    for e in eventos:
        comparacion[e["perfil"]][e["condicion"]][e["accion"]] += 1

    comparacion_resumen = []
    for perfil, por_condicion in sorted(comparacion.items()):
        fila = {"perfil": perfil}
        for condicion in ("contextual", "generico"):
            acciones = por_condicion.get(condicion, {})
            total = sum(acciones.values())
            fila[condicion] = {
                "total": total,
                "editar": acciones.get("editar", 0),
                "cancelar": acciones.get("cancelar", 0),
                "continuar": acciones.get("continuar", 0),
            }
        comparacion_resumen.append(fila)

    origenes = sorted({e["_origen"] for e in eventos})

    return {
        "total_eventos": len(eventos),
        "origenes": origenes,
        "matriz_por_combinacion": matriz,
        "comparacion_contextual_vs_generico": comparacion_resumen,
    }


def imprimir(resultado: dict) -> None:
    print(f"Total de eventos combinados: {resultado['total_eventos']} (de: {', '.join(resultado['origenes'])})")
    print()
    print("Matriz por combinacion (perfil / condicion / nivel):")
    for fila in resultado["matriz_por_combinacion"]:
        print(
            f"  {fila['perfil']:<10} {fila['condicion']:<11} {fila['nivel_riesgo']:<8} "
            f"editar={fila['editar']} cancelar={fila['cancelar']} continuar={fila['continuar']} "
            f"(tasa continuar: {fila['tasa_continuar']:.0%})"
        )
    print()
    print("Comparacion contextual vs. generico, por perfil (todos los niveles):")
    for fila in resultado["comparacion_contextual_vs_generico"]:
        c = fila["contextual"]
        g = fila["generico"]
        print(f"  {fila['perfil']}:")
        print(f"    Contextual -> editar={c['editar']} cancelar={c['cancelar']} continuar={c['continuar']} (total {c['total']})")
        print(f"    Generico   -> editar={g['editar']} cancelar={g['cancelar']} continuar={g['continuar']} (total {g['total']})")


if __name__ == "__main__":
    eventos = cargar_eventos()
    if not eventos:
        print("No se encontraron archivos simulacion_*.json en evaluacion/.")
        raise SystemExit(1)

    resultado = calcular_matriz(eventos)
    imprimir(resultado)

    salida = CARPETA / "matriz_resultados.json"
    salida.write_text(json.dumps(resultado, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"\nMatriz completa guardada en {salida}")
