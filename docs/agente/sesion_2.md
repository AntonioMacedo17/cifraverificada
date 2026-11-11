 ▐▛███▛█   Claude Code v2.1.321
▝▜██████▀  Opus 5.5 · Claude Pro
 ▝▝   ▝▝   ~\repos\cifraverificada

  Fable 5.2 is here for your longest and toughest coding tasks, and is included in your plan until November 16. It draws down usage faster than Opus 5.5. Switch with /model.

> Hola ccode. Retomo CifraVerificada (lee CLAUDE.md y README.md). Vamos a       
  desplegar ya en Streamlit Community Cloud: repo                               
  AntonioMacedo17/cifraverificada, rama main, archivo app/streamlit_app.py.     
  1. Revisa que la app arranque desde la raíz del repo como lo hará la nube     
  (imports de app/ y ai/, rutas de data/, lectura de                            
  st.secrets["GEMINI_API_KEY"]) y que requirements.txt y uv.lock estén          
  coherentes. Si tienes que corregir algo, hazlo.                               
  2. Corre uv run pytest -q y confirma que todo pase.                           
  3. Haz un commit pequeño de hoy (por ejemplo, ajustes de despliegue o una     
  nota en el README sobre la URL pendiente) y push.                             
  4. Dime qué Python version elegir en la nube y avísame si hay algún riesgo.   
  No toques el .env ni muestres la clave.                                       

  Ran 6 shell commands (ctrl+o to expand)
  ⎿  1 action blocked by auto mode
     │ Auto mode: No reason provided

● Revisé rutas, secretos e imports; las 25 pruebas pasan y la app responde en
  local. Ahora ejecuto el script completo con AppTest para confirmar que
  renderiza sin errores.

  Ran 1 shell command (ctrl+o to expand)

● Renderiza sin excepciones. Detengo el servidor de prueba que inicié (solo el
  del puerto 8599).

  Ran 1 shell command (ctrl+o to expand)

● Todo está en orden. Agrego al README una nota de despliegue (URL pendiente) y
  hago el commit sin incluir docs/agente/.

