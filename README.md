# Sistema de Prevención de Fuga de Datos por IA (Shadow AI) — PYMES

Trabajo final de Práctica Profesional Supervisada — UTN Facultad Regional Resistencia / CInApTIC.
Zaira Rosin (extensión + dashboard) y Denise Pujalte (backend de análisis).

## Qué es esto

Las PyMEs argentinas usan cada vez más herramientas de IA generativa (ChatGPT, Gemini, Claude) sin supervisión, exponiendo sin darse cuenta información sensible de la empresa: datos de clientes, código propietario, credenciales. Este fenómeno se conoce como **Shadow AI**.

Este proyecto es un sistema liviano que se interpone en el momento exacto en que un empleado intenta enviar ese tipo de información a una IA externa. No bloquea el uso de la herramienta: cuando detecta un dato sensible, muestra una explicación en lenguaje simple de por qué ese dato es riesgoso (intervención contextual), en vez de un bloqueo genérico sin justificación.

Se compone de tres módulos: una extensión de navegador que intercepta el texto antes del envío, un backend que lo analiza combinando expresiones regulares y NLP (spaCy) para clasificar el riesgo, y un dashboard de administración que registra los eventos para auditoría.

## Estructura del repositorio

```
GuardIA/
├── extension/    # Extensión de navegador (Manifest V3) — Zaira
├── backend/       # API de análisis en FastAPI — Denise
├── dashboard/      # Panel de administración en React — Zaira
├── docs/            # Contrato de simulación y perfiles de usuario (Etapa 4)
└── .gitignore
```

Los tres componentes están desacoplados y se comunican por HTTP según
el contrato de API descripto en el Marco Conceptual y de Arquitectura
del proyecto (documentación probatoria de la PPS, entregada aparte del
repositorio). `docs/` conserva la documentación técnica ligada
directamente al código: `perfiles_usuario.md` y
`diseno_simulacion_etapa4.md`, que definen los perfiles de usuario y el
contrato `perfil`/`condicion` usados en la simulación de la Etapa 4.
Cada componente tiene su propio README con instrucciones puntuales.

## Cómo levantar todo en local

Se necesitan 2 terminales abiertas en simultáneo (backend y dashboard); la extensión no usa terminal, se carga directo desde Chrome:

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

