# Kustomize Adventure – Projekt-Dokumentation

**Stand:** 15.11.2026 · **Live-Spiel:** https://kustomizeit.github.io/mietzgame/
**Repository:** https://github.com/kustomizeIT/mietzgame (GitHub Pages aktiv)

Diese Dokumentation ermöglicht es, in einer neuen Session nahtlos am Projekt
weiterzuarbeiten. Sie enthält alles Wichtige über Stand, Architektur,
Build-Prozess und offene Aufgaben.

---

## 1. Worum geht es?

Ein Jump-'n'-Run-Browserspiel als Marketing-Easter-Egg für **kustomize.it**
(eine KI-/IT-Firma). Die Katze „Kustomize" (das Firmen-Maskottchen) läuft durch
ein Level, sammelt Fische, schaltet Staubsauger-Roboter aus und beantwortet
KI-Quizfragen. Zielgruppe: Kunden und Interessenten, die über einen QR-Code
(Printmedien) oder die URL auf das Spiel stoßen.

**Design-Sprache (Firmen-Branding):**
- Farben: Weiß (Fell), Sanftgrün `#8CC9A5` (Konturen/Flecken), Dunkelgrün
  `#6FAE8A` (Details/Lidstriche), Pink `#FF66C4` (Akzente), Navy `#282E3B`
  (Text)
- Logo + Wordmark „KUSTOMIZE.IT" im Intro, Darwin-Zitat über Anpassungsfähigkeit
- Font: Verdana (muss nicht geladen werden – überall verfügbar)

## 2. Aktueller Feature-Stand (live)

| Feature | Umsetzung |
|---|---|
| **Katzen-Animation** | 23 Frames aus dem generierten Sprite-Sheet (`spr_*.png`): Laufen (8-Frame-Galopp, Tempo ∝ Laufgeschwindigkeit), Springen (3 Phasen), Fallen, Landen (Squash), Sitzen/Atmen, Lecken (nach ~4 s Idle), Schlafen + „Zzz" (nach 10 s Idle) |
| **KI-Quiz** | Trigger: **Bespringen eines Roboters** (Quiz-Säulen wurden entfernt). Wer Roboter umgeht = Speedrun ohne Fragen |
| **Fragen** | 50 Fragen (F01–F50, Kategorien: Grundlagen, Modelle & Technik, DSGVO, EU AI Act, Alltag & Beruf), Schwierigkeits-Badge + „Kracher"-Tag, kurze Erklärungen nach jeder Antwort (Lerneffekt) |
| **Schwierigkeits-Balance** | Pool wechselt systematisch Leicht → Mittel → Schwer → … (niemand bekommt nur schwere/leichte Fragen) |
| **Quiz-UI** | **3 Antwortoptionen** (gemischt), **25 s Countdown** (Balken, unter 5 s pink), Tasten 1–3 oder Touch, „Weiter" → Enter |
| **Punkte** | Roboter-KO +1 · richtige Antwort **+5** · Fische zählen mit. HUD: Herzen, Fische, Sterne (Bonus), Timer, 🔊 Musik-Toggle |
| **Speedrun** | Timer im HUD (pausiert während Quiz), Zeit im Sieg-Screen |
| **Highscore** | Sieg-Screen: Name eintragen → Top 10 nach Punkten/Zeit. **Lokal im Browser (localStorage)** – serverübergreifend wäre ein Backend nötig (offen) |
| **Musik** | „Kustomize Alley Run" als `bgm.mp3` (1,3 MB, mono 64 kbps, Endlosschleife), Volume 0.15 (deutlich unter den SFX), Start mit „Los geht's!" (Autoplay-Policy), 🔊/🔇-Toggle im HUD |
| **Soundeffekte** | WebAudio-Oszillatoren (Sprung, Fisch, Treffer, Stomp, Sieg) – keine Dateien nötig |
| **Roboter** | Staubsauger mit Augen, patrouillieren; Besprung = KO (fliegen mit X-Augen + Funken weg) |
| **Steuerung** | Pfeiltasten/WASD + Leerzeichen; Touch-Buttons auf Mobil (pointer events, `touch-action:none`) |
| **Robustheit** | `"use strict"` im Browser! `roundRect`-Polyfill für alte Safari, try/catch um den Spiel-Loop mit **sichtbarer Fehlermeldung** (rosa Kasten oben) statt stillem Tod |

## 3. Architektur & Dateien

