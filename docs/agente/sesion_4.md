 ▐▛███▛█   Claude Code v2.1.322
▝▜██████▀  Opus 5.5 · Claude Pro
 ▝▝   ▝▝   ~\repos\cifraverificada

  Fable 5.2 is here for your longest and toughest coding tasks, and is included in your plan until November 16. It draws down usage faster than Opus 5.5. Switch with /model.

> Hola ccode. Último tramo de CifraVerificada (lee CLAUDE.md y README.md).      
  Entrega HOY a las 23:59 en el Issue #204:                                     
  https://github.com/d2cml-ai/Data-Science-Python/issues/204 (lee de ahí las 9  
  partes del README, el checklist y la rúbrica). Sé eficiente y riguroso;       
  avísame al terminar cada bloque y haz un commit por bloque. Ya probé en la    
  nube: Gemini funciona, el diseño nuevo, "No hay pobres" da INCORRECTA y "No   
  hay democracia" da NO VERIFICABLE con fuentes. ¡Bien!                         
                                                                                
  0. DECISIONES Y AJUSTE: deja el límite de Gemini en 15 s (no lo subas).       
  Corrige la "Fecha de consulta" para que use la hora de Lima (America/Lima):   
  en la nube mostró 2026-11-11 a las 21:00 de Lima. Versiona docs/agente/: son  
  mis exportaciones de las sesiones con Claude Code (míos, sirven para "qué     
  hizo el agente"); revísalas antes buscando claves o tokens (mi nombre en las  
  rutas puede quedar).                                                          
                                                                                
  1. RESEARCH (las 3 conversaciones; vale 3 puntos):                            
  - Mis 3 entrevistados respondieron a estas 5 preguntas: (1) última vez que    
  verificaron una cifra económica o social; (2) cómo lo hicieron, dónde         
  buscaron y cuánto tiempo les tomó; (3) qué fue lo más difícil; (4) si vieron  
  una cifra equivocada o sin fuente; (5) si usarían una herramienta así y quién 
  debería financiarla. Dieron consentimiento para notas ANÓNIMAS.               
  - Archivos en C:\Users\Antonio Macedo\repos\cifraverificada_privado\audios\   
  (FUERA del repo): persona1_a.ogg (audio), persona2_a.ogg y persona2_b.ogg     
  (audios) y persona3_texto.txt (texto; si aparece como persona3_texto.txt.txt, 
  es el mismo).                                                                 
  - Roles: persona1 = estudiante de Comunicaciones para el Desarrollo; persona2 
  = estudiante de Economía; persona3 = estudiante de Comunicación Audiovisual.  
  - Transcribe los audios LOCALMENTE con Whisper (faster-whisper u              
  openai-whisper, como en mi Tarea 2: C:\Users\Antonio                          
  Macedo\repos\Python_Intermedio_2026\tarea_2), en español. Las transcripciones 
  completas se quedan en la carpeta privada, NUNCA en el repo.                  
  - En docs/research/ crea conversacion_1.md, conversacion_2.md y               
  conversacion_3.md: rol (sin nombre), fecha, canal (audio o texto de           
  WhatsApp), consentimiento para notas anónimas, respuesta resumida a cada      
  pregunta con 1-2 citas textuales cortas anonimizadas (borra cualquier nombre, 
  institución identificable o dato personal) y 2-3 hallazgos. Si algo no se     
  entiende, marca [inaudible]: no inventes.                                     
  - docs/research/sintesis.md: patrones comunes y DIFERENCIAS (tiempo que toma  
  verificar, dificultades, quién debería pagar), con citas, y qué cambia o      
  confirma para CifraVerificada. Reporta con honestidad lo que no confirme la   
  hipótesis (por ejemplo, si a alguien le resultó fácil verificar una cifra muy 
  conocida) y qué implica para el foco del producto.                            
                                                                                
  2. README FINAL con las 9 partes del Issue:                                   
  (1) One-liner. (2) Founder: Ricardo Antonio Macedo Villegas, estudiante de    
  Economía y sociólogo por la PUCP, interesado en política fiscal y             
  desigualdad; por qué es la persona indicada (proyectos previos con BCRP,      
  ENAHO y justicia tributaria: link a https://antoniomacedo17.github.io) y cómo 
  cubre producto, ingeniería, diseño y difusión con agentes de IA. (3)          
  Problema: quién lo sufre con precisión, cuánto cuesta (tiempo, errores) y     
  cómo se resuelve hoy, con la evidencia de docs/research/. (4) Solución e      
  insight: "la cifra detrás de la cifra", la trazabilidad visible y la          
  orientación a fuentes oficiales (ONU, CEPAL, PNUD) cuando no hay cifra. (5)   
  Why now: LLM con salida estructurada baratos y APIs abiertas (BCRP,           
  microdatos INEI). (6) Demo: URL https://cifraverificada.streamlit.app, 3      
  capturas del flujo (usa docs/capturas/despues_* o toma nuevas de la app en la 
  nube), diagrama de arquitectura (Mermaid, que GitHub muestra), y qué modelos  
  y APIs se usan y por qué (Gemini 3.8-flash con respaldo flash-lite y          
  respaldo por reglas en 15 s; API del BCRP con snapshot; agregados ENAHO       
  validados; lista curada de fuentes). Deja un espacio "Video de respaldo:      
  (link pendiente)". (7) Modelo de sostenibilidad: proyecto de impacto social;  
  gratis para ciudadanía y periodistas (con límite diario) y planes para        
  instituciones (máximo 3 planes, con precio concreto en soles); costo por      
  verificación calculado con los tokens registrados y el precio OFICIAL vigente 
  de la API de Gemini (búscalo en la página oficial de precios de Google y      
  cita el link y la fecha; si no puedes verificarlo, dilo y no inventes) +      
  costo de servidor (Streamlit Community Cloud, gratis) = margen de             
  contribución. (8) Herramientas del curso y en qué archivo están: LLM con      
  salida estructurada (sesión 08) → ai/; APIs del BCRP reutilizando mi servidor 
  MCP de la Tarea 4 (sesiones 03-04) → app/fuentes.py; mapa coroplético         
  (sesión 06) y dashboard en Streamlit (sesión 05) → app/streamlit_app.py;      
  agregados de la ENAHO producidos con mis Skills de la Tarea 4 (sesión 16) →   
  data/. Explica por qué esas. Menciona aparte que Whisper (sesión 13) se usó   
  en la investigación de usuarios, no dentro del producto. (9) Qué hizo el      
  agente: qué generó Claude Code y qué decidí yo (decisiones clave: respaldo    
  sin IA, límite de 15 s, tolerancias, lista curada de fuentes, paleta), con    
  links a docs/agente/.                                                         
  Opcional breve si da el tiempo: competencia (3-5 alternativas, incluidas "no  
  hacer nada" y "buscar a mano en el INEI/BCRP"), riesgos principales y plan a  
  3 meses.                                                                      
                                                                                
  3. REVISIÓN FINAL: LICENSE, .env.example y .gitignore presentes; ningún       
  audio, transcripción completa, .env ni secreto en el repo (git log -p         
  buscando api_key, secret, token y mi clave real sin imprimirla); links        
  relativos del README funcionando; pruebas en verde.                           
                                                                                
  4. Commit y push. Dime qué falta y escríbeme el comentario de entrega con     
  esta plantilla exacta:                                                        
  Nombre:                                                                       
  Startup y one-liner:                                                          
  Link del demo (URL pública, o "corre en local"):                              
  Link del repo:                                                                
  Herramientas del curso que usa:                                               
  Video de respaldo:                                                            

● Empiezo leyendo el estado del repo, el Issue y los archivos privados.

  Ran 3 shell commands (ctrl+o to expand)

● Arranco la transcripción primero (es lo más lento). Reviso cómo se usó Whisper
  en la Tarea 2.

  Ran 2 shell commands (ctrl+o to expand)

● Uso faster-whisper (el .venv de la Tarea 2) con el modelo large-v3-turbo que
  ya está en caché, en local y en CPU. Las transcripciones se guardan solo en la
  carpeta privada.

  Read 1 file, ran 2 shell commands (ctrl+o to expand)

● Persona 3 dice que le resultó fácil (eso no confirma la hipótesis y lo voy a
  reportar). Mientras transcribe, hago el bloque 0: la fecha de consulta.

  Ran 2 shell commands (ctrl+o to expand)

● Bash(cd "/c/Users/Antonio Macedo/repos/cifraverificada" && python - <<'EOF'
      import re, pathlib…)
  ⎿  app/fuentes.py:15:from datetime import date, datetime
     app/fuentes.py:17:from zoneinfo import ZoneInfo
     app/fuentes.py:34:LIMA = ZoneInfo("America/Lima")
     … +16 lines (ctrl+o to expand)
  ⎿  Updated ai\interpretar.py (+2 -1)
      15  import re
      16  import time
      17  from datetime import datetime
      18 +from zoneinfo import ZoneInfo                                  
      19  from pathlib import Path
      20  
      21  from dotenv import load_dotenv
     ...
      135              w = csv.writer(f)
      136              if nuevo:
      137                  w.writerow(["fecha", "etapa", "modelo", "token
           s_entrada", "tokens_salida", "tokens_total", "frase"])
      137 -            w.writerow([datetime.now().isoformat(timespec="sec
          -onds"), etapa, uso["modelo"], uso["entrada"],                 
      138 +            w.writerow([datetime.now(ZoneInfo("America/Lima"))
          +.isoformat(timespec="seconds"), etapa, uso["modelo"], uso["ent
          +rada"],                                                       
      139                          uso["salida"], uso["total"], frase[:20
           0]])
      140      except OSError:
      141          pass          # en la nube el disco puede ser de solo 
           lectura: el registro no debe romper la app
  ⎿  Updated app\fuentes.py (+201 -183)
        1 -"""Fuentes oficiales de CifraVerificada: API del BCRP (en vivo
          -, con snapshot de respaldo) y ENAHO 2024 agregada.            
        2 -                                                              
        3 -Las funciones `_fecha_api`, `_periodo` y `_pedir_api` vienen d
          -e mi Tarea 4 (Python_Intermedio_2026/tarea_4/mcp/             
        4 -server.py, servidor MCP del BCRP basado en la Sesión 04), adap
          -tadas: sin FastMCP, sin el catálogo de 7 MB (los              
        5 -metadatos de las 6 series usadas están en SERIES) y sin caché 
          -en disco (la app usa st.cache_data).                          
        6 -                                                              
        7 -Regenerar el snapshot (cuando se quiera actualizar el respaldo
          -):                                                            
        8 -    uv run python -m app.fuentes                              
        9 -"""                                                           
       10 -import calendar                                               
       11 -import json                                                   
       12 -import math                                                   
       13 -import re                                                     
       14 -import time                                                   
       15 -from datetime import date                                     
       16 -from pathlib import Path                                      
       17 -                                                              
       18 -import httpx                                                  
       19 -import pandas as pd                                           
       20 -                                                              
       21 -RAIZ = Path(__file__).resolve().parents[1]                    
       22 -DATA = RAIZ / "data"                                          
       23 -SNAPSHOT = DATA / "bcrp_snapshot.json"                        
       24 -ENAHO = DATA / "enaho2024_indicadores.csv"                    
       25 -GEOJSON = DATA / "peru_departamental_simple.geojson"          
       26 -                                                              
       27 -API = "https://estadisticas.bcrp.gob.pe/estadisticas/series/ap
          -i"                                                            
       28 -WEB = "https://estadisticas.bcrp.gob.pe/estadisticas/series"  
       29 -WEB_FRECUENCIA = {"diaria": "diarias", "mensual": "mensuales",
          - "trimestral": "trimestrales", "anual": "anuales"}            
       30 -URL_ENAHO = "https://proyectos.inei.gob.pe/microdatos/"       
       31 -REINTENTOS = 3                                                
       32 -ESPERA_BASE = 1.0                                             
       33 -MESES = {"ene": 1, "feb": 2, "mar": 3, "abr": 4, "may": 5, "ju
          -n": 6, "jul": 7, "ago": 8,                                    
       34 -         "sep": 9, "set": 9, "oct": 10, "nov": 11, "dic": 12} 
       35 -                                                              
       36 -# Metadatos tomados del catálogo oficial del BCRP (estadistica
          -s/series/metadata). Ventana: desde -> hasta.                  
       37 -SERIES = {                                                    
       38 -    "PN01273PM": {"nombre": "Índice de precios Lima Metropolit
          -ana (var% 12 meses) - IPC", "frecuencia": "Mensual",          
       39 -                  "unidad": "%", "fuente_primaria": "INEI", "d
          -esde": "2015-01", "hasta": "2025-12"},                        
       40 -    "PM04863AA": {"nombre": "Producto bruto interno (variación
          - porcentual real anual)", "frecuencia": "Anual",              
     … 344 more lines (ctrl+o to expand)
  ⎿  Updated app\verificador.py (+3 -5)
      10  Para "mayor_que"/"menor_que" ("más del 20 %") se compara el dat
          o oficial con el umbral; para "maximo"/"minimo"
      11  ("el departamento más pobre") se ordena el indicador entre los 
          25 departamentos.
      12  """
      13 -from datetime import date                                      
      14 -                                                               
      13  import pandas as pd
      14  
      15  from app import fuentes
     ...
      73  
      74  def _no_verificable(consulta: dict, motivo: str) -> dict:
      75      return {"veredicto": NO_VERIFICABLE, "motivo": motivo, "con
          sulta": consulta,
      78 -            "fecha_consulta": date.today().isoformat()}        
      76 +            "fecha_consulta": fuentes.fecha_consulta()}        
      77  
      78  
      79  # -------------------------------------------------------------
          -------------------------------------------------
     ...
      130             "fuente": {"tipo": "BCRP", "codigo": codigo, "nombr
           e": serie["nombre"], "origen": serie["origen"],
      131                        "fecha_datos": serie["fecha_datos"], "av
           iso": serie["aviso"], "url": serie["url_web"],
      132                        "url_api": serie["url_api"], "fuente_pri
           maria": serie["fuente_primaria"]},
      135 -           "serie": s, "fecha_consulta": date.today().isoforma
          -t()}                                                          
      133 +           "serie": s, "fecha_consulta": fuentes.fecha_consult
          +a()}                                                          
      134      res.update(_comparar(consulta, oficial, meta["tol"]))
      135      res["detras"] = _detras_bcrp(consulta["indicador"], s, per
           _usado, oficial, serie["unidad"])
      136      return res
     ...
      190                "nombre": meta["etiqueta"], "origen": "agregados
            validados en data/enaho2024_indicadores.csv",
      191                "fecha_datos": "2024 (anual)", "aviso": None, "u
           rl": fuentes.URL_ENAHO}
      192      base = {"indicador": meta["etiqueta"], "consulta": consult
           a, "periodo_usado": "2024", "unidad": "%",
      195 -            "fuente": fuente, "fecha_consulta": date.today().i
          -soformat(), "enaho": df, "columna": col,                      
      193 +            "fuente": fuente, "fecha_consulta": fuentes.fecha_
          +consulta(), "enaho": df, "columna": col,                      
      194              "detras": _detras_enaho(df, col)}
      195      tipo = consulta.get("tipo") or "valor"
      196  

● Bash(cd "/c/Users/Antonio Macedo/repos/cifraverificada" && sed -i 's/^from
      datetime import date, datetime$/from datetime import datetime/'
      app/fuentes.py && cat >> t…)
  ⎿  ............................................................
        [100%]
     60 passed in 8.37s
  ⎿  Updated tests\test_despliegue.py (+12 -0)
      58      r2 = verificar({"indicador": "tipo_cambio", "periodo": "202
          4", "tipo": "valor", "valor_afirmado": 3.75,
      59                      "unidad": "S/ por US$"}, en_vivo=False)
      60      assert all(d["unidad"] == "S/ por US$" for d in r2["detras"
          ])
      61 +                                                               
      62 +                                                               
      63 +def test_fecha_de_consulta_en_hora_de_lima():                  
      64 +    """En la nube el servidor corre en UTC: a las 21:00 de Lima
         + ya es el día siguiente en UTC."""                             
      65 +    from datetime import datetime, timedelta, timezone         
      66 +                                                               
      67 +    from app import fuentes                                    
      68 +    texto = fuentes.fecha_consulta()                           
      69 +    assert texto.endswith("(hora de Lima)")                    
      70 +    lima = datetime.now(timezone(timedelta(hours=-5)))  # Perú 
         +no usa horario de verano                                       
      71 +    assert texto.startswith(lima.strftime("%Y-%m-%d"))         
      72 +    assert fuentes.hoy_lima() == lima.date().isoformat()       
  ⎿  … 1 more file changed

● Pruebas en verde (60). Ahora reviso docs/agente/ en busca de claves antes de
  versionarlo.

  Ran 1 shell command (ctrl+o to expand)

● Ningún patrón de clave. Compruebo también contra tu clave real del .env (sin
  imprimirla) y busco correos u otros datos personales.

  Ran 1 shell command (ctrl+o to expand)

● Limpio. Commit del bloque 0 (dos commits: código y exportaciones).

  Ran 1 shell command (ctrl+o to expand)

● Bloque 0 quedó listo: la fecha de consulta usa hora de Lima, las 60 pruebas
  pasan, docs/agente/ no contiene claves y hice 2 commits. Ahora busco el precio
  oficial de Gemini mientras Whisper transcribe. · summary

  Ran 1 shell command (ctrl+o to expand)

● Web Search("Gemini API pricing gemini-3.8-flash gemini-3.1-flash-lite per 1M
            tokens ai.google.dev pricing")
  ⎿  Did 1 search in 5s

● Verifico las cifras directamente en la página oficial de precios.

● web-fetch(Verify Gemini official pricing)
  ⎿  Received 148 bytes

› Message from web-fetch
  Report on Gemini API pricing (Paid tier, Standard tab only; figures in USD per
  1M tokens)

  Source: the original URL https://ai.google.dev/gemini-api/docs/pricing
  returned HTTP 301 to https://aistudio.google.com/docs/pricing. I read the
  redirect target, which is the same pricing page. Its text was truncated, so I
  read the rest with a second call at offset 39947. I read the whole page
  verbatim except for a middle stretch; the Gemini 3.8 Flash and 3.1 Flash-Lite
  sections are fully covered.

  (a) Gemini 3.8 Flash (gemini-3.8-flash), Standard tab, verbatim:
  - Input price: "$0.75 through December 31, 2026." then "$1.50 starting January
  1, 2027." (text input; the page does not split text from other modalities for
  this model)
  - Output price: label "(including thinking tokens)"; "$3.75 through December
  31, 2026." then "$7.50 starting January 1, 2027." So output does include
  thinking tokens.
  - Context caching: "$0.075 through December 31, 2026." then "$0.15 starting
  January 1, 2027." Storage: "$0.50 / 1,000,000 tokens per hour (storage price)
  through December 31, 2026." then "$1.00 / 1,000,000 tokens per hour (storage
  price) starting January 1, 2027."
  - Promotional/intro pricing: the page does not use the word "promotional". The
  lower figures apply "through December 31, 2026", and the higher figures apply
  "starting January 1, 2027". So the post-promo price is $1.50 input and $7.50
  output.
  - Free tier: input "Free of charge", output "Free of charge", context caching
  "Free of charge". Grounding with Google Search is "Not available" on the free
  tier. "Used to improve our products" is "Yes" on the free tier and "No" on
  paid.
  - The page lists this model under the heading "## Gemini 3.8 Flash", separate
  from its Batch, Flex, and Priority tabs. The Standard tab figures are above.

  (b) Gemini 3.1 Flash-Lite (gemini-3.1-flash-lite), Standard tab, verbatim:
  - Input price: "$0.25 (text / image / video)" and "$0.50 (audio)"
  - Output price: label "(including thinking tokens)"; "$1.50"
  - Context caching: "$0.025 (text / image / video)" and "$0.05 (audio)", plus
  "$1.00 / 1,000,000 tokens per hour (storage price)"
  - Free tier: input "Free of charge", output "Free of charge". Context caching
  "Not available" on free tier. Grounding with Google Search "Not available" on
  free tier. "Used to improve our products" is "Yes" on free tier.

  Free tier conditions (page-wide): the Free card says "Limited access to
  certain models", "Free input & output tokens", "Google AI Studio access", and
  "Content used to improve our products". The page does not state rate or volume
  limits for the free tier in the text I read.

  Last updated date: not shown in any part of the page I read.

  Caveat about a model-extracted summary: the tool returned a model-written
  summary of the parts it did not show verbatim. That summary said the page has
  no Gemini 3.8 Flash section and gave a Gemini 3.1 Flash-Lite input price that
  differed from the verbatim figure. Both statements are wrong. The verbatim
  text does contain the 3.8 Flash section and the Flash-Lite prices above, so I
  used the verbatim text.

  Final URLs read: https://ai.google.dev/gemini-api/docs/pricing (301, not
  followed), https://aistudio.google.com/docs/pricing (200, read in two parts,
  with offset 39947).

  No figures in this report came from memory or from the summary.

● Precios confirmados en la página oficial. Ahora mido los tokens actuales con
  algunas llamadas reales: el prompt creció desde el 9/11 y la muestra
  registrada tiene solo 5 llamadas.

  Ran 4 shell commands (ctrl+o to expand)

● Medición lista: 8 de 10 llamadas cayeron al respaldo flash-lite y 2 usaron
  reglas sin IA. Ahora tomo el tipo de cambio del BCRP para pasar los costos a
  soles. · summary

  Ran 3 shell commands (ctrl+o to expand)

● Mientras Whisper termina, reúno los datos del README: cómo se generaron los
  agregados de la ENAHO y qué hay en el repo de tu sitio.

  Read 1 file, ran 1 shell command (ctrl+o to expand)

● Background command "Transcribe interview audios locally with faster-whisper"
completed (exit code 0)

  Ran 1 shell command (ctrl+o to expand)

● Las transcripciones están listas y se quedan solo en
  cifraverificada_privado/transcripciones/, fuera del repo. Escribo las notas
  anonimizadas.

● Write(docs\research\conversacion_1.md)
  ⎿  Wrote 54 lines to docs\research\conversacion_1.md
      1 # Conversación 1 · Estudiante de Comunicaciones para el Desarroll
        o
      2 
      3 | | |
      4 |---|---|
      5 | **Rol** | Estudiante universitaria/o de Comunicaciones para el 
        Desarrollo (sin nombre, por acuerdo) |
      6 | **Fecha** | Noviembre de 2026 (semana del 5 al 10) |
      7 | **Canal** | Nota de voz de WhatsApp (1 audio, 4 min 35 s) |
      8 | **Consentimiento** | Sí, para tomar notas **anónimas** |
     … +46 lines (ctrl+o to expand)
● Write(docs\research\conversacion_2.md)
  ⎿  Wrote 47 lines to docs\research\conversacion_2.md
      1 # Conversación 2 · Estudiante de Economía
      2 
      3 | | |
      4 |---|---|
      5 | **Rol** | Estudiante universitaria/o de Economía (sin nombre, p
        or acuerdo) |
      6 | **Fecha** | Noviembre de 2026 (semana del 5 al 10) |
      7 | **Canal** | Notas de voz de WhatsApp (2 audios, 1 min 18 s y 1 
        min 16 s) |
      8 | **Consentimiento** | Sí, para tomar notas **anónimas** |
     … +39 lines (ctrl+o to expand)

● Write(docs\research\conversacion_3.md)
  ⎿  Wrote 39 lines to docs\research\conversacion_3.md
       1 # Conversación 3 · Estudiante de Comunicación Audiovisual
       2 
       3 | | |
       4 |---|---|
       5 | **Rol** | Estudiante universitaria/o de Comunicación Audiovisu
         al (sin nombre, por acuerdo) |
       6 | **Fecha** | Noviembre de 2026 (semana del 5 al 10) |
       7 | **Canal** | Texto por WhatsApp (respuestas escritas a las 5 pr
         eguntas) |
       8 | **Consentimiento** | Sí, para tomar notas **anónimas** |
     … +31 lines (ctrl+o to expand)

● Write(docs\research\sintesis.md)
  ⎿  Wrote 70 lines to docs\research\sintesis.md
       1 # Síntesis de las 3 conversaciones
       2 
       3 Tres estudiantes universitarios de Lima, entrevistados por Whats
         App en noviembre de 2026 con las mismas 5
       4 preguntas (notas anónimas, con consentimiento):
       5 
       6 | | Rol | Canal |
       7 |---|---|---|
       8 | [Conversación 1](conversacion_1.md) | Comunicaciones para el D
         esarrollo | Audio |
     … +62 lines (ctrl+o to expand)

● Bash(cd "/c/Users/Antonio Macedo/repos/cifraverificada" && sed -i 's/Tres
      estudiantes universitarios de Lima, entrevistados/Tres estudiantes
      universitarios, entrevis…)
  ⎿  warning: in the working copy of 'docs/research/conversacion_1.md', LF
     will be replaced by CRLF the next time Git touches it
     warning: in the working copy of 'docs/research/conversacion_2.md', LF
     … +7 lines (ctrl+o to expand)
  ⎿  Deleted docs\research\.gitkeep (+0 -0)
  ⎿  Updated docs\research\sintesis.md (+1 -1)
      1  # Síntesis de las 3 conversaciones
      2  
      3 -Tres estudiantes universitarios de Lima, entrevistados por Whats
        -App en noviembre de 2026 con las mismas 5                       
      3 +Tres estudiantes universitarios, entrevistados por WhatsApp en n
        +oviembre de 2026 con las mismas 5                               
      4  preguntas (notas anónimas, con consentimiento):
      5  
      6  | | Rol | Canal |

● Bloque 1 listo: el commit tiene 3 notas anonimizadas y la síntesis. Ahora el
  README. Antes confirmo quién decidió las tolerancias, para no atribuírtelas
  sin respaldo.

  Ran 2 shell commands (ctrl+o to expand)

● Escribo el README final con las 9 partes.

● Write(README.md)
  ⎿  Added 325 lines, removed 54 lines
        1  # CifraVerificada
        2  
        3 -> Verificamos en segundos las cifras económicas y sociales del
          - debate público peruano para periodistas,                     
        4 -> fact-checkers y ONG, contrastándolas con datos oficiales del
          - BCRP y del INEI mediante un agente de IA.                    
        3 +> **Verificamos en segundos las cifras económicas y sociales d
          +el debate público peruano para periodistas,                   
        4 +> fact-checkers y ONG, contrastándolas con datos oficiales del
          + BCRP y del INEI mediante un agente de IA.**                  
        5  
        6 -Proyecto final del diplomado *Data Science con Python* (Issue 
          -#204). Proyecto de impacto social, gratuito.                  
        6 +**Demo:** https://cifraverificada.streamlit.app · Proyecto fin
          +al de la Diplomatura de Ciencia de Datos para las             
        7 +Ciencias Sociales y la Gestión Pública (Q-Lab PUCP), [Issue #2
          +04](https://github.com/d2cml-ai/Data-Science-Python/issues/204
          +).                                                            
        8 +Proyecto de impacto social, gratuito para la ciudadanía.      
        9  
        8 -*(README en construcción; la versión completa se publica en la
          - siguiente entrega.)*                                         
       10 +**Contenido:** [1. One-liner](#1-one-liner) · [2. Founder](#2-
          +founder) · [3. Problema](#3-problema) ·                       
       11 +[4. Solución e insight](#4-solución-e-insight) · [5. Why now](
          +#5-why-now) · [6. Demo](#6-demo) ·                            
       12 +[7. Modelo de sostenibilidad](#7-modelo-de-sostenibilidad) · [
          +8. Herramientas del curso](#8-herramientas-del-curso) ·       
       13 +[9. Qué hizo el agente](#9-qué-hizo-el-agente) · [Competencia,
          + riesgos y plan](#competencia-riesgos-y-plan-a-3-meses) ·     
       14 +[Cómo correrla](#cómo-correrla-en-local)                      
       15  
       10 -## Qué hace                                                   
       16 +---                                                           
       17  
       12 -1. Pegas una afirmación (p. ej., *"La inflación de Lima cerró 
          -2024 en 1.97 %"*).                                            
       13 -2. **Gemini** (`gemini-3.8-flash`, salida JSON con esquema) la
          - convierte en una consulta estructurada:                      
       14 -   indicador, ámbito, periodo, valor afirmado y unidad.       
       15 -3. **Python** consulta el dato oficial (API del BCRP en vivo, 
          -con snapshot fechado de respaldo, o los                       
       16 -   agregados de la ENAHO 2024 del INEI) y lo compara con una *
          -*tolerancia explícita**.                                      
       17 -4. Veredicto: **CORRECTA / APROXIMADA / INCORRECTA / NO VERIFI
          -CABLE CON ESTAS FUENTES**, con el dato                        
       18 -   oficial, la diferencia, un gráfico o mapa, *La cifra detrás
          - de la cifra* y una *ficha de trazabilidad*.                  
       18 +## 1. One-liner                                               
       19  
       20 -El modelo **nunca** calcula cifras: solo interpreta la frase y
          - redacta la explicación (que se revisa en                     
       21 -Python: si menciona un número que no está en los datos calcula
          -dos, se reemplaza por una plantilla).                         
       20 +**Hacemos** la verificación de cifras económicas y sociales **
          +para** periodistas, fact-checkers, ONG y                      
       21 +estudiantes que publican sobre el Perú, **mediante** una IA qu
          +e solo interpreta la frase, y un motor en Python              
       22 +que la contrasta con la serie oficial del BCRP o con la ENAHO 
          +del INEI y muestra el veredicto, la fuente y lo               
       23 +que el promedio esconde.                                      
       24  
       23 -## Indicadores verificables                                   
       25 +## 2. Founder                                                 
       26  
       25 -| Indicador | Fuente | Código / método |                      
       27 +**Ricardo Antonio Macedo Villegas.** Estudiante de Economía y 
          +sociólogo por la PUCP, interesado en política                 
       28 +fiscal y desigualdad.                                         
       29 +                                                              
       30 +**Por qué soy la persona indicada.** Ya trabajé con las mismas
          + fuentes que usa el producto:                                 
       31 +                                                              
       32 +- **BCRP:** construí un servidor MCP que consulta la API de se
          +ries estadísticas del BCRP (Tarea 4). Sus                     
       33 +  funciones son la base de [`app/fuentes.py`](app/fuentes.py).
       34 +- **ENAHO:** con mis *Skills* de Claude Code (limpiar, grafica
          +r y mapear la ENAHO) calculé la pobreza 2024                  
       35 +  ponderada con `facpob07`. De ahí salen los agregados de [`da
          +ta/`](data/).                                                 
       36 +- **Justicia tributaria:** proyectos sobre recaudación y desig
          +ualdad, de donde viene el "modo fiscal"                       
       37 +  (ingresos tributarios como % del PBI).                      
       38 +- Portafolio: **https://antoniomacedo17.github.io**           
       39 +                                                              
       40 +Como sociólogo y economista sé qué cifras se discuten, cuáles 
          +se distorsionan y por qué un promedio puede                   
       41 +ocultar una brecha. Eso define el producto más que el código. 
       42 +                                                              
       43 +**Cómo cubro los cuatro roles con agentes de IA:**            
       44 +                                                              
       45 +| Rol | Qué hago yo | Qué hace el agente |                    
       46  |---|---|---|
       27 -| Inflación Lima Metropolitana (var. % 12 meses) | BCRP | PN01
          -273PM |                                                       
       28 -| Crecimiento del PBI (anual / mensual) | BCRP | PM04863AA / P
          -N01728AM |                                                    
       29 -| Tipo de cambio bancario (S/ por US$) | BCRP | PN01210PM |   
       30 -| Tasa de referencia | BCRP | PD04722MM |                     
       31 -| Ingresos tributarios del gobierno general (% del PBI) | BCRP
          - | PM05876FA |                                                
       32 -| Pobreza y pobreza extrema 2024 (nacional, área, sexo, edad, 
          -25 departamentos) | INEI, ENAHO 2024 | personas ponderadas con
          - `facpob07` |                                                 
       47 +| Producto | Elijo el problema, entrevisto a usuarios, defino 
          +reglas y veredictos | Ordena la evidencia y redacta borradores
          + |                                                            
       48 +| Ingeniería | Reviso el código, decido arquitectura, respaldo
          +s y límites | Escribe el código y las pruebas (Claude Code) | 
       49 +| Diseño | Defino la paleta y el tono institucional | Implemen
          +ta el tema y toma capturas para comparar |                    
       50 +| Difusión | Presentación, redes, alianzas con universidades |
          + Borradores de textos que reviso |                            
       51  
       34 -**Frases sin cifra explícita.** Las negaciones se leen como un
          -a cifra implícita (*"ya no hay pobres"*,                      
       35 -*"la pobreza desapareció"* → 0 %; *"la mayoría de peruanos es 
          -pobre"* → más del 50 %) y se contrastan con la                
       36 -ENAHO; la ficha muestra la expresión usada. Si el tema no tien
          -e indicador (democracia, corrupción, educación,               
       37 -salud, empleo…), el veredicto es *NO VERIFICABLE CON ESTAS FUE
          -NTES* y se sugieren 2-4 fuentes oficiales de una              
       38 -**lista fija y curada** (`data/fuentes_orientacion.json`, prio
          -ridad al sistema de la ONU: CEPAL, PNUD, ONU/ODS,             
       39 -OMS, UNESCO, UNODC, UNICEF; luego INEI, BCRP y MEF). La IA sol
          -o elige el tema; los enlaces los pone Python.                 
       40 -Re-verificar los enlaces: `uv run python -m app.orientacion` (
          -solo se incluyen los que responden HTTP 200).                 
       52 +## 3. Problema                                                
       53  
       42 -La pobreza nacional calculada es 27.53 % frente al 27.6 % ofic
          -ial del INEI (diferencia de método).                          
       43 -El repositorio solo contiene agregados: **ningún microdato**. 
       54 +**Quién lo sufre.** Quien **publica** cifras sobre el Perú con
          + poco tiempo para revisarlas: redacciones                     
       55 +digitales, fact-checkers, ONG, comunicadores y estudiantes que
          + producen contenido (podcasts, ensayos, posts).               
       56 +Y quien los lee, porque las cifras erradas circulan. Las [3 co
          +nversaciones](docs/research/sintesis.md)                      
       57 +coinciden en dónde aparecen: los tres entrevistados vieron cif
          +ras equivocadas o sin fuente en **redes                       
       58 +sociales, medios digitales y blogs**.                         
       59  
       60 +**Cuánto cuesta.** Depende de qué tan específica es la cifra: 
       61 +                                                              
       62 +| Caso | Tiempo reportado | Fuente |                          
       63 +|---|---|---|                                                 
       64 +| Cifra de titular (pobreza nacional) | "un par de minutos" | 
          +[Conversación 3](docs/research/conversacion_3.md) |           
       65 +| Verificación rigurosa de una cifra conocida | 30 s (básico) 
          +a 5 min (riguroso) | [Conversación 2](docs/research/conversaci
          +on_2.md) |                                                    
       66 +| Dato de un tema puntual (El Niño, seguridad) | 30-40 min o m
          +ás | [Conversación 1](docs/research/conversacion_1.md) |      
       67 +                                                              
       68 +A esto se suma el costo de **equivocarse**: datos desactualiza
          +dos, enlaces que "cuando le doy clic no existe"               
       69 +(C1) y no llegar a la fuente original, "que no es un blog o al
          +go así" (C2).                                                 
       70 +                                                              
       71 +**Cómo se resuelve hoy.** Con Google y, cada vez más, con la *
          +*respuesta de IA del buscador**: C2 empieza por               
       72 +"lo que me dice Gemini" y solo abre la fuente si no le convenc
          +e. Para más rigor se va a mano al BCRP o al INEI.             
       73 +                                                              
       74 +**Lo que no confirmó la investigación.** Para la cifra más con
          +ocida (pobreza nacional), verificar **es fácil**              
       75 +(C3). El valor de CifraVerificada no está en repetir el titula
          +r, sino en el dato específico, la trazabilidad y              
       76 +el contexto. Detalle en la [síntesis](docs/research/sintesis.m
          +d). Límite: entrevisté a tres estudiantes, no a               
       77 +periodistas en ejercicio.                                     
       78 +                                                              
       79 +## 4. Solución e insight                                      
       80 +                                                              
       81 +Pegas una afirmación ("La pobreza en el Perú llegó a 20 % en 2
          +024") y en segundos obtienes:                                 
       82 +                                                              
       83 +1. **Veredicto:** CORRECTA / APROXIMADA / INCORRECTA / NO VERI
          +FICABLE CON ESTAS FUENTES, con una                            
       84 +   **tolerancia explícita** (ver [`app/verificador.py`](app/ve
          +rificador.py)).                                               
       85 +2. **Dato oficial, diferencia y gráfico o mapa** por departame
          +nto.                                                          
       86 +3. **"La cifra detrás de la cifra"** (el insight): lo que el p
          +romedio esconde, calculado de los mismos datos.               
       87 +   Pobreza nacional 27.53 %, pero rural 39.44 %, niñez de 0 a 
          +14 años 37.52 % y Cajamarca 44.99 % frente a                  
       88 +   Ica 5.91 % (ENAHO 2024, `facpob07`). Son contrastes descrip
          +tivos: **asociación no es causalidad**.                       
       89 +4. **Ficha de trazabilidad visible:** código de serie del BCRP
          + (o fuente ENAHO y factor `facpob07`), periodo,               
       90 +   URL, tolerancia, fecha y hora de consulta (hora de Lima), s
          +i el dato vino de la API en vivo o del snapshot               
       91 +   fechado, qué modelo interpretó la frase y cuántos tokens us
          +ó.                                                            
       92 +5. **Orientación cuando no hay cifra:** "En el Perú no hay dem
          +ocracia" da NO VERIFICABLE y sugiere 2-4                      
       93 +   **fuentes oficiales de una lista curada** ([`data/fuentes_o
          +rientacion.json`](data/fuentes_orientacion.json)),            
       94 +   priorizando el sistema de la ONU (CEPAL, PNUD, ONU/ODS, OMS
          +, UNESCO…). Python pone los enlaces, verificados              
       95 +   uno por uno; la IA solo elige el tema.                     
       96 +                                                              
       97 +**La regla que lo hace confiable:** el modelo **nunca** escrib
          +e una cifra. Interpreta la frase y redacta la                 
       98 +explicación. Si esa explicación menciona un número que no está
          + en los datos calculados por Python, se                       
       99 +reemplaza por una plantilla. Esto lo diferencia de la respuest
          +a de IA de un buscador.                                       
      100 +                                                              
      101 +Frases sin cifra explícita: "ya no hay pobres" se lee como 0 %
          + y "la mayoría de peruanos es pobre" como más                 
      102 +del 50 %, y se contrastan con la ENAHO.                       
      103 +                                                              
      104 +## 5. Why now                                                 
      105 +                                                              
      106 +- **LLM baratos con salida estructurada:** hoy un modelo devue
          +lve un JSON validado con esquema (indicador,                  
      107 +  ámbito, periodo, valor, unidad) por menos de **S/ 0.002 por 
          +verificación** (ver §7). Hace tres años esto era              
      108 +  caro, lento y poco fiable para el español peruano, y había q
          +ue escribir reglas para cada forma de decir una               
      109 +  cifra.                                                      
      110 +- **Datos oficiales abiertos y consultables por código:** la A
          +PI de series del BCRP responde en JSON sin clave              
      111 +  y los microdatos de la ENAHO del INEI son descargables. Con 
          +agentes de programación, una persona procesa la               
      112 +  ENAHO y conecta la API en días.                             
      113 +- **Más desinformación numérica:** las cifras circulan en rede
          +s y medios digitales sin tiempo de verificación               
      114 +  (lo dicen los tres entrevistados), y la respuesta de IA de l
          +os buscadores no garantiza que la cifra salga de              
      115 +  la serie oficial.                                           
      116 +                                                              
      117 +## 6. Demo                                                    
      118 +                                                              
      119 +**URL pública:** **https://cifraverificada.streamlit.app** (St
          +reamlit Community Cloud).                                     
      120 +**Video de respaldo:** (link pendiente)                       
      121 +                                                              
      122 +### Capturas del flujo                                        
      123 +                                                              
      124 +| 1. Inicio: ejemplos y frase | 2. Veredicto, mapa y cifra det
          +rás de la cifra | 3. Sin indicador: orientación a fuentes ofic
          +iales |                                                       
      125 +|---|---|---|                                                 
      126 +| ![Inicio](docs/capturas/despues_escritorio_inicio.png) | ![P
          +obreza](docs/capturas/despues_escritorio_pobreza.png) | ![Orie
          +ntación](docs/capturas/despues_escritorio_orientacion.png) |  
      127 +                                                              
      128 +Otras capturas (versión de celular, cifra implícita y el diseñ
          +o anterior) en [`docs/capturas/`](docs/capturas/).            
      129 +                                                              
      130 +### Arquitectura                                              
      131 +                                                              
      132 +```mermaid                                                    
      133 +flowchart LR                                                  
      134 +    U["Usuario: pega una afirmación"] --> I{"Interpretación<br
          +/>(15 s en total)"}                                           
      135 +    I -->|"1.º"| G1["Gemini 3.8 Flash<br/>JSON con esquema"]  
      136 +    I -->|"si 429/5xx o tiempo"| G2["Gemini 3.1 Flash-Lite"]  
      137 +    I -->|"si nada respondió"| R["Reglas en Python<br/>(sin IA
          +)"]                                                           
      138 +    G1 & G2 & R --> C["Consulta estructurada<br/>indicador · á
          +mbito · periodo · valor · unidad"]                            
      139 +    C --> V["Motor de verificación (Python)<br/>tolerancia exp
          +lícita"]                                                      
      140 +    B["API del BCRP<br/>(en vivo)"] --> V                     
      141 +    S["Snapshot fechado<br/>data/bcrp_snapshot.json"] -.->|"si
          + la API falla"| V                                             
      142 +    E["ENAHO 2024 agregada<br/>data/enaho2024_indicadores.csv"
          +] --> V                                                       
      143 +    V --> O["Veredicto · dato oficial · gráfico o mapa<br/>cif
          +ra detrás de la cifra · ficha de trazabilidad"]               
      144 +    V -->|"sin indicador"| F["Lista curada de fuentes oficiale
          +s<br/>data/fuentes_orientacion.json"]                         
      145 +    O --> X["Gemini redacta la explicación<br/>(se descarta si
          + inventa un número)"]                                         
      146 +```                                                           
      147 +                                                              
      148 +### Modelos y APIs, y por qué                                 
      149 +                                                              
      150 +| Componente | Qué es | Por qué |                             
      151 +|---|---|---|                                                 
      152 +| **Gemini 3.8 Flash** (`gemini-3.8-flash`) | Interpreta la fr
          +ase en JSON con esquema (Pydantic) y redacta la explicación | 
          +Salida estructurada fiable y barata; lo usé en la Tarea 2 |   
      153 +| **Gemini 3.1 Flash-Lite** (`gemini-3.1-flash-lite`) | Respal
          +do automático ante 429/500/503/504 o tiempo agotado | Más bara
          +to y disponible cuando el principal está saturado |           
      154 +| **Reglas en Python** ([`ai/reglas.py`](ai/reglas.py)) | Resp
          +aldo sin IA si en **15 s** nadie respondió | Que la demo nunca
          + se quede esperando; la ficha dice "reglas en Python (sin IA)"
          + y el motivo |                                                
      155 +| **API del BCRP** + snapshot fechado | 6 series: inflación de
          + Lima, PBI anual y mensual, tipo de cambio, tasa de referencia
          +, ingresos tributarios (% del PBI) | Fuente oficial abierta; s
          +i no responde se usa el snapshot y se muestra su fecha |      
      156 +| **ENAHO 2024** (agregados validados) | Pobreza y pobreza ext
          +rema por área, sexo, edad y 25 departamentos, ponderadas con `
          +facpob07` | El repo no contiene microdatos. La pobreza naciona
          +l calculada es 27.53 % frente al 27.6 % oficial del INEI (dife
          +rencia de método) |                                           
      157 +| **Lista curada de fuentes** | 2-4 enlaces oficiales por tema
          + (ONU, CEPAL, PNUD, INEI, BCRP, MEF) | Los enlaces no los gene
          +ra la IA; se re-verifican con `uv run python -m app.orientacio
          +n` |                                                          
      158 +                                                              
      159 +## 7. Modelo de sostenibilidad                                
      160 +                                                              
      161 +Es un **proyecto de impacto social**: gratis para quien verifi
          +ca y financiado por instituciones. Las                        
      162 +conversaciones lo respaldan: nadie propuso que pague el usuari
          +o final, los tres señalaron a **universidades**               
      163 +con apoyo del **Estado**, y una persona pidió **varias fuentes
          +** de financiamiento para cuidar la                           
      164 +independencia ([síntesis](docs/research/sintesis.md)).        
      165 +                                                              
      166 +### Planes (precios en soles)                                 
      167 +                                                              
      168 +| Plan | Para quién | Precio | Incluye |                      
      169 +|---|---|---|---|                                             
      170 +| **Ciudadanía** | Ciudadanía, periodistas, estudiantes | **S/
          + 0** | 20 verificaciones al día por usuario |                 
      171 +| **Equipo** | Redacciones, fact-checkers y ONG | **S/ 150 al 
          +mes** | 3,000 verificaciones al mes, fichas exportables, sopor
          +te |                                                          
      172 +| **Institucional** | Universidades, centros de investigación,
          + entidades públicas | **S/ 900 al mes** | 15,000 verificacione
          +s al mes, uso en aulas, indicadores nuevos a pedido |         
      173 +                                                              
      174 +### Costo por verificación (tokens medidos + precio oficial)  
      175 +                                                              
      176 +**Tokens medidos:** el 10 de noviembre de 2026 verifiqué 10 fr
          +ases en vivo con la app (registro local                       
      177 +`data/registro_tokens.csv`, que no se versiona). En 8 respondi
          +ó Gemini y en 2 entraron las reglas sin IA,                   
      178 +porque nadie respondió en 15 s. Las 8 respuestas vinieron del 
          +respaldo `gemini-3.1-flash-lite`: el modelo                   
      179 +principal no respondió a tiempo esa noche. Promedio por verifi
          +cación con IA:                                                
      180 +                                                              
      181 +| Etapa | Tokens de entrada | Tokens de salida |              
      182 +|---|---:|---:|                                               
      183 +| Interpretar la frase | 881 | 78 |                           
      184 +| Redactar la explicación | 277 | 66 |                        
      185 +| **Total** | **1,158** | **144** |                           
      186 +                                                              
      187 +**Precio oficial** (nivel pago estándar, USD por millón de tok
          +ens; la salida incluye los tokens de                          
      188 +razonamiento), según la [página oficial de precios de la API d
          +e Gemini](https://ai.google.dev/gemini-api/docs/pricing)      
      189 +consultada el **10 de noviembre de 2026** (la página no muestr
          +a fecha de actualización):                                    
      190 +                                                              
      191 +| Modelo | Entrada | Salida |                                 
      192 +|---|---:|---:|                                               
      193 +| `gemini-3.1-flash-lite` | USD 0.25 | USD 1.50 |             
      194 +| `gemini-3.8-flash` | USD 0.75 hasta el 31/12/2026; **USD 1.5
          +0** desde el 1/1/2027 | USD 3.75 hasta el 31/12/2026; **USD 7.
          +50** desde el 1/1/2027 |                                      
      195 +                                                              
      196 +**Costo por verificación**, con el tipo de cambio de S/ 3.367 
          +por US$ (BCRP, serie PN01210PM, diciembre de                  
      197 +2025, del snapshot del repositorio):                          
      198 +                                                              
      199 +| Escenario | USD | Soles | Por 1,000 verificaciones |        
      200 +|---|---:|---:|---:|                                          
      201 +| **Medido** (flash-lite, tokens de arriba) | 0.00051 | **S/ 0
          +.0017** | S/ 1.70 |                                           
      202 +| **Techo** (supuesto: todo con 3.8 Flash a precio 2027, redon
          +deado a 1,200 de entrada y 1,000 de salida por los tokens de r
          +azonamiento) | 0.0093 | **S/ 0.031** | S/ 31.31 |             
      203 +                                                              
      204 +El techo es un supuesto conservador, no una medición. La única
          + llamada registrada con 3.8 Flash (9/11, con un               
      205 +prompt más corto) usó 551 de entrada y 362 de salida con razon
          +amiento, solo para interpretar.                               
      206 +                                                              
      207 +**Servidor:** Streamlit Community Cloud, **S/ 0**. La API del 
          +BCRP y los agregados de la ENAHO son gratuitos.               
      208 +                                                              
      209 +### Margen de contribución mensual                            
      210 +                                                              
      211 +| Plan | Ingreso | Costo medido | Margen medido | Costo techo 
          +| Margen techo |                                              
      212 +|---|---:|---:|---:|---:|---:|                                
      213 +| Equipo (3,000 verificaciones) | S/ 150 | S/ 5.11 | **S/ 144.
          +89 (97 %)** | S/ 93.93 | **S/ 56.07 (37 %)** |                
      214 +| Institucional (15,000 verificaciones) | S/ 900 | S/ 25.56 | 
          +**S/ 874.44 (97 %)** | S/ 469.66 | **S/ 430.34 (48 %)** |     
      215 +                                                              
      216 +Al costo medido, el margen de un solo plan Equipo paga unas **
          +85,000 verificaciones gratuitas** al mes. Como                
      217 +la API de Gemini es de pago, en producción se fija un **tope d
          +e gasto** mensual en la cuenta de facturación, y              
      218 +el límite diario del plan gratuito evita abusos.              
      219 +                                                              
      220 +## 8. Herramientas del curso                                  
      221 +                                                              
      222 +Dentro del producto:                                          
      223 +                                                              
      224 +| Herramienta (sesión) | Archivo | Por qué esta |             
      225 +|---|---|---|                                                 
      226 +| **LLM con salida estructurada** (08) | [`ai/interpretar.py`]
          +(ai/interpretar.py) (y respaldo en [`ai/reglas.py`](ai/reglas.
          +py)) | Convertir lenguaje natural en una consulta con esquema 
          +es justo lo que un LLM hace bien. El esquema impide que el mod
          +elo devuelva cifras propias |                                 
      227 +| **APIs del BCRP**, reutilizando las funciones de mi servidor
          + **MCP** de la Tarea 4 (03-04) | [`app/fuentes.py`](app/fuente
          +s.py) | La fuente oficial de las series macro. Reutilicé códig
          +o probado (fechas, periodos, reintentos) en lugar de escribirl
          +o otra vez |                                                  
      228 +| **Mapa coroplético** (06) y **dashboard en Streamlit** (05) 
          +| [`app/streamlit_app.py`](app/streamlit_app.py) | El mapa por
          + departamento hace visible "la cifra detrás de la cifra". Stre
          +amlit permite desplegar gratis en una URL pública |           
      229 +| **Agregados de la ENAHO** producidos con mis **Skills** de l
          +a Tarea 4 (16) | [`data/enaho2024_indicadores.csv`](data/enaho
          +2024_indicadores.csv) | Los Skills (limpiar, graficar y mapear
          + la ENAHO) ya validaban la pobreza con `facpob07`. El producto
          + solo usa agregados, sin microdatos |                         
      230 +                                                              
      231 +Fuera del producto: **Whisper** (sesión 13) sirvió para la **i
          +nvestigación de usuarios**. Transcribí las                    
      232 +entrevistas en local con `faster-whisper` (large-v3-turbo), si
          +n enviar los audios a ningún servicio. Las                    
      233 +transcripciones completas no están en el repositorio, solo las
          + [notas anónimas](docs/research/).                            
      234 +                                                              
      235 +## 9. Qué hizo el agente                                      
      236 +                                                              
      237 +El código lo escribió **Claude Code** en tres sesiones, con in
          +strucciones mías en cada bloque. Las sesiones                 
      238 +exportadas están en [`docs/agente/`](docs/agente/):           
      239 +[sesión 1](docs/agente/sesion_1.md) (estructura, datos, motor,
          + Gemini, app y respaldo sin IA),                              
      240 +[sesión 2](docs/agente/sesion_2.md) (despliegue y diagnóstico 
          +en la nube),                                                  
      241 +[sesión 3](docs/agente/sesion_3.md) (cliente de Gemini en Pyth
          +on 3.14, frases sin cifra, orientación y                      
      242 +rediseño). Esta última sesión (README, research y revisión fin
          +al) también la hizo Claude Code.                              
      243 +                                                              
      244 +**Qué generó Claude Code:** la estructura del repo; la adaptac
          +ión de las funciones del BCRP de mi Tarea 4; el               
      245 +motor de verificación y sus tolerancias; el intérprete con esq
          +uema JSON y el registro de tokens; las reglas de              
      246 +respaldo; la interfaz en Streamlit (gráficos, mapa, ficha, CSS
          +); 61 pruebas en pytest; el snapshot; las                     
      247 +capturas antes y después; la transcripción local con Whisper; 
          +y los borradores de las notas de investigación,               
      248 +la síntesis y este README.                                    
      249 +                                                              
      250 +**Qué decidí yo:**                                            
      251 +                                                              
      252 +- **El problema, el one-liner y los tres sellos:** "la cifra d
          +etrás de la cifra", el modo fiscal (ingresos                  
      253 +  tributarios) y la ficha de trazabilidad.                    
      254 +- **La regla central:** el LLM solo interpreta y redacta; ning
          +una cifra sale del modelo ([`CLAUDE.md`](CLAUDE.md)).         
      255 +- **El respaldo sin IA** y sus condiciones: solo si Gemini fal
          +la, que la ficha diga "reglas en Python (sin IA)"             
      256 +  y el motivo, y que nunca invente.                           
      257 +- **El límite de 15 s** para pasar a las reglas. Lo mantuve en
          + 15 s a pesar de que el modelo principal a veces              
      258 +  tarda más.                                                  
      259 +- **Los modelos:** Gemini 3.8 Flash (de mi Tarea 2), con respa
          +ldo Flash-Lite aprobado el 9/11.                              
      260 +- **Las tolerancias:** que fueran explícitas y visibles en cad
          +a veredicto. Los umbrales concretos (0.1 y                    
      261 +  0.5 pp, 10 % relativo) los propuso el agente y yo los aprobé
          +.                                                             
      262 +- **La lista curada de fuentes** para frases sin indicador, co
          +n prioridad a la ONU, sin enlaces generados por               
      263 +  la IA.                                                      
      264 +- **La paleta institucional** marfil, azul y rojo, tomada de m
          +i sitio web y de mi Tarea 3.                                  
      265 +- **La investigación:** las 5 preguntas, las 3 entrevistas, el
          + consentimiento y la revisión de las notas.                   
      266 +                                                              
      267 +## Competencia, riesgos y plan a 3 meses                      
      268 +                                                              
      269 +**Competencia y alternativas**                                
      270 +                                                              
      271 +| Alternativa | Fortaleza | Limitación frente a CifraVerificad
          +a |                                                           
      272 +|---|---|---|                                                 
      273 +| No hacer nada (publicar sin verificar) | Cero tiempo | Es de
          + donde salen las cifras erradas que vieron los tres entrevista
          +dos |                                                         
      274 +| Buscar a mano en el INEI o el BCRP | Fuente primaria | De se
          +gundos a 40 minutos o más, enlaces caídos, sin desglose inmedi
          +ato |                                                         
      275 +| Respuesta de IA del buscador (Gemini, etc.) | Inmediata y gr
          +atuita | La cifra la escribe un modelo; no hay código de serie
          + ni tolerancia |                                              
      276 +| Fact-checkers profesionales | Rigor y contexto | Revisan poc
          +as frases, con días de trabajo |                              
      277 +| Portales oficiales (BCRPData, INEI) | Datos completos | Requ
          +ieren saber qué serie buscar; no responden a una frase |      
      278 +                                                              
      279 +**Riesgos principales**                                       
      280 +                                                              
      281 +1. **Disponibilidad de Gemini:** el modelo principal se satura
          + (503). Mitigación: respaldo Flash-Lite, reglas               
      282 +   en Python en 15 s y motivo visible en la ficha.            
      283 +2. **Cobertura limitada:** hoy hay 6 series del BCRP y la pobr
          +eza de la ENAHO. Fuera de eso, el veredicto es                
      284 +   NO VERIFICABLE más orientación.                            
      285 +3. **Datos que envejecen:** la ENAHO es anual y la API del BCR
          +P puede caerse. Mitigación: snapshot fechado y                
      286 +   fecha siempre visible.                                     
      287 +4. **Que se lea como causalidad o como verdad absoluta:** avis
          +o de verificación automática y regla de                       
      288 +   "asociación ≠ causalidad".                                 
      289 +5. **Costo si sube el uso o el precio (enero de 2027):** límit
          +e diario gratuito y tope de gasto.                            
      290 +                                                              
      291 +**Plan a 3 meses**                                            
      292 +                                                              
      293 +- **Mes 1:** conversar con 5 redacciones o fact-checkers perua
          +nos (el usuario que faltó en esta                             
      294 +  investigación) y medir cuántas cifras verifican por semana. 
      295 +- **Mes 2:** más indicadores desagregados (empleo e ingresos d
          +e la ENAHO, ejecución del gasto del MEF) y                    
      296 +  exportar la ficha a PDF.                                    
      297 +- **Mes 3:** piloto con una universidad (plan Institucional) e
          +n cursos de periodismo y economía; buscar fondos              
      298 +  de cooperación para el plan gratuito.                       
      299 +                                                              
      300 +---                                                           
      301 +                                                              
      302  ## Cómo correrla en local
      303  
      304  ```bash
      305  uv sync
       49 -cp .env.example .env        # y escribe tu GEMINI_API_KEY     
      306 +cp .env.example .env           # y escribe tu GEMINI_API_KEY  
      307  uv run streamlit run app/streamlit_app.py
       51 -uv run pytest -q            # pruebas del motor (sin red ni LL
          -M)                                                            
      308 +uv run pytest -q               # pruebas (sin red ni LLM)     
      309  uv run python -m app.fuentes   # (opcional) actualizar el snap
           shot del BCRP
      310  ```
      311  
       55 -## Despliegue (Streamlit Community Cloud)                     
      312 +Sin clave de Gemini la app funciona igual con las reglas en Py
          +thon (sin IA), y la ficha lo indica.                          
      313  
       57 -- **URL pública:** https://cifraverificada.streamlit.app      
       58 -- Repo `AntonioMacedo17/cifraverificada`, rama `main`, archivo
          - `app/streamlit_app.py`.                                      
       59 -- **Python:** la nube corre con **3.14** (según el log de desp
          -liegue); en local se desarrolla con 3.12. Las pruebas pasan en
          - ambas versiones (`uv run --isolated --python 3.14 --with pyte
          -st pytest -q`).                                               
       60 -- Si la ficha de trazabilidad dice "reglas en Python (sin IA)"
          -, la línea *Motivo del respaldo sin IA* indica la causa (503, 
          -429, tiempo agotado, falta la clave en Secrets u otro error co
          -n su tipo).                                                   
       61 -- `.streamlit/config.toml` desactiva la vigilancia de archivos
          - (`fileWatcherType = "none"`): al recargar tras un            
       62 -  push, Streamlit sacaba el paquete `app` de `sys.modules` mie
          -ntras otra sesión lo importaba (`KeyError: 'app'`).           
       63 -  Si tras un push la app no se actualiza, usar *Reboot app* en
          - el panel de la nube.                                         
       64 -- Gemini: un intento de 10 s con `gemini-3.8-flash`; si da 429
          -/500/503/504 o se agota, `gemini-3.1-flash-lite`              
       65 -  (la API rechaza plazos menores a 10 s). No se inicia un inte
          -nto pasados 15 s; luego, reglas en Python.                    
       66 -- La clave va en *Settings → Secrets* como `GEMINI_API_KEY = "
          -..."` (nunca en el repositorio).                              
       67 -- Dependencias: `uv.lock` (y `requirements.txt`, exportado del
          - mismo lock con `uv export`).                                 
       68 -- En la nube `data/registro_tokens.csv` no persiste entre rein
          -icios; si la API del BCRP no responde se                      
       69 -  usa el snapshot de `data/` y se muestra su fecha.           
      314 +### Indicadores verificables                                  
      315  
       71 -## Estructura                                                 
      316 +| Indicador | Fuente | Código / método |                      
      317 +|---|---|---|                                                 
      318 +| Inflación Lima Metropolitana (var. % 12 meses) | BCRP | PN01
          +273PM |                                                       
      319 +| Crecimiento del PBI (anual / mensual) | BCRP | PM04863AA / P
          +N01728AM |                                                    
      320 +| Tipo de cambio bancario (S/ por US$) | BCRP | PN01210PM |   
      321 +| Tasa de referencia | BCRP | PD04722MM |                     
      322 +| Ingresos tributarios del gobierno general (% del PBI) | BCRP
          + | PM05876FA |                                                
      323 +| Pobreza y pobreza extrema 2024 (nacional, área, sexo, edad, 
          +25 departamentos) | INEI, ENAHO 2024 | personas ponderadas con
          + `facpob07` |                                                 
      324  
      325 +**Tolerancias** (diferencia = afirmado − oficial): CORRECTA si
          + |diferencia| ≤ 0.1 pp o media unidad del último              
      326 +decimal afirmado ("20 %" acepta 19.5-20.5); APROXIMADA si ≤ 0.
          +5 pp o 10 % del valor oficial; INCORRECTA en otro             
      327 +caso. Para el tipo de cambio: 0.01, 0.05 y 2 %. Detalle en [`a
          +pp/verificador.py`](app/verificador.py).                      
      328 +                                                              
      329 +### Despliegue (Streamlit Community Cloud)                    
      330 +                                                              
      331 +- Repo `AntonioMacedo17/cifraverificada`, rama `main`, archivo
          + `app/streamlit_app.py`. La nube corre con                    
      332 +  Python 3.14; en local se desarrolla con 3.12, y las pruebas 
          +pasan en ambas versiones.                                     
      333 +- La clave va en *Settings → Secrets* como `GEMINI_API_KEY = "
          +..."`, nunca en el repositorio.                               
      334 +- Gemini: un intento de 10 s con `gemini-3.8-flash` y, si da 4
          +29/500/503/504 o se agota, `gemini-3.1-flash-lite`            
      335 +  (la API rechaza plazos menores a 10 s). No se inicia un inte
          +nto pasados 15 s; después entran las reglas en                
      336 +  Python.                                                     
      337 +- Las fechas se muestran en hora de Lima (`America/Lima`): el 
          +servidor corre en UTC.                                        
      338 +- `.streamlit/config.toml` desactiva la vigilancia de archivos
          + (evita un `KeyError: 'app'` al recargar). Si                 
      339 +  tras un push la app no se actualiza, usar *Reboot app*.     
      340 +- Dependencias: `uv.lock` y `requirements.txt` (exportado del 
          +mismo lock con `uv export`).                                  
      341 +                                                              
      342 +### Estructura                                                
      343 +                                                              
      344  ```
       74 -app/    streamlit_app.py (interfaz), verificador.py (comparaci
          -ón y tolerancias), fuentes.py (BCRP + ENAHO)                  
       75 -ai/     interpretar.py (Gemini: consulta estructurada y explic
          -ación; registro de tokens)                                    
       76 -data/   bcrp_snapshot.json, enaho2024_indicadores.csv, peru_de
          -partamental_simple.geojson                                    
       77 -tests/  test_verificador.py (6 afirmaciones con veredicto espe
          -rado)                                                         
       78 -docs/   documentación y docs/research/                        
      345 +app/    streamlit_app.py (interfaz), verificador.py (toleranci
          +as), fuentes.py (BCRP + ENAHO), orientacion.py                
      346 +ai/     interpretar.py (Gemini, esquema JSON, tokens), reglas.
          +py (respaldo sin IA)                                          
      347 +data/   bcrp_snapshot.json, enaho2024_indicadores.csv, fuentes
          +_orientacion.json, geojson departamental                      
      348 +tests/  pruebas del motor, reglas, frases sin cifra, cliente d
          +e Gemini y despliegue                                         
      349 +docs/   research/ (3 conversaciones y síntesis), agente/ (sesi
          +ones con Claude Code), capturas/                              
      350  ```
      351  
       81 -Licencia MIT (cubre el código; los datos pertenecen al BCRP y 
          -al INEI).                                                     
      352 +Licencia [MIT](LICENSE): cubre el código. Los datos pertenecen
          + al BCRP y al INEI.                                           

● Bash(cd "/c/Users/Antonio Macedo/repos/cifraverificada" && sed -i 's/61
      pruebas en pytest/60 pruebas en pytest/; s/3,000 verificaciones al mes,
      fichas exportables, s…)
  ⎿  OK  app/fuentes.py
     OK  data/
     OK  docs/research/sintesis.md
     … +27 lines (ctrl+o to expand)
  ⎿  Updated README.md (+2 -2)
      168  | Plan | Para quién | Precio | Incluye |
      169  |---|---|---|---|
      170  | **Ciudadanía** | Ciudadanía, periodistas, estudiantes | **S/
            0** | 20 verificaciones al día por usuario |
      171 -| **Equipo** | Redacciones, fact-checkers y ONG | **S/ 150 al 
          -mes** | 3,000 verificaciones al mes, fichas exportables, sopor
          -te |                                                          
      171 +| **Equipo** | Redacciones, fact-checkers y ONG | **S/ 150 al 
          +mes** | 3,000 verificaciones al mes, soporte y fichas exportab
          +les (en desarrollo) |                                         
      172  | **Institucional** | Universidades, centros de investigación,
            entidades públicas | **S/ 900 al mes** | 15,000 verificacione
           s al mes, uso en aulas, indicadores nuevos a pedido |
      173  
      174  ### Costo por verificación (tokens medidos + precio oficial)
     ...
      243  
      244  **Qué generó Claude Code:** la estructura del repo; la adaptac
           ión de las funciones del BCRP de mi Tarea 4; el
      245  motor de verificación y sus tolerancias; el intérprete con esq
           uema JSON y el registro de tokens; las reglas de
      246 -respaldo; la interfaz en Streamlit (gráficos, mapa, ficha, CSS
          -); 61 pruebas en pytest; el snapshot; las                     
      246 +respaldo; la interfaz en Streamlit (gráficos, mapa, ficha, CSS
          +); 60 pruebas en pytest; el snapshot; las                     
      247  capturas antes y después; la transcripción local con Whisper; 
           y los borradores de las notas de investigación,
      248  la síntesis y este README.
      249  

● Los links relativos funcionan y las 60 pruebas pasan. Commit del README.

  Ran 1 shell command (ctrl+o to expand)

● Bloque 2 listo (README con commit). Hago la revisión final de secretos en todo
  el historial.

  Ran 4 shell commands (ctrl+o to expand)

● Es una clave falsa de prueba (contiene "FALSA" y "prueba") y no coincide con
  tu clave real. El historial está limpio. Hago el push.

  Pushed to main (ctrl+o to expand)

● Terminé los 4 bloques. Hice 5 commits (fecha en hora de Lima, docs/agente/,
  research, README y LICENSE sin cambios) y el push a main funcionó. Las 60
  pruebas pasan.

  Bloque 0 · Ajustes
  - La "Fecha de consulta" ahora usa la hora de Lima y se muestra así:
    "2026-11-10 21:00 (hora de Lima)". Lo mismo vale para el snapshot y el
    registro de tokens. Agregué una prueba que lo comprueba.
  - El límite de Gemini sigue en 15 s.
  - docs/agente/ ya está versionado. Lo revisé contra patrones de clave y contra
    tu clave real del .env sin imprimirla: no tiene ninguna.

  Bloque 1 · Research
  - Transcribí los audios en local con faster-whisper. Las transcripciones
    completas están solo en C:\Users\Antonio 
    Macedo\repos\cifraverificada_privado\transcripciones\.
  - docs/research/ tiene las 3 notas anonimizadas y sintesis.md.
  - Lo que no confirma la hipótesis: la persona 3 encontró la pobreza nacional
    en "un par de minutos", y la persona 2 tarda entre 30 s y 5 min, empezando
    por la respuesta de Gemini en Google.
  - Lo que cambia para el producto: el foco pasa al dato específico, a "la cifra
    detrás de la cifra" y a la trazabilidad. Solo la persona 1, con temas
    puntuales, tardó de 30 a 40 minutos o más.
  - Quién debería pagar: los tres pusieron a la universidad, con el Estado como
    apoyo.
  - Límite de la muestra: son tres estudiantes, ningún periodista. Lo dejé dicho
    en la síntesis.

  Bloque 2 · README
  - Tiene las 9 partes, el diagrama Mermaid, 3 capturas y la sección opcional
    (competencia, riesgos y plan a 3 meses).
  - Precio oficial de Gemini (https://ai.google.dev/gemini-api/docs/pricing,
    consultado hoy): flash-lite cuesta USD 0.25 por millón de tokens de entrada
    y USD 1.50 de salida. 3.8-flash cuesta USD 0.75 y USD 3.75 hasta el
    31/12/2026, y USD 1.50 y USD 7.50 desde enero de 2027.
  - Costo por verificación: medido, S/ 0.0017. En el escenario techo, que es un
    supuesto y así está marcado, S/ 0.031.
  - Planes: S/ 0 para ciudadanía, S/ 150 al mes (Equipo) y S/ 900 al mes
    (Institucional).

  Bloque 3 · Revisión final
  - LICENSE, .env.example y .gitignore están presentes, y los 28 links relativos
    del README funcionan.
  - En todo el historial no hay ninguna coincidencia con tu clave real, ni
    audios, transcripciones o .env.
  - La única cadena con formato de clave es la clave falsa de una prueba (dice
    "FALSA" y "prueba").

  Riesgo para la demo: hoy medí 10 frases en vivo.
  - gemini-3.8-flash no respondió en ninguna a tiempo.
  - 8 frases las interpretó flash-lite y 2 pasaron a las reglas sin IA.
  - Cada verificación completa tardó entre 10 y 24 s.

  Ensaya con eso en mente: el veredicto sale igual, pero puede tardar.

  Qué falta (lo tienes que hacer tú):
  1. Video de respaldo: el README dice "(link pendiente)".
  2. Fechas de las entrevistas: puse "semana del 5 al 10 de noviembre" sin dato
     que lo respalde. Corrígelas si las sabes.
  3. Tolerancias: en la parte 9 escribí que tú exigiste que fueran explícitas y
     que los umbrales concretos los propuso el agente y tú los aprobaste. En las
     sesiones exportadas no encontré que tú hayas fijado los números. Ajusta la
     frase si no fue así.
  4. Comprobar en la nube: que la app se redesplegó y que la fecha sale con la
     hora de Lima. Si no se actualiza, usa Reboot app.
  5. Commits en varios días: solo hay commits del 9 y del 10. Un commit mañana
     antes de presentar (por ejemplo, el link del video) suma un tercer día.
  6. Ensayo de 3 minutos con cronómetro.

  Comentario de entrega:

  Nombre: Ricardo Antonio Macedo Villegas
  Startup y one-liner: CifraVerificada — Verificamos en segundos las cifras 
  económicas y sociales del debate público peruano para periodistas, 
  fact-checkers y ONG, contrastándolas con datos oficiales del BCRP y del INEI 
  mediante un agente de IA.
  Link del demo (URL pública, o "corre en local"): 
  https://cifraverificada.streamlit.app
  Link del repo: https://github.com/AntonioMacedo17/cifraverificada
  Herramientas del curso que usa: LLM con salida estructurada (sesión 08, Gemini
  con esquema JSON: ai/); API del BCRP reutilizando las funciones de mi 
  servidor MCP de la Tarea 4 (sesiones 03-04: app/fuentes.py); mapa coroplético 
  y dashboard en Streamlit (sesiones 06 y 05: app/streamlit_app.py); agregados 
  de la ENAHO 2024 producidos con mis Skills de Claude Code (sesión 16: data/). 
  Whisper (sesión 13) se usó en la investigación de usuarios, no dentro del 
  producto.
  Video de respaldo: (link pendiente)

  Fuentes:
  - Gemini Developer API pricing (https://ai.google.dev/gemini-api/docs/pricing)
  - Gemini 3.8 Flash
    (https://ai.google.dev/gemini-api/docs/models/gemini-3.8-flash)

✻ Baked for 11m 24s · done 9:28 p.m.

※ recap: Estamos cerrando la entrega de CifraVerificada para el Issue #204: los 4 bloques están listos y subidos, y el comentario de entrega ya está escrito. Lo siguiente es que grabes el video de respaldo y pongas su link en el README y en el comentario. (disable recaps in /config)

> Correcciones: (1) Las 3 conversaciones fueron el 10 de noviembre de 2026      
  (mensajes enviados y respondidos por WhatsApp ese mismo día): corrige la      
  fecha en las notas, la síntesis y el README. (2) La frase de las tolerancias  
  está bien: el agente propuso los umbrales y yo los revisé y aprobé. Commit y  
  push. En unos minutos te paso el link del video.                              

  Ran 1 shell command (ctrl+o to expand)

● Bash(cd "/c/Users/Antonio Macedo/repos/cifraverificada" && sed -i 's/|
      \*\*Fecha\*\* | Noviembre de 2026 (semana del 5 al 10) |/| **Fecha** | 10
      de noviembre de 2026…)
  ⎿  docs/research/conversacion_1.md:6:| **Fecha** | 10 de noviembre de 202
     6 (preguntas enviadas y respondidas por WhatsApp ese mismo día) |
     docs/research/conversacion_2.md:6:| **Fecha** | 10 de noviembre de 202
     … +22 lines (ctrl+o to expand)
  ⎿  Updated README.md (+1 -1)
      53  
      54  **Quién lo sufre.** Quien **publica** cifras sobre el Perú con 
          poco tiempo para revisarlas: redacciones
      55  digitales, fact-checkers, ONG, comunicadores y estudiantes que 
          producen contenido (podcasts, ensayos, posts).
      56 -Y quien los lee, porque las cifras erradas circulan. Las [3 con
         -versaciones](docs/research/sintesis.md)                        
      56 +Y quien los lee, porque las cifras erradas circulan. Las [3 con
         +versaciones](docs/research/sintesis.md) (10 de noviembre de 202
         +6, por WhatsApp)                                               
      57  coinciden en dónde aparecen: los tres entrevistados vieron cifr
          as equivocadas o sin fuente en **redes
      58  sociales, medios digitales y blogs**.
      59  
  ⎿  Updated docs\research\conversacion_1.md (+1 -1)
      3  | | |
      4  |---|---|
      5  | **Rol** | Estudiante universitaria/o de Comunicaciones para el
          Desarrollo (sin nombre, por acuerdo) |
      6 -| **Fecha** | Noviembre de 2026 (semana del 5 al 10) |          
      6 +| **Fecha** | 10 de noviembre de 2026 (preguntas enviadas y resp
        +ondidas por WhatsApp ese mismo día) |                           
      7  | **Canal** | Nota de voz de WhatsApp (1 audio, 4 min 35 s) |
      8  | **Consentimiento** | Sí, para tomar notas **anónimas** |
      9  | **Método** | Transcripción local con Whisper (`faster-whisper`
          large-v3-turbo, en español, sin enviar el audio a ningún servic
         io). La transcripción completa y el audio quedan fuera del repos
         itorio. |
  ⎿  Updated docs\research\conversacion_2.md (+1 -1)
      3  | | |
      4  |---|---|
      5  | **Rol** | Estudiante universitaria/o de Economía (sin nombre, 
         por acuerdo) |
      6 -| **Fecha** | Noviembre de 2026 (semana del 5 al 10) |          
      6 +| **Fecha** | 10 de noviembre de 2026 (preguntas enviadas y resp
        +ondidas por WhatsApp ese mismo día) |                           
      7  | **Canal** | Notas de voz de WhatsApp (2 audios, 1 min 18 s y 1
          min 16 s) |
      8  | **Consentimiento** | Sí, para tomar notas **anónimas** |
      9  | **Método** | Transcripción local con Whisper (`faster-whisper`
          large-v3-turbo, en español, sin enviar el audio a ningún servic
         io). La transcripción completa y los audios quedan fuera del rep
         ositorio. |
  ⎿  Updated docs\research\conversacion_3.md (+1 -1)
      3  | | |
      4  |---|---|
      5  | **Rol** | Estudiante universitaria/o de Comunicación Audiovisu
         al (sin nombre, por acuerdo) |
      6 -| **Fecha** | Noviembre de 2026 (semana del 5 al 10) |          
      6 +| **Fecha** | 10 de noviembre de 2026 (preguntas enviadas y resp
        +ondidas por WhatsApp ese mismo día) |                           
      7  | **Canal** | Texto por WhatsApp (respuestas escritas a las 5 pr
         eguntas) |
      8  | **Consentimiento** | Sí, para tomar notas **anónimas** |
      9  
  ⎿  Updated docs\research\sintesis.md (+1 -1)
      1  # Síntesis de las 3 conversaciones
      2  
      3 -Tres estudiantes universitarios, entrevistados por WhatsApp en n
        -oviembre de 2026 con las mismas 5                               
      3 +Tres estudiantes universitarios, entrevistados por WhatsApp el 1
        +0 de noviembre de 2026 con las mismas 5                         
      4  preguntas (notas anónimas, con consentimiento):
      5  
      6  | | Rol | Canal |

● Corregí la fecha y ya está en GitHub (commit f8aa213).

  - Fecha: las 3 notas dicen ahora "10 de noviembre de 2026 (preguntas enviadas
    y respondidas por WhatsApp ese mismo día)". La síntesis y la sección
    Problema del README dicen 10 de noviembre de 2026, por WhatsApp.
  - Tolerancias: la frase queda como está.

  Cuando me pases el link del video, lo pongo en el README en lugar de "(link
  pendiente)", hago commit y push, y te devuelvo el comentario de entrega con el
  link. Si ese commit es mañana, ya cuenta como tercer día de commits.

✻ Baked for 16s · done 10:17 p.m.

※ recap: Estamos cerrando la entrega de CifraVerificada para el Issue #204: el research, el README y la fecha de las conversaciones ya están corregidos y en GitHub. Falta que me pases el link del video para ponerlo en el README y completar el comentario de entrega. (disable recaps in /config)

> Video de respaldo listo (76 s, no listado en YouTube):                        
  https://youtu.be/HsRFOuhdgI4. Agrégalo al README en la sección Demo, en lugar 
  de "(link pendiente)". Commit y push, y dame el comentario de entrega final   
  con el link del video.                                                        

● Bash(cd "/c/Users/Antonio Macedo/repos/cifraverificada" && grep -n "link
      pendiente" README.md && sed -i 's|\*\*Video de respaldo:\*\* (link
      pendiente)|**Video de res…)
  ⎿  120:**Video de respaldo:** (link pendiente)
     120:**Video de respaldo (76 s):** https://youtu.be/HsRFOuhdgI4
     warning: in the working copy of 'README.md', LF will be replaced by CR
     … +2 lines (ctrl+o to expand)
  ⎿  Updated README.md (+1 -1)
      117  ## 6. Demo
      118  
      119  **URL pública:** **https://cifraverificada.streamlit.app** (St
           reamlit Community Cloud).
      120 -**Video de respaldo:** (link pendiente)                       
      120 +**Video de respaldo (76 s):** https://youtu.be/HsRFOuhdgI4    
      121  
      122  ### Capturas del flujo
      123  

● Agregué el link del video a la sección Demo del README, en lugar de "(link
  pendiente)". El cambio ya está en GitHub (commit e4d959c).

  Comentario de entrega final:

  Nombre: Ricardo Antonio Macedo Villegas
  Startup y one-liner: CifraVerificada — Verificamos en segundos las cifras 
  económicas y sociales del debate público peruano para periodistas, 
  fact-checkers y ONG, contrastándolas con datos oficiales del BCRP y del INEI 
  mediante un agente de IA.
  Link del demo (URL pública, o "corre en local"): 
  https://cifraverificada.streamlit.app
  Link del repo: https://github.com/AntonioMacedo17/cifraverificada
  Herramientas del curso que usa: LLM con salida estructurada (sesión 08, Gemini
  con esquema JSON: ai/); API del BCRP reutilizando las funciones de mi 
  servidor MCP de la Tarea 4 (sesiones 03-04: app/fuentes.py); mapa coroplético 
  y dashboard en Streamlit (sesiones 06 y 05: app/streamlit_app.py); agregados 
  de la ENAHO 2024 producidos con mis Skills de Claude Code (sesión 16: data/). 
  Whisper (sesión 13) se usó en la investigación de usuarios, no dentro del 
  producto.
  Video de respaldo: https://youtu.be/HsRFOuhdgI4

  Antes de las 23:59 te queda:
  1. Publicar el comentario en el Issue #204.
  2. Comprobar que el video abre en una ventana de incógnito: si es "no
     listado", cualquiera con el link puede verlo.
  3. Ensayar los 3 minutos con cronómetro, tomando en cuenta que cada
     verificación puede tardar hasta unos 24 s.

✻ Baked for 12s · done 10:55 p.m.

※ recap: Estás cerrando la entrega de CifraVerificada para el Issue #204: el README, la investigación, el link del video y el push ya están listos. Lo siguiente es publicar el comentario de entrega en el Issue antes de las 23:59. (disable recaps in /config)