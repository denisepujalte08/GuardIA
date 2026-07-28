**PLAN DE TRABAJO**

**DATOS DEL ALUMNO**

Apellido y Nombres:	Rosin, Zaira Antonella

DNI / DU / CI / CE: 4386450

Legajo UTN Nº: 26537

**LUGAR DE REALIZACIÓN DE LA PPS**

Datos de la Empresa / Institución / Organización

Identificación:	 UTN Facultad Regional Resistencia, Chaco.

Actividad Principal: Educación superior pública y gratuita, enfocada en la creación, preservación y transmisión de conocimientos en los campos científico, tecnológico y cultural.

Grupo de Investigación: Centro de Investigación Aplicada en Tecnologías de la Información y Comunicación (CINAPTIC)

Domicilio: Anexo UTN (Av. Laprida y French)

Director del Proyecto:  Ing. Diego Bolatti

Tutor:  Ing. Diego Bolatti

**TÍTULO DEL PROYECTO**

**Sistema de Prevención de Fuga de Datos en el Uso de Inteligencia Artificial mediante Intervención Contextual en Tiempo Real para PYMES**

**ANTECEDENTES DEL PROYECTO	**

El presente trabajo se desprende del proyecto de investigación **"Desarrollo de un Esquema de Ciberseguridad para Entornos Empresariales"**, el cual establece un marco integral de controles y arquitecturas seguras adaptadas a la realidad de las PyMEs regionales. Como base fundamental, el proyecto general ha establecido un ecosistema de controles basados en marcos como **NIST CSF 2.0** y **CIS Controls**, integrando arquitecturas de detección mediante **Inteligencia Artificial** y **Machine Learning**.

En abril de 2026, el Center for Internet Security (CIS) publicó guías complementarias específicas para sistemas de Inteligencia Artificial (IA) y Modelos de Lenguaje Grande (LLMs), incorporando el concepto de “Shadow AI” para referirse al uso no aprobado o no gestionado de herramientas de IA dentro de una organización. Este fenómeno representa un riesgo relevante de fuga de información, especialmente en organizaciones sin equipo de seguridad dedicado. Las PyMEs argentinas resultan particularmente expuestas a esta problemática, debido a que muchas veces carecen de soluciones accesibles que permitan auditar y controlar este uso sin requerir infraestructura costosa ni personal altamente especializado.

El desarrollo de este proyecto se llevará a cabo por las integrantes Denise Pujalte legajo: 26624 y Zaira Rosin legajo: 26537, donde mediante la división de tareas, en conjunto se implementará la propuesta. Ambos proyectos de prácticas comparten el mismo antecedente de investigación. El aporte conjunto al proyecto general del CInApTIC consiste en validar empíricamente que un sistema liviano puede detectar y mitigar el riesgo de fuga de datos por Shadow AI en el contexto específico de las PYMES argentinas, articulando un motor de detección basado en NLP con una interfaz de usuario orientada a la intervención contextual.

**DESCRIPCIÓN DEL PROYECTO**

El presente trabajo consiste en el diseño, implementación y validación de un sistema liviano de prevención de fuga de datos orientado a PYMES, que actúa en el momento exacto en que un empleado intenta enviar información sensible a una herramienta de IA externa (ChatGPT, Gemini, Claude u otras). El sistema se compone de tres módulos integrados: una extensión de navegador que intercepta el texto antes del envío, un backend de análisis que aplica técnicas de Procesamiento de Lenguaje Natural (NLP) y reglas para detectar datos sensibles, y un dashboard de administración que registra los eventos para auditoría.

A diferencia de las soluciones empresariales existentes (Netskope, Microsoft Defender for Cloud Apps), este sistema está diseñado para funcionar sin infraestructura de red compleja, a costo mínimo y sin requerir configuración especializada. El enfoque no es prohibir el uso de IA, sino intervenir contextualmente: cuando detecta riesgo, muestra al empleado una explicación en lenguaje simple de por qué el dato es sensible, preservando la autonomía del usuario y maximizando el aprendizaje en el momento del error.

