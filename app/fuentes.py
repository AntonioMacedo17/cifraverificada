"""Fuentes oficiales de CifraVerificada: API del BCRP (en vivo, con snapshot de respaldo) y ENAHO 2024 agregada.

Las funciones `_fecha_api`, `_periodo` y `_pedir_api` vienen de mi Tarea 4 (Python_Intermedio_2026/tarea_4/mcp/
server.py, servidor MCP del BCRP basado en la Sesión 04), adaptadas: sin FastMCP, sin el catálogo de 7 MB (los
metadatos de las 6 series usadas están en SERIES) y sin caché en disco (la app usa st.cache_data).

Regenerar el snapshot (cuando se quiera actualizar el respaldo):
    uv run python -m app.fuentes
"""
import calendar
import json
import math
import re
import time
from datetime import datetime
from pathlib import Path
from zoneinfo import ZoneInfo

import httpx
import pandas as pd

RAIZ = Path(__file__).resolve().parents[1]
DATA = RAIZ / "data"
SNAPSHOT = DATA / "bcrp_snapshot.json"
ENAHO = DATA / "enaho2024_indicadores.csv"
GEOJSON = DATA / "peru_departamental_simple.geojson"

API = "https://estadisticas.bcrp.gob.pe/estadisticas/series/api"
WEB = "https://estadisticas.bcrp.gob.pe/estadisticas/series"
WEB_FRECUENCIA = {"diaria": "diarias", "mensual": "mensuales", "trimestral": "trimestrales", "anual": "anuales"}
URL_ENAHO = "https://proyectos.inei.gob.pe/microdatos/"

# Fechas siempre en hora de Lima: el servidor de la nube corre en UTC (a las 21:00 de Lima ya es el día siguiente).
LIMA = ZoneInfo("America/Lima")


def ahora_lima() -> datetime:
    return datetime.now(LIMA)


def hoy_lima() -> str:
    """Fecha de hoy en Lima, AAAA-MM-DD."""
    return ahora_lima().date().isoformat()


def fecha_consulta() -> str:
    """Fecha y hora de la consulta en Lima, p. ej. '2026-11-10 21:00 (hora de Lima)'."""
    return ahora_lima().strftime("%Y-%m-%d %H:%M") + " (hora de Lima)"
REINTENTOS = 3
ESPERA_BASE = 1.0
MESES = {"ene": 1, "feb": 2, "mar": 3, "abr": 4, "may": 5, "jun": 6, "jul": 7, "ago": 8,
         "sep": 9, "set": 9, "oct": 10, "nov": 11, "dic": 12}

# Metadatos tomados del catálogo oficial del BCRP (estadisticas/series/metadata). Ventana: desde -> hasta.
SERIES = {
    "PN01273PM": {"nombre": "Índice de precios Lima Metropolitana (var% 12 meses) - IPC", "frecuencia": "Mensual",
                  "unidad": "%", "fuente_primaria": "INEI", "desde": "2015-01", "hasta": "2025-12"},
    "PM04863AA": {"nombre": "Producto bruto interno (variación porcentual real anual)", "frecuencia": "Anual",
                  "unidad": "%", "fuente_primaria": "INEI, BCRP", "desde": "2000", "hasta": "2025"},
    "PN01728AM": {"nombre": "PBI (variación porcentual interanual, mensual)", "frecuencia": "Mensual",
                  "unidad": "%", "fuente_primaria": "INEI", "desde": "2015-01", "hasta": "2025-12"},
    "PN01210PM": {"nombre": "Tipo de cambio bancario promedio del periodo (S/ por US$)", "frecuencia": "Mensual",
                  "unidad": "S/ por US$", "fuente_primaria": "BCRP, SBS", "desde": "2015-01", "hasta": "2025-12"},
    "PD04722MM": {"nombre": "Tasa de referencia de la política monetaria", "frecuencia": "Mensual",
                  "unidad": "%", "fuente_primaria": "BCRP", "desde": "2015-01", "hasta": "2025-12"},
    "PM05876FA": {"nombre": "Ingresos tributarios del gobierno general (% del PBI)", "frecuencia": "Anual",
                  "unidad": "% del PBI", "fuente_primaria": "MEF, Sunat, BCRP", "desde": "2000", "hasta": "2025"},
}


class FuenteError(Exception):
    """La fuente no devolvió datos utilizables."""


# --------------------------------------------------------------------------------------------------------------
# Copiado de tarea_4/mcp/server.py (fechas y periodos del BCRP)
# --------------------------------------------------------------------------------------------------------------

def _fecha_api(fecha: str, frecuencia: str, fin: bool = False) -> str:
    """"2025", "2025-03" -> formato de la API según la frecuencia (de tarea_4, versión reducida)."""
    m = re.fullmatch(r"\s*(\d{4})(?:-(\d{1,2}))?\s*", str(fecha))
    if not m:
        raise FuenteError(f"Fecha {fecha!r} no válida.")
    anio, mes = int(m[1]), int(m[2]) if m[2] else (12 if fin else 1)
    f = frecuencia.lower()
    if f == "anual":
        return f"{anio}"
    if f == "mensual":
        return f"{anio}-{mes}"
    if f == "trimestral":
        return f"{anio}-{(mes - 1) // 3 + 1}"
    if f == "diaria":
        d = calendar.monthrange(anio, mes)[1] if fin else 1
        return f"{anio}-{mes:02d}-{d:02d}"
    raise FuenteError(f"Frecuencia {frecuencia!r} no soportada.")


