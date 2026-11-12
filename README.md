# Mietz Adventure 🐱

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
- Staubsauber-Roboter: draufspringen schaltet sie aus
- Bewegliche Plattform, Ziel-Körbchen mit Fahne
- Sound-Effekte (WebAudio, keine Audiodateien)

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
- Brand-Farben: Grün `#8CC9A5`, Pink `#FF66C4`, Blau `#5CE1E6`, Navy `#282E3B`
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
- `mietz_small.png` – kleiner Mietz-Sprite (Referenz; im Spiel wird die Katze prozedural animiert gezeichnet)

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
