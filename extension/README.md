# Extensión - Capa de Intercepción y Alerta

Esqueleto funcional de la extensión (Manifest V3) para ChatGPT, Gemini y
Claude. El análisis de riesgo está **mockeado** en `service-worker.js`
con reglas simples (regex) que respetan el contrato ya consolidado con
el backend, para poder probar todo el flujo end-to-end sin esperar el
motor de detección real.

## Cómo probarla

1. Abrí `chrome://extensions` en Chrome.
2. Activá el interruptor **"Modo de desarrollador"** (arriba a la derecha).
3. Hacé clic en **"Cargar descomprimida"** y seleccioná esta carpeta (`extension/`).
4. Entrá a `chatgpt.com`, `gemini.google.com` o `claude.ai` (con sesión iniciada).
5. Escribí un mensaje que incluya, por ejemplo:
   - Un CUIT: `20-38456712-4` → riesgo **alto**
   - Un CBU (22 dígitos): `2850590940090418135201` → riesgo **alto**
   - Una palabra tipo `api_key: sk-12345` → riesgo **crítico**
   - Un email: `cliente@empresa.com` → riesgo **medio**
   - Texto sin datos sensibles → se envía normalmente (riesgo bajo, sin modal)
6. Al presionar Enter o el botón de enviar, debería aparecer el modal
   de intervención contextual en lugar del envío inmediato.

## Qué falta para pasar de mock a real

- En `service-worker.js`, reemplazar `mockAnalizar()` por el `fetch()`
  real hacia el endpoint de Denise (ya está comentado y listo, dentro
  de `callBackend()`).
- Revisar los selectores de `site-adapters.js`: los sitios cambian su
  DOM con frecuencia, así que conviene volver a verificarlos antes de
  cada tanda de pruebas.
- Sumar manejo de errores más robusto (timeouts, reintentos) una vez
  que se dependa de una red real en vez del mock local.
- Los íconos en `icons/` son placeholders — reemplazar antes de publicar.

## Estructura

```
extension/
├── manifest.json          # Configuración MV3, permisos y content scripts
├── site-adapters.js        # Selectores por sitio (ChatGPT/Gemini/Claude)
├── content-script.js       # Intercepción del envío + modal de intervención
├── content-style.css       # Estilos del modal
├── service-worker.js       # Mock del backend + registro local de eventos
└── icons/                  # Íconos placeholder
```
