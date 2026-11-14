# -*- coding: utf-8 -*-
"""Tegnede scener til tidslinja for reisedagen 8. juni 2027.

Hver scene er en frittstaende SVG paa 400x260. Fargene foelger sida:
deep #123A4A, amber #E2A02F, brick #A85434, paper #FCFAF6.
Scenene er illustrasjoner, ikke foto - de skal byttes ut med ekte bilder
etter hvert som vi faar tak i dem.
"""

import buss_inne

W, H = 400, 260

def _def(extra=""):
    return f'''<defs>
<linearGradient id="g-sky" x1="0" y1="0" x2="0" y2="1">
  <stop offset="0" stop-color="#9DC2D6"/><stop offset=".55" stop-color="#CFE0E8"/><stop offset="1" stop-color="#F0E6D2"/>
</linearGradient>
<linearGradient id="g-sky-hi" x1="0" y1="0" x2="0" y2="1">
  <stop offset="0" stop-color="#7FAEC6"/><stop offset=".6" stop-color="#C3D9E4"/><stop offset="1" stop-color="#E9DFCE"/>
</linearGradient>
<linearGradient id="g-room" x1="0" y1="0" x2="0" y2="1">
  <stop offset="0" stop-color="#F3EFE6"/><stop offset="1" stop-color="#DCD5C7"/>
</linearGradient>
<linearGradient id="g-win" x1="0" y1="0" x2="0" y2="1">
  <stop offset="0" stop-color="#BBD6E4"/><stop offset="1" stop-color="#E4D9C4"/>
</linearGradient>
{extra}</defs>'''

def _wrap(body, defs=""):
    return (f'<svg viewBox="0 0 {W} {H}" xmlns="http://www.w3.org/2000/svg" '
            f'preserveAspectRatio="xMidYMid slice" role="img">{_def(defs)}{body}</svg>')

# ---------- byggeklosser ----------

def folk(x, y, n=4, s=1.0, farger=None, bag=True):
    """En liten gruppe mennesker, sett forfra. y = bakkelinje."""
    farger = farger or ["#A85434", "#123A4A", "#2F6B47", "#96690C", "#7C746A", "#8E3F22"]
    ut = []
    for i in range(n):
        dx = x + i * 13 * s + (i % 3) * 2 * s
        dy = y - (i % 2) * 2 * s
        c = farger[i % len(farger)]
        h = 26 * s
        ut.append(
            f'<g transform="translate({dx:.1f},{dy:.1f}) scale({s:.2f})">'
            f'<rect x="-4" y="-18" width="8" height="12" rx="3.2" fill="{c}"/>'
            f'<rect x="-3.4" y="-7" width="2.8" height="8" rx="1.1" fill="#2B3A42"/>'
            f'<rect x="0.6" y="-7" width="2.8" height="8" rx="1.1" fill="#2B3A42"/>'
            f'<circle cx="0" cy="-22.5" r="3.6" fill="#E8C9A8"/>'
            + (f'<rect x="4" y="-13" width="6" height="8" rx="1.6" fill="#123A4A" opacity=".75"/>' if bag and i % 2 == 0 else "")
            + '</g>')
    return "".join(ut)

def bjork(x, y, s=1.0, mork=False):
    st = "#3E5A3A" if mork else "#5C7A46"
    return (f'<g transform="translate({x},{y}) scale({s})">'
            f'<path d="M0 0 L-1.6 -22 L1.6 -22 Z" fill="#E9E3D6"/>'
            f'<path d="M-1 -14 l-5 -6 M1 -17 l6 -7" stroke="#CFC7B6" stroke-width="1.2" fill="none"/>'
            f'<ellipse cx="0" cy="-26" rx="10" ry="8" fill="{st}"/>'
            f'<ellipse cx="-6" cy="-22" rx="6" ry="5" fill="{st}" opacity=".85"/>'
            f'<ellipse cx="6.5" cy="-23" rx="6" ry="5" fill="{st}" opacity=".9"/>'
            f'</g>')

