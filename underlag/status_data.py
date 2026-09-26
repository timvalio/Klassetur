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

OPPDATERT = '22. september 2026'

LEDE = ('Vi har spurt flybolag, reisebyrå og hotell om pris på de tre reisemålene. '
        'Her står hvem som har svart, og hvem vi fortsatt venter på.')

POSTER = [
    # --- fly og pakker
    dict(hvem='Norwegian gruppeavdeling', hva='Fly Alta–Oslo–Barcelona tur/retur',
         maal=['costabrava'], status='klar', dato='ikke sendt',
         tekst='Costa Brava er det eneste reisemålet uten noe flytilbud. Forespørselen gjelder DY 321 Alta–Oslo og '
               'D8 5523 Oslo–Barcelona ut tirsdag 8. juni, DY 1741 og DY 328 hjem tirsdag 15. juni. '
               'Fram til svaret kommer står flyprisen som billigste oppslag 26. september pluss 381 kroner per flyetappe — '
               'påslaget som er målt mot Norwegians tre gruppetilbud i september.'),

    dict(hvem='Norwegian gruppeavdeling', hva='Fly Oslo–Chania tur/retur',
         maal=['kreta'], status='tilbud', dato='17. sep', pp=4800,
         tekst='Tilbud XV5CP6: 134 400 kroner for 28 med skatter, på DY 1898 ut 8. juni og DY 1899 hjem 15. juni. '
               'Står i fem dager, altså til rundt 22. september.'),

    dict(hvem='Norwegian gruppeavdeling', hva='Fly Oslo–Split tur/retur',
         maal=['split'], status='tilbud', dato='17. sep', pp=2600,
         tekst='Tilbud XV8K8J: 72 800 kroner for 28 med skatter, på DY 1950 ut 8. juni og DY 1951 hjem 15. juni. '
               'Står i fem dager, altså til rundt 22. september.'),

    dict(hvem='Norwegian gruppeavdeling', hva='Fly Alta–Oslo tur/retur',
         maal=['kreta', 'split'], status='venter', dato='sendt 16. sep',
         tekst='Den siste biten som mangler før Kreta og Split kan regnes ferdig. Ut mandag 7. juni, hjem tirsdag 15. juni.'),

    dict(hvem='Apollo', hva='Direktefly Alta–Chania med hotell',
         maal=['kreta'], status='tilbud', dato='21. sep',
         tekst='Gruppetilbud for 28 på avreise 8. juni: Aegean A3 4559/4558 Alta–Chania tur/retur, sju netter med frokost, '
               '23 kg bagasje og transfer. Galeana Beach fra 13 739 per person i delt dobbeltrom, Ariadne Rethymnon fra 14 784. '
               'Én fri reiseleder fra 20 fullt betalende. Ingen plasser reservert; må bestilles senest 90 dager før avreise. '
               'Apollo trenger mer tid på priser for spesialbestilte utflukter. De har flere rom på lørdagsavgangen '
               'fra Tromsø 5. juni enn på tirsdagsavgangen fra Alta, og er 22. september bedt om pris også på den.'),

    dict(hvem='Peer Gynt Tours', hva='Pris på alle tre reisemål',
         maal=[], status='oss', dato='svarte 16. sep',
         tekst='De ser på mulighetene, men trenger å vite hva turen får koste og om vi vil bo i sentrum '
               'eller heller ved stranda. Svar er på vei.'),

    dict(hvem='Ving gruppeavdeling', hva='To charteralternativer fra Oslo',
         maal=['kreta-charter', 'brac-charter'], status='tilbud', dato='21. sep',
         tekst='Reiseforslag BO4FXR5: Sunclass Oslo–Chania 10.–18. juni og 7 netter i leilighet på Ilion Beach i Gerani, '
               '226 779 for 28. Reiseforslag B1M3CUA: Norwegian Oslo–Split 11.–18. juni og 7 netter på Waterman Supetrus '
               'i Supetar på Brač, 238 750 for 28. Begge uten måltider; frokost koster 945 og 1 240 per person. '
               'Ving flyr bare fra Oslo og selger ikke tilslutningsbilletter, så buss, Alta–Oslo og natt ved Gardermoen kommer i tillegg. '
               'Ingen plasser er reservert.'),

    dict(hvem='Travelmate', hva='Pris på alle tre reisemål',
         maal=[], status='nei', dato='svarte 16. sep',
         tekst='Finner ikke noe billigere: Norwegian holder allerede gruppen til Alicante, '
               'ingen god rute til Split, og over 8 000 kroner til Kreta fra Alta. '
               'Svaret gjaldt Costa Blanca, som siden er byttet ut med Costa Brava.'),

    # --- hotell
    dict(hvem='Olympic Palladium, Rethymno', hva='7 netter med frokost',
         maal=['kreta-billigst'], status='tilbud', dato='17. sep', pp=2820,
         tekst='HotelBrain har gitt gruppepris: 8 tremannsrom à 105 euro og 2 dobbeltrom à 78 euro per natt '
               'med frokost, pluss klimaskatt 5 euro per rom per natt. Til sammen 78 900 kroner for hele uka. '
               'Halvpensjon koster 16 euro ekstra per person per dag. Rommene er ikke holdt av ennå.'),

    dict(hvem='SANTA SUSANNA Chic! Apartments by ALEGRIA', hva='7 netter for 28',
         maal=['costabrava-billigst'], status='klar', dato='ikke sendt', pp=3057,
         tekst='Slått opp på booking.com 26. september for 8.–15. juni 2027: 48 907 kroner for 16 personer, '
               '3 057 per person, fri avbestilling. Booking.com priser bare 16 om gangen, så de siste tolv må bekreftes direkte.'),

    dict(hvem='AQUA Hotel Onabrava & Spa, Santa Susanna', hva='7 netter med halvpensjon for 28',
         maal=['costabrava-best'], status='klar', dato='ikke sendt', pp=4670,
         tekst='Slått opp på booking.com 26. september for 8.–15. juni 2027: 74 724 kroner for 16 personer, '
               '4 670 per person med frokost og middag, fri avbestilling og ingen forskuddsbetaling. '
               '9,0 av 10 i omtale. Hele gruppa må bekreftes direkte med hotellet: +34 93 767 83 70, onabrava@aquahotel.com.'),

    dict(hvem='Moventis Experience / From2 Travel', hva='Buss Barcelona lufthavn–Santa Susanna',
         maal=['costabrava'], status='klar', dato='ikke sendt',
         tekst='Publisert pris for delt buss er 18 euro per person hver vei, satt av ved overnattingsstedet. '
               'Pris på privat buss for 28 bør hentes inn, og det må bekreftes at siste avgang passer med landing 22:55.'),

    dict(hvem='Hotel San Antonio, Podstrana', hva='7 netter for 28',
         maal=['split-best'], status='nei', dato='svarte 18. sep',
         tekst='Har bare ledig 8.–10. juni, ikke hele uka. De setter oss på venteliste og sier fra hvis det blir avbestillinger. '
               'Samme gruppe driver også Classic Hotel Gala i Split og Jona Rooms i Podstrana, og åpner et femstjerners Marriott-hotell i Split neste år.'),

    dict(hvem='Design Hostel One, Split', hva='7 netter for 28',
         maal=['split-billigst'], status='oss', dato='svarte 16. sep',
         tekst='Kan ta hele gruppen: tre sovesaler med seks senger og én med fire til elevene, uten andre gjester inne, '
               'og private rom til de voksne. 5 prosent avslag. Frokost koster 12 euro per person per dag. '
               'De venter på svar om hvor mange rom de voksne trenger.'),

    dict(hvem='Quality Airport Hotel Gardermoen', hva='Natten i Oslo på veien ned',
         maal=['kreta', 'split'], status='tilbud', dato='17. sep', pp=750,
         tekst='Christer Johansen har ledige rom: tremannsrom 2 215, dobbeltrom 1 580 og noen få familierom 2 515, '
               'alle med frokost. Med 8 tremannsrom og 2 dobbeltrom blir det 20 880 for hele gruppen. '
               'Frokosten serveres fra klokka 04:00, så den rekkes før utsjekk 04:30. '
               'Hvordan 28 personer med bagasje kommer til terminalen, har de ikke svart på.'),
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
