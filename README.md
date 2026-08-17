# Spielplan 26 — TC 1928 Ochtrup

Eine statische Web-App (PWA), die den Spielplan der Mannschaften zeigt: Begegnungen,
Ergebnisse, Tabellen, Favoriten und Spielberichte. Die Daten kommen zur Laufzeit direkt
von **liga.nu**, es gibt keinen eigenen Server und keine Datenbank.

## Wo sie läuft

**https://a-c-d-c.github.io/ochtrup-spielplan/** — im Dock als „Spielplan 26".
Ausgeliefert über GitHub Pages aus diesem Repository.

## Dateien

| Datei | Wozu |
|---|---|
| `index.html` | die ganze App — Aufbau, Gestaltung und Logik in einer Datei |
| `info.html` | Hinweisseite |
| `manifest.json` · `sw.js` | machen sie zur installierbaren App (Homescreen, offline) |
| `logo.png` · `logo2.png` | Vereinswappen |
| `index-alt.html` | ältere Fassung, liegt im Repo |

## Ändern und ausliefern

1. `index.html` bearbeiten.
2. Im Browser ansehen — hell, dunkel und in Handybreite.
3. Committen.
4. Ausliefern per `git push`. **Das ist sofort öffentlich sichtbar** — es ist die Seite
   eines Vereins. Vorher fragen.

## Offener Punkt

`sw.js` liegt in zwei Fassungen vor, die sich im Caching-Verhalten unterscheiden.
Welche gelten soll, ist noch nicht entschieden — siehe [`docs/entscheidungen.md`](docs/entscheidungen.md).
