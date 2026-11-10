"""CifraVerificada · app Streamlit.   uv run streamlit run app/streamlit_app.py

Flujo: frase -> Gemini (consulta estructurada) -> Python (dato oficial + comparación con tolerancia) -> veredicto,
dato oficial, diferencia, gráfico o mapa, "La cifra detrás de la cifra", ficha de trazabilidad y fuente.
"""
import json
import sys
from pathlib import Path

RAIZ = Path(__file__).resolve().parents[1]
if str(RAIZ) not in sys.path:          # Streamlit Cloud solo agrega app/ al path
    sys.path.insert(0, str(RAIZ))

import plotly.express as px
import plotly.graph_objects as go
import streamlit as st

from ai.interpretar import MODELO, explicar, interpretar
from app import fuentes
from app.verificador import APROXIMADA, CORRECTA, INCORRECTA, NO_VERIFICABLE, verificar

st.set_page_config(page_title="CifraVerificada", page_icon="✔", layout="centered")

COLORES = {CORRECTA: ("#0f6e3f", "#e6f4ec"), APROXIMADA: ("#8a5a00", "#fdf3dc"),
           INCORRECTA: ("#a3261f", "#fbe9e7"), NO_VERIFICABLE: ("#4a4f57", "#eef0f2")}
ICONOS = {CORRECTA: "✔", APROXIMADA: "≈", INCORRECTA: "✖", NO_VERIFICABLE: "?"}
LINEA = "#2b5c8a"
EJEMPLOS = ["La pobreza en el Perú llegó a 20 % en 2024",
            "La inflación de Lima cerró 2024 en 1.97 %",
            "Cajamarca es el departamento más pobre",
            "El Perú recauda impuestos por más del 20 % del PBI",
            "La pobreza rural es de 40 %"]

st.markdown("""
<style>
  .block-container {max-width: 820px; padding-top: 2rem;}
  h1 {font-family: Georgia, 'Times New Roman', serif; font-weight: 600; letter-spacing: -0.5px;}
  .lema {color: #555; font-size: 1.02rem; margin-top: -0.6rem;}
  .veredicto {border-radius: 10px; padding: 1.1rem 1.3rem; margin: 1rem 0; border-left: 6px solid;}
  .veredicto .etiqueta {font-size: 1.35rem; font-weight: 700; letter-spacing: .5px;}
  .veredicto .frase {font-style: italic; margin-top: .3rem;}
  .aviso {font-size: .85rem; color: #666; border-top: 1px solid #ddd; padding-top: .6rem; margin-top: 2rem;}
  div.stButton > button {width: 100%; text-align: left; font-size: .85rem; white-space: normal;}
</style>""", unsafe_allow_html=True)

st.title("CifraVerificada")
st.markdown('<p class="lema">Verificamos en segundos las cifras económicas y sociales del debate público peruano '
            'para periodistas, fact-checkers y ONG, contrastándolas con datos oficiales del BCRP y del INEI '
            'mediante un agente de IA.</p>', unsafe_allow_html=True)


@st.cache_data(ttl=12 * 3600, show_spinner=False)
def obtener_serie_cache(codigo: str):
    return fuentes.obtener_serie_sin_cache(codigo, en_vivo=True)


if not hasattr(fuentes, "obtener_serie_sin_cache"):     # una sola vez por proceso (Streamlit re-ejecuta el script)
    fuentes.obtener_serie_sin_cache = fuentes.obtener_serie
fuentes.obtener_serie = lambda codigo, en_vivo=True: (obtener_serie_cache(codigo) if en_vivo
                                                      else fuentes.obtener_serie_sin_cache(codigo, False))

if "frase" not in st.session_state:
    st.session_state.frase = ""

st.caption("Prueba con un ejemplo:")
cols = st.columns(2)
for i, ej in enumerate(EJEMPLOS):
    if cols[i % 2].button(ej, key=f"ej{i}"):
        st.session_state.frase = ej
        st.session_state.ejecutar = True

