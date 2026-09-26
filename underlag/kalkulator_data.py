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

'kreta-charter': dict(
    hotellpost='Vings charterpakke: fly, transfer og 7 netter leilighet',
    matpost='Mat, delvis laget selv',
    aktivpost='Aktiviteter og lokalbusser',
    hotelltittel='Pakke og pensjon, sju netter',
    hotellnote='Fly, transfer og leilighet henger sammen i én pakke fra Ving. Valget her er hvor mye mat som legges inn i pakken — velger dere mer pensjon, kan matbudsjettet under settes ned.',
    hotell=[
        dict(navn='Ilion Beach, uten måltider', pp=8099, tekst='Åtte 1-romsleiligheter med kjøkkenkrok på stranda i Gerani. Fly, transfer og to kolli er med. Frokost og noen middager lages selv.'),
        dict(navn='Ilion Beach med frokost', pp=9044, tekst='Samme leiligheter med frokostbuffet på hotellet, 945 per person for uka. Da slipper man handling og oppvask om morgenen.'),
        dict(navn='Ilion Beach med halvpensjon', pp=10919, tekst='Frokost og middag på hotellet, 2 820 per person for uka. Dyrest i pakken, men matbudsjettet under kan da settes til det laveste.'),
    ],
    mat=[
        dict(navn='Nøktern', pp=1500, tekst='Frokost og de fleste middagene laget i leiligheten, lunsj ute (90) på utfluktsdagene.'),
        dict(navn='Som planlagt', pp=2200, tekst='Frokost i leiligheten, lunsj ute (90) og taverna fem av sju kvelder (200).'),
        dict(navn='Raus', pp=3000, tekst='Lunsj og middag ute hver dag, og is og drikke på utfluktene.'),
    ]),

'brac-charter': dict(
    hotellpost='Vings charterpakke: fly, transfer med ferje og 7 netter leilighet',
    matpost='Mat, delvis laget selv',
    aktivpost='Aktiviteter og øytransport',
    hotelltittel='Pakke og pensjon, sju netter',
    hotellnote='Fly, ferje, transfer og leilighet henger sammen i én pakke fra Ving. Valget her er hvor mye mat som legges inn i pakken.',
    hotell=[
        dict(navn='Waterman Supetrus, uten måltider', pp=8527, tekst='Åtte 2-romsleiligheter i Supetar på Brač, med bassenger og kort vei til havna. Fly, ferje, transfer og to kolli er med.'),
        dict(navn='Waterman Supetrus med frokost', pp=9767, tekst='Samme leiligheter med frokostbuffet, 1 240 per person for uka.'),
        dict(navn='Waterman Supetrus med All Inclusive', pp=12652, tekst='Alle måltider og drikke på anlegget, 4 125 per person for uka. Da kan matbudsjettet under settes til det laveste, men gruppen spiser da på hotellet hver dag.'),
    ],
    mat=[
        dict(navn='Nøktern', pp=1600, tekst='Frokost og de fleste middagene laget i leiligheten, lunsj ute (80) på utfluktsdagene.'),
        dict(navn='Som planlagt', pp=2300, tekst='Frokost i leiligheten, lunsj ute (80) og middag ute annenhver kveld (140).'),
        dict(navn='Raus', pp=3200, tekst='Lunsj og middag ute hver dag, og is og drikke underveis.'),
    ]),

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
    hotellpost='Fly, hotell med frokost, bagasje og transfer',
    matpost='Middag ute og lunsj',
    aktivpost='Aktiviteter med leiebuss',
    hotelltittel='Hotell og direktefly — Apollo-pakke',
    hotellnote='Her henger fly og hotell sammen i én pakke, så valget endrer begge deler.',
    hotell=[
        dict(navn='Galeana Beach, dobbeltrom med ekstraseng', pp=13233, tekst='3 stjerner rett på stranda i Platanes, frokost. Elevene tre og tre på rom på ca. 27 kvm.'),
        dict(navn='Galeana Beach, familierom til elevene', pp=13432, tekst='Samme hotell, men elevene bor på ca. 37 kvm i stedet for 27.'),
        dict(navn='Ariadne Rethymnon, ettroms leilighet', pp=14189, tekst='Frokost, 280 m fra stranda i Platanes. Leiligheter på ca. 25 kvm.'),
        dict(navn='Ariadne Rethymnon, toroms leilighet', pp=14503, tekst='Samme hotell, leiligheter på ca. 35 kvm med eget soverom.'),
    ],
    mat=[
        dict(navn='Nøktern', pp=2000, tekst='Frokost på hotellet, lunsj ved stranda (90 kr) og taverna fem av sju kvelder.'),
        dict(navn='Som planlagt', pp=2800, tekst='Frokost på hotellet, lunsj (120 kr) og taverna-middag (280 kr) hver dag.'),
        dict(navn='Raus', pp=3700, tekst='Taverna hver kveld med forrett og dessert, og mat kjøpt på utfluktene.'),
    ]),

