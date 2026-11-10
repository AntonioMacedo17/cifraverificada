"""Gemini: (1) convierte la afirmación en una consulta estructurada y (2) redacta la explicación del veredicto.

Mismo modelo y librería que en mi Tarea 2 (google-genai, gemini-3.8-flash, temperature=0, JSON con esquema).
Gemini NO calcula ni aporta cifras: la comparación la hace app/verificador.py. La explicación se revisa en
Python: si menciona un número que no está en los datos calculados, se descarta y se usa una plantilla.

La clave se lee de st.secrets["GEMINI_API_KEY"] o de la variable de entorno GEMINI_API_KEY (.env en local).
Cada llamada registra sus tokens en data/registro_tokens.csv (ignorado por git).
"""
import csv
import enum
import json
import os
import re
import time
from datetime import datetime
from pathlib import Path

from dotenv import load_dotenv
from pydantic import BaseModel, Field

RAIZ = Path(__file__).resolve().parents[1]
MODELO = "gemini-3.8-flash"
REGISTRO = RAIZ / "data" / "registro_tokens.csv"


class Indicador(str, enum.Enum):
    inflacion = "inflacion"
    crecimiento_pbi = "crecimiento_pbi"
    tipo_cambio = "tipo_cambio"
    tasa_referencia = "tasa_referencia"
    ingresos_tributarios = "ingresos_tributarios"
    pobreza = "pobreza"
    pobreza_extrema = "pobreza_extrema"
    no_disponible = "no_disponible"


class Tipo(str, enum.Enum):
    valor = "valor"
    mayor_que = "mayor_que"
    menor_que = "menor_que"
    maximo = "maximo"
    minimo = "minimo"


class Consulta(BaseModel):
    indicador: Indicador
    ambito: str | None = Field(description="nacional, rural, urbana, hombre, mujer, 0-14, 15-29, 30-44, 45-59, "
                                           "60 y más, el nombre de un departamento, o Lima Metropolitana")
    periodo: str | None = Field(description="AAAA o AAAA-MM; null si la frase no menciona periodo")
    tipo: Tipo
    valor_afirmado: float | None = Field(description="la cifra tal como aparece en la frase; null si no hay")
    unidad: str | None


PROMPT = """Eres el intérprete de un verificador de cifras del Perú. Convierte la afirmación en una consulta.
NO verifiques ni corrijas la cifra: solo extrae lo que la frase dice.

Indicadores disponibles (usa exactamente estas claves):
- inflacion: inflación / variación del IPC de Lima Metropolitana (BCRP PN01273PM).
- crecimiento_pbi: crecimiento de la economía / del PBI real (BCRP PM04863AA anual, PN01728AM mensual).
- tipo_cambio: precio del dólar en soles (BCRP PN01210PM).
- tasa_referencia: tasa de interés de referencia del BCRP (PD04722MM).
- ingresos_tributarios: recaudación tributaria / impuestos como % del PBI (BCRP PM05876FA).
- pobreza: pobreza monetaria, % de personas (INEI ENAHO 2024; nacional, rural/urbana, sexo, edad, departamento).
- pobreza_extrema: pobreza extrema monetaria (INEI ENAHO 2024, mismos ámbitos).
- no_disponible: cualquier otro tema (desempleo, anemia, delincuencia, salarios, etc.) o frase sin cifra verificable.

tipo: "valor" si afirma una cifra; "mayor_que" si dice "más de", "supera", "por encima de"; "menor_que" si dice
"menos de", "por debajo de"; "maximo" si dice que un departamento es el más alto/más pobre; "minimo" si dice que
es el más bajo/menos pobre (en ese caso ambito = el departamento y valor_afirmado = null).
ambito: para pobreza usa nacional (Perú), rural, urbana, hombre, mujer, 0-14 (niñez), 15-29, 30-44, 45-59,
60 y más, o el nombre del departamento. Si no se menciona, "nacional".
periodo: "AAAA" o "AAAA-MM" solo si la frase lo menciona; si no, null.
valor_afirmado: el número tal cual (20 % -> 20; 1.97 % -> 1.97; S/ 3.75 -> 3.75).

Afirmación: «{frase}»"""

