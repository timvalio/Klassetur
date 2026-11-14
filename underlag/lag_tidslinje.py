# -*- coding: utf-8 -*-
"""lag_tidslinje.py - bygger Klassetur-tidslinje-dag1.html

Testbit: reisedagen tirsdag 8. juni 2027, fra oppmoete ved skolen i Kautokeino
til ombordstigning paa DY 321 i Alta. Kartet foelger bussruta fra Kautokeino
til Alta lufthavn, og scenen ved siden av viser hvor gruppa er til enhver tid.

Leaflet og bussruta er hentet fra Klassetur-kart-2027.html, slik at sida virker
uten nett for alt annet enn kartflisene.
"""
import json, math, pathlib, sys

HER = pathlib.Path(__file__).resolve().parent
sys.path.insert(0, str(HER))
import scener
from rute_ekte import RUTE as EKTE_RUTE, STEDER as EKTE_STEDER, OSRM_KM, OSRM_MIN

# Leaflet, bussruta og flyplasskoordinatene hentes rett ut av kartsida, slik at
# det ikke ligger kopier av dem her. KART kan overstyres med foerste argument.
KART = pathlib.Path(sys.argv[1]) if len(sys.argv) > 1 else HER.parent / 'Klassetur-kart-2027.html'


def _les_kart():
    t = KART.read_text(encoding='utf-8')
    # Leaflet: foerste <style> og det <script> som starter med Leaflet-signaturen
    a = t.index('>', t.index('<style')) + 1
    css = t[a:t.index('</style>', a)]
    i = t.index('a JS library for interactive maps')
    b = t.rindex('<script', 0, i)
    js = t[t.index('>', b) + 1:t.index('</script>', b)]
    # datablokka
    d0 = t.index('klassetur-data')
    d1 = t.index('>', d0) + 1
    d = json.loads(t[d1:t.index('</script>', d1)])
    return css, js, None


LEAFLET_CSS, LEAFLET_JS, _ = _les_kart()

# ---------------------------------------------------------------- tidslinja
# t = minutter etter 07:15. Bussen gaar 07:30 og er framme 09:30.
BUSS_START, BUSS_SLUTT = 15, 150      # 07:15 til 09:30

FASER = [
    dict(t=0,   id='oppmote',  tittel='Oppmøte utenfor skolen',
         sted='Kautokeino skole', scene='skolen',
         tekst='Alle 28 møter utenfor skolen. Bussen er bestilt for hele gruppen tur/retur '
               'Kautokeino–Alta til 17 000 kroner.'),
    dict(t=10,  id='bagasje',  tittel='Bagasjen i lasterommet',
         sted='Kautokeino skole', scene='bagasjen',
         tekst='Hver reisende har 2 × 23 kg innsjekket bagasje, to håndbagasjer og én taxfreepose '
               'med i gruppeprisen. Store kofferter i lasterommet, håndbagasjen med inn.'),
    dict(t=15,  id='avgang',   tittel='Bussen går nordover på E45',
         sted='E45 mot Alta', scene='i-bussen',
         tekst='135,8 km nordover. Bilruta tar 2 timer og 9 minutter; vi regner 2 timer og 15 '
               'minutter med buss, så gruppen er framme i god tid før totimersmerket.'),
    dict(t=77,  id='masi',     tittel='Gjennom Masi',
         sted='E45 · 60 km kjørt', scene='masi',
         tekst='Masi (Máze) ligger ved elva omtrent midtveis, 60 km fra Kautokeino. '
               'Herfra stiger veien opp mot høyfjellet.'),
    dict(t=96,  id='suolovuopmi', tittel='Suolovuopmi',
         sted='E45 · 78 km kjørt', scene='suolovuopmi',
         tekst='Fjellstua ved veien, 78 km inn i turen og det høyeste partiet på strekningen. '
               'I juni ligger det fortsatt snøflekker i skrentene.'),
    dict(t=135, id='eiby',     tittel='Ned mot Eiby',
         sted='E45 · 117 km kjørt', scene='eibydalen',
         tekst='Veien faller ned fra vidda. Bjørkeskogen tar over, og etter Eiby og Øvre Alta '
               'kommer Altafjorden til syne.'),
    dict(t=150, id='framme',   tittel='Framme ved Alta lufthavn',
         sted='Alta lufthavn (ALF)', scene='alta-lufthavn',
         tekst='Bussen setter av ved terminalen 09:30. Det gir 25 minutter før totimersmerket 09:55.'),
    dict(t=165, id='innsjekk', tittel='Innsjekk og bagasjelevering',
         sted='Alta lufthavn', scene='innsjekk',
         tekst='28 navn og 28 kolli. Navnelista må være levert til Norwegian senest fem dager '
               'før avreise, altså 3. juni.'),
    dict(t=220, id='sikkerhet', tittel='Sikkerhetskontroll',
         sted='Alta lufthavn', scene='sikkerhetskontroll',
         tekst='Væske og elektronikk opp av sekken. En gruppe på 28 bruker lengre tid gjennom '
               'kontrollen enn enkeltreisende.'),
    dict(t=250, id='gate',     tittel='Ved gate',
         sted='Alta lufthavn', scene='ved-gate',
         tekst='Siste opptelling før ombordstigning. DY 321 går til Oslo-Gardermoen 11:55 '
               'og lander 13:55.'),
    dict(t=265, id='ombord',   tittel='Ombordstigning DY 321',
         sted='Alta lufthavn', scene='ombordstigning',
         tekst='Gruppen går om bord. Her stopper denne tidslinja — neste etappe er Gardermoen, '
               'der gruppen har fem timer og 40 minutter før flyet til Barcelona.'),
]

