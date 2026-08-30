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
```bash
cd backend
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
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
(reglas por ahora; NLP con spaCy es el próximo paso de Denise) en vez
del mock local.

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

## Próximos pasos (Etapa 3 / Etapa 4)

- Denise: completar `analizar_con_nlp()` en `backend/app/detection.py`
  con spaCy, y reemplazar el store en memoria por una base de datos.
- Zaira: validar los selectores de `extension/site-adapters.js` contra
  el DOM real de cada sitio, y sumar el historial de simulaciones al
  dashboard.
- Ambas: correr los casos de prueba de los tres perfiles de empleado
  definidos en el marco conceptual, para alimentar la matriz de
  resultados de la Etapa 4.
