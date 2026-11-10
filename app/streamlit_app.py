"""CifraVerificada · app Streamlit.   uv run streamlit run app/streamlit_app.py

Flujo: frase -> Gemini (consulta estructurada) -> Python (dato oficial + comparación con tolerancia) -> veredicto,
dato oficial, diferencia, gráfico o mapa, "La cifra detrás de la cifra", ficha de trazabilidad y fuente.
"""
import html
import json
import sys
from pathlib import Path

RAIZ = Path(__file__).resolve().parents[1]
if str(RAIZ) not in sys.path:          # Streamlit Cloud solo agrega app/ al path
    sys.path.insert(0, str(RAIZ))

import plotly.express as px
import plotly.graph_objects as go
import streamlit as st

from ai.interpretar import explicar, interpretar_con_respaldo
from app import fuentes, orientacion
from app.verificador import APROXIMADA, CORRECTA, INCORRECTA, NO_VERIFICABLE, verificar

st.set_page_config(page_title="CifraVerificada", page_icon="✔", layout="centered")

# Paleta «marfil» (Tarea 3 y sitio web); el tema base está en .streamlit/config.toml
AZUL, AZUL_OSC, ROJO, TINTA, TINTA_2, LINEA_C = "#1D4E89", "#0B3B6F", "#C8102E", "#1C2433", "#4A5468", "#E3E1DA"
# veredicto -> (color, fondo, ícono, lectura breve)
ESTILOS = {CORRECTA: ("#1E7A4C", "#E8F3EC", "✓", "Coincide con el dato oficial dentro de la tolerancia."),
           APROXIMADA: ("#8A5A00", "#FBF1DC", "≈", "Cerca del dato oficial, pero fuera del margen exacto."),
           INCORRECTA: (ROJO, "#FBE8EB", "✕", "No coincide con el dato oficial."),
           NO_VERIFICABLE: (TINTA_2, "#ECEEF2", "?", "No hay un indicador oficial disponible aquí para contrastarla.")}
LINEA = AZUL
ESCALA_MAPA = ["#EAF1FA", "#C9DBF1", "#9DBEE6", "#6C9BD6", "#4277BF", "#22579F", "#123C73"]   # --seq de la Tarea 3
FUENTE_GRAF = dict(family="Inter, sans-serif", color=TINTA, size=13)
EJEMPLOS = ["La pobreza en el Perú llegó a 20 % en 2024",
            "La inflación de Lima cerró 2024 en 1.97 %",
            "Cajamarca es el departamento más pobre",
            "El Perú recauda impuestos por más del 20 % del PBI",
            "La pobreza rural es de 40 %"]

