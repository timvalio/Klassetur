# -*- coding: utf-8 -*-
"""kalkulator_data.py — grunnlaget for «Sett sammen turen» på kartsida.

For hvert av de seks 10B-arkene sier denne fila tre ting:
  * hvilke rader i kostnadstabellen som er valgbare (hotell, mat, aktiviteter)
  * hvilke hotell man kan velge mellom, og hva de koster per reisende for sju netter
  * tre nivåer på matbudsjettet, med en forklaring på hva man faktisk får

Alt annet — buss, fly, forsikring, flyplasstransfer — regnes ut av lag_kart.py som
«fast» og kan ikke velges bort. Utfluktene hentes automatisk fra dagsprogrammet.

Priser er kroner per reisende for hele uka. pp=None betyr at vi ikke har pris ennå;
da vises alternativet, men kan ikke velges.
"""

DATA = {

'kreta-billigst': dict(
    hotellpost='Hotell i Rethymno, 7 netter med frokost',
    matpost='Middag ute og lunsj',
    aktivpost='Aktiviteter og lokalbusser',
    hotelltittel='Hotell, sju netter',
    hotell=[
        dict(navn='Olympic Palladium', pp=2820, tekst='3 stjerner i Rethymno by, 300 m fra stranda, frokost. Gruppepris fra hotellet: 8 tremannsrom og 2 dobbeltrom, klimaskatt medregnet.'),
        dict(navn='Welcome Apts', pp=2530, tekst='Leiligheter for fire med kjøkkenkrok i Georgioupolis, uten måltider. Billigst, men 1,5 km opp fra sentrum.'),
        dict(navn='Theros', pp=1910, tekst='Leiligheter 2,6 km fra Rethymno sentrum. Rimeligst av alle, men ikke kontrollert i detalj.'),
    ],
    mat=[
        dict(navn='Nøktern', pp=1300, tekst='Frokost på hotellet, gyros eller spanakopita til lunsj (70 kr), og handlemat til middag et par kvelder.'),
        dict(navn='Som planlagt', pp=1900, tekst='Frokost på hotellet, gyros til lunsj (70 kr) og enkel taverna til middag (140 kr) hver dag.'),
        dict(navn='Raus', pp=2600, tekst='Taverna hver kveld (200 kr), dessert, og is og drikke på utfluktene.'),
    ]),

'kreta-best': dict(
    hotellpost='Direktefly Alta–Chania og hotell, 7 netter med frokost',
    matpost='Middag ute og lunsj',
    aktivpost='Aktiviteter med leiebuss',
    hotelltittel='Hotell og direktefly — Apollo-pakke',
    hotellnote='Her henger fly og hotell sammen i én pakke, så valget endrer begge deler.',
    hotell=[
        dict(navn='Galeana Beach', pp=12820, tekst='3 stjerner rett på stranda i Platanes, frokost. Fem km øst for Rethymno by.'),
        dict(navn='Akti Chara', pp=12370, tekst='4 stjerner på stranda i Platanes, men studioer uten måltider — da må matbudsjettet opp.'),
        dict(navn='Ariadne Rethymnon', pp=13620, tekst='Frokost, 280 m fra stranda i Platanes. Dyrest av de tre.'),
    ],
    mat=[
        dict(navn='Nøktern', pp=2000, tekst='Frokost på hotellet, lunsj ved stranda (90 kr) og taverna fem av sju kvelder.'),
        dict(navn='Som planlagt', pp=2800, tekst='Frokost på hotellet, lunsj (120 kr) og taverna-middag (280 kr) hver dag.'),
        dict(navn='Raus', pp=3700, tekst='Taverna hver kveld med forrett og dessert, og mat kjøpt på utfluktene.'),
    ]),

'costablanca-billigst': dict(
    hotellpost='Leiligheter i Albir, 7 netter',
    matpost='Mat, delvis laget selv',
    aktivpost='Aktiviteter og transport',
    hotelltittel='Overnatting, sju netter',
    hotell=[
        dict(navn='Albir Garden Resort', pp=3090, tekst='Leiligheter for fire med kjøkken, midt i Albir, eget badeland. 15 minutters gange til stranda.'),
        dict(navn='Nacavi Albir Aparthotel', pp=2660, tekst='Leiligheter for fire i Albir. Rimeligst, men minst informasjon å gå på.'),
        dict(navn='Hotel Noguera El Albir', pp=3910, tekst='Lite familiedrevet hotell, 9,0 av 10 i omtale, dobbeltrom med frokost. Ingen kjøkken, så matbudsjettet må opp.'),
    ],
    mat=[
        dict(navn='Nøktern', pp=1400, tekst='Frokost og de fleste middagene laget i leiligheten, lunsj ute et par ganger.'),
        dict(navn='Som planlagt', pp=2000, tekst='Frokost i leiligheten, lunsj ute (150 kr) og middag ute annenhver kveld.'),
        dict(navn='Raus', pp=2800, tekst='Lunsj og middag ute hver dag — menú del día (170 kr) og tapas om kvelden.'),
    ]),

'costablanca-best': dict(
    hotellpost='Hotell med halvpensjon, 7 netter',
    matpost='Lunsj og mat underveis',
    aktivpost='Aktiviteter med leiebuss',
    hotelltittel='Hotell med halvpensjon, sju netter',
    hotellnote='Frokost og middag er med i hotellprisen, derfor er matbudsjettet lavere her.',
    hotell=[
        dict(navn='Hotel Cap Negret', pp=9000, tekst='4 stjerner rett på stranda i Altea, 9,0 av 10 i omtale, halvpensjon. Ikke kontaktet ennå.'),
        dict(navn='Albir Playa Hotel & Spa', pp=None, tekst='Svarte 16. september at de ikke tar imot skolegrupper. Ute av lista.'),
        dict(navn='Hotel Kaktus Albir', pp=None, tekst='4 stjerner på stranda i Albir, bekreftet tremannsrom. Prisen vi har er en Ving-pakke med fly fra Oslo, så den kan ikke regnes inn her. Forespørsel bør sendes.'),
    ],
    mat=[
        dict(navn='Nøktern', pp=1000, tekst='Frokost og middag er med i hotellet. Lunsj blir bocadillo eller pizzaskive (100 kr).'),
        dict(navn='Som planlagt', pp=1450, tekst='Frokost og middag på hotellet, lunsj ute (150 kr) hver dag, pluss mat på reisedagene.'),
        dict(navn='Raus', pp=2100, tekst='Lunsj ute hver dag (200 kr), is og drikke på utfluktene, og en kveld ute i Altea.'),
    ]),

'split-billigst': dict(
    hotellpost='Hostel i Split, 7 netter',
    matpost='Mat, enkel',
    aktivpost='Aktiviteter og lokaltransport',
    hotelltittel='Overnatting, sju netter',
    hotell=[
        dict(navn='Design Hostel One', pp=4330, tekst='Innenfor murene i gamlebyen, fem minutter fra Diokletians palass. Firemannsrom, dobbeltrom og sovesalsplasser, uten måltider.'),
        dict(navn='Plavi Horizont, Podstrana', pp=None, tekst='Gruppehotell ved stranda 20 minutter sør for Split. Pris på forespørsel.'),
        dict(navn='Hotel Zagreb, Duilovo', pp=None, tekst='3 stjerner, gruppehotell ved stranda. Ingen priser for juni 2027 ennå.'),
    ],
    mat=[
        dict(navn='Nøktern', pp=1500, tekst='Frokost og handlemat fra Konzum, burek eller pizzaskive til lunsj (60 kr).'),
        dict(navn='Som planlagt', pp=2100, tekst='Burek til lunsj (60 kr) og enkel konoba eller ćevapi til middag (160 kr).'),
        dict(navn='Raus', pp=2900, tekst='Middag ute hver kveld (230 kr), fisk én gang, og is på Rivaen.'),
    ]),

'split-best': dict(
    hotellpost='Hotell i Podstrana, 7 netter med frokost',
    matpost='Middag ute og lunsj',
    aktivpost='Aktiviteter med leiebuss',
    hotelltittel='Hotell, sju netter med frokost',
    hotell=[
        dict(navn='Hotel San Antonio', pp=5410, tekst='4 stjerner rett på stranda i Podstrana, frokost. Bybuss 60 inn til gamlebyen, 8–10 km.'),
        dict(navn='Cora Hotel', pp=5960, tekst='4 stjerner 1,5 km fra sentrum i Split, 9,3 av 10 i omtale, frokost. Nærmere byen, men ikke på stranda.'),
        dict(navn='Hotel Atrium', pp=None, tekst='5 stjerner 1,3 km fra sentrum. Prisen vi har er en Ving-pakke med SAS-fly, så den kan ikke regnes inn her.'),
    ],
    mat=[
        dict(navn='Nøktern', pp=2000, tekst='Frokost på hotellet, enkel lunsj (90 kr) og middag ute fem av sju kvelder.'),
        dict(navn='Som planlagt', pp=2750, tekst='Frokost på hotellet, lunsj ute (130 kr) og middag ute (250 kr) hver dag.'),
        dict(navn='Raus', pp=3600, tekst='Som over, men fiskerestaurant et par kvelder og mat kjøpt på utfluktene.'),
    ]),
}

LEDE = ('Sett sammen turen slik dere vil ha den, så regnes prisen om med en gang. '
        'Dette er et regnestykke på grunnlaget vi har nå — ikke et tilbud.')
FAST_TEKST = 'Buss til Alta, fly, forsikring og transport på stedet. Dette ligger fast.'
