# Prompt de subagente — resoluciones en paralelo (volumen grande)

Cuando hay muchos ejercicios (un examen entero, varias guías), despachá **un subagente por examen/guía** (no por ejercicio). Corren en paralelo, **escriben a `/tmp/RES_<tag>.md`** (no editan el archivo final), y después **vos integrás**. Este prompt es el que funcionó — copialo y completá lo que está entre `<…>`.

```
Sos asistente experto en finanzas/<materia> del curso <CURSO> (<UNIVERSIDAD>, prof. <PROFE>). Tu tarea: generar la **resolución paso a paso** de cada ejercicio del <EXAMEN/GUÍA>, fiel a las diapositivas de resolución de la cátedra, para insertarlas en un archivo de práctica de Obsidian.

## LEÉ ESTAS FUENTES (en este orden)
1. Soluciones crudas de la cátedra (texto exacto, con fórmulas y números): `/tmp/SOL_<TAG>.txt`
2. PDF de resolución (leelo como IMAGEN con la tool Read si una fórmula quedó desordenada en el texto): `<ruta al PDF>`
3. Archivo de práctica con los ENUNCIADOS, la RESPUESTA CORRECTA de cada ej (en los callouts actuales) y DOS EJEMPLOS YA HECHOS del formato exacto: `<ruta al .md>` → mirá <Ej simple> y <Ej complejo>: ESE es el molde.

## FORMATO (idéntico a esas dos muestras). Cada línea arranca con `> `:
> **Respuesta: <letra>) <valor exacto de la opción correcta>**
>
> **Datos:** <datos clave>   (opcional)
>
> **1) <título del paso>.** <fórmula con números y resultado>
> **2) <título>.** <...>

NIVEL DE DETALLE:
- SIMPLES (cálculo directo): paso a paso CONCISO.
- COMPLEJOS (<listá los complejos de ESTE examen>): primera línea **Idea.** con la intuición + el PORQUÉ de cada fórmula.
- CONCEPTUALES (teoría, elegir afirmación): explicá por qué la correcta lo es y, en una línea, por qué se descarta cada distractor. No hay cálculo.

## REGLAS DE LaTeX (CRÍTICAS — Obsidian; si las rompés no renderiza)
- Math inline `$...$`. Fracciones con `\dfrac`.
- Dentro de `$...$`, TODO `%` va como `\%` (si no, MathJax lo toma como comentario y rompe la línea). Ej: `$\dfrac{22\%}{2}=11\%$`.
- Decimales/miles con `{,}`: `$1{,}820{,}731$`, `$5{,}1271\%$`.
- Greek/subíndices en LaTeX: `$\sigma_p$`, `$\beta$`, `$E(r_p)$`.
- NUNCA un `$` de moneda suelto. NADA de `$$` display (rompe en callouts), TODO inline `$...$`.
- Línea en blanco dentro del callout = una línea con solo `>`.

## FIDELIDAD ABSOLUTA
Números y fórmulas TAL CUAL la solución de la cátedra (`/tmp/SOL_<TAG>.txt`). NO recalcules ni inventes pasos. La letra correcta está en el callout actual del archivo de práctica. Si la hoja de la cátedra tiene una inconsistencia interna, usá el cálculo que reproduce el resultado correcto y dejá una nota.

## ANULADAS (si las hay)
Para los ejercicios <N, M…> anulados, el contenido es exactamente:
> Pregunta anulada por la cátedra (error en la consigna) — sin respuesta oficial.

## SALIDA
Escribí TODO a `/tmp/RES_<TAG>.md`, un bloque por ejercicio con delimitador EXACTO:
=== EJ 1 ===
> **Respuesta: ...**
> ...
=== EJ 2 ===
> ...
Cubrí los <N> ejercicios. NO devuelvas el contenido en el chat: escribilo al archivo. Al terminar, confirmá cuántos escribiste y qué dudas de fidelidad tuviste (si alguna).
```

## Integración (lo hacés vos, después)

1. Verificá los `/tmp/RES_<tag>.md`: que estén los N ejercicios, todas las líneas empiecen con `>`, 0 `%` crudo, 0 `$$` (corré una validación rápida).
2. Parseá por el delimitador `^=== EJ (\d+) ===$` → `ANS[(tag, num)] = body`.
3. Regenerá los enunciados limpios e insertá cada `body` como callout tras las opciones de su ejercicio: `> [!success]- Ver resolución paso a paso` + el body. Anuladas → `> [!warning]- Respuesta` + el body.
4. Corré `scripts/verify_render.py <archivo> --expect <N>`.
5. Actualizá `index.md` + `log.md`.

**Patrón de inserción** (recorré el archivo; cuando ves `**N)**`, marcás el ejercicio abierto; cuando llega el próximo `**M)**`, un `---` o un `## `, insertás el callout del anterior). Es el mismo recorrido para respuestas cortas o resoluciones largas.