with st.form("verificar"):
    frase = st.text_area("Afirmación a verificar", key="frase", height=80,
                         placeholder="Ej.: La inflación de Lima cerró 2024 en 1.97 %")
    enviado = st.form_submit_button("Verificar", type="primary")


def plantilla(r: dict) -> str:
    if r["veredicto"] == NO_VERIFICABLE:
        return r.get("motivo", "No hay datos oficiales en estas fuentes para verificar la afirmación.")
    if r.get("ranking"):
        k = r["ranking"]
        return (f"Según la ENAHO 2024, {k['departamento']} ocupa el puesto {k['puesto']} de {k['de']} "
                f"({k['orden']}); el primero es {k['primero']} con {k['valor_primero']:.2f} %.")
    return (f"El dato oficial de {r['indicador'].lower()} para {r['periodo_usado']} es {r['oficial']:.2f} "
            f"({r['unidad']}); la diferencia con lo afirmado es {r['diferencia']:+.2f}. "
            f"Fuente: {r['fuente']['codigo']}.")


def datos_para_explicar(r: dict) -> dict:
    claves = ["veredicto", "indicador", "oficial", "periodo_usado", "unidad", "diferencia", "metodo", "motivo",
              "ranking", "ambito_usado"]
    d = {k: r[k] for k in claves if r.get(k) is not None}
    d["fuente"] = r.get("fuente", {}).get("codigo")
    return d


def tarjeta(r: dict, frase: str):
    fg, bg = COLORES[r["veredicto"]]
    st.markdown(f'<div class="veredicto" style="background:{bg}; border-color:{fg}; color:{fg}">'
                f'<div class="etiqueta">{ICONOS[r["veredicto"]]} {r["veredicto"]}</div>'
                f'<div class="frase" style="color:#333">«{frase}»</div></div>', unsafe_allow_html=True)


def grafico_bcrp(r: dict):
    s = r["serie"]
    fig = go.Figure(go.Scatter(x=s.index, y=s.values, mode="lines", line=dict(color=LINEA, width=2),
                               name=r["fuente"]["codigo"], hovertemplate="%{x}: %{y:.2f}<extra></extra>"))
    per = r["periodo_usado"]
    if per in s.index:
        fig.add_trace(go.Scatter(x=[per], y=[s[per]], mode="markers", marker=dict(size=11, color=LINEA,
                                 line=dict(color="white", width=2)), name="Dato oficial usado",
                                 hovertemplate="Oficial %{x}: %{y:.2f}<extra></extra>"))
    af = r["consulta"].get("valor_afirmado")
    if af is not None:
        fig.add_hline(y=af, line_dash="dot", line_color="#888", annotation_text=f"Afirmado: {af:g}",
                      annotation_position="top left")
    fig.update_layout(title=f"{r['fuente']['nombre']} ({r['fuente']['codigo']})", height=360, showlegend=False,
                      margin=dict(l=10, r=10, t=50, b=10), plot_bgcolor="white", yaxis_title=r["unidad"],
                      xaxis=dict(showgrid=False), yaxis=dict(gridcolor="#eee"))
    st.plotly_chart(fig, width="stretch")


@st.cache_data
def geojson():
    return json.loads(fuentes.GEOJSON.read_text(encoding="utf-8"))


def mapa_enaho(r: dict):
    df = r["enaho"].query("nivel == 'departamento'")
    col = r["columna"]
    fig = px.choropleth(df, geojson=geojson(), locations="codigo", featureidkey="properties.FIRST_IDDP",
                        color=col, hover_name="categoria", color_continuous_scale="Blues",
                        labels={col: "%"}, hover_data={"codigo": False, col: ":.2f"})
    fig.update_geos(fitbounds="locations", visible=False)
    fig.update_layout(title=f"{r['indicador']} por departamento, ENAHO 2024", height=480,
                      margin=dict(l=0, r=0, t=50, b=0))
    st.plotly_chart(fig, width="stretch")


