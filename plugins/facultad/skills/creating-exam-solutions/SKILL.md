---
name: creating-exam-solutions
description: Use when a facultad/university student wants to turn a course's exams (parciales/finales) or practice guides (TPs/prácticas) into a practice file — the statements transcribed verbatim (no answers) plus a collapsible step-by-step solution per exercise, faithful to the cátedra's resolution slides, for Obsidian. Trigger whenever the user wants to "transcribir los enunciados", "armar las resoluciones de", "pasar a limpio un parcial/final/TP", "practicar con" exam questions, or asks to add hidden/foldable step-by-step answers to exercises — even if they don't say "skill" or "Obsidian". Also when extracting exercises from a cátedra PDF (the "Resolución" version that has statement + solution) or building a practice sheet with foldable solutions.
---

# Crear resoluciones de exámenes y guías prácticas

## Qué es y para qué sirve

Convertís los **PDFs de la cátedra** (parciales, finales, TPs/prácticas — normalmente la versión **"Resolución"** que trae enunciado + solución) en **un archivo de práctica** en el wiki: los **enunciados literales** (sin respuestas, para resolver de cero) y, debajo de cada uno, su **resolución paso a paso en un callout plegable** (oculta hasta hacer clic). El objetivo es que el estudiante **practique como en el examen** y recién después destape la solución para corregirse.

Dos cosas no negociables:
1. **Fidelidad absoluta** a la cátedra: los enunciados y los números/fórmulas de las soluciones se **transcriben tal cual**, no se recalculan ni se inventan pasos.
2. **El render no se rompe en Obsidian**: hay reglas de LaTeX/escape muy específicas (sección "Reglas de render"). Es la parte que más cuesta y donde se cometen los errores.

## Inputs

PDFs en `raw/facultad/<materia>/`. Lo ideal es la versión **"Resolución"** (interlinea enunciado y solución). Si solo hay enunciado, igual sirve para la parte de transcripción, pero las resoluciones habrá que derivarlas (peor: preferí pedir la versión con solución).

## El proceso (fases)

### 1. Identificá el/los PDF y contá los ejercicios
`ls -lt raw/facultad/<materia>/` para encontrar el archivo (suele ser el más reciente si el user lo "acaba de subir"). Corré `scripts/extract_solutions.py <pdf>` para volcar el texto y ver cuántos ejercicios hay y de qué temas.

### 2. Extraé la capa de texto (NO OCR)
Estos PDFs tienen **capa de texto seleccionable**: el enunciado y las opciones a/b/c/d están en texto normal, y las **soluciones** están en caracteres **"negrita matemática" unicode** (𝑭𝑽, 𝑷𝑽…). `scripts/extract_solutions.py` normaliza con NFKC (𝑭𝑽 → `FV`) y marca dónde empieza el primer boldmath por página. **Usá esto en vez de leer el PDF como imagen** — te da los números y fórmulas EXACTOS, sin error de OCR. Leé el PDF como imagen (tool Read, `pages:`) **solo** para desambiguar una fórmula que en el texto quedó desordenada (subíndices, raíces).

### 3. Separá enunciado de solución (con criterio)
- **Enunciado** = pregunta + datos + **tablas de datos** + opciones a/b/c/d.
- **Solución** = las fórmulas/pasos que resuelven (el boldmath).
- **Trampas frecuentes** (revisá siempre):
  - Algunas soluciones están en **prosa**, no en boldmath (ej. "Al ser la tasa igual… el NPV es 0"). El corte por boldmath no las detecta.
  - Algunas **tablas de datos del enunciado** (cashflows de una IRR, tabla de proyectos) aparecen **después de las opciones**, en la zona de solución, por el layout del PDF. **Son parte del enunciado: conservalas.**
  - **Preguntas anuladas**: la cátedra a veces escribe "Pregunta anulada por…". Incluí el enunciado igual y marcalo.

