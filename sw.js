// v3
self.addEventListener('install', () => self.skipWaiting());
self.addEventListener('activate', e => e.waitUntil(self.clients.claim()));

/* Eigene Dateien immer beim Server nachfragen. GitHub Pages liefert sie mit
   cache-control: max-age=600 aus — ohne diesen Zusatz zeigt der Browser nach
   einer Änderung bis zu 10 Minuten die alte Fassung. Anfragen an fremde Server
   (liga.nu über die CORS-Proxys) bleiben unangetastet. */
self.addEventListener('fetch', e => {
  let req = e.request;
  if (req.url.startsWith(self.location.origin)) {
    try { req = new Request(req, { cache: 'no-cache' }); } catch (err) { req = e.request; }
  }
  e.respondWith(fetch(req).catch(() => caches.match(e.request)));
});
