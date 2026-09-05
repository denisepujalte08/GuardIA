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
│   ├── detection.py      # Motor de reglas/regex + punto de extensión para NLP (spaCy)
│   └── store.py          # Registro de eventos en memoria (reemplazable por DB)
├── requirements.txt
└── .env.example
```

## Próximos pasos (Etapa 3)

- Completar `analizar_con_nlp()` en `detection.py` con spaCy (NER de
  nombres propios, organizaciones, código propietario).
- Reemplazar `store.py` (en memoria) por una base de datos persistente.
- Sumar tests unitarios sobre las reglas de detección con el dataset
  sintético mencionado en el marco conceptual.