● Update(README.md)
  ⎿  Added 9 lines
      44  uv run python -m app.fuentes   # (opcional) actualizar el snaps
          hot del BCRP
      45  ```
      46  
      47 +## Despliegue (Streamlit Community Cloud)                      
      48 +                                                               
      49 +- **URL pública:** *pendiente (se agrega al terminar el desplie
         +gue).*                                                         
      50 +- Repo `AntonioMacedo17/cifraverificada`, rama `main`, archivo 
         +`app/streamlit_app.py`, Python 3.12.                           
      51 +- La clave va en *Settings → Secrets* como `GEMINI_API_KEY = ".
         +.."` (nunca en el repositorio).                                
      52 +- Dependencias: `uv.lock` (y `requirements.txt`, exportado del 
         +mismo lock con `uv export`).                                   
      53 +- En la nube `data/registro_tokens.csv` no persiste entre reini
         +cios; si la API del BCRP no responde se                        
      54 +  usa el snapshot de `data/` y se muestra su fecha.            
      55 +                                                               
      56  ## Estructura
      57  
      58  ```

  Pushed to main (ctrl+o to expand)

● La app está lista para desplegar: no tuve que corregir código, solo agregué
  una nota de despliegue al README, la subí con un commit y ya hice el push.

  1. Revisión para la nube
  - Imports: app/streamlit_app.py agrega la raíz del repo al path, así que from 
    app import … y from ai import … funcionan aunque la nube solo agregue app/.
    Ejecuté el script completo desde la raíz con el modo de prueba de Streamlit
    (AppTest): cero excepciones y aparece el título "CifraVerificada". El
    servidor también levantó y respondió normalmente.
  - Rutas de data/: se calculan desde la ubicación de cada archivo, así que no
    dependen de la carpeta desde donde se lance la app.
  - Clave: ai/interpretar.py lee primero st.secrets["GEMINI_API_KEY"] y, si no
    está, la busca en .env. Si falta la clave, se muestra un error claro. Si
    Gemini falla o tarda más de 15 s, se usa el modo de reglas sin IA.
  - Dependencias: uv lock --check sale sin problemas y requirements.txt coincide
    con un uv export nuevo; solo cambia la línea de comentario del encabezado.

  2. Pruebas: uv run pytest -q da 25 pasadas y ninguna falla.

  3. Commit: e142c2f agrega al README una sección "Despliegue" con la URL
  pendiente, Python 3.12, cómo poner la clave en Secrets y las dependencias. No
  incluí docs/agente/ porque no está versionado y no me lo pediste.

  4. Versión de Python: elige 3.12. Es la que usas en local (3.12.10) y con la
  que pasaron las pruebas, y tu proyecto pide 3.11 o más nueva.

  Riesgos a tener en cuenta:
  - La clave: en Advanced settings → Secrets escribe GEMINI_API_KEY = 
    "tu-clave", con comillas porque es formato TOML. No toqué el .env ni mostré
    la clave.
  - Qué archivo de dependencias usa la nube: si recuerdo bien, Streamlit Cloud
    prefiere uv.lock antes que requirements.txt. Como ahora los dos coinciden,
    no importa cuál use, pero si cambias dependencias vuelve a exportar
    requirements.txt desde el lock.
  - Registro de tokens: en la nube data/registro_tokens.csv se borra con cada
    reinicio. La app no se rompe si no puede escribirlo, pero no sirve como
    registro permanente.
  - API del BCRP: puede bloquear o hacer más lenta la conexión desde servidores
    fuera de Perú. Si pasa, la app usa el snapshot y muestra su fecha, como pide
    la regla 5. Conviene revisarlo con una consulta del BCRP en la app ya
    desplegada.
  - Cuota de Gemini: con la app pública, el plan gratuito puede devolver
    errores 429. En ese caso la app cambia al modelo de respaldo y luego a las
    reglas en Python, y lo indica en la ficha de trazabilidad.
  - Primer arranque: la app se apaga tras días sin visitas y el primer acceso
    después tarda un poco. Ábrela antes de una presentación.

  Cuando tengas la URL, pásamela y la pongo en el README en otro commit pequeño.

✻ Churned for 1m 16s · done 12:05 a.m.

※ recap: Estamos desplegando CifraVerificada en Streamlit Community Cloud: la app ya funciona, las 25 pruebas pasan y el commit con la nota de despliegue está subido. Ahora te toca crear la app en la nube con Python 3.12, poner la clave en Secrets y pasarme la URL. (disable recaps in /config)

> Ya está desplegada en https://cifraverificada.streamlit.app y el flujo        
  funciona en la nube. Ajustes:                                                 
  1. URL: reemplaza "pendiente" en el README por                                
  https://cifraverificada.streamlit.app. Nota: la nube está usando Python 3.14  
  (se ve en el log), no 3.12; anótalo en el README y revisa si hay algún        
  riesgo.                                                                       
  2. GEMINI EN LA NUBE: en la URL pública la ficha dice siempre "reglas en      
  Python (sin IA)", aunque ya puse GEMINI_API_KEY en Secrets. Agrega en la      
  ficha de trazabilidad el MOTIVO del respaldo (por ejemplo: "Gemini saturado   
  (503)", "cuota agotada (429)", "tiempo agotado (15 s)", "falta la clave en    
  Secrets", u otro error con su tipo), sin mostrar la clave, para que yo pueda  
  diagnosticarlo desde la app.                                                  
  3. MAPA: el mapa por departamento aparece muy acercado al cargar; haz que se  
  vea el Perú completo de entrada (fitbounds o un zoom y centro fijos).         
  4. FORMATO: en "La cifra detrás de la cifra" los valores salen con 4          
  decimales (27.5300); muéstralos con 1 o 2 decimales y su unidad (% o pp).     
     Corre las pruebas, haz commit y push, y avísame para probar en la nube.    

  Ran 4 shell commands (ctrl+o to expand)

● Ahora implemento los cambios. Primero el motivo del respaldo en
  ai/interpretar.py:

● Bash(cd "/c/Users/Antonio Macedo/repos/cifraverificada" && python - <<'EOF'
      from pathlib import Path…)
  ⎿  <stdin>:39: SyntaxWarning: invalid escape sequence '\-'
     138:                raise TimeoutError(f"Gemini no respondió en {limit
     e_s:g} s") from ultimo
     … +5 lines (ctrl+o to expand)
  ⎿  Updated ai\interpretar.py (+41 -2)
      135          for i in range(intentos):
      136              restante = limite_s - (time.monotonic() - inicio)
      137              if restante < 1:
      138 -                raise TimeoutError(f"Gemini no respondió en {l
          -imite_s:g} s ({ultimo!r})")                                   
      138 +                raise TimeoutError(f"Gemini no respondió en {l
          +imite_s:g} s") from ultimo                                    
      139              try:
      140                  r = _cliente(restante).models.generate_content
           (model=modelo, contents=prompt, config=cfg)
      141                  u = r.usage_metadata
     ...
      161      return c, uso
      162  
      163  
      164 +def motivo_respaldo(e: BaseException | None) -> str:          
      165 +    """Motivo legible de por qué no respondió Gemini, para la 
          +ficha de trazabilidad. Nunca incluye la clave."""             
      166 +    if e is None:                                             
      167 +        return "error desconocido"                            
      168 +    if isinstance(e, TimeoutError):                           
      169 +        causa = e.__cause__                                   
      170 +        return f"tiempo agotado ({LIMITE_S} s)" + (f"; último 
          +error: {motivo_respaldo(causa)}" if causa else "")            
      171 +    if isinstance(e, RuntimeError) and "GEMINI_API_KEY" in str
          +(e):                                                          
      172 +        return "falta la clave GEMINI_API_KEY en Secrets"     
      173 +    if isinstance(e, ImportError):                            
      174 +        return f"no se pudo cargar la librería de Gemini ({typ
          +e(e).__name__}: {e})"                                         
      175 +    codigo = getattr(e, "code", None)                         
      176 +    nombre = type(e).__name__                                 
      177 +    if codigo == 503:                                         
      178 +        return "Gemini saturado (503)"                        
      179 +    if codigo == 429:                                         
      180 +        return "cuota agotada (429)"                          
      181 +    if codigo in (400, 401, 403):                             
      182 +        detalle = "clave inválida o sin permiso" if "key" in s
          +tr(e).lower() or codigo != 400 else "solicitud rechazada"     
      183 +        texto = f"{detalle} ({codigo}, {nombre})"             
      184 +    elif codigo == 404:                                       
      185 +        texto = f"modelo no encontrado (404, {nombre})"       
      186 +    elif codigo is not None:                                  
      187 +        texto = f"error de la API de Gemini ({codigo}, {nombre
          +})"                                                           
      188 +    else:                                                     
      189 +        texto = nombre                                        
      190 +    mensaje = str(e)                                          
      191 +    clave = None                                              
      192 +    try:                                                      
     … 21 more lines (ctrl+o to expand)

  Ran 1 shell command (ctrl+o to expand)

● Ahora la ficha, el mapa y el formato de "La cifra detrás de la cifra":

● Bash(cd "/c/Users/Antonio Macedo/repos/cifraverificada" && python - <<'EOF'
      from pathlib import Path…)
  ⎿  def _detras_enaho(df: pd.DataFrame, col: str) -> list[dict]:
         g = df.set_index("categoria")[col]
         deps = df[df.nivel == "departamento"].set_index("categoria")[col]
     … +11 lines (ctrl+o to expand)
  ⎿  Updated app\streamlit_app.py (+20 -4)
      126      return json.loads(fuentes.GEOJSON.read_text(encoding="utf-
           8"))
      127  
      128  
      129 +def formato_valor(valor, unidad: str) -> str:                 
      130 +    """27.53 -> "27.53 %"; 15.0 -> "15.0 pp". Máximo 2 decimal
          +es, mínimo 1."""                                              
      131 +    if valor is None:                                         
      132 +        return "—"                                            
      133 +    v = round(float(valor), 2)                                
      134 +    txt = f"{v:.2f}" if round(v, 1) != v else f"{v:.1f}"      
      135 +    return f"{txt} {unidad}".strip()                          
      136 +                                                              
      137 +                                                              
      138  def mapa_enaho(r: dict):
      139      df = r["enaho"].query("nivel == 'departamento'")
      140      col = r["columna"]
      141      fig = px.choropleth(df, geojson=geojson(), locations="codi
           go", featureidkey="properties.FIRST_IDDP",
      142                          color=col, hover_name="categoria", col
           or_continuous_scale="Blues",
      143                          labels={col: "%"}, hover_data={"codigo
           ": False, col: ":.2f"})
      135 -    fig.update_geos(fitbounds="locations", visible=False)     
      144 +    # Encuadre fijo del Perú completo (fitbounds sobre el geoj
          +son acercaba demasiado al cargar)                             
      145 +    fig.update_geos(visible=False, projection_type="mercator",
          + fitbounds=False,                                             
      146 +                    lonaxis_range=[-81.6, -68.4], lataxis_rang
          +e=[-18.6, 0.2], center=dict(lon=-75.0, lat=-9.2))             
      147      fig.update_layout(title=f"{r['indicador']} por departament
           o, ENAHO 2024", height=480,
      148                        margin=dict(l=0, r=0, t=50, b=0))
      149      st.plotly_chart(fig, width="stretch")
     ...
      185          st.subheader("La cifra detrás de la cifra")
      186          st.caption("Lo que el promedio esconde, calculado desd
           e los mismos datos. Son contrastes descriptivos, "
      187                     "no relaciones de causa.")
      177 -        st.table([{"Concepto": d["concepto"], "Valor": d["valo
          -r"]} for d in r["detras"]])                                   
      188 +        st.table([{"Concepto": d["concepto"], "Valor": formato
          +_valor(d["valor"], d.get("unidad", r["unidad"]))}             
      189 +                  for d in r["detras"]])                      
      190  
      191          with st.expander("Ficha de trazabilidad"):
      192              st.markdown(f"""
     ...
      198  - **Fecha de consulta:** {r['fecha_consulta']}
      199  - **Consulta interpretada por IA:** `{json.dumps(r['consulta']
           , ensure_ascii=False)}`
      200  - **Interpretación:** {tok1['interpretacion']} · tokens usados
           : {tok1['total'] + tok2['total']} (interpretación {tok1['total
           ']}, explicación {tok2['total']}) · explicación {'redactada po
           r IA y revisada' if de_ia else 'de plantilla'}
      189 -""")                                                          
      201 +""" + (f"- **Motivo del respaldo sin IA:** {tok1['motivo_respa
          +ldo']}                                                        
      202 +" if tok1.get("motivo_respaldo") else ""))                    
     … 14 more lines (ctrl+o to expand)
  ⎿  Updated app\verificador.py (+3 -3)
      165                {"concepto": f"Mínimo de la ventana ({s.idxmin()
           })", "valor": round(float(s.min()), 2)},
      166                {"concepto": f"Promedio {s.index[0]} a {s.index[
           -1]}", "valor": round(float(s.mean()), 2)},
      167                {"concepto": f"Último dato disponible ({s.index[
           -1]})", "valor": round(float(s.iloc[-1]), 2)}]
      168 -    return filas                                              
      168 +    return [{**f, "unidad": unidad} for f in filas]           
      169  
      170  
      171  def _buscar_fila(df: pd.DataFrame, ambito: str | None) -> pd.S
           eries | None:
     ...
      224  def _detras_enaho(df: pd.DataFrame, col: str) -> list[dict]:
      225      g = df.set_index("categoria")[col]
      226      deps = df[df.nivel == "departamento"].set_index("categoria
           ")[col]
      227 -    return [{"concepto": "Nacional (Perú)", "valor": g["Perú"]
          -},                                                            
      227 +    filas = [{"concepto": "Nacional (Perú)", "valor": g["Perú"
          +]},                                                           
      228              {"concepto": "Área rural", "valor": g["rural"]},
      229              {"concepto": "Área urbana", "valor": g["urbana"]},
      230              {"concepto": "Niñas y niños de 0 a 14 años", "valo
           r": g["0-14"]},
      231              {"concepto": f"Departamento más alto ({deps.idxmax
           ()})", "valor": deps.max()},
      232              {"concepto": f"Departamento más bajo ({deps.idxmin
           ()})", "valor": deps.min()},
      233 -            {"concepto": "Brecha rural - urbana (pp)", "valor"
          -: round(g["rural"] - g["urbana"], 2)}]                        
      233 +            {"concepto": "Brecha rural - urbana", "valor": rou
          +nd(g["rural"] - g["urbana"], 2), "unidad": "pp"}]             

● Update(app\verificador.py)
  ⎿  Added 7 lines, removed 6 lines
      225      g = df.set_index("categoria")[col]
      226      deps = df[df.nivel == "departamento"].set_index("categoria
           ")[col]
      227      filas = [{"concepto": "Nacional (Perú)", "valor": g["Perú"
           ]},
      228 -            {"concepto": "Área rural", "valor": g["rural"]},  
      229 -            {"concepto": "Área urbana", "valor": g["urbana"]},
      230 -            {"concepto": "Niñas y niños de 0 a 14 años", "valo
          -r": g["0-14"]},                                               
      231 -            {"concepto": f"Departamento más alto ({deps.idxmax
          -()})", "valor": deps.max()},                                  
      232 -            {"concepto": f"Departamento más bajo ({deps.idxmin
          -()})", "valor": deps.min()},                                  
      233 -            {"concepto": "Brecha rural - urbana", "valor": rou
          -nd(g["rural"] - g["urbana"], 2), "unidad": "pp"}]             
      228 +             {"concepto": "Área rural", "valor": g["rural"]}, 
      229 +             {"concepto": "Área urbana", "valor": g["urbana"]}
          +,                                                             
      230 +             {"concepto": "Niñas y niños de 0 a 14 años", "val
          +or": g["0-14"]},                                              
      231 +             {"concepto": f"Departamento más alto ({deps.idxma
          +x()})", "valor": deps.max()},                                 
      232 +             {"concepto": f"Departamento más bajo ({deps.idxmi
          +n()})", "valor": deps.min()},                                 
      233 +             {"concepto": "Brecha rural - urbana", "valor": ro
          +und(g["rural"] - g["urbana"], 2), "unidad": "pp"}]            
      234 +    return [{**f, "valor": round(float(f["valor"]), 2), "unida
          +d": f.get("unidad", "%")} for f in filas]                     

  Ran 1 shell command (ctrl+o to expand)

● Agrego pruebas para el motivo del respaldo y las unidades:

● Write(tests\test_despliegue.py)
  ⎿  Wrote 60 lines to tests\test_despliegue.py
       1 """Ajustes de despliegue: motivo del respaldo sin IA (sin mostra
         r la clave) y unidades de "la cifra detrás"."""
       2 import pytest
       3 from google.genai import errors
       4 
       5 import ai.interpretar as ia
       6 from app.verificador import verificar
       7 
       8 
       9 def _api(cls, code, msg="detalle"):
     … +51 lines (ctrl+o to expand)

  Ran 1 shell command (ctrl+o to expand)

● 32 pruebas pasan. Verifico el render de la app y pruebo también con Python
  3.14 (el de la nube):

  Ran 1 shell command (ctrl+o to expand)

● Mi edición metió un salto de línea real dentro de un f-string; lo corrijo:

  Ran 2 shell commands (ctrl+o to expand)

● Update(app\streamlit_app.py)
  ⎿  Added 1 line, removed 2 lines
      198  - **Fecha de consulta:** {r['fecha_consulta']}
      199  - **Consulta interpretada por IA:** `{json.dumps(r['consulta']
           , ensure_ascii=False)}`
      200  - **Interpretación:** {tok1['interpretacion']} · tokens usados
           : {tok1['total'] + tok2['total']} (interpretación {tok1['total
           ']}, explicación {tok2['total']}) · explicación {'redactada po
           r IA y revisada' if de_ia else 'de plantilla'}
      201 -""" + (f"- **Motivo del respaldo sin IA:** {tok1['motivo_respa
          -ldo']}                                                        
      202 -" if tok1.get("motivo_respaldo") else ""))                    
      201 +""" + (f"- **Motivo del respaldo sin IA:** {tok1['motivo_respa
          +ldo']}\n" if tok1.get("motivo_respaldo") else ""))            
      202              if f.get("url_api"):
      203                  st.markdown(f"- **API:** {f['url_api']}")
      204          st.markdown(f"**Fuente oficial:** [{f['url']}]({f['url
           ']})")

● Update(app\streamlit_app.py)
  ⎿  Added 1 line, removed 2 lines
      207              st.markdown(f"- **Consulta interpretada por IA:** 
           `{json.dumps(r['consulta'], ensure_ascii=False)}`\n"
      208                          f"- **Motivo:** {r.get('motivo')}\n- *
           *Fecha de consulta:** {r['fecha_consulta']}\n"
      209                          f"- **Interpretación:** {tok1['interpr
           etacion']} · tokens usados: {tok1['total'] + tok2['total']}"
      210 -                        + (f"                                 
      211 -- **Motivo del respaldo sin IA:** {tok1['motivo_respaldo']}"  
      210 +                        + (f"\n- **Motivo del respaldo sin IA:
          +** {tok1['motivo_respaldo']}"                                 
      211                             if tok1.get("motivo_respaldo") else
            ""))
      212          st.info("Fuentes disponibles: BCRP (inflación, PBI, ti
           po de cambio, tasa de referencia, ingresos "
      213                  "tributarios) e INEI ENAHO 2024 (pobreza y pob
           reza extrema).")

● Ahora una prueba de punta a punta sin clave (forzando el respaldo, sin gastar
  tokens) para ver la ficha, la tabla y el mapa:
  Ran 2 shell commands (ctrl+o to expand)

● Todo correcto. Actualizo el README (URL y Python 3.14) y hago commit y push:

● Bash(cd "/c/Users/Antonio Macedo/repos/cifraverificada" && python - <<'EOF'
      from pathlib import Path…)
  ⎿  warning: in the working copy of 'tests/test_despliegue.py', LF will be
      replaced by CRLF the next time Git touches it
     M  README.md
     … +8 lines (ctrl+o to expand)
  ⎿  Updated README.md (+68 -66)
       1 -# CifraVerificada                                              
       2 -                                                               
       3 -> Verificamos en segundos las cifras económicas y sociales del 
         -debate público peruano para periodistas,                       
       4 -> fact-checkers y ONG, contrastándolas con datos oficiales del 
         -BCRP y del INEI mediante un agente de IA.                      
       5 -                                                               
       6 -Proyecto final del diplomado *Data Science con Python* (Issue #
         -204). Proyecto de impacto social, gratuito.                    
       7 -                                                               
       8 -*(README en construcción; la versión completa se publica en la 
         -siguiente entrega.)*                                           
       9 -                                                               
      10 -## Qué hace                                                    
      11 -                                                               
      12 -1. Pegas una afirmación (p. ej., *"La inflación de Lima cerró 2
         -024 en 1.97 %"*).                                              
      13 -2. **Gemini** (`gemini-3.8-flash`, salida JSON con esquema) la 
         -convierte en una consulta estructurada:                        
      14 -   indicador, ámbito, periodo, valor afirmado y unidad.        
      15 -3. **Python** consulta el dato oficial (API del BCRP en vivo, c
         -on snapshot fechado de respaldo, o los                         
      16 -   agregados de la ENAHO 2024 del INEI) y lo compara con una **
         -tolerancia explícita**.                                        
      17 -4. Veredicto: **CORRECTA / APROXIMADA / INCORRECTA / NO VERIFIC
         -ABLE CON ESTAS FUENTES**, con el dato                          
      18 -   oficial, la diferencia, un gráfico o mapa, *La cifra detrás 
         -de la cifra* y una *ficha de trazabilidad*.                    
      19 -                                                               
      20 -El modelo **nunca** calcula cifras: solo interpreta la frase y 
         -redacta la explicación (que se revisa en                       
      21 -Python: si menciona un número que no está en los datos calculad
         -os, se reemplaza por una plantilla).                           
      22 -                                                               
      23 -## Indicadores verificables                                    
      24 -                                                               
      25 -| Indicador | Fuente | Código / método |                       
      26 -|---|---|---|                                                  
      27 -| Inflación Lima Metropolitana (var. % 12 meses) | BCRP | PN012
         -73PM |                                                         
      28 -| Crecimiento del PBI (anual / mensual) | BCRP | PM04863AA / PN
         -01728AM |                                                      
      29 -| Tipo de cambio bancario (S/ por US$) | BCRP | PN01210PM |    
      30 -| Tasa de referencia | BCRP | PD04722MM |                      
      31 -| Ingresos tributarios del gobierno general (% del PBI) | BCRP 
         -| PM05876FA |                                                  
      32 -| Pobreza y pobreza extrema 2024 (nacional, área, sexo, edad, 2
         -5 departamentos) | INEI, ENAHO 2024 | personas ponderadas con `
         -facpob07` |                                                    
      33 -                                                               
      34 -La pobreza nacional calculada es 27.53 % frente al 27.6 % ofici
         -al del INEI (diferencia de método).                            
      35 -El repositorio solo contiene agregados: **ningún microdato**.  
      36 -                                                               
      37 -## Cómo correrla en local                                      
      38 -                                                               
      39 -```bash                                                        
      40 -uv sync                                                        
     … 94 more lines (ctrl+o to expand)