PROMPT_EXPLICACION = """Redacta en español, en 2 o 3 oraciones claras para un periodista, por qué la afirmación
recibió este veredicto. Usa SOLO las cifras que aparecen en los datos (con el mismo redondeo); no agregues cifras,
fechas ni causas nuevas; no digas que algo "causa" o "explica" otra cosa. Menciona la fuente y el periodo.

Afirmación: «{frase}»
Datos calculados por el verificador (JSON): {datos}"""


def _clave() -> str | None:
    try:
        import streamlit as st
        if "GEMINI_API_KEY" in st.secrets:
            return st.secrets["GEMINI_API_KEY"]
    except Exception:
        pass
    load_dotenv(RAIZ / ".env")
    return os.environ.get("GEMINI_API_KEY")


def _cliente():
    from google import genai
    clave = _clave()
    if not clave:
        raise RuntimeError("Falta GEMINI_API_KEY (en .env o en los secrets de Streamlit).")
    return genai.Client(api_key=clave)


def _registrar(etapa: str, frase: str, uso: dict) -> None:
    try:
        nuevo = not REGISTRO.exists()
        with REGISTRO.open("a", newline="", encoding="utf-8") as f:
            w = csv.writer(f)
            if nuevo:
                w.writerow(["fecha", "etapa", "modelo", "tokens_entrada", "tokens_salida", "tokens_total", "frase"])
            w.writerow([datetime.now().isoformat(timespec="seconds"), etapa, MODELO, uso["entrada"],
                        uso["salida"], uso["total"], frase[:200]])
    except OSError:
        pass          # en la nube el disco puede ser de solo lectura: el registro no debe romper la app


def _llamar(prompt: str, esquema=None, intentos: int = 3):
    from google.genai import errors, types
    cfg = types.GenerateContentConfig(temperature=0, **(
        {"response_mime_type": "application/json", "response_schema": esquema} if esquema else {}))
    cliente = _cliente()
    for i in range(intentos):
        try:
            r = cliente.models.generate_content(model=MODELO, contents=prompt, config=cfg)
            u = r.usage_metadata
            uso = {"entrada": u.prompt_token_count or 0, "salida": u.candidates_token_count or 0,
                   "total": u.total_token_count or 0}
            return r, uso
        except (errors.ServerError, errors.ClientError) as e:
            if getattr(e, "code", None) not in (429, 503) or i == intentos - 1:
                raise
            time.sleep(3 * 2 ** i)


def interpretar(frase: str) -> tuple[dict, dict]:
    """Frase -> (consulta dict, tokens usados)."""
    r, uso = _llamar(PROMPT.format(frase=frase), Consulta)
    _registrar("interpretar", frase, uso)
    c = Consulta.model_validate_json(r.text).model_dump(mode="json")
    return c, uso


def _numeros(texto: str) -> set[float]:
    return {float(x.replace(",", ".")) for x in re.findall(r"\d+(?:[.,]\d+)?", texto)}


def explicar(frase: str, datos: dict, plantilla: str) -> tuple[str, dict, bool]:
    """Explicación redactada por Gemini; si trae una cifra que no está en `datos`, se usa la plantilla.

    Devuelve (texto, tokens, es_de_gemini).
    """
    try:
        r, uso = _llamar(PROMPT_EXPLICACION.format(frase=frase, datos=json.dumps(datos, ensure_ascii=False)))
    except Exception:
        return plantilla, {"entrada": 0, "salida": 0, "total": 0}, False
    _registrar("explicar", frase, uso)
    texto = (r.text or "").strip()
    permitidos = _numeros(json.dumps(datos, ensure_ascii=False)) | _numeros(frase)
    permitidos |= {round(x, d) for x in list(permitidos) for d in (0, 1, 2)}
    if not texto or any(n not in permitidos for n in _numeros(texto)):
        return plantilla, uso, False
    return texto, uso, True
