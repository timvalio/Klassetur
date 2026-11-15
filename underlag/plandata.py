# -*- coding: utf-8 -*-
"""Datagrunnlag for Klassetur 10B — hva er bekreftet og hva må velges.

Alle beløp i kroner for hele gruppen (28 reisende) hvis ikke annet står.
Eurobeløp er regnet om med 10,56 (currency.wiki, 13.11.2026).
Hotellprisene er booking.com sine gruppepriser for 8.–15. juni 2027, slått
opp 14.10.2026, og gjelder alle 28 i én bestilling.
"""
import json, pathlib, re, sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
import beriket as B

EUR = 10.56
EUR_KILDE = 'currency.wiki, 13.11.2026'

GRUPPE, ELEVER, VOKSNE = 28, 21, 7
SAMLET_INN = 415000
SAMLET_INN_DATO = '2026-11-14'   # oppdateres etter hvert som kassa vokser
FRIST = '2027-03-30'          # første virkedag etter påska — 2. påskedag er mandag 29. mars 2027
AVREISE = '2027-06-08'
NETTER = 7


def kr(e):
    """Euro til kroner, avrundet til nærmeste ti."""
    return int(round(e * EUR / 10.0) * 10)


# ------------------------------------------------------------ bekreftet
FLY_SUM, FLY_AVGIFT = 178556, 14588
FLY_GRUNN = FLY_SUM - FLY_AVGIFT              # 163 968, depositum regnes av denne
FLY_DEPOSITUM = int(round(FLY_GRUNN * 0.30))
BUSS_SUM = 17000

BEKREFTET = [
    dict(id='buss', tittel='Buss Kautokeino–Alta tur/retur', kortnavn='Buss, Nils Rune Eira', kr=BUSS_SUM,
         hvem='Nils Rune Eira',
         kort='Kjøring og henting begge veier, fast pris for hele gruppen.',
         fakta=[('Leverandør', 'Nils Rune Eira'),
                ('Strekning', 'Kautokeino–Alta lufthavn, 136 km hver vei'),
                ('Pris', '17 000 for hele gruppen, 607 per reisende'),
                ('Betaling', 'Faktureres etter turen'),
                ('Datobinding', 'Prisen er ikke bundet til bestemte datoer')],
         tekst='Samme selskap oppga 26 200 for Kittilä, så prisen følger avstanden. '
               'Bussen henter ved skolen og kjører helt fram til terminalen.'),
    dict(id='fly', tittel='Fly Alta–Oslo–Barcelona tur/retur', kortnavn='Fly, Norwegian Y7XH8L', kr=FLY_SUM,
         hvem='Norwegian, gruppereferanse Y7XH8L',
         kort='Bekreftet gruppetilbud for alle 28, begge veier.',
         fakta=[('Gruppereferanse', 'Y7XH8L'),
                ('Ut tirsdag 8. juni', 'DY 321 Alta–Oslo 11:55–13:55, D8 5523 Oslo–Barcelona 19:35–22:55'),
                ('Hjem tirsdag 15. juni', 'DY 1741 Barcelona–Oslo 13:10–16:35, DY 328 Oslo–Alta 19:50–22:50'),
                ('Pris', '163 968 pluss 14 588 i skatter og avgifter = 178 556'),
                ('Per reisende', '6 377'),
                ('Bagasje', '2 × 23 kg innsjekket, to håndbagasjer og én taxfreepose per reisende'),
                ('Depositum', f'{FLY_DEPOSITUM} — 30 prosent av 163 968, altså uten skatter og avgifter'),
                ('Navneliste', 'Senest fem dager før avreise, altså 3. juni 2027')],
         tekst='Dato, tid og reisemål kan ikke endres på en gruppebestilling. Gruppen kan '
               'reduseres med inntil 10 prosent — to personer — uten å miste depositumet, '
               'og det må meldes skriftlig minst 31 dager før avreise. Faktura tilbys ikke '
               'i Norden, så begge innbetalinger må gjøres med kredittkort under «Mine reiser».',
         lenke='https://www.norwegian.com/no/booking/bestillingsinformasjon/gruppebestilling/vilkar/',
         lenketekst='Norwegians gruppevilkår'),
]

