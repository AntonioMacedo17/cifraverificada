"""Motor de verificación: recibe una consulta estructurada y calcula el veredicto. Todo en Python, sin LLM.

Veredictos: CORRECTA / APROXIMADA / INCORRECTA / NO VERIFICABLE CON ESTAS FUENTES.

Tolerancia explícita (para el tipo "valor"; diferencia = afirmado - oficial):
- CORRECTA   si |diferencia| <= max(tol_exacta, media unidad del último decimal afirmado)
             (decir "20 %" acepta 19.5-20.5; decir "1.97 %" acepta ±0.1 pp).
- APROXIMADA si |diferencia| <= max(tol_aprox, rel_aprox × |oficial|).
- INCORRECTA en otro caso.
Para "mayor_que"/"menor_que" ("más del 20 %") se compara el dato oficial con el umbral; para "maximo"/"minimo"
("el departamento más pobre") se ordena el indicador entre los 25 departamentos.
"""
from datetime import date

import pandas as pd

from app import fuentes

CORRECTA, APROXIMADA, INCORRECTA, NO_VERIFICABLE = (
    "CORRECTA", "APROXIMADA", "INCORRECTA", "NO VERIFICABLE CON ESTAS FUENTES")

TOLERANCIAS = {  # por unidad
    "pp": {"tol_exacta": 0.1, "tol_aprox": 0.5, "rel_aprox": 0.10, "texto": "puntos porcentuales"},
    "S/": {"tol_exacta": 0.01, "tol_aprox": 0.05, "rel_aprox": 0.02, "texto": "soles por dólar"},
}

# Indicadores verificables. regla_anual: qué dato se toma si la afirmación da solo un año.
INDICADORES = {
    "inflacion": {"etiqueta": "Inflación de Lima Metropolitana (IPC, var. % 12 meses)", "codigo": "PN01273PM",
                  "regla_anual": "diciembre", "tol": "pp"},
    "crecimiento_pbi": {"etiqueta": "Crecimiento del PBI real (var. % anual)", "codigo": "PM04863AA",
                        "codigo_mensual": "PN01728AM", "regla_anual": "anual", "tol": "pp"},
    "tipo_cambio": {"etiqueta": "Tipo de cambio bancario (S/ por US$)", "codigo": "PN01210PM",
                    "regla_anual": "promedio", "tol": "S/"},
    "tasa_referencia": {"etiqueta": "Tasa de referencia del BCRP (%)", "codigo": "PD04722MM",
                        "regla_anual": "diciembre", "tol": "pp"},
    "ingresos_tributarios": {"etiqueta": "Ingresos tributarios del gobierno general (% del PBI)",
                             "codigo": "PM05876FA", "regla_anual": "anual", "tol": "pp"},
    "pobreza": {"etiqueta": "Pobreza monetaria (% de la población)", "columna": "pobreza_pct", "tol": "pp"},
    "pobreza_extrema": {"etiqueta": "Pobreza monetaria extrema (% de la población)",
                        "columna": "pobreza_extrema_pct", "tol": "pp"},
}
METODO_ENAHO = ("ENAHO 2024 (INEI), módulos 02 y 34; personas ponderadas con facpob07. Pobreza nacional "
                "calculada 27.53 % frente al oficial del INEI 27.6 % (diferencia de método, ±0.1 pp).")

SINONIMOS_AMBITO = {"peru": "Perú", "nacional": "Perú", "pais": "Perú", "total": "Perú",
                    "rural": "rural", "urbana": "urbana", "urbano": "urbana", "hombres": "hombre",
                    "hombre": "hombre", "mujeres": "mujer", "mujer": "mujer", "ninos": "0-14", "ninez": "0-14",
                    "0-14": "0-14", "15-29": "15-29", "30-44": "30-44", "45-59": "45-59",
                    "60 y mas": "60 y más", "adultos mayores": "60 y más"}


def _norm(s) -> str:
    import unicodedata
    return unicodedata.normalize("NFD", str(s).lower().strip()).encode("ascii", "ignore").decode()


def media_unidad(valor: float) -> float:
    """Media unidad del último decimal con que se escribió la cifra: 20 -> 0.5; 1.97 -> 0.005."""
    texto = f"{valor:.6f}".rstrip("0").rstrip(".")
    dec = len(texto.split(".")[1]) if "." in texto else 0
    return 0.5 * 10 ** -dec


def clasificar(afirmado: float, oficial: float, tol: str) -> tuple[str, dict]:
    t = TOLERANCIAS[tol]
    dif = afirmado - oficial
    exacta = max(t["tol_exacta"], media_unidad(afirmado))
    aprox = max(t["tol_aprox"], t["rel_aprox"] * abs(oficial))
    veredicto = CORRECTA if abs(dif) <= exacta + 1e-9 else APROXIMADA if abs(dif) <= aprox + 1e-9 else INCORRECTA
    desc = (f"CORRECTA si |diferencia| ≤ {exacta:g} {t['texto']}; APROXIMADA si ≤ {aprox:.2f} "
            f"(máx. de {t['tol_aprox']:g} y {t['rel_aprox']:.0%} del dato oficial); si no, INCORRECTA.")
    return veredicto, {"diferencia": round(dif, 4), "tolerancia": desc}


