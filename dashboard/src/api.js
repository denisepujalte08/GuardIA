/**
 * api.js
 *
 * Cliente HTTP hacia el backend. Toda la app llama al backend a
 * través de estas funciones, para tener un único lugar que tocar si
 * cambia la URL base o el shape de la respuesta.
 */

const BACKEND_BASE_URL = import.meta.env.VITE_BACKEND_URL || "http://localhost:8000";

export async function obtenerEventos(filtros = {}) {
  const params = new URLSearchParams();
  if (filtros.usuario_id) params.set("usuario_id", filtros.usuario_id);
  if (filtros.ia_destino) params.set("ia_destino", filtros.ia_destino);
  if (filtros.nivel_riesgo) params.set("nivel_riesgo", filtros.nivel_riesgo);

  const resp = await fetch(`${BACKEND_BASE_URL}/eventos?${params.toString()}`);
  if (!resp.ok) throw new Error(`Error al consultar eventos: ${resp.status}`);
  return resp.json(); // { eventos: [...], total: N }
}