def snofonn(x, y, w, h):
    return (f'<path d="M{x} {y} q{w*0.2} {-h} {w*0.5} {-h*0.6} q{w*0.3} {-h*0.3} {w*0.5} {h*0.6} Z" '
            f'fill="#F4F1EA" opacity=".93"/>')

def hvit_buss(x, y, s=1.0, dor_apen=False, luke_apen=False, speil=True):
    """Hvit buss sett fra siden, front mot hoyre."""
    d = []
    d.append(f'<g transform="translate({x},{y}) scale({s})">')
    d.append('<ellipse cx="78" cy="2" rx="86" ry="5" fill="#1B1B1B" opacity=".16"/>')
    # karosseri
    d.append('<path d="M2 -52 q0 -8 9 -8 H140 q14 0 18 10 l6 16 q2 6 2 12 V-6 q0 6 -6 6 H6 q-6 0 -6 -6 V-44 Z" '
             'fill="#FBFAF7" stroke="#D4CEC0" stroke-width="1.4"/>')
    # vindusbånd
    d.append('<path d="M10 -50 H128 q8 0 11 7 l5 11 H10 Z" fill="#6E8C9E" opacity=".35"/>')
    for i in range(6):
        d.append(f'<rect x="{12+i*19}" y="-49" width="16" height="17" rx="2" fill="#AFC8D6"/>')
    d.append('<path d="M133 -49 q7 1 10 8 l4 9 h-18 Z" fill="#AFC8D6"/>')  # frontrute
    # stripe
    d.append('<rect x="2" y="-20" width="162" height="4" fill="#123A4A" opacity=".85"/>')
    d.append('<rect x="2" y="-14" width="162" height="2" fill="#E2A02F" opacity=".9"/>')
    # dør
    if dor_apen:
        d.append('<rect x="104" y="-30" width="18" height="30" fill="#2B3A42" opacity=".55"/>')
        d.append('<path d="M104 -30 l-13 -5 v34 l13 -3 Z" fill="#E7E2D6" stroke="#D4CEC0"/>')
        d.append('<path d="M106 -2 h16 l3 6 h-22 Z" fill="#9AA3A8"/>')
    else:
        d.append('<rect x="104" y="-30" width="18" height="30" rx="1" fill="#CBD8E0" stroke="#D4CEC0"/>')
        d.append('<line x1="113" y1="-30" x2="113" y2="0" stroke="#AFBCC6"/>')
    # bagasjeluke
    if luke_apen:
        d.append('<path d="M24 -20 h56 v-14 l-56 2 Z" fill="#E7E2D6" stroke="#D4CEC0"/>')
        d.append('<rect x="24" y="-20" width="56" height="14" fill="#2B3A42" opacity=".6"/>')
        for i in range(3):
            d.append(f'<rect x="{28+i*17}" y="-17" width="14" height="10" rx="2" fill="#A85434" opacity=".9"/>')
    else:
        d.append('<rect x="24" y="-20" width="56" height="13" rx="2" fill="#F1EDE4" stroke="#D4CEC0"/>')
    # hjul
    for cx in (36, 128):
        d.append(f'<circle cx="{cx}" cy="0" r="11" fill="#2B2B2B"/><circle cx="{cx}" cy="0" r="4.5" fill="#8C8C8C"/>')
    if speil:
        d.append('<path d="M150 -46 l9 -5" stroke="#5B6A72" stroke-width="2.4" fill="none"/>')
    d.append('<rect x="146" y="-14" width="8" height="5" rx="1.6" fill="#F0D79A"/>')
    d.append('</g>')
    return "".join(d)

