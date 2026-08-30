import { useEffect, useState } from "react";
import { obtenerEventos } from "./api.js";
import EventsTable from "./components/EventsTable.jsx";
import MetricsPanel from "./components/MetricsPanel.jsx";

const FILTROS_INICIALES = { usuario_id: "", ia_destino: "", nivel_riesgo: "" };

export default function App() {
  const [eventos, setEventos] = useState([]);
  const [filtros, setFiltros] = useState(FILTROS_INICIALES);
  const [cargando, setCargando] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    let activo = true;
    setCargando(true);
    obtenerEventos(filtros)
      .then((data) => {
        if (activo) {
          setEventos(data.eventos);
          setError(null);
        }
      })
      .catch((err) => {
        if (activo) setError(err.message);
      })
      .finally(() => activo && setCargando(false));
    return () => {
      activo = false;
    };
  }, [filtros]);

  return (
    <div className="app">
      <header>
        <h1>Prevención de Fuga de Datos por IA — Panel de Administración</h1>
        <p className="subtitle">Visibilidad de los eventos detectados por la extensión en la organización.</p>
      </header>

      {error && (
        <div className="error-banner">
          No se pudo conectar con el backend ({error}). Verificá que esté corriendo en{" "}
          <code>http://localhost:8000</code>.
        </div>
      )}

      <MetricsPanel eventos={eventos} />
      <EventsTable eventos={eventos} filtros={filtros} onFiltroChange={setFiltros} />

      {cargando && <p className="cargando">Actualizando…</p>}
    </div>
  );
}
