# Diseño de la simulación — Etapa 4

Decisiones técnicas conjuntas (Denise Pujalte y Zaira Rosin) para poder
correr las simulaciones con perfiles de usuario y comparar
intervención contextual vs. bloqueo genérico. Complementa
`perfiles_usuario.md` (que define el comportamiento esperado de cada
perfil) con el "cómo" técnico de la simulación.

## 1. Contrato extendido: campos `perfil` y `condicion`

Se agregaron dos campos **opcionales** al contrato entre la extensión
y el backend, usados solo durante las simulaciones (en uso real de la
extensión quedan en `null`):

- `perfil`: `"cuidadoso" | "apurado" | "esceptico"` — qué perfil de
  `perfiles_usuario.md` está actuando en ese envío.
- `condicion`: `"contextual" | "generico"` — qué variante de modal vio
  el usuario (ver punto 2).

**Cambios en el backend** (ya implementados, lado Denise):

- `schemas.py`: `AnalizarRequest` y `Evento` incluyen ambos campos.
- `store.py`: la tabla `eventos` en SQLite persiste `perfil` y
  `condicion`; `listar_eventos()` acepta filtrarlos.
- `main.py`: `POST /analizar` los recibe y los guarda en el evento;
  `GET /eventos` acepta `?perfil=...` y `?condicion=...` como filtros,
  además de los que ya existían.

> Importante: como cambia el esquema de la tabla, cada quien debe
> borrar su `backend/dlp.db` local (archivo de desarrollo, gitignorado)
> para que se recree con las columnas nuevas la próxima vez que
> levanten el backend.

**Implementado del lado de la extensión** (Zaira):

- `popup.html` / `popup.js`: agregan un popup ("Modo simulación") donde
  quien prueba activa la simulación y elige `perfil` y `condicion`
  antes de escribir el mensaje. Se guarda en
  `chrome.storage.local` (clave `simulacion`).
- `service-worker.js`: `obtenerConfigSimulacion()` lee esa config; si
  está activa, manda `perfil`/`condicion` en el `POST /analizar` y le
  devuelve `condicion` al content script junto con el resto de la
  respuesta (el backend no la devuelve porque solo la persiste).
- `content-script.js`: `mostrarModal()` usa esa `condicion` para elegir
  qué variante renderizar (ver punto 2). Con la simulación desactivada
  (uso normal), `condicion` siempre es `"contextual"` — no cambia nada
  del comportamiento actual.
- `dashboard`: `EventsTable.jsx` suma selectores para filtrar por
  `perfil` y `condicion`, y muestra ambos como columnas nuevas.

## 2. Variante de "bloqueo genérico"

Implementada en `content-script.js` (`mostrarModal`). Cuando
`condicion === "generico"`, el modal:

- Título: "Este envío fue bloqueado por política de seguridad" (en vez
  de "Este mensaje contiene información sensible").
- **No muestra** el tipo de dato detectado, el fragmento del mensaje
  ni la explicación contextual (`mensaje_contextual`) — es la
  diferencia central a medir contra la condición `"contextual"`.
- Mantiene la **misma lógica de botones** que la condición contextual:
  Editar/Cancelar siempre disponibles, "Continuar de todos modos"
  deshabilitado en riesgo alto/crítico (mismo `bloqueoEstricto` de la
  Sección 8). Lo único que varía entre condiciones es cuánta
  información recibe el usuario, no qué puede hacer.

Cómo se activa: desde el popup de la extensión, eligiendo `condicion:
"generico"` antes de mandar el mensaje de prueba.

## 3. Cómo correr una simulación

1. Levantar el backend y el dashboard (ver READMEs de cada uno).
2. Abrir el popup de la extensión (ícono en la barra de Chrome),
   activar "Simulación activa", elegir el **perfil** a actuar
   (`cuidadoso` / `apurado` / `esceptico`) y la **condición**
   (`contextual` / `generico`), y guardar.
3. Escribir en ChatGPT/Gemini/Claude uno de los textos de
   `backend/evaluacion/dataset.py` (o cualquier texto representativo de
   riesgo bajo/medio/alto/crítico) y enviarlo.
4. Ante el modal, elegir la acción que le corresponde al perfil actuado
   según `perfiles_usuario.md` (no la que "convendría" objetivamente —
   la idea es simular el comportamiento del perfil, no evitar el
   riesgo).
5. Repetir el paso 3-4 para cada combinación perfil × condición ×
   nivel de riesgo que se quiera cubrir, cambiando la config del popup
   entre corridas.
6. En el dashboard, filtrar por `perfil` y `condicion` para armar la
   matriz de resultados: tasa de aceptación de alertas y comparación
   contextual vs. genérico, por perfil y por nivel de riesgo.

Pendiente de definir (fuera del alcance técnico de este documento):
cuántas repeticiones por combinación son necesarias para que la
matriz de resultados sea representativa, y si las simulaciones las
corren Denise y Zaira mismas actuando los perfiles, u otras personas.
