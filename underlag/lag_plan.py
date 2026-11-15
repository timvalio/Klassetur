# -*- coding: utf-8 -*-
"""lag_plan.py — bygger Klassetur-10B-plan.html

Tredelt side: tidslinja med alle ledd til venstre, regnestykket nederst i samme
spalte slik at det alltid er synlig, og detaljvisning av det man klikker på i de
to tredelene til høyre.
"""
import json, pathlib, sys

HER = pathlib.Path(__file__).resolve().parent
sys.path.insert(0, str(HER))
import plandata as P


LEAFLET_CSS = (HER / 'leaflet.css').read_text(encoding='utf-8')
LEAFLET_JS = (HER / 'leaflet.js').read_text(encoding='utf-8')


def bygg():
    data = dict(
        basis=list(P.BASIS),
        gruppe=P.GRUPPE, elever=P.ELEVER, voksne=P.VOKSNE,
        samletInn=P.SAMLET_INN, samletInnDato=P.SAMLET_INN_DATO, frist=P.FRIST, avreise=P.AVREISE, netter=P.NETTER,
        eur=P.EUR, eurKilde=P.EUR_KILDE,
        bekreftet=P.BEKREFTET,
        flyDepositum=P.FLY_DEPOSITUM, flySum=P.FLY_SUM, bussSum=P.BUSS_SUM,
        transfer=P.TRANSFER, hotell=P.hoteller(), hotellUtelatt=P.HOTELL_UTELATT, mat=P.MAT,
        sikreInntekter=P.SIKRE_INNTEKTER, grunnvalg=P.grunnvalg(),
        aktiviteter=P.AKTIVITETER, buffer=P.BUFFER,
    )
    h = MAL.replace('/*__LEAFLET_CSS__*/', LEAFLET_CSS)
    h = h.replace('/*__LEAFLET_JS__*/', LEAFLET_JS)
    return h.replace('"__DATA__"', json.dumps(data, ensure_ascii=False))


