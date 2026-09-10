/**
 * content-script.js
 *
 * Responsable de:
 *  - RF-01: detectar el composer de ChatGPT / Gemini / Claude.
 *  - RF-02: interceptar el evento de envío antes de que el texto salga.
 *  - RF-03: pedirle al service worker el análisis de riesgo (que hoy
 *           resuelve con un mock, ver service-worker.js).
 *  - RF-04: dejar pasar el envío original si el riesgo es bajo.
 *  - RF-05/06/07: bloquear y mostrar el modal contextual si el riesgo
 *           es medio, alto o crítico, con las 3 opciones de acción.
 */

(function () {
  const adapter = window.__dlpGetActiveAdapter && window.__dlpGetActiveAdapter();
  if (!adapter) return; // sitio no soportado (no debería ocurrir por los "matches" del manifest)

  // Evita interceptar dos veces el mismo envío ya aprobado por el usuario
  // (cuando reproducimos el click/Enter "de verdad" tras la decisión).
  let bypassNext = false;

  function getComposerEl() {
    return document.querySelector(adapter.composerSelector);
  }

  function getSendButtonEl() {
    return document.querySelector(adapter.sendButtonSelector);
  }

  async function analizarTexto(texto) {
    return chrome.runtime.sendMessage({
      type: "ANALYZE_TEXT",
      text: texto,
      iaDestino: adapter.id,
    });
  }

  function logAccion(eventoId, accion) {
    if (!eventoId) return;
    chrome.runtime.sendMessage({ type: "LOG_ACTION", eventoId, accion });
  }

  function reenviarDeVerdad() {
    bypassNext = true;
    const btn = getSendButtonEl();
    if (btn) {
      btn.click();
    }
    // Se resetea en el próximo tick para no dejar la extensión "abierta"
    // indefinidamente si el click no dispara ningún handler interceptado.
    setTimeout(() => (bypassNext = false), 0);
  }

  // ---------------------------------------------------------------
  // Modal de intervención contextual
  // ---------------------------------------------------------------

  function cerrarModal() {
    const overlay = document.querySelector(".dlp-overlay");
    if (overlay) overlay.remove();
  }

  function mostrarModal({ nivel_riesgo, tipo_dato_detectado, fragmento_detectado, mensaje_contextual, evento_id }) {
    cerrarModal();

    const overlay = document.createElement("div");
    overlay.className = "dlp-overlay";

    const nivelClase = "riesgo-" + nivel_riesgo; // riesgo-medio | riesgo-alto | riesgo-critico
    const nivelLabel =
      nivel_riesgo === "critico" ? "Riesgo crítico" : nivel_riesgo === "alto" ? "Riesgo alto" : "Riesgo medio";

    // Marco Conceptual, Sección 8: se prioriza la explicación sobre la
    // restricción en riesgo bajo/medio, reservando el bloqueo estricto
    // (sin opción de continuar) para riesgo alto y crítico.
    const bloqueoEstricto = nivel_riesgo === "alto" || nivel_riesgo === "critico";

    overlay.innerHTML = `
      <div class="dlp-modal" role="dialog" aria-modal="true">
        <div class="dlp-modal-header">
          <div class="dlp-modal-icon ${nivelClase}">!</div>
          <div class="dlp-modal-title-group">
            <p class="dlp-modal-title">Este mensaje contiene información sensible</p>
            <p class="dlp-modal-subtitle">Destino detectado: ${labelDestino(adapter.id)}</p>
          </div>
          <span class="dlp-badge ${nivelClase}">${nivelLabel}</span>
        </div>

        ${
          tipo_dato_detectado
            ? `<p class="dlp-section-label">Tipo de dato detectado:</p>
               <span class="dlp-tag">${escapeHtml(tipo_dato_detectado)}</span>`
            : ""
        }

        ${
          fragmento_detectado
            ? `<p class="dlp-section-label">Fragmento detectado en tu mensaje:</p>
               <div class="dlp-snippet">${escapeHtml(fragmento_detectado)}</div>`
            : ""
        }

        <p class="dlp-section-label">Por qué te lo mostramos:</p>
        <p class="dlp-explanation">${escapeHtml(mensaje_contextual || "")}</p>

        <div class="dlp-actions">
          <button class="dlp-btn dlp-btn-primary" data-accion="editar">Editar el texto</button>
          <button class="dlp-btn dlp-btn-secondary" data-accion="cancelar">Cancelar envío</button>
          <button
            class="dlp-btn dlp-btn-ghost"
            data-accion="continuar"
            ${bloqueoEstricto ? "disabled" : ""}
            ${bloqueoEstricto ? 'title="No disponible para este nivel de riesgo"' : ""}
          >Continuar de todos modos</button>
        </div>
        <p class="dlp-hint">
          ${
            bloqueoEstricto
              ? "Este nivel de riesgo no permite continuar el envío: elegí \"Editar el texto\" o \"Cancelar envío\"."
              : "\"Editar el texto\" es la opción recomendada. \"Continuar de todos modos\" queda registrado en la auditoría."
          }
        </p>
      </div>
    `;

    overlay.addEventListener("click", (e) => {
      const accionBtn = e.target.closest("[data-accion]");
      if (!accionBtn) return;
      const accion = accionBtn.getAttribute("data-accion");

      logAccion(evento_id, accion);

      if (accion === "editar") {
        cerrarModal();
        const composer = getComposerEl();
        if (composer) composer.focus();
        return;
      }

      if (accion === "cancelar") {
        cerrarModal();
        return;
      }

      if (accion === "continuar") {
        cerrarModal();
        reenviarDeVerdad();
        return;
      }
    });

    document.body.appendChild(overlay);
  }

  function labelDestino(id) {
    return { chatgpt: "ChatGPT (chatgpt.com)", gemini: "Gemini (gemini.google.com)", claude: "Claude (claude.ai)" }[id] || id;
  }

  function escapeHtml(str) {
    const div = document.createElement("div");
    div.textContent = str;
    return div.innerHTML;
  }

  // ---------------------------------------------------------------
  // Intercepción del envío (RF-01 / RF-02)
  // Se escucha en fase de captura sobre `document` para adelantarse
  // a los handlers propios del sitio, tanto para el click en el botón
  // de enviar como para "Enter" (sin Shift) dentro del composer.
  // ---------------------------------------------------------------

  async function manejarIntentoDeEnvio(event) {
    if (bypassNext) return; // ya aprobado por el usuario, dejar pasar

    const composer = getComposerEl();
    if (!composer) return;

    const texto = (adapter.getText(composer) || "").trim();
    if (!texto) return; // nada que analizar, dejar seguir el comportamiento normal

    event.preventDefault();
    event.stopImmediatePropagation();

    let resultado;
    try {
      resultado = await analizarTexto(texto);
    } catch (err) {
      // Si el análisis falla (backend caído, extensión recién instalada, etc.)
      // se prioriza no bloquear al usuario: se deja pasar el envío original.
      console.warn("[DLP] No se pudo analizar el texto, se permite el envío:", err);
      reenviarDeVerdad();
      return;
    }

    if (resultado.nivel_riesgo === "bajo") {
      reenviarDeVerdad(); // RF-04
    } else {
      mostrarModal(resultado); // RF-05 / RF-06 / RF-07
    }
  }

  document.addEventListener(
    "click",
    (event) => {
      const btn = event.target.closest(adapter.sendButtonSelector);
      if (btn) manejarIntentoDeEnvio(event);
    },
    true
  );

  document.addEventListener(
    "keydown",
    (event) => {
      if (event.key !== "Enter" || event.shiftKey) return;
      const composer = getComposerEl();
      if (!composer) return;
      if (!composer.contains(event.target) && event.target !== composer) return;
      manejarIntentoDeEnvio(event);
    },
    true
  );
})();
