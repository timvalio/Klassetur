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

OPPDATERT = '16. september 2026'

LEDE = ('Vi har spurt flybolag, reisebyrå og hotell om pris på de tre reisemålene. '
        'Her står hvem som har svart, og hvem vi fortsatt venter på.')

POSTER = [
    # --- fly og pakker
    dict(hvem='Norwegian gruppeavdeling', hva='Fly Alta–Oslo–Alicante tur/retur',
         maal=['costablanca'], status='tilbud', dato='15. sep', pp=4971,
         tekst='Tilbud X2ETUP: 139 188 kroner for alle 28, skatter og innsjekket koffert inkludert. '
               'Tilbudet står til rundt 20. september.'),

    dict(hvem='TUI, via Eli Ristin', hva='Ferdig pakke fra Tromsø, all inclusive',
         maal=['kreta'], status='tilbud', dato='15. sep', pp=21200,
         tekst='470 925 kroner for 28 på Blue Star Caldera Creta Paradise i Gerani, med mat på flyet, '
               'bagasje og transfer. Avreise fra Tromsø, så buss dit kommer i tillegg.'),

    dict(hvem='Norwegian gruppeavdeling', hva='Fly til Chania og Split, via Oslo',
         maal=['kreta', 'split'], status='klar', dato='klar 16. sep',
         tekst='Tre forespørsler ligger ferdig utfylt: Alta–Oslo tur/retur, Oslo–Chania tur/retur '
               'og Oslo–Split tur/retur.'),

    dict(hvem='Apollo', hva='Direktefly Alta–Chania med hotell',
         maal=['kreta'], status='klar', dato='klar 15. sep',
         tekst='Skjemaet er ferdig utfylt. Gruppeavdelingen tar bare telefon, så det må ringes inn.'),

    dict(hvem='Peer Gynt Tours', hva='Pris på alle tre reisemål',
         maal=[], status='venter', dato='sendt 16. sep',
         tekst='Bare fly, overnatting og transfer, så prisene kan sammenlignes.'),

    dict(hvem='Ving gruppeavdeling', hva='Pris på alle tre reisemål',
         maal=[], status='oss', dato='svarte 16. sep',
         tekst='Ving har ingen charter fra Alta og må hente pris på rutefly for hver dato og hvert reisemål. '
               'De spør om vi kan flytte på datoene, hva turen får koste, og hvem andre vi har spurt. Svar er på vei.'),

    dict(hvem='Travelmate', hva='Pris på alle tre reisemål',
         maal=[], status='nei', dato='svarte 16. sep',
         tekst='Finner ikke noe billigere: Norwegian holder allerede gruppen til Alicante, '
               'ingen god rute til Split, og over 8 000 kroner til Kreta fra Alta.'),

    # --- hotell
    dict(hvem='Olympic Palladium, Rethymno', hva='7 netter for 28',
         maal=['kreta-billigst'], status='venter', dato='sendt 16. sep', tekst=''),

    dict(hvem='Albir Garden Resort', hva='7 netter for 28',
         maal=['costablanca-billigst'], status='venter', dato='sendt 16. sep', tekst=''),

    dict(hvem='Albir Playa Hotel & Spa', hva='7 netter for 28',
         maal=['costablanca-best'], status='nei', dato='svarte 16. sep',
         tekst='Hotellet tar ikke imot skolegrupper. Vi trenger et annet hotell til denne varianten.'),

    dict(hvem='Hotel San Antonio, Podstrana', hva='7 netter for 28',
         maal=['split-best'], status='venter', dato='sendt 16. sep', tekst=''),

    dict(hvem='Design Hostel One, Split', hva='7 netter for 28',
         maal=['split-billigst'], status='venter', dato='sendt 16. sep', tekst=''),

    dict(hvem='Quality Airport Hotel Gardermoen', hva='Natten i Oslo på veien ned',
         maal=['kreta', 'split'], status='venter', dato='sendt 16. sep', tekst=''),
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