CSS = """
<style>
  .block-container {max-width: 860px; padding-top: 1.2rem; padding-bottom: 3rem;}
  .cv-hero {background: #FFFDF8; border: 1px solid LINEA_C; border-bottom: 4px solid ROJO;
            border-radius: .8rem; padding: 1.6rem 1.7rem 1.3rem; margin-bottom: 1.4rem;}
  .cv-kicker {text-transform: uppercase; letter-spacing: .14em; font-size: .74rem; font-weight: 600;
              color: ROJO; margin: 0 0 .35rem;}
  .cv-hero h1 {color: AZUL_OSC; font-size: clamp(2.1rem, 7vw, 3.1rem); line-height: 1.05; margin: 0 0 .6rem;
               padding: 0;}
  .cv-lema {color: TINTA; font-size: 1.05rem; line-height: 1.55; margin: 0 0 1rem; max-width: 62ch;}
  .cv-confianza {display: flex; flex-wrap: wrap; gap: .4rem; align-items: center; font-size: .82rem;
                 color: TINTA_2;}
  .cv-confianza b {color: AZUL_OSC; font-weight: 600; margin-right: .2rem;}
  .cv-chip {border: 1px solid #C9DBF1; background: #EEF4FB; color: AZUL_OSC; border-radius: 999px;
            padding: .12rem .6rem; font-weight: 600;}
  .cv-etq {font-size: .78rem; text-transform: uppercase; letter-spacing: .1em; color: TINTA_2; font-weight: 600;
           margin: .2rem 0 .4rem;}
  div.stButton > button {width: 100%; text-align: left; justify-content: flex-start; font-size: .86rem;
                         white-space: normal; background: #FFFFFF; border: 1px solid LINEA_C; color: TINTA;
                         min-height: 2.6rem;}
  div.stButton > button:hover {border-color: AZUL; color: AZUL;}
  div.stButton > button p {white-space: normal; overflow: visible; text-overflow: clip;}
  [data-testid="stForm"] {background: #FFFFFF; border: 1px solid LINEA_C;}
  [data-testid="stFormSubmitButton"] button {width: 100%; background: AZUL; border-color: AZUL; color: #FFFFFF;
                                             font-weight: 600; min-height: 2.8rem;}
  [data-testid="stFormSubmitButton"] button:hover {background: AZUL_OSC; border-color: AZUL_OSC; color: #FFFFFF;}
  .cv-veredicto {display: flex; gap: 1rem; align-items: flex-start; border-radius: .8rem; padding: 1.2rem 1.3rem;
                 margin: 1.4rem 0 1rem; border: 1px solid; border-left-width: 6px;}
  .cv-icono {flex: 0 0 auto; width: 3rem; height: 3rem; border-radius: 50%; color: #FFFFFF; display: flex;
             align-items: center; justify-content: center; font-size: 1.55rem; font-weight: 700;}
  .cv-veredicto .cv-etiqueta {font-size: 1.3rem; font-weight: 700; letter-spacing: .04em; line-height: 1.2;}
  .cv-veredicto .cv-lectura {font-size: .92rem; margin-top: .15rem; color: TINTA;}
  .cv-veredicto .cv-frase {font-family: Fraunces, Georgia, serif; font-style: italic; font-size: 1.05rem;
                           color: TINTA; margin-top: .5rem;}
  .cv-metricas {display: grid; grid-template-columns: repeat(auto-fit, minmax(170px, 1fr)); gap: .7rem;
                margin: .8rem 0 .4rem;}
  .cv-metrica {background: #FFFFFF; border: 1px solid LINEA_C; border-radius: .7rem; padding: .85rem 1rem;}
  .cv-metrica.oficial {border-top: 3px solid AZUL;}
  .cv-metrica .t {font-size: .76rem; text-transform: uppercase; letter-spacing: .08em; color: TINTA_2;
                  font-weight: 600;}
  .cv-metrica .v {font-size: 1.85rem; font-weight: 700; color: TINTA; line-height: 1.2; margin-top: .2rem;
                  font-variant-numeric: tabular-nums;}
  .cv-metrica.oficial .v {color: AZUL_OSC;}
  .cv-metrica .v small {font-size: .95rem; font-weight: 500; color: TINTA_2; margin-left: .2rem;}
  .cv-metrica .s {font-size: .8rem; color: TINTA_2; margin-top: .1rem;}
  .cv-enlaces {display: grid; gap: .55rem; margin: .6rem 0;}
  .cv-enlace {display: block; background: #FFFFFF; border: 1px solid LINEA_C; border-left: 4px solid AZUL;
              border-radius: .6rem; padding: .7rem .9rem; text-decoration: none !important;}
  .cv-enlace:hover {border-color: AZUL;}
  .cv-enlace .i {display: block; font-size: .72rem; text-transform: uppercase; letter-spacing: .1em; color: ROJO;
                 font-weight: 600;}
  .cv-enlace .n {color: AZUL_OSC; font-weight: 600;}
  .cv-pie {margin-top: 3rem; border-top: 4px solid ROJO; padding-top: 1.3rem;}
  .cv-pie h3 {color: AZUL_OSC; margin: 0 0 .8rem; padding: 0;}
  .cv-pasos {display: grid; grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); gap: .8rem;
             margin-bottom: 1rem;}
  .cv-paso {background: #FFFFFF; border: 1px solid LINEA_C; border-radius: .7rem; padding: .9rem 1rem;
            font-size: .9rem; line-height: 1.5;}
  .cv-paso .n {display: inline-flex; width: 1.7rem; height: 1.7rem; border-radius: 50%; background: AZUL;
               color: #FFFFFF; font-weight: 700; align-items: center; justify-content: center; margin-bottom: .4rem;}
  .cv-paso b {display: block; color: AZUL_OSC; margin-bottom: .2rem;}
  .cv-aviso {font-size: .84rem; color: TINTA_2; background: #F1EDE3; border-radius: .6rem; padding: .75rem 1rem;
             line-height: 1.5;}
  @media (max-width: 640px) {
    .block-container {padding-left: 1rem; padding-right: 1rem; padding-top: .6rem;}
    .cv-hero {padding: 1.2rem 1.1rem 1rem;}
    .cv-veredicto {padding: 1rem; gap: .75rem;}
    .cv-icono {width: 2.5rem; height: 2.5rem; font-size: 1.3rem;}
    .cv-veredicto .cv-etiqueta {font-size: 1.1rem;}
    .cv-metricas {grid-template-columns: repeat(3, minmax(0, 1fr)); gap: .45rem;}
    .cv-metrica {padding: .6rem .6rem;}
    .cv-metrica .t {font-size: .64rem; letter-spacing: .04em;}
    .cv-metrica .v {font-size: 1.3rem;}
    .cv-metrica .v small {font-size: .8rem;}
    .cv-metrica .s {font-size: .72rem;}
  }
</style>"""
for _nombre, _color in (("AZUL_OSC", AZUL_OSC), ("AZUL", AZUL), ("ROJO", ROJO), ("TINTA_2", TINTA_2),
                        ("TINTA", TINTA), ("LINEA_C", LINEA_C)):
    CSS = CSS.replace(_nombre, _color)