MERKER = [
    dict(t=175, tekst='to timer før avgang'),
]

SLUTT = 265
AVGANG_TEKST = 'DY 321 går 11:55'

# ---------------------------------------------------------------- kamera
def _hav(a, b):
    R = 6371.0
    p1, p2 = math.radians(a[0]), math.radians(b[0])
    dp = p2 - p1
    dl = math.radians(b[1] - a[1])
    h = math.sin(dp / 2) ** 2 + math.cos(p1) * math.cos(p2) * math.sin(dl / 2) ** 2
    return 2 * R * math.asin(math.sqrt(h))

def rute_med_lengde():
    P = [list(x) for x in EKTE_RUTE]
    kum, s = [0.0], 0.0
    for i in range(len(P) - 1):
        s += _hav(P[i], P[i + 1])
        kum.append(s)
    return P, kum, s

# ---------------------------------------------------------------- bygg
def bygg():
    P, kum, tot = rute_med_lengde()
    merkesteder = [dict(navn=n, ll=[la, lo]) for n, (la, lo, _) in EKTE_STEDER.items()
                   if n not in ('Kautokeino skole', 'Alta lufthavn')]
    sc = scener.alle_unike()
    data = dict(
        faser=FASER, merker=MERKER, slutt=SLUTT, avgangTekst=AVGANG_TEKST,
        bussStart=BUSS_START, bussSlutt=BUSS_SLUTT,
        rute=P, kum=kum, total=round(tot, 2),
        alta=list(EKTE_STEDER['Alta lufthavn'][:2]),
        kautokeino=list(EKTE_STEDER['Kautokeino skole'][:2]),
        steder=merkesteder, osrmKm=OSRM_KM, osrmMin=OSRM_MIN,
        scener=sc,
    )
    html = MAL
    html = html.replace('/*__LEAFLET_CSS__*/', LEAFLET_CSS)
    html = html.replace('/*__LEAFLET_JS__*/', LEAFLET_JS)
    html = html.replace('"__DATA__"', json.dumps(data, ensure_ascii=False))
    return html

