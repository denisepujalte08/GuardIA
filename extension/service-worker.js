/**
 * service-worker.js
 *
 * Orquesta la comunicación "hacia afuera" de la extensión.
 *
 * IMPORTANTE - ESTADO ACTUAL (mock):
 * Mientras el motor de análisis de Denise (FastAPI + reglas/regex/NLP)
 * no esté expuesto, este service worker SIMULA la respuesta de
 * POST /analizar con reglas simples (regex), respetando exactamente
 * el contrato ya consolidado:
 *
 *   Request  POST /analizar
 *     { texto, usuario_id, ia_destino }
 *
 *   Response
 *     { nivel_riesgo: "bajo" | "medio" | "alto" | "critico",
 *       tipo_dato_detectado: string | null,
 *       fragmento_detectado: string | null,
 *       mensaje_contextual: string | null }
 *
 * Cuando el backend real esté disponible, el ÚNICO cambio necesario es
 * reemplazar la función `mockAnalizar()` por el `fetch()` real hacia
 * `BACKEND_BASE_URL + "/analizar"` (ver la función `callBackend`, que ya
 * tiene la llamada real comentada más abajo). El resto de la extensión
 * (content-script.js) no necesita tocarse porque solo depende del
 * contrato, no de cómo se resuelve.
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
// Punto único de integración con el backend. Hoy resuelve con el mock;
// el día que el endpoint real exista, se descomenta el fetch y se borra
// la línea del mock.
// ---------------------------------------------------------------------

async function callBackend(texto, usuarioId, iaDestino) {
  try {
    const resp = await fetch(`${BACKEND_BASE_URL}/analizar`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ texto, usuario_id: usuarioId, ia_destino: iaDestino }),
    });
    if (!resp.ok) throw new Error("Error del backend: " + resp.status);
    return await resp.json();
  } catch (err) {
    // Fallback de desarrollo: si el backend local no está levantado
    // (por ejemplo, mientras se prueba solo la extensión), se usa el
    // mock local para no bloquear el flujo. En producción esto debería
    // eliminarse o, como mínimo, avisarle al usuario que el análisis
    // no es el real.
    console.warn("[DLP] Backend no disponible, usando análisis mock local:", err.message);
    await new Promise((r) => setTimeout(r, 150));
    return mockAnalizar(texto);
  }
}

// ---------------------------------------------------------------------
// Registro de eventos local (mock del "registro de eventos" que en
// producción vive en el backend y se consulta con GET /eventos desde
// el dashboard). Guardar acá el mismo shape permite que, cuando el
// dashboard se conecte al backend real, no haya que cambiar nada del
// lado de la extensión.
// ---------------------------------------------------------------------

async function registrarEvento(evento) {
  const { eventos = [] } = await chrome.storage.local.get("eventos");
  eventos.unshift(evento);
  await chrome.storage.local.set({ eventos: eventos.slice(0, 200) }); // tope simple
  return evento;
}

async function actualizarAccionEvento(eventoId, accion) {
  const { eventos = [] } = await chrome.storage.local.get("eventos");
  const idx = eventos.findIndex((e) => e.id === eventoId);
  if (idx !== -1) {
    eventos[idx].accion = accion;
    await chrome.storage.local.set({ eventos });
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

      const evento = {
        id: "evt-" + Date.now() + "-" + Math.random().toString(36).slice(2, 6),
        usuario_id: usuarioId,
        ia_destino: message.iaDestino,
        nivel_riesgo: resultado.nivel_riesgo,
        tipo_dato_detectado: resultado.tipo_dato_detectado,
        mensaje_contextual: resultado.mensaje_contextual,
        accion: resultado.nivel_riesgo === "bajo" ? "permitido_automatico" : null,
        timestamp: new Date().toISOString(),
      };
      await registrarEvento(evento);

      sendResponse({ ...resultado, evento_id: evento.id });
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