st.markdown(CSS, unsafe_allow_html=True)

st.markdown("""
<div class="cv-hero">
  <p class="cv-kicker">Verificador de cifras · Perú</p>
  <h1>CifraVerificada</h1>
  <p class="cv-lema">Verificamos en segundos las cifras económicas y sociales del debate público peruano para
  periodistas, fact-checkers y ONG, contrastándolas con datos oficiales del BCRP y del INEI mediante un agente de IA.</p>
  <div class="cv-confianza"><b>Datos oficiales:</b><span class="cv-chip">BCRP</span><span class="cv-chip">INEI</span><span class="cv-chip">Fuentes ONU</span></div>
</div>""", unsafe_allow_html=True)


@st.cache_data(ttl=12 * 3600, show_spinner=False)
def obtener_serie_cache(codigo: str):
    return fuentes.obtener_serie_sin_cache(codigo, en_vivo=True)


if not hasattr(fuentes, "obtener_serie_sin_cache"):     # una sola vez por proceso (Streamlit re-ejecuta el script)
    fuentes.obtener_serie_sin_cache = fuentes.obtener_serie
fuentes.obtener_serie = lambda codigo, en_vivo=True: (obtener_serie_cache(codigo) if en_vivo
                                                      else fuentes.obtener_serie_sin_cache(codigo, False))

if "frase" not in st.session_state:
    st.session_state.frase = ""

st.markdown('<p class="cv-etq">Prueba con un ejemplo</p>', unsafe_allow_html=True)
cols = st.columns(2)
for i, ej in enumerate(EJEMPLOS):
    if cols[i % 2].button(ej, key=f"ej{i}"):
        st.session_state.frase = ej
        st.session_state.ejecutar = True

with st.form("verificar"):
    frase = st.text_area("Afirmación a verificar", key="frase", height=90,
                         placeholder="Pega aquí la frase. Ej.: La inflación de Lima cerró 2024 en 1.97 %")
    enviado = st.form_submit_button("Verificar con datos oficiales", type="primary")


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
    for k in ("valor_afirmado", "cifra_implicita", "tipo"):      # p. ej. «ya no hay pobres» = 0 %
        if r.get("consulta", {}).get(k) is not None:
            d[k] = r["consulta"][k]
    d["fuente"] = r.get("fuente", {}).get("codigo")
    return d


