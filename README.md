# Klassetur 2027

Interaktivt kart over kandidatene til klasseturen for 10. trinn ved Kautokeino skole, juni 2027 — to klasser i samme kart.

- `docs/index.html` er nettsiden (GitHub Pages publiserer fra `docs/`). Kartet åpner med 10B; `?klasse=10A` åpner 10A direkte, og en lenke med `#kreta` eller `#split-best` åpner reisemålet i riktig klasse.
- `Klassetur-kart-2027.html` er den samme fila, til lokal bruk.
- `underlag/` er 10A (20 reisende): 25 turark, oversiktsarket `Klassetur-kandidater-2027.html` og `lag_kart.py`.
- `underlag/10B/` er 10B (28 reisende): Kreta, Costa Blanca og Split, hvert regnet både billigst og best, med oversiktsarket `Klassetur-kandidater-10B.html`.
- `lag_kart.py` bygger kartet fra begge mappene: `cd underlag && python lag_kart.py`. Skriptet skriver `../Klassetur-kart-2027.html`, `../docs/index.html` og `../nett/`.
- `publiser.bat` gjør begge deler i ett: bygger kartet på nytt og gjør commit og push. Dobbeltklikk den i stedet for å åpne GitHub Desktop. Nettsida er oppdatert innen et minutt.
- `underlag/status_data.py` er lista over hvem som er spurt om pris og hva de har svart. Rediger den når det kommer et svar, kjør `publiser.bat`, og «Forespørsler»-boksen på sida er oppdatert.
- `underlag/kalkulator_data.py` er grunnlaget for «Sett sammen turen» inne på hvert 10B-reisemål: hotellalternativer med pris, tre nivåer på matbudsjettet, og hvilke rader i kostnadstabellen som er valgbare. Fast pris, utflukter og standardvalg regnes ut av `lag_kart.py` fra arkene, så de holder seg i synk av seg selv.
