#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
lag_kart.py — oppdaterer Klassetur-kart-2027.html med innholdet i turarkene.

Ligger i undermappa «underlag» sammen med arkene. Kjør:   python lag_kart.py
Skriptet leser Klassetur-kandidater-2027.html (oversikten) og hvert Klassetur-*.html (turark) i sin egen mappe,
og skriver innholdet inn i datablokken i ../Klassetur-kart-2027.html (mappa over). Selve kartsiden (HTML/JS) røres ikke.
Ingen eksterne biblioteker — bare standard Python 3.

Egne hotellbilder legges som underlag/bilder/hotell/<navn>.jpg (filnavnet står under hvert hotell i kartet);
de bakes inn i HTML-fila når skriptet kjøres. Arkene bakes også inn, så Klassetur-kart-2027.html kan tas med alene.
Koordinater, reisevei-tillegg (transfer) og bildekreditter ligger i KONFIG nederst her.
"""
import re, os, sys, json, html, glob, datetime
from urllib.parse import quote_plus

HER = os.path.dirname(os.path.abspath(__file__))
KART = os.path.join(os.path.dirname(HER), 'Klassetur-kart-2027.html')
if not os.path.exists(KART) and os.path.exists(os.path.join(HER, 'Klassetur-kart-2027.html')):
    KART = os.path.join(HER, 'Klassetur-kart-2027.html')   # alt i én mappe
OVERSIKT = os.path.join(HER, 'Klassetur-kandidater-2027.html')
PREFIX = os.path.relpath(HER, os.path.dirname(KART)).replace(os.sep, '/')
PREFIX = '' if PREFIX == '.' else PREFIX + '/'

# ---------------------------------------------------------------- hjelpere
def txt(s):
    """HTML -> ren tekst"""
    s = re.sub(r'<br\s*/?>', ' ', s or '')
    s = re.sub(r'<[^>]+>', '', s)
    return html.unescape(re.sub(r'\s+', ' ', s)).strip()

def num(s):
    """'470 320' -> 470320, '~363 800' -> 363800"""
    d = re.sub(r'[^\d]', '', s or '')
    return int(d) if d else None

def section(s, title):
    m = re.search(r'<section[^>]*>\s*<h2>' + re.escape(title) + r'</h2>(.*?)</section>', s, re.S)
    return m.group(1) if m else ''

# ---------------------------------------------------------------- oversikten
def les_oversikt():
    s = open(OVERSIKT, encoding='utf-8').read()
    o = {}
    band = re.findall(r'<div><b>([^<]*)</b><small>([^<]*)</small></div>', s)
    o['band'] = [[txt(a), txt(b)] for a, b in band]
    # avreisesteder
    avr = []
    for row in re.findall(r'<tr><td><b>([^<]*)</b></td><td>([^<]*)</td><td class="num">([^<]*)</td><td>([^<]*)</td></tr>', section(s, 'Avreisesteder')):
        avr.append({'flyplass': txt(row[0]), 'buss': txt(row[1]), 'pris': txt(row[2]), 'videre': txt(row[3])})
    o['avreise'] = avr
    m = re.search(r'</table>\s*<p[^>]*>(.*?)</p>', section(s, 'Avreisesteder'), re.S)
    o['direktefly'] = txt(m.group(1)) if m else ''
    # kandidattabellen
    rows = []; gruppe = None
    kand = section(s, 'Kandidatene')
    for tr in re.findall(r'<tr[^>]*>.*?</tr>', kand, re.S):
        g = re.search(r'<tr class="gruppe"><td colspan="4">([^<]*)</td>', tr)
        if g:
            gruppe = txt(g.group(1)); continue
        c = re.findall(r'<td[^>]*>(.*?)</td>', tr, re.S)
        if len(c) == 4 and '<b>' in c[0]:
            navn = txt(re.search(r'<b>(.*?)</b>', c[0], re.S).group(1))
            b = re.search(r'<span class="basis">(.*?)</span>', c[0], re.S)
            rows.append({'navn': navn, 'base': txt(b.group(1)) if b else '', 'vei': txt(c[1]),
                         'pp': num(c[2]), 'total': num(c[3]), 'gruppe': gruppe})
    o['kandidater'] = rows
    w = re.search(r'<div class="warn">(.*?)</div>', kand, re.S)
    o['warn'] = txt(w.group(1)) if w else ''
    # regnet inn per gruppe
    modeller = []
    for h2, tab in re.findall(r'<h2>(Regnet inn[^<]*)</h2>\s*<table>(.*?)</table>', s, re.S):
        poster = [[txt(a), txt(b)] for a, b in re.findall(r'<tr><td>(.*?)</td><td class="num">(.*?)</td></tr>', tab, re.S)]
        modeller.append({'tittel': txt(h2), 'poster': poster})
    o['modeller'] = modeller
    for t in ('Pass og helsetrygdkort', 'Feriesteder som ikke er tatt med', 'Neste steg'):
        sec = section(s, t)
        o[t] = [txt(p) for p in re.findall(r'<(?:p|li)[^>]*>(.*?)</(?:p|li)>', sec, re.S)]
    f = re.search(r'<footer>(.*?)</footer>', s, re.S)
    o['footer'] = txt(f.group(1)) if f else ''
    o['arkHtml'] = s
    return o

# ---------------------------------------------------------------- turarkene
def les_ark(fn):
    s = open(fn, encoding='utf-8').read()
    d = {'fil': os.path.basename(fn), 'arkHtml': s}
    m = re.search(r'<h1>(.*?)</h1>', s, re.S)
    h1 = m.group(1) if m else ''
    sp = re.search(r'<span>(.*?)</span>', h1, re.S)
    d['navn'] = txt(re.sub(r'<span>.*?</span>', '', h1, flags=re.S))
    d['under'] = txt(sp.group(1)) if sp else ''
    m = re.search(r'<p class="kicker">(.*?)</p>', s, re.S); d['kicker'] = txt(m.group(1)) if m else ''
    m = re.search(r'<p class="promise">(.*?)</p>', s, re.S); d['promise'] = txt(m.group(1)) if m else ''
    hb = re.search(r'<div class="heroband">(.*?)\n\s*</div>', s, re.S)
    d['band'] = [[txt(a), txt(b)] for a, b in re.findall(r'<div><b>(.*?)</b><small>(.*?)</small></div>', hb.group(1) if hb else '', re.S)]
    # bilder
    bilder = []
    for src, alt in re.findall(r'<img src="([^"]+)" alt="([^"]*)"', s):
        cap = re.search(r'<img src="' + re.escape(src) + r'"[^>]*>\s*<figcaption>(.*?)</figcaption>', s, re.S)
        bilder.append({'url': html.unescape(src), 'tekst': txt(cap.group(1)) if cap else html.unescape(alt)})
    d['bilder'] = bilder
    # reisevei
    d['reisevei'] = [{'strekning': txt(a), 'info': txt(b)} for a, b in re.findall(r'<div class="leg"><b>(.*?)</b><small>(.*?)</small></div>', s, re.S)]
    # uka
    uke = section(s, 'Slik ser uka ut')
    m = re.search(r'<h3>(.*?)</h3>', uke, re.S); d['uke_tittel'] = txt(m.group(1)) if m else ''
    d['dager'] = [{'tittel': txt(a), 'tekst': txt(b), 'pris': txt(c)} for a, b, c in
                  re.findall(r'<li><div class="day"><b>(.*?)</b><small>(.*?)</small></div><span class="act">(.*?)</span></li>', uke, re.S)]
    m = re.search(r'</ol>\s*<p[^>]*>(.*?)</p>', uke, re.S); d['uke_note'] = txt(m.group(1)) if m else ''
    # overnatting
    ov = section(s, 'Overnatting')
    m = re.search(r'<h3>(.*?)</h3>', ov, re.S); d['hotell_tittel'] = txt(m.group(1)) if m else ''
    m = re.search(r'<p class="lede">(.*?)</p>', ov, re.S); d['hotell_lede'] = txt(m.group(1)) if m else ''
    hot = []
    for navn, basis, tag in re.findall(r'<tr><td><b>(.*?)</b><span class="basis">(.*?)</span></td><td class="num"><span class="tag[^"]*">(.*?)</span></td></tr>', ov, re.S):
        hot.append({'navn': txt(navn), 'basis': txt(basis), 'tag': txt(tag)})
    d['hoteller'] = hot
    # i nærheten
    naer = section(s, 'I nærheten')
    d['naerhet'] = [{'navn': txt(a), 'tekst': txt(b)} for a, b in
                    re.findall(r'<li><b>(.*?)</b><span class="basis">(.*?)</span></li>', naer, re.S)]
    # kostnader
    ko = section(s, 'Hva turen koster')
    rows = []
    for tr in re.findall(r'<tr>(?!<th)(.*?)</tr>', ko, re.S):
        c = re.findall(r'<td[^>]*>(.*?)</td>', tr, re.S)
        if len(c) == 3:
            tag = re.search(r'<span class="tag[^"]*">(.*?)</span>', c[1], re.S)
            basis = re.search(r'<span class="basis">(.*?)</span>', c[1], re.S)
            rows.append({'post': txt(c[0]), 'tag': txt(tag.group(1)) if tag else txt(re.sub(r'<span class="basis">.*?</span>', '', c[1], flags=re.S)),
                         'basis': txt(basis.group(1)) if basis else '', 'belop': num(c[2])})
    d['kostnader'] = rows
    m = re.search(r'<tr class="sum"><td>(.*?)</td><td></td><td class="num">(.*?)</td></tr>', ko, re.S)
    d['sum'] = num(m.group(2)) if m else None
    d['headline'] = [[txt(a), txt(b)] for a, b in re.findall(r'<div><b>(.*?)</b><small>(.*?)</small></div>', ko, re.S)]
    m = re.search(r'<div class="warn">(.*?)</div>', ko, re.S); d['warn'] = txt(m.group(1)) if m else ''
    # ekstra avsnitt i kostnadsdelen (f.eks. liste over hva som må ringes) og footer
    m = re.search(r'<footer>(.*?)</footer>', s, re.S)
    d['footer'] = [txt(x) for x in re.split(r'<br\s*/?>', m.group(1))] if m else []
    d['footer'] = [x for x in d['footer'] if x]
    return d

# ---------------------------------------------------------------- KONFIG
# Steder brukt i reiseveiene (navn slik de står i arkene) -> [lat, lng]
STEDER = {
    'Kautokeino': [69.0117, 23.0417],
    'Alta': [69.9761, 23.3717], 'Kittilä': [67.7010, 24.8468], 'Tromsø': [69.6833, 18.9189], 'Kolari': [67.3306, 23.7947],
    'Oslo': [60.1976, 11.1004], 'Helsingfors': [60.3172, 24.9633],
    'Palma': [39.5517, 2.7388], 'Alicante': [38.2822, -0.5582], 'Barcelona': [41.2971, 2.0785],
    'Málaga': [36.6749, -4.4991], 'Faro': [37.0144, -7.9659], 'Split': [43.5389, 16.2980],
    'Malta': [35.8575, 14.4775], 'Heraklion': [35.3397, 25.1803], 'Rhodos': [36.4054, 28.0862],
    'Tirana': [41.4147, 19.7206], 'Burgas': [42.5696, 27.5152], 'Antalya': [36.8987, 30.8005],
    'Tivat': [42.4047, 18.7233], 'Gdańsk': [54.3776, 18.4662], 'Riga': [56.9236, 23.9711],
    'Vilnius': [54.6341, 25.2858],
    'Edinburgh': [55.9508, -3.3615],
    'Kraków': [50.0777, 19.7848], 'Keflavík': [63.9850, -22.6056],
    'Ljubljana': [46.2237, 14.4576], 'Bratislava': [48.1702, 17.2127], 'Venezia': [45.5053, 12.3519],
    'Tallinn': [59.4133, 24.8328], 'Bergen': [60.2934, 5.2181], 'Trondheim': [63.4578, 10.9240],
}
# Busstraseer (omtrentlige veipunkter langs veien) fra Kautokeino til flyplassene
BUSS = {
    'Alta': [[69.0117, 23.0417], [69.1250, 23.0300], [69.2600, 23.2500], [69.4300, 23.6600], [69.5600, 23.6300], [69.7100, 23.5700], [69.8300, 23.4300], [69.9500, 23.3000], [69.9761, 23.3717]],
    'Kittilä': [[69.0117, 23.0417], [68.8400, 23.0100], [68.6800, 23.0800], [68.5500, 23.1300], [68.4200, 23.1500], [68.2900, 23.0900], [68.1300, 23.3000], [67.9600, 23.6800], [67.8700, 24.0500], [67.7600, 24.4500], [67.6800, 24.8500], [67.7010, 24.8468]],
    'Kolari': [[69.0117, 23.0417], [68.8400, 23.0100], [68.6800, 23.0800], [68.5500, 23.1300], [68.4200, 23.1500], [68.2900, 23.0900], [68.1300, 23.3000], [67.9600, 23.6800], [67.8000, 23.7000], [67.6000, 23.6500], [67.4500, 23.7200], [67.3306, 23.7947]],
}
FLYPLASS = {  # navn -> IATA
    'Alta': 'ALF', 'Kittilä': 'KTT', 'Tromsø': 'TOS', 'Oslo': 'OSL', 'Helsingfors': 'HEL', 'Palma': 'PMI', 'Alicante': 'ALC',
    'Barcelona': 'BCN', 'Málaga': 'AGP', 'Faro': 'FAO', 'Split': 'SPU', 'Malta': 'MLA', 'Heraklion': 'HER', 'Rhodos': 'RHO',
    'Tirana': 'TIA', 'Burgas': 'BOJ', 'Antalya': 'AYT', 'Tivat': 'TIV', 'Gdańsk': 'GDN', 'Riga': 'RIX', 'Vilnius': 'VNO',
    'Edinburgh': 'EDI', 'Kraków': 'KRK', 'Keflavík': 'KEF',
    'Ljubljana': 'LJU', 'Bratislava': 'BTS', 'Venezia': 'VCE', 'Tallinn': 'TLL', 'Bergen': 'BGO', 'Trondheim': 'TRD',
}
REGIONER = {
    'Middelhavet': {'id': 'med', 'farge': '#D4901E'},
    'Adriaterhavet og Svartehavet': {'id': 'adr', 'farge': '#A85434'},
    'Østersjøen og Baltikum': {'id': 'balt', 'farge': '#123A4A'},
    'Nord- og Vest-Europa': {'id': 'by', 'farge': '#3F7A5A'},
    'Alpene og Sentral-Europa': {'id': 'sentral', 'farge': '#4A5D8F'},
    'Norge': {'id': 'norge', 'farge': '#5C3D8C'},
}
# Per ark: id, navn i oversikten, base (navn, lat, lng), land, pass påkrevd, transfer flyplass->base.
# Transfertid merket «(anslag)» står ikke i arkene — det er et grovt anslag ut fra kjøreavstand. De uten merking er hentet fra arket.
DEST = {
    'Klassetur-Mallorca.html':    dict(id='mallorca',    oversikt='Mallorca',      base=['Can Pastilla', 39.5350, 2.7170],   land='Spania',     pass_=False, transfer='Buss · ca. 10 min (anslag)'),
    'Klassetur-CostaBlanca.html': dict(id='costablanca', oversikt='Costa Blanca',  base=['Albir', 38.5697, -0.0642],         land='Spania',     pass_=False, transfer='Buss · ca. 50 min (anslag)'),
    'Klassetur-CostaBrava.html':  dict(id='costabrava',  oversikt='Costa Brava',   base=['Santa Susanna', 41.6360, 2.7130],  land='Spania',     pass_=False, transfer='Buss · ca. 1 t 10 min (anslag)'),
    'Klassetur-CostaDelSol.html': dict(id='costadelsol', oversikt='Costa del Sol', base=['Torremolinos', 36.6220, -4.4990],  land='Spania',     pass_=False, transfer='Tog eller buss · ca. 15 min (anslag)'),
    'Klassetur-Algarve.html':     dict(id='algarve',     oversikt='Algarve',       base=['Alvor', 37.1290, -8.5930],         land='Portugal',   pass_=False, transfer='Buss · ca. 50 min (anslag)'),
    'Klassetur-C-Split.html':     dict(id='split',       oversikt='Split',         base=['Split', 43.5081, 16.4402],         land='Kroatia',    pass_=False, transfer='Flybuss · ca. 30 min (anslag)'),
    'Klassetur-Malta.html':       dict(id='malta',       oversikt='Malta',         base=["St. Paul's Bay", 35.9490, 14.4020], land='Malta',      pass_=False, transfer='Buss · ca. 30 min (anslag)'),
    'Klassetur-B-Kreta.html':     dict(id='kreta',       oversikt='Kreta',         base=['Rethymno', 35.3650, 24.4820],      land='Hellas',     pass_=False, transfer=None),
    'Klassetur-Rhodos.html':      dict(id='rhodos',      oversikt='Rhodos',        base=['Kolymbia', 36.2530, 28.1650],      land='Hellas',     pass_=False, transfer='Buss · ca. 25 min (anslag)'),
    'Klassetur-Albania.html':     dict(id='albania',     oversikt='Albania',       base=['Durrës', 41.3230, 19.4410],        land='Albania',    pass_=True,  transfer='Buss · ca. 40 min'),
    'Klassetur-Bulgaria.html':    dict(id='bulgaria',    oversikt='Bulgaria',      base=['Nesebar', 42.6590, 27.7140],       land='Bulgaria',   pass_=False, transfer='Buss · ca. 40 min'),
    'Klassetur-Tyrkia.html':      dict(id='tyrkia',      oversikt='Tyrkia',        base=['Side', 36.7670, 31.3890],          land='Tyrkia',     pass_=True,  transfer='Buss · ca. 1 t'),
    'Klassetur-Montenegro.html':  dict(id='montenegro',  oversikt='Montenegro',    base=['Bečići', 42.2790, 18.8650],        land='Montenegro', pass_=True,  transfer='Buss · ca. 25 min'),
    'Klassetur-A-Gdansk.html':    dict(id='gdansk',      oversikt='Gdańsk',        base=['Gdańsk', 54.3520, 18.6466],        land='Polen',      pass_=False, transfer='Buss · ca. 25 min (anslag)'),
    'Klassetur-Riga.html':        dict(id='riga',        oversikt='Riga',          base=['Riga', 56.9496, 24.1052],          land='Latvia',     pass_=False, transfer='Buss · ca. 20 min (anslag)'),
    'Klassetur-Vilnius.html':     dict(id='vilnius',     oversikt='Vilnius',       base=['Vilnius', 54.6872, 25.2797],       land='Litauen',    pass_=False, transfer='Buss · ca. 15 min (anslag)'),
    'Klassetur-Edinburgh.html':   dict(id='edinburgh',   oversikt='Edinburgh',     base=['Edinburgh', 55.9533, -3.1883],     land='Skottland',  pass_=True,  transfer='Trikk · ca. 35 min (anslag)',
                                       pass_tekst='Storbritannia er utenfor EU og EØS: gyldig pass for alle 28 og digital innreisetillatelse (ETA, £20 per person) før avreise. Europeisk helsetrygdkort gjelder i Storbritannia.'),
    'Klassetur-Slovenia.html':    dict(id='slovenia',    oversikt='Slovenia',      base=['Bled', 46.3683, 14.1146],          land='Slovenia',   pass_=False, transfer='Buss · ca. 30 min (anslag)'),
    'Klassetur-Slovakia.html':    dict(id='slovakia',    oversikt='Slovakia',      base=['Bratislava', 48.1486, 17.1077],    land='Slovakia',   pass_=False, transfer='Bybuss 61 · ca. 30 min (anslag)'),
    'Klassetur-Italia.html':      dict(id='italia',      oversikt='Italia',        base=['Lido di Jesolo', 45.4972, 12.6403], land='Italia',     pass_=False, transfer='Buss · ca. 50 min (anslag)'),
    'Klassetur-Tallinn.html':     dict(id='tallinn',     oversikt='Tallinn',       base=['Tallinn', 59.4370, 24.7536],       land='Estland',    pass_=False, transfer='Til fots · ca. 15 min (anslag)'),
    'Klassetur-Fjordene.html':    dict(id='fjordene',    oversikt='Fjordene',      base=['Bergen', 60.3913, 5.3221],         land='Vestlandet', pass_=False, transfer='Bybanen · ca. 45 min (anslag)'),
    'Klassetur-Trondheim.html':   dict(id='trondheim',   oversikt='Trondheim',     base=['Trondheim', 63.4305, 10.3951],     land='Trøndelag',  pass_=False, transfer='Flybuss · ca. 40 min (anslag)'),
    'Klassetur-Krakow.html':      dict(id='krakow',      oversikt='Kraków',        base=['Kraków', 50.0614, 19.9366],        land='Polen',      pass_=False, transfer='Tog · ca. 20 min (anslag)'),
    'Klassetur-Island.html':      dict(id='island',      oversikt='Island',        base=['Reykjavík', 64.1466, -21.9426],    land='Island',     pass_=False, transfer='Buss · ca. 45 min (anslag)'),
}
# Tallinn har to reiseveier: buss/nattog/ferje via Kolari (står i arket) og fly via Oslo (står bare i oversikten).
TALLINN_VIA_OSLO = [
    {'strekning': 'Kautokeino → Alta', 'info': 'Buss · ca. 2 t'},
    {'strekning': 'Alta → Oslo', 'info': 'Norwegian eller SAS · ca. 2 t'},
    {'strekning': 'Oslo → Tallinn', 'info': 'Norwegian eller airBaltic, direkte · ca. 1 t 25 min'},
]
# Kreta har to reiseveier i oversikten. Arket beskriver veien via Kittilä/Helsingfors; veien via Alta/Oslo står bare i oversikten.
KRETA_VIA_OSLO = [
    {'strekning': 'Kautokeino → Alta', 'info': 'Buss · ca. 2 t'},
    {'strekning': 'Alta → Oslo', 'info': 'Norwegian eller SAS · ca. 2 t'},
    {'strekning': 'Oslo → Heraklion', 'info': 'Flyselskap og reisetid ikke oppgitt i arkene'},
]
# Bildekreditter (fotograf, lisens) for bildene som er brukt i arkene — filnavn på Wikimedia Commons
KREDITT = {
    'Gdansk_at_night.jpg': ('22Kartika', 'CC BY-SA 3.0'), 'PL_GD_Gdansk_crane.jpg': ('Andrei Stroe', 'CC BY-SA 3.0 pl'), 'Motława_Gdańsk.jpg': ('Wikimedia Commons', 'CC BY-SA 3.0'),
    '20100820_Spinalonga_island_Crete_Panorama.jpg': ('Ggia', 'CC BY-SA 3.0'), 'Rethymno_lighthouse_Crete_Greece.jpg': ('Jebulon', 'CC0'), 'Columns_in_Knossos,_Crete.jpg': ('Jebulon', 'CC0'),
    "Aerial_view_of_Diocletian's_Palace_in_Split,_Croatia_(48608247353).jpg": ('dronepicr', 'CC BY 2.0'), "Peristyle_of_Diocletian's_Palace,_Split_(11908116224).jpg": ('Following Hadrian', 'CC BY-SA 2.0'), 'Dioklecijanova_palača,_Split_-_jugoistok.JPG': ('Silverije', 'CC BY-SA 3.0'),
    'Torremolinos_-_beach.jpg': ('Tiia Monto', 'CC BY-SA 3.0'), 'Playamar,_Torremolinos.JPG': ('Hans Olav Lien', 'CC BY-SA 3.0'),
    'Durres,Portez_beach.jpg': ('Durres1998', 'CC BY-SA 4.0'), 'Durrës_beach_(by_Pudelek).JPG': ('Pudelek (Marcin Szala)', 'CC BY-SA 3.0'),
    'Praia_dos_Três_Irmãos_-_Portugal_(4793272312).jpg': ('Vitor Oliveira', 'CC BY-SA 2.0'), 'Praia_de_Alvor_-_Portugal_(49756771263).jpg': ('Vitor Oliveira', 'CC BY-SA 2.0'),
    'Panorama_Nesebar.jpg': ('FrankySyes', 'CC BY-SA 4.0'), 'Nesebar-panorama-night.JPG': ('Japus', 'CC BY 2.5'),
    "Playa_de_l'Albir.JPG": ('Kisueses', 'CC BY-SA 3.0 es'), 'Playa_del_Racó_del_Albir.JPG': ('Jackrm', 'Public domain'),
    'Platja_de_les_Dunes,_2.jpg': ('Isidro Jabato', 'CC BY-SA 4.0'), 'Santa_Susanna_Beach.jpg': ('ElenaStromberger', 'CC BY-SA 3.0 es'),
    'Can_Pastilla_and_San_Antonio_de_la_Playa_marina_aerial_view2.jpg': ('Steffen Mokosch', 'CC BY-SA 4.0'), 'Vista_aèria_de_Cala_Estància.JPG': ('Chixoy', 'CC BY-SA 3.0'),
    'Bugibba_-_Malta_-_panoramio.jpg': ('ianpudsey', 'CC BY 3.0'), "Malta_-_St._Paul's_Bay_-_Dawret_Il-Gzejjer_02.jpg": ('Txllxt TxllxT', 'CC BY-SA 4.0'),
    'Montenegro_Becici_beach.jpg': ('Liilia Moroz', 'CC0'), 'Bečići_Beach.jpg': ('Milan B.', 'CC BY-SA 3.0'),
    '20210826-Lindos-DJI_0205.jpg': ('Thomas Berwing', 'CC BY-SA 4.0'), 'Rhodos_Kolymbia_Beach_R01.jpg': ('Marc Ryckaert', 'CC BY 3.0'),
    'Riga_(33844464828).jpg': ('Jorge Franganillo', 'CC BY 2.0'), 'Riga_Panorama.jpg': ('Benjamin Snyder', 'Public domain'),
    'Sunrise_apollo_side.jpg': ('Saffron Blaze', 'CC BY-SA 3.0'), 'Side_Turkey_beach_(122502321).jpg': ('Astrowoosie', 'CC BY 2.0'),
    'Vilnius_old_town_1.JPG': ('Karmen media', 'CC BY-SA 3.0'), 'Vilnius_-_Panorama_02.jpg': ('Lestat (Jan Mehlich)', 'CC BY-SA 3.0'),
    'The_Nyhavn_Canal_3.jpg': ('European Commission', 'CC BY 4.0'), 'Tivoli_Gardens_20180721-2.jpg': ('Suicasmo', 'CC BY-SA 4.0'),
    'Hamburg,_Landungsbrücken_--_2016_--_3131-7.jpg': ('Dietmar Rabich', 'CC BY-SA 4.0'), 'Speicherstadt_abends.jpg': ('Thomas Wolf', 'CC BY-SA 3.0'),
    'Skyline_of_Edinburgh.jpg': ('Andrew Colin', 'CC BY 2.0'), 'City_of_Edinburgh_-_Edinburgh_Castle_-_20140421004403.jpg': ('Enric', 'CC BY-SA 4.0'),
    'La_Tour_Eiffel_vue_de_la_Tour_Saint-Jacques,_Paris_août_2014_(2).jpg': ('Yann Caradec', 'CC BY-SA 2.0'), 'Notre-Dame_de_Paris_and_Île_de_la_Cité_at_dusk_140516_1.jpg': ('DXR', 'CC BY-SA 3.0'),
    'Sukiennice_and_Main_Market_Square_Krakow_Poland.JPG': ('Jorge Lascar', 'CC BY 2.0'), 'Saint_Kinga_Chapel_in_Wieliczka_Salt_Mine.jpg': ('Андрей Романенко', 'CC BY-SA 4.0'),
    'Gullfoss_from_the_Air_(cropped).jpg': ('Nickspix', 'CC BY-SA 4.0'), 'Reykjavík,_view_from_Hallgrímskirkja_(2).jpg': ('Olga Ernst', 'CC BY-SA 4.0'),
    'Bled_Island_05.jpg': ('Krzysztof Golik', 'CC BY-SA 4.0'), 'Blejski_Vintgar_01.jpg': ('Smihael', 'CC BY-SA 3.0'),
    'Bratislava_Castle_with_Danube.jpeg': ('Ingo Mehling', 'CC BY-SA 4.0'), 'Devín_Castle_and_Morava-Danube_Confluence_01.jpg': ('Uoaei1', 'CC BY-SA 4.0'),
    'Lido_di_Jesolo_Pier_5.jpg': ('kallerna', 'CC BY-SA 4.0'), 'Canal_Grande_Chiesa_della_Salute_e_Dogana_dal_ponte_dell_Accademia.jpg': ('Wolfgang Moroder', 'CC BY-SA 3.0'),
    'Old_town_of_Tallinn_06-03-2012.jpg': ('Ivar Leidus', 'CC BY-SA 3.0 ee'), 'Lennusadam_2015.jpg': ('Hiiumaa mudeliklubi', 'CC BY-SA 4.0'),
    "Nærøyfjord_-_The_world's_most_beautiful_fjord_(32060514105).jpg": ('Jorge Láscar', 'CC BY 2.0'), 'Bergen_Bryggen_2986.jpg': ('Anna Anichkova', 'CC BY-SA 3.0'),
    'Catedral_de_Nidaros,_Trondheim,_Noruega,_2019-09-06,_DD_103.jpg': ('Diego Delso', 'CC BY-SA 4.0'), 'Islote_Munkholmen,_Trondheim,_Noruega,_2019-09-06,_DD_12.jpg': ('Diego Delso', 'CC BY-SA 4.0'),
}
# Hotellbilder med fri lisens (Wikimedia Commons). Andre hoteller får lenke til Google Maps og en plass for eget bilde i bilder/hotell/.
HOTELLBILDER = {
    'Sol Torremolinos Don Pablo': ('https://commons.wikimedia.org/wiki/Special:FilePath/Sol_Don_Pablo_Hotel_Torremolinos.JPG?width=800', 'EveryPicture', 'Public domain'),
}

def slug(s):
    s = s.lower()
    for a, b in (('æ', 'ae'), ('ø', 'o'), ('å', 'a'), ('é', 'e'), ('á', 'a'), ('ö', 'o'), ('ü', 'u'), ('č', 'c'), ('ć', 'c'), ('š', 's'), ('ż', 'z'), ('ł', 'l'), ('ń', 'n'), ('ā', 'a'), ('ū', 'u'), ('ė', 'e'), ('ğ', 'g'), ('ı', 'i'), ('ş', 's'), ('&', 'og')):
        s = s.replace(a, b)
    s = re.sub(r"['’.]", '', s)
    return re.sub(r'[^a-z0-9]+', '-', s).strip('-')

def kreditt_for(url):
    from urllib.parse import unquote
    m = re.search(r'FilePath/([^?]+)', url)
    if not m: return None
    fil = unquote(m.group(1))
    k = KREDITT.get(fil)
    tittel = os.path.splitext(fil)[0].replace('_', ' ')
    return {'fil': fil, 'tittel': tittel, 'fotograf': k[0] if k else '', 'lisens': k[1] if k else ''}

def bygg_legs(reisevei, base, transfer):
    """Reisevei fra arket -> etapper med koordinater og type."""
    legs = []
    for r in reisevei:
        fra, til = [x.strip() for x in re.split(r'\s*→\s*', r['strekning'])]
        info = r['info']
        if til == 'hotellet':
            legs.append({'type': 'transfer', 'fra': fra, 'til': base[0], 'info': info, 'a': STEDER[fra], 'b': base[1:3]})
            continue
        lav = info.lower()
        if lav.startswith(('tog', 'vr nattog', 'nattog')):
            legs.append({'type': 'tog', 'fra': fra, 'til': til, 'info': info, 'a': STEDER[fra], 'b': STEDER[til]})
            continue
        if lav.startswith(('ferje', 'ferge', 'tallink', 'hurtigbåt', 'båt')):
            legs.append({'type': 'ferje', 'fra': fra, 'til': til, 'info': info, 'a': STEDER[fra], 'b': STEDER[til]})
            continue
        if info.lower().startswith('buss'):
            legs.append({'type': 'buss', 'fra': fra, 'til': til, 'info': info, 'a': STEDER[fra], 'b': STEDER[til], 'trase': BUSS.get(til)})
        else:
            legs.append({'type': 'fly', 'fra': fra, 'til': til, 'info': info, 'a': STEDER[fra], 'b': STEDER[til],
                         'fraKode': FLYPLASS.get(fra, ''), 'tilKode': FLYPLASS.get(til, '')})
    if transfer and not any(l['type'] == 'transfer' for l in legs) and legs:
        siste = legs[-1]
        legs.append({'type': 'transfer', 'fra': siste['til'], 'til': base[0], 'info': transfer, 'a': siste['b'], 'b': base[1:3]})
    return legs

def varighet_min(info):
    """'Buss · ca. 3 t 30 min' -> 210, 'ca. 40 min' -> 40, ingen tid -> None"""
    m = re.search(r'ca\.\s*((?:\d+)\s*t)?\s*((?:\d+)\s*min)?', info or '')
    if not m or not (m.group(1) or m.group(2)): return None
    t = int(re.sub(r'\D', '', m.group(1))) if m.group(1) else 0
    mi = int(re.sub(r'\D', '', m.group(2))) if m.group(2) else 0
    return t * 60 + mi

import base64, mimetypes
def eget_bilde(slug_):
    """Finner underlag/bilder/hotell/<slug>.jpg|jpeg|png|webp og returnerer data-URI, ellers None."""
    for ext in ('.jpg', '.jpeg', '.png', '.webp'):
        fn = os.path.join(HER, 'bilder', 'hotell', slug_ + ext)
        if os.path.exists(fn):
            mime = mimetypes.guess_type(fn)[0] or 'image/jpeg'
            data = open(fn, 'rb').read()
            if len(data) > 600_000:
                print('  NB: %s er %d KB — vurder a krympe bildet (under 300 KB per bilde holder)' % (os.path.basename(fn), len(data) // 1024))
            return 'data:%s;base64,%s' % (mime, base64.b64encode(data).decode('ascii'))
    return None

def maps_link(q):
    return 'https://www.google.com/maps/search/?api=1&query=' + quote_plus(q)

def bygg():
    o = les_oversikt()
    ark = {os.path.basename(f): les_ark(f) for f in glob.glob(os.path.join(HER, 'Klassetur-*.html')) if 'kandidater' not in f and 'kart' not in f}
    dest = []
    for fil, k in DEST.items():
        if fil not in ark:
            print('mangler ark:', fil); continue
        a = ark[fil]
        rader = [r for r in o['kandidater'] if r['navn'] == k['oversikt']]
        if not rader:
            print('finner ikke', k['oversikt'], 'i oversikten'); continue
        gruppe = rader[0]['gruppe']
        reg = REGIONER.get(gruppe, {'id': 'x', 'farge': '#555'})
        # reiseveier: én per rad i oversikten
        ruter = []
        for r in rader:
            via = r['vei']
            if k['id'] == 'kreta' and via.startswith('Alta'):
                legs = bygg_legs(KRETA_VIA_OSLO, k['base'], 'Buss · ca. 1 t 15 min')
                kilde = 'oversikt'
            elif k['id'] == 'tallinn' and via.startswith('Alta'):
                legs = bygg_legs(TALLINN_VIA_OSLO, k['base'], 'Trikk · ca. 21 min (anslag)')
                kilde = 'oversikt'
            else:
                legs = bygg_legs(a['reisevei'], k['base'], k['transfer'])
                kilde = 'ark'
            tider = [varighet_min(l['info']) for l in legs]
            ruter.append({'via': via, 'pp': r['pp'], 'total': r['total'], 'legs': legs, 'kilde': kilde,
                          'fra': legs[0]['til'] if legs else '', 'hub': (lambda L: L[0]['til'] if len(L) > 1 else '')([l for l in legs if l['type'] in ('fly', 'tog', 'ferje')]),
                          'hubType': 'fly' if any(l['type'] == 'fly' for l in legs) else 'annet',
                          'reisetid': {'min': sum(t for t in tider if t), 'mangler': [l['fra'] + ' → ' + l['til'] for l, t in zip(legs, tider) if not t],
                                       'bareTransfer': all(l['type'] == 'transfer' for l, t in zip(legs, tider) if not t)}})
        ruter.sort(key=lambda r: r['pp'])
        hoteller = []
        for h in a['hoteller']:
            hb = HOTELLBILDER.get(h['navn'])
            sl = slug(h['navn'])
            eget = eget_bilde(sl)
            hoteller.append({**h, 'slug': sl, 'maps': maps_link(h['navn'] + ' ' + h['basis'].split('·')[0].strip() if '·' in h['basis'] else h['navn'] + ' ' + k['base'][0]),
                             'bilde': eget or (hb[0] if hb else None), 'bildekreditt': 'eget bilde' if eget else ((hb[1] + ', ' + hb[2]) if hb else None)})
        bilder = []
        for b in a['bilder']:
            bilder.append({**b, 'kreditt': kreditt_for(b['url'])})
        dest.append({
            'id': k['id'], 'fil': fil, 'navn': a['navn'], 'under': a['under'], 'kicker': a['kicker'], 'promise': a['promise'],
            'region': reg['id'], 'regionNavn': gruppe, 'farge': reg['farge'], 'land': k['land'], 'pass': k['pass_'], 'passTekst': k.get('pass_tekst'),
            'base': {'navn': k['base'][0], 'lat': k['base'][1], 'lng': k['base'][2], 'beskrivelse': rader[0]['base'], 'maps': maps_link(k['base'][0] + ', ' + k['land'])},
            'pp': ruter[0]['pp'], 'total': ruter[0]['total'], 'ruter': ruter,
            'band': a['band'], 'bilder': bilder, 'reisevei': a['reisevei'],
            'naerhet': a['naerhet'],
            'ukeTittel': a['uke_tittel'], 'dager': a['dager'], 'ukeNote': a['uke_note'],
            'hotellTittel': a['hotell_tittel'], 'hotellLede': a['hotell_lede'], 'hoteller': hoteller,
            'kostnader': a['kostnader'], 'sum': a['sum'], 'headline': a['headline'], 'warn': a['warn'], 'footer': a['footer'],
            'arkHtml': a['arkHtml'],
        })
    dest.sort(key=lambda d: (d['pp'], d['navn']))
    data = {
        'generert': datetime.date.today().isoformat(),
        'prefix': PREFIX,
        'oversikt': {'fil': os.path.basename(OVERSIKT), 'band': o['band'], 'avreise': o['avreise'], 'direktefly': o['direktefly'],
                     'warn': o['warn'], 'modeller': o['modeller'], 'pass': o['Pass og helsetrygdkort'], 'utelatt': o['Feriesteder som ikke er tatt med'],
                     'neste': o['Neste steg'], 'footer': o['footer'], 'arkHtml': o['arkHtml']},
        'origo': {'navn': 'Kautokeino', 'lat': STEDER['Kautokeino'][0], 'lng': STEDER['Kautokeino'][1]},
        'steder': {n: {'lat': v[0], 'lng': v[1], 'kode': FLYPLASS.get(n, '')} for n, v in STEDER.items()},
        'buss': BUSS,
        'regioner': {v['id']: {'navn': n, 'farge': v['farge']} for n, v in REGIONER.items()},
        'destinasjoner': dest,
    }
    return data

def main():
    data = bygg()
    js = json.dumps(data, ensure_ascii=False, separators=(',', ':')).replace('</', '<\\/')
    if not os.path.exists(KART):
        print('Finner ikke', KART, '— kartsiden må ligge i samme mappe som dette skriptet.'); sys.exit(1)
    s = open(KART, encoding='utf-8', newline='').read()
    m = re.search(r'(<script id="klassetur-data" type="application/json">)(.*?)(</script>)', s, re.S)
    if not m:
        print('Fant ikke datablokken i kartsiden.'); sys.exit(1)
    s = s[:m.start(2)] + js + s[m.end(2):]
    open(KART, 'w', encoding='utf-8', newline='').write(s)   # bevarer linjeskift som de er
    print('Oppdatert', os.path.basename(KART), 'med', len(data['destinasjoner']), 'reisemal —', round(os.path.getsize(KART) / 1024), 'KB. Fila er komplett i seg selv (arkene ligger inni).')
    # nettversjon: samme fil som docs/index.html (GitHub Pages, mappa docs/ ved siden av kartet) og/eller nett/ (Netlify Drop, med zip)
    import zipfile
    m = os.path.join(os.path.dirname(KART), 'docs')
    if os.path.isdir(m):
        open(os.path.join(m, 'index.html'), 'w', encoding='utf-8', newline='').write(s)
        print('Oppdatert docs/index.html — commit og push, sa er nettsiden oppdatert innen et minutt.')
    m = os.path.join(os.path.dirname(KART), 'nett')
    if os.path.isdir(m):
        open(os.path.join(m, 'index.html'), 'w', encoding='utf-8', newline='').write(s)
        with zipfile.ZipFile(os.path.join(m, 'klassetur-2027.zip'), 'w', zipfile.ZIP_DEFLATED) as z:
            z.write(os.path.join(m, 'index.html'), 'index.html')
        print('Oppdatert nett/index.html og nett/klassetur-2027.zip — dra zip-fila inn pa Deploys-sida i Netlify.')

if __name__ == '__main__':
    main()
