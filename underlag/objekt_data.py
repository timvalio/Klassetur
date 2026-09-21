# -*- coding: utf-8 -*-
"""objekt_data.py — det som vises nederst til høyre når man klikker på noe i lista.

For hvert navn: hvilke bilder som hører til, hvilke punkter i «Dette finnes i området»
teksten og lenken skal hentes fra, og eventuelt en egen tekst.

Bildene er de samme Wikimedia-filene som allerede står i arkene, så fotograf og lisens
er kjent fra før (bildekreditt.py). Nøklene under er bare en bit av filnavnet — _f()
slår opp hele navnet og stopper bygget hvis nøkkelen treffer null eller flere filer.

Hotellene har vi ikke frie bilder av. Der viser vi et bilde av stedet rundt, tydelig
merket med at det ikke er hotellet, og lenker videre til hotellets egne bilder i
Google Maps. Legges det en jpg i underlag/bilder/hotell/, brukes den i stedet.
"""
import re
import omraade_data

_PAR = [(f, t) for d in omraade_data.OMRAADE.values() for tm in d['temaer'] for f, t in tm['bilder']]
_FILER = [f for f, _ in _PAR]
_TEKST = dict(_PAR)


def _f(nokkel):
    """Filnavnet som inneholder nøkkelen. Må treffe nøyaktig én fil.

    Er nøkkelen et helt filnavn (slutter på .jpg/.png), brukes det som det er — da er det
    et bilde vi har hentet fra Wikimedia selv, og som ikke står i arkene fra før."""
    if re.search(r'\.(jpe?g|png)$', nokkel, re.I):
        return nokkel
    treff = [f for f in _FILER if nokkel.lower() in f.lower()]
    if len(treff) != 1:
        raise KeyError('bildenøkkelen %r traff %d filer: %s' % (nokkel, len(treff), treff))
    return treff[0]


# Bildetekst for filene vi har hentet inn selv (de i arkene har sin egen fra før).
EGNE_TEKSTER = {
    'Cala de Finestrat, Finestrat, España, 2014-07-03, DD 01.JPG': 'Cala de Finestrat, finsand i en lukket bukt',
    'Cala La Almadrava, Benidorm, España, 2014-07-02, DD 75.JPG': 'Cala Almadrava nord for Benidorm',
    'Terra Natura - panoramio.jpg': 'Terra Natura i Benidorm',
    'Platanias near Rethymno, Crete 001.JPG': 'Stranda ved Platanes, øst for Rethymno',
    'Georgioupoli, Crete - panoramio.jpg': 'Georgioupolis',
    'Aptera - Thermen - Ruinen 2.jpg': 'De romerske badene i Aptera',
    'Imbros Gorge, Crete.jpg': 'Imbros-juvet',
    'Croatia Split beach Znjan panorama.jpg': 'Žnjan-stranda i Split',
    '2. SKYWALK (BIOKOVO).jpg': 'Skywalk-plattformen på Biokovo',
    'Bisevo blue cave - panoramio.jpg': 'Den blå grotta på Biševo',
    'Fruit at Pazar.jpg': 'Frukt på Pazar, torget i Split',
}


def bildetekst(fil):
    return EGNE_TEKSTER.get(fil) or _TEKST.get(fil, '')