def fly_737(x, y, s=1.0, dor_x=None):
    """Rutefly sett skrätt fra siden, rod hale. Ingen logo."""
    return (f'<g transform="translate({x},{y}) scale({s})">'
            '<path d="M0 0 q14 -16 54 -18 H168 q26 0 36 9 q-6 9 -30 10 H54 Q14 1 0 0 Z" fill="#F7F5F0" stroke="#CFC8B9" stroke-width="1.2"/>'
            '<path d="M148 -17 q10 -30 20 -30 h8 q-3 18 -4 30 Z" fill="#C0392B"/>'
            '<path d="M150 -17 q8 -22 16 -22" stroke="#A33226" stroke-width="1" fill="none"/>'
            '<path d="M74 -8 q24 20 44 22 h18 q-20 -12 -26 -22 Z" fill="#E2DCCE"/>'
            '<path d="M58 -9 h44 q6 0 4 5 h-52 Z" fill="#D9D2C2"/>'
            '<ellipse cx="78" cy="2" rx="13" ry="8" fill="#5B6A72"/>'
            '<ellipse cx="78" cy="2" rx="9.5" ry="6" fill="#2B3A42"/>'
            + "".join(f'<circle cx="{30+i*11}" cy="-11" r="2.1" fill="#AFC8D6"/>' for i in range(11))
            + '<path d="M196 -8 q10 0 12 4" stroke="#CFC8B9" stroke-width="1" fill="none"/>'
            '<path d="M14 -6 q8 -6 18 -7" stroke="#AFC8D6" stroke-width="3" fill="none" stroke-linecap="round"/>'
            + (f'<rect x="{dor_x}" y="-17" width="9" height="15" rx="3" fill="#2B3A42"/>'
               f'<rect x="{dor_x}" y="-17" width="9" height="15" rx="3" fill="none" stroke="#CFC8B9" stroke-width="1"/>'
               if dor_x is not None else "")
            + '</g>')

def koffert(x, y, s=1.0, c="#A85434"):
    return (f'<g transform="translate({x},{y}) scale({s})">'
            f'<rect x="-9" y="-14" width="18" height="14" rx="2.6" fill="{c}"/>'
            f'<rect x="-9" y="-9" width="18" height="1.6" fill="#00000022"/>'
            f'<path d="M-3 -14 v-5 h6 v5" stroke="#5B6A72" stroke-width="1.6" fill="none"/>'
            f'<circle cx="-5" cy="1" r="1.6" fill="#2B2B2B"/><circle cx="5" cy="1" r="1.6" fill="#2B2B2B"/>'
            f'</g>')

# ---------- scenene ----------

def skolen():
    b = []
    b.append('<rect width="400" height="260" fill="url(#g-sky)"/>')
    b.append('<circle cx="318" cy="56" r="20" fill="#FBEFD4" opacity=".9"/>')
    b.append('<circle cx="318" cy="56" r="34" fill="#FBEFD4" opacity=".28"/>')
    b.append('<path d="M0 150 q60 -10 120 -4 q70 7 140 -6 q80 -14 140 -2 V260 H0 Z" fill="#B9C6B2"/>')
    b.append('<rect y="168" width="400" height="92" fill="#8FA383"/>')
    # skolebygg
    b.append('<g>')
    b.append('<path d="M54 168 V110 l62 -22 l62 22 v58 Z" fill="#E7E0D1" stroke="#CDC4B2"/>')
    b.append('<path d="M48 112 L116 86 L184 112 l-6 7 L116 95 L54 119 Z" fill="#A85434"/>')
    b.append('<rect x="176" y="124" width="104" height="44" fill="#EDE7DA" stroke="#CDC4B2"/>')
    b.append('<rect x="176" y="118" width="104" height="7" fill="#A85434"/>')
    for i in range(4):
        b.append(f'<rect x="{184+i*25}" y="132" width="17" height="22" rx="1.5" fill="#9FBDCD"/>')
    for i in range(3):
        b.append(f'<rect x="{68+i*28}" y="124" width="20" height="22" rx="1.5" fill="#9FBDCD"/>')
    b.append('<rect x="108" y="140" width="17" height="28" rx="1.5" fill="#123A4A"/>')
    b.append('</g>')
    b.append('<line x1="300" y1="168" x2="300" y2="92" stroke="#B6AE9D" stroke-width="2.4"/>')
    b.append('<path d="M301 94 h22 l-6 7 l6 7 h-22 Z" fill="#C0392B"/>')
    b.append(bjork(28, 172, 1.1))
    b.append(bjork(368, 176, 0.95, True))
    b.append(hvit_buss(228, 230, 0.78, dor_apen=True))
    b.append(folk(88, 228, 6, 1.0))
    b.append(koffert(70, 230, 0.9))
    b.append(koffert(176, 232, 0.9, "#123A4A"))
    return _wrap("".join(b))