FORFALL = [
    dict(dato='2026-11-25', hva='Depositum fly, 30 prosent av 163 968', kr=FLY_DEPOSITUM,
         note='21 dager etter at forespørselen ble sendt 4. november. Kredittkort.'),
    dict(dato='2027-05-09', hva='Restbeløp fly', kr=FLY_SUM - FLY_DEPOSITUM,
         note='30 dager før avreise. Kredittkort.'),
    dict(dato='etter turen', hva='Buss Kautokeino–Alta', kr=BUSS_SUM,
         note='Faktureres i etterkant.'),
]

# ------------------------------------------------------------ transfer
TRANSFER = [
    dict(id='moventis', navn='Delt flybuss, Moventis Experience', kr=kr(28 * 2 * 18),
         type='Transport, flyplass–hotell',
         hvaer='Transport. Fast flybussrute som samler flere reisende og setter gruppen av ved overnattingsstedet.',
         kort='18 euro per person hver vei, avsatt ved overnattingsstedet.',
         fakta=[('Grunnlag', '28 × 2 × 18 euro'), ('Type', 'Delt buss med flere stopp'),
                ('Slått opp', '26. september 2026')],
         tekst='Avsetter gruppen ved overnattingsstedet. At siste avgang passer med landing '
               '22:55 må bekreftes før dette kan velges endelig.',
         lenke='https://www.moventisexperience.com/', lenketekst='Moventis Experience'),
    dict(id='suntransfers', navn='Delt flybuss, Suntransfers', kr=kr(28 * 2 * 19.55),
         type='Transport, flyplass–hotell',
         hvaer='Transport. Delt buss med flere stopp underveis, bestilt på forhånd for hele gruppen.',
         kort='19,55 euro per person hver vei, 75 km og omtrent 75 minutter.',
         fakta=[('Grunnlag', '28 × 2 × 19,55 euro'), ('Reisetid', 'omtrent 75 minutter'),
                ('Avstand', '75 km'), ('Slått opp', '13. november 2026')],
         tekst='Delt transport med flere stopp underveis. Samme selskap tilbyr privat minivan '
               'til 200 euro for åtte personer — fire slike blir 1 600 euro tur/retur, altså '
               'dyrere enn delt buss for 28.',
         lenke='https://www.suntransfers.com/barcelona-airport-to-santa-susanna',
         lenketekst='Suntransfers'),
    dict(id='tog', navn='Tog via Barcelona sentrum', kr=None,
         type='Transport, flyplass–hotell',
         hvaer='Transport. Flyplasstog inn til Barcelona sentrum og videre med lokaltoget R1 ut til Santa Susanna, med bytte underveis.',
         kort='Billigst i kroner, men vanskelig med landing 22:55.',
         fakta=[('Togpris', '7 euro per person hver vei'), ('Reisetid', '1 t 15 min på R1'),
                ('Mangler', 'flyplasstog og siste avgang')],
         tekst='R1 går direkte Barcelona–Santa Susanna, men gruppen må først fra flyplassen '
               'inn til sentrum, og flyet lander 22:55. Siste avgang må sjekkes før dette kan '
               'prises. 28 personer med koffert på nattog er uansett tungvint.',
         lenke='https://www.omio.fr/trains/santa-susanna/barcelone-n88mi', lenketekst='Rutetider'),
    dict(id='privatbuss', navn='Privat buss for hele gruppen', kr=None,
         type='Transport, flyplass–hotell',
         hvaer='Transport. Egen buss bare for klassen, som møter gruppen i ankomsthallen og kjører rett til overnattingsstedet.',
         kort='Egen buss som møter gruppen ved ankomst. Pris må innhentes.',
         fakta=[('Status', 'Forespørsel ikke sendt'),
                ('Sammenligning', 'Beniconnect ga 607 euro tur/retur for 28 til Costa Blanca')],
         tekst='Dette er alternativet med størst sparepotensial. Blir prisen i samme leie som '
               'Costa Blanca-tilbudet, koster det rundt en tredel av delt flybuss, og gruppen '
               'slipper å vente på andre passasjerer midt på natta.'),
]