MAL = r'''<!doctype html>
<html lang="no">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Reisedagen · 8. juni 2027</title>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Archivo:wght@400;500;600;800&family=Newsreader:opsz,wght@6..72,400;6..72,500&display=swap" rel="stylesheet">
<style>/*__LEAFLET_CSS__*/</style>
<style>
:root{
  --deep:#123A4A; --deeper:#0A2531; --amber:#E2A02F; --amber-soft:#F5E3C2; --brick:#A85434;
  --paper:#FCFAF6; --ink:#1B1B1B; --muted:#6B6459; --line:#DFD9CD;
  --top:58px; --bar:96px;
}
*{box-sizing:border-box}
html,body{height:100%;margin:0}
body{background:var(--paper);color:var(--ink);font-family:'Archivo',system-ui,-apple-system,'Segoe UI',sans-serif;font-size:14.5px;line-height:1.5;overflow:hidden}
button{font:inherit;color:inherit;background:none;border:0;padding:0;cursor:pointer}
.num{font-variant-numeric:tabular-nums}

.top{height:var(--top);display:flex;align-items:center;gap:18px;padding:0 18px;background:var(--deep);color:var(--paper);position:relative;z-index:1200}
.top .brand{display:flex;flex-direction:column;line-height:1.15;min-width:0}
.top .brand b{font-size:16px;font-weight:800;letter-spacing:-.01em;white-space:nowrap}
.top .brand small{font-size:11.5px;color:#9FB8C4;letter-spacing:.06em;text-transform:uppercase;white-space:nowrap}
.top .ctrl{margin-left:auto;display:flex;align-items:center;gap:10px}
.chip{font-size:12.5px;background:rgba(255,255,255,.1);padding:5px 11px;border-radius:999px;white-space:nowrap}
.chip b{color:var(--amber)}
.seg{display:inline-flex;background:rgba(255,255,255,.1);border-radius:999px;padding:3px}
.seg button{padding:5px 11px;border-radius:999px;font-size:12.5px;font-weight:600;color:#CFE0E8;white-space:nowrap}
.seg button.on{background:var(--paper);color:var(--deep)}

.wrap{height:calc(100% - var(--top) - var(--bar));display:flex;min-height:0}
.kart{flex:1 1 auto;position:relative;min-width:0}
#map{position:absolute;inset:0;background:#DCE6EC}
.maptype{position:absolute;right:12px;top:12px;z-index:620;display:inline-flex;background:rgba(252,250,246,.94);border:1px solid var(--line);border-radius:999px;padding:3px;box-shadow:0 2px 10px rgba(0,0,0,.14)}
.maptype button{padding:5px 12px;border-radius:999px;font-size:12.5px;font-weight:600;color:var(--muted)}
.maptype button.on{background:var(--deep);color:var(--paper)}

.panel{flex:0 0 400px;border-left:1px solid var(--line);background:var(--paper);display:flex;flex-direction:column;min-height:0;overflow:hidden}
.scene{position:relative;aspect-ratio:400/260;background:#E9E2D3;border-bottom:1px solid var(--line);flex:0 0 auto}
.scene > svg{width:100%;height:100%;display:block}
.scene .merk{position:absolute;left:12px;bottom:10px;background:rgba(18,58,74,.9);color:var(--paper);font-size:11px;letter-spacing:.07em;text-transform:uppercase;padding:4px 9px;border-radius:4px}
.tekst{padding:18px 20px;overflow:auto;flex:1 1 auto}
.tekst .klokke{font-size:30px;font-weight:800;letter-spacing:-.02em;color:var(--deep);line-height:1}
.tekst h2{font-family:'Newsreader',Georgia,serif;font-size:24px;font-weight:500;margin:6px 0 2px;letter-spacing:-.01em}
.tekst .sted{font-size:12px;letter-spacing:.07em;text-transform:uppercase;color:var(--muted)}
.tekst p{margin:12px 0 0;color:#36322C}
.neste{margin-top:16px;padding-top:12px;border-top:1px solid var(--line);font-size:13px;color:var(--muted)}
.neste b{color:var(--deep);font-weight:600}
.liste{margin-top:18px;border-top:1px solid var(--line);padding-top:12px}
.liste h3{font-size:11px;letter-spacing:.09em;text-transform:uppercase;color:var(--muted);margin:0 0 8px;font-weight:600}
.liste button{display:flex;gap:11px;width:100%;text-align:left;padding:5px 7px;border-radius:5px;color:var(--muted);line-height:1.35}
.liste button:hover{background:#F2EDE2}
.liste button .k{font-size:12.5px;font-weight:700;color:var(--deep);min-width:38px;font-variant-numeric:tabular-nums}
.liste button .n{font-size:13px}
.liste button.na{background:var(--amber-soft)}
.liste button.na .n{color:var(--ink);font-weight:600}
.liste .avg{display:flex;gap:11px;padding:7px;margin-top:3px;border-top:1px dashed var(--line);color:var(--muted);font-size:13px}
.liste .avg .k{font-size:12.5px;font-weight:700;min-width:38px;font-variant-numeric:tabular-nums}
.fotnote{margin:14px 0 0;font-size:11.5px;line-height:1.45;color:var(--muted)}

.bar{height:var(--bar);border-top:1px solid var(--line);background:var(--paper);display:flex;align-items:center;gap:16px;padding:0 18px;position:relative;z-index:900}
.play{width:44px;height:44px;border-radius:50%;background:var(--deep);color:var(--paper);display:grid;place-items:center;flex:0 0 auto}
.play:hover{background:var(--deeper)}
.play svg{width:17px;height:17px;fill:currentColor}
.klokkestor{font-size:21px;font-weight:800;color:var(--deep);min-width:62px;letter-spacing:-.01em}
.spor{flex:1 1 auto;position:relative;height:52px;min-width:0}
.linje{position:absolute;left:0;right:0;top:25px;height:5px;border-radius:3px;background:var(--line)}
.fylt{position:absolute;left:0;top:25px;height:5px;border-radius:3px;background:var(--amber)}
.etikett{position:absolute;top:0;transform:translateX(-50%);font-size:10.5px;color:var(--muted);white-space:nowrap;letter-spacing:.03em}
.knott{position:absolute;top:19px;width:17px;height:17px;border-radius:50%;background:var(--deep);border:3px solid var(--paper);box-shadow:0 1px 5px rgba(0,0,0,.3);transform:translateX(-50%);cursor:grab;z-index:5}
.fase-pr{position:absolute;top:21px;width:11px;height:11px;border-radius:50%;background:var(--paper);border:2.5px solid #B9C6CC;transform:translateX(-50%);cursor:pointer;z-index:6}
.fase-pr.passert{border-color:var(--amber);background:var(--amber)}
.fase-pr:hover{border-color:var(--deep)}
.merkepinne{position:absolute;top:20px;width:2px;height:15px;background:var(--brick);transform:translateX(-50%)}
.merketekst{position:absolute;top:38px;transform:translateX(-50%);font-size:10.5px;color:var(--brick);white-space:nowrap}
.slutttekst{font-size:12px;color:var(--muted);text-align:right;min-width:92px;flex:0 0 auto}
.slutttekst b{display:block;color:var(--deep);font-size:13px;font-weight:600}

.bussmerke{width:26px;height:26px;border-radius:50%;background:var(--amber);border:3px solid var(--paper);box-shadow:0 2px 8px rgba(0,0,0,.4);display:grid;place-items:center}
.bussmerke span{width:9px;height:9px;border-radius:50%;background:var(--deeper)}
.endemerke{font-size:11px;font-weight:700;color:var(--paper);background:var(--deep);padding:3px 8px;border-radius:4px;white-space:nowrap;box-shadow:0 1px 5px rgba(0,0,0,.35)}
.stedmerke{font-size:10.5px;font-weight:600;color:var(--deep);background:rgba(252,250,246,.92);padding:2px 6px;border-radius:3px;white-space:nowrap;box-shadow:0 1px 4px rgba(0,0,0,.25)}

@media (max-width:900px){
  .top{gap:10px;padding:0 12px}
  .top .brand b{font-size:13px}
  .top .brand small{display:none}
  .top .seg button{padding:4px 8px;font-size:11.5px}
  .bar{padding:0 12px;gap:10px}
  .klokkestor{font-size:18px;min-width:52px}
  .slutttekst{min-width:76px;font-size:11px}
  .wrap{flex-direction:column}
  .panel{flex:1 1 auto;border-left:0;border-top:1px solid var(--line)}
  .kart{flex:0 0 42%}
  .scene{display:none}
  .top .chip{display:none}
}
</style>
</head>
<body>

<header class="top">
  <div class="brand"><b>Reisedagen · tirsdag 8. juni 2027</b><small>Kautokeino → Alta → ombordstigning</small></div>
  <div class="ctrl">
    <span class="chip">28 reisende · <b>DY 321</b> 11:55</span>
    <div class="seg" id="fart">
      <button data-f="1">1 min/s</button><button data-f="2">2</button><button data-f="4" class="on">4</button><button data-f="8">8</button>
    </div>
  </div>
</header>

<div class="wrap">
  <div class="kart">
    <div id="map"></div>
    <div class="maptype" id="maptype"><button data-v="sat" class="on" type="button">Satellitt</button><button data-v="kart" type="button">Kart</button></div>
  </div>
  <aside class="panel">
    <div class="scene" id="scene"></div>
    <div class="tekst">
      <div class="klokke num" id="t-klokke">07:15</div>
      <h2 id="t-tittel">Oppmøte utenfor skolen</h2>
      <div class="sted" id="t-sted">Kautokeino skole</div>
      <p id="t-tekst"></p>
      <div class="neste" id="t-neste"></div>
      <div class="liste" id="t-liste"><h3>Hele dagen</h3></div>
    </div>
  </aside>
</div>

<div class="bar">
  <button class="play" id="play" type="button" aria-label="Spill av"></button>
  <div class="klokkestor num" id="b-klokke">07:15</div>
  <div class="spor" id="spor">
    <div class="linje"></div><div class="fylt" id="fylt"></div>
  </div>
  <div class="slutttekst"><b id="s-klokke">11:25</b>ombordstigning</div>
</div>

<script>/*__LEAFLET_JS__*/</script>
<script>
(function(){
'use strict';
const D = "__DATA__";
const T0 = 7*60 + 0;                       // 07:15 i minutter
const SLUTT = D.slutt;

/* ---------- klokke ---------- */
function klokke(t){
  const m = Math.round(T0 + t);
  return String(Math.floor(m/60)).padStart(2,'0') + ':' + String(m%60).padStart(2,'0');
}

/* ---------- kart ---------- */
const map = L.map('map', {zoomControl:false, attributionControl:true, zoomSnap:0, fadeAnimation:false});
map.attributionControl.setPrefix(false);
const flis = {
  sat: L.tileLayer('https://server.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer/tile/{z}/{y}/{x}',
       {maxZoom:19, attribution:'Bilder: © Esri, Maxar, Earthstar Geographics'}),
  kart: L.tileLayer('https://tile.openstreetmap.org/{z}/{x}/{y}.png',
       {maxZoom:19, attribution:'Kart: © <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a>-bidragsytere'})
};
let flisnaa = 'sat';
flis.sat.addTo(map);
map.setView(D.kautokeino, 11);

L.polyline(D.rute, {color:'#0A2531', weight:6, opacity:.35}).addTo(map);
L.polyline(D.rute, {color:'#E2A02F', weight:3, opacity:.95}).addTo(map);

function endemerke(ll, tekst, klasse){
  return L.marker(ll, {icon: L.divIcon({className:'', html:'<div class="'+klasse+'">'+tekst+'</div>',
         iconSize:[0,0], iconAnchor:[-8,8]}), interactive:false}).addTo(map);
}
endemerke(D.kautokeino, 'Kautokeino skole', 'endemerke');
endemerke(D.alta, 'Alta lufthavn', 'endemerke');
D.steder.forEach(s => {
  L.circleMarker(s.ll, {radius:4, color:'#FCFAF6', weight:2, fillColor:'#123A4A', fillOpacity:1, interactive:false}).addTo(map);
  endemerke(s.ll, s.navn, 'stedmerke');
});

const buss = L.marker(D.kautokeino, {icon: L.divIcon({className:'',
  html:'<div class="bussmerke"><span></span></div>', iconSize:[26,26], iconAnchor:[13,13]}),
  interactive:false, zIndexOffset:500}).addTo(map);

document.getElementById('maptype').addEventListener('click', e => {
  const b = e.target.closest('button'); if(!b) return;
  const v = b.dataset.v; if(v === flisnaa) return;
  map.removeLayer(flis[flisnaa]); flis[v].addTo(map); flisnaa = v;
  [...e.currentTarget.children].forEach(x => x.classList.toggle('on', x === b));
});

/* ---------- posisjon langs ruta ---------- */
function punkt(f){                                   // f = 0..1 av total lengde
  const mal = f * D.total, K = D.kum, P = D.rute;
  if (mal <= 0) return P[0];
  for (let i = 1; i < K.length; i++){
    if (mal <= K[i]){
      const a = P[i-1], b = P[i], d = K[i] - K[i-1];
      const u = d > 0 ? (mal - K[i-1]) / d : 0;
      return [a[0] + (b[0]-a[0])*u, a[1] + (b[1]-a[1])*u];
    }
  }
  return P[P.length-1];
}

function kamera(t){
  // posisjon
  let ll;
  if (t <= D.bussStart) ll = D.rute[0];
  else if (t >= D.bussSlutt) ll = D.alta;
  else ll = punkt((t - D.bussStart) / (D.bussSlutt - D.bussStart));
  // zoom: nær ved start, vidt over vidda, nær igjen ved Alta
  const kf = [[0,13.4],[D.bussStart,11.0],[60,8.9],[110,8.9],[D.bussSlutt-12,11.2],[D.bussSlutt,13.4],[165,14.8],[SLUTT,15.4]];
  let z = kf[kf.length-1][1];
  for (let i = 1; i < kf.length; i++){
    if (t <= kf[i][0]){
      const a = kf[i-1], b = kf[i];
      const u = b[0] === a[0] ? 0 : (t - a[0]) / (b[0] - a[0]);
      z = a[1] + (b[1]-a[1]) * (u*u*(3-2*u));        // mykt inn/ut
      break;
    }
  }
  return {ll, z};
}

/* ---------- faser ---------- */
function faseFor(t){
  let f = D.faser[0];
  for (const x of D.faser) if (t >= x.t) f = x;
  return f;
}
const elListe = document.getElementById('t-liste');
const listeKnapper = [];
D.faser.forEach(f => {
  const b = document.createElement('button');
  b.type = 'button';
  b.innerHTML = '<span class="k">' + klokke(f.t) + '</span><span class="n"></span>';
  b.querySelector('.n').textContent = f.tittel;
  b.addEventListener('click', () => { stopp(); sett(f.t); });
  elListe.appendChild(b);
  listeKnapper.push({el:b, id:f.id});
});
(function(){
  const d = document.createElement('div');
  d.className = 'avg';
  d.innerHTML = '<span class="k">11:55</span><span>DY 321 går til Oslo-Gardermoen</span>';
  elListe.appendChild(d);
  const n = document.createElement('p');
  n.className = 'fotnote';
  n.textContent = 'Bussruta følger den faktiske kjøreruta på E45 (OSRM, 11.11.2026): ' + D.osrmKm
                + ' km og ' + D.osrmMin + ' minutters kjøretid. Masi, Suolovuopmi, Eiby og Øvre Alta er '
                + 'slått opp i OpenStreetMap og ligger alle under 530 m fra veien. Scenene er tegnet. '
                + 'Tidene for innsjekk, sikkerhetskontroll og ombordstigning er vår plan, ikke tider fra Norwegian.';
  elListe.appendChild(n);
})();

const elScene = document.getElementById('scene');
let sceneNaa = null;
function tegnFase(f){
  if (f.id === sceneNaa) return;
  sceneNaa = f.id;
  elScene.innerHTML = D.scener[f.scene] + '<div class="merk">' + f.sted + '</div>';
  document.getElementById('t-klokke').textContent = klokke(f.t);
  document.getElementById('t-tittel').textContent = f.tittel;
  document.getElementById('t-sted').textContent = f.sted;
  document.getElementById('t-tekst').textContent = f.tekst;
  listeKnapper.forEach(o => o.el.classList.toggle('na', o.id === f.id));
  const rute = document.querySelector('.tekst');
  if (rute) rute.scrollTop = 0;
  const i = D.faser.indexOf(f), n = D.faser[i+1];
  document.getElementById('t-neste').innerHTML = n
    ? 'Neste: <b>' + klokke(n.t) + '</b> ' + n.tittel
    : 'Deretter: <b>11:55</b> avgang mot Oslo-Gardermoen';
}

/* ---------- sporet ---------- */
const spor = document.getElementById('spor'), fylt = document.getElementById('fylt');
const prikker = [];
D.faser.forEach(f => {
  const p = document.createElement('div');
  p.className = 'fase-pr'; p.style.left = (100*f.t/SLUTT) + '%';
  p.title = klokke(f.t) + ' ' + f.tittel;
  p.addEventListener('click', () => { stopp(); sett(f.t); });
  spor.appendChild(p); prikker.push({el:p, t:f.t});
});
[D.faser[0], D.faser[D.faser.length-1]].forEach((f,k) => {
  const e = document.createElement('div');
  e.className = 'etikett'; e.style.left = (100*f.t/SLUTT) + '%';
  e.style.transform = k === 0 ? 'translateX(-2px)' : 'translateX(calc(-100% + 2px))';
  e.textContent = klokke(f.t); spor.appendChild(e);
});
D.merker.forEach(m => {
  const s = document.createElement('div');
  s.className = 'merkepinne'; s.style.left = (100*m.t/SLUTT) + '%'; spor.appendChild(s);
  const e = document.createElement('div');
  e.className = 'merketekst'; e.style.left = (100*m.t/SLUTT) + '%';
  e.textContent = klokke(m.t) + ' · ' + m.tekst; spor.appendChild(e);
});
const knott = document.createElement('div');
knott.className = 'knott'; knott.tabIndex = 0; spor.appendChild(knott);

/* ---------- avspilling ---------- */
let t = 0, spiller = false, fart = 4, sist = 0;
const elPlay = document.getElementById('play');
const IKON_PLAY = '<svg viewBox="0 0 24 24"><path d="M7 4.5v15l13-7.5z"/></svg>';
const IKON_PAUSE = '<svg viewBox="0 0 24 24"><path d="M6.5 4.5h4v15h-4zM13.5 4.5h4v15h-4z"/></svg>';

function sett(nt, flyttKart){
  t = Math.max(0, Math.min(SLUTT, nt));
  const p = 100 * t / SLUTT;
  fylt.style.width = p + '%'; knott.style.left = p + '%';
  document.getElementById('b-klokke').textContent = klokke(t);
  prikker.forEach(o => o.el.classList.toggle('passert', t >= o.t - .001));
  tegnFase(faseFor(t));
  if (flyttKart !== false){
    const k = kamera(t);
    buss.setLatLng(k.ll);
    map.setView(k.ll, k.z, {animate:false});
  }
}
function spill(){
  if (t >= SLUTT) t = 0;
  spiller = true; sist = performance.now();
  elPlay.innerHTML = IKON_PAUSE; elPlay.setAttribute('aria-label','Pause');
  requestAnimationFrame(steg);
}
function stopp(){
  spiller = false; elPlay.innerHTML = IKON_PLAY; elPlay.setAttribute('aria-label','Spill av');
}
function steg(naa){
  if (!spiller) return;
  const dt = Math.min(0.25, (naa - sist) / 1000); sist = naa;
  sett(t + dt * fart);
  if (t >= SLUTT){ stopp(); return; }
  requestAnimationFrame(steg);
}
elPlay.innerHTML = IKON_PLAY;
elPlay.addEventListener('click', () => spiller ? stopp() : spill());

document.getElementById('fart').addEventListener('click', e => {
  const b = e.target.closest('button'); if(!b) return;
  fart = +b.dataset.f;
  [...e.currentTarget.children].forEach(x => x.classList.toggle('on', x === b));
});

/* dra i knotten / klikk i sporet */
const SNAPP = SLUTT * 0.018;                       // ca. 4 minutter
function fraKlikk(ev){
  const r = spor.getBoundingClientRect();
  const x = (ev.touches ? ev.touches[0].clientX : ev.clientX) - r.left;
  let nt = SLUTT * Math.max(0, Math.min(1, x / r.width));
  let beste = null, avst = SNAPP;
  for (const f of D.faser){
    const d = Math.abs(f.t - nt);
    if (d <= avst){ avst = d; beste = f.t; }
  }
  sett(beste !== null ? beste : nt);
}
let drar = false;
function ned(ev){ drar = true; stopp(); fraKlikk(ev); ev.preventDefault(); }
spor.addEventListener('mousedown', ned);
spor.addEventListener('touchstart', ned, {passive:false});
window.addEventListener('mousemove', ev => { if (drar) fraKlikk(ev); });
window.addEventListener('touchmove', ev => { if (drar){ fraKlikk(ev); ev.preventDefault(); } }, {passive:false});
window.addEventListener('mouseup', () => drar = false);
window.addEventListener('touchend', () => drar = false);

document.addEventListener('keydown', ev => {
  if (ev.key === ' '){ ev.preventDefault(); spiller ? stopp() : spill(); }
  else if (ev.key === 'ArrowRight'){ stopp(); sett(t + 5); }
  else if (ev.key === 'ArrowLeft'){ stopp(); sett(t - 5); }
  else if (ev.key === 'Home'){ stopp(); sett(0); }
  else if (ev.key === 'End'){ stopp(); sett(SLUTT); }
});

document.getElementById('s-klokke').textContent = klokke(SLUTT);
sett(0);
setTimeout(() => map.invalidateSize(), 60);
window.addEventListener('resize', () => map.invalidateSize());
})();
</script>
</body>
</html>
'''

if __name__ == '__main__':
    ut = KART.parent / 'Klassetur-tidslinje-dag1.html'
    ut.write_text(bygg(), encoding='utf-8')
    print('skrev', ut, ut.stat().st_size, 'byte')
