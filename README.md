# CifraVerificada

> Verificamos en segundos las cifras económicas y sociales del debate público peruano para periodistas,
> fact-checkers y ONG, contrastándolas con datos oficiales del BCRP y del INEI mediante un agente de IA.

Proyecto final del diplomado *Data Science con Python* (Issue #204). Proyecto de impacto social, gratuito.

*(README en construcción; la versión completa se publica en la siguiente entrega.)*

## Qué hace

1. Pegas una afirmación (p. ej., *"La inflación de Lima cerró 2024 en 1.97 %"*).
2. **Gemini** (`gemini-3.8-flash`, salida JSON con esquema) la convierte en una consulta estructurada:
   indicador, ámbito, periodo, valor afirmado y unidad.
3. **Python** consulta el dato oficial (API del BCRP en vivo, con snapshot fechado de respaldo, o los
   agregados de la ENAHO 2024 del INEI) y lo compara con una **tolerancia explícita**.
4. Veredicto: **CORRECTA / APROXIMADA / INCORRECTA / NO VERIFICABLE CON ESTAS FUENTES**, con el dato
   oficial, la diferencia, un gráfico o mapa, *La cifra detrás de la cifra* y una *ficha de trazabilidad*.

El modelo **nunca** calcula cifras: solo interpreta la frase y redacta la explicación (que se revisa en
Python: si menciona un número que no está en los datos calculados, se reemplaza por una plantilla).

## Indicadores verificables

| Indicador | Fuente | Código / método |
|---|---|---|
| Inflación Lima Metropolitana (var. % 12 meses) | BCRP | PN01273PM |
| Crecimiento del PBI (anual / mensual) | BCRP | PM04863AA / PN01728AM |
| Tipo de cambio bancario (S/ por US$) | BCRP | PN01210PM |
| Tasa de referencia | BCRP | PD04722MM |
| Ingresos tributarios del gobierno general (% del PBI) | BCRP | PM05876FA |
| Pobreza y pobreza extrema 2024 (nacional, área, sexo, edad, 25 departamentos) | INEI, ENAHO 2024 | personas ponderadas con `facpob07` |

**Frases sin cifra explícita.** Las negaciones se leen como una cifra implícita (*"ya no hay pobres"*,
*"la pobreza desapareció"* → 0 %; *"la mayoría de peruanos es pobre"* → más del 50 %) y se contrastan con la
ENAHO; la ficha muestra la expresión usada. Si el tema no tiene indicador (democracia, corrupción, educación,
salud, empleo…), el veredicto es *NO VERIFICABLE CON ESTAS FUENTES* y se sugieren 2-4 fuentes oficiales de una
**lista fija y curada** (`data/fuentes_orientacion.json`, prioridad al sistema de la ONU: CEPAL, PNUD, ONU/ODS,
OMS, UNESCO, UNODC, UNICEF; luego INEI, BCRP y MEF). La IA solo elige el tema; los enlaces los pone Python.
Re-verificar los enlaces: `uv run python -m app.orientacion` (solo se incluyen los que responden HTTP 200).

La pobreza nacional calculada es 27.53 % frente al 27.6 % oficial del INEI (diferencia de método).
El repositorio solo contiene agregados: **ningún microdato**.

## Cómo correrla en local

```bash
uv sync
cp .env.example .env        # y escribe tu GEMINI_API_KEY
uv run streamlit run app/streamlit_app.py
uv run pytest -q            # pruebas del motor (sin red ni LLM)
uv run python -m app.fuentes   # (opcional) actualizar el snapshot del BCRP
```

## Despliegue (Streamlit Community Cloud)

- **URL pública:** https://cifraverificada.streamlit.app
- Repo `AntonioMacedo17/cifraverificada`, rama `main`, archivo `app/streamlit_app.py`.
- **Python:** la nube corre con **3.14** (según el log de despliegue); en local se desarrolla con 3.12. Las pruebas pasan en ambas versiones (`uv run --isolated --python 3.14 --with pytest pytest -q`).
- Si la ficha de trazabilidad dice "reglas en Python (sin IA)", la línea *Motivo del respaldo sin IA* indica la causa (503, 429, tiempo agotado, falta la clave en Secrets u otro error con su tipo).
- `.streamlit/config.toml` desactiva la vigilancia de archivos (`fileWatcherType = "none"`): al recargar tras un
  push, Streamlit sacaba el paquete `app` de `sys.modules` mientras otra sesión lo importaba (`KeyError: 'app'`).
  Si tras un push la app no se actualiza, usar *Reboot app* en el panel de la nube.
- Gemini: un intento de 10 s con `gemini-3.8-flash`; si da 429/500/503/504 o se agota, `gemini-3.1-flash-lite`
  (la API rechaza plazos menores a 10 s). No se inicia un intento pasados 15 s; luego, reglas en Python.
- La clave va en *Settings → Secrets* como `GEMINI_API_KEY = "..."` (nunca en el repositorio).
- Dependencias: `uv.lock` (y `requirements.txt`, exportado del mismo lock con `uv export`).
- En la nube `data/registro_tokens.csv` no persiste entre reinicios; si la API del BCRP no responde se
  usa el snapshot de `data/` y se muestra su fecha.

## Estructura

```
app/    streamlit_app.py (interfaz), verificador.py (comparación y tolerancias), fuentes.py (BCRP + ENAHO)
ai/     interpretar.py (Gemini: consulta estructurada y explicación; registro de tokens)
data/   bcrp_snapshot.json, enaho2024_indicadores.csv, peru_departamental_simple.geojson
tests/  test_verificador.py (6 afirmaciones con veredicto esperado)
docs/   documentación y docs/research/
```

Licencia MIT (cubre el código; los datos pertenecen al BCRP y al INEI).