def _no_verificable(consulta: dict, motivo: str) -> dict:
    return {"veredicto": NO_VERIFICABLE, "motivo": motivo, "consulta": consulta,
            "fecha_consulta": date.today().isoformat()}


# --------------------------------------------------------------------------------------------------------------

def verificar(consulta: dict, en_vivo: bool = True) -> dict:
    """consulta: {indicador, ambito, periodo, tipo, valor_afirmado, unidad} (lo produce ai/interpretar.py)."""
    ind = consulta.get("indicador")
    if ind not in INDICADORES:
        return _no_verificable(consulta, "La afirmación no corresponde a ninguno de los indicadores disponibles "
                                         "(inflación, PBI, tipo de cambio, tasa de referencia, ingresos tributarios, "
                                         "pobreza y pobreza extrema).")
    if "codigo" in INDICADORES[ind]:
        return _verificar_bcrp(consulta, en_vivo)
    return _verificar_enaho(consulta)


def _verificar_bcrp(consulta: dict, en_vivo: bool) -> dict:
    meta = INDICADORES[consulta["indicador"]]
    periodo = (consulta.get("periodo") or "").strip()
    codigo = meta["codigo"]
    if consulta["indicador"] == "crecimiento_pbi" and len(periodo) == 7:   # "2024-05": serie mensual
        codigo = meta["codigo_mensual"]
    serie = fuentes.obtener_serie(codigo, en_vivo)
    s = serie["datos"]
    mensual = serie["frecuencia"] == "Mensual"

    # elegir el dato oficial según el periodo pedido
    if not periodo:
        per_usado = s.index[-1]
        metodo = f"Sin periodo en la afirmación: se usa el último dato disponible ({per_usado})."
        oficial = float(s.iloc[-1])
    elif len(periodo) == 4 and mensual:
        sub = s[s.index.str.startswith(periodo)]
        if sub.empty:
            return _no_verificable(consulta, f"La serie {codigo} no tiene datos para {periodo}.")
        if meta["regla_anual"] == "promedio":
            oficial, per_usado = float(sub.mean()), periodo
            metodo = f"Promedio de los {len(sub)} meses de {periodo}."
        else:
            if f"{periodo}-12" not in sub.index:
                return _no_verificable(consulta, f"Aún no hay dato de diciembre de {periodo} en {codigo}.")
            oficial, per_usado = float(sub[f"{periodo}-12"]), f"{periodo}-12"
            metodo = f"Dato de diciembre de {periodo} (cierre del año)."
    else:
        clave = periodo[:4] if not mensual else periodo
        if clave not in s.index:
            return _no_verificable(consulta, f"La serie {codigo} no tiene dato para {periodo} "
                                             f"(hay de {s.index[0]} a {s.index[-1]}).")
        oficial, per_usado = float(s[clave]), clave
        metodo = f"Dato del periodo {clave}."

    res = {"indicador": meta["etiqueta"], "consulta": consulta, "oficial": round(oficial, 4),
           "periodo_usado": per_usado, "unidad": serie["unidad"], "metodo": metodo,
           "fuente": {"tipo": "BCRP", "codigo": codigo, "nombre": serie["nombre"], "origen": serie["origen"],
                      "fecha_datos": serie["fecha_datos"], "aviso": serie["aviso"], "url": serie["url_web"],
                      "url_api": serie["url_api"], "fuente_primaria": serie["fuente_primaria"]},
           "serie": s, "fecha_consulta": date.today().isoformat()}
    res.update(_comparar(consulta, oficial, meta["tol"]))
    res["detras"] = _detras_bcrp(consulta["indicador"], s, per_usado, oficial, serie["unidad"])
    return res


def _comparar(consulta: dict, oficial: float, tol: str) -> dict:
    tipo, af = consulta.get("tipo") or "valor", consulta.get("valor_afirmado")
    if af is None:
        return {"veredicto": NO_VERIFICABLE, "motivo": "La afirmación no da una cifra concreta que comparar.",
                "diferencia": None, "tolerancia": "—"}
    if tipo == "mayor_que":
        v = CORRECTA if oficial > af else INCORRECTA
        return {"veredicto": v, "diferencia": round(oficial - af, 4),
                "tolerancia": f"Umbral: se afirma que el dato supera {af:g}; se compara el dato oficial con el umbral."}
    if tipo == "menor_que":
        v = CORRECTA if oficial < af else INCORRECTA
        return {"veredicto": v, "diferencia": round(oficial - af, 4),
                "tolerancia": f"Umbral: se afirma que el dato es menor que {af:g}; se compara el dato oficial con el umbral."}
    v, extra = clasificar(af, oficial, tol)
    return {"veredicto": v, **extra}


