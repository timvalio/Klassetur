# -*- coding: utf-8 -*-
"""Innsiden av bussen sett ned midtgangen, med gruppa om bord.

21 elever og 7 voksne. Radene tegnes i perspektiv fra naermest til fjernest,
slik at folk lenger bak blir mindre og delvis skjult av setene foran.
"""
import random

HAR  = ['#2B2118', '#4A3524', '#6B4A2A', '#8A5A2B', '#1F1A16', '#C08A3E', '#3A2A1E', '#5A4030']
HETTE= ['#A85434', '#2F6B47', '#123A4A', '#96690C', '#8E3F22', '#4C6274', '#7C746A', '#B5762F']
HUD  = ['#E8C9A8', '#DFBB97', '#C99A72', '#EBD3B6', '#D4A980']


def _hode(x, y, s, rng, voksen=False, vendt=0):
    """Hode med haar, sett bakfra/skraatt. vendt: -1 venstre, 0 bak, 1 hoyre."""
    hud = rng.choice(HUD)
    har = rng.choice(HAR)
    g = [f'<g transform="translate({x:.1f},{y:.1f}) scale({s:.3f})">']
    g.append(f'<ellipse cx="0" cy="0" rx="9.5" ry="10.5" fill="{hud}"/>')
    # haar: bakhodet dekker mest naar man ser bakfra
    if rng.random() < .35 and not voksen:          # hestehale eller lang
        g.append(f'<path d="M-9.5 -1 q0 -12 9.5 -12 q9.5 0 9.5 12 q0 9 -3 13 h-13 q-3 -4 -3 -13 Z" fill="{har}"/>')
        g.append(f'<ellipse cx="{4*vendt if vendt else 0}" cy="13" rx="4" ry="7" fill="{har}"/>')
    else:
        g.append(f'<path d="M-9.5 -1 q0 -12 9.5 -12 q9.5 0 9.5 12 q0 5 -2 7 h-15 q-2 -2 -2 -7 Z" fill="{har}"/>')
    if vendt:                                       # litt profil: oere og kinn
        g.append(f'<ellipse cx="{8.2*vendt}" cy="1.5" rx="2" ry="2.8" fill="{hud}"/>')
    if rng.random() < .22:                          # hodetelefoner
        g.append('<path d="M-10.5 0 q0 -13 10.5 -13 q10.5 0 10.5 13" stroke="#1B1B1B" stroke-width="2.4" fill="none"/>')
        g.append('<rect x="-13" y="-2" width="5" height="8" rx="2.2" fill="#1B1B1B"/>')
        g.append('<rect x="8" y="-2" width="5" height="8" rx="2.2" fill="#1B1B1B"/>')
    if voksen and rng.random() < .5:                # lue
        g.append('<path d="M-10 -2 q0 -11 10 -11 q10 0 10 11 Z" fill="#123A4A"/>')
        g.append('<rect x="-10.5" y="-3" width="21" height="3.4" rx="1.6" fill="#0A2531"/>')
    g.append('</g>')
    return ''.join(g)


def _skulder(x, y, s, rng):
    c = rng.choice(HETTE)
    return (f'<path d="M{x-14*s:.1f} {y+16*s:.1f} q{3*s:.1f} {-10*s:.1f} {14*s:.1f} {-11*s:.1f} '
            f'q{11*s:.1f} {1*s:.1f} {14*s:.1f} {11*s:.1f} Z" fill="{c}"/>')


def _mobil(x, y, s, rng):
    return (f'<g transform="translate({x:.1f},{y:.1f}) scale({s:.3f})">'
            f'<rect x="-3.4" y="-6" width="6.8" height="11" rx="1.6" fill="#1B1B1B"/>'
            f'<rect x="-2.6" y="-5.2" width="5.2" height="9.4" rx="1" fill="#9FC4D4"/></g>')


