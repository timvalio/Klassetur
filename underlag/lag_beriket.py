# -*- coding: utf-8 -*-
"""Samler bilder, koordinater, beskrivelser og fasiliteter i beriket.py."""
import hashlib, json, urllib.parse, pathlib

# -------- hotellene: booking.com-bilder (id~signatur), beskrivelse og fasiliteter
RAA = json.loads(pathlib.Path('booking_raa.json').read_text(encoding='utf-8'))

# -------- koordinater, slått opp i Nominatim 14.11.2026 eller hentet fra kart_punkter.py
KOORD = {
    'safari':                        (41.61329, 2.65761, True),   # Calella sentrum
    'odissea-park':                  (41.63409, 2.72093, False),
    'sant-jordi-santa-susanna':      (41.63618, 2.72495, False),
    'santa-susanna-chic-apartments': (41.63850, 2.70750, False),
    'htopplanamar':                  (41.64018, 2.73663, False),
    'haromar':                       (41.61065, 2.65156, False),
    'president-calella':             (41.61470, 2.65113, False),
    'boutique-rivolto-rooms':        (41.63750, 2.71100, False),
    'internacional':                 (41.61329, 2.65761, True),   # Calella sentrum
    'alhambra':                      (41.63563, 2.72433, False),
    'reymar-playa':                  (41.64591, 2.74141, True),   # Malgrat sentrum
    'hotel-maritim':                 (41.61148, 2.65378, False),
    'mar-blau-calella':              (41.61419, 2.65119, False),
    'aqua-aquamarina':               (41.63200, 2.70400, False),
    'alegria-florida-park':          (41.63180, 2.70200, False),
    'aqua-onabrava':                 (41.63300, 2.70650, False),
}

AKT_KOORD = {
    'strand':       (41.63573, 2.70659),
    'sagrada':      (41.40350, 2.17443),
    'bcn-tog':      (41.38510, 2.17340),
    'guell':        (41.41423, 2.15246),
    'illafantasia': (41.50289, 2.36371),
    'marineland':   (41.66113, 2.75383),
    'waterworld':   (41.70737, 2.82762),
    'portaventura': (41.08696, 1.15858),
    'tossa':        (41.71677, 2.93403),
}

BASIS = (41.63573, 2.70659)   # Santa Susanna

# -------- Wikimedia Commons: filnavn, fotograf, lisens
COMMONS = {
 'strand': [('Playa de Santa Susanna (2).JPG', 'Alberto-g-rovi', 'CC BY-SA 4.0', 'Stranda i Santa Susanna'),
            ('Playa de Santa Susanna (3).JPG', 'Alberto-g-rovi', 'CC BY-SA 4.0', 'Stranda i Santa Susanna'),
            ('Platja de les Dunes, 1.jpg', 'Isidro Jabato', 'CC BY-SA 4.0', 'Platja de les Dunes i Santa Susanna')],
 'sagrada': [('Simetría na Sagrada Familia. Barcelona B30.jpg', 'Luis Miguel Bugallo Sánchez', 'CC BY-SA 3.0', 'Sagrada Família innvendig'),
             ('Sagrada Familia, Barcelona (P1170693).jpg', 'Matti Blume', 'CC BY-SA 4.0', 'Sagrada Família utvendig')],
 'bcn-tog': [('Barcelona - Passeig de Gràcia - Casa Amatller & Casa Batlló.jpg', 'Txllxt TxllxT', 'CC BY-SA 4.0', 'Casa Batlló og Casa Amatller på Passeig de Gràcia'),
             ('Platja de la Barceloneta 2018.jpg', 'Nicholas Gemini', 'CC BY-SA 4.0', 'Bystranda Barceloneta'),
             ('Barcelona - Barri Gotic. Carrer dels Arcs.jpg', 'Fred Romero', 'CC BY 2.0', 'Gotikerkvarteret i Barcelona'),
             ("Estació d'Arenys de Mar 05 2018.jpg", '9pm', 'CC BY-SA 4.0', 'R1-toget, samme linje som går fra Santa Susanna')],
 'guell': [('Park Güell - cafe terrace 01.jpg', 'Joe Mabel', 'CC BY-SA 4.0', 'Park Güell'),
           ('Terrace of Parc Güell, Barcelona, Spain.jpg', 'Julian Lupyan', 'CC0', 'Terrassen i Park Güell')],
 'illafantasia': [('Slides.jpg', 'Illa Fantasia', 'CC BY-SA 4.0', 'Sklier i Illa Fantasia'),
                  ('Laberint pirata.jpg', 'Illa Fantasia', 'CC0', 'Piratområdet i Illa Fantasia')],
 'marineland': [('Delphinarium Marineland Catalogne.jpg', 'Olivier Duquesne', 'CC BY-SA 2.0', 'Delfinshowet i Marineland Catalunya'),
                ('Parc aquatique marineland Catalogne.jpg', 'Olivier Duquesne', 'CC BY-SA 2.0', 'Vannparken på samme billett'),
                ('Toboggan Marineland Catalogne.jpg', 'Olivier Duquesne', 'CC BY-SA 2.0', 'Sklie i vannparken')],
 'waterworld': [],
 'portaventura': [('Shambhala in the top (76 meters).JPG', 'Sotti', 'CC0', 'Shambhala på toppen, 76 meter over bakken'),
                  ('Dragon Khan Big Vertical Loop.jpg', 'Sotti', 'CC0', 'Dragon Khan gjennom den store loopen'),
                  ('Shambhala Splash.JPG', 'Sotti', 'CC0', 'Shambhala gjennom vannet'),
                  ("Vue d'ensemble de ferrari land.jpg", 'Ahs 34000', 'CC BY-SA 4.0', 'Ferrari Land, som ligger vegg i vegg')],
 'tossa': [('Costa Brava - Tossa de Mar - La Vila Vella - Plaça Pintor Roig Soler - View NNW.jpg', 'Txllxt TxllxT', 'CC BY-SA 4.0', 'Vila Vella i Tossa de Mar'),
           ("Costa Brava - Tossa de Mar - La Vila Vella - Passeig del Mar - View ENE towards 14th century Torre d'en Joanàs & Portal (Passeig de la Vila Vella).jpg", 'Txllxt TxllxT', 'CC BY-SA 4.0', 'Bymuren i Tossa de Mar')],
}


