# Backend de Análisis (FastAPI)

Expone el motor de análisis de riesgo y el registro de eventos.
Responsable: Denise Pujalte.

## Cómo correrlo

Requiere **Python 3.11** (ver `.python-version`): spaCy no instala de forma confiable con Python 3.13+ porque sus dependencias (`blis`, `thinc`) no tienen paquetes precompilados para esas versiones.

```bash
cd backend
py -3.11 -m venv .venv        # en Linux/Mac: python3.11 -m venv .venv
source .venv/bin/activate    # en Windows: .venv\Scripts\activate
pip install -r requirements.txt
python -m spacy download es_core_news_sm
uvicorn app.main:app --reload --port 8000
```

Documentación interactiva (Swagger) en http://localhost:8000/docs

## Estructura

```
backend/
├── app/
│   ├── main.py         # Endpoints (POST /analizar, PATCH /eventos/{id}, GET /eventos)
│   ├── schemas.py       # Contrato formal (Pydantic) compartido con extensión y dashboard
│   ├── detection.py      # Motor de reglas/regex + NLP (spaCy) + código propietario
│   └── store.py          # Registro de eventos persistido en SQLite (backend/dlp.db)
├── tests/
│   └── test_detection.py # Pruebas unitarias del motor de detección
├── evaluacion/
│   ├── dataset.py             # Dataset sintético de 36 casos (seguros/sospechosos/críticos)
│   ├── correr_evaluacion.py   # Corre el dataset contra el motor y calcula métricas
│   ├── exportar_simulacion.py # Exporta eventos de simulación (perfil/condicion)
│   └── matriz_resultados.py   # Combina simulaciones y arma la matriz de usabilidad
├── requirements.txt
└── .env.example
```

## Motor de detección — estado actual

- Reglas por expresiones regulares: CUIT/CUIL y CBU (nivel crítico),
  credenciales/tokens (crítico), DNI y teléfono (alto), correo
  electrónico (alto).
- NLP con spaCy (`es_core_news_sm`): detección de nombres propios y
  organizaciones en texto libre (nivel medio).
- Detección de código propietario: combina sintaxis de código con una
  lista configurable de términos propios de la empresa
  (`TERMINOS_PROPIETARIOS` en `detection.py`).
- Registro de eventos persistido en SQLite (`backend/dlp.db`, no se
  versiona — ver `.gitignore`).
- 15 pruebas unitarias en `tests/test_detection.py` (correr con
  `python -m pytest -v` desde `backend/`).

## Resultados de la evaluación (Etapa 4)

Sobre un dataset sintético de 36 casos (`evaluacion/dataset.py`), corrido con `python evaluacion/correr_evaluacion.py` desde `backend/`:

| Métrica | Valor |
|---|---|
| Accuracy (nivel de riesgo exacto) | 80,6% |
| Precisión / Recall / F1-score | 87,0% / 83,3% / 85,1% |
| Tiempo de respuesta promedio | 2,47 ms |

Los resultados completos quedan en `evaluacion/resultados.json`. La matriz de usabilidad (intervención contextual vs. bloqueo genérico, 36 eventos combinados con la simulación de Zaira) se genera con `python evaluacion/matriz_resultados.py` y queda en `evaluacion/matriz_resultados.json`.
