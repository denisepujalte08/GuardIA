# Contexto del Proyecto

## Problema

Las PyMES argentinas están adoptando herramientas de IA generativa (ChatGPT, Gemini, Claude, etc.) de forma no supervisada. Los empleados copian y pegan información sensible (DNI, CUIT, CBU, datos comerciales, código propietario) directamente en estos servicios sin comprender el riesgo que implica enviar datos confidenciales a plataformas externas. Este fenómeno, denominado **Shadow AI** por el Center for Internet Security (CIS), es una de las principales fuentes de fuga de datos en organizaciones que no cuentan con equipos de seguridad dedicados.

Las soluciones comerciales existentes (Netskope, Microsoft Defender for Cloud Apps) requieren infraestructura de red compleja, licencias costosas y personal especializado, lo que las hace inaccesibles para la mayoría de las PyMES de la región.

## Qué proponemos

Desarrollar un **sistema liviano de prevención de fuga de datos** que se interponga entre el empleado y la herramienta de IA en el momento exacto del envío. El sistema no prohíbe el uso de IA, sino que **interviene contextualmente**: cuando detecta que el texto contiene información sensible, muestra al usuario una explicación en lenguaje simple de por qué ese dato es riesgoso, preservando su autonomía y favoreciendo la concientización.

## Arquitectura del sistema

El sistema se compone de tres módulos principales:

```
┌─────────────────────┐
│   Extensión Chrome   │  ← Intercepta el texto antes del envío
│   (JavaScript)       │
└────────┬────────────┘
         │ POST /analyze
         ▼
┌─────────────────────┐
│   Backend (FastAPI)  │  ← Analiza el texto con NLP y reglas
│   Python + spaCy     │
└────────┬────────────┘
         │ Score + mensaje
         ▼
┌─────────────────────┐
│   Modal de alerta    │  ← Muestra la intervención contextual
│   (en el navegador)  │
└─────────────────────┘
         │
         ▼
┌─────────────────────┐
│   Dashboard React    │  ← Registra eventos para auditoría
│   (admin panel)      │
└─────────────────────┘
```

### 1. Extensión de navegador (Chrome, Manifest V3)

El componente del frontend que se ejecuta directamente en el navegador del empleado. Utiliza content scripts para detectar cuándo el usuario está escribiendo en un formulario de una herramienta de IA conocida (ChatGPT, Gemini, Claude, etc.) y captura el texto antes de que sea enviado.

**Responsabilidades:**
- Detectar formularios de texto en sitios de IA externos
- Interceptar el contenido antes del envío
- Enviar el texto al backend para su análisis
- Recibir el resultado del análisis (score de riesgo + mensaje contextual)
- Mostrar un modal de alerta si se detecta riesgo
- Permitir al usuario decidir si envía, edita o cancela

### 2. Backend de análisis (Python, FastAPI)

El motor central del sistema. Recibe el texto de la extensión, lo analiza mediante técnicas de Procesamiento de Lenguaje Natural (NLP) y reglas configurables, y retorna un score de riesgo junto con un mensaje explicativo.

**Responsabilidades:**
- Recibir texto via API REST
- Aplicar expresiones regulares para patrones específicos argentinos (DNI, CUIT/CUIL, CBU, emails, teléfonos, tokens)
- Ejecutar detección de entidades nombradas con spaCy (nombres, organizaciones, ubicaciones)
- Clasificar el riesgo en niveles: bajo, medio, alto, crítico
- Generar mensajes contextuales explicativos para cada nivel
- Exponer endpoints REST para la extensión y el dashboard

### 3. Dashboard de administración (React)

Panel web destinado al administrador o responsable de seguridad de la PyME. Permite visualizar los eventos de intercepción, los tipos de datos detectados, los usuarios involucrados y las herramientas de IA de destino.

**Responsabilidades:**
- Registrar cada evento de intercepción (usuario, texto parcial, tipo de dato, IA destino, nivel de riesgo, acción tomada)
- Visualizar métricas y estadísticas de uso
- Permitir la auditoría de actividad

## División de trabajo

El proyecto se desarrolla de forma conjunta entre dos integrantes, cada una enfocada en un componente:

| Integrante | Enfoque principal | Componentes |
|---|---|---|
| **Denise Pujalte** (26624) | Motor de detección e IA | Backend FastAPI, motor NLP, expresiones regulares, scoring de riesgo, clasificación |
| **Zaira Rosin** (26537) | Interfaz de usuario y auditoría | Extensión Chrome, modal de intervención contextual, dashboard React, registro de eventos |

Ambas comparten tareas de diseño de arquitectura, definición del contrato de integración API, pruebas y cierre.

## Stack tecnológico

| Capa | Tecnología |
|---|---|
| Extensión | JavaScript, Chrome Extensions (Manifest V3), APIs de Chrome |
| Backend | Python 3, FastAPI, spaCy (NER en español), scikit-learn |
| Dashboard | React, JavaScript |
| Comunicación | API REST (JSON) |
| Normativa | NIST CSF 2.0, CIS Controls v8.1, Ley 25.326 |

## Datos sensibles a detectar

El motor de detección busca los siguientes patrones en el texto enviado por el usuario:

- **DNI** argentino (8 dígitos)
- **CUIT / CUIL** (formato XX-XXXXXXXX-X)
- **CBU** (22 dígitos)
- **Correos electrónicos**
- **Teléfonos** argentinos
- **Credenciales y tokens** (API keys, contraseñas, tokens de acceso)
- **Datos comerciales** (montos, facturas, datos de clientes)
- **Código propietario** (nombres de funciones, variables, fragmentos de código)

## Clasificación de riesgo

| Nivel | Criterio | Ejemplo |
|---|---|---|
| **Bajo** | Texto genérico sin datos identificables | "Necesito ayuda con Python" |
| **Medio** | Posibles datos personales sin confirmar | Nombre completo, organización |
| **Alto** | Datos personales confirmados | DNI, email, teléfono |
| **Crítico** | Datos financieros o credenciales | CUIT, CCBU, tokens, API keys |

## Flujo completo de una intercepción

1. El empleado escribe un prompt en ChatGPT/Gemini/Claude
2. Antes de enviar, la extensión detecta el formulario y captura el texto
3. La extensión envía el texto al backend via POST
4. El backend analiza el texto: regex + NER + scoring
5. El backend retorna el nivel de riesgo y un mensaje contextual
6. Si el riesgo es medio/alto/crítico, la extensión muestra un modal explicativo
7. El empleado decide: enviar, editar o cancelar
8. El evento se registra en el dashboard para auditoría

## Marco normativo

- **NIST CSF 2.0**: Framework de ciberseguridad para gestión de riesgos
- **CIS Controls v8.1**: Controles específicos para protección ante Shadow AI (publicados abril 2026)
- **Ley 25.326**: Protección de Datos Personales de Argentina, que define categorías de datos sensibles y obligaciones de las organizaciones

## Resultados esperados

- Módulo de detección funcional con métricas cuantitativas (precisión, recall, F1-score, falsos positivos/negativos)
- Extensión Chrome operativa con intervención contextual
- Dashboard de administración con registro de eventos
- Dataset de prueba documentado con escenarios representativos de PyMES
- Documentación técnica completa para transferencia al grupo CInApTIC
