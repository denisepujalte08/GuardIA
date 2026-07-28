**PLAN DE TRABAJO**

**DATOS DEL ALUMNO**

Apellido y Nombres:	Pujalte, Denise Macarena

DNI / DU / CI / CE: 44153986

Legajo UTN Nº: 26624

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

El desarrollo de este proyecto se llevará a cabo por las integrantes Denise Pujalte legajo: 26624 y Zaira Rosin legajo: 26537, donde, en conjunto, implementarán la solución mediante la división de tareas. Ambos proyectos de prácticas comparten el mismo antecedente de investigación. El aporte conjunto al proyecto general del CInApTIC consiste en validar empíricamente que un sistema liviano puede detectar y mitigar el riesgo de fuga de datos por Shadow AI en el contexto específico de las PYMES argentinas, articulando un motor de detección basado en NLP con una interfaz de usuario orientada a la intervención contextual.

**DESCRIPCIÓN DEL PROYECTO**

El presente trabajo consiste en el diseño, implementación y validación de un sistema liviano de prevención de fuga de datos orientado a PYMES, que actúa en el momento exacto en que un empleado intenta enviar información sensible a una herramienta de IA externa (ChatGPT, Gemini, Claude u otras). El sistema se compone de tres módulos integrados: una extensión de navegador que intercepta el texto antes del envío, un backend de análisis que aplica técnicas de Procesamiento de Lenguaje Natural (NLP) y reglas para detectar datos sensibles, y un dashboard de administración que registra los eventos para auditoría.

A diferencia de las soluciones empresariales existentes (Netskope, Microsoft Defender for Cloud Apps), este sistema está diseñado para funcionar sin infraestructura de red compleja, a costo mínimo y sin requerir configuración especializada. El enfoque no es prohibir el uso de IA, sino intervenir contextualmente: cuando detecta riesgo, muestra al empleado una explicación en lenguaje simple de por qué el dato es sensible, preservando la autonomía del usuario y favoreciendo la concientización en el momento del error.

De esta manera, el aporte específico de esta práctica será proveer el componente de detección inteligente del sistema, encargado de determinar cuándo un contenido puede representar un riesgo de fuga de datos y justificar dicha clasificación mediante criterios comprensibles y trazables.

**OBJETIVOS DEL PROYECTO**

- Diseñar e implementar un módulo de detección de información sensible aplicable al uso de herramientas de IA generativa externas en entornos de PyMEs.
- Desarrollar un motor de análisis multicapa que combine reglas configurables y técnicas de Procesamiento de Lenguaje Natural para detectar contenido potencialmente sensible.
- Validar el módulo de detección mediante simulaciones controladas, utilizando casos de prueba representativos y métricas cuantitativas.
- Alinear los criterios de detección y clasificación con los lineamientos de CIS Controls v8.1 y la Ley 25.326 de Protección de Datos Personales de Argentina.

**OBJETIVOS PARA LA PS DEL PROYECTO**

- Aplicar conocimientos de inteligencia artificial, procesamiento de lenguaje natural, ciberseguridad e ingeniería de software en el desarrollo de un módulo funcional de detección de información sensible.
- Transformar criterios teóricos de protección de datos y prevención de fuga de información en reglas, patrones y mecanismos técnicos de análisis automatizado.
- Evaluar empíricamente el desempeño del motor de detección mediante métricas cuantitativas, identificando aciertos, errores, limitaciones y oportunidades de mejora.
- Producir evidencia técnica y documentación que pueda integrarse al sistema general desarrollado en conjunto, aportando al proyecto de investigación del grupo CInApTIC.

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

Denise Pujalte

Zaira Rosin

**1. Relevamiento y Marco Teórico**

Estudio de estándares NIST CSF 2.0, CIS Controls v8.1 y regulación Ley 25326.

40

Marco teórico documentado, catálogo de patrones de datos sensibles definido y especificación inicial de reglas configurables del sistema.

X

Relevamiento del problema: uso de IA no supervisada en PYMES.

X

Investigación de técnicas de detección mediante expresiones regulares, NLP y NER.

X

Identificación de patrones de datos sensibles para el contexto argentino (CUIT, CBU, código propietario).

X

Redacción del marco teórico del módulo de detección y definición del catálogo de patrones a cubrir.

X

Definición conjunta de la estructura de datos, payloads y flujo de comunicación entre la extensión de navegador y el motor de análisis.

X

X

**2. Diseño del motor de detección y clasificación de riesgo**

Definición de patrones a detectar: DNI, CUIT/CUIL, CBU, correos, teléfonos, credenciales, tokens, datos comerciales y código propietario.

