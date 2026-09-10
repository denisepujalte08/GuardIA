# Perfiles de usuario — Etapa 4 (Simulación y Prueba)

Definición conjunta (Denise Pujalte y Zaira Rosin) de los 3 perfiles de
empleado a usar en las simulaciones de la Etapa 4, según lo previsto en
ambos planes de trabajo ("Ejecución de simulaciones con tres perfiles
de empleado diferenciados").

Esta definición asume el bloqueo estricto ya implementado en el modal
(ver Marco Conceptual, Sección 8): para riesgo **alto** o **crítico**,
la opción "Continuar de todos modos" no está disponible — solo se
puede **editar** o **cancelar**. Para riesgo **medio**, las 3 opciones
siguen disponibles.

## 1. Cuidadoso

Lee la explicación del modal, entiende el riesgo y prioriza cumplir la
recomendación del sistema.

| Nivel de riesgo | Comportamiento esperado |
|---|---|
| Medio | Edita o cancela. Rara vez continúa. |
| Alto / Crítico | Edita o cancela. |

## 2. Apurado

Prioriza terminar su tarea lo más rápido posible, minimizando el
esfuerzo dedicado a la alerta.

| Nivel de riesgo | Comportamiento esperado |
|---|---|
| Medio | Ignora la explicación y elige "Continuar de todos modos". |
| Alto / Crítico | Como no puede continuar, elige la opción de **menor esfuerzo** entre las disponibles: **cancela** (rápido) en vez de editar (le implica revisar y reescribir el texto). |

> Nota: esta definición fue corregida durante la coordinación entre
> Denise y Zaira — la primera versión no contemplaba que el bloqueo
> estricto en alto/crítico invalida la opción "continúa igual" que
> definía al perfil originalmente.

## 3. Escéptico / cuestionador

No confía ciegamente en la alerta. Su decisión varía según qué tan
convincente le resulte el mensaje contextual mostrado — es el perfil
más relevante para medir si la *explicación* (y no solo el bloqueo)
cambia el comportamiento del usuario, que es el objetivo central del
proyecto (intervención contextual vs. bloqueo genérico).

| Nivel de riesgo | Comportamiento esperado |
|---|---|
| Medio | Variable: puede continuar si el mensaje no lo convence, o editar/cancelar si sí. |
| Alto / Crítico | Variable entre editar y cancelar, sin un patrón fijo. |

## Uso previsto

- **Zaira (Etapa 4 propia)**: ejecutar simulaciones con estos 3
  perfiles para armar la matriz de resultados de usabilidad y tasa de
  aceptación de alertas, comparando intervención contextual vs.
  bloqueo genérico.
- **Denise y Zaira (tarea compartida)**: ejecutar la simulación del
  flujo completo de extremo a extremo utilizando estos perfiles, según
  lo previsto en ambos planes de trabajo.
