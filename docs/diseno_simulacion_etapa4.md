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

**Pendiente del lado de la extensión** (Zaira):

- Que la extensión mande `perfil` y `condicion` en el body de
  `POST /analizar` durante una simulación (por ejemplo, seteados desde
  una pantalla/config de "modo simulación" en la extensión, o
  hardcodeados en un script de prueba que dispare los envíos).
- Que el dashboard permita filtrar la tabla de eventos por `perfil` y
  `condicion`, para poder armar la matriz de resultados comparando
  ambas condiciones por perfil.

## 2. Variante de "bloqueo genérico"

*(Sección a completar por Zaira — definición de qué muestra el modal
en la condición "generico": un mensaje sin explicación tipo "Este
envío fue bloqueado por política de seguridad", sin detalle de qué
dato se detectó ni por qué, para poder comparar contra la intervención
contextual actual. Falta decidir también cómo se activa esta variante
en la extensión durante una simulación — por ejemplo, un flag de
configuración que el content script lee antes de renderizar el modal.)*

## 3. Cómo correr una simulación

*(Sección a completar una vez definido el punto 2 — protocolo paso a
paso: qué perfil actúa, con qué condición, usando qué textos del
dataset de `backend/evaluacion/dataset.py` como estímulos, y cómo se
registra el resultado.)*
