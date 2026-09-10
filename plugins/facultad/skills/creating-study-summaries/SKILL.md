---
name: creating-study-summaries
description: Use when the user (a university/facultad student) wants a comprehensive study summary ("resumen") for a course built from theory notes ("apuntes") and practice guides ("prácticas") so they can solve every exercise in the guides using only the summary — also when expanding, clarifying, auditing, or adding graphics to such a summary, or when the student says they don't understand a calculation or formula in one ("no entiendo las cuentas de...").
---

# Crear resúmenes de estudio (facultad)

## Principio central

**El resumen tiene que alcanzar, por sí solo, para resolver TODOS los ejercicios de las guías prácticas** (problemas, ejercicios y verdadero/falso). Y tiene que ser **didáctico**: explica conceptos, **métodos de resolución** e **intuición** — **no es un volcado de fórmulas**. Si con el resumen el estudiante no puede resolver un tipo de ejercicio, o lee una fórmula y no sabe *cómo* ni *por qué* usarla, el resumen está incompleto.

## Inputs

- Apuntes teóricos (PDF/PPTX) + guías prácticas (PDF), en `raw/facultad/<materia>/`.
- A veces también **apuntes de clase manuscritos** (GoodNotes exportado a PDF): se leen visualmente y traen los ejemplos tal como los hizo el profe — oro para que el resumen explique como el curso.
- **Fotos/capturas de los apuntes del estudiante** pegadas en el chat: suelen traer (a) su estilo de redacción a imitar, y (b) **los números de los "casos para resolver" que las slides dejan vacíos** → incorporarlos como worked examples etiquetados **📓**.
- Los .pptx de cátedra esconden contenido fuera del texto visible de las slides: tablas en imágenes WMF/EMF (extraer strings UTF-16LE del binario, regex `(?:[\x20-\x7e]\x00){3,}`) y **baterías enteras de ejercicios en Excel embebidos** (`ppt/embeddings/*.xlsx`, leer con openpyxl; a veces traen las soluciones de la cátedra en otra hoja). **Siempre revisar los embeddings y las imágenes**: la batería real puede ser mucho más grande que lo que muestran las slides.

## El formato por tema (el corazón)

Cada tema/sección sigue **el mismo patrón**:

1. **💡 La idea** — qué es y para qué sirve, en palabras simples (la intuición). Cuando ayude, **🧠 analogía** de la vida real (el PN residual = depto menos hipoteca; la dilución = club que vende membresías al precio fundacional).
2. **📐 Definición / 📋 Propiedades** — lo formal, **enunciado explícitamente** (el estudiante quiere "tener todo": no dejes las definiciones/propiedades implícitas). **Cada regla lleva su porqué** (la razón económica/legal/matemática detrás), no solo el enunciado.
3. **🛠️ Cómo se resuelve** — el **método/receta paso a paso**, explicado (no solo la fórmula: el procedimiento).
4. **✍️ Ejemplo** — resuelto mostrando **el porqué de cada paso**, etiquetando de dónde sale: **📕** (apunte/clase), **📘** (guía + número de ejercicio) o **📓** (apuntes del propio estudiante).

**TODOS los ejercicios se resuelven PASO POR PASO** — no solo los difíciles, y nunca "en bloque" (mostrar la tabla/resultado final sin el camino no cuenta como resolución). Estructura: **🧭 Cómo pensarlo** (qué estrategia y por qué) → **micro-pasos numerados con el porqué de cada uno** → **resultado** → **✓ chequeo** (invariantes para auto-verificar: "el total no cambió", "la columna X siempre vale Y") → **⚡ atajo** si existe. En tablas multi-período (p.ej. dividendos acumulativos año a año): **fila por fila y celda por celda** — de dónde sale cada número. En asientos contables: **renglón por renglón** con el origen de cada importe.

**Los porqués y analogías que NO están en el material de la cátedra se marcan** *(interpretación propia)* o 🧠; las conexiones con otras materias, con 🔗 (ej.: acción preferida ≈ bono → renta fija de Finanzas). Así el estudiante sabe qué puede citar en el parcial y qué es andamiaje.

## Anatomía de cada fórmula (obligatorio)

Una fórmula "explicada" no es una fórmula con el resultado al lado. **Cada fórmula del resumen se abre así**, en este orden (observado 2026-09 con ROA/ROE de ICG II: el estudiante tenía la fórmula, los números y el resultado, y aun así no entendía "de dónde sacás la $i$, la $t$"):