def mostrar(frase: str):
    with st.spinner("Interpretando la afirmación con Gemini…"):
        try:
            consulta, tok1 = interpretar(frase)
        except Exception as e:
            st.error(f"No pude interpretar la afirmación con Gemini ({type(e).__name__}). Intenta de nuevo.")
            return
    with st.spinner("Consultando el dato oficial…"):
        r = verificar(consulta, en_vivo=True)
    with st.spinner("Redactando la explicación…"):
        texto, tok2, de_ia = explicar(frase, datos_para_explicar(r), plantilla(r))

    tarjeta(r, frase)
    st.write(texto)
    if r["veredicto"] != NO_VERIFICABLE or r.get("oficial") is not None:
        f = r["fuente"]
        if f.get("aviso"):
            st.warning(f"La API del BCRP no respondió; uso el snapshot guardado el {f['fecha_datos']}.")
        c1, c2, c3 = st.columns(3)
        af = r["consulta"].get("valor_afirmado")
        c1.metric("Dato afirmado", f"{af:g}" if af is not None else "—")
        c2.metric(f"Dato oficial ({r['periodo_usado']})", f"{r['oficial']:.2f}")
        c3.metric("Diferencia (afirmado − oficial)", f"{r['diferencia']:+.2f}" if r.get("diferencia") is not None else "—")
        st.caption(f"Valor oficial exacto: {r['oficial']:g} · Unidad: {r['unidad']} · {r['indicador']}"
                   + (f" · ámbito: {r['ambito_usado']}" if r.get("ambito_usado") else ""))

        if f["tipo"] == "BCRP":
            grafico_bcrp(r)
        else:
            mapa_enaho(r)

        st.subheader("La cifra detrás de la cifra")
        st.caption("Lo que el promedio esconde, calculado desde los mismos datos. Son contrastes descriptivos, "
                   "no relaciones de causa.")
        st.table([{"Concepto": d["concepto"], "Valor": d["valor"]} for d in r["detras"]])

        with st.expander("Ficha de trazabilidad"):
            st.markdown(f"""
- **Fuente / código:** {f['codigo']} — {f['nombre']}
- **Origen del dato:** {f['origen']} (datos al {f['fecha_datos']}); fuente primaria: {f.get('fuente_primaria', 'INEI')}
- **Periodo usado:** {r['periodo_usado']}
- **Método:** {r['metodo']}
- **Tolerancia:** {r['tolerancia']}
- **Fecha de consulta:** {r['fecha_consulta']}
- **Consulta interpretada por IA:** `{json.dumps(r['consulta'], ensure_ascii=False)}`
- **Modelo:** {MODELO} · tokens usados: {tok1['total'] + tok2['total']} (interpretación {tok1['total']}, explicación {tok2['total']}) · explicación {'redactada por IA y revisada' if de_ia else 'de plantilla'}
""")
            if f.get("url_api"):
                st.markdown(f"- **API:** {f['url_api']}")
        st.markdown(f"**Fuente oficial:** [{f['url']}]({f['url']})")
    else:
        with st.expander("Ficha de trazabilidad"):
            st.markdown(f"- **Consulta interpretada por IA:** `{json.dumps(r['consulta'], ensure_ascii=False)}`\n"
                        f"- **Motivo:** {r.get('motivo')}\n- **Fecha de consulta:** {r['fecha_consulta']}\n"
                        f"- **Modelo:** {MODELO} · tokens usados: {tok1['total'] + tok2['total']}")
        st.info("Fuentes disponibles: BCRP (inflación, PBI, tipo de cambio, tasa de referencia, ingresos "
                "tributarios) e INEI ENAHO 2024 (pobreza y pobreza extrema).")


if (enviado or st.session_state.pop("ejecutar", False)) and st.session_state.frase.strip():
    mostrar(st.session_state.frase.strip())

st.markdown('<div class="aviso">Verificación automática: revisa siempre la fuente. La IA solo interpreta la frase '
            'y redacta la explicación; las cifras y comparaciones las calcula Python con datos del BCRP y del '
            'INEI (ENAHO 2024).</div>', unsafe_allow_html=True)
