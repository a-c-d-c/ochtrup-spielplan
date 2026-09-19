# Entscheidungen

> Warum die Dinge so sind, wie sie sind. Neue Entscheidung? Oben anfügen, mit Datum.

## 2026-09-19 — Abgeschlossene Saisons einfrieren (Sommer 2026)

Ansgars Entscheidung. Die Sommersaison 2026 ist gespielt (20 Mannschaften, 107
Begegnungen, keine offen). Alle liga.nu-Seiten, die die App für diese Saison je
anfragt, liegen jetzt als Kopie unter `archiv/sommer-2026/` — 20 Gruppenseiten, 328
Spielberichte (auch die fremder Begegnungen, damit die Gruppen-Detailansicht wie
gewohnt funktioniert), 20 Kaderseiten, beide LK-Listen, dazu ein Schnappschuss der
Vereinsseite. Rund 20 MB.

**Warum:** liga.nu vergibt Gruppen-Nummern je Saison neu und räumt alte Saisons
irgendwann aus der Vereinsseite. Ohne Kopie würde der Sommer 2026 von selbst
verschwinden oder falsche Daten zeigen. Außerdem hängt die Saison so nicht mehr an
den CORS-Proxys — dem häufigsten Ausfallgrund.

**Wie:** `tools/einfrieren.py "MS 2026" sommer-2026` lädt alles direkt von liga.nu
(ohne Proxy) und schreibt `index.json` (URL → Datei). In `index.html` steht der Ordner
in `ARCHIVE_DIRS`; `fetchURL()` liefert für die aktive Saison die lokale Kopie, sonst
geht es wie bisher über die Proxys. Die Parser blieben unverändert, weil rohes HTML
abgelegt wird — die App sieht dieselben Seiten wie vorher.

**Bewusst so:** Die LK-Listen sind auf liga.nu nicht saisonspezifisch. Eingefroren
zeigt die Sommer-Statistik die LKs vom 19.09.2026, also vom Saisonende — passender
als die Winter-LKs, die die Live-Variante später zeigen würde.

**Nächstes Mal:** Nach Ende der Wintersaison 2026/27 dasselbe Skript mit
`"MS Winter 26/27" winter-2026-27` laufen lassen und den Ordner in `ARCHIVE_DIRS`
eintragen (älteste zuerst).

## 2026-09-08 — Service Worker: `no-cache` ja, Caches löschen nein

Löst den offenen Punkt vom 17.08.2026 (weiter unten). Ansgars Entscheidung.

GitHub Pages liefert die Seite mit `cache-control: max-age=600` aus — der Browser darf
sie also **zehn Minuten** aus eigenem Speicher zeigen, ohne nachzufragen. Genau das ist
der Grund, warum eine Änderung auf dem Handy verzögert ankam. `sw.js` (jetzt `// v3`)
setzt deshalb für **eigene** Dateien `cache: 'no-cache'`; Anfragen an fremde Server
(liga.nu über die CORS-Proxys) bleiben unangetastet.

**Das Cache-Löschen aus der alten v2-Fassung wurde bewusst nicht übernommen** — es
bringt nichts (siehe unten) und wäre nur ein zusätzliches Risiko.

**Nebenbefund: Der Offline-Rückfall ist wirkungslos.** Weder die alte noch die neue
Fassung legt jemals etwas in den Cache — kein `caches.put`, kein `caches.add`. Das
`caches.match()` im Fehlerfall greift also ins Leere, und ohne Netz zeigt die App
nichts. Das ist verkraftbar, weil sie ihre Daten ohnehin live von liga.nu holt, aber
es erklärt, warum bei einem Proxy-Ausfall einfach eine leere Seite dasteht.

Die Konstruktion des umgeleiteten Requests steht in einem `try`/`catch`: Scheitert sie
in irgendeinem Browser, geht die ursprüngliche Anfrage durch, statt dass die Seite tot
ist.

## 2026-09-08 — Saison-Umschalter statt einer festen Saison

liga.nu listet auf der Vereinsseite in der Übergangszeit **beide Runden zusammen**
(Sommer 2026 und Winter 2026/27). Die App zeigte dadurch die Mannschaften beider
Saisons vermischt. Seitdem trennt sie nach der `championship` aus der liga.nu-URL,
und im Kopf stehen zwei Buttons zum Umschalten.

**Die Gruppen-Nummern zählen je Saison neu.** `group=18` ist im Sommer *Damen 30 4er 1*
und im Winter *Damen 40 4er 1* — deshalb hatte die alte Entdopplung eine Winter-Mannschaft
verschluckt. Die Mannschafts-Schlüssel (`g18`) sind nur **innerhalb** einer Saison
eindeutig; daran hängen Einstellungen, Favoriten und der Spielplan-Cache, die deshalb
jetzt je Saison getrennt gespeichert werden.

**Ein Saisonwechsel lädt die Seite neu.** Sauberer als alle Ansichten, Statistiken und
Caches einzeln umzuhängen — und dadurch kann sich nichts vermischen.

**Beim allerersten Start wählt die App die laufende Saison** anhand des nächsten
anstehenden Spiels (`clubMeetings`, ein Abruf). Danach gilt die gespeicherte Wahl.
Ohne das sähe ein Vereinsmitglied im September die leere, durchgespielte Sommerrunde.

**Die Spielberechtigungen im Jugendbereich bleiben saisonübergreifend** — sie gelten
weiter, unabhängig von der gewählten Runde (Ansgars Vorgabe).

## 2026-08-17 — ERLEDIGT (08.09.2026): zwei Service-Worker-Fassungen

Beim Umzug gefunden. Der lokale Ordner und die ausgelieferte Fassung unterscheiden
sich in `sw.js` um 18 Zeilen — **in allen anderen Dateien um null.**

| | Stand | Verhalten |
|---|---|---|
| **Live** (dieses Repo) | 13.06.2026 | einfach: reicht Anfragen durch, Cache nur als Rückfall |
| **Lokal** (alter Ordner) | 29.05.2026 | `// v2`: löscht beim Aktivieren **alle** Caches und erzwingt `no-cache` für eigene Dateien |

Die **lokale** Fassung ist die ausgefeiltere und löst ein bekanntes Problem: Ohne
`no-cache` auf eigenen Dateien wirkt eine Änderung beim Nutzer unter Umständen nicht,
weil der Browser die alte Fassung behält. Sie ist aber **älter** — live läuft die
einfachere.

**Ungeklärt: ob das Absicht war.** Deshalb wurde beim Umzug nichts überschrieben —
die ausgelieferte Fassung bleibt, die andere steht unten vollständig.

### Die lokale Fassung im Wortlaut

```javascript
// v2
self.addEventListener('install', () => self.skipWaiting());
self.addEventListener('activate', e => {
  e.waitUntil(
    caches.keys()
      .then(keys => Promise.all(keys.map(k => caches.delete(k))))
      .then(() => self.clients.claim())
  );
});
self.addEventListener('fetch', e => {
  const req = e.request.url.startsWith(self.location.origin)
    ? new Request(e.request, { cache: 'no-cache' })
    : e.request;
  e.respondWith(fetch(req).catch(() => caches.match(e.request)));
});
```