1. **Cada símbolo, uno por uno**: qué es en palabras, **de dónde sale** (qué renglón del balance/EERR, qué slide/página lo define) y **la cuenta desde los datos** ("$t = \text{Imp.}/EBT$: la tasa que pagó de verdad; se divide por EBT porque el impuesto se calcula después de intereses → $10/28{,}5 = 35{,}088\%$"). Un símbolo que aparece en la fórmula sin este párrafo es un hueco.
2. **El porqué de cada pieza** de la fórmula (por qué EBIT y no neta; por qué $(1-t)$; por qué activo total y no PN). Sin esto se memoriza sin entender.
3. **Derivación** cuando la fórmula es compuesta o "sale de otra" (leverage, DuPont, WACC, cualquier identidad): el álgebra paso a paso desde la definición base, **un comentario por línea** (`aligned` con `&&`). El estudiante tiene que ver que no es un invento.
4. **Mecanismos con tabla "sin / con / diferencia"**: cuando la fórmula describe un efecto (tax shield, leverage, dilución, absorción vs variable), el mismo caso **con y sin** el efecto lado a lado, columna diferencia, y lectura **fila por fila** de qué cambió y por qué. "Tax shield = interés × t" en una línea no alcanza.
5. **El reparto**: cuando un total se divide entre partes (acreedores/accionistas, fisco/empresa, divisiones), tabla **puso / se lleva / rendimiento** y ✓ de que las partes suman el total. Es la intuición que hace clic antes que la fórmula.
6. **Cerrar por dos vías**: el resultado por fórmula tiene que coincidir con el cálculo directo (ROE por leverage = neta/PN). Si no cierra, decí si es redondeo o error.

**Precisión numérica (regla fija): 3 decimales en todo**, tasas en % con 3 decimales (35,088%, no 35%), **arrastradas sin redondear entre pasos**, y la convención declarada al inicio de la sección. Cuando la cátedra redondea (casi siempre), mostrá los dos: el exacto y "(slide: 21%)". Si la slide **fuerza** un número para que cierre (21% + 13% = 34%), ⚠️ explícita con tabla "versión exacta / t redondeada / slide" y una **regla para el parcial** (qué usar cuando el enunciado da la tasa vs cuando da el impuesto en pesos). Nunca mezcles precisiones dentro de una misma cadena: si el estudiante recalcula con tus propios valores intermedios tiene que llegar al mismo número.

## Baterías de ejercicios (guías, repasos, parciales)

Cuando la fuente es una batería de ejercicios (no teoría):

- **Source page propia** con cada enunciado transcripto completo + **resolución plegable** (`> [!success]- Resolución paso a paso`) — el estudiante practica primero y abre después (*active recall*).
- **Marcar cada resolución:** ✅ = verificada contra la solución que trae la cátedra · 🤖 = resolución propia (la fuente no la trae). Los **supuestos** que la resolución necesita (política de pago, saldos iniciales) van explícitos y marcados.
- **Solución de cátedra con criterio no explicado** (números que cierran pero lógica ambigua): transcribir sus números, verificar la aritmética, ofrecer la lectura más consistente marcada *(interpretación propia)* y dejar **flag "preguntar en clase"**. Nunca adivinar en silencio.
- **Títulos de ejercicio = anclas estables:** cortos, sin emojis ni comillas (los marcadores ✅/🤖 y el detalle de origen van en la primera línea del cuerpo, no en el heading) — se van a linkear por `[[Página#Encabezado]]` y un heading recargado obliga a renombrar después.
- **Deep-links en las dos direcciones:** cada sección de teoría del resumen termina con 🎯 *Practicá:* `[[Batería#Ejercicio N|alias]]` apuntando al ejercicio que la ejercita; y cada resolución cita la sección del resumen que usa (§N).

## El proceso (fases)

