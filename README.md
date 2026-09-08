# Sistema de Prevención de Fuga de Datos por IA (Shadow AI) — PYMES

Práctica Profesional Supervisada — UTN FRRe / CInApTIC.
Zaira Rosin (extensión + dashboard) y Denise Pujalte (backend de análisis).

## Estructura del repositorio

```
dlp-pyme/
├── extension/    # Extensión de navegador (Manifest V3) — Zaira
├── backend/       # API de análisis en FastAPI — Denise
├── dashboard/      # Panel de administración en React — Zaira
├── docs/            # Marco conceptual y demás documentación
└── .gitignore
```

Los tres componentes están desacoplados y se comunican por HTTP según
el contrato documentado en `docs/Marco_Conceptual_y_Arquitectura.docx`
(Sección 7). Cada uno tiene su propio README con instrucciones
puntuales.

## Cómo levantar todo en local

Se necesitan 3 terminales abiertas en simultáneo:

**1. Backend**

Requiere Python 3.11 (ver `backend/.python-version` y el README del backend para el detalle).

```bash
cd backend
py -3.11 -m venv .venv && .venv\Scripts\activate    # en Linux/Mac: python3.11 -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
python -m spacy download es_core_news_sm
uvicorn app.main:app --reload --port 8000
```

**2. Dashboard**
```bash
cd dashboard
npm install
npm run dev
```
Se abre en `http://localhost:5173`.

**3. Extensión**
En `chrome://extensions`: activar "Modo de desarrollador" → "Cargar
descomprimida" → seleccionar la carpeta `extension/`.

Con el backend corriendo, la extensión ya analiza contra el motor real
(reglas + NLP con spaCy) en vez del mock local.

## Subir esto a Git / GitHub

Desde la carpeta `dlp-pyme/`:

```bash
git init
git add .
git commit -m "Estructura inicial: extensión, backend y dashboard"
```

Crear el repositorio vacío en GitHub (sin README, sin .gitignore, para
no pisar lo que ya tenés) y después:

```bash
git branch -M main
git remote add origin https://github.com/<usuario-o-org>/dlp-pyme.git
git push -u origin main
```

Si van a trabajar cada una en su parte, una convención simple para dos
personas:

```bash
git checkout -b feature/backend-nlp        # Denise
git checkout -b feature/dashboard-metricas # Zaira
```

y luego Pull Request a `main` cuando cada parte esté lista para
integrarse, en vez de commitear directo a `main` para evitar pisarse
código entre las dos.

## Próximos pasos (Etapa 4)

- Denise: construir el dataset sintético de prueba y medir precisión,
  recall, falsos positivos/negativos y tiempo de respuesta del motor
  de detección (ver `backend/README.md`).
- Zaira: corregir el selector del botón de envío de ChatGPT en
  `extension/site-adapters.js` (no reconoce el aria-label en español),
  y sumar el historial de simulaciones al dashboard.
- Ambas: correr los casos de prueba de los tres perfiles de empleado
  definidos en el marco conceptual, para alimentar la matriz de
  resultados de la Etapa 4.