35

Especificación funcional del motor de detección, matriz de riesgo, modelo de scoring, reglas de clasificación y contrato de integración documentados.

X

Diseño de reglas de clasificación y definición de niveles de riesgo bajo, medio, alto y crítico.

X

Diseño del modelo de scoring para asignar el nivel de riesgo del contenido analizado.

X

Diseño de mensajes contextuales asociados a cada nivel.

X

Diseño del formato de entrada/salida del módulo de análisis para integrarse con el sistema general.

X

Consolidación y validación del contrato de la API y el flujo de decisión (riesgo bajo / medio / alto) entre el frontend y el backend.

X

X

**3. Implementación**

Implementación de expresiones regulares para patrones locales.

75

Módulo de detección funcional, capaz de analizar texto, identificar datos sensibles, clasificar riesgo y generar respuestas contextuales.

X

Implementación de técnicas de Procesamiento de Lenguaje Natural para la detección de entidades o información contextual.

X

Desarrollo de reglas configurables para identificar información confidencial o propietaria.

X

Implementación del scoring de riesgo.

X

Generación de mensajes explicativos para el usuario.

X

Exposición del módulo mediante endpoints del backend para su integración con la extensión y el dashboard.

X

Pruebas unitarias del módulo de detección.

X

Integración y conexión de la extensión con el backend para validar el envío de datos y la recepción de la respuesta con el análisis de riesgo.

X

X

**4. Simulación y Prueba**

Construcción de casos de prueba sintéticos con textos seguros, sospechosos y críticos.

35

Dataset de prueba documentado, resultados cuantitativos del desempeño del módulo y matriz comparativa de evaluación

X

Diseño de escenarios de simulación con distintos perfiles de usuario.

X

Ejecución de pruebas controladas.

X

Medición de precisión, recall, falsos positivos, falsos negativos y tiempo de respuesta.

X

Ajuste de reglas a partir de resultados obtenidos.

X

Ejecución de la simulación del flujo completo de extremo a extremo (escritura, intercepción, envío, análisis y respuesta) utilizando los perfiles de prueba.

X

X

**5. Análisis y Cierre**

Análisis de resultados obtenidos.

15

Informe final del módulo de IA/detección, documentación técnica y componente integrado al prototipo general.

X

Identificación de limitaciones técnicas y riesgos residuales.

X

Documentación del módulo de detección.

X

Elaboración de recomendaciones para futuras mejoras.

X

Preparación de informe final y demo.

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

Inteligencia Artificial

Procesamiento de lenguaje natural, detección de entidades nombradas, clasificación de texto, evaluación de modelos.

Diseño e implementación del motor de detección de información sensible.

Seguridad en Sistemas de Información

Estándares NIST CSF 2.0 y CIS Controls, protección de datos (Ley 25326), clasificación de información sensible, gestión de riesgos.

Definición de riesgos, criterios de detección y alineación con marcos de ciberseguridad.

Algoritmos y Estructuras de Datos

Búsqueda de patrones, procesamiento de cadenas, estructuras para clasificación, eficiencia algorítmica, recursividad.

Implementación de reglas, expresiones regulares y análisis del contenido ingresado por el usuario.

Ingeniería y Calidad de Software

Modularización, diseño de componentes, pruebas, documentación técnica, control de versiones, despliegue de software.

Desarrollo del módulo de detección e integración con el backend del sistema.

Análisis de Sistemas de Información

Relevamiento de requerimientos, definición de reglas de negocio, modelado funcional.

Definición del flujo de análisis, clasificación y respuesta ante contenido riesgoso.

Probabilidad y Estadística

Métricas de evaluación (precisión, recall), falsos positivos, falsos negativos, inferencia estadística, análisis de resultados.

Validación experimental del módulo de detección.

Desarrollo de Software

Arquitectura de aplicaciones multicapa, APIs REST, desarrollo seguro, pruebas unitarias, integración de módulos.

Implementación del backend en Python/FastAPI y exposición de endpoints para integración con la extensión y el dashboard.

Sintaxis y Semántica de los Lenguajes

Expresiones regulares, gramáticas formales, análisis léxico y sintáctic

Implementación y diseño de los patrones regex para detectar DNI, CUIT, CBU, tokens, etc.

Diseño de Sistemas de Información

Diseño de arquitecturas, diseño de componentes, integración de sistemas, calidad y seguridad en diseño.

Diseño del motor de detección y del contrato de integración con el sistema general.