def tarjeta(r: dict, frase: str):
    fg, bg, icono, lectura = ESTILOS[r["veredicto"]]
    st.markdown(f'<div class="cv-veredicto" style="background:{bg}; border-color:{fg}">'
                f'<div class="cv-icono" style="background:{fg}" aria-hidden="true">{icono}</div><div>'
                f'<div class="cv-etiqueta" style="color:{fg}">{r["veredicto"]}</div>'
                f'<div class="cv-lectura">{lectura}</div>'
                f'<div class="cv-frase">«{html.escape(frase)}»</div></div></div>', unsafe_allow_html=True)


def unidad_diferencia(unidad: str) -> str:
    """La diferencia entre dos porcentajes se expresa en puntos porcentuales (pp)."""
    return "pp" if unidad.startswith("%") else unidad


def metricas(r: dict):
    """Dato afirmado, dato oficial y diferencia como tarjetas (mismos valores que antes, con su unidad)."""
    c = r["consulta"]
    af, u = c.get("valor_afirmado"), r["unidad"]
    prefijo = {"mayor_que": "más de ", "menor_que": "menos de "}.get(c.get("tipo"), "")
    sub_af = (f"implícito: «{html.escape(c['cifra_implicita'])}»" if c.get("cifra_implicita")
              else "lo que dice la frase")
    dif = r.get("diferencia")

    def tile(clase, titulo, valor, unidad, sub):
        uni = f"<small>{html.escape(unidad)}</small>" if unidad and valor != "—" else ""
        return (f'<div class="cv-metrica {clase}"><div class="t">{titulo}</div><div class="v">{valor}{uni}</div>'
                f'<div class="s">{sub}</div></div>')
    st.markdown('<div class="cv-metricas">'
                + tile("", "Dato afirmado", f"{prefijo}{af:g}" if af is not None else "—", u, sub_af)
                + tile("oficial", f"Dato oficial · {r['periodo_usado']}", f"{r['oficial']:.2f}", u,
                       html.escape(r.get("ambito_usado") or r["fuente"]["codigo"]))
                + tile("", "Diferencia", f"{dif:+.2f}".replace("-", "−") if dif is not None else "—",
                       unidad_diferencia(u), "afirmado − oficial")
                + "</div>", unsafe_allow_html=True)


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
        fig.add_hline(y=af, line_dash="dot", line_color=ROJO, annotation_text=f"Afirmado: {af:g}",
                      annotation_position="top left", annotation_font_color=ROJO)
    st.markdown(f"**{r['fuente']['nombre']}**  \n<span style='color:{TINTA_2};font-size:.85rem'>BCRP · "
                f"{r['fuente']['codigo']}</span>", unsafe_allow_html=True)
    fig.update_layout(height=340, showlegend=False, font=FUENTE_GRAF, margin=dict(l=8, r=8, t=10, b=8),
                      plot_bgcolor="#FFFFFF", paper_bgcolor="rgba(0,0,0,0)", yaxis_title=r["unidad"],
                      xaxis=dict(showgrid=False, linecolor=LINEA_C), yaxis=dict(gridcolor="#EFEDE6"))
    st.plotly_chart(fig, width="stretch")


@st.cache_data
def geojson():
    return json.loads(fuentes.GEOJSON.read_text(encoding="utf-8"))


def formato_valor(valor, unidad: str) -> str:
    """27.53 -> "27.53 %"; 15.0 -> "15.0 pp". Máximo 2 decimales, mínimo 1."""
    if valor is None:
        return "—"
    v = round(float(valor), 2)
    txt = f"{v:.2f}" if round(v, 1) != v else f"{v:.1f}"
    return f"{txt} {unidad}".strip()


