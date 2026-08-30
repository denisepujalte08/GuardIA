import { BarChart, Bar, XAxis, YAxis, Tooltip, ResponsiveContainer, CartesianGrid } from "recharts";

const COLORES_RIESGO = { bajo: "#16a34a", medio: "#d97706", alto: "#dc2626", critico: "#7f1d1d" };

function agruparPor(eventos, campo) {
  const conteo = {};
  eventos.forEach((ev) => {
    const clave = ev[campo] || "sin dato";
    conteo[clave] = (conteo[clave] || 0) + 1;
  });
  return Object.entries(conteo).map(([nombre, cantidad]) => ({ nombre, cantidad }));
}

export default function MetricsPanel({ eventos }) {
  const porRiesgo = agruparPor(eventos, "nivel_riesgo");
  const porIA = agruparPor(eventos, "ia_destino");
  const porUsuario = agruparPor(eventos, "usuario_id");

  return (
    <div className="metrics-grid">
      <div className="card">
        <h3>Eventos por nivel de riesgo</h3>
        <ResponsiveContainer width="100%" height={220}>
          <BarChart data={porRiesgo}>
            <CartesianGrid strokeDasharray="3 3" />
            <XAxis dataKey="nombre" />
            <YAxis allowDecimals={false} />
            <Tooltip />
            <Bar dataKey="cantidad" fill="#1d4ed8" />
          </BarChart>
        </ResponsiveContainer>
      </div>

      <div className="card">
        <h3>Eventos por IA de destino</h3>
        <ResponsiveContainer width="100%" height={220}>
          <BarChart data={porIA}>
            <CartesianGrid strokeDasharray="3 3" />
            <XAxis dataKey="nombre" />
            <YAxis allowDecimals={false} />
            <Tooltip />
            <Bar dataKey="cantidad" fill="#7c3aed" />
          </BarChart>
        </ResponsiveContainer>
      </div>

      <div className="card">
        <h3>Eventos por usuario</h3>
        <ResponsiveContainer width="100%" height={220}>
          <BarChart data={porUsuario}>
            <CartesianGrid strokeDasharray="3 3" />
            <XAxis dataKey="nombre" />
            <YAxis allowDecimals={false} />
            <Tooltip />
            <Bar dataKey="cantidad" fill="#0891b2" />
          </BarChart>
        </ResponsiveContainer>
      </div>
    </div>
  );
}
