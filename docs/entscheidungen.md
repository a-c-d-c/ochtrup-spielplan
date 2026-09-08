# Entscheidungen

> Warum die Dinge so sind, wie sie sind. Neue Entscheidung? Oben anfügen, mit Datum.

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

## 2026-08-17 — OFFEN: zwei Service-Worker-Fassungen

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
