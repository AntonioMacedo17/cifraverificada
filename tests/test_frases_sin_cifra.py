"""Frases sin cifra explícita: negaciones / cifras implícitas y temas sin indicador (orientación con lista fija)."""
import json

import httpx
import pydantic
import pytest
from google import genai
from google.genai import types

import ai.interpretar as ia
from ai.reglas import interpretar_reglas
from app import orientacion
from app.verificador import CORRECTA, INCORRECTA, NO_VERIFICABLE, verificar

# ---------------------------------------------------------------- 1. cifras implícitas (reglas en Python)

IMPLICITAS = [  # frase -> (tipo, valor afirmado implícito, veredicto con ENAHO 2024: pobreza nacional 27.53 %)
    ("No existe pobreza en el Perú", "valor", 0, INCORRECTA),
    ("Ya no hay pobres", "valor", 0, INCORRECTA),
    ("La pobreza desapareció", "valor", 0, INCORRECTA),
    ("Este gobierno erradicó la pobreza", "valor", 0, INCORRECTA),
    ("Ya no hay pobreza extrema en Puno", "valor", 0, INCORRECTA),
    ("La mayoría de peruanos es pobre", "mayor_que", 50, INCORRECTA),
    ("Más de la mitad de los peruanos es pobre", "mayor_que", 50, INCORRECTA),
    ("Menos de la mitad de los peruanos es pobre", "menor_que", 50, CORRECTA),
]


@pytest.mark.parametrize("frase,tipo,valor,veredicto", IMPLICITAS, ids=[x[0] for x in IMPLICITAS])
def test_cifra_implicita_con_reglas(frase, tipo, valor, veredicto):
    c = interpretar_reglas(frase)
    assert c is not None and c["tipo"] == tipo and c["valor_afirmado"] == valor and c["unidad"] == "%"
    assert c["cifra_implicita"]                          # queda registrada la expresión de la frase
    r = verificar(c, en_vivo=False)
    assert r["veredicto"] == veredicto
    assert r["oficial"] > 0                              # el dato oficial sale de la ENAHO, no de la frase


def test_no_existe_pobreza_usa_ambito_y_dato_oficial():
    r = verificar(interpretar_reglas("Ya no hay pobreza extrema en Puno"), en_vivo=False)
    assert r["ambito_usado"] == "Puno" and r["indicador"].startswith("Pobreza monetaria extrema")
    assert r["diferencia"] == pytest.approx(-r["oficial"])


@pytest.mark.parametrize("frase", ["La pobreza es alta", "La pobreza bajó mucho"])
def test_sin_cifra_ni_implicita_no_inventa(frase):
    assert interpretar_reglas(frase) is None


def test_cifra_escrita_tiene_prioridad():
    c = interpretar_reglas("No es cierto que la pobreza llegue al 20 %")
    assert c["valor_afirmado"] == 20 and c["cifra_implicita"] is None

# ---------------------------------------------------------------- 2. temas sin indicador -> orientación


TEMAS = [("El Perú es una democracia plena", "democracia"),
         ("La corrupción le cuesta al país 20 mil millones al año", "corrupcion"),
         ("La educación pública en el Perú es la peor de la región", "educacion"),
         ("La anemia infantil bajó a la mitad", "salud"),
         ("El desempleo en Lima es 7 %", "empleo"),
         ("La delincuencia se duplicó", "seguridad")]


@pytest.mark.parametrize("frase,tema", TEMAS, ids=[t[0] for t in TEMAS])
def test_tema_sin_indicador_con_reglas(frase, tema):
    c = interpretar_reglas(frase)
    assert c["indicador"] == "no_disponible" and c["tema_orientacion"] == tema
    r = verificar(c, en_vivo=False)
    assert r["veredicto"] == NO_VERIFICABLE
    o = orientacion.enlaces_para(c["tema_orientacion"])
    assert 2 <= len(o["enlaces"]) <= 4 and o["texto"].startswith("Esta afirmación no se puede verificar")


