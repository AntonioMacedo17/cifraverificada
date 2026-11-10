"""Modo de respaldo sin IA: reglas en Python (ai/reglas.py) y cambio automático cuando Gemini falla."""
import pytest

import ai.interpretar as ia
from ai.reglas import interpretar_reglas
from app.verificador import APROXIMADA, CORRECTA, INCORRECTA, verificar

EJEMPLOS = [  # las 5 frases de ejemplo de la app -> veredicto esperado (desde los datos)
    ("La pobreza en el Perú llegó a 20 % en 2024", INCORRECTA),
    ("La inflación de Lima cerró 2024 en 1.97 %", CORRECTA),
    ("Cajamarca es el departamento más pobre", CORRECTA),
    ("El Perú recauda impuestos por más del 20 % del PBI", INCORRECTA),
    ("La pobreza rural es de 40 %", APROXIMADA),
]


@pytest.mark.parametrize("frase,esperado", EJEMPLOS, ids=[e[0] for e in EJEMPLOS])
def test_ejemplos_con_reglas(frase, esperado):
    c = interpretar_reglas(frase)
    assert c is not None
    assert verificar(c, en_vivo=False)["veredicto"] == esperado


@pytest.mark.parametrize("frase,campos", [
    ("La pobreza extrema en Puno es 12.6 %", {"indicador": "pobreza_extrema", "ambito": "Puno", "valor_afirmado": 12.6}),
    ("El tipo de cambio promedió 3,75 soles en 2024", {"indicador": "tipo_cambio", "periodo": "2024", "valor_afirmado": 3.75}),
    ("La tasa de referencia estaba en 5 % en diciembre de 2024", {"indicador": "tasa_referencia", "periodo": "2024-12"}),
    ("El PBI creció 3.3 % en 2024", {"indicador": "crecimiento_pbi", "periodo": "2024", "valor_afirmado": 3.3}),
    ("Ica es el departamento menos pobre", {"indicador": "pobreza", "ambito": "Ica", "tipo": "minimo"}),
    ("La pobreza infantil supera el 35 %", {"ambito": "0-14", "tipo": "mayor_que", "valor_afirmado": 35}),
])
def test_patrones(frase, campos):
    c = interpretar_reglas(frase)
    assert c is not None and {k: c[k] for k in campos} == campos


@pytest.mark.parametrize("frase", ["El desempleo en Lima es 7 %", "La anemia infantil bajó"])
def test_tema_sin_indicador_no_inventa(frase):
    c = interpretar_reglas(frase)          # tema sin indicador: solo se elige el tema de orientación
    assert c["indicador"] == "no_disponible" and c["valor_afirmado"] is None and c["tema_orientacion"]


@pytest.mark.parametrize("frase", ["La pobreza es alta", "Hoy hace calor"])
def test_no_reconoce_no_inventa(frase):
    assert interpretar_reglas(frase) is None


def test_respaldo_si_gemini_falla(monkeypatch):
    def falla(frase):
        raise TimeoutError("Gemini no respondió en 15 s")
    monkeypatch.setattr(ia, "interpretar", falla)
    c, uso = ia.interpretar_con_respaldo("La pobreza rural es de 40 %")
    assert uso["interpretacion"] == "reglas en Python (sin IA)" and not uso["con_ia"]
    assert c["indicador"] == "pobreza" and c["ambito"] == "rural"


def test_gemini_si_responde(monkeypatch):
    monkeypatch.setattr(ia, "interpretar", lambda f: ({"indicador": "pobreza"}, {"modelo": ia.MODELO, "total": 900}))
    _, uso = ia.interpretar_con_respaldo("x")
    assert uso["interpretacion"] == f"Gemini (modelo {ia.MODELO})" and uso["con_ia"]
