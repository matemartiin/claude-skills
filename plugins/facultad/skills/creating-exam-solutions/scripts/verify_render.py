#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Verifica que un archivo .md de Obsidian con matemática + currency no rompa el render.

Chequea, separando SIEMPRE el currency (\\$) de la matemática ($...$) para no dar
falsos positivos:
  - balance de delimitadores $ de math (debe ser PAR)
  - líneas con un número impar de $ de math (un span sin cerrar)
  - % CRUDO dentro de un span de math (rompe MathJax: % inicia comentario)
  - $$ display (frágil dentro de callouts)
  - doble-escape de currency (\\\\$ → barra visible)
  - conteo de callouts plegables [!success]-/[!warning]- (pasale --expect N)

Uso:
    python verify_render.py "archivo.md"
    python verify_render.py "archivo.md" --expect 66      # exige 66 callouts plegables

Sale con código 0 si todo OK, 1 si hay algún problema real.
"""
import argparse
import re
import sys


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("file")
    ap.add_argument("--expect", type=int, default=None,
                    help="cantidad esperada de callouts plegables [!...]-")
    args = ap.parse_args()

    c = open(args.file, encoding="utf-8").read()
    lines = c.split("\n")
    problems = 0

    # 1) doble-escape de currency
    dbl = c.count(r"\\$")
    if dbl:
        print(f"✗ Currency doble-escapado (\\\\$): {dbl} casos — deberían ser \\$ simples")
        problems += 1

    # 2) balance de $ de math (quitando el currency \$)
    no_curr = c.replace(r"\$", "")
    nmath = no_curr.count("$")
    if nmath % 2 == 0:
        print(f"✓ $ de math balanceados (PAR): {nmath}")
    else:
        print(f"✗ $ de math IMPAR: {nmath} — hay un span sin cerrar")
        problems += 1

    # 3) líneas con $ impar (tras quitar currency)
    odd = [i for i, l in enumerate(lines, 1) if l.replace(r"\$", "").count("$") % 2 == 1]
    if odd:
        print(f"✗ Líneas con $ de math impar: {odd}")
        for i in odd[:10]:
            print(f"    L{i}: {lines[i-1][:110]}")
        problems += 1
    else:
        print("✓ 0 líneas con $ impar")

    # 4) % crudo dentro de spans math REALES (marcar currency con placeholder primero)
    clean = c.replace(r"\$", "§")          # neutraliza el currency
    raw = []
    for i, l in enumerate(clean.split("\n"), 1):
        for span in re.findall(r"\$([^$]+?)\$", l):     # span math real
            if re.search(r"(?<!\\)%", span):
                raw.append((i, span[:55]))
    if raw:
        print(f"✗ % CRUDO dentro de math (rompe MathJax): {len(raw)} — deben ser \\%")
        for i, s in raw[:10]:
            print(f"    L{i}: [{s}]")
        problems += 1
    else:
        print("✓ 0 % crudo real dentro de math")

    # 5) $$ display
    dd = no_curr.count("$$")
    if dd:
        print(f"⚠ $$ display: {dd} — frágiles dentro de callouts; preferí inline $…$ con \\dfrac")
    else:
        print("✓ 0 $$ display")

    # 6) conteo de callouts plegables
    n_call = c.count("[!success]-") + c.count("[!warning]-") + c.count("[!note]-") + c.count("[!tip]-")
    if args.expect is not None:
        ok = "✓" if n_call == args.expect else "✗"
        print(f"{ok} Callouts plegables: {n_call} (esperado {args.expect})")
        if n_call != args.expect:
            problems += 1
    else:
        print(f"· Callouts plegables: {n_call}")

    print()
    if problems:
        print(f"RESULTADO: {problems} problema(s) — revisá arriba.")
        sys.exit(1)
    print("RESULTADO: render OK ✓")
    sys.exit(0)


if __name__ == "__main__":
    main()
