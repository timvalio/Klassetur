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

    # «Fridag» og «Sove lenge» har ingen bestemt plass og får ingen zoom.
}
