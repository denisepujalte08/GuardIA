/**
 * service-worker.js
 *
 * Orquesta la comunicación "hacia afuera" de la extensión.
 *
 * Contrato con el backend real (Denise, FastAPI):
 *
 *   Request  POST /analizar
 *     { texto, usuario_id, ia_destino }
 *
 *   Response
 *     { evento_id: string,
 *       nivel_riesgo: "bajo" | "medio" | "alto" | "critico",
 *       tipo_dato_detectado: string | null,
 *       fragmento_detectado: string | null,
 *       mensaje_contextual: string | null }
 *
 * `callBackend()` intenta ese fetch real y, si el backend local no
 * responde, cae al mock (`mockAnalizar`) para no bloquear el flujo de
 * desarrollo — ver el catch de `callBackend`.
 */

const BACKEND_BASE_URL = "http://localhost:8000"; // backend local (Etapa 3). Cambiar cuando exista un despliegue real.

// ---------------------------------------------------------------------
// Identificación de usuario (mock de autenticación / configuración)
// ---------------------------------------------------------------------

async function getUsuarioId() {
  const stored = await chrome.storage.local.get("usuario_id");
  if (stored.usuario_id) return stored.usuario_id;

  const nuevoId = "usr-" + Math.random().toString(36).slice(2, 10);
  await chrome.storage.local.set({ usuario_id: nuevoId });
  return nuevoId;
}

// ---------------------------------------------------------------------
// Catálogo de patrones de datos sensibles (versión mock, simplificada)
// Alineado a los tipos definidos en el marco conceptual: CUIT/CUIL,
// CBU, credenciales/tokens, emails, y una heurística simple de código
// propietario. El motor real de Denise reemplaza esto con reglas +
// spaCy; acá alcanza con detectar lo suficiente para probar el flujo.
// ---------------------------------------------------------------------

const PATRONES = [
  {
    tipo: "CUIT/CUIL",
    regex: /\b\d{2}-?\d{8}-?\d\b/,
    nivel: "alto",
    mensaje:
      "El CUIT/CUIL es un identificador personal protegido por la Ley 25.326. Enviarlo a una IA externa lo expone fuera del control de la empresa. Podés editarlo, cancelar el envío o continuar si estás seguro de que corresponde compartirlo.",
  },
  {
    tipo: "CBU",
    regex: /\b\d{22}\b/,
    nivel: "alto",
    mensaje:
      "Detectamos un CBU en el texto. Es información financiera sensible: compartirla con una IA externa puede exponer datos bancarios de un cliente o de la empresa.",
  },
  {
    tipo: "Credencial o token",
    regex: /(api[_-]?key|token|password|contrase[ñn]a|secret)\s*[:=]\s*\S+/i,
    nivel: "critico",
    mensaje:
      "El texto parece incluir una credencial o clave de acceso. Compartir esto con una IA externa puede comprometer sistemas de la empresa. Te recomendamos no continuar sin removerla.",
  },
  {
    tipo: "Correo electrónico",
    regex: /[\w.+-]+@[\w-]+\.[a-zA-Z]{2,}/,
    nivel: "medio",
    mensaje:
      "Detectamos una dirección de correo electrónico. Puede tratarse de un dato personal de un cliente o proveedor; revisá si es necesario incluirla antes de enviarla a una IA externa.",
  },
];

function mockAnalizar(texto) {
  for (const patron of PATRONES) {
    const match = texto.match(patron.regex);
    if (match) {
      return {
        nivel_riesgo: patron.nivel,
        tipo_dato_detectado: patron.tipo,
        fragmento_detectado: extraerFragmento(texto, match),
        mensaje_contextual: patron.mensaje,
      };
    }
  }
  return {
    nivel_riesgo: "bajo",
    tipo_dato_detectado: null,
    fragmento_detectado: null,
    mensaje_contextual: null,
  };
}

function extraerFragmento(texto, match) {
  const inicio = Math.max(0, match.index - 20);
  const fin = Math.min(texto.length, match.index + match[0].length + 10);
  return (inicio > 0 ? "…" : "") + texto.slice(inicio, fin) + (fin < texto.length ? "…" : "");
}

// ---------------------------------------------------------------------
// Punto único de integración con el backend: intenta el fetch real y,
// si el backend local no responde, cae al mock (ver catch más abajo).
// ---------------------------------------------------------------------

async function callBackend(texto, usuarioId, iaDestino) {
  try {
    const resp = await fetch(`${BACKEND_BASE_URL}/analizar`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ texto, usuario_id: usuarioId, ia_destino: iaDestino }),
    });
    if (!resp.ok) throw new Error("Error del backend: " + resp.status);
    return await resp.json(); // incluye el evento_id real, asignado por el backend
  } catch (err) {
    // Fallback de desarrollo: si el backend local no está levantado
    // (por ejemplo, mientras se prueba solo la extensión), se usa el
    // mock local para no bloquear el flujo. En producción esto debería
    // eliminarse o, como mínimo, avisarle al usuario que el análisis
    // no es el real.
    console.warn("[DLP] Backend no disponible, usando análisis mock local:", err.message);
    await new Promise((r) => setTimeout(r, 150));
    return {
      ...mockAnalizar(texto),
      // Prefijo "mock-" para distinguirlo de un evento_id real del backend:
      // no existe ningún registro en el servidor contra el cual hacer PATCH.
      evento_id: "mock-" + Date.now() + "-" + Math.random().toString(36).slice(2, 6),
    };
  }
}

// ---------------------------------------------------------------------
// Sincronización de la acción elegida en el modal con el backend, que
// es la única fuente de verdad de los eventos (el dashboard lee de
// ahí). Si el evento vino del mock (backend caído), no existe ningún
// registro real contra el cual hacer PATCH.
// ---------------------------------------------------------------------

async function actualizarAccionEvento(eventoId, accion) {
  if (eventoId.startsWith("mock-")) return; // no hay evento real en el backend contra el cual hacer PATCH

  try {
    const resp = await fetch(`${BACKEND_BASE_URL}/eventos/${eventoId}`, {
      method: "PATCH",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ accion }),
    });
    if (!resp.ok) throw new Error("Error al actualizar la acción: " + resp.status);
  } catch (err) {
    console.warn("[DLP] No se pudo sincronizar la acción con el backend:", err.message);
  }
}

// ---------------------------------------------------------------------
// Listener de mensajes provenientes del content script
// ---------------------------------------------------------------------

chrome.runtime.onMessage.addListener((message, _sender, sendResponse) => {
  if (message.type === "ANALYZE_TEXT") {
    (async () => {
      const usuarioId = await getUsuarioId();
      const resultado = await callBackend(message.text, usuarioId, message.iaDestino);

      sendResponse(resultado);
    })();
    return true; // mantiene el canal abierto para la respuesta async
  }

  if (message.type === "LOG_ACTION") {
    (async () => {
      await actualizarAccionEvento(message.eventoId, message.accion);
      sendResponse({ ok: true });
    })();
    return true;
  }
});
