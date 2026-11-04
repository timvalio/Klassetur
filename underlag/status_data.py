# -*- coding: utf-8 -*-
"""status_data.py — hvem som er spurt om pris på 10B-turen, og hva de har svart.

Én post per mottaker. Oppdater «status», «tekst» og «oppdatert» når det kommer svar;
lag_kart.py legger dette inn i kartsiden, og template.html tegner boksen og merkene.

status:  tilbud  — pris mottatt
         oss     — de har svart, men venter på noe fra oss
         venter  — forespørsel sendt, ikke besvart
         klar    — ferdig utfylt, men ikke sendt
         nei     — svart nei, eller ikke aktuelt

maal:    liste med reisemål-id-er ('kreta', 'costablanca', 'split'), eller
         variant-id-er ('costablanca-best') når det bare gjelder den ene varianten.
         Tom liste = gjelder alle tre.
"""

OPPDATERT = '14. oktober 2026'

LEDE = ('Costa Brava er valgt, og de andre reisemålene er tatt ut. Flyet er det eneste noen leverandør har gitt pris på: Norwegians gruppetilbud ZJIHGF av 14. oktober, som sto i sju dager og nå er utløpt. Overnattingene er slått opp på booking.com for hele gruppa på 28 i ett søk, men ingen av hotellene har gitt gruppepris. Apollo, Ving og GHT Hotels er spurt om Costa Brava og har ikke svart.')

POSTER = [
    # --- fly og pakker
    dict(hvem='Norwegian gruppeavdeling', hva='Fly Alta–Oslo–Barcelona tur/retur',
         maal=['costabrava'], status='tilbud', dato='14. okt', pp=6145,
         tekst='Tilbud ZJIHGF: 157 304 pluss skatter og avgifter 14 756 = 172 060 kroner for 28, altså 6 145 per person '
               'med 2 × 23 kg koffert. DY 321 Alta–Oslo og D8 5523 Oslo–Barcelona ut tirsdag 8. juni, DY 1741 og DY 328 '
               'hjem tirsdag 15. juni. Står i sju dager, til rundt 21. oktober. Det er 25 424 kroner mer enn anslaget — '
               'påslaget over nettpris ble 608 kroner per flyetappe, ikke 381 som målt i september.'),

    dict(hvem='Apollo', hva='Kreta med direktefly, og pris på Costa Brava',
         maal=['costabrava'], status='oss', dato='purret 9. okt',
         tekst='Bedt om fornyet gruppepris på begge avgangene: Alta 8.–15. juni (A3 4559/4558) og Tromsø 5.–12. juni '
               '(SK 7355/7356), Galeana Beach med frokost, koffert og transfer, og «den 21. gratis» regnet inn. '
               'Tilbudet fra 21. og 25. september sto til Galeana Beach fra 13 739 per person fra Alta og 12 305 fra Tromsø. '
               'Saksnummer DTN:08490001588. Utfluktsprisene de skyldte oss er etterspurt på nytt. '
               'Elisabeth Holmsen purret 9. oktober og spør om vi har bestemt oss eller valgt en annen reise — hun venter på svar fra oss. '
               'Samme svar kan spørre om de selger Costa Brava, og be om utfluktsprisene de trengte mer tid på.'),

    dict(hvem='Ving gruppeavdeling', hva='To charteralternativer, og et forslag på Costa Brava',
         maal=['costabrava'], status='venter', dato='sendt 12. okt',
         tekst='Bedt om fornyede priser på BO4FXR5 (Oslo–Chania 10.–18. juni, Ilion Beach i Gerani) og '
               'B1M3CUA (Oslo–Split 11.–18. juni, Waterman Supetrus på Brač). Reiseforslagene fra 21. september '
               'lød på 226 779 og 238 750 for 28, begge uten måltider og uten reserverte plasser. '
               'Ving har egne hoteller i Lloret de Mar, så de er også bedt om et tredje forslag på Costa Brava — '
               'ett rimelig og ett med halvpensjon.'),

    dict(hvem='Peer Gynt Tours', hva='Pris på alle tre reisemål',
         maal=[], status='venter', dato='svart 16. sep',
         tekst='De fikk svar allerede 16. september: inntil 15 000 kroner per person for hele turen, base ved stranda '
               'med gangavstand til butikker, elevene på tremannsrom og de voksne på dobbelt- og tremannsrom, frokost '
               'som minimum. Datoene er ikke låst — lørdag til lørdag, for eksempel 5.–12. juni, går også fint. '
               'Siden har det vært stille. Trenger en purring, ikke et nytt svar.'),

    dict(hvem='Travelmate', hva='Pris på alle tre reisemål',
         maal=[], status='nei', dato='svarte 16. sep',
         tekst='Finner ikke noe billigere: Norwegian holder allerede gruppen til Alicante, '
               'ingen god rute til Split, og over 8 000 kroner til Kreta fra Alta. '
               'Svaret gjaldt Costa Blanca, som siden er byttet ut med Costa Brava.'),

    # --- hotell
    dict(hvem='SANTA SUSANNA Chic! Apartments by ALEGRIA', hva='7 netter for 28',
         maal=['costabrava-billigst'], status='venter', dato='sendt 12. okt',
         tekst='Leiligheter med kjøkken, selvhushold, 8.–15. juni. Booking.com priser hele gruppa på 28 i ett søk: '
               '80 855 for uka 14. oktober, 2 888 per person, fordelt på seks leiligheter. Raten var ikke merket '
               'med fri avbestilling, så vi ber om gruppepris og om leilighetene kan holdes på opsjon.'),

    dict(hvem='AQUA Hotel Onabrava & Spa, Santa Susanna', hva='7 netter med halvpensjon for 28',
         maal=['costabrava-best'], status='venter', dato='sendt 12. okt',
         tekst='Firemannsrom til elevene og dobbeltrom til de voksne, frokost og middag, 8.–15. juni. '
               'Booking.com priser hele gruppa i ett søk: 131 334 for uka med halvpensjon 14. oktober '
               '(4 691 per person) og 110 365 med bare frokost, med fri avbestilling og ingen forskuddsbetaling. '
               '9,0 av 10 i omtale. +34 93 767 83 70, onabrava@aquahotel.com.'),

    dict(hvem='GHT Hotels, Costa Brava', hva='7 netter for 28, kjeden med gruppeavdeling',
         maal=['costabrava'], status='venter', dato='sendt 12. okt',
         tekst='Kjede med hoteller i Calella, Lloret de Mar og Tossa de Mar, og egen gruppeavdeling for '
               'bestillinger over 20 rom. Spurt om pris både med frokost og med halvpensjon, og om hvilke av '
               'hotellene som tar imot skolegrupper på dette alderstrinnet. GHT Marítim i Calella lå på '
               '60 504 for 16 personer med halvpensjon da det ble slått opp 26. september. '
               'grups@ghthotels.com, +34 93 766 20 72.'),

    dict(hvem='Moventis Experience / From2 Travel', hva='Buss Barcelona lufthavn–Santa Susanna',
         maal=['costabrava'], status='venter', dato='sendt 12. okt',
         tekst='Bedt om pris på privat buss for 28 begge veier, og om den delte bussen går sent nok til '
               'landing 22:55. Publisert pris for delt buss er 18 euro per person hver vei.'),
]

