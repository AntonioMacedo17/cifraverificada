"""Orientación cuando una afirmación NO es verificable: enlaces de una lista fija y curada.

Los enlaces salen solo de data/fuentes_orientacion.json (verificados con HTTP 200 antes de incluirlos; se
re-verifican con `uv run python -m app.orientacion`). La IA solo elige el TEMA entre las claves del archivo;
Python pone los enlaces, con prioridad al sistema de la ONU. Nunca se genera un enlace.
"""
import json
import re
import unicodedata
from functools import lru_cache
from pathlib import Path

RAIZ = Path(__file__).resolve().parents[1]
ARCHIVO = RAIZ / "data" / "fuentes_orientacion.json"
TEXTO = ("Esta afirmación no se puede verificar con cifras oficiales disponibles aquí; te sugerimos revisar "
         "estas fuentes oficiales:")
MAX_ENLACES = 4


def _norm(s: str) -> str:
    return unicodedata.normalize("NFD", s.lower()).encode("ascii", "ignore").decode()


@lru_cache(maxsize=1)
def cargar() -> dict:
    return json.loads(ARCHIVO.read_text(encoding="utf-8"))


def temas() -> list[str]:
    return list(cargar()["temas"])


def tema_por_palabras(frase: str) -> str | None:
    """Tema de la lista cuya palabra clave más larga aparece en la frase (para el modo sin IA)."""
    t = _norm(frase)
    mejor, largo = None, 0
    for clave, tema in cargar()["temas"].items():
        for p in tema["palabras_clave"]:
            if re.search(r"\b" + re.escape(_norm(p)), t) and len(p) > largo:
                mejor, largo = clave, len(p)
    return mejor


def enlaces_para(tema: str | None) -> dict:
    """{"tema", "etiqueta", "texto", "enlaces": [2-4 enlaces, primero los de la ONU]} desde la lista fija."""
    d = cargar()
    clave = tema if tema in d["temas"] else "general"
    t = d["temas"][clave]
    enlaces = [{"id": i, **d["enlaces"][i]} for i in t["enlaces"]]
    enlaces.sort(key=lambda e: e["sistema"] != "ONU")          # estable: conserva el orden curado
    return {"tema": clave, "etiqueta": t["etiqueta"], "texto": TEXTO, "enlaces": enlaces[:MAX_ENLACES],
            "verificado": d["verificado"]}


def verificar_enlaces(timeout: float = 25) -> dict[str, int | str]:
    """Estado HTTP de cada enlace de la lista (para re-verificar la curaduría)."""
    import concurrent.futures as cf

    import httpx
    cab = {"User-Agent": "Mozilla/5.0 (CifraVerificada; verificador de enlaces)"}

    def estado(url: str):
        try:
            return httpx.get(url, headers=cab, follow_redirects=True, timeout=timeout).status_code
        except Exception as e:
            return type(e).__name__
    ids = list(cargar()["enlaces"])
    with cf.ThreadPoolExecutor(8) as ex:
        res = ex.map(lambda i: estado(cargar()["enlaces"][i]["url"]), ids)
    return dict(zip(ids, res))


if __name__ == "__main__":
    for i, e in verificar_enlaces().items():
        print(f"{e!s:>4}  {i:15} {cargar()['enlaces'][i]['url']}")
