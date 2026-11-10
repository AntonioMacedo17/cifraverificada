"""Ajustes de despliegue: motivo del respaldo sin IA (sin mostrar la clave) y unidades de "la cifra detrás"."""
import pytest
from google.genai import errors

import ai.interpretar as ia
from app.verificador import verificar


def _api(cls, code, msg="detalle"):
    return cls(code, {"error": {"code": code, "message": msg, "status": "X"}})


@pytest.mark.parametrize("exc,esperado", [
    (_api(errors.ServerError, 503), "Gemini saturado (503)"),
    (_api(errors.ClientError, 429), "cuota agotada (429)"),
    (RuntimeError("Falta GEMINI_API_KEY (en .env o en los secrets de Streamlit)."),
     "falta la clave GEMINI_API_KEY en Secrets"),
])
def test_motivos_conocidos(exc, esperado):
    assert ia.motivo_respaldo(exc) == esperado


def test_motivo_tiempo_agotado_con_causa():
    try:
        try:
            raise _api(errors.ServerError, 503)
        except errors.ServerError as e:
            raise TimeoutError("Gemini no respondió en 15 s") from e
    except TimeoutError as t:
        m = ia.motivo_respaldo(t)
    assert m.startswith("tiempo agotado (15 s)") and "503" in m


def test_motivo_otros_errores_con_tipo_y_sin_clave(monkeypatch):
    clave = "AIzaSyFALSA_de_prueba_1234567890abcdef"
    monkeypatch.setattr(ia, "_clave", lambda: clave)
    m = ia.motivo_respaldo(_api(errors.ClientError, 400, f"API key not valid: {clave}"))
    assert "400" in m and "ClientError" in m and clave not in m
    assert ia.motivo_respaldo(_api(errors.ClientError, 404)).startswith("modelo no encontrado (404")
    assert ia.motivo_respaldo(ValueError("x")) == "ValueError: x"


def test_respaldo_expone_motivo(monkeypatch):
    def falla(frase):
        raise _api(errors.ClientError, 429)
    monkeypatch.setattr(ia, "interpretar", falla)
    c, uso = ia.interpretar_con_respaldo("La inflación de Lima cerró 2024 en 1.97 %")
    assert not uso["con_ia"] and uso["motivo_respaldo"] == "cuota agotada (429)"


def test_cifra_detras_con_unidad_y_dos_decimales():
    r = verificar({"indicador": "pobreza", "ambito": "nacional", "periodo": "2024", "tipo": "valor",
                   "valor_afirmado": 20, "unidad": "%"}, en_vivo=False)
    filas = {d["concepto"]: d for d in r["detras"]}
    assert filas["Brecha rural - urbana"]["unidad"] == "pp"
    assert filas["Nacional (Perú)"]["unidad"] == "%"
    assert all(round(d["valor"], 2) == d["valor"] for d in r["detras"])
    r2 = verificar({"indicador": "tipo_cambio", "periodo": "2024", "tipo": "valor", "valor_afirmado": 3.75,
                    "unidad": "S/ por US$"}, en_vivo=False)
    assert all(d["unidad"] == "S/ por US$" for d in r2["detras"])
