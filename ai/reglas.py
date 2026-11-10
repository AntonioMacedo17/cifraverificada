"""Modo de respaldo SIN IA: interpreta la frase con reglas en Python cuando Gemini falla o tarda más de 15 s.

Reconoce indicador + número + ámbito/periodo con palabras clave y expresiones regulares. Si no reconoce la
frase devuelve None (la app dice "No pude interpretar la frase ahora"): nunca adivina ni inventa.
"""
import re
import unicodedata

from app import fuentes, orientacion

MESES = {"enero": 1, "febrero": 2, "marzo": 3, "abril": 4, "mayo": 5, "junio": 6, "julio": 7, "agosto": 8,
         "septiembre": 9, "setiembre": 9, "octubre": 10, "noviembre": 11, "diciembre": 12}
# el orden importa: lo más específico primero
INDICADORES = [
    ("pobreza_extrema", ("pobreza extrema", "extrema pobreza", "pobres extremos")),
    ("pobreza", ("pobreza", "pobre")),
    ("inflacion", ("inflacion", "ipc", "precios")),
    ("tipo_cambio", ("tipo de cambio", "dolar")),
    ("tasa_referencia", ("tasa de referencia", "tasa de interes")),
    ("ingresos_tributarios", ("impuesto", "tributari", "recauda")),
    ("crecimiento_pbi", ("pbi", "crecimiento", "economia crecio", "economia peruana crecio")),
]
MAYOR = ("mas de", "mas del", "supera", "por encima", "mayor a", "mayor al", "mayor que")
MENOR = ("menos de", "menos del", "por debajo", "menor a", "menor al", "menor que")
MAXIMO = ("mas pobre", "mas alto", "mas alta", "mayor pobreza", "mayor tasa")
MINIMO = ("menos pobre", "mas bajo", "mas baja", "menor pobreza", "menor tasa")
# Cifras implícitas (solo pobreza): negar el fenómeno = 0 %; "la mayoría" = más del 50 %.
NIEGA = [r"\bno (existe|existen|hay|queda|quedan)\b.*?\bpobre\w*", r"\bya no hay\b.*?\bpobre\w*",
         r"\bpobreza (ya )?(desaparecio|ha desaparecido|se acabo|se termino|se erradico|fue erradicada|es cero)",
         r"\b(erradico|erradicamos|elimino|eliminamos|acabo con|acabamos con|se acabo) la pobreza",
         r"\b(nadie|ningun peruano|ninguna persona) es pobre", r"\bcero pobres\b", r"\bsin pobreza\b"]
MAYORIA = (r"\bla mayoria\b", r"\bmas de la mitad\b", r"\bla mayor parte\b")
MINORIA = (r"\bmenos de la mitad\b", r"\buna minoria\b")
AMBITOS = [("rural", "rural"), ("urban", "urbana"), ("nin", "0-14"), ("infancia", "0-14"), ("infantil", "0-14"),
           ("mujer", "mujer"), ("hombre", "hombre"), ("adultos mayores", "60 y más")]


def _norm(s: str) -> str:
    return unicodedata.normalize("NFD", s.lower()).encode("ascii", "ignore").decode()


def _departamentos() -> list[str]:
    df = fuentes.leer_enaho()
    return df[df.nivel == "departamento"].categoria.tolist()


def interpretar_reglas(frase: str) -> dict | None:
    t = _norm(frase)
    indicador = next((k for k, claves in INDICADORES if any(c in t for c in claves)), None)
    if indicador is None:
        tema = orientacion.tema_por_palabras(frase)      # tema sin indicador: orientar con la lista fija
        if tema is None:
            return None
        return {"indicador": "no_disponible", "ambito": None, "periodo": None, "tipo": "valor",
                "valor_afirmado": None, "unidad": None, "cifra_implicita": None, "tema_orientacion": tema}

    anio = re.search(r"\b(19[5-9]\d|20[0-4]\d)\b", t)
    periodo = anio[1] if anio else None
    mes = re.search(r"\b(" + "|".join(MESES) + r")\s+(?:de|del)?\s*(19[5-9]\d|20[0-4]\d)\b", t)
    if mes:
        periodo = f"{mes[2]}-{MESES[mes[1]]:02d}"

    sin_anios = re.sub(r"\b(19[5-9]\d|20[0-4]\d)\b", " ", t)
    num = re.search(r"(\d+(?:[.,]\d+)?)", sin_anios)
    valor = float(num[1].replace(",", ".")) if num else None

    ambito = "nacional"
    dep = next((d for d in sorted(_departamentos(), key=len, reverse=True) if _norm(d) in t), None)
    if indicador.startswith("pobreza"):
        ambito = dep or next((a for clave, a in AMBITOS if clave in t), "nacional")

    implicita = None
    if valor is None and indicador.startswith("pobreza"):
        for patrones, tipo_imp, v in ((NIEGA, "valor", 0.0), (MINORIA, "menor_que", 50.0), (MAYORIA, "mayor_que", 50.0)):
            m = next((re.search(p, t) for p in patrones if re.search(p, t)), None)
            if m:
                implicita, valor = m[0], v
                break
    if implicita is not None:
        return {"indicador": indicador, "ambito": ambito, "periodo": periodo, "tipo": tipo_imp,
                "valor_afirmado": valor, "unidad": "%", "cifra_implicita": implicita, "tema_orientacion": None}

    if any(c in t for c in MAXIMO) and dep and valor is None:
        tipo = "maximo"
    elif any(c in t for c in MINIMO) and dep and valor is None:
        tipo = "minimo"
    elif valor is None:
        return None                       # sin cifra ni ranking: no hay nada que verificar
    elif any(c in t for c in MAYOR):
        tipo = "mayor_que"
    elif any(c in t for c in MENOR):
        tipo = "menor_que"
    else:
        tipo = "valor"
    return {"indicador": indicador, "ambito": ambito, "periodo": periodo, "tipo": tipo,
            "valor_afirmado": valor, "unidad": "%" if "%" in frase or "por ciento" in t else None,
            "cifra_implicita": None, "tema_orientacion": None}