def _periodo(nombre: str, frecuencia: str) -> str:
    """"Ene.2025" -> "2025-01"; "2025" -> "2025" (de tarea_4)."""
    f = frecuencia.lower()
    try:
        if f == "mensual":
            mes, anio = nombre.split(".")
            return f"{int(anio)}-{MESES[mes.lower()[:3]]:02d}"
        if f == "anual":
            return str(int(nombre))
    except (ValueError, KeyError):
        pass
    raise FuenteError(f"No pude interpretar el periodo {nombre!r} que devolvió el BCRP ({frecuencia}).")


def _pedir_api(url: str) -> dict:
    """GET a la API del BCRP con reintentos y espera creciente (de tarea_4, sin caché en disco)."""
    error = None
    for intento in range(REINTENTOS):
        try:
            r = httpx.get(url, timeout=20)
            r.raise_for_status()
            datos = r.json()              # la API responde text/html incluso con JSON
            if not isinstance(datos, dict) or "periods" not in datos:
                raise ValueError("respuesta sin 'periods'")
            return datos
        except (httpx.HTTPError, ValueError) as e:
            error = e
            if intento < REINTENTOS - 1:
                time.sleep(ESPERA_BASE * 2 ** intento)
    raise FuenteError(f"El BCRP no respondió tras {REINTENTOS} intentos ({type(error).__name__}).")


def url_api(codigo: str) -> str:
    s = SERIES[codigo]
    return f"{API}/{codigo}/json/{_fecha_api(s['desde'], s['frecuencia'])}/{_fecha_api(s['hasta'], s['frecuencia'], True)}"


def url_web(codigo: str) -> str:
    fr = SERIES[codigo]["frecuencia"].lower()
    return f"{WEB}/{WEB_FRECUENCIA.get(fr, 'mensuales')}/resultados/{codigo}/html"


def descargar_serie(codigo: str) -> list[dict]:
    """Datos [{periodo, valor}] de la serie en su ventana, en vivo desde la API del BCRP."""
    fr = SERIES[codigo]["frecuencia"]
    datos = []
    for p in _pedir_api(url_api(codigo)).get("periods", []):
        bruto = (p.get("values") or ["n.d."])[0]
        try:
            valor = float(bruto)
        except (TypeError, ValueError):   # "n.d.": sin dato
            continue
        if not math.isnan(valor):
            datos.append({"periodo": _periodo(p["name"], fr), "valor": round(valor, 6)})
    if not datos:
        raise FuenteError(f"La serie {codigo} no devolvió datos.")
    return datos


# --------------------------------------------------------------------------------------------------------------
# Serie con respaldo: API en vivo -> snapshot fechado
# --------------------------------------------------------------------------------------------------------------

def leer_snapshot() -> dict:
    return json.loads(SNAPSHOT.read_text(encoding="utf-8"))


def obtener_serie(codigo: str, en_vivo: bool = True) -> dict:
    """Devuelve {codigo, datos (pd.Series), origen, fecha_datos, url_api, url_web}.

    origen = "api" (consulta en vivo) o "snapshot" (respaldo guardado en data/, con su fecha).
    """
    aviso = None
    if en_vivo:
        try:
            datos, origen, fecha = descargar_serie(codigo), "API del BCRP en vivo", hoy_lima()
        except FuenteError as e:
            aviso = str(e)
            en_vivo = False
    if not en_vivo:
        snap = leer_snapshot()
        datos, origen, fecha = snap["series"][codigo], "snapshot guardado", snap["fecha_descarga"]
    s = pd.Series({d["periodo"]: d["valor"] for d in datos}, name=codigo).sort_index()
    return {"codigo": codigo, **SERIES[codigo], "datos": s, "origen": origen, "fecha_datos": fecha,
            "aviso": aviso, "url_api": url_api(codigo), "url_web": url_web(codigo)}


def leer_enaho() -> pd.DataFrame:
    df = pd.read_csv(ENAHO, dtype={"codigo": str})
    return df


def crear_snapshot() -> None:
    snap = {"fecha_descarga": hoy_lima(),
            "fuente": "API de series estadísticas del BCRP (estadisticas.bcrp.gob.pe)",
            "urls": {c: url_api(c) for c in SERIES}, "series": {}}
    for codigo in SERIES:
        snap["series"][codigo] = descargar_serie(codigo)
        print(f"{codigo}: {len(snap['series'][codigo])} datos, último {snap['series'][codigo][-1]}")
    SNAPSHOT.write_text(json.dumps(snap, ensure_ascii=False, indent=1), encoding="utf-8")


if __name__ == "__main__":
    crear_snapshot()
