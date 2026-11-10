# Registro de pruebas · 9 de noviembre de 2026

## Pruebas automáticas (`uv run pytest -q`)
9 pruebas aprobadas: 6 afirmaciones con veredicto esperado (2 CORRECTA, 2 INCORRECTA, 1 APROXIMADA,
1 NO VERIFICABLE), calculado desde el snapshot del BCRP y los agregados de la ENAHO 2024, más 3 pruebas
del método (cifras oficiales, periodo fuera de la ENAHO, media unidad de redondeo).

## Interfaz (AppTest de Streamlit, con la API del BCRP en vivo)
Los 6 casos se muestran sin excepciones: tarjeta con el veredicto esperado, métricas, gráfico o mapa,
"La cifra detrás de la cifra" y ficha de trazabilidad.

## Gemini en vivo
`gemini-3.8-flash` respondió 503 ("high demand") en la mayoría de las llamadas de esta tarde. Se agregó un
respaldo automático con `gemini-3.1-flash-lite`. Interpretaciones obtenidas (todas correctas):

| Afirmación | Consulta | Veredicto |
|---|---|---|
| La pobreza en el Perú llegó a 20 % en 2024 | pobreza · nacional · 2024 · valor 20 | INCORRECTA (oficial 27.53) |
| Cajamarca es el departamento más pobre | pobreza · Cajamarca · máximo | CORRECTA (44.99, puesto 1/25) |
| La pobreza rural es de 40 % | pobreza · rural · valor 40 | APROXIMADA (oficial 39.44) |

Tokens por llamada (registro local `data/registro_tokens.csv`, 5 llamadas): interpretar ≈ 605 con
3.1-flash-lite y 913 con 3.8-flash (incluye tokens de razonamiento); explicar ≈ 223. Muestra pequeña:
repetir con más consultas para el costo por usuario.
