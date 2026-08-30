export default function EventsTable({ eventos, filtros, onFiltroChange }) {
  return (
    <div className="card">
      <div className="card-header">
        <h2>Eventos registrados</h2>
        <div className="filtros">
          <select
            value={filtros.ia_destino}
            onChange={(e) => onFiltroChange({ ...filtros, ia_destino: e.target.value })}
          >
            <option value="">Todas las IAs</option>
            <option value="chatgpt">ChatGPT</option>
            <option value="gemini">Gemini</option>
            <option value="claude">Claude</option>
          </select>
          <select
            value={filtros.nivel_riesgo}
            onChange={(e) => onFiltroChange({ ...filtros, nivel_riesgo: e.target.value })}
          >
            <option value="">Todos los niveles</option>
            <option value="bajo">Bajo</option>
            <option value="medio">Medio</option>
            <option value="alto">Alto</option>
            <option value="critico">Crítico</option>
          </select>
          <input
            placeholder="Filtrar por usuario…"
            value={filtros.usuario_id}
            onChange={(e) => onFiltroChange({ ...filtros, usuario_id: e.target.value })}
          />
        </div>
      </div>

      <table>
        <thead>
          <tr>
            <th>Fecha</th>
            <th>Usuario</th>
            <th>IA destino</th>
            <th>Tipo de dato</th>
            <th>Riesgo</th>
            <th>Acción del usuario</th>
          </tr>
        </thead>
        <tbody>
          {eventos.length === 0 && (
            <tr>
              <td colSpan={6} className="vacio">
                Sin eventos para los filtros aplicados.
              </td>
            </tr>
          )}
          {eventos.map((ev) => (
            <tr key={ev.id}>
              <td>{new Date(ev.timestamp).toLocaleString("es-AR")}</td>
              <td>{ev.usuario_id}</td>
              <td>{ev.ia_destino}</td>
              <td>{ev.tipo_dato_detectado || "—"}</td>
              <td>
                <span className={`badge riesgo-${ev.nivel_riesgo}`}>{ev.nivel_riesgo}</span>
              </td>
              <td>{ev.accion || "—"}</td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}