def commons_url(navn, bredde=1280):
    n = navn.replace(' ', '_')
    h = hashlib.md5(n.encode('utf-8')).hexdigest()
    q = urllib.parse.quote(n)
    return (f'https://upload.wikimedia.org/wikipedia/commons/thumb/'
            f'{h[0]}/{h[0:2]}/{q}/{bredde}px-{q}')


def _py(j):
    return j.replace(': true', ': True').replace(': false', ': False')


def main():
    hot = {}
    for slug, v in RAA.items():
        la, lo, omtrent = KOORD[slug]
        hot[slug] = dict(
            koord=[la, lo], omtrentlig=omtrent,
            beskrivelse=' '.join(v['d'].split()).strip(),
            fasiliteter=v['f'],
            bilder=[f'https://cf.bstatic.com/xdata/images/hotel/max1024x768/{b.split("~")[0]}.jpg?k={b.split("~")[1]}'
                    for b in v['b']])
    akt = {}
    for k, liste in COMMONS.items():
        akt[k] = [dict(url=commons_url(n), tittel=t, fotograf=f, lisens=l) for n, f, l, t in liste]

    ut = pathlib.Path('beriket.py')
    ut.write_text(
        '# -*- coding: utf-8 -*-\n'
        '"""Bilder, koordinater, beskrivelser og fasiliteter.\n\n'
        'Hotellbilder, beskrivelser og fasiliteter er hentet fra booking.com 14.11.2026.\n'
        'Aktivitetsbilder er fra Wikimedia Commons med fotograf og lisens oppgitt.\n'
        'Koordinater er slått opp i Nominatim; omtrentlig=True betyr at bare stedet\n'
        'er funnet, ikke selve bygningen.\n"""\n\n'
        'BASIS = ' + repr(list(BASIS)) + '\n\n'
        'HOTELL = ' + _py(json.dumps(hot, ensure_ascii=False, indent=1)) + '\n\n'
        'AKT_KOORD = ' + json.dumps({k: list(v) for k, v in AKT_KOORD.items()}, ensure_ascii=False, indent=1) + '\n\n'
        'AKT_BILDER = ' + json.dumps(akt, ensure_ascii=False, indent=1) + '\n',
        encoding='utf-8')
    print('skrev beriket.py —', len(hot), 'hoteller,', sum(len(v) for v in akt.values()), 'aktivitetsbilder')


if __name__ == '__main__':
    main()