def bagasjen():
    b = []
    b.append('<rect width="400" height="260" fill="url(#g-sky)"/>')
    b.append('<circle cx="52" cy="44" r="17" fill="#FBEFD4" opacity=".85"/>')
    b.append('<path d="M0 142 q90 -12 200 -6 q110 6 200 -4 V260 H0 Z" fill="#AEBFA9"/>')
    b.append('<rect y="176" width="400" height="84" fill="#857F72"/>')
    b.append('<path d="M0 182 H400" stroke="#9C958899" stroke-width="2"/>')
    b.append(bjork(360, 180, 0.8, True))
    b.append(hvit_buss(96, 236, 1.18, dor_apen=True, luke_apen=True))
    b.append(folk(48, 236, 3, 0.95))
    b.append(folk(276, 240, 3, 1.0))
    b.append(koffert(146, 240, 1.0))
    b.append(koffert(168, 242, 1.0, "#2F6B47"))
    return _wrap("".join(b))

def _buss_interior(utsyn_svg, lys="#E9E2D3"):
    """Innsiden av bussen: seterader, midtgang og vinduer med utsyn.
    Utsynet legges i et nestet <svg> slik at landskapet skaleres til vindusflata."""
    b = []
    b.append(f'<rect width="400" height="260" fill="{lys}"/>')
    # tak og hattehylle
    b.append('<path d="M0 0 H400 V30 q-200 18 -400 0 Z" fill="#D8D1C2"/>')
    b.append('<path d="M0 26 q200 18 400 0 v10 q-200 18 -400 0 Z" fill="#C6BEAD"/>')
    for i in range(5):
        b.append(f'<circle cx="{34+i*84}" cy="20" r="3.4" fill="#F4EFE2"/>')
    # fremre vindu (stort)
    b.append('<g><rect x="18" y="56" width="168" height="98" rx="9" fill="#B6AFA0"/>')
    b.append('<svg x="23" y="61" width="158" height="88" viewBox="0 78 400 136" preserveAspectRatio="xMidYMid slice">'
             + utsyn_svg + '</svg>')
    b.append('<rect x="18" y="56" width="168" height="98" rx="9" fill="none" stroke="#BDB5A4" stroke-width="3"/>')
    b.append('<path d="M30 64 l44 -2 l-48 30 Z" fill="#FFFFFF" opacity=".20"/></g>')
    b.append('<rect x="16" y="49" width="172" height="5" rx="2.5" fill="#C6BEAD"/>')
    # setebrystning foran vinduet (venstre rad, sett bakfra)
    b.append('<path d="M0 260 V150 q22 -8 44 -6 q24 2 24 14 V260 Z" fill="#3B4D5C"/>')
    b.append('<path d="M6 260 V158 q18 -6 34 -4 q18 2 18 12 V260 Z" fill="#4C6274"/>')
    # høyre seterader, avtagende
    b.append('<path d="M212 172 q0 -56 27 -60 h29 q25 4 25 60 Z" fill="#45596A"/>')
    b.append('<path d="M218 172 q2 -50 24 -53 h25 q21 4 21 53 Z" fill="#556C7E"/>')
    b.append('<rect x="216" y="172" width="76" height="12" rx="4" fill="#3A4C5A"/>')
    b.append('<path d="M300 260 q0 -96 44 -102 h56 V260 Z" fill="#3B4D5C"/>')
    b.append('<path d="M309 260 q2 -88 40 -94 h51 V260 Z" fill="#4C6274"/>')
    # gulv og midtgang i perspektiv
    b.append('<path d="M0 260 V214 q100 -12 196 -8 q110 5 204 12 V260 Z" fill="#6E6A60"/>')
    b.append('<path d="M74 260 q56 -38 136 -36 q84 2 132 36 Z" fill="#5A5750"/>')
    for i in range(5):
        y = 224 + i * 8
        b.append(f'<path d="M{96 - i*14} {y} H{300 + i*16}" stroke="#6E6A60" stroke-width="1.6" opacity=".5"/>')
    return _wrap("".join(b))

