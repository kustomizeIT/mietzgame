#!/usr/bin/env python3
"""Baut index.html aus game.template.html (Level + Mietz-Sprite als Data-URI)."""
import base64, re, sys

COLS, ROWS = 170, 15
grid = [[" "] * COLS for _ in range(ROWS)]

def fill(c0, c1, r0, r1, ch):
    for c in range(c0, c1 + 1):
        for r in range(r0, r1 + 1):
            grid[r][c] = ch

def make_level2():
    """Serverraum: laenger, mehr Roboter, fahrende Plattformen, Endgegner."""
    cols = 200
    g = [[" "] * cols for _ in range(ROWS)]
    def f(c0, c1, r0, r1, ch):
        for c in range(c0, c1 + 1):
            for r in range(r0, r1 + 1):
                g[r][c] = ch
    # Boden-Segmente (Luecken max 3 Felder = springbar)
    segs = [(0,14),(18,29),(33,47),(51,64),(68,79),(83,95),(99,111),(115,126),(130,142),(146,158),(162,174),(178,199)]
    for s0, s1 in segs:
        f(s0, s1, 13, 14, "#")
    # Plattformen
    for p0, p1, r in [(5,8,10),(10,12,8),(20,23,9),(26,28,7),(35,37,10),(40,43,8),(46,48,10),(53,55,9),(57,59,7),(61,63,10),(70,72,8),(75,77,10),(85,87,9),(89,92,7),(96,98,10),(103,105,8),(108,110,10),(117,119,9),(122,124,7),(128,130,10),(133,135,8),(138,140,10),(148,150,9),(153,155,7),(159,161,10),(165,167,8),(170,172,10),(180,183,9),(186,188,7),(191,193,10)]:
        f(p0, p1, r, r, "=")
    # Fische
    fish = [(6,11),(7,11),(10,7),(21,7),(27,5),(36,8),(41,6),(47,8),(54,7),(58,5),(62,8),(71,6),(76,8),(86,7),(90,5),(97,8),(104,6),(109,8),(118,7),(123,5),(129,8),(134,6),(139,8),(149,7),(154,5),(160,8),(166,6),(171,8),(181,7),(187,5),(192,8)]
    for c, r in fish:
        g[r][c] = "f"
    # Roboter (7)
    for c in [15, 38, 60, 86, 106, 137, 168]:
        g[12][c] = "e"
    # Fahrende Plattformen (3)
    g[11][31] = "m"
    g[10][66] = "m"
    g[11][113] = "m"
    g[11][144] = "m"
    # Endgegner + Ziel
    g[12][188] = "B"
    g[12][197] = "G"
    g[12][2] = "P"
    return ["".join(r) for r in g], cols

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

level = ["".join(r) for r in grid]
assert all(len(r) == COLS for r in level)
level2, cols2 = make_level2()
assert all(len(r) == cols2 for r in level2)
js_level = "[\n[" + ",\n".join('"%s"' % r for r in level) + "],\n[" + ",\n".join('"%s"' % r for r in level2) + "]\n]"

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
