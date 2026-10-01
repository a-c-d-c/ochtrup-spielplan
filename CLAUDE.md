# Spielplan Ochtrup — Regeln für die Arbeit an diesem Projekt

> Router. Was die App tut, steht im [README](README.md).
> Entscheidungen und offene Punkte: [`docs/entscheidungen.md`](docs/entscheidungen.md).

## Was das hier ist

Eine **statische PWA** für den Spielplan des TC 1928 Ochtrup — kein Server, keine
Datenbank. `index.html` trägt alles: Aufbau, Gestaltung und Logik. Die Spieldaten holt
die Seite zur Laufzeit direkt von **liga.nu** über CORS-Proxys.

Ausgeliefert wird über **GitHub Pages**: `a-c-d-c.github.io/ochtrup-spielplan/`
(im Dock als „Spielplan").

## Nur Ochtrup

Es gab einmal vier weitere Vereins-Ordner (Rheine, Ahaus, Feldmark, eine „pro"-Variante)
und ein Verteilskript `propagate.py`. **Sie gehören seit dem 17.08.2026 nicht mehr zu
diesem Projekt** (Ansgars Entscheidung). Sie liegen unberührt im Archiv unter
`KI Betriebssystem/Module/Hobby/Spielplaene`.

**Nicht wieder anfangen, hier für mehrere Vereine zu bauen**, ohne dass Ansgar es
ausdrücklich will.

## Vor jeder Änderung: der Live-Stand ist die Wahrheit

Dieses Projekt hatte lange **zwei auseinandergelaufene Arbeitskopien**, und der Ordner
mit dem irreführenden Namen war der richtige. Damit das nicht wiederkommt:

```bash
curl -s https://a-c-d-c.github.io/ochtrup-spielplan/index.html -o /tmp/live.html
diff /tmp/live.html index.html
```

**Null Abweichungen = der Arbeitsstand ist der Live-Stand.** Weicht etwas ab, erst
klären, welcher gilt — nicht drauflosarbeiten.

## Wie ausgeliefert wird

Die Live-Historie besteht aus Commits namens „Add files via upload" — die Dateien wurden
bisher über die **GitHub-Weboberfläche** hochgeladen, nicht gepusht. Seit dem Umzug ist
dieser Ordner ein echter Klon mit richtigem Remote, `git push` funktioniert also.

**Ausliefern ist nach außen sichtbar** — es ist die Seite eines fremden Vereins. Vor
einem Push fragen.

## Vorsicht bei den CORS-Proxys

Die Seite holt liga.nu-Daten über fremde Vermittler (`api.allorigins.win`,
`corsproxy.io`, `api.codetabs.com`, dazu ein eigener Cloudflare Worker). Fällt einer
aus, bleibt die Seite leer, **ohne Fehlermeldung** — das ist der wahrscheinlichste
Grund, wenn „nichts mehr geht". Zuerst in der Browser-Konsole nachsehen, nicht im Code
suchen.

## Am Bildschirm prüfen

Es ist eine Oberfläche. Nach jeder Änderung im Browser ansehen — hell **und** dunkel,
und in Handybreite. Eine Messung ersetzt hier keinen Blick.