# ------------------------------------------------------------ mat
MAT = [
    dict(id='selvhushold', navn='Selvhushold i leilighet, menú del día ellers', kr=56000,
         type='Mat for åtte dager',
         hvaer='Mat. Frokost og en del middager lages selv i leilighetene, resten spises ute.',
         kort='28 × 2 000. Forutsetter leilighet med kjøkken.', anslag=True,
         fakta=[('Grunnlag', '28 × 2 000'), ('Per dag', 'rundt 250 per person'),
                ('Status', 'Anslag, ikke innhentet pris')],
         tekst='Frokost og noen middager laget selv i leilighetene, bocadillo til lunsj, '
               'menú del día (13–17 euro) ellers. Krever at hotellvalget har kjøkken.'),
    dict(id='halvpensjon', navn='Lunsj ute, hotellet dekker frokost og middag', kr=40600,
         type='Mat for åtte dager',
         hvaer='Mat. Hotellet serverer frokost og middag, og bare lunsj kjøpes ute.',
         kort='28 × 1 450. Forutsetter hotell med halvpensjon.', anslag=True,
         fakta=[('Grunnlag', '28 × 1 450'), ('Lunsj ute', 'rundt 150 per person per dag'),
                ('Status', 'Anslag, ikke innhentet pris')],
         tekst='Billigste matpost, men bare hvis hotellvalget faktisk har frokost og middag. '
               'Hotellene merket «frokost og middag» i lista dekker to måltider om dagen.'),
    dict(id='alt-ute', navn='Alle måltider ute', kr=78400,
         type='Mat for åtte dager',
         hvaer='Mat. Alle måltider kjøpes underveis, uten binding til hotellets servering.',
         kort='28 × 2 800. Frokost på hotellet, lunsj og middag ute.', anslag=True,
         fakta=[('Grunnlag', '28 × 2 800'), ('Status', 'Anslag, ikke innhentet pris')],
         tekst='Dyreste modell, men den enkleste å gjennomføre med 21 ungdommer. '
               'Gir mest frihet i programmet.'),
]

# ------------------------------------------------------------ sikre inntekter
# Inntekter klassen vet kommer, og som derfor kan regnes med i budsjettet.
# kr=None betyr at beløpet ennå ikke er fylt inn.
SIKRE_INNTEKTER = [
    dict(id='paskefestival', navn='Vakthold påskefestivalen', kr=60000,
         dato='2027-03-28', note='Garantert oppdrag. Omtrentlig beløp oppgitt av klassen.'),
]

# ------------------------------------------------------------ husregler, booking.com 14.11.2026
# alder = laveste alder for den som sjekker inn, slik booking.com oppgir den.
# fest  = stedet skriver at det ikke tar imot utdrikningslag eller lignende grupper.
# Ingen av stedene sier noe om skoleklasser i husreglene — det må spørres om.
HUSREGLER = {
    'safari':                        dict(alder=20, fest=True),
    'odissea-park':                  dict(alder=18, fest=True),
    'sant-jordi-santa-susanna':      dict(alder=18, fest=False),
    'santa-susanna-chic-apartments': dict(alder=None, fest=True),
    'htopplanamar':                  dict(alder=18, fest=False),
    'haromar':                       dict(alder=None, fest=False),
    'president-calella':             dict(alder=18, fest=False),
    'boutique-rivolto-rooms':        dict(alder=None, fest=True),
    'internacional':                 dict(alder=21, fest=False),
    'alhambra':                      dict(alder=18, fest=False),
    'reymar-playa':                  dict(alder=None, fest=False),
    'hotel-maritim':                 dict(alder=None, fest=False),
    'mar-blau-calella':              dict(alder=None, fest=False),
    'aqua-aquamarina':               dict(alder=None, fest=False),
    'alegria-florida-park':          dict(alder=None, fest=False),
    'aqua-onabrava':                 dict(alder=None, fest=False),
}
HUSREGLER_KILDE = 'booking.com, husregler lest 14. november 2026'

# Steder som er tatt ut av lista fordi aldersgrensen for innsjekking er over 18.
# Med 21 elever på 15–16 år er det en reell sperre, ikke en formalitet.
HOTELL_UTELATT = []