MAL = r'''<!doctype html>
<html lang="no">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Klassetur 10B · plan og kostnad</title>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Archivo:wght@400;500;600;800&family=Newsreader:opsz,wght@6..72,400;6..72,500&display=swap" rel="stylesheet">
<style>/*__LEAFLET_CSS__*/</style>
<style>
:root{
  --deep:#123A4A; --deeper:#0A2531; --amber:#E2A02F; --amber-soft:#F5E3C2; --brick:#A85434;
  --paper:#FCFAF6; --ink:#1B1B1B; --muted:#6B6459; --line:#DFD9CD; --kort:#FFFFFF;
  --ok:#2F6B47; --ok-bg:#E3EFE6; --apen:#96690C; --apen-bg:#F7EBD1;
  --mangler:#8E3F22; --mangler-bg:#F4E1D8; --top:60px;
}
*{box-sizing:border-box}
html,body{height:100%;margin:0}
body{background:var(--paper);color:var(--ink);font-family:'Archivo',system-ui,-apple-system,'Segoe UI',sans-serif;font-size:14.5px;line-height:1.55;overflow:hidden}
button{font:inherit;color:inherit;background:none;border:0;padding:0;cursor:pointer}
a{color:var(--deep)}
.num{font-variant-numeric:tabular-nums}

.top{height:var(--top);background:var(--deep);color:var(--paper);padding:0 20px;display:flex;align-items:center;gap:18px}
.top b{font-size:15.5px;font-weight:800;letter-spacing:-.01em;display:block;line-height:1.2}
.top small{font-size:11px;color:#9FB8C4;letter-spacing:.06em;text-transform:uppercase}
.top .nullstill{margin-left:auto;font-size:12.5px;color:#CFE0E8;border:1px solid rgba(255,255,255,.3);padding:5px 12px;border-radius:999px}
.top .nullstill:hover{background:rgba(255,255,255,.12);color:#fff}

.wrap{height:calc(100% - var(--top));display:grid;grid-template-columns:minmax(330px,34%) 1fr}
.venstre{display:flex;flex-direction:column;min-height:0;border-right:1px solid var(--line);background:var(--paper)}
.liste{flex:1 1 auto;overflow-y:auto;padding:14px 14px 20px}
.hoyre{overflow-y:auto;background:#F7F3EA}

/* ---------- tidslinja ---------- */
.ledd{margin-bottom:12px;background:var(--kort);border:1px solid var(--line);border-radius:9px;overflow:hidden}
.lhode{padding:10px 13px;display:flex;align-items:center;gap:9px;flex-wrap:wrap}
.lhode h2{font-size:14px;font-weight:600;margin:0;letter-spacing:-.01em;flex:1 1 auto;min-width:0}
.lhode .sum{font-weight:800;color:var(--deep);white-space:nowrap;font-size:14.5px}
.lhode .ikkevalgt{font-size:11.5px;font-weight:700;color:var(--apen)}
.merke{font-size:9.5px;font-weight:700;letter-spacing:.07em;text-transform:uppercase;padding:2px 6px;border-radius:3px;white-space:nowrap}
.m-ok{background:var(--ok-bg);color:var(--ok)}
.m-apen{background:var(--apen-bg);color:var(--apen)}

.rad{display:flex;gap:9px;padding:8px 13px;border-top:1px solid var(--line);align-items:flex-start;cursor:pointer}
.rad:hover{background:#FAF6EC}
.rad.pa{background:var(--amber-soft)}
.rad.aktiv{box-shadow:inset 3px 0 0 var(--deep)}
.rad.ingenpris .velg{opacity:.35;pointer-events:none}
.rad .velg{flex:0 0 auto;width:17px;height:17px;margin-top:2px;border:2px solid #AFA896;border-radius:50%;display:grid;place-items:center;background:var(--paper)}
.rad .velg.boks{border-radius:4px}
.rad.pa .velg{border-color:var(--deep);background:var(--deep)}
.rad.pa .velg::after{content:'';width:7px;height:7px;border-radius:50%;background:var(--paper)}
.rad.pa .velg.boks::after{content:'';width:9px;height:5px;border-left:2px solid var(--paper);border-bottom:2px solid var(--paper);transform:rotate(-45deg);border-radius:0;background:none;margin-top:-2px}
.rad .tekst{flex:1 1 auto;min-width:0;display:block}
.rad .navn{display:block;font-weight:600;font-size:13.5px;line-height:1.3}
.rad .meta{display:block;font-size:11.5px;color:var(--muted);line-height:1.35;margin-top:1px;overflow:hidden;text-overflow:ellipsis;white-space:nowrap}
.rad .pris{flex:0 0 auto;text-align:right;white-space:nowrap;font-size:13px;display:block}
.rad .pris b{color:var(--deep);font-weight:700}
.rad .pris small{display:block;font-size:10.5px;color:var(--muted)}
.rad .ingen{font-size:10px;font-weight:700;color:var(--mangler);background:var(--mangler-bg);padding:2px 5px;border-radius:3px}
.vis-mer{padding:8px 13px;border-top:1px solid var(--line);font-size:12.5px;color:var(--deep);font-weight:600;width:100%;text-align:left}
.vis-mer:hover{background:#FAF6EC}

/* ---------- skyvknapper ---------- */
.bryter{display:inline-flex;background:#EFEADF;border-radius:999px;padding:2px;gap:2px}
.bryter button{font-size:11px;font-weight:600;padding:4px 10px;border-radius:999px;color:var(--muted);white-space:nowrap}
.bryter button.on{background:var(--kort);color:var(--deep);box-shadow:0 1px 3px rgba(0,0,0,.14)}

/* ---------- regnskapet ---------- */
.bok{margin-top:6px}
.bok .b{display:flex;justify-content:space-between;gap:10px;padding:1.5px 0;font-size:12px;line-height:1.3}
.bok .b span{color:var(--ink);min-width:0;overflow:hidden;text-overflow:ellipsis;white-space:nowrap}
.bok .b b{font-variant-numeric:tabular-nums;font-weight:600;white-space:nowrap}
.bok .b.inn b{color:var(--ok)}
.bok .b.ut b{color:var(--ink)}
.bok .b.tom span,.bok .b.tom b{color:var(--apen)}
.bok .strek{border-top:1px solid var(--line);margin-top:5px;padding-top:7px}

/* ---------- regnestykket nederst ---------- */
.sumboks{flex:0 0 auto;border-top:2px solid var(--deep);background:var(--kort);padding:10px 14px 12px;max-height:52vh;overflow-y:auto}
.srad{display:flex;justify-content:space-between;gap:10px;font-size:13px;padding:2px 0}
.srad span{color:var(--muted)}
.srad b{font-weight:600}
.stot{display:flex;justify-content:space-between;align-items:baseline;gap:10px;padding:6px 0 2px;border-top:1px solid var(--line);margin-top:6px}
.stot span{font-size:13px;color:var(--muted)}
.stot b{font-size:21px;font-weight:800;color:var(--deep);letter-spacing:-.02em}
.felt{display:flex;gap:8px;margin:8px 0 0}
.felt label{flex:1 1 0;min-width:0}
.felt .l{display:block;font-size:10px;letter-spacing:.06em;text-transform:uppercase;color:var(--muted);margin-bottom:3px}
.felt input{width:100%;font:inherit;font-variant-numeric:tabular-nums;font-weight:700;font-size:14px;color:var(--deep);border:1px solid var(--line);border-radius:6px;padding:5px 8px;background:var(--paper)}
.gap{margin-top:8px;padding:9px 11px;border-radius:7px;background:var(--mangler-bg);color:var(--mangler)}
.gap.nok{background:var(--ok-bg);color:var(--ok)}
.gap .t{font-size:10px;letter-spacing:.06em;text-transform:uppercase;opacity:.85}
.gap .v{font-size:21px;font-weight:800;letter-spacing:-.02em;line-height:1.15}
.gap .u{font-size:12px;margin-top:2px}
.sknapp{margin-top:8px;width:100%;text-align:center;font-size:12.5px;font-weight:600;color:var(--deep);border:1px solid var(--line);border-radius:7px;padding:7px}
.sknapp:hover{background:#FAF6EC}

/* ---------- detaljruta ---------- */
.detalj{max-width:760px;margin:0 auto;padding:26px 30px 60px}
.galleri{margin-bottom:20px}
.galleri .stor{width:100%;aspect-ratio:16/9;object-fit:cover;border-radius:10px;background:#E4DDCE;display:block}
.galleri .strip{display:flex;gap:8px;margin-top:8px}
.galleri .strip button{flex:1 1 0;aspect-ratio:16/10;border-radius:7px;overflow:hidden;border:2px solid transparent;padding:0;background:#E4DDCE}
.galleri .strip button.pa{border-color:var(--deep)}
.galleri .strip img{width:100%;height:100%;object-fit:cover;display:block}
.galleri .tekst{font-size:11.5px;color:var(--muted);margin-top:7px}
.dbilde{width:100%;aspect-ratio:16/9;object-fit:cover;border-radius:10px;background:#E4DDCE;display:block;margin-bottom:20px}
.chips{display:flex;flex-wrap:wrap;gap:7px;margin:0 0 20px}
.chips span{font-size:12.5px;background:var(--kort);border:1px solid var(--line);border-radius:999px;padding:4px 11px;color:#36322C}
.kartboks{margin:0 0 20px}
.kartboks .k{height:260px;border-radius:10px;overflow:hidden;border:1px solid var(--line);background:#DCE6EC}
.kartboks .k:fullscreen{height:100%;width:100%;border:0;border-radius:0}
.kartboks .k.stor{position:fixed;inset:0;height:auto;width:auto;border:0;border-radius:0;z-index:9000}
a.kart-full{font-size:16px;font-weight:700;color:#36322C}
.est{display:block;font-size:10px;letter-spacing:.06em;text-transform:uppercase;color:#8A7A4E;font-weight:700}
.rad .pris small.grunn{display:block;font-size:10px;letter-spacing:.06em;text-transform:uppercase;
  color:var(--deep);font-weight:700}
.rad .pris small.opp{display:block;color:#9A5B2E;font-weight:700}
.rad .pris small.ned{display:block;color:#3F6B45;font-weight:700}
.dest{font-size:11.5px;letter-spacing:.06em;text-transform:uppercase;color:#8A7A4E;font-weight:700;
  background:#F6EFD9;border:1px solid #E4D8B4;border-radius:5px;padding:2px 7px;align-self:center}
.dgrunn{font-size:11.5px;letter-spacing:.06em;text-transform:uppercase;color:var(--deep);font-weight:700;
  background:#E6EDF1;border:1px solid #C9D8E0;border-radius:5px;padding:2px 7px;align-self:center}
.ddiff{font-size:13px;font-weight:700;align-self:center;border-radius:5px;padding:2px 8px}
.ddiff.opp{color:#8A4E22;background:#F7E8DC;border:1px solid #E6CDB8}
.ddiff.ned{color:#2F5A36;background:#E2EEE4;border:1px solid #C4DCC8}
.lnote{font-size:12px;color:var(--muted);padding:8px 13px;border-top:1px solid var(--line);
  background:#FBF8F0;line-height:1.45}
.intro{font-size:12.5px;line-height:1.5;color:#44403A;background:var(--kort);
  border:1px solid var(--line);border-radius:9px;padding:11px 13px;margin-bottom:12px}
.bekreft{font-size:12.5px;color:#6B5324;background:#FBF3DE;border:1px solid #E8DCBB;
  border-radius:8px;padding:10px 13px;margin:0 0 18px;line-height:1.5}
.reise{border:1px solid var(--line);border-radius:8px;padding:11px 13px;margin:0 0 18px;background:var(--kort)}
.reise .rh{font-size:10px;letter-spacing:.07em;text-transform:uppercase;color:var(--muted);margin-bottom:7px}
.reise .rrad{display:flex;align-items:baseline;gap:10px;font-size:13.5px;padding:3px 0}
.reise .rrad span{flex:1}
.reise .rrad.sum{border-top:1px solid var(--line);margin-top:4px;padding-top:6px;font-weight:700}
.reise .ru{font-size:12px;color:var(--muted);margin-top:7px;line-height:1.45}
.kartboks .u{font-size:12px;color:var(--muted);margin-top:6px}
.kartboks.hero{margin-bottom:22px}
.kartboks.hero .k{height:380px}
.typemerke{display:inline-block;font-size:11.5px;font-weight:700;letter-spacing:.06em;
  text-transform:uppercase;color:#6B5E3C;background:#F3ECD9;border:1px solid #E4D8B4;
  border-radius:999px;padding:3px 10px;margin:0 0 10px 8px;vertical-align:2px}
p.lead{font-size:16.5px;line-height:1.55;color:#2E2A24;margin:0 0 18px}
.kartmerke{width:20px;height:20px;border-radius:50%;border:3px solid var(--paper);box-shadow:0 1px 5px rgba(0,0,0,.4)}
.kartmerke.her{background:var(--amber)}
.kartmerke.base{background:var(--deep)}
.kartetikett{font-size:11px;font-weight:700;color:var(--paper);background:var(--deep);padding:2px 7px;border-radius:4px;white-space:nowrap;box-shadow:0 1px 4px rgba(0,0,0,.35)}
h2.dh{font-size:16px;margin:0 0 9px;font-weight:600}
.dmerke{display:inline-block;margin-bottom:8px}
.detalj h1{font-family:'Newsreader',Georgia,serif;font-weight:500;font-size:31px;margin:0 0 4px;letter-spacing:-.015em}
.detalj .under{color:var(--muted);margin:0 0 18px}
.dpris{display:flex;align-items:baseline;gap:12px;flex-wrap:wrap;padding:14px 0;border-top:1px solid var(--line);border-bottom:1px solid var(--line);margin-bottom:18px}
.dpris b{font-size:27px;font-weight:800;color:var(--deep);letter-spacing:-.02em}
.dpris span{color:var(--muted);font-size:13.5px}
.dpris .mangler{font-size:14px;font-weight:700;color:var(--mangler);background:var(--mangler-bg);padding:4px 10px;border-radius:5px}
.dvelg{margin-left:auto;background:var(--deep);color:var(--paper);font-weight:600;font-size:13.5px;padding:9px 18px;border-radius:7px}
.dvelg:hover{background:var(--deeper)}
.dvelg.av{background:var(--amber-soft);color:var(--deep)}
.fakta{margin:0 0 20px;border:1px solid var(--line);border-radius:9px;overflow:hidden;background:var(--kort)}
.fakta div{display:flex;gap:16px;padding:9px 14px;font-size:13.5px}
.fakta div+div{border-top:1px solid var(--line)}
.fakta dt{flex:0 0 38%;color:var(--muted);margin:0}
.fakta dd{flex:1 1 auto;margin:0}
.detalj p{margin:0 0 14px;max-width:62ch}
.dlenke{display:inline-block;font-weight:600;font-size:13.5px}
.tom{color:var(--muted);text-align:center;padding:70px 20px}


.regne{background:var(--kort);border:1px solid var(--line);border-radius:9px;padding:4px 16px;margin:0 0 20px}
.regne .r{display:flex;justify-content:space-between;gap:14px;padding:7px 0;font-size:14px}
.regne .r.sub{font-size:13px;color:var(--muted);padding-left:16px}
.regne .r.strek{border-top:1px solid var(--line);margin-top:3px;padding-top:9px}
.regne .r.tot{border-top:2px solid var(--deep);margin-top:4px;padding-top:11px;font-size:16px}
.regne .r.tot b{font-size:21px;font-weight:800;color:var(--deep)}
.regne .r b{font-variant-numeric:tabular-nums;font-weight:700}
.regne a.bl{color:var(--deep);text-decoration:none;border-bottom:1px solid var(--line)}
.regne a.bl:hover{border-bottom-color:var(--deep)}
.varsel{padding:12px 15px;border-radius:8px;background:var(--mangler-bg);color:var(--mangler);margin:0 0 20px;font-size:13.5px}
.fot{color:var(--muted);font-size:12.5px;border-top:1px solid var(--line);padding-top:14px;margin-top:26px}
.fot p{margin:0 0 7px;max-width:70ch}

@media (max-width:900px){
  body{overflow:auto}
  html,body{height:auto}
  .wrap{display:block;height:auto}
  .venstre{border-right:0}
  .liste{overflow:visible;padding:12px}
  .sumboks{position:sticky;bottom:0;z-index:20;box-shadow:0 -4px 16px rgba(0,0,0,.1)}
  .hoyre{overflow:visible;border-top:1px solid var(--line)}
  .detalj{padding:20px 16px 50px}
}
</style>
</head>
<body>

<header class="top">
  <div><b>Klassetur 10B · Costa Brava</b><small>8.–15. juni 2027 · 28 reisende</small></div>
  <button class="nullstill" id="nullstill" type="button">Tilbake til grunnvalget</button>
</header>

<div class="wrap">
  <div class="venstre">
    <div class="liste" id="liste"></div>
    <div class="sumboks" id="sumboks"></div>
  </div>
  <div class="hoyre" id="hoyre"></div>
</div>

<script>/*__LEAFLET_JS__*/</script>
<script>
(function(){
'use strict';
const D = "__DATA__";
const nf = n => Math.round(n).toLocaleString('no-NO').replace(/ /g,' ');
const esc = s => String(s).replace(/[&<>"]/g, c => ({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;'}[c]));
const dato = s => { const d = new Date(s + 'T00:00:00');
  return isNaN(d) ? s : d.toLocaleDateString('no-NO', {day:'numeric', month:'long', year:'numeric'}); };
const datoKort = s => { const d = new Date(s + 'T00:00:00');
  return isNaN(d) ? s : d.toLocaleDateString('no-NO', {day:'numeric', month:'short'}).replace(/\.$/, ''); };

/* ---------------- tilstand ---------------- */
// alt er valgt fra start: billigste oppsett som henger sammen
const start = {transfer:D.grunnvalg.transfer, hotell:D.grunnvalg.hotell,
               mat:D.grunnvalg.mat, akt:D.grunnvalg.akt.slice(), buffer:D.grunnvalg.buffer};
const erGrunn = (g,id) => D.grunnvalg[g] === id;
let S = JSON.parse(JSON.stringify(start));
let samletInn = D.samletInn, samletInnDato = D.samletInnDato;
let visAlleHotell = false, visPerElev = false;
let vis = {type:'kasse', id:null};
try {
  const l = localStorage.getItem('k10b'); if (l) S = Object.assign(S, JSON.parse(l));
  const k = localStorage.getItem('k10b-inn'); if (k !== null) samletInn = +k;
  const kd = localStorage.getItem('k10b-inndato'); if (kd) samletInnDato = kd;
  const e = localStorage.getItem('k10b-elev'); if (e !== null) visPerElev = e === '1';
} catch(e){}
function lagre(){ try {
  localStorage.setItem('k10b', JSON.stringify(S));
  localStorage.setItem('k10b-inn', String(samletInn));
  localStorage.setItem('k10b-inndato', samletInnDato);
  localStorage.setItem('k10b-elev', visPerElev ? '1' : '0');
} catch(e){} }

/* ---------------- oppslag ---------------- */
const GRUPPER = {transfer:D.transfer, hotell:D.hotell, mat:D.mat, akt:D.aktiviteter,
                 buffer:D.buffer, bekreftet:D.bekreftet};
const finn = (g,id) => (GRUPPER[g]||[]).find(x => x.id === id) || null;
function valgt(){
  return {transfer:finn('transfer',S.transfer), hotell:finn('hotell',S.hotell),
          mat:finn('mat',S.mat), akt:S.akt.map(i=>finn('akt',i)).filter(Boolean),
          buffer:finn('buffer',S.buffer)||D.buffer[0]};
}

/* ---------------- regnestykket ---------------- */
function regn(){
  const v = valgt();
  const bok = [];
  D.bekreftet.forEach(b => bok.push({navn: b.kortnavn || b.tittel, kr: b.kr, id: b.id, g: 'bekreftet'}));
  const bundet = D.bekreftet.reduce((s,b)=>s+b.kr,0);
  let ut = bundet;
  const legg = (navn, o, kr) => {
    if (!o){ bok.push({navn: navn, kr: null}); return; }
    ut += kr; bok.push({navn: navn + ', ' + o.navn, kr: kr, id: o.id, g: o.gruppe});
  };
  if (v.transfer) v.transfer.gruppe = 'transfer';
  legg('Transfer', v.transfer, v.transfer ? (v.transfer.kr||0) : 0);
  if (v.hotell) v.hotell.gruppe = 'hotell';
  legg('Hotell', v.hotell, v.hotell ? v.hotell.kr : 0);
  if (v.hotell){ ut += v.hotell.skatt; bok.push({navn:'Turistskatt', kr: v.hotell.skatt}); }
  if (v.mat) v.mat.gruppe = 'mat';
  legg('Mat', v.mat, v.mat ? v.mat.kr : 0);
  if (v.akt.length){
    const a = v.akt.reduce((s,x)=>s+(x.kr||0),0); ut += a;
    bok.push({navn:'Aktiviteter (' + v.akt.length + ')', kr: a});
  } else bok.push({navn:'Aktiviteter', kr: null});
  const buf = Math.round(ut * (v.buffer.pct||0) / 100);
  if (buf){ ut += buf; bok.push({navn:'Buffer ' + v.buffer.pct + ' %', kr: buf}); }

  const uvalgt = bok.filter(b => b.kr === null).map(b => b.navn);
  // inntekter klassen vet kommer, og som derfor teller med
  const sikre = D.sikreInntekter || [];
  const sikkerSum = sikre.reduce((t,x) => t + (x.kr || 0), 0);
  const sikreMangler = sikre.filter(x => !x.kr).length;
  const mangler = ut - samletInn - sikkerSum;
  const manglerUtenSikre = ut - samletInn;

  const f = new Date(D.frist+'T00:00:00'), n = new Date();
  let mnd = (f.getFullYear()-n.getFullYear())*12 + (f.getMonth()-n.getMonth());
  if (f.getDate() < n.getDate()) mnd -= 1;
  mnd = Math.max(1, mnd);

  return {v, bok, bundet, total: ut, buf, mangler, manglerUtenSikre, uvalgt, mnd,
          sikre, sikkerSum, sikreMangler,
          bundetUdekket: bundet - samletInn - sikkerSum};
}

/* ---------------- venstre: tidslinja ---------------- */
/* Hotell og mat henger sammen: et sted uten måltider kan ikke ha halvpensjon,
   og et sted med frokost og middag kan ikke ha selvhushold. */
function matPasser(h, m){
  if (!h) return true;
  if (h.mat === 'Uten måltider') return m.id !== 'halvpensjon';
  return m.id !== 'selvhushold';
}
function billigsteMat(h){
  const gyldige = D.mat.filter(m => matPasser(h, m));
  return gyldige.reduce((a,b) => (b.kr < a.kr ? b : a), gyldige[0]);
}
/* hva hotellet faktisk koster når maten som må følge med er regnet inn */
function hotellMedMat(h){
  return h.kr + (h.skatt||0) + billigsteMat(h).kr;
}

/* differansen mot grunnvalget, så det synes hva en oppgradering koster */
function diffmerke(g, a){
  if (g === 'akt') return '<small class="num">' + nf(a.kr/D.gruppe) + ' pp</small>';
  if (erGrunn(g, a.id)) return '<small class="grunn">grunnvalg</small>';
  const b = finn(g, D.grunnvalg[g]);
  if (!b || b.kr === null || a.kr === null) return '<small class="num">' + nf(a.kr/D.gruppe) + ' pp</small>';
  const d = g === 'hotell' ? hotellMedMat(a) - hotellMedMat(b) : a.kr - b.kr;
  if (!d) return '<small class="num">samme pris</small>';
  return '<small class="num ' + (d>0?'opp':'ned') + '">' + (d>0?'+':'−') + nf(Math.abs(d)) + '</small>';
}

function rad(g, a, flervalg){
  const pa = flervalg ? S.akt.includes(a.id) : S[g] === a.id;
  const ingen = a.kr === null || a.kr === undefined;
  const aktiv = vis.type === g && vis.id === a.id;
  const d = document.createElement('div');
  d.className = 'rad' + (pa?' pa':'') + (ingen?' ingenpris':'') + (aktiv?' aktiv':'');
  d.innerHTML =
    '<span class="velg' + (flervalg?' boks':'') + '"></span>' +
    '<span class="tekst"><span class="navn">' + esc(a.navn) + '</span>' +
      (a.kort ? '<span class="meta">' + esc(a.kort) + '</span>' : '') + '</span>' +
    '<span class="pris">' + (ingen ? '<span class="ingen">pris mangler</span>'
      : '<b class="num">' + nf(a.kr) + '</b>' + diffmerke(g, a) +
        (a.anslag ? '<small class="est">estimat</small>' : '')) + '</span>';
  d.querySelector('.velg').addEventListener('click', ev => { ev.stopPropagation(); velg(g, a, flervalg); });
  d.addEventListener('click', () => { vis = {type:g, id:a.id}; tegn(); });
  return d;
}

function velg(g, a, flervalg){
  if (a.kr === null || a.kr === undefined) return;
  if (flervalg) S.akt = S.akt.includes(a.id) ? S.akt.filter(x=>x!==a.id) : S.akt.concat([a.id]);
  else S[g] = (S[g] === a.id) ? null : a.id;
  // maten må passe til hotellet
  if (g === 'hotell' && S.hotell){
    const h = finn('hotell', S.hotell), m = finn('mat', S.mat);
    if (!m || !matPasser(h, m)) S.mat = billigsteMat(h).id;
  }
  if (g === 'mat' && S.mat){
    const h = finn('hotell', S.hotell), m = finn('mat', S.mat);
    if (h && !matPasser(h, m)) S.hotell = null;
  }
  tegn();
}

function ledd(o){
  const d = document.createElement('div'); d.className = 'ledd';
  const h = document.createElement('div'); h.className = 'lhode';
  h.innerHTML = '<span class="merke ' + (o.ok?'m-ok':'m-apen') + '">' + (o.ok?'Bekreftet':'Velges') + '</span>' +
    '<h2>' + esc(o.tittel) + '</h2>' +
    (o.sum !== null && o.sum !== undefined
      ? '<span class="sum num">' + nf(o.sum) + '</span>'
      : '<span class="ikkevalgt">ikke valgt</span>');
  if (o.klikk) { h.style.cursor = 'pointer'; h.addEventListener('click', o.klikk); }
  d.appendChild(h);
  (o.rader||[]).forEach(r => d.appendChild(r));
  return d;
}

function tegnListe(){
  const R = regn(), v = R.v;
  const L = document.getElementById('liste'); L.innerHTML = '';

  D.bekreftet.forEach(b => L.appendChild(ledd({ok:true, tittel:b.tittel, sum:b.kr,
    klikk:() => { vis = {type:'bekreftet', id:b.id}; tegn(); }})));

  const intro = document.createElement('div');
  intro.className = 'intro';
  intro.innerHTML = '<b>Alt er valgt fra start.</b> Transfer, hotell og mat står på det billigste ' +
    'oppsettet som henger sammen, og stranda er med fordi den er gratis. ' +
    'Alt annet i lista er oppgraderinger og tillegg — tallet til høyre viser hva de koster ' +
    'i forhold til grunnvalget.';
  L.appendChild(intro);

  L.appendChild(ledd({ok:false, tittel:'Transfer flyplass – hotell',
    sum: v.transfer ? v.transfer.kr : null,
    rader: D.transfer.map(a => rad('transfer', a, false))}));

  const hot = visAlleHotell ? D.hotell : D.hotell.slice(0,5);
  const hr = hot.map(a => rad('hotell', a, false));
  if (!visAlleHotell && D.hotell.length > 5){
    const b = document.createElement('button');
    b.type='button'; b.className='vis-mer';
    b.textContent = 'Vis alle ' + D.hotell.length + ' hoteller →';
    b.addEventListener('click', () => { visAlleHotell = true; tegn(); });
    hr.push(b);
  }
  if (D.hotellUtelatt && D.hotellUtelatt.length){
    const n = document.createElement('div'); n.className = 'lnote';
    n.textContent = 'Alle hotellpriser er estimater fra ett booking.com-søk — ingen gruppepris er ' +
      'innhentet. ' + D.hotellUtelatt.length + ' hoteller er tatt ut av lista: ' +
      D.hotellUtelatt.map(x => x[0] + ' (' + x[1] + ')').join('; ') + '.';
    hr.push(n);
  }
  L.appendChild(ledd({ok:false, tittel:'Hotell, 7 netter', sum: v.hotell ? v.hotell.kr : null, rader:hr}));

  L.appendChild(ledd({ok:false, tittel:'Mat', sum: v.mat ? v.mat.kr : null,
    rader: D.mat.map(a => rad('mat', a, false))}));

  L.appendChild(ledd({ok:false, tittel:'Aktiviteter — tillegg',
    sum: v.akt.length ? v.akt.reduce((s,x)=>s+(x.kr||0),0) : null,
    rader: D.aktiviteter.map(a => rad('akt', a, true))}));

  const grunn = R.total - R.buf;
  L.appendChild(ledd({ok:false, tittel:'Buffer', sum: R.buf || null,
    rader: D.buffer.map(a => rad('buffer',
      {id:a.id, navn:a.navn, kr: Math.round(grunn*a.pct/100),
       kort: a.pct ? a.pct + ' prosent av summen over' : 'ingenting lagt til'}, false))}));
}

/* ---------------- venstre: regnskapet ---------------- */
function tegnSum(){
  const R = regn();
  const del = visPerElev ? D.elever : 1;
  const v = x => nf(x / del);
  const B = document.getElementById('sumboks');

  let rader = '<div class="b inn"><span>Samlet inn per ' + datoKort(samletInnDato) +
              '</span><b class="num">+' + v(samletInn) + '</b></div>';
  R.sikre.forEach(i => {
    rader += '<div class="b ' + (i.kr ? 'inn' : 'tom') + '"><span>' + esc(i.navn) +
      (i.dato ? ' <small style="opacity:.7">' + datoKort(i.dato) + '</small>' : '') + '</span>' +
      (i.kr ? '<b class="num">+' + v(i.kr) + '</b>' : '<b>beløp mangler</b>') + '</div>';
  });
  R.bok.forEach(p => {
    if (p.kr === null) rader += '<div class="b tom"><span>' + esc(p.navn) + '</span><b>ikke valgt</b></div>';
    else rader += '<div class="b ut"><span>' + esc(p.navn) + '</span><b class="num">−' + v(p.kr) + '</b></div>';
  });

  B.innerHTML =
    '<div style="display:flex;align-items:center;gap:8px;margin-bottom:2px">' +
      '<span style="font-size:10px;letter-spacing:.07em;text-transform:uppercase;color:var(--muted);flex:1">Regnskap</span>' +
      '<span class="bryter" id="br-elev">' +
        '<button type="button" data-v="0"' + (visPerElev?'':' class="on"') + '>Hele klassen</button>' +
        '<button type="button" data-v="1"' + (visPerElev?' class="on"':'') + '>Per elev</button>' +
      '</span>' +
    '</div>' +
    '<div class="bok">' + rader + '</div>' +
    '<div class="gap' + (R.mangler<=0?' nok':'') + '" style="margin-top:9px">' +
      '<div class="t">' + (R.mangler>0?'Mangler':'Til overs') + '</div>' +
      '<div class="v num">' + nf(Math.abs(R.mangler) / del) + '</div>' +
      '<div class="u">' + (R.mangler>0
        ? 'til sammen' + (visPerElev?' per elev':' for hele klassen') + ' — ' +
          nf(R.mangler / del / R.mnd) + ' per måned i ' + R.mnd + ' måneder til ' + dato(D.frist)
        : 'det som er valgt er dekket') + '</div>' +
      (R.sikkerSum
        ? '<div class="u" style="margin-top:4px">Sikre inntekter på ' + v(R.sikkerSum) +
          ' er regnet med. Uten dem ville det stått ' + nf(Math.abs(R.manglerUtenSikre)/del) + '.</div>'
        : '') +
      (R.sikreMangler
        ? '<div class="u" style="margin-top:4px">' + R.sikreMangler + ' sikker inntekt mangler beløp ' +
          'og er ikke regnet med.</div>'
        : '') +
    '</div>' +
    '<div class="felt">' +
      '<label style="flex:1.3"><span class="l">Samlet inn så langt</span>' +
      '<input class="num" id="f-inn" inputmode="numeric"></label>' +
      '<label style="flex:1"><span class="l">Per dato</span>' +
      '<input type="date" id="f-dato" style="font-size:12.5px;font-weight:600"></label></div>' +
    '<button class="sknapp" id="b-kasse" type="button">Vis regnskapet i full bredde →</button>';

  const fi = document.getElementById('f-inn'), fd = document.getElementById('f-dato');
  fi.value = nf(samletInn); fd.value = samletInnDato;
  fi.addEventListener('input', () => { samletInn = +fi.value.replace(/\D/g,'')||0; lagre(); tegnSum(); tegnDetalj(); });
  fd.addEventListener('change', () => { samletInnDato = fd.value || samletInnDato; lagre(); tegnSum(); tegnDetalj(); });
  document.getElementById('br-elev').addEventListener('click', e => {
    const b = e.target.closest('button'); if(!b) return;
    visPerElev = b.dataset.v === '1'; lagre(); tegnSum(); tegnDetalj();
  });
  document.getElementById('b-kasse').addEventListener('click', () => { vis={type:'kasse',id:null}; tegn(); });
}

/* ---------------- høyre: detaljruta ---------------- */
function faktaliste(f){
  if (!f || !f.length) return '';
  return '<dl class="fakta">' + f.map(([k,v]) =>
    '<div><dt>' + esc(k) + '</dt><dd>' + esc(v) + '</dd></div>').join('') + '</dl>';
}

function detaljDiff(g, o){
  if (!D.grunnvalg[g]) return '';
  if (erGrunn(g, o.id)) return '<span class="dgrunn">grunnvalg</span>';
  const b = finn(g, D.grunnvalg[g]);
  if (!b || b.kr === null || o.kr === null) return '';
  const d = g === 'hotell' ? hotellMedMat(o) - hotellMedMat(b) : o.kr - b.kr;
  if (!d) return '<span class="dgrunn">samme pris som grunnvalget</span>';
  return '<span class="ddiff ' + (d>0?'opp':'ned') + '">' + (d>0?'+':'−') + nf(Math.abs(d)) +
         ' mot grunnvalget</span>';
}

function detaljObjekt(g, o){
  const flervalg = g === 'akt';
  const pa = flervalg ? S.akt.includes(o.id) : S[g] === o.id;
  const ingen = o.kr === null || o.kr === undefined;
  const erBekreftet = g === 'bekreftet';
  const del = visPerElev ? D.elever : 1;

  // bildene: hoteller har booking-bilder, aktiviteter har Commons-bilder med kreditering
  let bilder = [];
  if (o.bilder && o.bilder.length) bilder = o.bilder.map(u => ({url:u, kreditt:''}));
  else if (o.bilder2 && o.bilder2.length)
    bilder = o.bilder2.map(b => ({url:b.url, kreditt:b.tittel + ' · foto ' + b.fotograf + ', ' + b.lisens}));
  else if (o.bilde) bilder = [{url:o.bilde, kreditt:''}];

  const utenBilde = !bilder.length && !!o.koord;
  window.__satellitt = utenBilde;

  let h = '';
  if (utenBilde)
    h += '<div class="kartboks hero"><div class="k" id="d-kart"></div>' +
         '<div class="u" id="d-kart-u"></div></div>';
  if (bilder.length){
    h += '<div class="galleri" id="gal">' +
      '<img class="stor" id="gal-stor" src="' + esc(bilder[0].url) + '" alt="' + esc(o.navn||o.tittel) + '" loading="lazy">';
    if (bilder.length > 1){
      h += '<div class="strip">' + bilder.map((b,i) =>
        '<button type="button" data-i="' + i + '"' + (i===0?' class="pa"':'') +
        '><img src="' + esc(b.url) + '" alt="" loading="lazy"></button>').join('') + '</div>';
    }
    h += '<div class="tekst" id="gal-tekst">' + esc(bilder[0].kreditt) + '</div></div>';
  }

  h += '<span class="merke ' + (erBekreftet?'m-ok':'m-apen') + ' dmerke">' +
       (erBekreftet?'Bekreftet':'Må velges') + '</span>';
  if (o.type) h += '<span class="typemerke">' + esc(o.type) + '</span>';
  h += '<h1>' + esc(o.navn || o.tittel) + '</h1>';
  if (o.hvem) h += '<p class="under">' + esc(o.hvem) + '</p>';
  else if (o.sted) h += '<p class="under">' + esc(o.sted) + '</p>';
  if (o.hvaer) h += '<p class="lead">' + esc(o.hvaer) + '</p>';

  h += '<div class="dpris">' +
    (ingen ? '<span class="mangler">pris mangler</span><span>må innhentes før dette kan velges</span>'
     : (o.anslag ? '<span class="dest">estimat</span>' : '') +
       (erBekreftet || flervalg ? '' : detaljDiff(g, o)) +
       '<b class="num">' + nf(o.kr/del) + '</b><span>kroner ' +
       (visPerElev ? 'per elev · ' + nf(o.kr/D.gruppe) + ' per reisende'
                   : 'for hele klassen · ' + nf(o.kr/D.gruppe) + ' per reisende') + '</span>') +
    (erBekreftet || ingen ? '' :
      '<button class="dvelg' + (pa?' av':'') + '" id="d-velg" type="button">' +
      (pa ? (flervalg?'Fjern fra planen':'Valgt — klikk for å fjerne') : (flervalg?'Legg til':'Velg dette')) + '</button>') +
    '</div>';

  if (o.reise && o.reise.kr){
    const r = o.reise;
    h += '<div class="reise">' +
      '<div class="rh">Reise fram og tilbake</div>' +
      '<div class="rrad"><span>Billetter</span><b class="num">' + nf(o.billettKr/del) + '</b></div>' +
      '<div class="rrad"><span>' + esc(r.hva) + '</span><b class="num">' + nf(r.kr/del) + '</b></div>' +
      '<div class="rrad sum"><span>Til sammen</span><b class="num">' + nf(o.kr/del) + '</b></div>' +
      '<div class="ru">' +
      (r.km ? r.km + ' km hver vei fra Santa Susanna, omtrent ' +
        (r.minutter >= 60 ? Math.floor(r.minutter/60) + ' t ' + (r.minutter%60) + ' min' : r.minutter + ' minutter') +
        ' med bil. ' : '') +
      'Bussprisen er ' + esc(r.kilde) + '.</div></div>';
  } else if (o.reise && o.reise.hva && o.gruppe !== 'hotell'){
    h += '<div class="reise"><div class="rh">Reise</div><div class="ru" style="margin-top:0">' +
      esc(o.reise.hva) + '.</div></div>';
  }
  if (o.husregler){
    h += '<div class="bekreft"><b>Må bekreftes med hotellet før dette velges.</b> ' +
      (o.husregler.length
        ? 'Husreglene oppgir at ' + o.husregler.join(', og at ') + '. '
        : 'Husreglene oppgir ingen aldersgrense eller gruppesperre. ') +
      'Ingen av hotellene sier noe om skoleklasser, så at en gruppe på 21 elever på 15–16 år ' +
      'og 7 voksne tas imot, må bekreftes skriftlig. Kilde: ' + esc(o.husreglerKilde) + '.</div>';
  }
  if (o.beskrivelse) h += '<p>' + esc(o.beskrivelse) + '</p>';
  if (o.fasiliteter && o.fasiliteter.length)
    h += '<div class="chips">' + o.fasiliteter.map(f => '<span>' + esc(f) + '</span>').join('') + '</div>';

  if (o.koord && !utenBilde)
    h += '<div class="kartboks"><h2 class="dh">Hvor det ligger</h2>' +
         '<div class="k" id="d-kart"></div><div class="u" id="d-kart-u"></div></div>';

  h += faktaliste(o.fakta);
  if (o.tekst) h += '<p>' + esc(o.tekst) + '</p>';
  if (o.lenke) h += '<a class="dlenke" href="' + esc(o.lenke) + '" target="_blank" rel="noopener">' +
                    esc(o.lenketekst || 'Kilde') + ' →</a>';
  window.__bilder = bilder;
  window.__koord = o.koord || null;
  window.__navn = o.navn || o.tittel;
  return h;
}

/* ---------- kart i detaljruta ---------- */
let kartInst = null;
function avstand(a, b){
  const R = 6371, t = x => x * Math.PI / 180;
  const d1 = t(b[0]-a[0]), d2 = t(b[1]-a[1]);
  const q = Math.sin(d1/2)**2 + Math.cos(t(a[0]))*Math.cos(t(b[0]))*Math.sin(d2/2)**2;
  return 2 * R * Math.asin(Math.sqrt(q));
}
function tegnKart(koord, navn, omtrentlig, satellitt){
  const el = document.getElementById('d-kart');
  if (!el || !koord) return;
  if (kartInst){ kartInst.remove(); kartInst = null; }
  const m = L.map(el, {zoomControl:true, attributionControl:true, scrollWheelZoom:false});
  m.attributionControl.setPrefix(false);
  // Esri, ikke OpenStreetMap: OSM avviser oppslag fra en lokal fil uten referrer.
  const E = 'https://server.arcgisonline.com/ArcGIS/rest/services/';
  const gatekart = L.tileLayer(E + 'World_Street_Map/MapServer/tile/{z}/{y}/{x}',
    {maxZoom:19, attribution:'Kart: © Esri og bidragsytere'});
  const flyfoto = L.layerGroup([
    L.tileLayer(E + 'World_Imagery/MapServer/tile/{z}/{y}/{x}',
      {maxZoom:19, attribution:'Bilder: © Esri, Maxar, Earthstar Geographics'}),
    L.tileLayer(E + 'Reference/World_Boundaries_and_Places/MapServer/tile/{z}/{y}/{x}',
      {maxZoom:19})]);
  (satellitt ? flyfoto : gatekart).addTo(m);
  L.control.layers({'Kart': gatekart, 'Satellitt': flyfoto}, null,
    {position:'topright', collapsed:false}).addTo(m);

  const full = L.control({position:'topleft'});
  full.onAdd = function(){
    const d = L.DomUtil.create('div', 'leaflet-bar');
    const a = L.DomUtil.create('a', 'kart-full', d);
    a.href = '#'; a.title = 'Vis kartet i fullskjerm';
    a.setAttribute('role', 'button'); a.innerHTML = '⤢';
    L.DomEvent.on(a, 'click', function(e){ L.DomEvent.stop(e); vekslFull(); });
    L.DomEvent.disableClickPropagation(d);
    return d;
  };
  full.addTo(m);
  const ikon = (k) => L.divIcon({className:'', html:'<div class="kartmerke ' + k + '"></div>',
    iconSize:[20,20], iconAnchor:[10,10]});
  L.marker(koord, {icon:ikon('her')}).addTo(m);
  L.marker(koord, {icon:L.divIcon({className:'', html:'<div class="kartetikett">' + navn + '</div>',
    iconSize:[0,0], iconAnchor:[-14,8]}), interactive:false}).addTo(m);
  const d = avstand(D.basis, koord);
  if (satellitt){
    // satellittbildet erstatter fotografiet, så det skal vise stedet tett på
    m.setView(koord, 16);
  } else if (d > 0.4){
    L.marker(D.basis, {icon:ikon('base')}).addTo(m);
    L.marker(D.basis, {icon:L.divIcon({className:'', html:'<div class="kartetikett">Santa Susanna</div>',
      iconSize:[0,0], iconAnchor:[-14,8]}), interactive:false}).addTo(m);
    m.fitBounds(L.latLngBounds([D.basis, koord]).pad(0.35));
  } else m.setView(koord, 15);
  const u = document.getElementById('d-kart-u');
  if (u) u.textContent = (d > 0.4 ? 'Omtrent ' + (d < 10 ? d.toFixed(1).replace('.', ',') : Math.round(d)) +
      ' km i luftlinje fra Santa Susanna. ' : 'I Santa Susanna. ') +
      (omtrentlig ? 'Punktet viser stedet, ikke selve bygningen — adressen må sjekkes ved bestilling. ' : '') +
      (window.__satellitt ? 'Satellittbilde fordi det ikke finnes fritt lisensierte fotografier av stedet.' : '');
  setTimeout(() => m.invalidateSize(), 60);
  kartInst = m;
}

/* fullskjerm: ekte fullskjerm der nettleseren tillater det, ellers kartet
   strukket over hele vinduet */
function settFullIkon(){
  const a = document.querySelector('a.kart-full');
  const el = document.getElementById('d-kart');
  if (!a || !el) return;
  const pa = document.fullscreenElement === el || el.classList.contains('stor');
  a.innerHTML = pa ? '⤡' : '⤢';
  a.title = pa ? 'Lukk fullskjerm' : 'Vis kartet i fullskjerm';
  if (kartInst) setTimeout(() => kartInst.invalidateSize(), 80);
}
function vekslFull(){
  const el = document.getElementById('d-kart');
  if (!el) return;
  if (document.fullscreenElement){ document.exitFullscreen(); return; }
  if (el.classList.contains('stor')){ el.classList.remove('stor'); settFullIkon(); return; }
  let p = null;
  try { p = el.requestFullscreen && el.requestFullscreen(); } catch (e) { p = null; }
  Promise.resolve(p).then(() => settFullIkon())
    .catch(() => { el.classList.add('stor'); settFullIkon(); });
  if (!p){ el.classList.add('stor'); settFullIkon(); }
}
document.addEventListener('fullscreenchange', settFullIkon);
document.addEventListener('keydown', e => {
  if (e.key !== 'Escape') return;
  const el = document.getElementById('d-kart');
  if (el && el.classList.contains('stor')){ el.classList.remove('stor'); settFullIkon(); }
});


function detaljKasse(){
  const R = regn();
  const del = visPerElev ? D.elever : 1;
  const v = x => nf(x / del);
  const enhet = visPerElev ? 'per elev' : 'for hele klassen';

  let h = '<h1>Regnskap</h1>' +
    '<p class="under">Det vi har samlet inn, minus alt turen koster. Nederst står det som mangler.</p>';

  h += '<div style="display:flex;gap:8px;margin:0 0 16px">' +
    '<span class="bryter" id="d-elev">' +
      '<button type="button" data-v="0"' + (visPerElev?'':' class="on"') + '>Hele klassen</button>' +
      '<button type="button" data-v="1"' + (visPerElev?' class="on"':'') + '>Per elev (21)</button>' +
    '</span></div>';

  h += '<div class="regne">' +
    '<div class="r"><span>Samlet inn så langt<br><small style="color:var(--muted)">status per ' +
      dato(samletInnDato) + '</small></span><b class="num" style="color:var(--ok)">+' + v(samletInn) + '</b></div>';
  R.sikre.forEach(i => {
    h += '<div class="r"><span>' + esc(i.navn) +
      '<br><small style="color:var(--muted)">sikker inntekt' +
      (i.dato ? ', ' + dato(i.dato) : '') + '</small></span>' +
      (i.kr ? '<b class="num" style="color:var(--ok)">+' + v(i.kr) + '</b>'
            : '<b style="color:var(--muted)">beløp mangler</b>') + '</div>';
  });
  R.bok.forEach(b => {
    h += '<div class="r">' +
      (b.id ? '<span><a href="#" data-g="' + b.g + '" data-i="' + b.id + '" class="bl">' + esc(b.navn) + '</a></span>'
            : '<span>' + esc(b.navn) + '</span>') +
      (b.kr === null ? '<b style="color:var(--apen)">ikke valgt</b>'
                     : '<b class="num">−' + v(b.kr) + '</b>') + '</div>';
  });
  h += '<div class="r tot"><span>' + (R.mangler>0 ? 'Mangler' : 'Til overs') + '</span>' +
       '<b class="num" style="color:' + (R.mangler>0?'var(--mangler)':'var(--ok)') + '">' +
       (R.mangler>0?'−':'+') + v(Math.abs(R.mangler)) + '</b></div>';
  if (R.mangler > 0)
    h += '<div class="r sub"><span>fordelt på ' + R.mnd + ' måneder fram til ' + dato(D.frist) + '</span>' +
         '<b class="num">' + v(R.mangler / R.mnd) + ' per måned</b></div>';
  h += '</div>';

  if (R.mangler > 0)
    h += '<div class="varsel"><b>' + v(R.mangler) + ' kroner ' + enhet + '.</b> ' +
         'Siste innbetaling er satt til ' +
         dato(D.frist) + ', første virkedag etter påska. Da er det ' + R.mnd + ' måneder igjen.</div>';

  if (R.bundetUdekket > 0)
    h += '<div class="varsel">Fly og buss alene er <b>' + v(R.bundetUdekket) + '</b> mer enn det som er samlet inn. ' +
         'De to er bindende uansett hva dere velger videre.</div>';

  if (R.uvalgt.length)
    h += '<div class="varsel" style="background:var(--apen-bg);color:var(--apen)">Ikke valgt ennå: ' +
         esc(R.uvalgt.join(', ')) + '. Regnskapet er derfor ikke komplett.</div>';

  h += '<p>Depositumet på flyet, ' + nf(D.flyDepositum) + ', er betalt. Restbeløpet på ' +
       nf(D.flySum - D.flyDepositum) + ' forfaller 9. mai 2027, altså etter innsamlingsfristen, og ' +
       'bussen faktureres først etter turen. Hotellene i lista krever ingen forskuddsbetaling.</p>';
  h += fotnoter();
  return h;
}

function fotnoter(){
  return '<div class="fot">' +
    '<p><b>Grunnlag.</b> Flyprisen er Norwegians bekreftede gruppetilbud Y7XH8L. Bussprisen er bekreftet ' +
    'av Nils Rune Eira. Hotellprisene er booking.com sine gruppepriser for alle 28 i ett søk, slått opp ' +
    '14. oktober 2026 for 8.–15. juni 2027. Inngangsbilletter er veiledende nettpriser slått opp ' +
    '13. november 2026. Eurobeløp er regnet om med ' + String(D.eur).replace('.',',') + ' (' + D.eurKilde + ').</p>' +
    '<p><b>Anslag, ikke tilbud.</b> Hotellprisene er booking.com-søk uten gruppepris. Matpostene er ' +
    'anslag. Bussen til aktivitetene er regnet ut fra publiserte satser for leiebuss med sjåfør, ' +
    'ikke fra spanske tilbud. Fortsatt uten pris: privat buss fra flyplassen, tog fra flyplassen om ' +
    'kvelden, og billetten til Tossa de Mar.</p>' +
    '<p><b>Valgene lagres i din egen nettleser.</b> Andre som åpner sida ser sine egne valg.</p></div>';
}

function tegnDetalj(){
  const H = document.getElementById('hoyre');
  let h;
  if (vis.type === 'kasse') h = detaljKasse();
  else {
    const o = finn(vis.type, vis.id);
    h = o ? detaljObjekt(vis.type, o) : '<div class="tom">Klikk på et alternativ i lista.</div>';
  }
  if (kartInst){ kartInst.remove(); kartInst = null; }
  H.innerHTML = '<div class="detalj">' + h + '</div>';
  H.scrollTop = 0;
  const gal = document.getElementById('gal');
  if (gal) gal.querySelectorAll('.strip button').forEach(b => b.addEventListener('click', () => {
    const i = +b.dataset.i, bl = window.__bilder[i];
    document.getElementById('gal-stor').src = bl.url;
    document.getElementById('gal-tekst').textContent = bl.kreditt;
    gal.querySelectorAll('.strip button').forEach(x => x.classList.toggle('pa', x === b));
  }));
  if (window.__koord){
    const o = finn(vis.type, vis.id);
    tegnKart(window.__koord, window.__navn, o && o.omtrentlig, window.__satellitt);
  }
  const b = document.getElementById('d-velg');
  if (b) b.addEventListener('click', () => {
    const o = finn(vis.type, vis.id);
    if (o) velg(vis.type, o, vis.type === 'akt');
  });
  H.querySelectorAll('a.bl').forEach(a => a.addEventListener('click', ev => {
    ev.preventDefault(); vis = {type:a.dataset.g, id:a.dataset.i}; tegn();
  }));
  const be = document.getElementById('d-elev');
  if (be) be.addEventListener('click', e => { const t=e.target.closest('button'); if(!t) return;
    visPerElev = t.dataset.v === '1'; lagre(); tegnSum(); tegnDetalj(); });
}

function tegn(){ lagre(); tegnListe(); tegnSum(); tegnDetalj(); }

document.getElementById('nullstill').addEventListener('click', () => {
  S = JSON.parse(JSON.stringify(start));
  samletInn = D.samletInn; samletInnDato = D.samletInnDato; visAlleHotell = false; visPerElev = false;
  try { localStorage.removeItem('k10b'); } catch(e){}
  vis = {type:'kasse', id:null};
  tegn();
});

tegn();
})();
</script>
</body>
</html>
'''

if __name__ == '__main__':
    html = bygg()
    # Sida skal ligge to steder i repoet: i rota for lokal bruk, og som
    # docs/index.html, som er forsida GitHub Pages publiserer. Uten kopien i
    # docs/ blir endringene liggende i repoet uten å vises på nettstedet.
    # NB: underlag/lag_kart.py skriver også til docs/index.html. Kjøres den,
    # blir forsida overskrevet med det gamle kartet.
    rot = HER.parent if HER.name == 'underlag' else HER
    mål = [rot / 'Klassetur-10B-plan.html']
    if (rot / 'docs').is_dir():
        mål.append(rot / 'docs' / 'index.html')
    for m in mål:
        m.write_text(html, encoding='utf-8')
        print('skrev', m, m.stat().st_size, 'byte')