'costabrava-billigst': dict(
    hotellpost='Leiligheter i Santa Susanna, 7 netter',
    matpost='Mat, delvis laget selv',
    aktivpost='Aktiviteter og transport',
    hotelltittel='Overnatting, sju netter',
    hotell=[
        dict(navn='SANTA SUSANNA Chic! Apartments by ALEGRIA', pp=3057, tekst='Leiligheter med kjøkken og basseng, 600 m fra sentrum og 850 m fra stranda. 8,6 av 10 i omtale.'),
        dict(navn='ALEGRIA Cartago Nova', pp=2194, tekst='Rett ved stranda i Malgrat de Mar, 1,7 km fra Santa Susanna. Frokost inkludert, 8,0 av 10. Uten kjøkken, så matbudsjettet må opp.'),
        dict(navn='Santa Susanna Resort Affiliated by FERGUS', pp=2718, tekst='Firemannsrom med frokost, 650 m fra stranda. 6,0 av 10 i omtale.'),
        dict(navn='Hostal Boutique Rivolto Rooms', pp=2817, tekst='150 m fra sentrum og 750 m fra stranda, 8,7 av 10. Uten måltider og uten basseng, og lite nok til at gruppa fyller huset.'),
    ],
    mat=[
        dict(navn='Nøktern', pp=1400, tekst='Frokost og de fleste middagene laget i leiligheten, lunsj ute et par ganger.'),
        dict(navn='Som planlagt', pp=2000, tekst='Frokost i leiligheten, lunsj ute (150 kr) og middag ute annenhver kveld.'),
        dict(navn='Raus', pp=2800, tekst='Lunsj og middag ute hver dag — menú del día (170 kr) og tapas om kvelden.'),
    ]),

'costabrava-best': dict(
    hotellpost='Hotell med halvpensjon, 7 netter',
    matpost='Lunsj og mat underveis',
    aktivpost='Aktiviteter med leiebuss',
    hotelltittel='Hotell med halvpensjon, sju netter',
    hotellnote='Frokost og middag er med i hotellprisen, derfor er matbudsjettet lavere her. Alle fire ligger i Santa Susanna og hadde halvpensjon ledig 8.–15. juni 2027 med fri avbestilling.',
    hotell=[
        dict(navn='AQUA Hotel Onabrava & Spa 4*Sup', pp=4670, tekst='4 stjerner superior, 9,0 av 10, basseng og spa, 300 m fra stranda. Firemannsrom med frokost og middag.'),
        dict(navn='AQUA Hotel Aquamarina & Spa', pp=4241, tekst='4 stjerner, 8,2 av 10, 250 m fra stranda. Firemannsrom med frokost og middag — rimeligst av de fire.'),
        dict(navn='ALEGRIA Caprici Verd 4 SUP', pp=4551, tekst='4 stjerner superior, 7,9 av 10, 250 m fra stranda. Firemannsrom med frokost og middag.'),
        dict(navn='ALEGRIA Florida & Spa', pp=4741, tekst='4 stjerner, 8,3 av 10, 250 m fra stranda. Familierom med frokost og middag.'),
    ],
    mat=[
        dict(navn='Nøktern', pp=1000, tekst='Frokost og middag er med i hotellet. Lunsj blir bocadillo eller pizzaskive (100 kr).'),
        dict(navn='Som planlagt', pp=1450, tekst='Frokost og middag på hotellet, lunsj ute (150 kr) hver dag, pluss mat på reisedagene.'),
        dict(navn='Raus', pp=2100, tekst='Lunsj ute hver dag (200 kr), is og drikke på utfluktene, og en kveld ute i Barcelona.'),
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
        dict(navn='Cora Hotel', pp=5960, tekst='4 stjerner 1,5 km fra sentrum i Split, 9,3 av 10 i omtale, frokost. Nærmere byen, men ikke på stranda. Eneste alternativ vi har pris på nå.'),
        dict(navn='Hotel San Antonio', pp=None, tekst='4 stjerner rett på stranda i Podstrana. Svarte 18. september at de bare har ledig 8.–10. juni, ikke hele uka. Vi står på venteliste.'),
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