# ------------------------------------------------------------ reise til aktivitetene
# Ingen spansk busselskap publiserer km-pris, og ingen har gitt tilbud ennå.
# Anslagene bygger på publiserte satser for leiebuss med sjåfør for 30 personer:
# kort tur under 200 km fra 650 euro, dagstur rundt 500 km fra 950 euro.
# Kilde: https://agtlogistik.de/en/reisebus-mieten-kosten
# Satsene er europeiske referansepriser, ikke spanske tilbud. Alt må innhentes.
REISE_HALVDAG = round(kr(650), -2)    # buss med sjåfør en halv dag
REISE_DAGSTUR = round(kr(950), -2)    # buss med sjåfør en hel dag
REISE_KILDE = ('anslag — publisert sats for leiebuss med sjåfør for 30 personer, '
               'ikke et spansk tilbud')


def reise(km, minutter, kr_, hva='Leiebuss for hele gruppen'):
    return dict(km=km, minutter=minutter, kr=kr_, hva=hva, kilde=REISE_KILDE)


# ------------------------------------------------------------ aktiviteter
AKTIVITETER = [
    dict(id='strand', navn='Strand, basseng og Santa Susanna', kr=0, sted='gangavstand',
         type='Strand og bading',
         hvaer='Bading og strandliv. Santa Susanna har lang sandstrand og promenade, '
               'og alle overnattingsstedene ligger i gangavstand. Det koster ingenting.',
         kort='Koster ingenting og fyller dagene mellom utfluktene.',
         fakta=[('Avstand', 'gangavstand fra alle overnattingsstedene'), ('Pris', 'ingen')],
         tekst='Santa Susanna er en strandby med lang sandstrand og promenade. '
               'Dette er det turen hviler på mellom utfluktene.'),
    dict(id='sagrada', navn='Sagrada Família med guide', kr=kr(ELEVER * 15), sted='Barcelona',
         type='Severdighet med omvisning',
         hvaer='Severdighet. Gaudís kirke i Barcelona, påbegynt i 1882 og fortsatt under '
               'bygging. Besøket er en guidet omvisning inne i kirken.',
         kort='Skolegruppepris: 15 euro per elev, lærere gratis.',
         fakta=[('Grunnlag', '21 elever × 15 euro, 7 lærere gratis'),
                ('Vanlig pris', '26 euro per person, altså 7 700 for gruppa'),
                ('Krav', 'offisiell guide godkjent av Generalitat'),
                ('Kommer i tillegg', 'tog til Barcelona')],
         tekst='Skolegrupper får guidet omvisning til 15 euro per elev, og lærere går gratis. '
               'Det halverer prisen mot vanlig billett. Må bestilles som skolegruppe.',
         lenke='https://sagradafamilia.org/en/prices', lenketekst='Priser hos Sagrada Família'),
    dict(id='bcn-tog', navn='Dagstur til Barcelona, tog tur/retur', kr=kr(GRUPPE * 14),
         sted='Santa Susanna–Barcelona',
         type='Transport',
         hvaer='Transport, ikke en aktivitet i seg selv. Lokaltoget R1 går fra Santa Susanna '
               'stasjon langs sjøen inn til Barcelona. Billettene dekker bare reisen — det '
               'man skal se i byen kommer i tillegg.',
         kort='R1 direkte, 1 t 15 min hver vei.',
         fakta=[('Grunnlag', '28 × 7 euro hver vei'), ('Linje', 'Rodalies R1, direkte'),
                ('Reisetid', '1 t 15 min'),
                ('Til stasjonen', '2 km fra hotellområdet'),
                ('Dekker', 'reisen, ikke inngangsbilletter')],
         tekst='Toget går fra Santa Susanna stasjon. Dette er transporten til alt som ligger '
               'i Barcelona — Sagrada Família og Park Güell kommer i tillegg.',
         lenke='https://www.omio.fr/trains/santa-susanna/barcelone-n88mi', lenketekst='Rutetider'),
    dict(id='guell', navn='Park Güell', kr=kr(GRUPPE * 18), sted='Barcelona',
         type='Severdighet, uteområde',
         hvaer='Severdighet utendørs. Park og hage tegnet av Gaudí i åssiden over Barcelona, '
               'med mosaikkbenker, terrasse og utsikt over byen. Man går rundt ute.',
         kort='28 × 18 euro. Tidsbestilt inngang.',
         fakta=[('Grunnlag', '28 × 18 euro'), ('Full pris fra', '13 år'),
                ('Åpent', 'tidsbestilt inngang 09:30–17:30'),
                ('Kommer i tillegg', 'tog til Barcelona')],
         tekst='Gaudís park i åssiden over byen. Billetten er tidsbestilt, så den må kjøpes '
               'på forhånd med klokkeslett.',
         lenke='https://parkguell.barcelona/en/planning-your-visit/prices-and-times',
         lenketekst='Priser og åpningstider'),
    dict(id='illafantasia', navn='Illa Fantasia', kr=kr(GRUPPE * 33),
         sted='Vilassar de Dalt, 37 km',
         type='Vannpark',
         hvaer='Bading hele dagen. Vannpark med 22 sklier, bølgebasseng og et piratområde '
               'for de minste. Alle er i badetøy fra man går inn til man går ut.',
         kort='28 × 33 euro. Åpner 6. juni, to dager før gruppa kommer.',
         fakta=[('Grunnlag', '28 × 33 euro'), ('Åpent', '6. juni–6. september, 10–18'),
                ('Avstand', '37 km, omtrent 30 minutter med bil'),
                ('Mangler', 'transport er ikke priset')],
         tekst='Vannpark i Maresme med 22 sklier. Åpner akkurat i tide. '
               'Transport for gruppen kommer i tillegg og er ikke hentet inn.',
         lenke='https://www.taquilla.com/entradas/illa-fantasia', lenketekst='Priser'),
    dict(id='marineland', navn='Marineland Catalunya', kr=kr(GRUPPE * 36), sted='Palafolls, 7 km',
         type='Dyrepark og vannpark',
         hvaer='Dyrepark og bading i ett. Delfinshow og vannpark med sklier ligger på samme '
               'område og går på samme billett.',
         kort='28 × 36 euro. Nærmeste store attraksjon.',
         fakta=[('Grunnlag', '28 × 36 euro'), ('Åpent', '28. mai–20. september, 10:30–18'),
                ('Avstand', '7 km, omtrent 10 minutter med bil'),
                ('Gruppepris', 'finnes på forespørsel, ikke regnet inn')],
         tekst='Delfinarium og vannpark rett ved. Den korte avstanden gjør transporten billig, '
               'og gruppepris på forespørsel kan trekke prisen videre ned.',
         lenke='https://www.taquilla.com/entradas/marineland-catalunya', lenketekst='Priser'),
    dict(id='waterworld', navn='Water World', kr=kr(GRUPPE * 40), sted='Lloret de Mar, 16 km',
         type='Vannpark',
         hvaer='Bading hele dagen. Vannpark i Lloret de Mar med sklier og bassenger. '
               'Alle er i badetøy fra man går inn til man går ut.',
         kort='28 × 40 euro. Gruppepris på forespørsel.',
         fakta=[('Grunnlag', '28 × 40 euro'), ('Åpent', '23. mai–13. september, 10–18 i juni'),
                ('Avstand', '16 km, omtrent 20 minutter med bil'),
                ('Gruppepris', 'booking@waterworld.es, ikke regnet inn'),
                ('Mangler', 'transport er ikke priset'),
                ('Bilder', 'ingen fritt lisensierte bilder av parken finnes — '
                           'se parkens egne sider')],
         tekst='Stor vannpark i Lloret de Mar. Parken oppgir at den har egne gruppepriser, '
               'så prisen her er veiledende nettpris og trolig for høy.',
         lenke='https://waterworld.es/en/frequently-asked-questions/', lenketekst='Water World'),
    dict(id='portaventura', navn='PortAventura og Ferrari Land', kr=kr(GRUPPE * 44),
         sted='Salou, 173 km',
         type='Fornøyelsespark',
         hvaer='Fornøyelsespark med berg-og-dal-baner. Shambhala er 76 meter høy og går i '
               '134 km/t, og Dragon Khan har åtte looper. Ferrari Land ligger vegg i vegg '
               'og er med på kombibilletten.',
         kort='28 × 44 euro for én dag i to parker. Over to timer hver vei.',
         fakta=[('Grunnlag', '28 × 44 euro, én dag to parker'),
                ('Alternativ', 'bare PortAventura: 37 euro per person'),
                ('Avstand', '173 km sørover, omtrent 2 timer og 10 minutter hver vei'),
                ('Mangler', 'leiebuss for hele gruppen er ikke priset')],
         tekst='Spanias største fornøyelsespark. Avstanden gjør at dette blir en hel dag med '
               'over fire timer i buss, og leiebussen kommer i tillegg til billettene.',
         lenke='https://www.portaventuraworld.com/en/tickets', lenketekst='Priser'),
    dict(id='tossa', navn='Tossa de Mar', kr=None, sted='28 km nordover',
         type='Severdighet og strand',
         hvaer='Severdighet og bading. Befestet gamleby med bymur og tårn ute på neset, '
               'og strand rett innenfor. Selve byen koster ingenting å gå rundt i.',
         kort='Middelalderbyen med bymur i sjøen. Pris må innhentes.',
         fakta=[('Avstand', '28 km nordover langs kysten, omtrent 35 minutter med bil'),
                ('Mangler', 'billett på kystbåt eller buss')],
         tekst='Gammel befestet by rett i sjøkanten. Kystbåten fra Calella eller Blanes er '
               'den fine måten å komme dit på, men prisen må hentes inn.'),
]