Dentro del desarrollo integral del producto, esta práctica se concentra específicamente en la capa de interfaz de usuario y auditoría, que se compone de los siguientes elementos:

**Extensión de navegador:** Desarrollo del frontend encargado de interceptar el texto en los formularios de las herramientas de IA (ChatGPT, Gemini, Claude, entre otras) antes de que el usuario envíe la información.

**Interfaz de intervención contextual:** Implementación del sistema de alertas que muestra al usuario una explicación en lenguaje simple sobre por qué el dato es sensible, preservando su autonomía y maximizando el aprendizaje.

**Dashboard de administración:** Desarrollo del panel de registro y auditoría que almacena los eventos detallando el usuario, el tipo de dato detectado y la IA de destino.

**OBJETIVOS DEL PROYECTO**

- Implementar la extensión de navegador capaz de detectar formularios de IA e interceptar el texto antes del envío de información sensible.
- Desarrollar el dashboard de administración para el registro de eventos, usuario, tipo de dato detectado e IA destino.
- Diseñar e implementar la interfaz de intervención contextual que muestra explicaciones en lenguaje simple al usuario en caso de riesgo.
- Validar el sistema mediante simulaciones controladas con escenarios representativos del contexto empresarial local, evaluando la efectividad de la intervención contextual frente al bloqueo genérico.

**OBJETIVOS PARA LA PS DEL PROYECTO**

- Aplicar y consolidar conocimientos de ingeniería de software, redes y diseño de sistemas mediante el desarrollo de la extensión y el dashboard de administración del sistema.
- Transformar marcos teóricos de ciberseguridad en una implementación técnica funcional orientada al usuario final no técnico de una PYME argentina.
- Diseñar e implementar un entorno de pruebas reproducible para evaluar la efectividad de la intervención contextual frente al bloqueo genérico en el comportamiento del usuario.
- Producir evidencia empírica sobre la usabilidad del sistema que retroalimente el proyecto general del grupo CInApTIC.
- Integrar la extensión con el motor de detección desarrollado por la otra integrante, garantizando la comunicación correcta entre el frontend y el backend de análisis.
- Validar el sistema mediante simulaciones controladas con escenarios representativos del contexto empresarial local, evaluando la efectividad de la intervención contextual frente al bloqueo genérico.

**TIEMPO ESTIMADO DE DURACIÓN DE LA PPS (en horas)**

Fecha inicio: 5/05/2026

Fecha fin: 20/10/2026

Horario de trabajo que deberá cumplir el alumno: 15:00 a 18:00 hs.

Semana laboral: Horas: Lunes, Martes y Jueves

Horas semanales: 6hs.

Duración Total: 200 horas

**DESCRIPCIÓN DE LAS ACTIVIDADES**

En función de los Objetivos indicados para la PS, se listarán detalladamente las Etapas y las tareas a desarrollar.

ETAPA

TAREAS

DURACIÓN en HS

RESULTADOS ESPERADOS

Zaira Rosin

Denise Pujalte

**1. Relevamiento y Marco Teórico**

Estudio de estándares NIST CSF 2.0, CIS Controls v8.1 y regulación Ley 25326.

40

Marco teórico documentado con foco en arquitectura del sistema, requerimientos funcionales definidos y escenario de simulación redactado.

X

Relevamiento del problema: uso de IA no supervisada en PYMES.

X

Investigación de la API de extensiones de, arquitecturas y frameworks de dashboard.

X

Redacción del escenario de simulación y especificación de los casos de uso del sistema.

X

Definición conjunta de la estructura de datos, payloads y flujo de comunicación entre la extensión de navegador y el motor de análisis.

X

X

**2. Diseño de Arquitectura**

Diseño de la arquitectura del sistema: extensión de Chrome, backend de análisis y dashboard de administración.

30

Arquitectura técnica documentada con diagramas de flujo, especificaciones de componentes y diseño de interfaz de usuario definido.