def buss_innvendig(utsyn_svg, frø=7):
    rng = random.Random(frø)
    b = []
    VP_X, VP_Y = 200, 86
    RADER = 6

    def sk(i):
        return 1.26 / (1 + i * 0.47)

    b.append('<rect width="400" height="260" fill="#CFC6B4"/>')

    # ---- bakvegg: bakrute og bakerste benk
    sb = sk(RADER - 1) * 0.86
    bw = (74 + 150 * sb)
    b.append(f'<rect x="{VP_X-bw:.1f}" y="{VP_Y-18*sb:.1f}" width="{2*bw:.1f}" height="{150*sb:.1f}" fill="#B9AF9B"/>')
    rw, rh = 1.25 * bw, 40 * sb
    b.append(f'<rect x="{VP_X-rw/2:.1f}" y="{VP_Y+4*sb:.1f}" width="{rw:.1f}" height="{rh:.1f}" rx="{4*sb:.1f}" fill="#9E947F"/>')
    b.append(f'<clipPath id="bakrute"><rect x="{VP_X-rw/2+2:.1f}" y="{VP_Y+4*sb+2:.1f}" width="{rw-4:.1f}" height="{rh-4:.1f}" rx="{3*sb:.1f}"/></clipPath>')
    b.append(f'<g clip-path="url(#bakrute)"><svg x="{VP_X-rw/2:.1f}" y="{VP_Y+4*sb:.1f}" width="{rw:.1f}" height="{rh:.1f}" '
             f'viewBox="0 96 400 110" preserveAspectRatio="xMidYMid slice">{utsyn_svg}</svg></g>')

    # ---- vinduer langs sidene, mellom hattehylle og seterygg
    for side in (-1, 1):
        for i in range(RADER - 1):
            s0, s1 = sk(i), sk(i + 1)
            x0 = VP_X + side * (74 + 150 * s0); x1 = VP_X + side * (74 + 150 * s1)
            t0, n0 = VP_Y + 4 * s0, VP_Y + 46 * s0
            t1, n1 = VP_Y + 4 * s1, VP_Y + 46 * s1
            b.append(f'<path d="M{x0:.1f} {t0:.1f} L{x1:.1f} {t1:.1f} L{x1:.1f} {n1:.1f} L{x0:.1f} {n0:.1f} Z" fill="#A79D88"/>')
            idd = f'vc{"v" if side<0 else "h"}{i}'
            b.append(f'<clipPath id="{idd}"><path d="M{x0 - side*2:.1f} {t0+3:.1f} L{x1 + side*2:.1f} {t1+2:.1f} '
                     f'L{x1 + side*2:.1f} {n1-2:.1f} L{x0 - side*2:.1f} {n0-3:.1f} Z"/></clipPath>')
            xa, xb = min(x0, x1), max(x0, x1)
            b.append(f'<g clip-path="url(#{idd})"><svg x="{xa:.1f}" y="{min(t0,t1)-2:.1f}" width="{max(xb-xa,6):.1f}" '
                     f'height="{max(n0-t0,6):.1f}" viewBox="0 96 400 110" preserveAspectRatio="xMidYMid slice">{utsyn_svg}</svg></g>')
            b.append(f'<path d="M{x1:.1f} {t1:.1f} L{x1:.1f} {n1:.1f}" stroke="#B5AB96" stroke-width="{2.4*s1:.1f}"/>')

    # ---- hattehylle og tak
    for side in (-1, 1):
        pts = []
        for i in range(RADER):
            s0 = sk(i)
            pts.append((VP_X + side * (74 + 150 * s0), VP_Y - 20 * s0))
        for i in range(RADER - 1, -1, -1):
            s0 = sk(i)
            pts.append((VP_X + side * (74 + 150 * s0), VP_Y + 2 * s0))
        d = 'M' + ' L'.join(f'{x:.1f} {y:.1f}' for x, y in pts) + ' Z'
        b.append(f'<path d="{d}" fill="#C2B9A4"/>')
        # bagasje oppe
        for i in range(RADER - 1):
            if rng.random() < .62:
                s0 = sk(i)
                w, h = 46 * s0, 15 * s0
                b.append(f'<rect x="{VP_X + side*(74+150*s0) - w/2:.1f}" y="{VP_Y-18*s0:.1f}" width="{w:.1f}" '
                         f'height="{h:.1f}" rx="{3*s0:.1f}" fill="{rng.choice(HETTE)}" opacity=".92"/>')
    s0 = sk(0)
    b.append(f'<path d="M0 0 H400 V{VP_Y-56*s0:.0f} L{VP_X+74+150*sb:.1f} {VP_Y-20*sb:.1f} '
             f'H{VP_X-74-150*sb:.1f} L0 {VP_Y-56*s0:.0f} Z" fill="#DED6C6"/>')
    for i in range(RADER - 1):
        s1 = sk(i)
        for side in (-1, 1):
            b.append(f'<circle cx="{VP_X + side*(40+96*s1):.1f}" cy="{VP_Y-34*s1:.1f}" r="{2.6*s1:.1f}" fill="#F7F2E6"/>')

    # ---- gulv og midtgang
    b.append(f'<path d="M0 260 L{VP_X-30*sb:.1f} {VP_Y+120*sb:.1f} H{VP_X+30*sb:.1f} L400 260 Z" fill="#5A5750"/>')
    b.append(f'<path d="M58 260 L{VP_X-20*sb:.1f} {VP_Y+122*sb:.1f} H{VP_X+20*sb:.1f} L342 260 Z" fill="#6B675D"/>')

    # ---- seterader, bakerst foerst
    for i in range(RADER - 1, -1, -1):
        s = sk(i)
        y = VP_Y + 118 * s
        h = 70 * s
        for side in (-1, 1):
            cx = VP_X + side * (60 + 64 * s)
            bre = 118 * s
            for k in (-1, 1):
                px = cx + k * bre * 0.25
                voksen = (i >= 4) or (i == 2 and side * k > 0)
                if rng.random() < 0.06 and i > 0:
                    continue
                b.append(_skulder(px, y - h * 0.60, s, rng))
                b.append(_hode(px, y - h * 0.82, s, rng, voksen, vendt=rng.choice([-1, 0, 0, 1])))
                if rng.random() < 0.28:
                    b.append(_mobil(px + 12 * s * side, y - h * 0.46, s, rng))
            b.append(f'<path d="M{cx-bre/2:.1f} {y:.1f} q0 {-h*0.60:.1f} {bre*0.18:.1f} {-h*0.64:.1f} '
                     f'h{bre*0.64:.1f} q{bre*0.18:.1f} {h*0.04:.1f} {bre*0.18:.1f} {h*0.64:.1f} Z" fill="#45596A"/>')
            b.append(f'<path d="M{cx-bre/2+3*s:.1f} {y:.1f} q0 {-h*0.54:.1f} {bre*0.17:.1f} {-h*0.58:.1f} '
                     f'h{bre*0.58:.1f} q{bre*0.17:.1f} {h*0.04:.1f} {bre*0.17:.1f} {h*0.58:.1f} Z" fill="#55697C"/>')
            b.append(f'<line x1="{cx:.1f}" y1="{y-h*0.56:.1f}" x2="{cx:.1f}" y2="{y:.1f}" stroke="#3B4D5C" stroke-width="{1.6*s:.1f}"/>')
            b.append(f'<rect x="{cx-bre/2:.1f}" y="{y:.1f}" width="{bre:.1f}" height="{9*s:.1f}" rx="{3*s:.1f}" fill="#3A4C5A"/>')

        # en elev staar i midtgangen ved rad 2
        if i == 2:
            ss = s * 1.15
            gx, gy = VP_X + 8, y - h * 0.10
            b.append(f'<g transform="translate({gx:.1f},{gy:.1f})">')
            b.append(f'<path d="M{-13*ss:.1f} 0 q{1.5*ss:.1f} {-30*ss:.1f} {13*ss:.1f} {-31*ss:.1f} '
                     f'q{11.5*ss:.1f} {1*ss:.1f} {13*ss:.1f} {31*ss:.1f} Z" fill="{rng.choice(HETTE)}"/>')
            b.append(_hode(0, -40 * ss, ss, rng, False, vendt=-1))
            b.append('</g>')
    return ''.join(b)