def test_enlaces_solo_de_la_lista_fija_y_onu_primero():
    d = json.loads(orientacion.ARCHIVO.read_text(encoding="utf-8"))
    urls = {e["url"] for e in d["enlaces"].values()}
    for clave, tema in d["temas"].items():
        assert all(i in d["enlaces"] for i in tema["enlaces"]), clave
        o = orientacion.enlaces_para(clave)
        assert 2 <= len(o["enlaces"]) <= 4
        assert o["enlaces"][0]["sistema"] == "ONU", clave        # prioridad al sistema de la ONU
        sistemas = [e["sistema"] for e in o["enlaces"]]
        assert sistemas == sorted(sistemas, key=lambda s: s != "ONU")
        assert all(e["url"] in urls and e["url"].startswith("https://") for e in o["enlaces"])
    instituciones = {e["institucion"] for e in d["enlaces"].values()}
    assert {"CEPAL", "PNUD", "INEI", "BCRP", "MEF"} <= instituciones


def test_tema_desconocido_o_nulo_usa_general():
    assert orientacion.enlaces_para(None)["tema"] == "general"
    assert orientacion.enlaces_para("tema-inventado")["tema"] == "general"


def test_gemini_solo_puede_elegir_temas_de_la_lista():
    base = {"indicador": "no_disponible", "ambito": None, "periodo": None, "tipo": "valor",
            "valor_afirmado": None, "unidad": None}
    assert ia.Consulta.model_validate({**base, "tema_orientacion": "democracia"})
    with pytest.raises(pydantic.ValidationError):
        ia.Consulta.model_validate({**base, "tema_orientacion": "https://sitio-inventado.org"})
    assert {t.value for t in ia.Tema} == set(orientacion.temas())

# ---------------------------------------------------------------- 3. camino con Gemini (transporte simulado)


def _gemini_responde(monkeypatch, consulta: dict):
    respuesta = {"candidates": [{"content": {"role": "model", "parts": [{"text": json.dumps(consulta)}]},
                                 "finishReason": "STOP"}],
                 "usageMetadata": {"promptTokenCount": 1, "candidatesTokenCount": 1, "totalTokenCount": 2}}
    prompts = []

    def manejar(req):
        prompts.append(req.content.decode("utf-8"))
        return httpx.Response(200, json=respuesta)
    monkeypatch.setattr(ia, "_cliente", lambda t=15: genai.Client(api_key="clave-de-prueba", http_options=types.HttpOptions(
        timeout=10_000, client_args={"transport": httpx.MockTransport(manejar)})))
    monkeypatch.setattr(ia, "_registrar", lambda *a, **k: None)
    return prompts


def test_gemini_cifra_implicita(monkeypatch):
    prompts = _gemini_responde(monkeypatch, {
        "indicador": "pobreza", "ambito": "nacional", "periodo": None, "tipo": "valor", "valor_afirmado": 0,
        "unidad": "%", "cifra_implicita": "no existe pobreza", "tema_orientacion": "general"})
    c, uso = ia.interpretar_con_respaldo("No existe pobreza en el Perú")
    assert uso["con_ia"] and c["valor_afirmado"] == 0 and c["tema_orientacion"] is None
    assert verificar(c, en_vivo=False)["veredicto"] == INCORRECTA
    assert "ya no hay pobres" in prompts[0] and "democracia" in prompts[0]   # el prompt lista los temas


def test_gemini_tema_sin_indicador(monkeypatch):
    _gemini_responde(monkeypatch, {
        "indicador": "no_disponible", "ambito": None, "periodo": None, "tipo": "valor", "valor_afirmado": None,
        "unidad": None, "cifra_implicita": None, "tema_orientacion": "corrupcion"})
    c, _ = ia.interpretar_con_respaldo("El Perú es el país más corrupto de la región")
    assert verificar(c, en_vivo=False)["veredicto"] == NO_VERIFICABLE
    assert orientacion.enlaces_para(c["tema_orientacion"])["enlaces"][0]["institucion"] == "UNODC"
