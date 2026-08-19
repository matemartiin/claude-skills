# mateo-skills

Marketplace de plugins de [Claude Code](https://claude.com/claude-code) con mis skills personales, para tenerlas en todos mis dispositivos.

## Instalar

```
/plugin marketplace add matemartiin/claude-skills
/plugin install facultad@mateo-skills
```

Después de instalar, `/help` o el listado de skills debería mostrar `facultad:creating-study-summaries` y `facultad:creating-exam-solutions`.

Para actualizar a la última versión publicada:

```
/plugin marketplace update mateo-skills
```

## Plugins

### `facultad`

Flujo de estudio universitario sobre un vault de Obsidian.

| Skill | Para qué |
|---|---|
| `creating-study-summaries` | Arma un resumen de estudio completo de una materia a partir de los apuntes de teoría y las guías de práctica, con el criterio de que se pueda resolver **cualquier** ejercicio de las guías usando solo el resumen. También sirve para ampliar, aclarar, auditar o agregarle gráficos a un resumen que ya existe. |
| `creating-exam-solutions` | Transcribe los enunciados de parciales, finales y TPs tal cual, y le agrega abajo de cada ejercicio una resolución paso a paso plegable, fiel a las slides de resolución de la cátedra. |

Ambas asumen Obsidian: LaTeX con `$...$` y `$$...$$`, wikilinks `[[...]]`, callouts plegables, Excalidraw para los diagramas (nunca Mermaid) y Chart.js para las funciones.

## Editar

Las skills viven en `plugins/facultad/skills/`. En mi máquina principal `~/.claude/skills/` tiene symlinks a esas carpetas, así que editar la skill en cualquiera de los dos lados es lo mismo: se edita el repo. Commit + push y el resto de los dispositivos lo toman con `/plugin marketplace update mateo-skills`.