X

Definición del flujo completo: captura del texto en el navegador, envío al backend, recepción de la decisión y muestra del mensaje contextual al usuario.

X

Diseño de la interfaz de la extensión: modal de alerta, mensajes explicativos por tipo de dato y opciones de acción.

X

Documentación de la arquitectura técnica, diagramas de componentes y especificaciones de cada módulo del sistema.

X

Consolidación y validación del contrato de la API y el flujo de decisión (riesgo bajo / medio / alto) entre el frontend y el backend.

X

X

**3. Implementación**

Desarrollo de la extensión: interceptación de texto en formularios de IAs externas (ChatGPT, Gemini, Claude).

70

Extensión funcional con intercepción y alerta contextual, y dashboard de administración operativo con registro de eventos.

X

Implementación del canal de comunicación entre la extensión y el backend FastAPI: envío del texto, recepción del score de riesgo y mensaje contextual.

X

Desarrollo del módulo de scoring de riesgo y generación de mensajes contextuales explicativos.

X

Implementación del dashboard de administración con registro de eventos, usuario, tipo de dato detectado e IA destino.

X

Integración y conexión de la extensión con el backend para validar el envío de datos y la recepción de la respuesta con el análisis de riesgo.

X

X

**4. Simulación y Prueba**

Diseño de escenarios de prueba: texto sin y con datos sensibles, texto con código propietario, combinaciones mixtas.

35

Matriz de resultados con métricas de usabilidad, tasa de aceptación de alertas y comportamiento del usuario ante diferentes tipos de intervención.

X

Ejecución de simulaciones con tres perfiles de empleado diferenciados.

X

Evaluación del impacto de la intervención contextual: comparación entre recibir una explicación vs. un mensaje de bloqueo genérico.

X

Registro sistemático de resultados y tabulación comparativa.

X

Ejecución de la simulación del flujo completo de extremo a extremo (escritura, intercepción, envío, análisis y respuesta) utilizando los perfiles de prueba.

X

X

**5. Análisis y Cierre**

Análisis de la brecha entre el comportamiento esperado y el empírico del sistema.

25

Informe final con análisis de usabilidad, efectividad de la intervención contextual y recomendaciones documentadas.

X

Evaluación del impacto en la experiencia del usuario: intervención contextual vs. bloqueo sin explicación

X

Redacción del informe final con hallazgos, limitaciones y recomendaciones.

X

Consolidación de la documentación, integración de los entornos de prueba y transferencia final del sistema al grupo CInApTIC.

X

X

Ambas integrantes comparten el mismo horario y carga horaria de 200 horas. Las etapas incluyen instancias de trabajo conjunto para definir el contrato de integración y consolidar la documentación y los entregables finales del sistema completo. El sistema se implementa mediante un stack desacoplado donde el backend, desarrollado en Python con FastAPI, se encarga del análisis de datos mediante técnicas de NLP, mientras que el frontend, desarrollado en JavaScript mediante una extensión de navegador y un dashboard en React, gestiona la interacción con el usuario y la visualización de eventos.

**ÁREAS DE CONOCIMIENTO QUE INVOLUCRA **

1. De acuerdo a las actividades especificadas respectivamente, completar la siguiente tabla indicando que asignaturas de la carrera le sirvieron para llevar a cabo las mismas, por cada una enumerar los temas involucrados y en qué actividad los aplica.

Asignatura

Temas

Tarea

Sistemas Operativos

Gestión de procesos, permisos, ejecución de scripts, comunicación entre procesos (IPC).

Desarrollo del backend Python (FastAPI) y lógica de intercepción en la extensión.

Redes de Datos

Protocolos HTTP/HTTPS, arquitectura cliente-servidor, proxies, APIs REST.

Diseño del canal de comunicación entre la extensión y el backend de análisis.

Análisis de Sistemas

Relevamiento de requerimientos, modelado de procesos, especificación funcional.

