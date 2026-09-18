# -*- coding: utf-8 -*-
"""betaling_data.py — når hver kostnadspost forfaller, til boksen «Når må pengene være der».

Hver rad i kostnadstabellen på turarket knyttes til ett eller flere forfallstidspunkt.
lag_kart.py summerer beløpene per tidspunkt og regner om til kroner per reisende.

Endres et vilkår hos en leverandør, rettes det her — beløpene henter seg selv fra arkene.
"""

# Tidspunktene, i rekkefølge. tekst = når, under = hva som utløser det.
TRINN = [
    ('okt26',     'Oktober 2026',        'Tre uker etter at gruppetilbudet på flyet bekreftes. Dette er bindende — Norwegian har ingen fri avbestilling etterpå.'),
    ('mar27',     'Mars 2027',           'Nitti dager før avreise. Depositumet til hotellet er ikke refunderbart.'),
    ('mai27',     'Mai 2027',            'Resten av fly og hotell, to til fire uker før avreise.'),
    ('jun27',     'Ved avreise',         'Betales på stedet, ved innsjekk eller ankomst.'),
    ('underveis', 'Underveis på turen',  'Mat, inngangsbilletter og lokalbusser. Dette betaler hver enkelt selv, det går ikke over klassekassa.'),
    ('etter',     'Etter turen',         'Bussen til og fra Alta faktureres i etterkant.'),
    ('ukjent',    'Ikke avklart ennå',   'Leverandøren har ikke oppgitt betalingsplan.'),
]

# post i kostnadstabellen -> [(andel, trinn, forklaring)]
POST = {
    'Fly, 28 personer t/r':
        [(0.30, 'okt26', 'Depositum på flyet, 30 prosent'),
         (0.70, 'mai27', 'Resten av flyet, 30 dager før avreise')],
    'Fly, 28 personer t/r, gruppetilbud':
        [(0.30, 'okt26', 'Depositum på flyet, 30 prosent'),
         (0.70, 'mai27', 'Resten av flyet, 30 dager før avreise')],
    'Hotell i Rethymno, 7 netter med frokost':
        [(0.30, 'mar27', 'Depositum til Olympic Palladium, 30 prosent'),
         (0.70, 'mai27', 'Resten av hotellet, 14 dager før ankomst')],
    'Hostel i Split, 7 netter':
        [(0.30, 'okt26', 'Depositum til Design Hostel One, 30 prosent ved bekreftelse'),
         (0.70, 'mai27', 'Resten av hostellet, 15 dager før ankomst')],
    'Leiligheter i Albir, 7 netter':      [(1.0, 'jun27', 'Leilighetene, betales ved ankomst')],
    'Hotell med halvpensjon, 7 netter':   [(1.0, 'jun27', 'Hotellet, betales ved ankomst')],
    'Hotell i Podstrana, 7 netter med frokost': [(1.0, 'jun27', 'Hotellet, betales ved ankomst')],
    'Hotell ved Gardermoen, 1 natt':      [(1.0, 'jun27', 'Natten i Oslo, betales ved ankomst')],
    'Hotell ved Gardermoen, 1 natt med frokost': [(1.0, 'jun27', 'Natten i Oslo, betales ved ankomst')],
    'Direktefly Alta–Chania og hotell, 7 netter med frokost':
        [(1.0, 'ukjent', 'Apollo-pakken med fly og hotell — betalingsplan ikke oppgitt')],
    'Koffert og transfer':                [(1.0, 'ukjent', 'Tillegg hos Apollo — betalingsplan ikke oppgitt')],
    'Reiseforsikring for gruppen':        [(1.0, 'jun27', 'Reiseforsikring — tilbud ikke innhentet ennå')],
    'Buss Kautokeino–Alta t/r':           [(1.0, 'etter', 'Buss til og fra Alta')],
    'Middag ute og lunsj':                [(1.0, 'underveis', 'Mat')],
    'Mat, delvis laget selv':             [(1.0, 'underveis', 'Mat')],
    'Mat, enkel':                         [(1.0, 'underveis', 'Mat')],
    'Lunsj og mat underveis':             [(1.0, 'underveis', 'Lunsj — frokost og middag er med i hotellet')],
    'Aktiviteter og lokalbusser':         [(1.0, 'underveis', 'Utflukter og lokalbusser')],
    'Aktiviteter og transport':           [(1.0, 'underveis', 'Utflukter og transport')],
    'Aktiviteter og lokaltransport':      [(1.0, 'underveis', 'Utflukter og lokaltransport')],
    'Aktiviteter med leiebuss':           [(1.0, 'underveis', 'Utflukter med leiebuss')],
}

BUNN = ('Alle beløp er for hele gruppen. Datoene bygger på at gruppetilbudet på flyet bekreftes i løpet av september 2026 og at turen går '
        '7.–15. juni 2027. Fram til depositumet er betalt kan alt avbestilles fritt.')