def _vidde(sno=0.3, fjell="#8C9A86", himmel="url(#g-sky-hi)", vann=True, mark="#7E8C72"):
    b = [f'<rect x="0" y="0" width="400" height="260" fill="{himmel}"/>']
    b.append(f'<path d="M0 104 q60 -20 120 -8 q70 14 140 -10 q80 -20 140 -4 V260 H0 Z" fill="{fjell}" opacity=".55"/>')
    b.append(f'<path d="M0 126 q80 -14 160 2 q90 18 240 -10 V260 H0 Z" fill="{fjell}"/>')
    if vann:
        b.append('<path d="M20 160 q60 -12 130 -2 q50 8 96 0 q-40 22 -120 22 q-80 0 -106 -20 Z" fill="#9FBCCB"/>')
    b.append(f'<rect y="178" width="400" height="82" fill="{mark}"/>')
    n = int(sno * 9)
    for i in range(n):
        b.append(snofonn(22 + i * 44, 150 + (i % 3) * 16, 40, 12))
    for i in range(n):
        b.append(snofonn(10 + i * 50, 206 + (i % 2) * 18, 46, 10))
    return "".join(b)

def i_bussen():
    """Hele gruppa om bord, sett ned midtgangen."""
    return _wrap(buss_inne.buss_innvendig(_vidde(0.2, "#8E9C84", mark="#76855F")))

def masi():
    return _buss_interior(_vidde(0.35, "#8C9A86", mark="#7D8A6C"))


def suolovuopmi():
    return _buss_interior(_vidde(0.75, "#8795A0", mark="#89907A"))

def sennalandet():
    return _buss_interior(_vidde(1.0, "#9AA9B4", vann=False, mark="#9B9E8E"))

def eibydalen():
    b = ['<rect width="400" height="260" fill="url(#g-sky-hi)"/>']
    b.append('<path d="M0 96 q70 -22 150 -6 q80 16 250 -16 V260 H0 Z" fill="#7C8E99" opacity=".6"/>')
    b.append('<path d="M0 140 q110 -30 400 -8 V260 H0 Z" fill="#4E7FA0"/>')   # fjorden
    b.append('<path d="M0 150 q90 -16 190 4 q110 22 210 -2 V260 H0 Z" fill="#5E7A4A"/>')
    for i in range(9):
        b.append(bjork(16 + i * 46, 196 + (i % 3) * 14, 0.8 + (i % 3) * .18, i % 2 == 0))
    return _buss_interior("".join(b))

def alta_lufthavn():
    b = []
    b.append('<rect width="400" height="260" fill="url(#g-sky)"/>')
    b.append('<path d="M0 120 q80 -16 160 -4 q90 14 240 -10 V180 H0 Z" fill="#9DAE98" opacity=".7"/>')
    b.append('<rect y="176" width="400" height="84" fill="#8A8477"/>')
    # terminal
    b.append('<rect x="40" y="118" width="250" height="58" fill="#EFE9DC" stroke="#CDC4B2"/>')
    b.append('<path d="M34 118 H296 l-8 -12 H42 Z" fill="#123A4A"/>')
    b.append('<rect x="40" y="130" width="250" height="30" fill="#A9C3D2"/>')
    for i in range(9):
        b.append(f'<line x1="{46+i*28}" y1="130" x2="{46+i*28}" y2="160" stroke="#EFE9DC" stroke-width="3"/>')
    b.append('<rect x="128" y="160" width="40" height="16" fill="#123A4A"/>')
    b.append('<text x="60" y="113" font-family="Archivo,sans-serif" font-size="13" font-weight="800" fill="#FCFAF6" letter-spacing="3">ALTA</text>')
    # tårn
    b.append('<rect x="306" y="96" width="14" height="80" fill="#E3DCCB" stroke="#CDC4B2"/>')
    b.append('<path d="M298 96 h30 l-5 -16 h-20 Z" fill="#4C6274"/>')
    b.append('<rect x="301" y="82" width="24" height="10" fill="#A9C3D2"/>')
    b.append(hvit_buss(74, 214, 0.72))
    b.append(folk(246, 216, 4, 0.82))
    b.append('<rect x="0" y="186" width="400" height="3" fill="#9C9588"/>')
    return _wrap("".join(b))

