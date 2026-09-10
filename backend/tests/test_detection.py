"""
test_detection.py

Pruebas unitarias del motor de análisis de riesgo (app/detection.py).
Cubre cada regla configurada, la capa de NLP (NER con spaCy) y el caso
de riesgo bajo (texto sin datos sensibles).
"""

from app.detection import analizar_texto


def test_texto_sin_datos_sensibles_es_riesgo_bajo():
    resultado = analizar_texto("Necesito ayuda para escribir una función en Python que ordene una lista")
    assert resultado.nivel_riesgo == "bajo"
    assert resultado.tipo_dato_detectado is None


def test_cuit_es_riesgo_critico():
    resultado = analizar_texto("Mi CUIT es 20-38456712-4")
    assert resultado.nivel_riesgo == "critico"
    assert resultado.tipo_dato_detectado == "CUIT/CUIL"


def test_cbu_es_riesgo_critico():
    resultado = analizar_texto("El CBU es 2850590940090418135201")
    assert resultado.nivel_riesgo == "critico"
    assert resultado.tipo_dato_detectado == "CBU"


def test_credencial_es_riesgo_critico():
    resultado = analizar_texto("La clave es api_key: sk-12345abcde")
    assert resultado.nivel_riesgo == "critico"
    assert resultado.tipo_dato_detectado == "Credencial o token"


def test_dni_es_riesgo_alto():
    resultado = analizar_texto("Mi DNI es 30123456")
    assert resultado.nivel_riesgo == "alto"
    assert resultado.tipo_dato_detectado == "DNI"


def test_dni_con_puntos_es_riesgo_alto():
    resultado = analizar_texto("Mi DNI es 30.123.456")
    assert resultado.nivel_riesgo == "alto"
    assert resultado.tipo_dato_detectado == "DNI"


def test_telefono_es_riesgo_alto():
    resultado = analizar_texto("Llamame al 3624 456789")
    assert resultado.nivel_riesgo == "alto"
    assert resultado.tipo_dato_detectado == "Teléfono"


def test_telefono_con_guion_interno_es_riesgo_alto():
    resultado = analizar_texto("El teléfono de la oficina es 011 4444-5555")
    assert resultado.nivel_riesgo == "alto"
    assert resultado.tipo_dato_detectado == "Teléfono"


def test_email_es_riesgo_alto():
    resultado = analizar_texto("Mandale un mail a cliente@empresa.com")
    assert resultado.nivel_riesgo == "alto"
    assert resultado.tipo_dato_detectado == "Correo electrónico"


def test_nombre_propio_es_riesgo_medio_via_nlp():
    resultado = analizar_texto("Envié el presupuesto a Juan Perez")
    assert resultado.nivel_riesgo == "medio"
    assert resultado.tipo_dato_detectado in ("Nombre de persona", "Nombre de organización")


def test_codigo_con_termino_propietario_es_riesgo_alto():
    resultado = analizar_texto("def calcular(cliente): return cliente.total  # parte del sistema interno")
    assert resultado.nivel_riesgo == "alto"
    assert resultado.tipo_dato_detectado == "Código o información propietaria"


def test_codigo_generico_sin_termino_propietario_es_riesgo_bajo():
    resultado = analizar_texto("def ordenar_lista(numeros): return sorted(numeros)")
    assert resultado.nivel_riesgo == "bajo"


def test_reglas_regex_tienen_prioridad_sobre_nlp():
    # Un texto con un CUIT y también un nombre propio debe clasificarse
    # por la regla (más precisa) y no caer en la rama de NLP.
    resultado = analizar_texto("Juan Perez tiene CUIT 20-38456712-4")
    assert resultado.nivel_riesgo == "critico"
    assert resultado.tipo_dato_detectado == "CUIT/CUIL"
