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
├── requirements.txt
└── .env.example
```

## Motor de detección — estado actual

- Reglas por expresiones regulares: CUIT/CUIL, CBU, credenciales/tokens,
  DNI, teléfono, correo electrónico.
- NLP con spaCy (`es_core_news_sm`): detección de nombres propios y
  organizaciones en texto libre.
- Detección de código propietario: combina sintaxis de código con una
  lista configurable de términos propios de la empresa
  (`TERMINOS_PROPIETARIOS` en `detection.py`).
- Registro de eventos persistido en SQLite (`backend/dlp.db`, no se
  versiona — ver `.gitignore`).
- 12 pruebas unitarias en `tests/test_detection.py` (correr con
  `python -m pytest -v` desde `backend/`).

## Próximos pasos (Etapa 4)

- Construir el dataset sintético de textos (seguros, sospechosos,
  críticos) para medir precisión, recall, falsos positivos/negativos y
  tiempo de respuesta.
- Ajustar reglas y umbrales a partir de los resultados obtenidos.
