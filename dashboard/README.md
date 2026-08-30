# Dashboard de Administración (React + Vite)

Panel de auditoría: tabla filtrable de eventos (RF-09) y métricas
agregadas (RF-10). Responsable: Zaira Rosin.

## Cómo correrlo

```bash
cd dashboard
npm install
npm run dev
```

Por defecto apunta a `http://localhost:8000` (el backend local). Para
cambiarlo, copiar `.env.example` a `.env` y editar `VITE_BACKEND_URL`.

El backend debe estar corriendo antes de levantar el dashboard (ver
`../backend/README.md`).

## Estructura

```
dashboard/
├── src/
│   ├── main.jsx              # Punto de entrada
│   ├── App.jsx                # Estado de filtros + orquestación
│   ├── api.js                  # Cliente HTTP hacia el backend
│   ├── index.css                # Estilos base
│   └── components/
│       ├── EventsTable.jsx      # Tabla filtrable (RF-09)
│       └── MetricsPanel.jsx     # Gráficos agregados (RF-10)
├── index.html
├── vite.config.js
└── package.json
```