# Veiavstand og kjøretid fra Santa Susanna, slått opp i OSRM 14.11.2026.
REISER = {
    'strand':       reise(0, 0, 0, 'Gangavstand fra overnattingsstedene'),
    'sagrada':      reise(None, None, 0, 'Dekkes av togbilletten til Barcelona'),
    'bcn-tog':      reise(None, 75, 0, 'Toget er selve reisen'),
    'guell':        reise(None, None, 0, 'Dekkes av togbilletten til Barcelona'),
    'illafantasia': reise(37, 30, REISE_HALVDAG),
    'marineland':   reise(7, 10, REISE_HALVDAG,
                          'Leiebuss for hele gruppen — så kort at lokalbuss eller '
                          'drosjer trolig blir billigere'),
    'waterworld':   reise(16, 20, REISE_HALVDAG),
    'portaventura': reise(173, 130, REISE_DAGSTUR,
                          'Leiebuss for hele gruppen — over fire timer kjøring, '
                          'altså en hel dag for sjåføren'),
    'tossa':        reise(28, 35, REISE_HALVDAG,
                          'Leiebuss for hele gruppen, eller kystbåt fra Calella '
                          'eller Blanes der prisen mangler'),
}

def _tall(n):
    return f'{int(round(n)):,}'.replace(',', ' ')


