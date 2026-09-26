# -*- coding: utf-8 -*-
"""kart_punkter.py — hvor kartet skal zoome når man klikker på et hotell eller en utflukt.

navn -> [breddegrad, lengdegrad, zoom]

Koordinatene er omtrentlige og peker på stedet, ikke på selve bygningen: for hoteller
er det kvartalet eller strandstrekningen, for utflukter selve attraksjonen. Det holder
til å vise hvor noe ligger, men skal ikke brukes til navigasjon.

Zoom: 15 = kvartal, 13 = by, 11 = område, 9 = hele øya eller regionen.
Navn som ikke står her får ingen zoom — da skjer ingenting ved klikk.
"""

PUNKT = {
    # --- Kreta, hoteller
    'Olympic Palladium':        [35.3690, 24.4790, 15],   # Rethymno by, 300 m fra stranda
    'Welcome Apts':             [35.3480, 24.2780, 14],   # Exopoli ved Georgioupolis
    'Theros':                   [35.3650, 24.5030, 14],   # 2,6 km øst for Rethymno sentrum
    'Galeana Beach':            [35.3760, 24.5450, 15],   # Platanes, på stranda
    'Akti Chara':               [35.3762, 24.5470, 15],   # Platanes, på stranda
    'Ariadne Rethymnon':        [35.3752, 24.5410, 15],   # Platanes, 280 m fra stranda
    # --- Kreta, utflukter
    'Rethymno':                 [35.3687, 24.4746, 14],   # gamlebyen og Fortezza
    'Knossos':                  [35.2980, 25.1630, 14],
    'Kournas-sjøen':            [35.3300, 24.2760, 14],
    'Chania':                   [35.5155, 24.0180, 14],   # den venetianske havna
    'Elafonisi':                [35.2710, 23.5400, 13],
    'Balos og Gramvousa':       [35.5820, 23.5860, 12],
    'Limnoupolis':              [35.4830, 23.9800, 14],   # badeland utenfor Chania
    'Preveli og Kournas':       [35.1540, 24.4700, 12],   # Preveli-stranda

    # --- Costa Blanca, hoteller
    'Albir Garden Resort':      [38.5720, -0.0690, 15],
    'Nacavi Albir Aparthotel':  [38.5705, -0.0665, 15],
    'Hotel Noguera El Albir':   [38.5690, -0.0615, 15],
    'Hotel Cap Negret':         [38.5880, -0.0700, 15],   # N-332 km 159, Altea
    'Albir Playa Hotel & Spa':  [38.5700, -0.0595, 15],
    'Hotel Kaktus Albir':       [38.5672, -0.0575, 15],
    # --- Costa Blanca, utflukter
    'Altea':                    [38.5990, -0.0520, 14],
    'Aqualandia':               [38.5470, -0.1050, 15],   # Benidorm
    'Algar-fossene':            [38.6430, -0.1195, 14],
    'Isla de Benidorm':         [38.5070, -0.1300, 13],
    'Guadalest':                [38.6760, -0.1960, 14],
    'Terra Mítica':             [38.5620, -0.1250, 14],
    'Guadalest og Algar':       [38.6600, -0.1580, 12],
    'Tabarca':                  [38.1650, -0.4790, 13],

    # --- Costa Brava, hoteller (Santa Susanna, 60 km nord for Barcelona)
    'SANTA SUSANNA Chic! Apartments by ALEGRIA': [41.6385, 2.7075, 15],
    'ALEGRIA Cartago Nova':     [41.6430, 2.7400, 15],   # Malgrat de Mar, ved stranda
    'Santa Susanna Resort Affiliated by FERGUS': [41.6350, 2.7175, 15],
    'Hostal Boutique Rivolto Rooms': [41.6375, 2.7110, 16],
    'AQUA Hotel Onabrava & Spa 4*Sup': [41.6330, 2.7065, 15],
    'AQUA Hotel Aquamarina & Spa': [41.6320, 2.7040, 15],
    'ALEGRIA Caprici Verd 4 SUP': [41.6335, 2.7095, 15],
    'ALEGRIA Florida & Spa':    [41.6318, 2.7020, 15],
    # --- Costa Brava, utflukter og steder
    'Santa Susanna':            [41.6360, 2.7130, 14],
    'Barcelona':                [41.3851, 2.1734, 12],
    'Sagrada Família':          [41.4036, 2.1744, 16],
    'Park Güell':               [41.4145, 2.1527, 15],
    'Tossa de Mar':             [41.7197, 2.9317, 14],
    'Water World':              [41.7133, 2.8352, 15],   # Carretera de Vidreres, Lloret de Mar
    'PortAventura og Ferrari Land': [41.0870, 1.1560, 13],
    'Marineland Catalunya':     [41.6620, 2.7500, 14],   # Palafolls
    'Calella':                  [41.6140, 2.6560, 14],
    'Blanes':                   [41.6740, 2.7910, 14],
    'Malgrat de Mar':           [41.6460, 2.7420, 14],

    # --- Split, hoteller
    'Design Hostel One':        [43.5085, 16.4400, 16],   # innenfor murene i gamlebyen
    'Plavi Horizont, Podstrana':[43.4870, 16.5520, 15],
    'Hotel Zagreb, Duilovo':    [43.4985, 16.4900, 15],
    'Hotel San Antonio':        [43.4880, 16.5530, 15],   # Grljevačka, Podstrana
    'Cora Hotel':               [43.5090, 16.4230, 15],   # Put Supavla
    'Hotel Atrium':             [43.5150, 16.4560, 15],
    # --- Split, utflukter
    'Krka nasjonalpark':        [43.8060, 15.9690, 13],   # Skradinski buk
    'Klis og kjellerne':        [43.5580, 16.5230, 14],   # festningen i Klis
    'Klis og Trogir':           [43.5370, 16.3900, 11],   # mellom Klis og Trogir
    'Brač':                     [43.2570, 16.6350, 12],   # Zlatni Rat ved Bol
    'Trogir':                   [43.5150, 16.2520, 15],
    'Diokletians palass':       [43.5081, 16.4402, 16],
    'Rafting i Cetina':         [43.4450, 16.6900, 13],   # Cetina-elva ved Omiš

    # --- Kreta, steder i «Dette finnes i området» og «I nærheten»
    'Bystranda i Rethymno og Platanes': [35.3760, 24.5200, 13],
    'Preveli':                  [35.1540, 24.4700, 14],
    'Damnoni':                  [35.1840, 24.4230, 15],
    'Balos':                    [35.5820, 23.5860, 12],
    'Falassarna':               [35.5000, 23.5740, 13],
    'Georgioupolis — med forbehold': [35.3600, 24.2670, 14],
    'Arkeologisk museum i Heraklion': [35.3395, 25.1355, 15],
    'Arkadi-klosteret':         [35.3090, 24.6280, 14],
    'Fortezza i Rethymno':      [35.3705, 24.4720, 16],
    'Gamlebyen i Rethymno':     [35.3690, 24.4750, 16],
    'Den venetianske havna i Chania': [35.5180, 24.0190, 16],
    'Aptera':                   [35.4620, 24.1400, 14],
    'Samaria-juvet':            [35.2800, 23.9600, 12],
    'Samaria-kløfta':           [35.2800, 23.9600, 12],
    'Imbros-juvet':             [35.2400, 24.1700, 13],
    'Limnoupolis vannpark':     [35.4830, 23.9800, 14],
    'Balos og Gramvousa med båt': [35.5820, 23.5860, 12],
    'Balos og Elafonisi':       [35.4200, 23.5600, 10],
    'Gokart i Varipetro':       [35.4790, 23.9930, 14],
    'Agreco-gården':            [35.3390, 24.5560, 14],
    'Folkloreopptoget i Chania': [35.5155, 24.0180, 15],
    'Renaissance-festivalen i Rethymno': [35.3690, 24.4750, 15],
    'Markedsdager':             [35.3690, 24.4790, 14],
    'Kvelden i gamlebyen':      [35.3688, 24.4745, 16],

    # --- Costa Blanca, steder
    'Albirstranda':             [38.5700, -0.0630, 15],
    'Playa de Levante i Benidorm': [38.5400, -0.1230, 15],
    'Cala del Tio Ximo og Cala Almadrava': [38.5460, -0.1030, 15],
    'Cala de Finestrat':        [38.5230, -0.1450, 15],
    'Strendene i Altea':        [38.5940, -0.0490, 14],
    'Villa Romana de l\'Albir': [38.5730, -0.0580, 16],
    'Turen til fyret':          [38.5620, -0.0480, 14],
    'Fyret på Serra Gelada':    [38.5620, -0.0480, 14],
    'Torre Bombarda':           [38.5690, -0.0520, 15],
    'Altea gamleby':            [38.5990, -0.0520, 16],
    'Altea og Benidorm':        [38.5700, -0.0900, 12],
    'Santa Bárbara-borgen i Alicante': [38.3490, -0.4770, 15],
    'Villajoyosa og sjokolademuseet': [38.5070, -0.2320, 14],
    'Terra Natura og Aqua Natura': [38.5450, -0.1400, 15],
    'Les Fonts de l\'Algar':    [38.6430, -0.1195, 14],
    'Cuevas del Canelobre':     [38.4700, -0.4270, 14],
    'Kajakk fra Albirstranda':  [38.5680, -0.0600, 15],
    'Søndagsmarkedet i Albir':  [38.5710, -0.0640, 15],
    'Filmfestivalen i l\'Alfàs del Pi': [38.5790, -0.1020, 14],
    'Norsk i Albir':            [38.5700, -0.0660, 15],
    'Hogueras de San Juan':     [38.3450, -0.4810, 13],

    # --- Split, steder
    'Bačvice':                  [43.5030, 16.4460, 15],
    'Picigin':                  [43.5030, 16.4460, 15],
    'Kašjuni':                  [43.5040, 16.4180, 15],
    'Žnjan':                    [43.4990, 16.4790, 15],
    'Strendene i Podstrana':    [43.4880, 16.5490, 14],
    'Omiš — Velika Plaža':      [43.4430, 16.6870, 14],
    'Brela':                    [43.3720, 16.9060, 14],
    'Zlatni Rat på Brač':       [43.2570, 16.6350, 14],
    'Øyene Brač og Hvar':       [43.2200, 16.5500, 10],
    'Katedralen sv. Duje':      [43.5082, 16.4404, 17],
    'Klis-festningen':          [43.5580, 16.5230, 14],
    'Salona':                   [43.5390, 16.4820, 14],
    'Marjan':                   [43.5090, 16.4200, 13],
    'Marjan og Bačvice':        [43.5060, 16.4330, 13],
    'Krka-fossene':             [43.8060, 15.9690, 13],
    'Rafting på Cetina':        [43.4450, 16.6900, 13],
    'Zipline i Omiš':           [43.4440, 16.6880, 14],
    'Havkajakk under Marjan':   [43.5060, 16.4150, 14],
    'Biokovo Skywalk':          [43.3130, 17.0450, 13],
    'Blå grotte og Hvar':       [43.1640, 16.4400, 11],
    'Middelhavets filmfestival': [43.5081, 16.4402, 15],
    'Pazar og fisketorget':     [43.5090, 16.4420, 16],
    'Rivaen':                   [43.5070, 16.4390, 16],
    'Kvelden — verdt å planlegge': [43.5081, 16.4402, 16],

    # --- Vings charteralternativer
    'Ilion Beach, uten måltider':  [35.5225, 23.8760, 15],
    'Ilion Beach med frokost':     [35.5225, 23.8760, 15],
    'Ilion Beach med halvpensjon': [35.5225, 23.8760, 15],
    'Waterman Supetrus, uten måltider':        [43.3850, 16.5480, 15],
    'Waterman Supetrus med frokost':            [43.3850, 16.5480, 15],
    'Waterman Supetrus med All Inclusive':      [43.3850, 16.5480, 15],
    'Supetar':                  [43.3833, 16.5500, 14],
    'Zlatni Rat':               [43.2570, 16.6350, 14],
    'Vidova Gora':              [43.2870, 16.6070, 13],
    'Split':                    [43.5081, 16.4402, 13],
    'Pučišća':                 [43.3450, 16.7280, 14],

    # «Fridag» og «Sove lenge» har ingen bestemt plass og får ingen zoom.
}