def innsjekk():
    b = ['<rect width="400" height="260" fill="url(#g-room)"/>']
    b.append('<rect y="0" width="400" height="26" fill="#D6CFC0"/>')
    for i in range(6):
        b.append(f'<rect x="{18+i*66}" y="8" width="40" height="7" rx="3" fill="#EFEAE0"/>')
    # bakvegg med skjermer
    b.append('<rect x="24" y="44" width="352" height="54" rx="4" fill="#123A4A"/>')
    for i in range(3):
        b.append(f'<rect x="{38+i*116}" y="54" width="96" height="34" rx="2" fill="#17485C"/>')
        b.append(f'<rect x="{44+i*116}" y="60" width="54" height="5" rx="2.5" fill="#E2A02F" opacity=".9"/>')
        for r in range(3):
            b.append(f'<rect x="{44+i*116}" y="{70+r*6}" width="{74-r*13}" height="3" rx="1.5" fill="#9FC4D4" opacity=".75"/>')
    # skranke
    b.append('<path d="M18 176 h364 v30 H18 Z" fill="#E7E0D1" stroke="#CDC4B2"/>')
    b.append('<rect x="18" y="168" width="364" height="10" rx="3" fill="#123A4A"/>')
    for i in range(3):
        x = 40 + i * 118
        b.append(f'<rect x="{x}" y="140" width="76" height="30" rx="3" fill="#D8D1C2"/>')
        b.append(f'<rect x="{x+8}" y="146" width="36" height="18" rx="2" fill="#2B3A42"/>')
        b.append(f'<circle cx="{x+62}" cy="155" r="7" fill="#E8C9A8"/>')
    # bagasjebelte
    b.append('<rect x="18" y="206" width="364" height="14" rx="3" fill="#5B6A72"/>')
    b.append('<rect x="18" y="206" width="364" height="4" fill="#78858C"/>')
    b.append(koffert(70, 206, 1.0))
    b.append(koffert(132, 206, 1.0, "#2F6B47"))
    b.append(koffert(286, 206, 1.0, "#123A4A"))
    b.append('<rect y="226" width="400" height="34" fill="#BDB5A4"/>')
    b.append(folk(44, 250, 5, 1.0))
    b.append(folk(250, 252, 4, 1.02))
    return _wrap("".join(b))

