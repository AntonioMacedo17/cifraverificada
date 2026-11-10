"""6 afirmaciones de prueba con veredicto esperado calculado desde los datos (snapshot del BCRP y ENAHO 2024).

Prueban el motor en Python a partir de la consulta estructurada (la que produciría Gemini), sin red ni LLM:
    uv run pytest -q
Datos de referencia: PN01273PM 2024-12 = 1.9663 %; PM05876FA 2025 = 14.81 % del PBI; pobreza nacional 2024
= 27.53 %; rural = 39.44 %; Cajamarca = 44.99 % (la más alta de 25 departamentos).
"""
import pytest

from app.verificador import APROXIMADA, CORRECTA, INCORRECTA, NO_VERIFICABLE, media_unidad, verificar

CASOS = [
    # (frase, consulta, veredicto esperado)
    ("La inflación de Lima cerró 2024 en 1.97 %",
     {"indicador": "inflacion", "ambito": "Lima Metropolitana", "periodo": "2024", "tipo": "valor",
      "valor_afirmado": 1.97, "unidad": "%"}, CORRECTA),
    ("Cajamarca es el departamento más pobre",
     {"indicador": "pobreza", "ambito": "Cajamarca", "periodo": None, "tipo": "maximo",
      "valor_afirmado": None, "unidad": None}, CORRECTA),
    ("La pobreza en el Perú llegó a 20 % en 2024",
     {"indicador": "pobreza", "ambito": "nacional", "periodo": "2024", "tipo": "valor",
      "valor_afirmado": 20, "unidad": "%"}, INCORRECTA),
    ("El Perú recauda impuestos por más del 20 % del PBI",
     {"indicador": "ingresos_tributarios", "ambito": "nacional", "periodo": None, "tipo": "mayor_que",
      "valor_afirmado": 20, "unidad": "% del PBI"}, INCORRECTA),
    ("La pobreza rural es de 40 %",
     {"indicador": "pobreza", "ambito": "rural", "periodo": None, "tipo": "valor",
      "valor_afirmado": 40, "unidad": "%"}, APROXIMADA),
    ("El desempleo en Lima es 7 %",
     {"indicador": "no_disponible", "ambito": "Lima", "periodo": None, "tipo": "valor",
      "valor_afirmado": 7, "unidad": "%"}, NO_VERIFICABLE),
]


@pytest.mark.parametrize("frase,consulta,esperado", CASOS, ids=[c[0] for c in CASOS])
def test_veredicto(frase, consulta, esperado):
    r = verificar(consulta, en_vivo=False)
    assert r["veredicto"] == esperado, r


def test_cifras_oficiales_vienen_de_los_datos():
    r = verificar(CASOS[0][1], en_vivo=False)
    assert r["oficial"] == pytest.approx(1.9663, abs=1e-4)
    assert r["fuente"]["codigo"] == "PN01273PM" and r["periodo_usado"] == "2024-12"
    assert verificar(CASOS[2][1], en_vivo=False)["oficial"] == pytest.approx(27.53)


def test_periodo_fuera_de_enaho_no_se_inventa():
    c = {**CASOS[2][1], "periodo": "2019"}
    assert verificar(c, en_vivo=False)["veredicto"] == NO_VERIFICABLE


def test_media_unidad():
    assert media_unidad(20) == 0.5 and media_unidad(1.97) == pytest.approx(0.005)
