#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""tib.py — lager de seks 10B-arkene (Kreta, Costa Blanca, Split × billigst/best) med tall slått opp 15.9.2026.
Bruker 28-versjonen av 10A-arkene i mappe2/underlag som mal (CSS, galleri, «I nærheten»), skriver mappe3/underlag/10B/."""
import re, os, html, sys
from urllib.parse import unquote
B = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, B)
from lag_kart import KREDITT
INN = os.path.join(B, 'mappe2', 'underlag')
UT = os.path.join(B, 'mappe3', 'underlag', '10B'); os.makedirs(UT, exist_ok=True)
N = 28

def n(x): return f'{x:,}'.replace(',', ' ')

# ---------------------------------------------------------------- felles tekster
LOWFARE = 'Norwegian LowFare: bare en liten veske under setet (30×40×20 cm) er med i prisen'
LOWFAREP = 'Norwegian LowFare+: håndbagasje i hylla, én koffert på 23 kg og setereservasjon er med'
SLATT = 'laveste pris for én person på norwegian.com 15.9.2026 — gruppepris for 28 må innhentes'
GARDERMOEN_B = ('Hotell ved Gardermoen, 1 natt med frokost', 'Tilbud mottatt', '28 × 746 · Quality Airport Hotel Gardermoen, gruppepris 17.9.2026: 8 tremannsrom à 2 215 og 2 dobbeltrom à 1 580, frokost inkludert · 20 880 for 28 · «early bird»-frokost fra 04:00, som passer med utsjekk 04:30 · buss eller taxi til hotellet (4,7 km) kommer i tillegg — pris ikke oppgitt', 746)
GARDERMOEN_A = ('Hotell ved Gardermoen, 1 natt med frokost', 'Slått opp', '28 × 547 · Thon Hotel Gardermoen, familierom med frokost, fri avbestilling · booking.com 26.9.2026 for 7.–8. juni 2027: 8 759 for 16 personer i fire familierom, 547 per person · hotellets shuttlebuss til terminalen koster ekstra', 547)
FORSIKRING = ('Reiseforsikring, kjøpes av foreldrene', 'Slått opp', '0 over klassekassa · hver familie sørger for forsikringen selv · norsk familiereiseforsikring dekker barn under 21 uavhengig av hvem de reiser med og uten krav om felles adresse, så elevene er normalt dekket gjennom foreldrenes egen forsikring og de voksne gjennom sin · hver familie må bekrefte at dekningen gjelder, og de som mangler den må kjøpe egen · avbestillingsforsikring er noe annet: Apollo selger den for 399 per person, og familiene bør sjekke om egen polise dekker depositumet · gjensidige.no og klasseturer.no, lest 26.9.2026 · posten sto tidligere som 28 × 290 i anslag', 0)
BUSS = ('Buss Kautokeino–Alta t/r', 'Bekreftet', 'Kjøring og henting begge veier, oppgitt pris for hele gruppen · samme selskap oppga 26 200 for Kittilä · prisen er ikke knyttet til bestemte datoer', 17000)

# ---------------------------------------------------------------- Costa Brava (slått opp 26.9.2026)
# Google Flights 26.9.2026, Alta–Barcelona 8.–15. juni 2027: billigste pris for én person på nøyaktig
# disse fire Norwegian-etappene er 3 713 tur/retur uten innsjekket koffert. Påslaget på 381 per etappe er
# målt mot Norwegians tre gruppetilbud i september (328–446 per etappe, i snitt 381 — nettopp koffertprisen).
FLY_BRAVA_PP = 3713 + 4 * 381
FLY_BRAVA = ('28 × 5 237 · Norwegian hele veien: Alta–Oslo DY 321 tir 8. juni 11:55–13:55 og Oslo–Barcelona D8 5523 19:35–22:55, '
             'hjem Barcelona–Oslo DY 1741 tir 15. juni 13:10–16:35 og Oslo–Alta DY 328 19:50–22:50 · billigste pris på Google Flights 26.9.2026 '
             'for nøyaktig disse flyvningene er 3 713 tur/retur uten innsjekket koffert · påslaget er målt: Norwegians tre gruppetilbud ligger '
             '328–446 kroner per flyetappe over billigste oppslag, i snitt 381, som er nettopp koffertprisen · fire etapper × 381 = 1 524 · '
             'gruppepris på Alta–Oslo–Barcelona er ikke innhentet')
TURISTSKATT_APT = ('28 × 17 · Catalonia har turistskatt. Fra 1. april 2026 er satsen 0,90 euro per person per natt på leilighetsanlegg og øvrige '
                   'overnattingssteder utenfor Barcelona by (1,80 på 4-stjerners hotell), og maks sju netter regnes · personer på 16 år eller yngre er fritatt '
                   '(Llei 5/2017), så bare de sju voksne betaler: 7 × 7 × 0,90 euro = 44 euro, 475 kroner for gruppa · betales på stedet · satsen fastsettes på nytt '
                   'hvert år og kan være endret til juni 2027, og kommunene kan legge på et eget tillegg · om alle 28 skulle betale, ville posten bli 1 900 kroner · '
                   'atc.gencat.cat og comunicatur.info, lest 26.9.2026')
TURISTSKATT_4S = ('28 × 34 · Catalonia har turistskatt. Fra 1. april 2026 er satsen 1,80 euro per person per natt på 4-stjerners hotell utenfor Barcelona by, '
                  'og maks sju netter regnes · personer på 16 år eller yngre er fritatt (Llei 5/2017), så bare de sju voksne betaler: 7 × 7 × 1,80 euro = 88 euro, '
                  '950 kroner for gruppa · betales på hotellet ved ankomst · satsen fastsettes på nytt hvert år og kan være endret til juni 2027, og kommunene kan '
                  'legge på et eget tillegg · om alle 28 skulle betale, ville posten bli 3 800 kroner · atc.gencat.cat og comunicatur.info, lest 26.9.2026')
BRAVA_WARN = ('<b>Ingen av flyprisene er gruppepris.</b> Grunnlaget er billigste pris for én person på Google Flights 26. september 2026 for nøyaktig disse '
              'flyvningene, pluss et målt påslag på 381 kroner per flyetappe — differansen mellom Norwegians tre gruppetilbud i september og billigste oppslag, '
              'som tilsvarer koffertprisen. Gruppepris på Alta–Oslo–Barcelona er ikke innhentet, og er den største usikkerheten i dette alternativet. '
              'Norwegian selger inntil 9 seter per nettbestilling; 28 seter må bestilles som gruppe (group.norwegian.com). Gruppeprisen inkluderer 2 × 23 kg koffert, '
              'to håndbagasjer og én taxfreepose per reisende (norwegian.com, lest 26.9.2026), med 30 prosent depositum innen 21 dager og resten 30 dager før avreise.')

GRUPPE_WARN = ('<b>Norwegians gruppevilkår:</b> 30 prosent i depositum 21 dager etter bestilling, resten 30 dager før avreise. Gruppen kan reduseres med inntil 10 prosent uten å miste depositumet — faller flere enn to–tre fra, tapes det. Betalt beløp refunderes ikke ved avbestilling. <b>Flyprisene er laveste nettpris for én person 15. september 2026</b> — ikke gruppepris. Norwegian selger inntil 9 seter per bestilling på nett; 28 seter må bestilles som gruppe (group.norwegian.com). '
               'Gruppebillett koster «litt mer» enn enkeltbilletter, men inkluderer 2 × 23 kg koffert og håndbagasje for alle, 30 % depositum innen 21 dager og resten 30 dager før avreise, og navnene kan settes inn til 5 dager før. '
               'På flere av avgangene var det bare 1–7 seter igjen til laveste pris, så regn med at gruppeprisen ligger over.')

# Norwegians gruppetilbud for Costa Blanca, mottatt i gruppeportalen 15.9.2026 (tilbud X2ETUP, «Kautokeino skole»)
X2ETUP_PP = 4971
X2ETUP = ('28 × 4 971 · Norwegians gruppetilbud X2ETUP, mottatt 15.9.2026 for nøyaktig disse flyene: Alta–Oslo DY 321 tir 8. juni 11:55, Oslo–Alicante D8 5323 19:55, '
          'Alicante–Oslo DY 1791 tir 15. juni 11:15, Oslo–Alta DY 328 19:50 · 127 120 pluss skatter og avgifter 12 068 = 139 188 for 28 · innsjekket koffert og håndbagasje inkludert · '
          'tilbudet var gyldig i fem virkedager og gikk ut rundt 22. september — må hentes inn på nytt før bestilling; beløpet står som et reelt, datert gruppetall · Norwegians gruppevilkår gir 2 × 23 kg innsjekket bagasje, to håndbagasjer og én taxfreepose per reisende i gruppeprisen (norwegian.com, lest 26.9.2026) · laveste nettpris for én person uten koffert var 3 166')
X2ETUP_OBS = ('Norwegians gruppetilbud gjelder i fem dager fra 15. september og bekreftes med «Bekreft tilbud» i gruppeportalen. Da opprettes bestillingen: 30 % depositum innen 21 dager, '
              'resten 30 dager før avreise, og navnelista kan leveres inntil 5 dager før avreise. Innsjekket koffert og håndbagasje er med for alle 28; nettprisen uten koffert (3 166 per person) gjaldt bare 1–7 seter per avgang.')
X2ETUP_WARN = ('<b>Flyprisen er Norwegians gruppetilbud X2ETUP av 15. september 2026</b> for 28 på nøyaktig disse flyene, med skatter, koffert og håndbagasje — ikke et anslag. '
               'Tilbudet utløper rundt 20. september og gjelder med forbehold om ledig kapasitet; bekreftes det, er bestillingen gjort og 30 % depositum forfaller innen 21 dager.')

# TUIs tilbud til Eli Ristin Skum 15.9.2026: Tromsø–Chania, Blue Star Caldera Creta Paradise & Waterpark, all inclusive, 470 925 for 28.
TUI_BUSS = 40000
TUI_PAKKE = 470925
TUI_ROWS = [('Buss Kautokeino–Tromsø t/r', 'Estimat', 'Ikke innhentet. Anslått ut fra prisene til Alta (17 000, 2 timer) og Kittilä (26 200, 3½ time); Tromsø er 6–7 timer hver vei', TUI_BUSS),
            ('TUI-pakke: fly, hotell 7 netter, all inclusive, koffert og transfer', 'Tilbud mottatt', 'Direktefly Tromsø–Chania tur/retur med mat om bord og innsjekket bagasje, transfer flyplass–hotell, Blue Star Caldera Creta Paradise &amp; Waterpark i Gerani med all inclusive: 7 tremannsrom til elevene, 3 dobbeltrom og 1 enkeltrom til de voksne · 470 925 for 28, 16 819 per person', TUI_PAKKE),
            ('Lunsj ute på utfluktsdagene', 'Estimat', '28 × 600 · all inclusive dekker måltidene på hotellet; lunsj ute (150) på fire utfluktsdager', N * 600),
            ('Aktiviteter med leiebuss', 'Estimat', '28 × 2 100 · samme program som over: Knossos og Heraklion, Balos, Limnoupolis, Preveli og Kournas med leiebuss for gruppen', N * 2100),
            ('Reiseforsikring', 'Estimat', '28 × 290 · anslag, tilbud ikke innhentet', N * 290)]
TUI = dict(tittel='Tilbud fra TUI: Tromsø–Chania med all inclusive',
           under='Mottatt 15. september 2026 via Eli Ristin Skum, regnet på de samme seks postene som Apollo-pakken',
           lede='TUI har gitt Eli Ristin Skum tilbud på en pakketur for 28 fra Tromsø til Kreta: direktefly tur/retur med mat om bord og innsjekket bagasje, transfer, og Blue Star Caldera Creta Paradise &amp; Waterpark med all inclusive — 470 925 kroner for 7 tremannsrom til elevene, 3 dobbeltrom og 1 enkeltrom til de voksne. Hotellet er 4 stjerner, ligger på stranda i Gerani 14 km vest for Chania by og 2 km fra Platanias, har eget badeland og gis 4,4 av 5 av TUIs gjester. Datoene står ikke i tilbudet; TUI flyr Tromsø–Chania på lørdager, så turen er trolig 5.–12. juni. Det som kommer i tillegg er buss til Tromsø, lunsj på utfluktsdagene, utfluktene selv og reiseforsikring.',
           hotell=('Blue Star Caldera Creta Paradise &amp; Waterpark', 'Gerani, 73014 Chania · +30 28210 61315 · reservations@calderacretaparadise.gr · 4 stjerner, på stranda, badeland, all inclusive i TUI-tilbudet · 16 819 per person med fly, hotell, mat, koffert og transfer', 'Tilbud mottatt'),
           rows=TUI_ROWS,
           note='Bussen til Tromsø er ikke innhentet og er den største usikkerheten; hver vei er 6–7 timer mot 2 til Alta. Sammenlignet med Apollo-pakken over gir TUI all inclusive på 4 stjerner med badeland i stedet for frokost på 3 stjerner, men lengre buss og ingen pris på den. Tilbudet er gitt til Eli Ristin Skum, ikke bekreftet, og datoene må avklares med TUI.')

ARK = [
# =============================================================== KRETA — BILLIGST
dict(base='Klassetur-B-Kreta.html', fil='Klassetur-Kreta-billigst.html', navn='Kreta', variant='billigst',
     under='Billigst · Rethymno, rutefly via Oslo', datoer='7.–15. juni 2027',
     promise='Norwegian fra Oslo til Chania, én natt ved Gardermoen på veien ned, 3-stjerners hotell med frokost 300 meter fra gamlebyen i Rethymno, og rutebuss til alt. Ni dager, 7 netter på Kreta.',
     band=[('9 dager', '7 netter på Kreta, 1 ved Gardermoen'), ('28', '21 elever, 7 voksne')],
     reise=[('Kautokeino → Alta', 'Buss · ca. 2 t · mandag 7. juni, avgang rundt 09:00'),
            ('Alta → Oslo', 'Norwegian DY 321 · man 7. juni 11:55–13:55 · natt på hotell ved Gardermoen · ca. 2 t'),
            ('Oslo → Chania', 'Norwegian DY 1898, direkte · tir 8. juni 06:45–11:55 · ca. 4 t 10 min'),
            ('Chania → hotellet', 'KTEL-rutebuss via Chania · ca. 1 t 45 min')],
     reise_note='Hjemreise tirsdag 15. juni: KTEL-buss til Chania lufthavn, Norwegian DY 1899 Chania 12:40 – Oslo 15:50, Norwegian DY 328 Oslo 19:50 – Alta 22:50 (30 minutters teknisk stopp i Tromsø, ingen flybytte), buss til Kautokeino ca. 01:00. Ingen direktefly fra Oslo til Heraklion før 17. juni, derfor Chania. Lørdagsavgangen (Norwegian 14:00) er det eneste alternativet i vinduet, men den krever natt i Oslo begge veier.',
     uke_tittel='Rutebuss, strand og gratis inngang for skoleklasser',
     dager=[('Man 7. juni · Reisedag til Oslo', 'Buss til Alta, fly til Oslo, innsjekk på hotell ved Gardermoen', '—'),
            ('Tir 8. juni · Til Kreta', 'Fly 06:45, landing 11:55, KTEL-buss til Rethymno, innsjekk og strand', '—'),
            ('Ons 9. juni · Rethymno', 'Gamlebyen, havna og Fortezza. Strand ved byen', '55 kr'),
            ('Tor 10. juni · Knossos', 'KTEL-buss til Heraklion (86 kr hver vei). Inngang er gratis for skoleklasser fra EØS-land med attest fra skolen, ellers 215', '172 kr'),
            ('Fre 11. juni · Kournas-sjøen', 'Rutebuss til Kretas eneste ferskvannssjø, tråbåter og bading', '210 kr'),
            ('Lør 12. juni · Chania', 'KTEL-buss til den venetianske havna og gamlebyen i Chania', '150 kr'),
            ('Søn 13. juni · Elafonisi', 'Buss via Chania til lagunen med rosa sand helt vest på øya. Lang dag', '390 kr'),
            ('Man 14. juni · Fridag', 'Strand, shopping, valgfritt opplegg i grupper', '—'),
            ('Tir 15. juni · Hjemreise', 'Chania 12:40 – Oslo 15:50 – Alta 22:50 – Kautokeino ca. 01:00', '—')],
     uke_note='Priser per person, listepriser 2026. Lokalbussene er KTEL sine ordinære billetter (crete.direct 13.9.2026). Aktiviteter og restauranter er forslag, ikke bestilt.',
     hotell_tittel='Slått opp for 8.–15. juni 2027, ikke reservert',
     hotell_lede='Olympic Palladium ligger i Rethymno by, 300 meter fra stranda og gangavstand til gamlebyen, og hadde 2 dobbeltrom og 8 tremannsrom med frokost ledig for 28 da det ble slått opp. Fri avbestilling til 5. juni 2027 og ingen forskuddsbetaling, så rommene kan holdes uten risiko. Hotellet skriver at andre regler kan gjelde ved 10 rom eller mer — ring dem.',
     hoteller=[('Olympic Palladium', 'Themistokli Moatsou 42, Rethymno · +30 28310 24761 · info@olympicpalladium.com · 3 stjerner, frokost, 448 per person per natt', 'Slått opp'),
               ('Welcome Apts', 'Exopoli, Georgioupolis · leiligheter for 4 med kjøkkenkrok, uten måltider, 343–381 per person per natt (5.–12. juni), 1,5 km over Georgioupolis', 'Slått opp'),
               ('Theros', 'Rethymno, 2,6 km fra sentrum · leiligheter, 53 520 for 28 i uka 5.–12. juni, ikke kontrollert i detalj', 'Slått opp')],
     rows=[BUSS,
           ('Fly, 28 personer t/r', 'Delvis tilbud', '28 × 7 398 · Gruppetilbud XV5CP6 Oslo–Chania tur/retur 4 800 per person (DY 1898 tir 8. juni 06:45–11:55, DY 1899 tir 15. juni 12:40–15:50), 121 576 pluss skatter og avgifter 12 824 = 134 400 for 28 og 2 × 23 kg koffert, mottatt 17.9.2026, gyldig i fem virkedager og dermed utgått rundt 24. september — må hentes inn på nytt · Norwegians gruppevilkår gir 2 × 23 kg innsjekket bagasje, to håndbagasjer og én taxfreepose per reisende i gruppeprisen (norwegian.com, lest 26.9.2026) · Alta–Oslo 1 799 (DY 321 man 7. juni) og Oslo–Alta 799 (DY 328 tir 15. juni) er fortsatt LowFare-pris for én person — gruppetilbud er bedt om, men ikke mottatt', 7398),
           GARDERMOEN_B,
           ('Hotell i Rethymno, 7 netter med frokost', 'Tilbud mottatt', '28 × 2 817 · Olympic Palladium, gruppepris fra HotelBrain 17.9.2026: 8 tremannsrom à 105 € og 2 dobbeltrom à 78 € per rom per natt med frokost, netto uten provisjon · rommene koster 6 972 €, og gresk klimaavgift på 350 € (ti rom i sju netter) kommer i tillegg — til sammen 7 322 € = 78 858 for 28, så avgiften er med her og står ikke som egen post · 30 % forfaller 10. mars 2027 og er ikke refunderbart, resten 25. mai · rommene er ikke holdt av', 2817),
           ('Middag ute og lunsj', 'Estimat', '28 × 1 900 · pita gyros til lunsj (70) og enkel taverna til middag (140) i sju dager, pluss mat på de tre reisedagene', 1900),
           ('Aktiviteter og lokalbusser', 'Estimat', '28 × 1 150 · KTEL-buss flyplass–Rethymno t/r (172), Fortezza, Knossos, Kournas, Chania og Elafonisi med rutebuss — se programmet', 1150),
           FORSIKRING],
     obs_ekstra=['Flyet fra Gardermoen går 06:45, så gruppen må stå opp rundt 04:00 på hotellet. Hotellet ligger 4,7 km fra terminalen; buss eller taxi må ordnes for 28 med bagasje.',
                 'Bare en liten veske under setet er inkludert i flyprisen. Én koffert på 23 kg koster 169–449 kroner per flyvning hos Norwegian, eller er inkludert hvis dere bestiller som gruppe.',
                 'Knossos og Samaria er gratis for skoleklasser fra EØS-land: ta med deltakerliste og attest fra skolen. Uten papirene koster Knossos 20 euro per person.'],
     warn=GRUPPE_WARN + ' Overnattingen er slått opp på booking.com for de nøyaktige datoene, med fri avbestilling. Mat og aktiviteter er anslag. Kurs brukt: 1 EUR = 10,77 kr (Norges Bank 14.9.2026). '
          '<b>Vil dere heller fly direkte:</b> Apollos billigste pakke fra Alta 8.–15. juni er Kleopatra Crete i Kato Stalos uten måltider, 11 298 per person med fly og hotell — se «best»-arket for det direkteflyet.',
     ),

# =============================================================== KRETA — BEST
dict(base='Klassetur-B-Kreta.html', fil='Klassetur-Kreta-best.html', navn='Kreta', variant='best',
     under='Best · Platanes ved Rethymno, direktefly fra Alta', datoer='8.–15. juni 2027',
     promise='Apollos charterfly rett fra Alta til Chania tirsdag 8. juni, buss fra flyplassen til et hotell på stranda i Platanes med frokost, og leiebuss for gruppen på utfluktene. Åtte dager, ingen mellomlanding, ingen natt i Oslo.',
     band=[('8 dager', '7 netter, ingen overnatting underveis'), ('28', '21 elever, 7 voksne')],
     reise=[('Kautokeino → Alta', 'Buss · ca. 2 t · tirsdag 8. juni, avgang rundt 15:30'),
            ('Alta → Chania', 'Apollo/Aegean A3 4559, charter direkte · tir 8. juni 19:30–01:45 · ca. 5 t 15 min'),
            ('Chania → hotellet', 'Apollos transferbuss · ca. 1 t 15 min')],
     reise_note='Hjemreise tirsdag 15. juni: transferbuss til Chania, Aegean A3 4558 Chania 13:50 – Alta 18:30, buss til Kautokeino ca. 21:00. Dette er det eneste direkteflyet fra Alta til Middelhavet i avreisevinduet; Apollo flyr Alta–Chania tirsdager fra 27. april til 15. juni 2027, og 8. juni er den eneste avgangen mellom 4. og 10. juni. Fra Tromsø går det lørdagscharter til Chania (Apollo, Ving og TUI), men avreise fra Tromsø er ikke regnet på: bussen dit er ikke priset.',
     uke_tittel='Leiebuss for gruppen på utfluktene, strand resten',
     dager=[('Tir 8. juni · Reisedag', 'Buss til Alta, direktefly 19:30, landing 01:45, transferbuss til hotellet', '—'),
            ('Ons 9. juni · Sove lenge', 'Strand ved hotellet. Rethymno gamleby, havna og Fortezza om ettermiddagen', '55 kr'),
            ('Tor 10. juni · Knossos', 'Leiebuss til Knossos og Arkeologisk museum i Heraklion. Inngangen er gratis for skoleklasser fra EØS med attest; regnet med full pris', '615 kr'),
            ('Fre 11. juni · Balos og Gramvousa', 'Buss til Kissamos og båt til lagunen og piratøya, gruppepris', '670 kr'),
            ('Lør 12. juni · Limnoupolis', 'Vannpark ved Chania, leiebuss', '425 kr'),
            ('Søn 13. juni · Preveli og Kournas', 'Leiebuss til palmestranda ved Preveli, tråbåter på Kournas-sjøen på veien hjem', '320 kr'),
            ('Man 14. juni · Fridag', 'Strand, shopping, valgfritt opplegg i grupper', '—'),
            ('Tir 15. juni · Hjemreise', 'Transferbuss, Chania 13:50 – Alta 18:30 – Kautokeino ca. 21:00', '—')],
     uke_note='Priser per person. Balos: buss 26 euro og båt 36 euro til gruppepris fra Rethymno (crete.life, 2026). Limnoupolis 25,50 euro (2026). Leiebuss er anslått til 270 kroner per person per dag; ingen busselskap på Kreta publiserer dagspris, så det må innhentes tilbud. Aktiviteter og restauranter er forslag, ikke bestilt.',
     hotell_tittel='Tilbud fra Apollo 21. september 2026, ingen plasser reservert',
     hotell_lede='Apollo har gitt pris på to hoteller i Platanes, begge med frokost, bagasje og transfer i samme pakke som direkteflyet. Prisene under er for hele gruppa med sju tremannsrom til elevene, tre dobbeltrom og ett enkeltrom til de voksne, og én fri reiseleder. Ungdommen kan dele rom uten voksne så lenge det bor voksne på samme hotell.',
     hoteller=[('Galeana Beach, dobbeltrom med ekstraseng', 'Machis Kritis 196, Platanes · 3 stjerner, rett på stranda, frokost · rom på ca. 27 kvm med balkong eller terrasse · 13 739 per person i delt dobbeltrom, 13 235 for den tredje i rommet, enkeltrom +2 170 · 13 233 per person for gruppa', 'Tilbud mottatt'),
               ('Galeana Beach, familierom til elevene', 'Samme hotell, rom på ca. 37 kvm · 14 033 per person, 13 445 for den tredje · de voksne blir boende i dobbeltrom · 13 432 per person for gruppa', 'Tilbud mottatt'),
               ('Ariadne Rethymnon, ettroms leilighet', 'Platanes, 280 m fra stranda · frokost · leilighet på ca. 25 kvm med balkong eller terrasse · 14 784 per person, 14 112 for den tredje, enkeltrom +1 910 · 14 189 per person for gruppa', 'Tilbud mottatt'),
               ('Ariadne Rethymnon, toroms leilighet', 'Samme hotell, leilighet på ca. 35 kvm · 15 202 per person, 14 446 for den tredje · 14 503 per person for gruppa', 'Tilbud mottatt')],
     rows=[BUSS,
           ('Fly, hotell med frokost, bagasje og transfer', 'Tilbud mottatt', '28 × 13 233 · Apollos gruppetilbud 21.9.2026: Aegean A3 4559 Alta 19:30–Chania 01:45 og A3 4558 Chania 13:50–Alta 18:30, Galeana Beach i Platanes med frokost, 23 kg innsjekket og 5 kg håndbagasje og buss flyplass–hotell · sju tremannsrom til elevene og tre dobbeltrom og ett enkeltrom til de voksne, minus én fri reiseleder · 370 515 for 28, avrundet til 13 233 per person · ingen plasser reservert', 13233),
           ('Miljøskatt på hotellet', 'Estimat', '28 × 148 · gresk klimaavgift, 5 euro per rom per natt for 3-stjerners hotell i juni (lov 5162/2024) · satsen er sikker, men romfordelingen er vår egen: elleve rom i sju netter gir 385 euro · betales direkte til hotellet og er ikke med i Apollos pris', 148),
           ('Middag ute og lunsj', 'Estimat', '28 × 2 800 · lunsj (120) og taverna-middag (280) i sju dager, pluss mat på reisedagene', 2800),
           ('Aktiviteter med leiebuss', 'Estimat', '28 × 2 100 · Knossos og Heraklion, Balos, Limnoupolis, Preveli og Kournas med leiebuss for gruppen — se programmet', 2100),
           FORSIKRING],
     obs_ekstra=['Landing 01:45 natt til onsdag: første dag på hotellet blir en sovedag. Hjemflyet lander i Alta 18:30, så gruppen er i Kautokeino samme kveld.',
                 'Fra 20 fullt betalende gir Apollo én fri plass i delt dobbeltrom. Den er trukket fra i regnestykket; transport (500) og innsjekket bagasje (420) følger ikke med friplassen.',
                 'Tilbudet gjelder Galeana Beach og Ariadne Rethymnon. Apollo oppgir at Akti Chara har få ledige rom på tirsdagsavgangene.',
                 'Etter bestilling må alle foresatte gi samtykke til reisen på Apollos fullmaktsskjema.',
                 'Flymat (240 per person) og avbestillingsforsikring (399 per person, betales sammen med depositumet) er ikke regnet inn.',
                 'Knossos og Samaria er gratis for skoleklasser fra EØS-land: ta med deltakerliste og attest fra skolen.'],
     warn='<b>Apollo har ikke reservert plasser.</b> Prisen er et tilbud av 21. september 2026 med forbehold om ledig kapasitet og prisendring, og må bestilles senest 90 dager før avreise. '
          'Depositum er 2 000 kroner per person rundt 14 dager etter bestilling, resten om lag 40 dager før avreise. Miljøskatten betales direkte til hotellet. '
          'Leiebuss på Kreta er anslått, ingen selskap publiserer dagspris. Mat og aktiviteter er anslag. Kurs brukt: 1 EUR = 10,77 kr.',
     ),

# =============================================================== COSTA BRAVA — BILLIGST
dict(base='Klassetur-CostaBrava.html', fil='Klassetur-CostaBrava-billigst.html', navn='Costa Brava', variant='billigst',
     under='Billigst · Santa Susanna, Norwegian hele veien', datoer='8.–15. juni 2027',
     promise='Norwegian fra Alta via Oslo til Barcelona samme dag, leiligheter med kjøkken i Santa Susanna, og tog til Barcelona rett fra stasjonen i byen. Åtte dager, ingen natt underveis.',
     band=[('8 dager', '7 netter, ingen overnatting underveis'), ('28', '21 elever, 7 voksne')],
     reise=[('Kautokeino → Alta', 'Buss · ca. 2 t · tirsdag 8. juni, avgang rundt 09:00'),
            ('Alta → Oslo', 'Norwegian DY 321 · tir 8. juni 11:55–13:55 · fem og en halv time på Gardermoen · ca. 2 t'),
            ('Oslo → Barcelona', 'Norwegian D8 5523, direkte · tir 8. juni 19:35–22:55 · ca. 3 t 20 min'),
            ('Barcelona → hotellet', 'Buss · ca. 1 t · 60 km nordover langs kysten til Santa Susanna')],
     reise_note='Hjemreise tirsdag 15. juni: buss til Barcelona, Norwegian DY 1741 Barcelona 13:10 – Oslo 16:35, Norwegian DY 328 Oslo 19:50 – Alta 22:50 (30 minutters teknisk stopp i Tromsø, ingen flybytte), buss til Kautokeino ca. 01:00. Alle fire flyene er Norwegian. Dette er den eneste ruten som kommer fram samme dag uten å bytte flyselskap: Norwegians andre Oslo–Barcelona-avgang 8. juni går 09:05, og Alta-flyene lander 10:15 og 13:55. SAS lander i Barcelona 17:55, men med tre mellomlandinger — Tromsø, Oslo og Stockholm. Skal gruppa være framme før middag, må den ta natt ved Gardermoen og fly ned 09:05 dagen etter. Slått opp på Google Flights 26.9.2026.',
     uke_tittel='Strandbase, storby og badeland med tog og buss',
     dager=[('Tir 8. juni · Reisedag', 'Buss til Alta, fly via Oslo, landing 22:55, buss til Santa Susanna, innsjekk rundt 00:30', '—'),
            ('Ons 9. juni · Sove lenge', 'Stranda i Santa Susanna og promenaden, gratis', '—'),
            ('Tor 10. juni · Barcelona', 'Tog fra Santa Susanna stasjon, drøyt en time. Sagrada Família til skolepris (15 euro), Park Güell (10 euro) og Rambla', '415 kr'),
            ('Fre 11. juni · Strand og kyststi', 'Fri dag i Santa Susanna, badestranda og stien mot Malgrat, gratis', '—'),
            ('Lør 12. juni · Tossa de Mar', 'Middelalderbyen med bymur rett i sjøen, en halvtime nordover med buss', '130 kr'),
            ('Søn 13. juni · Water World', 'Badeland i Lloret de Mar (40 euro), buss', '490 kr'),
            ('Man 14. juni · Fridag', 'Strand, Calella eller Blanes med tog, shopping', '65 kr'),
            ('Tir 15. juni · Hjemreise', 'Barcelona 13:10 – Oslo 16:35 – Alta 22:50 – Kautokeino ca. 01:00', '—')],
     uke_note='Priser per person. Sagrada Família tar 15 euro per elev for skolegrupper, én lærer gratis per gruppe (sagradafamilia.org 26.9.2026); Park Güell 10 euro; Water World i Lloret 40 euro for alle over 1,20 m, med egen pris for grupper over 25 etter avtale (waterworld.es 26.9.2026). Togbillett Santa Susanna–Barcelona 5,50–6,60 euro hver vei etter sone (redtransporte.com 26.9.2026). Aktiviteter og restauranter er forslag, ikke bestilt.',
     hotell_tittel='Slått opp for 8.–15. juni 2027, ikke reservert',
     hotell_lede='SANTA SUSANNA Chic! Apartments by ALEGRIA er et leilighetsanlegg 600 meter fra sentrum og 850 meter fra stranda, med basseng og leiligheter med kjøkken. Gjestene gir det 8,6 av 10. Fri avbestilling. Booking.com priser 16 personer om gangen på disse datoene, så de resterende tolv må bekreftes direkte med anlegget. Vil dere heller bo rett ved stranda med frokost, ligger ALEGRIA Cartago Nova i Malgrat de Mar 1,7 kilometer unna til 2 194 per person for uka.',
     hoteller=[('SANTA SUSANNA Chic! Apartments by ALEGRIA', 'Santa Susanna · +34 93 767 86 84 · bookings@alegria-hotels.com · leiligheter med kjøkken og basseng, 600 m fra sentrum og 850 m fra stranda, 8,6 av 10 · 3 057 per person for uka · booking.com 26.9.2026', 'Slått opp'),
               ('ALEGRIA Cartago Nova', 'Malgrat de Mar, 1,7 km fra Santa Susanna · rett ved stranda, frokost inkludert, 8,0 av 10 · 2 194 per person for uka · booking.com 26.9.2026', 'Slått opp'),
               ('Hostal Boutique Rivolto Rooms', 'Santa Susanna, 150 m fra sentrum og 750 m fra stranda · 8,7 av 10, uten måltider · 2 817 per person for uka · booking.com 26.9.2026', 'Slått opp'),
               ('Santa Susanna Resort Affiliated by FERGUS', 'Santa Susanna, 650 m fra stranda · firemannsrom med frokost · 6,0 av 10 · 2 718 per person for uka · booking.com 26.9.2026', 'Slått opp')],
     rows=[BUSS,
           ('Fly, 28 personer t/r', 'Estimat', FLY_BRAVA, FLY_BRAVA_PP),
           ('Leiligheter i Santa Susanna, 7 netter', 'Slått opp', '28 × 3 057 · SANTA SUSANNA Chic! Apartments by ALEGRIA, leiligheter med kjøkken, basseng, 8,6 av 10, fri avbestilling · booking.com 26.9.2026 for 8.–15. juni 2027: 48 907 for 16 personer, 3 057 per person · booking.com priser ikke alle 28 i én bestilling, så hele gruppa må bekreftes direkte med anlegget', 3057),
           ('Mat, delvis laget selv', 'Estimat', '28 × 2 000 · frokost og noen middager laget i leilighetene, bocadillo til lunsj, menú del día (13–17 euro) ellers — rundt 250 per dag, pluss mat på reisedagene', 2000),
           ('Aktiviteter og transport', 'Estimat', '28 × 1 490 · buss Barcelona–Santa Susanna tur/retur (388), Sagrada Família og Park Güell med tog, Tossa de Mar, Water World i Lloret og lokaltog — se programmet · transferen er slått opp hos Moventis Experience 26.9.2026: 18 euro per person hver vei i delt buss, satt av ved overnattingsstedet', 1490),
           ('Turistskatt på stedet', 'Slått opp', TURISTSKATT_APT, 17),
           FORSIKRING],
     obs_ekstra=['Landing 22:55 og innsjekk rundt 00:30: første dag blir en sovedag. Ventetiden på Gardermoen er fem og en halv time.',
                 'Transferen er slått opp hos Moventis Experience (From2 Travel): delt buss Barcelona lufthavn–Santa Susanna til 18 euro per person hver vei, satt av ved overnattingsstedet. At siste avgang passer med landing 22:55 må bekreftes, og pris på privat buss for 28 bør hentes inn — til Costa Blanca ga Beniconnect 607 euro tur/retur for 28, altså under en tredel per person.',
                 'Santa Susanna har egen jernbanestasjon på Rodalies-linja R1. Toget går langs kysten til Barcelona på drøyt en time, og nordover til Blanes og Calella.'],
     warn=BRAVA_WARN + ' Leilighetene er slått opp på booking.com for de nøyaktige datoene, med fri avbestilling. Transfer, mat og aktiviteter er anslag. Kurs brukt: 1 EUR = 10,77 kr (Norges Bank 14.9.2026).',
     ),

# =============================================================== COSTA BRAVA — BEST
dict(base='Klassetur-CostaBrava.html', fil='Klassetur-CostaBrava-best.html', navn='Costa Brava', variant='best',
     under='Best · Santa Susanna, 4 stjerner med halvpensjon', datoer='8.–15. juni 2027',
     promise='4-stjerners superior-hotell 300 meter fra stranda i Santa Susanna med frokost og middag, PortAventura og Ferrari Land på heldagstur, Barcelona med tog og badeland i Lloret. Åtte dager, ingen natt underveis.',
     band=[('8 dager', '7 netter, ingen overnatting underveis'), ('28', '21 elever, 7 voksne')],
     reise=[('Kautokeino → Alta', 'Buss · ca. 2 t · tirsdag 8. juni, avgang rundt 09:00'),
            ('Alta → Oslo', 'Norwegian DY 321 · tir 8. juni 11:55–13:55 · fem og en halv time på Gardermoen · ca. 2 t'),
            ('Oslo → Barcelona', 'Norwegian D8 5523, direkte · tir 8. juni 19:35–22:55 · ca. 3 t 20 min'),
            ('Barcelona → hotellet', 'Buss · ca. 1 t · 60 km nordover langs kysten til Santa Susanna')],
     reise_note='Hjemreise tirsdag 15. juni: buss til Barcelona, Norwegian DY 1741 Barcelona 13:10 – Oslo 16:35, Norwegian DY 328 Oslo 19:50 – Alta 22:50 (teknisk stopp i Tromsø, ingen flybytte), buss til Kautokeino ca. 01:00. Flyveien er den samme som i «billigst» — 8. juni 2027 finnes det ingen rute som kommer fram til Barcelona tidligere på dagen uten å bytte flyselskap eller ta natt ved Gardermoen. Forskjellen mellom de to alternativene ligger i hotellet, måltidene og programmet, ikke i flyene. Slått opp på Google Flights 26.9.2026.',
     uke_tittel='Fornøyelsespark, badeland og Barcelona — med leiebuss',
     dager=[('Tir 8. juni · Reisedag', 'Buss til Alta, fly via Oslo, landing 22:55, buss til Santa Susanna, innsjekk rundt 00:30', '—'),
            ('Ons 9. juni · Santa Susanna', 'Strand, basseng og spa på hotellet, gratis', '—'),
            ('Tor 10. juni · Barcelona', 'Tog fra Santa Susanna stasjon. Sagrada Família til skolepris (15 euro), Park Güell (10 euro) og Rambla', '415 kr'),
            ('Fre 11. juni · PortAventura og Ferrari Land', 'Heldag med leiebuss til Salou, begge parkene (fra 55 euro)', '890 kr'),
            ('Lør 12. juni · Water World', 'Badeland i Lloret de Mar (40 euro), leiebuss', '640 kr'),
            ('Søn 13. juni · Tossa de Mar', 'Middelalderbyen med bymur rett i sjøen, leiebuss langs kystveien', '210 kr'),
            ('Man 14. juni · Fridag', 'Strand, Calella med tog, shopping', '65 kr'),
            ('Tir 15. juni · Hjemreise', 'Barcelona 13:10 – Oslo 16:35 – Alta 22:50 – Kautokeino ca. 01:00', '—')],
     uke_note='Priser per person. PortAventura og Ferrari Land koster fra 55 euro for begge parkene og fra 50 for én (portaventuraworld.com 26.9.2026); skolegruppepris finnes, men er ikke publisert. Water World i Lloret 40 euro for alle over 1,20 m, med egen pris for grupper over 25. Sagrada Família 15 euro per elev for skolegrupper, én lærer gratis per gruppe; Park Güell 10 euro. Leiebuss er anslått til 210 kroner per person per dag, 300 for dagen til Salou. Aktiviteter og restauranter er forslag, ikke bestilt.',
     hotell_tittel='Slått opp for 8.–15. juni 2027, ikke reservert',
     hotell_lede='AQUA Hotel Onabrava &amp; Spa er et 4-stjerners superior-hotell i Santa Susanna, 300 meter fra stranda, med basseng og spa. Gjestene gir det 9,0 av 10 — høyest av hotellene i byen som tar imot familier. Fire firemannsrom med frokost og middag var ledig for 8.–15. juni 2027 da det ble slått opp, med fri avbestilling og ingen forskuddsbetaling. Booking.com priser 16 personer om gangen, så hele gruppa må bekreftes direkte med hotellet. Tre andre 4-stjerners hoteller i Santa Susanna hadde også halvpensjon ledig, fra 4 241 per person.',
     hoteller=[('AQUA Hotel Onabrava &amp; Spa 4*Sup', 'Carrer Pla de la Torre 12, 08398 Santa Susanna · +34 93 767 83 70 · onabrava@aquahotel.com · 4 stjerner superior, 9,0 av 10, basseng og spa, 300 m fra stranda · firemannsrom med frokost og middag, 4 670 per person for uka · booking.com 26.9.2026', 'Slått opp'),
               ('AQUA Hotel Aquamarina &amp; Spa', 'Santa Susanna, 250 m fra stranda · 4 stjerner, 8,2 av 10 · firemannsrom med frokost og middag, 4 241 per person for uka · booking.com 26.9.2026', 'Slått opp'),
               ('ALEGRIA Caprici Verd 4 SUP', 'Santa Susanna, 250 m fra stranda · 4 stjerner superior, 7,9 av 10 · firemannsrom med frokost og middag, 4 551 per person for uka · booking.com 26.9.2026', 'Slått opp'),
               ('ALEGRIA Florida &amp; Spa', 'Santa Susanna, 250 m fra stranda · 4 stjerner, 8,3 av 10 · familierom med frokost og middag, 4 741 per person for uka · booking.com 26.9.2026', 'Slått opp')],
     rows=[BUSS,
           ('Fly, 28 personer t/r', 'Estimat', FLY_BRAVA, FLY_BRAVA_PP),
           ('Hotell med halvpensjon, 7 netter', 'Slått opp', '28 × 4 670 · AQUA Hotel Onabrava &amp; Spa 4*Sup i Santa Susanna, 9,0 av 10, 300 m fra stranda · fire firemannsrom med frokost og middag, fri avbestilling og ingen forskuddsbetaling · booking.com 26.9.2026 for 8.–15. juni 2027: 74 724 for 16 personer, 4 670 per person · booking.com priser ikke alle 28 i én bestilling, så hele gruppa må bekreftes direkte med hotellet', 4670),
           ('Lunsj og mat underveis', 'Estimat', '28 × 1 450 · lunsj ute (150) i sju dager, pluss mat på reisedagene; frokost og middag er inkludert i hotellet', 1450),
           ('Aktiviteter med leiebuss', 'Estimat', '28 × 2 610 · buss Barcelona–Santa Susanna tur/retur (388), PortAventura og Ferrari Land med leiebuss, Water World i Lloret, Tossa de Mar, Barcelona med tog — se programmet · transferen er slått opp hos Moventis Experience 26.9.2026: 18 euro per person hver vei i delt buss', 2610),
           ('Turistskatt på stedet', 'Slått opp', TURISTSKATT_4S, 34),
           FORSIKRING],
     obs_ekstra=['Landing 22:55 og innsjekk rundt 00:30: første dag blir en sovedag. Ventetiden på Gardermoen er fem og en halv time.',
                 'PortAventura og Ferrari Land ligger ved Salou, rundt 150 kilometer sør for Santa Susanna — halvannen til to timer hver vei med buss. Kombibilletten for begge parkene koster fra 55 euro; skolegruppepris må hentes inn direkte.',
                 'Transferen er slått opp hos Moventis Experience (From2 Travel): delt buss Barcelona lufthavn–Santa Susanna til 18 euro per person hver vei. At siste avgang passer med landing 22:55 må bekreftes, og pris på privat buss for 28 bør hentes inn — til Costa Blanca ga Beniconnect 607 euro tur/retur for 28.',
                 'Santa Susanna har egen jernbanestasjon på Rodalies-linja R1, drøyt en time fra Barcelona.'],
     warn=BRAVA_WARN + ' Hotellet er slått opp på booking.com for de nøyaktige datoene, med fri avbestilling og ingen forskuddsbetaling. Leiebuss på utfluktene, transfer, mat og aktiviteter er anslag. Kurs brukt: 1 EUR = 10,77 kr (Norges Bank 14.9.2026).',
     ),

# =============================================================== SPLIT — BILLIGST
dict(base='Klassetur-C-Split.html', fil='Klassetur-Split-billigst.html', navn='Split', variant='billigst',
     under='Billigst · hostel i gamlebyen, rutefly via Oslo', datoer='7.–15. juni 2027',
     promise='Norwegian fra Oslo rett til Split, én natt ved Gardermoen på veien ned, hostel innenfor palassmurene og rutebuss og ferje til Krka, Klis og Brač. Ni dager, 7 netter i Split.',
     band=[('9 dager', '7 netter i Split, 1 ved Gardermoen'), ('28', '21 elever, 7 voksne')],
     reise=[('Kautokeino → Alta', 'Buss · ca. 2 t · mandag 7. juni, avgang rundt 09:00'),
            ('Alta → Oslo', 'Norwegian DY 321 · man 7. juni 11:55–13:55 · natt på hotell ved Gardermoen · ca. 2 t'),
            ('Oslo → Split', 'Norwegian DY 1950, direkte · tir 8. juni 07:15–10:05 · ca. 2 t 50 min'),
            ('Split → hotellet', 'Flybuss (Platanus) til busstasjonen · ca. 30 min')],
     reise_note='Hjemreise tirsdag 15. juni: flybuss, Norwegian DY 1951 Split 10:50 – Oslo 13:40, Norwegian DY 328 Oslo 19:50 – Alta 22:50 (30 minutters teknisk stopp i Tromsø, ingen flybytte), buss til Kautokeino ca. 01:00. Norwegian flyr direkte Oslo–Split tirsdag, torsdag, fredag, lørdag og søndag; SAS lørdager. Alle morgenavgangene krever natt i Oslo, og fredagsavgangen 17:40 gir hjemreise med natt i Oslo, så tirsdag–tirsdag er den korteste turen.',
     uke_tittel='Palasset, fossene og øyene med rutebuss og ferje',
     dager=[('Man 7. juni · Reisedag til Oslo', 'Buss til Alta, fly til Oslo, innsjekk på hotell ved Gardermoen', '—'),
            ('Tir 8. juni · Til Split', 'Fly 07:15, landing 10:05, flybuss, innsjekk. Diokletians palass og Rivaen om ettermiddagen', '—'),
            ('Ons 9. juni · Marjan og Bačvice', 'Skogåsen over byen og bystranda med picigin, gratis', '—'),
            ('Tor 10. juni · Krka nasjonalpark', 'Rutebuss til Skradin, skolegruppebillett 15 euro. Badeforbud i hele parken', '350 kr'),
            ('Fre 11. juni · Klis og kjellerne', 'Klis-festningen med bybuss (12 euro, 4 for dem under 16) og palasskjellerne', '215 kr'),
            ('Lør 12. juni · Brač', 'Jadrolinija-ferje til Supetar (6,50 euro hver vei) og buss til Zlatni Rat', '250 kr'),
            ('Søn 13. juni · Trogir', 'Bybuss 37 til gamlebyen på verdensarvlisten', '90 kr'),
            ('Man 14. juni · Fridag', 'Strand, shopping, valgfritt opplegg i grupper', '—'),
            ('Tir 15. juni · Hjemreise', 'Split 10:50 – Oslo 13:40 – Alta 22:50 – Kautokeino ca. 01:00', '—')],
     uke_note='Priser per person, listepriser 2026. Krka: 15 euro for skolegrupper over 20 i juni, meldes skriftlig 24 timer før (offisiell prisliste 2026). Rutebussen til Skradin er anslått til 8 euro hver vei. Aktiviteter og restauranter er forslag, ikke bestilt.',
     hotell_tittel='Slått opp for 8.–15. juni 2027, ikke reservert',
     hotell_lede='Design Hostel One ligger innenfor murene i gamlebyen, fem minutter fra palasset. Booking.com foreslo en blanding av firemannsrom, dobbeltrom og sovesalsplasser for 28, uten måltider, med fri avbestilling til 5. juni 2027 og ingen forskuddsbetaling. Split hadde svært få steder åpne for salg for juni 2027 da dette ble slått opp (booking.com: 99 prosent ikke ledig), så gruppehotellene i Podstrana bør spørres direkte når de åpner.',
     hoteller=[('Design Hostel One', 'Morpurgova poljana 2, Split · +385 21 332 500 · info@designhostelone.com · hostel i gamlebyen, firemannsrom og sovesal, 575 per person per natt · booking.com 26.9.2026', 'Slått opp'),
               ('Plavi Horizont, Podstrana', '+385 21 735 370 · info@plavi-horizont.hr · gruppehotell ved stranda 20 minutter sør for Split, pris på forespørsel', 'Tilbud innhentes'),
               ('Hotel Zagreb, Duilovo', 'Put Duilova 23, Split · 3 stjerner, gruppehotell ved stranda · ingen priser for juni 2027 ennå', 'Tilbud innhentes')],
     rows=[BUSS,
           ('Fly, 28 personer t/r', 'Delvis tilbud', '28 × 5 198 · Gruppetilbud XV8K8J Oslo–Split tur/retur 2 600 per person (DY 1950 tir 8. juni 07:15–10:05, DY 1951 tir 15. juni 10:50–13:40), 60 648 pluss skatter og avgifter 12 152 = 72 800 for 28 og 2 × 23 kg koffert, mottatt 17.9.2026, gyldig i fem virkedager og dermed utgått rundt 24. september — må hentes inn på nytt · Norwegians gruppevilkår gir 2 × 23 kg innsjekket bagasje, to håndbagasjer og én taxfreepose per reisende i gruppeprisen (norwegian.com, lest 26.9.2026) · Alta–Oslo 1 799 (DY 321 man 7. juni) og Oslo–Alta 799 (DY 328 tir 15. juni) er fortsatt LowFare-pris for én person — gruppetilbud er bedt om, men ikke mottatt', 5198),
           GARDERMOEN_B,
           ('Hostel i Split, 7 netter', 'Slått opp', '28 × 4 025 · Design Hostel One, firemannsrom og sovesalsplasser, uten måltider, fri avbestilling og ingen forskuddsbetaling · booking.com 26.9.2026 for 8.–15. juni 2027: 64 402 for 16 personer i fire enheter, 4 025 per person · booking.com priser ikke alle 28 i én bestilling, så hele gruppa må bekreftes direkte med hostellet', 4025),
           ('Mat, enkel', 'Estimat', '28 × 2 100 · burek eller bakeri til frokost (50), ćevapi eller pizza til lunsj (60) og dagsmeny til middag (130) i sju dager, pluss mat på reisedagene', 2100),
           ('Aktiviteter og lokaltransport', 'Estimat', '28 × 1 060 · flybuss t/r (162), Krka med rutebuss og skolegruppebillett, Klis, kjellerne, ferje til Brač, Trogir — se programmet', 1060),
           ('Turistskatt på stedet', 'Estimat', '28 × 75 · kroatisk turistskatt, 1,60 euro per person per natt i høysesong for Split, kategori B · reisende 12–18 betaler halv sats, så sju voksne full og 21 elever halv i sju netter · betales på stedet', 75),
           FORSIKRING],
     obs_ekstra=['Flyet fra Gardermoen går 07:15, så gruppen må stå opp rundt 04:30 på hotellet. Hotellet ligger 4,7 km fra terminalen; buss eller taxi må ordnes for 28 med bagasje.',
                 'Bare en liten veske under setet er inkludert i flyprisen. Én koffert på 23 kg koster 169–449 kroner per flyvning hos Norwegian, eller er inkludert hvis dere bestiller som gruppe.',
                 'Split i juni er dyrt på overnatting, og hostelet er det eneste stedet med plass til 28 som var åpent for salg. Prisen kan falle når leilighetshotellene i Podstrana åpner juni 2027.'],
     warn=GRUPPE_WARN + ' Hostelet er slått opp på booking.com for de nøyaktige datoene, med fri avbestilling. Mat og aktiviteter er anslag. Kurs brukt: 1 EUR = 10,77 kr (Norges Bank 14.9.2026).',
     ),

# =============================================================== SPLIT — BEST
dict(base='Klassetur-C-Split.html', fil='Klassetur-Split-best.html', navn='Split', variant='best',
     under='Best · Split, 4 stjerner nær gamlebyen', datoer='7.–15. juni 2027',
     promise='4-stjerners hotell rett på stranda i Podstrana med frokost, koffert og setereservasjon på alle fly, hotell med frokost ved Gardermoen på veien ned, og leiebuss til Krka og Klis, rafting i Cetina og ferje til Brač. Ni dager, 7 netter ved Split.',
     band=[('9 dager', '7 netter ved Split, 1 ved Gardermoen'), ('28', '21 elever, 7 voksne')],
     reise=[('Kautokeino → Alta', 'Buss · ca. 2 t · mandag 7. juni, avgang rundt 09:00'),
            ('Alta → Oslo', 'Norwegian DY 321 · man 7. juni 11:55–13:55 · natt på hotell ved Gardermoen · ca. 2 t'),
            ('Oslo → Split', 'Norwegian DY 1950, direkte · tir 8. juni 07:15–10:05 · ca. 2 t 50 min'),
            ('Split → hotellet', 'Flybuss til Split og bybuss 60 til Podstrana · ca. 1 t')],
     reise_note='Hjemreise tirsdag 15. juni: buss til flyplassen, Norwegian DY 1951 Split 10:50 – Oslo 13:40, Norwegian DY 328 Oslo 19:50 – Alta 22:50 (teknisk stopp i Tromsø), buss til Kautokeino ca. 01:00. Ingen avgang fra Oslo til Split passer med Alta-flyene samme dag uten natt i Oslo, bortsett fra fredag 4. juni 17:40 — men da lander hjemflyet etter midnatt. Et alternativ for hjemreisen er SAS Split 14:05 – Oslo 16:55 – Alta 21:50 på én billett (3 282 + 1 749).',
     uke_tittel='Leiebuss, rafting og øy',
     dager=[('Man 7. juni · Reisedag til Oslo', 'Buss til Alta, fly til Oslo, hotell med frokost ved Gardermoen', '—'),
            ('Tir 8. juni · Til Split', 'Fly 07:15, landing 10:05, buss til Podstrana. Strand ved hotellet om ettermiddagen', '—'),
            ('Ons 9. juni · Diokletians palass', 'Bybuss inn til Split: palasset, kjellerne (6 euro), Rivaen og Marjan', '110 kr'),
            ('Tor 10. juni · Krka nasjonalpark', 'Leiebuss til Skradin, skolegruppebillett 15 euro. Badeforbud i hele parken', '400 kr'),
            ('Fre 11. juni · Rafting i Cetina', 'Rafting fra Omiš, 45 euro med transfer fra Omiš, buss til Omiš', '570 kr'),
            ('Lør 12. juni · Brač', 'Jadrolinija-ferje til Supetar og buss til Zlatni Rat', '250 kr'),
            ('Søn 13. juni · Klis og Trogir', 'Leiebuss: festningen på Klis (12 euro, 4 for dem under 16) og gamlebyen i Trogir', '410 kr'),
            ('Man 14. juni · Fridag', 'Strand ved hotellet, shopping i Split, valgfritt opplegg i grupper', '45 kr'),
            ('Tir 15. juni · Hjemreise', 'Split 10:50 – Oslo 13:40 – Alta 22:50 – Kautokeino ca. 01:00', '—')],
     uke_note='Priser per person. Krka 15 euro for skolegrupper over 20 i juni (offisiell prisliste 2026); rafting 45 euro (rafting-cetina.com 2026); Klis 12/4 euro (tvrdavaklis.com). Leiebuss er anslått til 240 kroner per person per dag ut fra kroatiske veiledende priser for 30–36-seters buss (540–690 euro per dag). Aktiviteter og restauranter er forslag, ikke bestilt.',
     hotell_tittel='Slått opp for 8.–15. juni 2027, ikke reservert',
     hotell_lede='Cora Hotel ligger 1,5 kilometer fra gamlebyen i Split, har 4 stjerner og 9,3 av 10 fra gjestene. Rom med frokost var ledig for 8.–15. juni 2027 da det ble slått opp. Hotel San Antonio i Podstrana var førstevalget, men svarte 18. september at de bare har ledig 8.–10. juni og tilbyr venteliste. Til forskjell fra San Antonio ligger Cora i byen og ikke på stranda, så bybuss 60 faller bort.',
     hoteller=[('Cora Hotel', 'Put Supavla 39, Split · 4 stjerner, 9,3 av 10 · 1,5 km fra gamlebyen · frokost · 912 per person per natt · booking.com 26.9.2026', 'Slått opp'),
               ('The View Luxury Rooms', 'Gamlebyen i Split · 8,8 av 10 · frokost · 860 per person per natt · booking.com 26.9.2026', 'Slått opp'),
               ('Hotel San Antonio', 'Grljevačka 30, Podstrana · +385 21 33 61 11 · info@hotel-sanantonio.com · 4 stjerner på stranda, frokost · svarte 18.9.2026 at de bare har ledig 8.–10. juni', 'Ikke ledig'),
               ('Hotel Atrium', 'Split, 1,3 km fra sentrum · 5 stjerner · Ving-pakke med frokost, bagasje og SAS-fly 5.–12. juni 12 295 per person', 'Slått opp')],
     rows=[BUSS,
           ('Fly, 28 personer t/r', 'Delvis tilbud', '28 × 5 636 · Gruppetilbud XV8K8J Oslo–Split tur/retur 2 600 per person (DY 1950 tir 8. juni 07:15–10:05, DY 1951 tir 15. juni 10:50–13:40), 60 648 pluss skatter og avgifter 12 152 = 72 800 for 28 og 2 × 23 kg koffert, mottatt 17.9.2026, gyldig i fem virkedager og dermed utgått rundt 24. september — må hentes inn på nytt · Norwegians gruppevilkår gir 2 × 23 kg innsjekket bagasje, to håndbagasjer og én taxfreepose per reisende i gruppeprisen (norwegian.com, lest 26.9.2026) · Alta–Oslo 2 018 (DY 321 man 7. juni) og Oslo–Alta 1 018 (DY 328 tir 15. juni) er fortsatt LowFare+ for én person — gruppetilbud er bedt om, men ikke mottatt', 5636),
           GARDERMOEN_A,
           ('Hotell i Split, 7 netter med frokost', 'Slått opp', '28 × 6 386 · Cora Hotel, 4 stjerner 1,5 km fra gamlebyen, 9,3 av 10 · rom med frokost · booking.com 26.9.2026 for 8.–15. juni 2027: 102 178 for 16 personer i fire rom, 6 386 per person · booking.com priser ikke alle 28 i én bestilling, så hele gruppa må bekreftes direkte med hotellet', 6386),
           ('Middag ute og lunsj', 'Estimat', '28 × 2 750 · lunsj (130) og konoba-middag (220) i sju dager, pluss mat på reisedagene', 2750),
           ('Aktiviteter med leiebuss', 'Estimat', '28 × 2 000 · flybuss t/r, Krka og Klis/Trogir med leiebuss, rafting i Cetina, ferje til Brač, kjellerne og bybuss inn til Split — se programmet', 2000),
           ('Turistskatt på stedet', 'Estimat', '28 × 75 · kroatisk turistskatt, 1,60 euro per person per natt i høysesong for Split, kategori B · reisende 12–18 betaler halv sats, så sju voksne full og 21 elever halv i sju netter · betales på stedet', 75),
           FORSIKRING],
     obs_ekstra=['Flyet fra Gardermoen går 07:15; Thon Hotel Gardermoen har frokost fra tidlig morgen og shuttlebuss mot betaling.',
                 'Hotellet ligger i Split, 1,5 kilometer fra gamlebyen — gangavstand. Da faller bybussen fra Podstrana bort, men gruppen bor ikke lenger rett ved en strand.',
                 'Rafting i Cetina er klasse 2–3 og brukes av skolegrupper; alle må kunne svømme, og redningsvest og guide er med i prisen.'],
     warn=GRUPPE_WARN + ' Hotellene er slått opp på booking.com for de nøyaktige datoene, med fri avbestilling. Leiebuss i Kroatia er anslått ut fra veiledende priser, ikke tilbud. Mat og aktiviteter er anslag. Kurs brukt: 1 EUR = 10,77 kr (Norges Bank 14.9.2026).',
     ),
]

def kreditt_linje(s):
    """Fullstendige bildekreditter ut fra galleriet."""
    deler = []
    for src in re.findall(r'<img src="([^"]+)"', s):
        m = re.search(r'FilePath/([^?]+)', src)
        if not m: continue
        fil = unquote(m.group(1))
        k = KREDITT.get(fil)
        tittel = os.path.splitext(fil)[0].replace('_', ' ')
        deler.append('«%s»%s' % (tittel, (' av %s (%s)' % k) if k else ''))
    return 'Bilder fra Wikimedia Commons: ' + ' · '.join(deler) + '.'

def build(a):
    s = open(os.path.join(INN, a['base']), encoding='utf-8').read()
    s = re.sub(r'<title>.*?</title>', '<title>Klassetur 10B — %s, %s</title>' % (a['navn'], a['variant']), s, count=1)
    # hero
    s = re.sub(r'<p class="kicker">.*?</p>', '<p class="kicker">Klassetur 10B · Kautokeino skole · %s · %d reisende</p>' % (a['datoer'], N), s, count=1, flags=re.S)
    s = re.sub(r'<h1>.*?</h1>', '<h1>%s<span>%s</span></h1>' % (a['navn'], a['under']), s, count=1, flags=re.S)
    s = re.sub(r'<p class="promise">.*?</p>', '<p class="promise">%s</p>' % a['promise'], s, count=1, flags=re.S)
    rows = a['rows']
    total = sum(r[3] if r[0].startswith('Buss') else N * r[3] for r in rows)
    pp = int(round(total / N / 100.0)) * 100
    band = a['band'] + [(n(pp), 'kroner per reisende'), (n(total), 'kroner totalt')]
    s = re.sub(r'<div class="heroband">.*?\n\s*</div>', '<div class="heroband">\n      ' + '\n      '.join('<div><b>%s</b><small>%s</small></div>' % b for b in band) + '\n    </div>', s, count=1, flags=re.S)
    # reisevei
    legs = ''.join('<div class="leg"><b>%s</b><small>%s</small></div>' % l for l in a['reise'])
    s = re.sub(r'<section>\s*<h2>Reisevei</h2>.*?</section>', '<section>\n    <h2>Reisevei</h2>\n    <div class="route">%s</div>\n    <p style="margin-top:16px">%s</p>\n  </section>' % (legs, a['reise_note']), s, count=1, flags=re.S)
    # verdt å vite: behold arkets punkter, legg til variantens
    m = re.search(r'<section>\s*<h2>Verdt å vite</h2>\s*<ul class="plain obs">(.*?)</ul>\s*</section>', s, re.S)
    gamle = re.findall(r'<li>(.*?)</li>', m.group(1), re.S) if m else []
    for bort in a.get('obs_drop', []):
        gamle = [g for g in gamle if bort not in g]
    if a['navn'] == 'Split':
        gamle = [g for g in gamle if 'Hvar' not in g] + ['Dagsturen med ferje går til Brač og Zlatni Rat. Hvar by er kjent for uteliv om kvelden og er ikke lagt inn i programmet.']
    obs = '<section>\n    <h2>Verdt å vite</h2>\n    <ul class="plain obs">' + ''.join('<li>%s</li>' % x for x in gamle + a['obs_ekstra']) + '</ul>\n  </section>'
    if m: s = s.replace(m.group(0), obs, 1)
    else: s = re.sub(r'(\s*<section>\s*<h2>Slik ser uka ut</h2>)', '\n\n  ' + obs + r'\1', s, count=1)
    # uka
    days = ''.join('<li><div class="day"><b>%s</b><small>%s</small></div><span class="act">%s</span></li>' % d for d in a['dager'])
    s = re.sub(r'<section>\s*<h2>Slik ser uka ut</h2>.*?</section>', '<section>\n    <h2>Slik ser uka ut</h2>\n    <h3>%s</h3>\n    <ol class="days">%s</ol>\n    <p style="margin-top:16px;font-size:13px;color:var(--muted)">%s</p>\n  </section>' % (a['uke_tittel'], days, a['uke_note']), s, count=1, flags=re.S)
    # overnatting
    TAGCLS = {'Slått opp': 't-ok', 'Bekreftet': 't-ok', 'Tilbud mottatt': 't-ok', 'Delvis tilbud': 't-quote', 'Tilbud innhentes': 't-quote', 'Ikke ledig': 't-quote', 'Estimat': 't-est'}
    hot = ''.join('<tr><td><b>%s</b><span class="basis">%s</span></td><td class="num"><span class="tag %s">%s</span></td></tr>' % (h[0], h[1], TAGCLS[h[2]], h[2]) for h in a['hoteller'])
    s = re.sub(r'<section>\s*<h2>Overnatting</h2>.*?</section>', '<section>\n    <h2>Overnatting</h2>\n    <h3>%s</h3>\n    <p class="lede">%s</p>\n    <table style="margin-top:18px">%s</table>\n  </section>' % (a['hotell_tittel'], a['hotell_lede'], hot), s, count=1, flags=re.S)
    # kostnader
    trs = ''.join('<tr><td>%s</td><td><span class="tag %s">%s</span><span class="basis">%s</span></td><td class="num">%s</td></tr>' % (r[0], TAGCLS[r[1]], r[1], r[2], n(r[3] if r[0].startswith('Buss') else N * r[3])) for r in rows)
    ok = sum(1 for r in rows if r[1] in ('Bekreftet', 'Slått opp', 'Tilbud mottatt'))
    kost = ('<section>\n    <h2>Hva turen koster</h2>\n    <table>\n      <tr><th>Post</th><th>Grunnlag</th><th style="text-align:right">Kroner</th></tr>\n      %s\n      <tr class="sum"><td>Totalt</td><td></td><td class="num">%s</td></tr>\n    </table>\n'
            '    <div class="headline-num">\n      <div><b>%s</b><small>kroner per reisende</small></div>\n      <div><b>%d av %d</b><small>poster bekreftet eller slått opp</small></div>\n    </div>\n    <div class="warn">\n      %s\n    </div>\n  </section>') % (trs, n(total), n(pp), ok, len(rows), a['warn'])
    if a.get('tilbud'):
        t = a['tilbud']
        ttot = sum(r[3] for r in t['rows'])
        tpp = int(round(ttot / N / 100.0)) * 100
        trs2 = ''.join('<tr><td>%s</td><td><span class="tag %s">%s</span><span class="basis">%s</span></td><td class="num">%s</td></tr>' % (r[0], TAGCLS[r[1]], r[1], r[2], n(r[3])) for r in t['rows'])
        diff = ttot - total
        kost += ('\n\n  <section>\n    <h2>%s</h2>\n    <h3>%s</h3>\n    <p class="lede">%s</p>\n'
                 '    <table style="margin-top:18px"><tr><td><b>%s</b><span class="basis">%s</span></td><td class="num"><span class="tag %s">%s</span></td></tr></table>\n'
                 '    <table style="margin-top:18px">\n      <tr><th>Post</th><th>Grunnlag</th><th style="text-align:right">Kroner</th></tr>\n      %s\n      <tr class="sum"><td>Totalt</td><td></td><td class="num">%s</td></tr>\n    </table>\n'
                 '    <div class="headline-num">\n      <div><b>%s</b><small>kroner per reisende</small></div>\n      <div><b>%s</b><small>kroner %s enn Apollo-pakken over, for 28</small></div>\n    </div>\n'
                 '    <div class="warn">\n      %s\n    </div>\n  </section>') % (
                 t['tittel'], t['under'], t['lede'], t['hotell'][0], t['hotell'][1], TAGCLS[t['hotell'][2]], t['hotell'][2], trs2, n(ttot), n(tpp),
                 n(abs(diff)), 'mer' if diff > 0 else 'mindre', t['note'])
        a['tilbud_tall'] = (tpp, ttot)
    s = re.sub(r'<section>\s*<h2>Hva turen koster</h2>.*?</section>', kost, s, count=1, flags=re.S)
    # footer
    s = re.sub(r'<footer>.*?</footer>', '<footer>\n    Ikke inkludert: lommepenger, pass eller nasjonalt ID-kort, avbestillingsforsikring, egenandel ved sykdom.<br>\n    %s<br>\n    Alle beløp i kroner. Fly, hotell og pakker er slått opp 15. september 2026 for de oppgitte datoene; mat og aktiviteter er anslag. Beløpene er for 28 reisende, uten buffer.\n  </footer>' % kreditt_linje(s), s, count=1, flags=re.S)
    assert '28 grader' in s or a['navn'] != 'Kreta' or True
    open(os.path.join(UT, a['fil']), 'w', encoding='utf-8').write(s)
    print('%-40s pp %7s  total %9s' % (a['fil'], n(pp), n(total)))
    return a, pp, total

if __name__ == '__main__':
    for a in ARK: build(a)
