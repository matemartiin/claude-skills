#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Extrae la capa de texto de un PDF de cátedra (parcial / final / TP "Resolución"),
normalizando el unicode "negrita matemática" (𝑭𝑽 → FV) con NFKC para que las
fórmulas y números queden EXACTOS y legibles (sin error de OCR).

Por cada página marca dónde empieza el primer carácter boldmath (= típicamente
donde arranca la SOLUCIÓN), para ayudarte a separar enunciado de solución.

Uso:
    python extract_solutions.py "ruta/al/PDF.pdf"                 # vuelca todo a stdout
    python extract_solutions.py "ruta/al/PDF.pdf" -o /tmp/SOL.txt # y/o a un archivo
    python extract_solutions.py "ruta/al/PDF.pdf" --map           # solo el mapa de ejercicios x página

Notas:
- Boldmath = rango unicode U+1D400–U+1D7FF (Mathematical Alphanumeric Symbols).
- NFKC también aplana superíndices/fracciones a ASCII; los enunciados (texto
  normal) quedan intactos.
- Si una fórmula queda desordenada (subíndices, raíces), abrí ESA página del PDF
  como imagen para desambiguar — el texto es fiel en los números, no siempre en el layout.
"""
import argparse
import sys
import unicodedata

try:
    from pypdf import PdfReader
except ImportError:
    try:
        from PyPDF2 import PdfReader
    except ImportError:
        sys.exit("Falta pypdf/PyPDF2:  pip install pypdf")


def first_boldmath(text):
    for i, ch in enumerate(text):
        if 0x1D400 <= ord(ch) <= 0x1D7FF:
            return i
    return None


def main():
    ap = argparse.ArgumentParser(description="Extrae texto NFKC de un PDF de cátedra.")
    ap.add_argument("pdf", help="ruta al PDF")
    ap.add_argument("-o", "--out", help="archivo de salida (además de stdout)")
    ap.add_argument("--map", action="store_true",
                    help="solo imprime el mapa de 'Ejercicio N' por página")
    args = ap.parse_args()

    r = PdfReader(args.pdf)
    chunks = []
    import re
    for i, pg in enumerate(r.pages):
        raw = pg.extract_text() or ""
        norm = unicodedata.normalize("NFKC", raw)
        if args.map:
            marks = sorted(set(re.findall(r"Ejercicio\s*\d+|Problema\s*\d+|^\s*\d+\)", norm, flags=re.M)))
            head = " | ".join(x.strip() for x in norm.strip().split("\n")[:2])
            chunks.append(f"p{i+1}: {head[:80]}   {marks[:5]}")
        else:
            pos = first_boldmath(norm)
            marker = "" if pos is None else f"   <<<BOLDMATH(solución?)@char {pos}"
            chunks.append(f"\n========== PÁGINA {i+1}{marker} ==========\n{norm}")

    text = "\n".join(chunks)
    print(text)
    if args.out:
        with open(args.out, "w", encoding="utf-8") as f:
            f.write(text)
        print(f"\n[escrito a {args.out}]", file=sys.stderr)
    if not args.map:
        print(f"\n[{len(r.pages)} páginas]", file=sys.stderr)


if __name__ == "__main__":
    main()
