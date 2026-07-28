

### **Cómo simularlo para la práctica supervisada**

#### **Componente 1 — La extensión de Chrome**

Para el MVP no necesitás interceptar tráfico real de red. La extensión puede usar la API de Chrome para leer el contenido del textarea antes de que el usuario presione Enter en ChatGPT, Gemini o Claude.

javascript  
// content\_script.js — se inyecta en la página de la IA  
document.addEventListener('keydown', (e) \=\> {  
  if (e.key \=== 'Enter') {  
    const textarea \= document.querySelector('textarea');  
    const texto \= textarea?.value;  
    if (texto) analizarTexto(texto, e); // intercepta antes de enviar  
  }  
});

Para la demo podés simular tres escenarios: empleado escribe texto normal, empleado escribe algo con un CUIT o CBU, y empleado pega código con comentarios que dicen "confidencial".

---

#### **Componente 2 — El backend de análisis**

Tres detectores en Python que podés levantar con FastAPI en localhost:

El primer detector usa `spaCy` con el modelo en español (`es_core_news_sm`, gratuito) para detectar personas, organizaciones y lugares. El segundo usa expresiones regulares para patrones argentinos específicos: CUIT (formato XX-XXXXXXXX-X), CBU (22 dígitos), patentes, números de póliza. El tercero es un clasificador simple entrenado con 50-100 ejemplos de textos "propietarios" versus textos genéricos, usando `scikit-learn` con TF-IDF. No necesitás miles de ejemplos para una demo funcional.

python  
\# detector.py  
import spacy  
import re

nlp \= spacy.load("es\_core\_news\_sm")

PATRONES \= {  
    "CUIT": r"\\b\\d{2}-\\d{8}-\\d{1}\\b",  
    "CBU":  r"\\b\\d{22}\\b",  
    "tarjeta": r"\\b\\d{4}\[\\s-\]\\d{4}\[\\s-\]\\d{4}\[\\s-\]\\d{4}\\b"  
}

def analizar(texto):  
    doc \= nlp(texto)  
    hallazgos \= \[\]  
    for pat, regex in PATRONES.items():  
        if re.search(regex, texto):  
            hallazgos.append({"tipo": pat, "severidad": "alta"})  
    for ent in doc.ents:  
        if ent.label\_ in \["PER", "ORG"\]:  
            hallazgos.append({"tipo": ent.label\_, "texto": ent.text, "severidad": "media"})  
    return hallazgos  
---

#### **Componente 3 — El mensaje contextual**

Lo más importante para la demo es que el mensaje que aparece NO sea genérico. Tiene que explicar exactamente qué detectó y por qué es riesgoso:

En vez de "Acción bloqueada por política de seguridad", mostrar algo como: "Detectamos un CUIT en el texto que estás por enviar. Los CUITs son datos fiscales que identifican a tu empresa o clientes. Compartirlos con una IA externa puede violar la Ley 25326 de protección de datos. ¿Querés continuar de todas formas o editá el texto primero?"

Eso se puede hacer con una ventana modal inyectada desde la extensión, sin necesidad de UI compleja.

---

#### **Componente 4 — El dashboard**

Para el MVP alcanza con una página web simple en React o incluso HTML plano que muestre una tabla con los eventos registrados: fecha, usuario simulado, tipo de dato detectado, IA de destino, y si el empleado continuó o canceló. Eso es suficiente para demostrar el valor del sistema ante el jurado.

---

### **Entorno de simulación para la demo**

Para demostrar todo sin infraestructura real podés usar tres usuarios simulados en el mismo equipo, un documento de "datos sensibles de clientes" con CUITs y nombres ficticios, y tres escenarios: uno donde el empleado intenta pegar esos datos en ChatGPT, otro donde escribe código con comentarios confidenciales, y otro donde escribe texto totalmente genérico que pasa sin alerta.

Eso en 5 minutos de demo comunica perfectamente el problema y la solución.

¿Querés que armemos el código base de la extensión y el backend, o primero definimos el stack tecnológico completo con las versiones específicas?