### 4. Escribí los enunciados literales (sin respuestas)
Un archivo en `wiki/facultad/<materia>/sources/[YYYY-MM-DD] <Título>.md` (frontmatter `type: source`). Cada ejercicio: `**N)** <enunciado>` + opciones como lista `- a) …`. Marcá anuladas: `**N) (anulada)**`. Para guías/TPs sin opción múltiple, transcribí la consigna tal cual.
- **Reparar artefactos de extracción** (palabras pegadas por el salto de línea: "combinaciónde" → "combinación de", "TNAcon" → "TNA con") **restaura** el original — hacelo. Pero **nunca** cambies un número ni una palabra del contenido.
- Escapá el currency (ver Reglas de render). El modo más seguro: escribí el texto con `$` normales y al final corré un `.replace("$", r"\$")` por Python (los enunciados no llevan LaTeX, así que todo `$` es moneda).

### 5. Confirmá el FORMATO con 1–2 muestras ANTES de hacer todo
Esto es clave cuando hay muchos ejercicios. Resolvé **un ejercicio simple y uno complejo**, integralos al archivo, y mostráselos al user (en el chat en texto plano, y pedile que los abra en Obsidian para ver el render). Confirmá nivel de detalle antes de escalar. Rehacer 60 resoluciones porque el formato no era el que quería es el peor desperdicio.

### 6. Escribí las resoluciones (formato y nivel — ver abajo)
En callouts plegables. Adaptá el detalle a la complejidad del ejercicio.

### 7. Para volumen grande: subagentes en paralelo
Si son muchos ejercicios (un examen entero, varias guías), **despachá un subagente por examen/guía** (no por ejercicio — demasiados). Cada uno **lee** las fuentes y **escribe** sus resoluciones a `/tmp/RES_<tag>.md` en un formato delimitado; **no editan el archivo final** (chocarían). Después **vos integrás**. Ver `references/subagent-prompt.md` para el prompt exacto que funciona (incluye las reglas de render, el formato, y la exigencia de fidelidad).

### 8. Verificá el render
Corré `scripts/verify_render.py <archivo.md>`. Tiene que dar: `$` math PAR, 0 líneas impares, **0 `%` crudo real** en math, 0 `$$` display, y el conteo de callouts esperado. **No te fíes de un chequeo ingenuo de `%`**: los `\$` de moneda generan falsos positivos (un span que cruza dos `\$` con un `%` de prosa en el medio). El script ya quita el currency antes de mirar.

### 9. Registrá en el wiki
`index.md` (entrada del archivo) + `log.md` (entrada del op), **en el mismo turno** que la edición.

## Reglas de render (Obsidian) — el corazón técnico

Obsidian renderiza MathJax. Estas son las reglas que evitan que se rompa (cada una corresponde a un error real y recurrente):

- **Currency `$` → `\$`.** Un `$` suelto abre un span de matemática. Una línea con `97$ … 92.87$` se interpreta como math entre los dos `$`. Escapá **todo** `$` de moneda.
- **`%` dentro de `$…$` → `\%`.** En matemática, `%` inicia un **comentario** de MathJax y se come el resto de la línea. `$\dfrac{22\%}{2}=11\%$`, nunca `$\dfrac{22%}{2}=11%$`. Este es el error #1 que rompe las fórmulas.
- **Nada de `$$` display dentro de callouts.** El bloque `$$…$$` con prefijo `>` es frágil y suele no renderizar. **Todo inline `$…$`**; para que se vea grande usá `\dfrac` (fuerza tamaño display inline).
- **Decimales y miles con `{,}`** dentro de math: `$5{,}657\%$`, `$400{,}000$` (el `{,}` evita que MathJax meta espacio después de la coma).
- **Símbolos (σ, β, subíndices) en LaTeX** dentro de math (`$\sigma_p$`, `$\beta$`); pero en los **enunciados** (que escapan todo `$`) usá **unicode** (σ, ₁, ₂) para no necesitar delimitadores LaTeX que choquen con el escape.
- **Cuidado con doble-escape.** Si ya escapaste el currency a `\$` y volvés a correr `.replace("$", r"\$")`, te queda `\\$` (barra visible). Escapá una sola vez; el verificador detecta los `\\$`.