```
mietzgame/
├── index.html          ← DAS SPIEL (generiert, ~267 KB, alles eingebettet:
│                          Level, Quiz-Daten, 23 Sprites als Data-URIs, CSS, JS)
├── game.template.html  ← QUELLE für index.html (mit __PLATZHALTERN__)
├── build.py            ← Generator: baut index.html aus dem Template
├── frames.json         ← Sprite-Metadaten (ox/oy/w/h je Frame, Ansatzpunkte)
├── quiz.json           ← 50 Quizfragen (aus dem Fragenkatalog geparst)
├── spr_*.png           ← 23 zugeschnittene Animations-Frames (99 KB gesamt)
├── bgm.mp3             ← Hintergrundmusik (1,3 MB, als eigene Datei neben dem Spiel)
├── README.md           ← Feature-Übersicht (für Nutzer)
└── (historisch) svg_*.png, runpart_*.png  ← frühere Posen-Versionen, ungenutzt
```

**Build-Prozess (wichtig für neue Sessions):**
```bash
python3 build.py        # liest game.template.html + frames.json + quiz.json
                        # + spr_*.png → schreibt index.html
```
Platzhalter im Template: `__LEVEL__`, `__QUIZ__`, `__SHEET_META__`,
`__SHEET_SRC__`, `__LOGO_B64__`, `__MIETZ_B64__`. build.py asserted, dass alle
ersetzt wurden – ein fehlender Platzhalter bricht den Build.

**Level:** wird in build.py als ASCII-Grid generiert (13 Zeilen × ~167 Spalten,
TILE=48): `#`=Gras, `=`=Plattformen, `f`=Fische, `e`=Roboter, `m`=fahrende
Plattformen, `P`=Start, `G`=Ziel-Körbchen. Boden-Linie der Katzen-Sprites:
y=359 (alte SVG-Posen) bzw. y=385 (Sprite-Sheet), Anker X=260.

## 4. Spiel-Code-Kernpunkte (game.template.html)

- `"use strict"` am Anfang – **Achtung bei Tests:** Node-Harness ohne
  Strict Mode erkennt Tippfehler wie Zuweisungen an undeklarierte Variablen
  NICHT (das war der Start-Button-Bug!). Immer den Strict-Mode-Test laufen
  lassen (siehe Abschnitt 6).
- Zustandsmaschine: `state ∈ {start, play, quiz, win, over}`. Quiz pausiert die
  Welt (`update()` returned früh), Countdown läuft separat.
- `drawCat()` wählt Frame nach Zustand (vy, landT, idleTime, anim) und zeichnet
  mit Anker (Füße-Mitte): `drawImage(img, (M.ox-260)*CAT_S, (M.oy-385)*CAT_S, …)`
  mit `CAT_S = 64/351`, gespiegelt bei Laufrichtung links.
- Musik: `const bgm = new Audio("bgm.mp3")` – **relative URL**, Datei liegt im
  Repo-Root, GitHub Pages serviert sie neben index.html.
- Highscores: `localStorage.getItem("kustomizeHS")`, Top 10, Sortierung
  Punkte ↓ dann Zeit ↑.

## 5. Historie / Entscheidungen (warum es so ist)

1. **Frontale Kopf-Version** (SVG-Kopf der Katze auf prozeduralem Körper) →
   funktionierte, war aber „nachgebaut".
