# Kustomize Adventure 🐱

Ein kleines Jump-'n'-Run-Browser-Spiel mit dem Maskottchen **Mietz** – im Stil von Super Mario Land. Läuft als **eine einzige, eigenständige HTML-Datei** ohne externe Abhängigkeiten. Ideal als Easter Egg auf der Webseite oder per **QR-Code auf Printmedien**.

## Spielen

Einfach `index.html` auf einen Webserver hochlegen (z. B. `https://deine-webseite.de/mietz/`) und im Browser öffnen.

**Steuerung**

| Aktion | Desktop | Handy |
|---|---|---|
| Laufen | Pfeiltasten / A, D | ◄ ► Buttons |
| Springen | Leertaste / ↑ / W | rosa Sprung-Button |
| Neustart | Enter | Button im Overlay |

## Features

- 37 rosa Fische sammeln, 3 Leben (Herzen)
- Staubsauber-Roboter: draufspringen lässt sie albern davonfliegen (X-Augen, Funken) – gibt einen rosa Bonuspunkt (+1, Stern-Zähler im HUD)
- Bewegliche Plattform, Ziel-Körbchen mit Fahne
- Sound-Effekte (WebAudio, keine Audiodateien)

## Aussehen

Kustomizes Kopf stammt **direkt aus der Original-SVG** des Maskottchens (via `kustomize_head.png` als Data-URI eingebettet): exaktes Gesicht mit grünem Fellfleck über dem rechten Auge bis zur Stirn, Weißeck, Schnurrhaaren. Blinzeln/geschlossene Augen werden als Fellfarben-Überlagerung auf dem SVG-Kopf animiert.

## KI-Quiz

Quiz-Fragen &ouml;ffnen sich, **wenn man auf einen Staubsauger-Roboter springt** &ndash; wer die Roboter umgeht, spielt automatisch einen Speedrun ohne Fragen:

- **Balancierter Fragen-Pool**: Die 50 Fragen wechseln systematisch zwischen Leicht/Mittel/Schwer &ndash; niemand bekommt nur schwere oder nur leichte Fragen
- **3 Antwortoptionen** (gemischt, Tasten 1&ndash;3 oder antippen)
- **25-Sekunden-Countdown** &ndash; genug Zeit zum Lesen und Verstehen; l&auml;uft er ab, gilt die Frage als falsch
- **Richtig: +5 Bonuspunkte** (plus +1 f&uuml;r den Roboter-KO), danach erscheint die kurze Erkl&auml;rung &ndash; Lerneffekt!
- Falsch/Timeout: Aufl&ouml;sung mit Erkl&auml;rung, 0 Punkte
- Das Spiel pausiert w&auml;hrend des Quiz; die Statistik erscheint im Sieg-Screen
- **Speedrun-Timer** im HUD (l&auml;uft nur im Spiel, pausiert im Quiz)
- **Highscore-Liste**: Nach dem Sieg Namen eintragen &ndash; Top 10 nach Punkten/Zeit (lokal im Browser gespeichert, da das Spiel eine serverlose Einzeldatei ist)
- Fragenkatalog: Grundlagen, Modelle &amp; Technik, Datenschutz/DSGVO, EU AI Act, Alltag &amp; Beruf (F01&ndash;F50, inkl. Schwierigkeitsgrad- und &bdquo;Kracher&ldquo;-Badge)

## Animationen

Mietz wird prozedural in Canvas gezeichnet (kein starres Bild) und reagiert auf das Spielverhalten:

- **Stehen** (kurz): sitzt aufrecht, blinzelt zufällig alle 2–5 s, wedelt mit dem Schwanz
- **Lecken** (nach ~4 s Stillstand): hebt die Pfote zur Schnauze und leckt sich mit rosa Zunge
- **Schlafen** (nach 10 s Stillstand): legt sich hin, Augen zu, Atembewegung, „Z z z" steigt auf
- **Aufwachen**: bei Eingabe hüpft sie kurz auf und legt los
- **Rennen**: Laufzyklus mit Beinen, Körperneigung und Schweif
- **Springen/Fallen**: gestreckte bzw. gespreizte Pose, Ohren nach oben
- **Landen**: Kurzzeitiges Zusammendrücken (Squash) mit Staubpartikeln
- Touch-Optimierung: keine versehentliche Zoom/Scroll-Gesten, Safe-Area-Support
- Brand-Farben: Grün `#8CC9A5` (Logo-Grün: `#82DCA8`), Pink `#FF66C4`, Blau `#5CE1E6`, Navy `#282E3B` / `#181D23`
- Intro im kustomize.it-Branding: Logo, KUSTOMIZE.IT-Wordmark und das Darwin-Zitat mit der Katze
- Mietz-Sprite ist als Data-URI eingebettet – die Datei funktioniert überall, auch offline

## Veröffentlichen mit GitHub Pages (für den QR-Code)

1. Repo auf GitHub öffnen → **Settings → Pages**
2. Source: **Deploy from a branch**, Branch: `main`, Ordner: `/ (root)`
3. Die URL lautet dann: `https://kustomizeit.github.io/mietzgame/`
4. Einen QR-Code auf diese URL generieren (z. B. mit einem beliebigen QR-Generator) und aufs Printmaterial drucken

Alternativ: `index.html` einfach in einen beliebigen Ordner der bestehenden Webseite kopieren.

## Dateien

- `index.html` – das fertige, eigenständige Spiel (nur diese eine Datei wird benötigt)
- `game.template.html` – Quellcode-Vorlage (Platzhalter für das Level)
- `build.py` – generiert `index.html` aus der Vorlage (Level einbetten)
- `kustomize_head.png` – Kopf aus der Original-Maskottchen-SVG für die Spielfigur (als Data-URI eingebettet)
- `kustomize_intro.png` – Original-Maskottchen für das Intro-Zitat (aus der SVG gerendert)
- `quiz.json` – 50 KI-Quizfragen (aus dem Fragenkatalog generiert; wird per `build.py` eingebettet)
- `logo_small.png` – kustomize.it-Logo für das Intro (als Data-URI eingebettet)

## Level anpassen

Das Level ist eine ASCII-Karte in `build.py` (bzw. direkt im `LEVEL`-Array in `index.html`):

| Zeichen | Bedeutung |
|---|---|
| `#` | Boden/Block |
| `=` | Einweg-Plattform (blau) |
| `f` | Fisch (Sammelobjekt) |
| `e` | Staubsauber-Roboter |
| `m` | Bewegliche Plattform (rosa) |
| `P` | Startpunkt |
| `G` | Ziel (Körbchen) |

Nach Änderungen in `game.template.html` oder `build.py`: `python3 build.py` ausführen – das schreibt die neue `index.html`.
