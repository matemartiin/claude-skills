"""
excalidraw-helper.py — generar diagramas .excalidraw.md válidos para Obsidian.

Por qué existe: el formato nativo de Excalidraw es JSON con muchos campos
obligatorios por elemento; a mano se rompe fácil. Estas funciones arman el JSON
correcto y lo envuelven en el markdown que el plugin de Obsidian sabe leer.

Uso típico (copiá este patrón y adaptá las coordenadas):

    import math
    # 1) mapeo math -> canvas (Excalidraw tiene la y hacia ABAJO):
    S, OX, OY = 55, 110, 360          # escala px/unidad, origen en canvas
    def C(x, y): return (OX + S*x, OY - S*y)

    E = []
    E.append(seg("xaxis", C(-1,0), C(5,0), GRAY, 1))          # eje x
    E.append(seg("yaxis", C(0,-1), C(0,4), GRAY, 1))          # eje y
    E.append(seg("v", C(0,0), C(3,1), TEAL, 3, arrow=True))   # vector (flecha)
    E.append(ell("circ", *C(0,0), S*1, S*1, CORAL, sw=2))     # circunferencia r=1
    E.append(text("lbl", *C(3,1), "v=(3,1)", 16, TEAL))       # etiqueta
    write("/ruta/al/wiki/facultad/<materia>/excalidraw/Mi Diagrama.excalidraw.md",
          E, "excalidraw, matematica-2, vectores")

Después embebés en el resumen con:  ![[Mi Diagrama.excalidraw|520]]

Reglas de oro:
- Coordenadas SIEMPRE positivas; la y va hacia abajo (por eso C() hace OY - S*y).
- Para flechas usá seg(..., arrow=True). Para curvas (parábola, hipérbola) usá
  poly() con una lista de puntos que vos calculás.
- Validá: write() ya hace json.loads para chequear que el JSON es válido.
"""

import json, math, os

# Paleta segura (estos hex se ven bien en modo claro y oscuro de Obsidian)
TEAL = "#1D9E75"; BLUE = "#378ADD"; CORAL = "#D85A30"
GRAY = "#888780"; GREEN = "#639922"; PURPLE = "#7F77DD"; RED = "#E24B4A"

_seed = [1000]


def _el(eid, etype, x, y, w, h, stroke="#1e1e1e", bg="transparent",
        sw=2, fill="solid", dashed=False, extra=None):
    """Elemento base con TODOS los campos que Excalidraw exige."""
    _seed[0] += 1
    e = {
        "id": eid, "type": etype, "x": round(x, 2), "y": round(y, 2),
        "width": round(w, 2), "height": round(h, 2), "angle": 0,
        "strokeColor": stroke, "backgroundColor": bg, "fillStyle": fill,
        "strokeWidth": sw, "strokeStyle": "dashed" if dashed else "solid",
        "roughness": 1, "opacity": 100, "groupIds": [], "frameId": None,
        "roundness": None, "seed": _seed[0], "version": 1,
        "versionNonce": _seed[0], "isDeleted": False, "boundElements": None,
        "updated": 1700000000000, "link": None, "locked": False,
    }
    if extra:
        e.update(extra)
    return e


def text(eid, x, y, s, size=16, color="#1e1e1e"):
    """Etiqueta de texto. (x,y) es la esquina superior-izquierda en canvas."""
    w = max((len(l) for l in s.split("\n")), default=1) * size * 0.58
    h = (s.count("\n") + 1) * size * 1.25
    return _el(eid, "text", x, y, w, h, stroke=color, extra={
        "text": s, "fontSize": size, "fontFamily": 1, "textAlign": "left",
        "verticalAlign": "top", "containerId": None, "originalText": s,
        "lineHeight": 1.25, "baseline": round(size * 0.85)})


