#!/usr/bin/env python3
"""Eine abgeschlossene Saison einfrieren: alle liga.nu-Seiten, die die App für diese
Saison je anfragt, einmal herunterladen und unter archiv/<ordner>/ ablegen.

    python3 tools/einfrieren.py "MS 2026" sommer-2026

Die App liest danach archiv/<ordner>/index.json: Die Datei ordnet jeder liga.nu-URL
die lokale Kopie zu; fetchURL() in index.html greift für die archivierte Saison
darauf zu, statt über die CORS-Proxys zu gehen. verein.html ist ein Schnappschuss
der Vereinsseite, aus dem die App Mannschaften und Kader der Saison parst — so
bleibt die Saison im Umschalter, auch wenn liga.nu sie nicht mehr listet.

Es wird nur gelesen; die Parser der App bleiben unverändert, weil die rohen
HTML-Seiten abgelegt werden."""

import json, re, sys, time, urllib.parse, urllib.request
from datetime import date
from pathlib import Path

BASE      = 'https://wtv.liga.nu'
CLUB_URL  = BASE + '/cgi-bin/WebObjects/nuLigaTENDE.woa/wa/clubTeams?club=26831'
LK_URL    = BASE + '/cgi-bin/WebObjects/nuLigaTENDE.woa/wa/clubRankinglistLK?federation=WTV&club=2015325'
PAUSE     = 0.4   # Sekunden zwischen zwei Abrufen

def holen(url):
    req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0 (Spielplan Ochtrup Archiv)'})
    for versuch in range(3):
        try:
            with urllib.request.urlopen(req, timeout=30) as r:
                text = r.read().decode('utf-8', 'replace')
            if len(text) < 200:
                raise ValueError('Antwort zu kurz')
            time.sleep(PAUSE)
            return text
        except Exception as e:
            print(f'   ! {e} – Versuch {versuch + 1}/3')
            time.sleep(2)
    raise SystemExit(f'Abbruch: {url} nicht ladbar')

def absolut(href):
    href = href.replace('&amp;', '&')
    return href if href.startswith('http') else BASE + href

def main():
    if len(sys.argv) != 3:
        raise SystemExit(__doc__)
    saison, ordner = sys.argv[1], sys.argv[2]
    ziel = Path(__file__).resolve().parent.parent / 'archiv' / ordner
    ziel.mkdir(parents=True, exist_ok=True)
    # so schreibt liga.nu die Saison in URLs: „MS 2026" → „MS+2026"
    saison_url = urllib.parse.quote_plus(saison)
    dateien = {}

    def speichern(url, name, html):
        (ziel / name).write_text(html, encoding='utf-8')
        dateien[url] = name

    print('Vereinsseite …')
    verein = holen(CLUB_URL)
    (ziel / 'verein.html').write_text(verein, encoding='utf-8')

    gruppen = []
    for m in re.finditer(r'href="([^"]*groupPage\?[^"]*)"', verein):
        url = absolut(m.group(1))
        if f'championship={saison_url}&' not in url and not url.endswith(f'championship={saison_url}'):
            continue
        g = re.search(r'[?&]group=(\d+)', url).group(1)
        if url not in dateien and g not in [x[0] for x in gruppen]:
            gruppen.append((g, url))
    if not gruppen:
        raise SystemExit(f'Keine Mannschaften für „{saison}" auf der Vereinsseite gefunden.')
    print(f'{len(gruppen)} Gruppenseiten …')
    berichte = {}
    for g, url in gruppen:
        html = holen(url)
        speichern(url, f'gruppe-{g}.html', html)
        for r in re.finditer(r'href="([^"]*meetingReport\?[^"]*)"', html):
            rurl = absolut(r.group(1))
            berichte[rurl] = re.search(r'meeting=(\d+)', rurl).group(1)
        print(f'   Gruppe {g}: {len(berichte)} Berichte bisher')

    print(f'{len(berichte)} Spielberichte …')
    for i, (url, meeting) in enumerate(sorted(berichte.items(), key=lambda x: x[1]), 1):
        speichern(url, f'bericht-{meeting}.html', holen(url))
        if i % 25 == 0:
            print(f'   {i}/{len(berichte)}')

    kader = []
    for m in re.finditer(r'href="([^"]*teamPortrait\?[^"]*)"', verein):
        url = absolut(m.group(1))
        if f'championship={saison_url}' in url and url not in kader:
            kader.append(url)
    print(f'{len(kader)} Kaderseiten …')
    for url in kader:
        team = re.search(r'team=(\d+)', url).group(1)
        speichern(url, f'kader-{team}.html', holen(url))

    print('LK-Listen …')
    speichern(LK_URL + '&gender=1', 'lk-herren.html', holen(LK_URL + '&gender=1'))
    speichern(LK_URL + '&gender=0', 'lk-damen.html',  holen(LK_URL + '&gender=0'))

    index = {
        'saison':    saison,
        'erstellt':  date.today().isoformat(),
        'verein':    'verein.html',
        'dateien':   dateien,
    }
    (ziel / 'index.json').write_text(json.dumps(index, ensure_ascii=False, indent=1), encoding='utf-8')
    groesse = sum(p.stat().st_size for p in ziel.iterdir()) / 1e6
    print(f'Fertig: {len(dateien) + 1} Dateien, {groesse:.1f} MB in {ziel}')

if __name__ == '__main__':
    main()