Diseño del flujo de intercepción, análisis y decisión del sistema.

Ingeniería y Calidad de Software

Ciclo de vida del software, patrones de diseño, pruebas unitarias, integración de módulos.

Implementación modular del sistema, integración entre extensión y backend, y diseño de escenarios de prueba.

Diseño de Sistemas

Diseño de experiencia de usuario (UX), componentes interactivos, accesibilidad.

Diseño e implementación del modal de alerta de la extensión y del dashboard de administración en React.

1. De acuerdo a las actividades especificadas respectivamente, completar la siguiente tabla indicando los nuevos conocimientos que debe investigar y en qué actividades los aplicará.

Temas

Tarea

Referencia Bibliográfica[\[1\]](#footnote-1)

**Desarrollo de extensiones **

Implementación del content script que intercepta texto en formularios de IAs externas antes del envío.

Google Developers. (2024). Chrome Extensions – Manifest V3. Recuperado de https://developer.chrome.com/docs/extensions/mv3

**Diseño de APIs REST con FastAPI (Python)**

Implementación del endpoint que recibe el texto de la extensión, invoca el módulo de análisis y retorna la decisión.

Ramírez, S. (2023). FastAPI Documentation. Recuperado de https://fastapi.tiangolo.com

**Desarrollo de dashboards con React**

Implementación del panel de administración con visualización de eventos, métricas y registros de actividad.

Meta. (2024). React – A JavaScript library for building user interfaces. Recuperado de https://react.dev

**Shadow AI y fuga de datos en herramientas de IA externas**

Marco conceptual del problema: empleados que envían datos sensibles a IAs no autorizadas (ChatGPT, Gemini, etc.).

Center for Internet Security. (2026). AI and LLM Companion Guide to CIS Controls v8.1. CIS.

**Ley 25326 – Protección de Datos Personales (Argentina)**

Definición legal de datos sensibles y su impacto en el diseño de los mensajes contextuales de la extensión.

Agencia de Acceso a la Información Pública. (2000). Ley 25.326. Recuperado de https://www.argentina.gob.ar/aaip



**TIPO DE TEMA EN EL QUE SE ENMARCARÁ EL TRABAJO** (monográfico; panorámico; teórico; científico; práctico; etc.)

Este trabajo se enmarca bajo una modalidad práctica-experimental e integrada. La dimensión práctica se materializa en el desarrollo de un módulo funcional de detección y clasificación de información sensible, mientras que la dimensión experimental se refleja en su validación mediante simulaciones controladas y métricas cuantitativas. A su vez, el proyecto posee una dimensión integrada, dado que el módulo desarrollado será articulado con los componentes de interfaz, backend y dashboard desarrollados en conjunto, permitiendo evaluar el funcionamiento del sistema completo



**APORTES QUE SE ESPERA REALIZAR CON ESTE TRABAJO **(tanto para la formación profesional como para la empresa y la comunidad)

Formación profesional: desarrollo de competencias avanzadas en NLP, aplicado a seguridad, desarrollo de extensiones de navegador y diseño de sistemas orientados a usuarios no técnicos.

Aporte al grupo CInApTIC: sistema funcional documentado, entorno de pruebas reproducible y reporte de resultados empíricos que retroalimentarán el proyecto de investigación general.

Aporte a la comunidad: el proyecto visibiliza un riesgo concreto y creciente en las PYMES de la región (fuga de datos por uso de IA externa) y ofrece una solución adaptada a sus limitaciones económicas y técnicas, alineada con la normativa argentina vigente.

**Firma del Director del Proyecto:          **

Aclaración de Firma: Diego A. Bolatti

**Firma del Alumno:       **

**Aclaración de Firma: Rosin, Zaira Antonella**

**Fecha de Presentación: 05/ 05 / 2026**

**Aceptación de la PPS**

**Firma Profesor:	**

__Fecha Aceptación: ___ / ____ / ______

1.  Aplicar Norma APA para realizar la referencia bibliográfica