def sikkerhetskontroll():
    b = ['<rect width="400" height="260" fill="url(#g-room)"/>']
    b.append('<rect y="0" width="400" height="24" fill="#D6CFC0"/>')
    b.append('<rect x="20" y="40" width="150" height="26" rx="4" fill="#123A4A"/>')
    b.append('<text x="32" y="58" font-family="Archivo,sans-serif" font-size="12" font-weight="700" fill="#FCFAF6">Sikkerhet</text>')
    # portal
    b.append('<path d="M214 196 V86 q0 -10 12 -10 h78 q12 0 12 10 v110" fill="none" stroke="#C9C1B0" stroke-width="15"/>')
    b.append('<path d="M214 196 V86 q0 -10 12 -10 h78 q12 0 12 10 v110" fill="none" stroke="#E7E0D1" stroke-width="9"/>')
    b.append('<rect x="226" y="88" width="78" height="5" rx="2.5" fill="#2F6B47"/>')
    # røntgen
    b.append('<rect x="24" y="130" width="120" height="58" rx="5" fill="#4C6274"/>')
    b.append('<rect x="34" y="140" width="46" height="30" rx="2" fill="#17485C"/>')
    b.append('<path d="M40 162 l10 -12 l9 9 l8 -14 l9 17 Z" fill="#8FD0B0" opacity=".8"/>')
    b.append('<rect x="92" y="140" width="42" height="30" rx="2" fill="#2B3A42"/>')
    # rullebånd
    b.append('<rect x="10" y="188" width="196" height="12" rx="3" fill="#5B6A72"/>')
    for i in range(9):
        b.append(f'<line x1="{16+i*22}" y1="188" x2="{16+i*22}" y2="200" stroke="#78858C" stroke-width="2.4"/>')
    for i, c in enumerate(["#A85434", "#123A4A", "#96690C"]):
        b.append(f'<rect x="{18+i*58}" y="172" width="46" height="16" rx="3" fill="{c}" opacity=".9"/>')
        b.append(f'<rect x="{24+i*58}" y="176" width="20" height="8" rx="2" fill="#FFFFFF" opacity=".28"/>')
    b.append('<rect y="214" width="400" height="46" fill="#BDB5A4"/>')
    b.append(folk(252, 212, 3, 0.92, bag=False))
    b.append(folk(150, 246, 4, 1.0))
    return _wrap("".join(b))

def ved_gate():
    b = ['<rect width="400" height="260" fill="url(#g-room)"/>']
    b.append('<rect y="0" width="400" height="22" fill="#D6CFC0"/>')
    # stort vindu
    b.append('<rect x="20" y="36" width="360" height="110" rx="4" fill="url(#g-win)"/>')
    b.append('<clipPath id="cg"><rect x="20" y="36" width="360" height="110" rx="4"/></clipPath>')
    b.append('<g clip-path="url(#cg)">')
    b.append('<rect x="20" y="104" width="360" height="42" fill="#8A8477"/>')
    b.append('<rect x="20" y="112" width="360" height="3" fill="#D8D1C2" opacity=".7"/>')
    b.append(fly_737(96, 112, 0.74))
    b.append('</g>')
    for i in range(5):
        b.append(f'<line x1="{20+i*72}" y1="36" x2="{20+i*72}" y2="146" stroke="#E7E0D1" stroke-width="7"/>')
    b.append('<rect x="20" y="36" width="360" height="110" rx="4" fill="none" stroke="#CDC4B2" stroke-width="3"/>')
    # gateskilt
    b.append('<rect x="238" y="158" width="142" height="34" rx="4" fill="#123A4A"/>')
    b.append('<text x="250" y="174" font-family="Archivo,sans-serif" font-size="11" font-weight="700" fill="#E2A02F">DY 321</text>')
    b.append('<text x="250" y="186" font-family="Archivo,sans-serif" font-size="10" fill="#CFE0E8">OSLO · 11:55</text>')
    # benkerad
    b.append('<rect x="18" y="186" width="200" height="10" rx="4" fill="#4C6274"/>')
    for i in range(4):
        b.append(f'<rect x="{26+i*48}" y="162" width="40" height="26" rx="4" fill="#556C7E"/>')
        b.append(f'<rect x="{28+i*48}" y="196" width="4" height="20" fill="#3A4C5A"/>')
        b.append(f'<rect x="{60+i*48}" y="196" width="4" height="20" fill="#3A4C5A"/>')
    b.append('<rect y="216" width="400" height="44" fill="#BDB5A4"/>')
    b.append(folk(44, 248, 4, 0.98))
    b.append(folk(258, 250, 4, 1.02))
    b.append(koffert(220, 250, 0.95, "#A85434"))
    return _wrap("".join(b))