def mapa_enaho(r: dict):
    df = r["enaho"].query("nivel == 'departamento'")
    col = r["columna"]
    fig = px.choropleth(df, geojson=geojson(), locations="codigo", featureidkey="properties.FIRST_IDDP",
                        color=col, hover_name="categoria", color_continuous_scale=ESCALA_MAPA,
                        labels={col: "%"}, hover_data={"codigo": False, col: ":.2f"})
    fig.update_traces(marker_line_color="#FFFFFF", marker_line_width=0.6)
    # Encuadre fijo del Perú completo (fitbounds sobre el geojson acercaba demasiado al cargar)
    fig.update_geos(visible=False, projection_type="mercator", fitbounds=False, bgcolor="rgba(0,0,0,0)",
                    lonaxis_range=[-81.6, -68.4], lataxis_range=[-18.6, 0.2], center=dict(lon=-75.0, lat=-9.2))
    st.markdown(f"**{r['indicador']} por departamento**  \n<span style='color:{TINTA_2};font-size:.85rem'>"
                "INEI · ENAHO 2024</span>", unsafe_allow_html=True)
    fig.update_layout(height=460, font=FUENTE_GRAF, margin=dict(l=0, r=0, t=6, b=0),
                      paper_bgcolor="rgba(0,0,0,0)", coloraxis_colorbar=dict(thickness=12, len=0.7, title="%"))
    st.plotly_chart(fig, width="stretch")


def mostrar(frase: str):
    with st.spinner("Interpretando la afirmación con Gemini…"):
        consulta, tok1 = interpretar_con_respaldo(frase)
    if consulta is None:
        st.warning("No pude interpretar la frase ahora; intenta de nuevo o usa un ejemplo.")
        return
    with st.spinner("Consultando el dato oficial…"):
        r = verificar(consulta, en_vivo=True)
    with st.spinner("Redactando la explicación…"):
        if tok1["con_ia"]:
            texto, tok2, de_ia = explicar(frase, datos_para_explicar(r), plantilla(r))
        else:                                   # Gemini no disponible: explicación de plantilla, sin esperar
            texto, tok2, de_ia = plantilla(r), {"total": 0}, False

    tarjeta(r, frase)
    st.write(texto)
    if r["veredicto"] != NO_VERIFICABLE or r.get("oficial") is not None:
        f = r["fuente"]
        if f.get("aviso"):
            st.warning(f"La API del BCRP no respondió; uso el snapshot guardado el {f['fecha_datos']}.")
        metricas(r)
        af = r["consulta"].get("valor_afirmado")
        if r["consulta"].get("cifra_implicita"):
            st.caption(f"Cifra implícita en la frase: «{r['consulta']['cifra_implicita']}» se lee como "
                       f"{'más de ' if r['consulta'].get('tipo') == 'mayor_que' else 'menos de ' if r['consulta'].get('tipo') == 'menor_que' else ''}"
                       f"{af:g} %.")
        st.caption(f"Valor oficial exacto: {r['oficial']:g} · Unidad: {r['unidad']} · {r['indicador']}"
                   + (f" · ámbito: {r['ambito_usado']}" if r.get("ambito_usado") else ""))

        if f["tipo"] == "BCRP":
            grafico_bcrp(r)
        else:
            mapa_enaho(r)

        st.subheader("La cifra detrás de la cifra")
        st.caption("Lo que el promedio esconde, calculado desde los mismos datos. Son contrastes descriptivos, "
                   "no relaciones de causa.")
        st.table([{"Concepto": d["concepto"], "Valor": formato_valor(d["valor"], d.get("unidad", r["unidad"]))}
                  for d in r["detras"]])

        with st.expander("Ficha de trazabilidad"):
            st.markdown(f"""
- **Fuente / código:** {f['codigo']} — {f['nombre']}
- **Origen del dato:** {f['origen']} (datos al {f['fecha_datos']}); fuente primaria: {f.get('fuente_primaria', 'INEI')}
- **Periodo usado:** {r['periodo_usado']}
- **Método:** {r['metodo']}
- **Tolerancia:** {r['tolerancia']}
- **Fecha de consulta:** {r['fecha_consulta']}
- **Consulta interpretada por IA:** `{json.dumps(r['consulta'], ensure_ascii=False)}`
- **Interpretación:** {tok1['interpretacion']} · tokens usados: {tok1['total'] + tok2['total']} (interpretación {tok1['total']}, explicación {tok2['total']}) · explicación {'redactada por IA y revisada' if de_ia else 'de plantilla'}
""" + (f"- **Motivo del respaldo sin IA:** {tok1['motivo_respaldo']}\n" if tok1.get("motivo_respaldo") else ""))
            if f.get("url_api"):
                st.markdown(f"- **API:** {f['url_api']}")
        st.markdown(f"**Fuente oficial:** [{f['url']}]({f['url']})")
    else:
        with st.expander("Ficha de trazabilidad"):
            st.markdown(f"- **Consulta interpretada por IA:** `{json.dumps(r['consulta'], ensure_ascii=False)}`\n"
                        f"- **Motivo:** {r.get('motivo')}\n- **Fecha de consulta:** {r['fecha_consulta']}\n"
                        f"- **Interpretación:** {tok1['interpretacion']} · tokens usados: {tok1['total'] + tok2['total']}"
                        + (f"\n- **Motivo del respaldo sin IA:** {tok1['motivo_respaldo']}"
                           if tok1.get("motivo_respaldo") else ""))
        if r["consulta"].get("indicador") == "no_disponible":
            seccion_orientacion(orientacion.enlaces_para(r["consulta"].get("tema_orientacion")))
        st.info("Fuentes disponibles: BCRP (inflación, PBI, tipo de cambio, tasa de referencia, ingresos "
                "tributarios) e INEI ENAHO 2024 (pobreza y pobreza extrema).")


