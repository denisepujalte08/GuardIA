# Extensión - Capa de Intercepción y Alerta

Extensión de navegador (Manifest V3) para ChatGPT, Gemini y Claude.
Intercepta el texto antes del envío, lo manda al backend real (FastAPI
+ reglas/regex + NLP con spaCy) y muestra el modal de intervención
contextual según el nivel de riesgo. Si el backend local no está
levantado, cae a un análisis mock simplificado para no bloquear el
flujo de desarrollo (ver `callBackend()` en `service-worker.js`).

## Cómo probarla

1. Levantá el backend (`cd backend && uvicorn app.main:app --reload --port 8000`) — ver `../backend/README.md`.
2. Abrí `chrome://extensions` en Chrome.
3. Activá el interruptor **"Modo de desarrollador"** (arriba a la derecha).
4. Hacé clic en **"Cargar descomprimida"** y seleccioná esta carpeta (`extension/`).
5. Entrá a `chatgpt.com`, `gemini.google.com` o `claude.ai` (con sesión iniciada).
6. Escribí un mensaje que incluya, por ejemplo:
   - Un CUIT: `20-38456712-4` → riesgo **crítico**
   - Un CBU (22 dígitos): `2850590940090418135201` → riesgo **crítico**
   - Una credencial: `api_key: sk-12345` → riesgo **crítico**
   - Un DNI: `30123456` → riesgo **alto**
   - Un teléfono: `3624 456789` → riesgo **alto**
   - Un email: `cliente@empresa.com` → riesgo **alto**
   - Un nombre propio u organización: `Envié el presupuesto a Juan Perez` → riesgo **medio**
   - Texto sin datos sensibles → se envía normalmente (riesgo bajo, sin modal)
7. Al presionar Enter o el botón de enviar, debería aparecer el modal
   de intervención contextual en lugar del envío inmediato (salvo
   riesgo bajo, que se envía directo).
8. Elegí una acción en el modal (Editar / Cancelar / Continuar) y
   verificá en el dashboard (`../dashboard/`) o en `GET /eventos` del
   backend que la columna "Acción" se actualizó — confirma que el
   `PATCH /eventos/{id}` está sincronizando bien con el backend.

## Notas de mantenimiento

- Los selectores de `site-adapters.js` dependen del DOM de cada sitio
  externo, que puede cambiar sin aviso — conviene volver a verificarlos
  antes de cada tanda de pruebas. Ya se corrigieron dos bugs de este
  tipo en ChatGPT: el composer real es un `div[contenteditable]` con
  `id="prompt-textarea"` (no el `<textarea>` oculto de respaldo que
  también existe en el DOM), y el botón de enviar usa
  `aria-label="Enviar mensaje"` en español (no solo `"Send"`).
- Los íconos en `icons/` son placeholders — reemplazar antes de publicar.
- Sumar manejo de errores más robusto (timeouts, reintentos) si se
  pasa a depender de una red real en producción.

## Estructura

```
extension/
├── manifest.json          # Configuración MV3, permisos y content scripts
├── site-adapters.js        # Selectores por sitio (ChatGPT/Gemini/Claude)
├── content-script.js       # Intercepción del envío + modal de intervención
├── content-style.css       # Estilos del modal
├── service-worker.js       # Integración con el backend real (fallback a mock) + sincronización de acciones (PATCH /eventos/{id})
└── icons/                  # Íconos placeholder
```