● Hice los 4 ajustes, las pruebas pasan y ya hice el push (commit 5061954).
  Streamlit Cloud debería redesplegar solo en un par de minutos.

  1. README y Python 3.14
  - Cambié "pendiente" por https://cifraverificada.streamlit.app y anoté que la
    nube usa Python 3.14 y en local se desarrolla con 3.12.
  - Riesgo con 3.14: es bajo. Corrí todas las pruebas con 3.14 y pasan las 32, y
    uv.lock tiene versiones compatibles de todos los paquetes. La pantalla
    completa la probé solo con 3.12 en local; con 3.14 lo único probado es que
    la app ya funciona en la nube.
  - Si alguna vez quieres cambiar de versión, en Streamlit Cloud hay que borrar
    la app y volver a desplegarla, así que te recomiendo quedarte con 3.14.

  2. Motivo del respaldo en la ficha
  - Cuando se usan las reglas sin IA, la ficha agrega la línea "Motivo del 
    respaldo sin IA". Puede decir:
    - "Gemini saturado (503)"
    - "cuota agotada (429)"
    - "tiempo agotado (15 s); último error: …"
    - "falta la clave GEMINI_API_KEY en Secrets"
    - "clave inválida o sin permiso (403, …)"
    - "modelo no encontrado (404, …)"
    - en otro caso, el tipo de error y su mensaje recortado
  - La clave nunca se muestra: se borra del mensaje y también cualquier texto
    con forma de clave de Google. Una prueba lo comprueba.
  - Lo probé en local quitando la clave: la ficha mostró "falta la clave
    GEMINI_API_KEY en Secrets".

  3. Mapa: ahora abre con un encuadre fijo que muestra el Perú completo.

  4. Formato: "La cifra detrás de la cifra" ahora sale con 1 o 2 decimales y su
  unidad, por ejemplo "27.53 %", "39.44 %" y "14.7 pp" en la brecha rural −
  urbana. En las series del BCRP se usa la unidad de cada serie, como "S/ por
  US$".

  Pruebas: uv run pytest -q da 32 pasadas. Son 7 más que antes, en
  tests/test_despliegue.py. También hay que decir que en mi primera edición de
  la ficha metí un error de sintaxis; lo encontré al ejecutar la app en local y
  lo corregí antes del commit.

  Cómo probar en la nube: verifica una frase y abre la ficha de trazabilidad. Si
  sigue diciendo "reglas en Python (sin IA)", la línea del motivo dirá por qué;
  pásamela y lo diagnosticamos. Revisa también que el mapa abra con todo el
  país.

✻ Baked for 3m 37s · done 12:22 a.m.

※ recap: CifraVerificada ya está en Streamlit Cloud, y subí los ajustes de la ficha (motivo del respaldo sin IA), el mapa, el formato de las cifras y el README. Tu siguiente paso es verificar una frase en la app pública y mandarme el motivo que muestre la ficha. (disable recaps in /config)