def seccion_orientacion(o: dict):
    """Enlaces de la lista fija data/fuentes_orientacion.json (la IA solo eligió el tema)."""
    st.subheader("Para profundizar en fuentes oficiales")
    st.write(o["texto"])
    st.markdown('<div class="cv-enlaces">' + "".join(
        f'<a class="cv-enlace" href="{html.escape(e["url"])}" target="_blank" rel="noopener">'
        f'<span class="i">{html.escape(e["institucion"])}{" · Sistema ONU" if e["sistema"] == "ONU" else ""}</span>'
        f'<span class="n">{html.escape(e["nombre"])} ↗</span></a>' for e in o["enlaces"]) + "</div>",
        unsafe_allow_html=True)
    st.caption(f"Tema: {o['etiqueta']}. Lista curada y fija (enlaces verificados el {o['verificado']}); "
               "no la genera la IA.")


if (enviado or st.session_state.pop("ejecutar", False)) and st.session_state.frase.strip():
    mostrar(st.session_state.frase.strip())

st.markdown("""
<div class="cv-pie">
  <h3>Cómo funciona</h3>
  <div class="cv-pasos">
    <div class="cv-paso"><span class="n">1</span><b>Interpreta</b>La IA (Gemini) lee la frase y extrae qué
    indicador, ámbito, periodo y cifra se afirman. No calcula ni completa cifras.</div>
    <div class="cv-paso"><span class="n">2</span><b>Consulta</b>Python trae el dato oficial: API del BCRP (con
    respaldo fechado) o agregados de la ENAHO 2024 del INEI.</div>
    <div class="cv-paso"><span class="n">3</span><b>Compara</b>Python contrasta ambas cifras con una tolerancia
    explícita y muestra el veredicto, la fuente y la ficha de trazabilidad.</div>
  </div>
  <div class="cv-aviso"><b>Verificación automática:</b> revisa siempre la fuente. La IA solo interpreta la frase y
  redacta la explicación; las cifras y comparaciones las calcula Python con datos del BCRP y del INEI (ENAHO 2024).
  Asociación no es causalidad.</div>
</div>""", unsafe_allow_html=True)
