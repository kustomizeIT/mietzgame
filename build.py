#!/usr/bin/env python3
"""Baut index.html aus game.template.html (Level + Mietz-Sprite als Data-URI)."""
import base64, re, sys

COLS, ROWS = 170, 15
grid = [[" "] * COLS for _ in range(ROWS)]

def fill(c0, c1, r0, r1, ch):
    for c in range(c0, c1 + 1):
        for r in range(r0, r1 + 1):
            grid[r][c] = ch

for g0, g1 in [(0,18),(22,34),(39,51),(56,68),(76,88),(93,105),(110,122),(127,139),(144,156),(160,169)]:
    fill(g0, g1, 13, 14, "#")
for p0, p1, r in [(8,11,10),(24,26,8),(30,33,9),(43,45,10),(59,61,7),(64,66,10),(82,85,10),(88,90,8),(99,101,8),(102,104,11),(116,118,10),(121,123,8),(133,135,9),(138,140,11),(148,150,9),(162,164,9)]:
    fill(p0, p1, r, r, "=")
for c, r in [(3,11),(4,11),(5,11),(9,8),(10,8),(11,8),(25,6),(26,6),(31,7),(32,7),(44,8),(45,8),(60,5),(61,5),(65,8),(66,8),(72,9),(73,9),(74,9),(83,8),(84,8),(85,8),(89,6),(90,6),(100,6),(101,6),(103,9),(117,8),(118,8),(122,6),(134,7),(135,7),(139,9),(149,7),(150,7),(163,7),(164,7)]:
    grid[r][c] = "f"
for c in [12, 28, 44, 62, 80, 98, 116, 132, 148]:
    grid[12][c] = "e"
grid[11][72] = "m"
grid[12][2] = "P"
grid[12][166] = "G"
for c in [16, 48, 85, 111, 153]:
    grid[12][c] = "Q"

level = ["".join(r) for r in grid]
assert all(len(r) == COLS for r in level)
js_level = "[\n" + ",\n".join('"%s"' % r for r in level) + "\n]"

def datauri(path):
    return "data:image/png;base64," + base64.b64encode(open(path, "rb").read()).decode()

import json as _json
quiz = _json.load(open("quiz.json"))

html = open("game.template.html").read()
assert "__LEVEL__" in html and "__LOGO_B64__" in html and "__MIETZ_B64__" in html and "__QUIZ__" in html
assert "__SHEET_META__" in html and "__SHEET_SRC__" in html
html = html.replace("__LEVEL__", js_level)
html = html.replace("__QUIZ__", _json.dumps(quiz, ensure_ascii=False, separators=(",", ":")))
html = html.replace("__LOGO_B64__", datauri("logo_small.png"))
html = html.replace("__MIETZ_B64__", datauri("kustomize_intro.png"))
sheet_meta = _json.load(open("frames.json"))
sheet_src = {}
for _n in sheet_meta:
    sheet_src[_n] = datauri("spr_%s.png" % _n)
html = html.replace("__SHEET_META__", _json.dumps(sheet_meta, separators=(",", ":")))
html = html.replace("__SHEET_SRC__", _json.dumps(sheet_src, separators=(",", ":")))
open("index.html", "w").write(html)
print("index.html geschrieben:", len(html), "Bytes")
