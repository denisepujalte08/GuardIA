/**
 * site-adapters.js
 *
 * Configuración declarativa de selectores por sitio de IA soportado.
 * Centralizar esto acá evita hardcodear selectores dentro del content
 * script y facilita actualizarlos cuando cambie el DOM de cada sitio
 * (algo esperable, ya que ninguno expone una API estable para esto).
 *
 * Cada adapter define:
 *  - id: identificador usado como "ia_destino" en el contrato con el backend.
 *  - composerSelector: el elemento donde el usuario escribe (textarea o
 *    contenteditable, según el sitio).
 *  - sendButtonSelector: el botón de envío, usado como fallback para
 *    reintentar el envío una vez aprobado por el usuario.
 *  - getText(el): cómo extraer el texto plano del composer.
 */
window.__dlpSiteAdapters = [
  {
    id: "chatgpt",
    hostMatch: (host) => host.includes("chatgpt.com"),
    composerSelector: "#prompt-textarea, form textarea",
    sendButtonSelector: "[data-testid='send-button'], button[aria-label*='Send' i]",
    getText: (el) => (el.value !== undefined ? el.value : el.innerText) || "",
  },
  {
    id: "gemini",
    hostMatch: (host) => host.includes("gemini.google.com"),
    composerSelector: "div.ql-editor, rich-textarea div[contenteditable='true']",
    sendButtonSelector: "button[aria-label*='Send' i], button[aria-label*='Enviar' i]",
    getText: (el) => el.innerText || "",
  },
  {
    id: "claude",
    hostMatch: (host) => host.includes("claude.ai"),
    composerSelector: "div[contenteditable='true'].ProseMirror, div[contenteditable='true']",
    sendButtonSelector: "button[aria-label*='Send' i], button[aria-label*='Enviar' i]",
    getText: (el) => el.innerText || "",
  },
];

/**
 * Devuelve el adapter correspondiente al hostname actual, o null si el
 * sitio no está soportado (no debería pasar dado que el content script
 * solo se inyecta en los "matches" declarados en el manifest, pero se
 * valida igual por robustez).
 */
window.__dlpGetActiveAdapter = function () {
  const host = window.location.hostname;
  return window.__dlpSiteAdapters.find((a) => a.hostMatch(host)) || null;
};