## Formato de la resolución (el corazón pedagógico)

Cada resolución es el contenido de un **callout plegable**:

```
> [!success]- Ver resolución paso a paso
> **Respuesta: <letra>) <valor exacto de la opción>**
>
> **Datos:** <los datos clave>          (opcional, si ordena)
>
> **1) <título del paso>.** <fórmula con números y resultado>
> **2) <título>.** <...>
```
Las **anuladas** van con `> [!warning]- Respuesta` y una línea explicando que se anuló.

**Nivel de detalle según complejidad** (esto lo pidió explícitamente el estudiante):
- **Simples** (cálculo directo: TEA/TNA/TEM, plazo fijo, perpetuidad, una fórmula): paso a paso **conciso**. Datos → pasos → resultado.
- **Complejos** (bootstrapping, árboles de decisión, opciones combinadas, Markowitz/Sharpe, arbitraje, default con probabilidad implícita): agregá una primera línea **`**Idea.**`** con la intuición y el **porqué de cada fórmula**, no solo el cálculo.
- **Conceptuales** (elegir afirmación correcta/incorrecta, V/F): explicá **por qué la correcta lo es** y, en una línea, **por qué se descarta cada distractor**. No hay cálculo: es teoría.

**Etiquetá la respuesta arriba** (`**Respuesta: c) 5,995,177**`) para que, al destapar, lo primero que vea sea la letra correcta y después el procedimiento.

## Fidelidad

Transcribí números y fórmulas **tal cual** la solución de la cátedra. No recalcules "para mejorar". **Excepción honesta:** si la hoja de la cátedra tiene una **inconsistencia interna** (un encabezado de fórmula que daría un número distinto al que ellos mismos computan), usá el cálculo que **reproduce el resultado correcto** y **avisale al user** esa nota de fidelidad. Lo mismo si una opción está marcada y el número cierra: respetá el número de la cátedra aunque el enunciado parezca pedir otra cosa (pasa con conversiones de tasa).

## Checklist

- [ ] Identifiqué el PDF y conté los ejercicios (`extract_solutions.py`)
- [ ] Separé enunciado de solución con criterio (prosa, tablas que migran, anuladas)
- [ ] Enunciados literales escritos, currency escapado, artefactos reparados (sin tocar números)
- [ ] Confirmé el formato con 1–2 muestras antes de hacer todo
- [ ] Resoluciones con nivel adaptado (conciso / Idea+porqué / conceptual)
- [ ] Volumen grande → subagentes por examen a `/tmp`, integré yo
- [ ] `verify_render.py` limpio (math PAR, 0 impares, 0 `%` crudo real, 0 `$$`, callouts = N)
- [ ] `index.md` + `log.md` actualizados en el mismo turno

## Errores comunes (observados en uso real)

| Error | Síntoma | Arreglo |
|---|---|---|
| `%` sin escapar en math | la fórmula se corta a la mitad | `\%` SIEMPRE dentro de `$…$` |
| `$` de moneda suelto | medio renglón se vuelve "matemática" | escapá todo a `\$` |
| `$$` display en callout | la fórmula no aparece | todo inline `$…$` con `\dfrac` |
| Doble escape | aparece `\$` con barra visible | escapá una sola vez |
| Tabla de datos perdida | la IRR/PI no tiene los flujos | conservá tablas que migran a la zona de solución |
| Solución en prosa ignorada | quedó sin resolución | revisá los ejercicios sin boldmath |
| Hacer 60 y rehacer | el formato no era el querido | muestra de 1–2 y confirmar primero |
| Falsos positivos de `%` | el verificador "encuentra" errores que no son | quitá `\$` antes de chequear (el script ya lo hace) |