2. **Seitenansicht aus einzelnen Posen-SVGs** (sitzend/laufend/…) → statisch.
3. **Teil-Animation** (Fernbeine/Schweif aus der Lauf-SVG rotiert) → Test,
   wurde verworfen („nicht lebendig genug").
4. **Sprite-Sheet** (vom Kunden per KI generiert, 6 Zeilen × Frames) →
   **aktuelle Lösung**: echte Frame-Animation, alle 23 Frames pixelgenau
   am Boden verankert (Boden y=385 konstant verifiziert).
5. Quiz-Trigger wanderten von **Säulen** (Blockieren des Speedruns) zu
   **Roboter-Besprung** (Spieler kann Fragen umgehen = Speedrun-Pfad frei).
6. Fragenkatalog: vom Kunden geliefert (Markdown, F01–F50) → automatisch nach
   `quiz.json` geparst (Parser in der Session-Historie; bei neuen Fragen:
   IDs fortführen ab F51, Antwort markieren, Kracher-Tag optional).

## 6. Tests (in neuer Session wiederherstellen)

Die Test-Harness-Dateien (stub.js, bot.js, quiztest2.js, render_poses.js)
liegen NICHT im Repo (nur in der Arbeits-Sandbox). Wichtigste Tests:
- **Strict-Mode-Ladetest:** Spielcode in `new Function(code)()` mit
  Browser-Stubs (document, Image, Audio, localStorage, matchMedia, rAF)
  ausführen – fängt Ladefehler wie den Start-Button-Bug.
- **Bot-Durchlauf:** simulierter Lauf bis Ziel (state=win).
- **Quiz-Flow:** Stomp → Quiz öffnet, 3 Optionen, 25 s, +5, Timeout, Highscore.
- Stubs brauchen: `document.getElementById` (elStub mit classList/style),
  `querySelectorAll→[]`, `localStorage`, `Audio`, `Image`,
  `CanvasRenderingContext2D`, `matchMedia`, `requestAnimationFrame`,
  `performance.now`.

## 7. Deploy-Prozess

```bash
# Änderungen in Sandbox bauen & testen, dann:
cd /workspace/github__kustomizeIT__mietzgame
cp <sandbox>/index.html <sandbox>/game.template.html <sandbox>/build.py .
git checkout -b vibe/<name>     # Branch, committen, pushen
git checkout main && git merge --ff-only vibe/<name> && git push origin main
# GitHub Pages baut automatisch; prüfen:
gh api repos/kustomizeIT/mietzgame/pages/builds/latest --jq '{status,commit}'
```
- Pages-URL: https://kustomizeit.github.io/mietzgame/
- **Cache-Falle:** Browser/CDN cachen hart → beim Testen immer neu laden
  (Strg+F5) und den Nutzer darauf hinweisen.
- Git-Tag `v1-stabil` markiert den stabilen Stand vor den Experimenten.

## 8. Offene Aufgaben / Ideen des Kunden

- [ ] **Frontalansicht**: Katze schaut den Spieler am Anfang an (~1,5 s) und
      kurz nach jedem Quiz frontal. Kunde generiert dafür noch ein Frontal-
      Sprite-Sheet (gleiche Regeln: horizontale Reihe, transparenter
      Hintergrund, gleiche Boden-Linie). Einbau: Frame-Auswahl in `drawCat()`
      über `frontalT`-Timer (Abbruch bei Eingabe), setzen in `startGame()`
      und `closeQuiz()`.
- [ ] **Geräteübergreifende Highscore-Liste** (bräuchte Backend/Cloud-Service,
      aktuell nur localStorage pro Gerät).
- [ ] Musik-Lautstärke feintunen (aktuell 0.15) falls Kunde es lauter/leiser will.
- [ ] Blinzeln fehlt in der Sprite-Sheet-Version (Sitz-Frames haben nur offene
      Augen) – Kunde könnte „sitzend-augen-zu"-Frames nachliefern.
- [ ] Unbenutzte Alt-Dateien aufräumen (svg_*.png, runpart_*.png, alte
      Preview-Sheets) – optional.

## 9. Kontaktwege & Assets des Kunden

- Fragenkatalog: vom Kunden als Markdown geliefert (KI-Quiz 50 Fragen)
- Sprite-Sheet: `mieze-spritesheet.svg` (23 eingebettete Frame-SVGs,
  viewBox „-70 -27 480 400" je Frame, 6-Zeilen-Raster)
- Musik: „Kustomize Alley Run" (Original 4,1 MB → optimiert auf 1,3 MB mono
  64 kbps); Original auch unter
  https://kustomize.it/downloads/Kustomize_Alley_Run.mp3
- Maskottchen-Original: `kustomize_intro.png` (Intro-Zitat), `logo_small.png`
- Kunden-SharePoint-Ordner „Game":
  https://redballooner.sharepoint.com/:f:/s/KUSTOMIZE/IgDi6SyxERo8Qq3zqSbPJWSaAfHWshVcNrAG8uhjxpPKYbA
  (⚠️ SharePoint-Connector der Sessions ist auf Mandant `eagmerx.sharepoint.com`
  authentifiziert – Ordner liegt bei `redballooner.sharepoint.com`, dort kann
  die Session nicht direkt hochladen. Dateien aus dem Repo manuell kopieren.)

## 10. Schnellstart für eine neue Session

1. Repo klonen: `gh repo clone kustomizeIT/mietzgame` → diese Doku und README lesen
2. `python3 build.py` muss ohne Fehler durchlaufen
3. Änderungen immer am `game.template.html`/`build.py` machen, nie an
   `index.html` direkt (wird generiert!)
4. Nach jedem Build: Syntax-Check + Strict-Mode-Ladetest + Bot-Durchlauf
5. Deploy über Branch + ff-Merge auf main (Abschnitt 7)