def seg(eid, p0, p1, color="#1e1e1e", sw=2, arrow=False, dashed=False):
    """Segmento (line) o flecha (arrow) de p0 a p1 (ambos en canvas)."""
    (x0, y0), (x1, y1) = p0, p1
    return _el(eid, "arrow" if arrow else "line", x0, y0,
               abs(x1 - x0), abs(y1 - y0), stroke=color, sw=sw, dashed=dashed,
               extra={"points": [[0, 0], [round(x1 - x0, 2), round(y1 - y0, 2)]],
                      "lastCommittedPoint": None, "startBinding": None,
                      "endBinding": None, "startArrowhead": None,
                      "endArrowhead": "arrow" if arrow else None})


def poly(eid, pts, color="#1e1e1e", sw=2, dashed=False,
         bg="transparent", fill="hachure", closed=False):
    """Polilínea por una lista de puntos canvas (para parábolas, hipérbolas,
    polígonos sombreados). closed=True + bg=color → región rellena."""
    p = list(pts) + ([pts[0]] if closed else [])
    x0, y0 = p[0]
    xs = [a[0] for a in p]; ys = [a[1] for a in p]
    return _el(eid, "line", x0, y0, (max(xs) - min(xs)) or 1,
               (max(ys) - min(ys)) or 1, stroke=color, sw=sw, dashed=dashed,
               bg=bg, fill=fill,
               extra={"points": [[round(a - x0, 2), round(b - y0, 2)] for a, b in p],
                      "lastCommittedPoint": None, "startBinding": None,
                      "endBinding": None, "startArrowhead": None,
                      "endArrowhead": None})


def ell(eid, cx, cy, rx, ry, stroke="#1e1e1e", bg="transparent",
        sw=2, fill="solid", dashed=False):
    """Elipse/circunferencia con CENTRO (cx,cy) y semiejes rx,ry (en px canvas).
    Para circunferencia: rx=ry. Para un punto/dot: rx=ry chico + bg=stroke."""
    return _el(eid, "ellipse", cx - rx, cy - ry, 2 * rx, 2 * ry,
               stroke=stroke, bg=bg, sw=sw, fill=fill, dashed=dashed)


def rect(eid, x, y, w, h, stroke=GRAY, bg="#e9ecef", fill="hachure", sw=1):
    """Rectángulo (para sombrear regiones/cuadrantes)."""
    return _el(eid, "rectangle", x, y, w, h, stroke=stroke, bg=bg, sw=sw, fill=fill)


def arc(eid, cx, cy, r, a0_deg, a1_deg, color="#1e1e1e", sw=2):
    """Arco aproximado (para marcar un ángulo). Ángulos en grados; ojo que la y
    va hacia abajo, por eso se usa cy - r*sin()."""
    n = 16
    pts = [(cx + r * math.cos(math.radians(a0_deg + (a1_deg - a0_deg) * i / n)),
            cy - r * math.sin(math.radians(a0_deg + (a1_deg - a0_deg) * i / n)))
           for i in range(n + 1)]
    return poly(eid, pts, color, sw)


def write(path, elements, tags):
    """Valida el JSON y escribe el .excalidraw.md (frontmatter + envoltorio que
    el plugin de Obsidian reconoce). tags: string, ej 'excalidraw, matematica-2'."""
    scene = {"type": "excalidraw", "version": 2,
             "source": "https://github.com/zsviczian/obsidian-excalidraw-plugin/releases",
             "elements": elements,
             "appState": {"gridSize": None, "viewBackgroundColor": "#ffffff"},
             "files": {}}
    json.loads(json.dumps(scene))  # falla acá si el JSON quedó inválido
    body = ("---\nexcalidraw-plugin: parsed\ntags: [" + tags + "]\n---\n"
            "==⚠  Switch to EXCALIDRAW VIEW in the MORE OPTIONS menu of this document. ⚠==\n\n\n"
            "# Text Elements\n\n# Embedded files\n\n%%\n## Drawing\n```json\n"
            + json.dumps(scene, ensure_ascii=False, indent=2) + "\n```\n%%\n")
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w") as f:
        f.write(body)
    return len(elements)
