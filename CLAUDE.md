# Reglas del proyecto · CifraVerificada

Valen para cualquier sesión de Claude Code abierta en este repositorio.

1. **Ninguna cifra inventada.** Toda cifra sale de código (API del BCRP, snapshot fechado en `data/` o los
   agregados validados de ENAHO 2024 en `data/`). El LLM (Gemini) solo interpreta la frase del usuario y
   redacta la explicación: nunca calcula, completa ni estima cifras. Si no hay dato, el veredicto es
   "NO VERIFICABLE CON ESTAS FUENTES".
2. **Asociación ≠ causalidad.** "La cifra detrás de la cifra" describe brechas y contrastes; nunca dice que
   algo "causa" o "explica" otra cosa.
3. **Citar siempre** el código de serie del BCRP (o la fuente ENAHO y el factor `facpob07`), el periodo, la
   fuente (URL) y la tolerancia usada junto a cada veredicto.
4. **Preguntar antes de decisiones importantes** (cambiar tolerancias, fuentes, modelo de IA, estructura del
   repo o despliegue).
5. **Si algo falla, decirlo.** Si la API del BCRP no responde se usa el snapshot y se muestra su fecha; no se
   rellenan resultados.
6. **Nunca se versionan** claves (`.env`, `secrets.toml`), microdatos ni el entorno (`.venv/`).
7. Commits pequeños y descriptivos, repartidos en varios días.