1. De acuerdo a las actividades especificadas respectivamente, completar la siguiente tabla indicando los nuevos conocimientos que debe investigar y en qué actividades los aplicará.

Temas

Tarea

Referencia Bibliográfica[\[1\]](#footnote-1)

**Shadow AI y riesgos de fuga de datos en IA generativa**

Fundamentar el problema del uso no supervisado de herramientas externas de IA en organizaciones.

Center for Internet Security. (2026). *Artificial Intelligence and Large Language Models Companion Guide v1.0: CIS Critical Security Controls v8.1*. CIS.

**Detección de entidades nombradas con spaCy en español**

Implementar detección de nombres, organizaciones, ubicaciones y posibles datos personales en texto.

Honnibal, M., & Montani, I. (2017). *spaCy 2: Natural language understanding with Bloom embeddings, convolutional neural networks and incremental parsing*. [https://spacy.io](https://spacy.io)

**Clasificación de texto y scoring de riesgo**

Definir criterios para clasificar textos según niveles de riesgo bajo, medio, alto y crítico e implementar el modelo de scoring.

Pedregosa, F., et al. (2011). Scikit-learn: Machine Learning in Python. *Journal of Machine Learning Research*, *12*, 2825–2830.

**Métricas de evaluación de modelos de clasificación**

Medir precisión, recall, F1-score, falsos positivos, falsos negativos y tiempo de respuesta del módulo.

Powers, D. M. W. (2011). Evaluation: From precision, recall and F-measure to ROC, informedness, markedness and correlation. *Journal of Machine Learning Technologies*, *2*(1), 37–63.



**Ley 25.326 de Protección de Datos Personales**

Definir categorías de datos personales y sensibles aplicables al contexto argentino.

Agencia de Acceso a la Información Pública. (2000). *Ley 25.326 de Protección de los Datos Personales*. [https://www.argentina.gob.ar/aaip](https://www.argentina.gob.ar/aaip)

**Diseño de datasets sintéticos para pruebas de seguridad**

Construir casos de prueba representativos con textos seguros, sospechosos y críticos que simulen situaciones reales en PyMEs.

Lison, P., & Brandl, R. (2021). Anonymisation models for clinical data: State of the art and future directions. En *Proceedings of the 59th Annual Meeting of the Association for Computational Linguistics* (pp. 4291–4306). ACL.

**Expresiones regulares aplicadas a detección de datos sensibles**

Implementar patrones regex para identificar DNI, CUIT/CUIL, CBU, correos electrónicos, teléfonos y tokens.

Friedl, J. E. F. (2006). *Mastering Regular Expressions* (3rd ed.). O'Reilly Media.

**TIPO DE TEMA EN EL QUE SE ENMARCARÁ EL TRABAJO** (monográfico; panorámico; teórico; científico; práctico; etc.)

Este trabajo se enmarca bajo una modalidad práctica-experimental e integrada. La dimensión práctica se materializa en el desarrollo de un módulo funcional de detección y clasificación de información sensible, mientras que la dimensión experimental se refleja en su validación mediante simulaciones controladas y métricas cuantitativas. A su vez, el proyecto posee una dimensión integrada, dado que el módulo desarrollado será articulado con los componentes de interfaz, backend y dashboard desarrollados en conjunto, permitiendo evaluar el funcionamiento del sistema completo.



**APORTES QUE SE ESPERA REALIZAR CON ESTE TRABAJO **(tanto para la formación profesional como para la empresa y la comunidad)

- Formación profesional: desarrollo de competencias en Procesamiento de Lenguaje Natural aplicado a ciberseguridad, detección de información sensible, diseño de reglas de clasificación, validación experimental e integración de módulos dentro de un sistema de software.
- Aporte al grupo CInApTIC: sistema funcional documentado, entorno de pruebas reproducible y reporte de resultados empíricos que retroalimentarán el proyecto de investigación general.
- Aporte a la comunidad: el proyecto visibiliza un riesgo concreto y creciente en las PYMES de la región (fuga de datos por uso de IA externa) y ofrece una solución adaptada a sus limitaciones económicas y técnicas, alineada con la normativa argentina vigente.

**Firma del Director del Proyecto:          **

Aclaración de Firma: Diego A. Bolatti

**Firma del Alumno:       **

**Aclaración de Firma: Pujalte, Denise Macarena**

**Fecha de Presentación: 05/ 05 / 2026**

**Aceptación de la PPS**

**Firma Profesor:	**

__Fecha Aceptación: ___ / ____ / ______

1.  Aplicar Norma APA para realizar la referencia bibliográfica