1. **Reunir** los archivos en `raw/facultad/<materia>/` (mover ahí si están sueltos; folder en minúsculas-sin-espacios).
2. **Leer TODAS las prácticas primero** y **enumerar cada tipo de ejercicio**. Esto es la **especificación**: define qué tiene que cubrir el resumen.
3. **Leer los apuntes** → definiciones, métodos, ejemplos y, clave, **la NOTACIÓN EXACTA del curso** (no inventes notación). Apuntes grandes → despachá **subagentes en paralelo** (uno por apunte) que devuelvan digests estructurados.
4. **Confirmá con el estudiante**: el **orden** de los temas y qué **enfatizar**. (No asumas el orden; te lo van a dar.)
5. **Escribí el resumen** con el formato de arriba, en el orden pedido, en **español**, con **LaTeX para toda fórmula** (`$...$` / `$$...$$`). **Cero omisiones:** el resumen cubre TODO lo que dice el material fuente — incluso lo que parece administrativo (programa, evaluación, escala de notas) y los bullets sueltos; si algo de verdad no aporta, mencionalo comprimido antes que omitirlo.
6. **Gráficos donde un dibujo explica mejor** (vectores, cónicas, curvas de nivel + gradiente, tangencia/Lagrange, regiones, sistemas como rectas, órdenes/jerarquías, comparaciones antes/después): **Excalidraw** para lo geométrico/conceptual (generado con Python → `excalidraw-helper.py`, embebido con `![[Nombre.excalidraw|ancho]]`) y **Charts** (Chart.js, bloque ` ```chart `) para funciones $y=f(x)$. **Nunca Mermaid.** Agregá las imágenes **por iniciativa propia** donde convengan — no esperes a que las pidan.
7. **Auditoría de completitud** (al terminar, o cuando el estudiante la pida): despachá **subagentes en paralelo, uno por tema, READ-ONLY**, que crucen **cada ejercicio de la guía** y **cada concepto del apunte** contra el resumen y reporten **huecos de ejercicios / huecos de teoría / errores**, con el contenido exacto a agregar y la sección destino. Después **tapás los huecos vos** (los agentes solo reportan, para no chocar editando el mismo archivo). Meta: **ningún tipo de ejercicio sin método**.
8. **Iterá con el feedback**: cuando el estudiante dice "no entiendo X", expandí ese ejemplo/método con el tratamiento paso a paso. Las definiciones/métodos que estén "en una sola línea" suelen pasar desapercibidos → desarrollalos en serio. **Feedback de estilo = modificar el resumen EXISTENTE** (no crear uno nuevo). Si el feedback es general ("de ahora en más hacelo así"), **actualizá también esta skill** en el mismo turno para que aplique a todos los resúmenes futuros.
9. **Las preguntas conceptuales del estudiante se responden Y se archivan.** "¿Qué pasa con X antes y después?", "¿cómo sé cuándo se paga Y?": respondé en el chat y **guardá la respuesta en la sección correspondiente** del resumen o la batería (bloque 📓 con su pregunta como título, o checklist 🛠️ de filtros/pasos) — la duda resuelta tiene que quedar estudiable, no perderse en el chat. El estudiante también dicta apuntes por chat, manda fotos, o deja **stubs a medias** dentro del resumen ("sube porque la fórmula es=…") → completalos en su lugar manteniendo sus palabras, formateados como 📓.
10. **Wiki**: source page por cada apunte/práctica, el resumen como **synthesis page** en `facultad/<materia>/synthesis/`, y actualizá `index.md` + `log.md` en el mismo turno.
11. **Las dos vistas: por unidad + unificado.** Cuando la materia acumula más de un resumen por unidad, mantené además un **"Resumen <materia> Completo"** que los **transcluye** con embeds (`![[Resumen U1]]`, `![[Resumen U2]]`) + un mapa de la materia con estado por unidad. Los resúmenes por unidad son la **fuente editable** (los apuntes 📓 del estudiante se integran ahí, nunca solo en una source page); el Completo se actualiza solo vía transclusión — nunca dupliques el contenido a mano (diverge). Cada unidad nueva = su resumen + su embed + su fila en el mapa.

## Lo que el estudiante dejó claro (preferencias firmes)

- **NO solo fórmulas** — explicá el **método de resolución** y la **intuición**.
- **Ejemplos completos, etiquetados** (📕/📘/📓), con el **porqué** de cada paso; cuando no se entienden, expandilos.
- **TODOS los ejercicios paso por paso** (2026-08: "los ejercicios resolvelos paso por paso") — micro-pasos numerados, tablas fila-por-fila, asientos renglón-por-renglón, con ✓ chequeos.
- **Cero omisiones** del material fuente (2026-08: "no omitas cosas de las diapositivas").
- **Analogías y porqués en cada tema** (2026-08: "ejemplos, analogías, explicaciones de porque cada cosa"), marcados *(interpretación propia)*/🧠 si no son de la cátedra; 🔗 para conexiones entre materias.
- **Todo apodo/metáfora se DEFINE la primera vez que aparece — o no se usa** (2026-08: *"no entiendo qué significan las panzas esas, o sea panza para arriba, abajo, costado"* — había usado "panza" para el solapamiento de dos círculos sin definirlo nunca). Un apodo sin definir es **peor** que el término técnico: el estudiante no puede ni buscarlo. Si usás una imagen coloquial: (a) definila explícitamente al presentarla, (b) mostrá **en un dibujo** a qué parte señala, (c) aclará qué **NO** significa si la palabra sugiere algo falso (orientación, movimiento, tamaño), y (d) usala **consistentemente** después. Antes de cerrar un resumen, grepeá tus propias metáforas y verificá que cada una tenga su definición.
- **Antes de las reglas, el MAPA** *(corolario del anterior)*: cuando un tema tiene un dibujo base del que se leen todas las fórmulas (las 4 zonas de un Venn, el árbol de probabilidad, la tabla de doble entrada), va una sección **🗺️ mapa** ANTES de la lista de reglas: las partes numeradas y nombradas, un ejemplo **contado con unidades reales** (personas, pesos) que haga visible el mecanismo, y una tabla **"frase del enunciado → qué parte del dibujo es"** con las confusiones típicas señaladas. Después las reglas se explican señalando partes del mapa, no en abstracto.
- **Menos monótono**: variar el ritmo — tablas comparativas con preguntas guía ("¿cambia el total? ¿sale caja?"), trampas de parcial ⚠️, diagramas, voz de los apuntes del estudiante (paréntesis de intuición en primera persona: *"quiero hacer la reducción porque no quiero ver un RNA negativo"*).
- **Definiciones y propiedades explícitas** (📐/📋) — que con el resumen "tenga todo".
- **Notación exacta del curso** (no inventar).
- **LaTeX** siempre; **español**; **Excalidraw, no Mermaid**; imágenes por iniciativa propia.
- Para temas donde el estudiante es flojo (ej. estadística): desglosá **todo** paso por paso, desde cero, sin asumir base.
- **Anatomía de cada fórmula + 3 decimales** (2026-09, ROA/ROE de ICG II: *"explicámelo mejor, explicando de dónde sacás la i, la t, cada fórmula; explicá mejor el tax shield; usá 3 decimales siempre"*): cada símbolo con su origen y su cuenta, el porqué de cada pieza, derivación de las fórmulas compuestas, mecanismos con tabla sin/con, el reparto del total, cierre por dos vías, y los redondeos de la cátedra señalados, no heredados. Ver sección "Anatomía de cada fórmula".

## Errores comunes (qué pasa SIN esto — observado en uso real)

| Error | Síntoma | Arreglo |
|---|---|---|
| Resumen "muy numérico" | el estudiante lee fórmulas y no entiende | formato 💡→📐/📋→🛠️→✍️ |
| Faltan tipos de ejercicio | no puede resolver parte de la guía | leer prácticas primero + auditoría |
| Ejemplos en una línea | no se siguen | paso a paso con el porqué |
| Ejercicio resuelto "en bloque" (tabla/resultado final sin el camino) | pide "resolvelo paso por paso" | fila por fila / celda por celda, micro-pasos numerados + ✓ chequeos |
| Omitir contenido que parece administrativo (programa, evaluación, bullets sueltos) | pide "no omitas cosas de las diapositivas" | cero omisiones: todo entra, comprimido si hace falta |
| Reglas enunciadas sin su porqué | se memoriza sin entender; pide "explicaciones de por qué cada cosa" | cada regla con razón económica/legal + analogía, marcadas si son propias |
| Resumen monótono (solo texto corrido) | cuesta estudiarlo | variar: tablas con preguntas guía, ⚠️ trampas, diagramas, voz del estudiante |
| Definición/método en una línea | "no lo vi en el resumen" | desarrollá cada uno como sección |
| Saltearse la auditoría | quedan huecos sin método | subagentes por tema, read-only |
| Apodo o metáfora sin definir | *"no entiendo qué significan las panzas esas"* — y la palabra sugiere algo falso | definila al presentarla + señalala en un dibujo + aclará qué NO significa |
| Reglas antes que el dibujo base | las fórmulas se leen en abstracto y no se fijan | 🗺️ mapa primero (partes numeradas + ejemplo contado + tabla frase→parte), reglas después |
| No etiquetar el ejemplo | no sabe de qué ejercicio sale | siempre 📕 apunte/clase, 📘 guía+nº o 📓 apuntes del estudiante |
| Inventar notación | no coincide con el parcial | copiar la notación del apunte |
| Leer solo el texto visible del pptx | falta media batería (Excel/WMF embebidos) | revisar siempre `ppt/embeddings/` + imágenes |
| Headings de ejercicio con emojis/comillas/largos | anclas de wikilink frágiles; hay que renombrar después | títulos cortos y estables; marcadores al cuerpo |
| **Wikilink con alias dentro de una celda de tabla** | *"las tablas en Obsidian a veces tiran error"* — el `\|` del alias parte la fila y rompe la tabla | escribí **`[[X\|alias]]`** con el pipe escapado; y dejá una línea `>` en blanco entre el título de un callout y una tabla, y una línea en blanco tras un code fence |
| Teoría y ejercicios sin cross-links | pide "agregá wikilinks que lleven directo al ejercicio" | 🎯 deep-links por sección, en ambas direcciones |
| Adivinar un criterio de cátedra no explicado | resolución inventada sin aviso | transcribir + lectura marcada *(propia)* + "preguntar en clase" |
| Responder una duda solo en el chat | la explicación no queda estudiable | archivarla como bloque 📓/🛠️ en la sección correspondiente |
| Fórmula con símbolos "caídos del cielo" | *"no entiendo de dónde sacás la i, la t"* — tiene la fórmula y el resultado, no el camino | anatomía: cada símbolo con origen (slide/renglón) + cuenta desde los datos + porqué de cada pieza + derivación |
| Efecto explicado en una línea (tax shield = interés × t) | *"explicá mejor el tax shield"* | tabla sin/con/diferencia + lectura fila por fila + reparto puso/se lleva |
| Heredar el redondeo de la cátedra (21% + 13% = 34%) | el estudiante recalcula, le da 12,22% y no sabe quién tiene razón | 3 decimales arrastrados; ⚠️ con tabla exacta/redondeada/slide + regla para el parcial |

## Checklist

- [ ] Leí TODAS las prácticas y enumeré cada tipo de ejercicio
- [ ] Leí los apuntes (con su notación exacta) — subagentes si son grandes
- [ ] Confirmé orden y énfasis con el estudiante
- [ ] Cada tema con 💡 idea (+🧠 analogía) → 📐/📋 def/prop (con su porqué) → 🛠️ método → ✍️ ejemplo (etiquetado 📕/📘/📓)
- [ ] TODOS los ejercicios paso por paso (tablas fila-por-fila, asientos renglón-por-renglón) con ✓ chequeos
- [ ] Cada fórmula abierta: símbolos con origen y cuenta, porqué de cada pieza, derivación si es compuesta, tabla sin/con para mecanismos, reparto del total, cierre por dos vías
- [ ] 3 decimales en todo, arrastrados; convención declarada; redondeos de la cátedra marcados "(slide: X)" y los forzados con ⚠️
- [ ] Cero omisiones: crucé el resumen contra el material fuente completo
- [ ] Porqués/analogías propias marcadas *(interpretación propia)*; conexiones entre materias con 🔗
- [ ] Baterías: enunciado transcripto + resolución plegable, marcas ✅/🤖, supuestos explícitos, ambigüedades con flag "preguntar en clase"
- [ ] Títulos de ejercicio como anclas estables + deep-links 🎯 teoría↔ejercicios
- [ ] Preguntas del estudiante respondidas en el chat Y archivadas en la página
- [ ] Gráficos donde ayudan, por iniciativa propia (Excalidraw / Charts), nunca Mermaid
- [ ] Auditoría de completitud (subagentes por tema) → huecos tapados
- [ ] `index.md` + `log.md` actualizados; verifiqué 0 wikilinks/embeds rotos (**incluidas las anclas de encabezado**)
- [ ] Chequeé la **sintaxis de las tablas**: ningún `[[X|alias]]` sin escapar dentro de una celda, ninguna tabla pegada al título de un callout ni a un cierre de code fence

## Referencia: gráficos

- **Excalidraw** (geométrico): generá el `.excalidraw.md` con Python usando `excalidraw-helper.py` (JSON válido garantizado), guardalo en `facultad/<materia>/excalidraw/` y embebelo con `![[Nombre.excalidraw|520]]`.
- **Charts** (función $y=f(x)$): bloque markdown
  ```
  ```chart
  type: line
  labels: [0.5, 1, 2, 3]
  series:
    - title: f = 1/x
      data: [2, 1, 0.5, 0.33]
  tension: 0.4
  labelColors: true
  ```
  ```