def _detras_bcrp(ind: str, s: pd.Series, per: str, oficial: float, unidad: str) -> list[dict]:
    """La cifra detrás de la cifra para series del BCRP: el dato frente al máximo, el mínimo y el promedio."""
    filas = [{"concepto": f"Dato oficial ({per})", "valor": round(oficial, 2)}]
    if ind == "inflacion":
        pico = s["2022":"2023"]                     # el episodio inflacionario reciente
        filas.append({"concepto": f"Pico 2022-2023 ({pico.idxmax()})", "valor": round(float(pico.max()), 2)})
    filas += [{"concepto": f"Máximo de la ventana ({s.idxmax()})", "valor": round(float(s.max()), 2)},
              {"concepto": f"Mínimo de la ventana ({s.idxmin()})", "valor": round(float(s.min()), 2)},
              {"concepto": f"Promedio {s.index[0]} a {s.index[-1]}", "valor": round(float(s.mean()), 2)},
              {"concepto": f"Último dato disponible ({s.index[-1]})", "valor": round(float(s.iloc[-1]), 2)}]
    return filas


def _buscar_fila(df: pd.DataFrame, ambito: str | None) -> pd.Series | None:
    a = _norm(ambito or "nacional")
    a = SINONIMOS_AMBITO.get(a, a)
    for _, f in df.iterrows():
        if _norm(f.categoria) == _norm(a):
            return f
    for _, f in df.iterrows():       # "departamento de Cajamarca", "región Puno"
        if f.nivel == "departamento" and _norm(f.categoria) in a:
            return f
    return None


def _verificar_enaho(consulta: dict) -> dict:
    meta = INDICADORES[consulta["indicador"]]
    col = meta["columna"]
    periodo = (consulta.get("periodo") or "2024").strip()
    if periodo[:4] != "2024":
        return _no_verificable(consulta, f"Solo hay pobreza de la ENAHO 2024; la afirmación habla de {periodo}.")
    df = fuentes.leer_enaho()
    deps = df[df.nivel == "departamento"].sort_values(col, ascending=False)
    fuente = {"tipo": "ENAHO", "codigo": "ENAHO 2024 (INEI), agregados ponderados con facpob07",
              "nombre": meta["etiqueta"], "origen": "agregados validados en data/enaho2024_indicadores.csv",
              "fecha_datos": "2024 (anual)", "aviso": None, "url": fuentes.URL_ENAHO}
    base = {"indicador": meta["etiqueta"], "consulta": consulta, "periodo_usado": "2024", "unidad": "%",
            "fuente": fuente, "fecha_consulta": date.today().isoformat(), "enaho": df, "columna": col,
            "detras": _detras_enaho(df, col)}
    tipo = consulta.get("tipo") or "valor"

    if tipo in ("maximo", "minimo"):
        fila = _buscar_fila(deps, consulta.get("ambito"))
        if fila is None:
            return _no_verificable(consulta, "No identifiqué el departamento de la afirmación.")
        rank = int((deps[col] > fila[col]).sum()) + 1 if tipo == "maximo" else int((deps[col] < fila[col]).sum()) + 1
        top = deps.iloc[0] if tipo == "maximo" else deps.iloc[-1]
        es = rank == 1
        return {**base, "oficial": float(fila[col]), "metodo": METODO_ENAHO, "diferencia": None,
                "veredicto": CORRECTA if es else INCORRECTA,
                "ranking": {"departamento": fila.categoria, "puesto": rank, "de": len(deps),
                            "orden": "de mayor a menor" if tipo == "maximo" else "de menor a mayor",
                            "primero": top.categoria, "valor_primero": float(top[col])},
                "tolerancia": "Ranking: la afirmación es correcta solo si el departamento ocupa el puesto 1 entre "
                              "los 25 (sin considerar el margen de error muestral de la encuesta)."}

    fila = _buscar_fila(df, consulta.get("ambito"))
    if fila is None:
        return _no_verificable(consulta, f"No hay datos de pobreza para el ámbito {consulta.get('ambito')!r} "
                                         "(hay: nacional, área, sexo, grupos de edad y 25 departamentos).")
    oficial = float(fila[col])
    res = {**base, "oficial": oficial, "ambito_usado": fila.categoria, "metodo": METODO_ENAHO}
    res.update(_comparar(consulta, oficial, meta["tol"]))
    return res


def _detras_enaho(df: pd.DataFrame, col: str) -> list[dict]:
    g = df.set_index("categoria")[col]
    deps = df[df.nivel == "departamento"].set_index("categoria")[col]
    return [{"concepto": "Nacional (Perú)", "valor": g["Perú"]},
            {"concepto": "Área rural", "valor": g["rural"]},
            {"concepto": "Área urbana", "valor": g["urbana"]},
            {"concepto": "Niñas y niños de 0 a 14 años", "valor": g["0-14"]},
            {"concepto": f"Departamento más alto ({deps.idxmax()})", "valor": deps.max()},
            {"concepto": f"Departamento más bajo ({deps.idxmin()})", "valor": deps.min()},
            {"concepto": "Brecha rural - urbana (pp)", "valor": round(g["rural"] - g["urbana"], 2)}]
