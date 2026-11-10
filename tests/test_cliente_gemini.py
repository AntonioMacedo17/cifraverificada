"""El cliente de google-genai debe seguir abierto durante toda la llamada (bug de la nube con Python 3.14).

`genai.Client.__del__` cierra el cliente HTTP que comparte con `.models`. Con un cliente temporal
(`_cliente(...).models.generate_content(...)`) el Client se recolectaba antes de la petición y la nube mostraba
"RuntimeError: Cannot send a request, as the client has been closed." Esta prueba usa un genai.Client real con un
transporte httpx simulado: sin red y sin clave real.
"""
import gc
import json

import httpx
from google import genai
from google.genai import types

import ai.interpretar as ia

RESPUESTA = {
    "candidates": [{"content": {"role": "model", "parts": [{"text": json.dumps({
        "indicador": "pobreza", "ambito": "nacional", "periodo": "2024", "tipo": "valor",
        "valor_afirmado": 20, "unidad": "%"})}]}, "finishReason": "STOP"}],
    "usageMetadata": {"promptTokenCount": 10, "candidatesTokenCount": 5, "totalTokenCount": 15},
}


def _cliente_simulado(peticiones: list):
    def manejar(req: httpx.Request) -> httpx.Response:
        peticiones.append(req)
        return httpx.Response(200, json=RESPUESTA)

    def fabrica(timeout_s: float = 15):
        gc.collect()          # fuerza la recolección de cualquier cliente temporal anterior
        return genai.Client(api_key="clave-de-prueba", http_options=types.HttpOptions(
            timeout=int(timeout_s * 1000), client_args={"transport": httpx.MockTransport(manejar)}))
    return fabrica


def test_llamar_no_usa_un_cliente_cerrado(monkeypatch):
    peticiones = []
    monkeypatch.setattr(ia, "_cliente", _cliente_simulado(peticiones))
    monkeypatch.setattr(ia, "_registrar", lambda *a, **k: None)
    r, uso = ia._llamar("hola", ia.Consulta)
    assert len(peticiones) == 1 and uso["modelo"] == ia.MODELO and uso["total"] == 15
    assert ia.Consulta.model_validate_json(r.text).indicador == ia.Indicador.pobreza


def test_interpretar_con_respaldo_usa_gemini(monkeypatch):
    monkeypatch.setattr(ia, "_cliente", _cliente_simulado([]))
    monkeypatch.setattr(ia, "_registrar", lambda *a, **k: None)
    c, uso = ia.interpretar_con_respaldo("La pobreza en el Perú llegó a 20 % en 2024")
    assert uso["con_ia"], uso.get("motivo_respaldo")
    assert c["indicador"] == "pobreza" and c["valor_afirmado"] == 20


def test_principal_saturado_pasa_al_respaldo_con_plazo_minimo(monkeypatch):
    plazos, modelos = [], []

    def manejar(req: httpx.Request) -> httpx.Response:
        modelos.append(req.url.path)
        if ia.MODELO in req.url.path:
            return httpx.Response(503, json={"error": {"code": 503, "message": "high demand",
                                                       "status": "UNAVAILABLE"}})
        return httpx.Response(200, json=RESPUESTA)

    def fabrica(timeout_s: float = 15):
        plazos.append(timeout_s)
        return genai.Client(api_key="clave-de-prueba", http_options=types.HttpOptions(
            timeout=int(timeout_s * 1000), client_args={"transport": httpx.MockTransport(manejar)}))

    monkeypatch.setattr(ia, "_cliente", fabrica)
    _, uso = ia._llamar("hola", ia.Consulta)
    assert uso["modelo"] == ia.MODELO_RESPALDO
    assert len(modelos) == 2 and all(p >= ia.PLAZO_MIN_S for p in plazos)