for _a in AKTIVITETER:
    _a['koord'] = list(B.AKT_KOORD.get(_a['id'], ())) or None
    _a['bilder2'] = B.AKT_BILDER.get(_a['id'], [])
    _r = REISER.get(_a['id'])
    _a['reise'] = _r
    _a['billettKr'] = _a['kr']
    if _r and _r['kr']:
        _a['anslag'] = True
        if _a['kr'] is not None:
            _a['kr'] = _a['kr'] + _r['kr']
            _a['kort'] = _a['kort'] + f" Pluss {_tall(_r['kr'])} i buss."
        else:
            _a['kort'] = _a['kort'] + f" Buss anslått til {_tall(_r['kr'])}."
        _a['fakta'] = list(_a['fakta']) + [
            ('Reise fram og tilbake',
             f"{_tall(_r['kr'])} — {_r['kilde']}"),
        ]

BASIS = B.BASIS

BUFFER = [
    dict(id='b0', navn='Ingen buffer', pct=0),
    dict(id='b5', navn='5 prosent buffer', pct=5),
    dict(id='b10', navn='10 prosent buffer', pct=10),
]


def _nf(n):
    """Tall med mellomrom som tusenskille."""
    return f'{int(round(n)):,}'.replace(',', ' ')


def hoteller():
    kilde = pathlib.Path(__file__).resolve().parent / 'hoteller.json'
    data = json.loads(kilde.read_text(encoding='utf-8'))
    HOTELL_UTELATT.clear()
    ut = []
    for h in data['costabrava']:
        fire = '4*' in h['navn'] or h['navn'] in (
            'AQUA Hotel Aquamarina & Spa', 'ALEGRIA Florida & Spa', 'GHT Maritim')
        sats = 1.80 if fire else 0.90
        skatt = kr(VOKSNE * NETTER * sats)
        fakta = [('Sted', h['sted']),
                 ('Måltider', h['mat']),
                 ('Gjestevurdering', f"{h['score']} av 10 av {h['omtaler']} omtaler"),
                 ('Pris for gruppen', f"{_nf(h['pris'])} for 7 netter, {_nf(h['pp'])} per reisende"),
                 ('Per natt per reisende', _nf(h['pp'] / NETTER)),
                 ('Turistskatt', f"{_nf(skatt)} — {sats:.2f} euro per voksen per natt, "
                                 f"elevene er fritatt til og med 16 år".replace('.', ','))]
        if h['vilkaar']:
            fakta.append(('Vilkår', h['vilkaar']))
        else:
            fakta.append(('Vilkår', 'ikke merket 14.10.2026, må bekreftes ved bestilling'))
        slug = re.search(r'/hotel/es/([^.]+)\.', h['url'])
        slug = slug.group(1) if slug else ''

        regel = HUSREGLER.get(slug, {})
        alder, fest = regel.get('alder'), regel.get('fest')
        if alder and alder > 18:
            HOTELL_UTELATT.append((h['navn'], f'aldersgrensen for innsjekking er {alder} år'))
            continue
        hindre = []
        if alder:
            hindre.append(f'den som sjekker inn må være minst {alder} år')
        if fest:
            hindre.append('stedet ikke tar imot utdrikningslag eller lignende grupper')
        fakta.append(('Husregler', '; '.join(hindre) if hindre
                      else 'ingen aldersgrense eller gruppesperre oppgitt'))
        fakta.append(('Skolegruppe', 'ikke bekreftet — ingen av stedene sier noe om '
                                     'skoleklasser, det må spørres om skriftlig'))

        eks = B.HOTELL.get(slug, {})
        ut.append(dict(
            anslag=True, husregler=hindre, husreglerKilde=HUSREGLER_KILDE,
            maaBekreftes=bool(hindre),
            id=re.sub(r'[^a-z0-9]+', '-', h['navn'].lower()).strip('-'),
            navn=h['navn'], sted=h['sted'], mat=h['mat'], score=h['score'],
            omtaler=h['omtaler'], kr=h['pris'], pp=h['pp'], url=h['url'],
            bilde=h['bilde'], skatt=skatt,
            bilder=eks.get('bilder', []),
            koord=eks.get('koord'), omtrentlig=eks.get('omtrentlig', False),
            beskrivelse=eks.get('beskrivelse', ''),
            fasiliteter=eks.get('fasiliteter', []),
            type=f"Overnatting · {NETTER} netter",
            hvaer=f"Overnatting for hele gruppen i {NETTER} netter, 8.–15. juni 2027. "
                  f"{h['mat']} er inkludert i prisen.",
            kort=f"{h['sted']} · {h['mat'].lower()} · {h['score']} av 10",
            fakta=fakta,
            tekst='Prisen er et estimat. Den kommer fra ett booking.com-søk på hele gruppen '
                  'på 28 for 8.–15. juni 2027, sto 14. oktober 2026, er ikke holdt av og er '
                  'ingen gruppepris. Ingen av hotellene har fått forespørsel som skolegruppe. '
                  'Husregler, beskrivelse, bilder og fasiliteter er hentet fra booking.com '
                  '14. november 2026.',
            lenke=h['url'], lenketekst='Se på booking.com'))
    ut.sort(key=lambda x: x['kr'])
    return ut


def grunnvalg():
    """Det billigste oppsettet som faktisk henger sammen.

    Hotell og mat må passe til hverandre: et sted uten måltider må ha
    selvhushold eller alle måltider ute, et sted med frokost og middag må ha
    halvpensjon eller alle måltider ute. Billigste hotell er derfor ikke
    nødvendigvis billigste kombinasjon.
    """
    tra = min((t for t in TRANSFER if t['kr']), key=lambda t: t['kr'])
    beste = None
    for h in hoteller():
        for m in MAT:
            if h['mat'] == 'Uten måltider' and m['id'] == 'halvpensjon':
                continue
            if h['mat'] != 'Uten måltider' and m['id'] == 'selvhushold':
                continue
            sum_ = h['kr'] + h['skatt'] + m['kr']
            if beste is None or sum_ < beste[0]:
                beste = (sum_, h, m)
    _, h, m = beste
    return dict(transfer=tra['id'], hotell=h['id'], mat=m['id'],
                akt=[a['id'] for a in AKTIVITETER if a['kr'] == 0],
                buffer='b0',
                sum=tra['kr'] + h['kr'] + h['skatt'] + m['kr'])