# Sjekket, men ikke aktuelle — vises som én linje under lista.
FORKASTET = ('Sjekket og lagt bort: Klasseturer.no kjører bare Norge, Polen og Tyskland. '
             'Ingen finsk operatør flyr charter fra Kittilä om sommeren. '
             'Ticket har ingen e-post til gruppeavdelingen.')

MERKE = {'tilbud': 'Tilbud mottatt', 'oss': 'Venter på oss', 'venter': 'Venter svar',
         'klar': 'Klar til å sendes', 'nei': 'Ikke aktuelt'}
# Rekkefølge i lista: det vi må gjøre noe med først.
RANG = {'oss': 0, 'tilbud': 1, 'klar': 2, 'venter': 3, 'nei': 4}
# Merket på reisemålskortet skal vise det beste resultatet, ikke gjøremålet.
RANG_MERKE = {'tilbud': 0, 'klar': 1, 'venter': 2, 'oss': 3, 'nei': 4}


def bygg(par_ider):
    """Returnerer {'oppdatert','lede','forkastet','poster':[...],'merke':{...},'per':{par-id: status}}."""
    poster = sorted(POSTER, key=lambda p: (RANG[p['status']], p['hvem']))
    per = {}
    for p in poster:
        for m in (p['maal'] or list(par_ider)):
            par = m.split('-')[0]
            if RANG_MERKE[p['status']] < RANG_MERKE.get(per.get(par), 9):
                per[par] = p['status']
    return {'oppdatert': OPPDATERT, 'lede': LEDE, 'forkastet': FORKASTET,
            'merke': MERKE, 'poster': poster, 'per': per}