# type: 'utflukt' | 'hotell' | 'sted'
# bilder:    bilder av selve stedet
# omrbilder: bilder av området rundt — brukes når vi ikke har bilde av objektet selv
# punkt:     navn i «Dette finnes i området» som teksten, fakta og lenken hentes fra
OBJEKT = {

# ---------------------------------------------------------------- Kreta, utflukter
'Rethymno': dict(type='utflukt', bilder=['8236', 'Rimondi', 'Rethymno, Alter Hafen'],
    punkt=['Gamlebyen i Rethymno', 'Fortezza i Rethymno']),
'Knossos': dict(type='utflukt', bilder=['Knossos R03', 'Bull leaping'],
    punkt=['Knossos', 'Arkeologisk museum i Heraklion']),
'Kournas-sjøen': dict(type='utflukt', bilder=['Kournas-See'], punkt=['Kournas-sjøen']),
'Chania': dict(type='utflukt', bilder=['Chania, Alter Hafen', 'Harbor, Venetian shipyards'],
    punkt=['Den venetianske havna i Chania']),
'Elafonisi': dict(type='utflukt', bilder=['Elafonisi'], punkt=['Elafonisi']),
'Balos og Gramvousa': dict(type='utflukt', bilder=['Balos 1'],
    punkt=['Balos', 'Balos og Gramvousa med båt']),
'Limnoupolis': dict(type='utflukt', punkt=['Limnoupolis vannpark']),
'Preveli og Kournas': dict(type='utflukt', bilder=['Palm Beach 03', 'Kournas-See'],
    punkt=['Preveli', 'Kournas-sjøen']),
'Samaria-kløfta': dict(type='sted', bilder=['Samaria'], punkt=['Samaria-juvet']),
'Balos og Elafonisi': dict(type='sted', bilder=['Balos 1', 'Elafonisi'], punkt=['Balos', 'Elafonisi']),

# ---------------------------------------------------------------- Costa Blanca, utflukter
'Altea': dict(type='utflukt', bilder=["Cúpula d'Altea", 'Altea, Spain (26889065385)'],
    punkt=['Altea gamleby', 'Strendene i Altea']),
'Aqualandia': dict(type='utflukt', omrbilder=['DD 33'], punkt=['Aqualandia'],
    omrtekst='Benidorm — Aqualandia ligger på høyden over Levante-stranda.'),
'Algar-fossene': dict(type='utflukt', bilder=['toll Blau', 'toll del Baladre'],
    punkt=["Les Fonts de l'Algar"]),
'Isla de Benidorm': dict(type='utflukt', bilder=['Isla de Benidorm, España', 'DD 86'],
    punkt=['Isla de Benidorm', 'Playa de Levante i Benidorm']),
'Guadalest': dict(type='utflukt', bilder=['DD 11', 'Castillo, Guadalest'], punkt=['Guadalest']),
'Terra Mítica': dict(type='utflukt', bilder=['Magnus_Colossus'], punkt=['Terra Mítica']),
'Guadalest og Algar': dict(type='utflukt', bilder=['DD 11', 'toll Blau'],
    punkt=['Guadalest', "Les Fonts de l'Algar"]),
'Tabarca': dict(type='utflukt', bilder=['Tabarca Island'], punkt=['Tabarca']),
'Altea og Benidorm': dict(type='sted', bilder=["Cúpula d'Altea", 'DD 86'],
    punkt=['Altea gamleby', 'Playa de Levante i Benidorm']),
'Fyret på Serra Gelada': dict(type='sted', bilder=['Faro de Punta Albir', 'Des de la Serra Gelada'],
    punkt=['Turen til fyret', 'Torre Bombarda']),

# ---------------------------------------------------------------- Split, utflukter
'Diokletians palass': dict(type='utflukt',
    bilder=['Aerial_view_of_Diocletian', 'Peristyle', 'Bell Tower Of Cathedral'],
    punkt=['Diokletians palass', 'Katedralen sv. Duje']),
'Krka nasjonalpark': dict(type='utflukt', bilder=['Skradinski Buk'], punkt=['Krka nasjonalpark']),
'Rafting i Cetina': dict(type='utflukt', bilder=['Rafting Cetina', 'Blue Eye'],
    punkt=['Rafting på Cetina', 'Zipline i Omiš']),
'Brač': dict(type='utflukt', bilder=['Zlatni Rat, Hvar'], punkt=['Zlatni Rat på Brač']),
'Klis og Trogir': dict(type='utflukt', bilder=['Fortress of Klis', 'from-NW'],
    punkt=['Klis-festningen', 'Trogir']),
'Klis og kjellerne': dict(type='utflukt', bilder=['Fortress of Klis', 'Peristyle'],
    punkt=['Klis-festningen', 'Diokletians palass']),
'Trogir': dict(type='utflukt', bilder=['from-NW', 'Panorama of Trogir'], punkt=['Trogir']),
'Marjan og Bačvice': dict(type='utflukt', bilder=['Marjana-Telegrin', 'Bacvice Beach', 'Picigolwiki'],
    punkt=['Marjan', 'Bačvice', 'Picigin']),
'Krka-fossene': dict(type='sted', bilder=['Skradinski Buk'], punkt=['Krka nasjonalpark']),
'Øyene Brač og Hvar': dict(type='sted', bilder=['Zlatni Rat, Hvar'],
    punkt=['Zlatni Rat på Brač', 'Blå grotte og Hvar']),

# ---------------------------------------------------------------- steder vi har hentet bilde til selv
'Cala de Finestrat': dict(type='sted', bilder=['Cala de Finestrat, Finestrat, España, 2014-07-03, DD 01.JPG']),
'Cala del Tio Ximo og Cala Almadrava': dict(type='sted', bilder=['Cala La Almadrava, Benidorm, España, 2014-07-02, DD 75.JPG']),
'Terra Natura og Aqua Natura': dict(type='sted', bilder=['Terra Natura - panoramio.jpg']),
'Bystranda i Rethymno og Platanes': dict(type='sted', bilder=['Platanias near Rethymno, Crete 001.JPG']),
'Georgioupolis — med forbehold': dict(type='sted', bilder=['Georgioupoli, Crete - panoramio.jpg']),
'Aptera': dict(type='sted', bilder=['Aptera - Thermen - Ruinen 2.jpg']),
'Imbros-juvet': dict(type='sted', bilder=['Imbros Gorge, Crete.jpg']),
'Žnjan': dict(type='sted', bilder=['Croatia Split beach Znjan panorama.jpg']),
'Biokovo Skywalk': dict(type='sted', bilder=['2. SKYWALK (BIOKOVO).jpg']),
'Blå grotte og Hvar': dict(type='sted', bilder=['Bisevo blue cave - panoramio.jpg', 'Zlatni Rat, Hvar']),
'Pazar og fisketorget': dict(type='sted', bilder=['Fruit at Pazar.jpg']),
'Havkajakk under Marjan': dict(type='sted', bilder=['Marjana-Telegrin']),
'Turen til fyret': dict(type='sted', bilder=['Faro de Punta Albir']),
# Omiš — Velika Plaža, Zipline i Omiš og Torre Bombarda star uten bilde med vilje:
# det eneste Omiš-bildet vi har er en iskrem, og fyrbildet viser ikke Torre Bombarda.

# ---------------------------------------------------------------- steder i omradet som mangler eget bilde
'Gamlebyen i Rethymno': dict(type='sted', bilder=['Rimondi', '8236']),
'Balos og Gramvousa med båt': dict(type='sted', bilder=['Balos 1']),
'Strendene i Altea': dict(type='sted', bilder=['Altea, Spain (26889065385)']),
'Kajakk fra Albirstranda': dict(type='sted', bilder=["Playa de l'Albir"]),
'Katedralen sv. Duje': dict(type='sted', bilder=['Bell Tower Of Cathedral', 'Vestibule']),
'Marjan': dict(type='sted', bilder=['Marjana-Telegrin']),

# ---------------------------------------------------------------- dager uten sted
'Fridag': dict(type='dag', tekst='Ingen felles utflukt. Stranda, byen og bassenget ligger der de ligger — '
    'dagen koster bare det den enkelte bruker. Der det står et beløp, er det satt av til lokalbuss og inngang.'),
'Sove lenge': dict(type='dag', tekst='Ingen felles utflukt om formiddagen. Beløpet som står, er lokalbuss '
    'til stranda og litt inngang, ikke en bestilt aktivitet.'),

# ---------------------------------------------------------------- hoteller, Kreta
'Olympic Palladium': dict(type='hotell', omrbilder=['Rethymno, Alter Hafen'],
    omrtekst='Rethymno — hotellet ligger i byen, 300 meter fra stranda.'),
'Welcome Apts': dict(type='hotell', omrbilder=['Kournas-See'],
    omrtekst='Kournas-sjøen ovenfor Georgioupolis, der leilighetene ligger.'),
'Theros': dict(type='hotell', omrbilder=['8239'],
    omrtekst='Rethymno fra festningsmurene. Theros ligger 2,6 km øst for sentrum.'),
'Galeana Beach': dict(type='hotell', omrbilder=['Rethymno, Alter Hafen'],
    omrtekst='Rethymno, fem kilometer vest for Platanes der hotellet ligger.'),
'Akti Chara': dict(type='hotell', omrbilder=['Rethymno, Alter Hafen'],
    omrtekst='Rethymno, fem kilometer vest for Platanes der hotellet ligger.'),
'Ariadne Rethymnon': dict(type='hotell', omrbilder=['Rethymno, Alter Hafen'],
    omrtekst='Rethymno, fem kilometer vest for Platanes der hotellet ligger.'),

# ---------------------------------------------------------------- hoteller, Costa Blanca
'Albir Garden Resort': dict(type='hotell', omrbilder=["Playa de l'Albir"],
    omrtekst='Albirstranda, et kvarters gange fra leilighetene.'),
'Nacavi Albir Aparthotel': dict(type='hotell', omrbilder=["Playa de l'Albir"],
    omrtekst='Albirstranda, noen minutter fra leilighetene.'),
'Hotel Noguera El Albir': dict(type='hotell', omrbilder=['Racó del Albir'],
    omrtekst='Racó del Albir, stranda nedenfor hotellet.'),
'Hotel Cap Negret': dict(type='hotell', omrbilder=["Cúpula d'Altea"],
    omrtekst='Altea — hotellet ligger på kysten to kilometer sør for gamlebyen.'),
'Albir Playa Hotel & Spa': dict(type='hotell', omrbilder=["Playa de l'Albir"],
    omrtekst='Albirstranda, rett over veien for hotellet.'),
'Hotel Kaktus Albir': dict(type='hotell', omrbilder=["Playa de l'Albir"],
    omrtekst='Albirstranda, et par minutter fra hotellet.'),

# ---------------------------------------------------------------- hoteller, Split
'Design Hostel One': dict(type='hotell', omrbilder=['Peristyle'],
    omrtekst='Peristylet i Diokletians palass — hostellet ligger innenfor de samme murene.'),
'Cora Hotel': dict(type='hotell', omrbilder=['City of Split Riva'],
    omrtekst='Rivaen i Split. Hotellet ligger vest for sentrum, ved Put Supavla.'),
'Hotel Atrium': dict(type='hotell', omrbilder=['City of Split Riva'],
    omrtekst='Rivaen i Split. Hotellet ligger i Poljička cesta, øst for sentrum.'),
'Plavi Horizont, Podstrana': dict(type='hotell', omrbilder=['Podstrana Split'],
    omrtekst='Kysten i Podstrana, der hotellet ligger.'),
'Hotel San Antonio': dict(type='hotell', omrbilder=['Podstrana Split'],
    omrtekst='Kysten i Podstrana, der hotellet ligger.'),
'Hotel Zagreb, Duilovo': dict(type='hotell', omrbilder=['Kasjuni'],
    omrtekst='Badebuktene under Marjan. Hotellet ligger i Duilovo, øst for sentrum.'),
}


def hent(navn):
    """Oppslaget som lag_kart.py bruker. Bildenøklene er byttet ut med hele filnavn."""
    o = OBJEKT.get(navn)
    if not o:
        return None
    ut = dict(o)
    ut['bilder'] = [_f(k) for k in o.get('bilder', [])]
    ut['omrbilder'] = [_f(k) for k in o.get('omrbilder', [])]
    return ut
