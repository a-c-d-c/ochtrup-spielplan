# Entscheidungen

> Warum die Dinge so sind, wie sie sind. Neue Entscheidung? Oben anfügen, mit Datum.

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