def ombordstigning():
    b = ['<rect width="400" height="260" fill="url(#g-sky)"/>']
    b.append('<circle cx="44" cy="44" r="17" fill="#FBEFD4" opacity=".85"/>')
    b.append('<circle cx="44" cy="44" r="30" fill="#FBEFD4" opacity=".25"/>')
    b.append('<path d="M0 112 q90 -14 190 -4 q100 10 210 -8 V152 H0 Z" fill="#9DAE98" opacity=".55"/>')
    b.append('<rect y="150" width="400" height="110" fill="#8A8477"/>')
    b.append('<rect y="155" width="400" height="4" fill="#A49D8F"/>')
    for i in range(7):
        b.append(f'<rect x="{6+i*58}" y="246" width="36" height="5" rx="2" fill="#C9C1B0" opacity=".6"/>')
    # flyet: nese til venstre, hale til hoyre
    b.append(fly_737(26, 168, 1.42, dor_x=30))
    # trappevogn ved fremre dor
    b.append('<g transform="translate(96,168)">')
    b.append('<path d="M-4 0 h74 v-7 h-66 Z" fill="#B7AFA0"/>')
    for i in range(9):
        b.append(f'<rect x="{2+i*7.4}" y="{-7-i*6.6}" width="14" height="4" rx="1" fill="#DCD5C7" stroke="#B0A896" stroke-width=".6"/>')
    b.append('<path d="M0 -4 L70 -66" stroke="#8E948F" stroke-width="2.6" fill="none"/>')
    b.append('<path d="M12 2 L82 -60" stroke="#8E948F" stroke-width="2.6" fill="none"/>')
    b.append('<circle cx="4" cy="1" r="5.5" fill="#2B2B2B"/><circle cx="62" cy="1" r="5.5" fill="#2B2B2B"/>')
    b.append('</g>')
    # ko paa asfalten og folk i trappa
    b.append(folk(28, 172, 4, 1.0))
    b.append(folk(76, 170, 2, 0.95, bag=False))
    b.append('<g transform="translate(128,120) scale(.84)">'
             '<rect x="-4" y="-18" width="8" height="12" rx="3.2" fill="#2F6B47"/>'
             '<circle cx="0" cy="-22.5" r="3.6" fill="#E8C9A8"/>'
             '<rect x="-3.4" y="-7" width="2.8" height="8" rx="1.1" fill="#2B3A42"/>'
             '<rect x="0.6" y="-7" width="2.8" height="8" rx="1.1" fill="#2B3A42"/></g>')
    b.append('<g transform="translate(146,104) scale(.82)">'
             '<rect x="-4" y="-18" width="8" height="12" rx="3.2" fill="#96690C"/>'
             '<circle cx="0" cy="-22.5" r="3.6" fill="#E8C9A8"/>'
             '<rect x="-3.4" y="-7" width="2.8" height="8" rx="1.1" fill="#2B3A42"/>'
             '<rect x="0.6" y="-7" width="2.8" height="8" rx="1.1" fill="#2B3A42"/></g>')
    return _wrap("".join(b))

SCENER = {
    'skolen': skolen,
    'bagasjen': bagasjen,
    'i-bussen': i_bussen,
    'masi': masi,
    'suolovuopmi': suolovuopmi,
    'eibydalen': eibydalen,
    'alta-lufthavn': alta_lufthavn,
    'innsjekk': innsjekk,
    'sikkerhetskontroll': sikkerhetskontroll,
    'ved-gate': ved_gate,
    'ombordstigning': ombordstigning,
}

def alle():
    return {k: f() for k, f in SCENER.items()}

import re as _re

def _unik(svg, suff):
    """Gjor alle id-er unike, slik at flere scener kan ligge i samme DOM."""
    ids = set(_re.findall(r'id="([A-Za-z][\w-]*)"', svg))
    for i in sorted(ids, key=len, reverse=True):
        svg = svg.replace(f'id="{i}"', f'id="{i}-{suff}"')
        svg = svg.replace(f'url(#{i})', f'url(#{i}-{suff})')
    return svg

def alle_unike():
    return {k: _unik(f(), k) for k, f in SCENER.items()}
