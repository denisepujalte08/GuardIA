/**
 * popup.js
 *
 * Configura el "modo simulación" usado en las simulaciones de la Etapa 4
 * (ver docs/diseno_simulacion_etapa4.md): guarda en chrome.storage.local
 * qué perfil está actuando la persona que prueba y con qué condición
 * (contextual/generico), para que service-worker.js los mande en
 * POST /analizar y content-script.js elija qué variante de modal mostrar.
 */

const activoEl = document.getElementById("activo");
const perfilEl = document.getElementById("perfil");
const condicionEl = document.getElementById("condicion");
const estadoEl = document.getElementById("estado");
const guardarBtn = document.getElementById("guardar");

async function cargar() {
  const { simulacion } = await chrome.storage.local.get("simulacion");
  if (!simulacion) return;
  activoEl.checked = !!simulacion.activo;
  perfilEl.value = simulacion.perfil || "cuidadoso";
  condicionEl.value = simulacion.condicion || "contextual";
}

guardarBtn.addEventListener("click", async () => {
  const simulacion = {
    activo: activoEl.checked,
    perfil: perfilEl.value,
    condicion: condicionEl.value,
  };
  await chrome.storage.local.set({ simulacion });
  estadoEl.textContent = simulacion.activo
    ? `Simulación activa: ${simulacion.perfil} / ${simulacion.condicion}`
    : "Simulación desactivada (uso normal)";
});

cargar();
