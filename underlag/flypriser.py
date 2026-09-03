#!/usr/bin/env python3
"""
flypriser.py — henter flypriser for en liste ruter og skriver dem til CSV.

Leser ruter.csv, slår opp hver rute mot Google Flights, og skriver priser.csv
med pris per person og pris ganget opp med antall reisende.

Bruk:
    pip install fast-flights
    python flypriser.py                        # ruter.csv -> priser.csv, 28 reisende
    python flypriser.py --pax 28 --bagasje 1
    python flypriser.py --inn andre-ruter.csv --ut andre-priser.csv

ruter.csv har fire eller fem kolonner med semikolon:

    navn;fra;til;ut;hjem
    Gdansk 4. juni;KTT;GDN;2026-06-04;2026-06-11

Utelates «hjem» blir det en enveisreise. Linjer som starter med # hoppes over.
"""

import argparse
import csv
import sys
import time
from pathlib import Path

try:
    from fast_flights import create_query, FlightQuery, Passengers, get_flights
except ImportError:
    sys.exit("Mangler fast-flights. Kjør:  pip install fast-flights")


FELT = ["navn", "fra", "til", "ut", "hjem", "pris_pp", "pris_gruppe",
        "selskap", "stopp", "varighet_t", "avgang", "status"]


def les_ruter(sti):
    ruter = []
    with open(sti, newline="", encoding="utf-8-sig") as f:
        for rad in csv.reader(f, delimiter=";"):
            if not rad or not rad[0].strip() or rad[0].lstrip().startswith("#"):
                continue
            if rad[0].strip().lower() == "navn":      # overskriftsrad
                continue
            rad = [c.strip() for c in rad] + [""] * (5 - len(rad))
            ruter.append({
                "navn": rad[0], "fra": rad[1].upper(), "til": rad[2].upper(),
                "ut": rad[3], "hjem": rad[4],
            })
    return ruter


def sok(rute, bagasje, valuta):
    """Returnerer det billigste tilbudet for én rute, eller None."""
    ben = [FlightQuery(date=rute["ut"], from_airport=rute["fra"], to_airport=rute["til"])]
    if rute["hjem"]:
        ben.append(FlightQuery(date=rute["hjem"], from_airport=rute["til"], to_airport=rute["fra"]))

    q = create_query(
        flights=ben,
        trip="round-trip" if rute["hjem"] else "one-way",
        seat="economy",
        passengers=Passengers(adults=1),
        currency=valuta,
        language="en-GB",
        checked_bags=bagasje,
    )
    treff = [f for f in get_flights(q) if getattr(f, "price", None)]
    return min(treff, key=lambda f: f.price) if treff else None


def beskriv(tilbud):
    etapper = tilbud.flights or []
    ut = etapper[0] if etapper else None
    return {
        "selskap": ", ".join(dict.fromkeys(tilbud.airlines or [])),
        "stopp": max(len(etapper) - 1, 0),
        "varighet_t": round(sum(e.duration for e in etapper) / 60, 1) if etapper else "",
        "avgang": f"{ut.departure.time[0]:02d}:{ut.departure.time[1]:02d}" if ut else "",
    }


def main():
    p = argparse.ArgumentParser()
    p.add_argument("--inn", default="ruter.csv")
    p.add_argument("--ut", default="priser.csv")
    p.add_argument("--pax", type=int, default=28, help="antall reisende å gange opp med")
    p.add_argument("--bagasje", type=int, default=1, help="innsjekket kolli per person")
    p.add_argument("--valuta", default="NOK")
    p.add_argument("--pause", type=float, default=4.0, help="sekunder mellom søk")
    a = p.parse_args()

    if not Path(a.inn).exists():
        sys.exit(f"Fant ikke {a.inn}. Lag den først — se toppen av dette skriptet.")

    ruter = les_ruter(a.inn)
    if not ruter:
        sys.exit(f"{a.inn} inneholder ingen ruter.")

    print(f"{len(ruter)} ruter, {a.pax} reisende, {a.bagasje} kolli hver.\n")
    rader, treff = [], 0

    for i, rute in enumerate(ruter, 1):
        merkelapp = f"[{i}/{len(ruter)}] {rute['navn'] or rute['fra'] + '-' + rute['til']}"
        rad = dict(rute, pris_pp="", pris_gruppe="", selskap="", stopp="",
                   varighet_t="", avgang="", status="")
        try:
            tilbud = sok(rute, a.bagasje, a.valuta)
            if tilbud:
                rad.update(beskriv(tilbud))
                rad["pris_pp"] = tilbud.price
                rad["pris_gruppe"] = tilbud.price * a.pax
                rad["status"] = "ok"
                treff += 1
                print(f"{merkelapp}: {tilbud.price} {a.valuta} pp  →  "
                      f"{tilbud.price * a.pax} for {a.pax}  ({rad['selskap']}, "
                      f"{rad['stopp']} stopp)")
            else:
                rad["status"] = "ingen treff"
                print(f"{merkelapp}: ingen treff")
        except Exception as e:
            rad["status"] = f"feil: {type(e).__name__}"
            print(f"{merkelapp}: FEIL — {type(e).__name__}: {e}")

        rader.append(rad)
        if i < len(ruter):
            time.sleep(a.pause)

    with open(a.ut, "w", newline="", encoding="utf-8-sig") as f:
        w = csv.DictWriter(f, fieldnames=FELT, delimiter=";")
        w.writeheader()
        w.writerows(rader)

    print(f"\n{treff} av {len(ruter)} ruter priset. Skrevet til {a.ut}")
    gyldige = [r for r in rader if r["status"] == "ok"]
    if gyldige:
        billigst = min(gyldige, key=lambda r: r["pris_pp"])
        print(f"Billigst: {billigst['navn']} — {billigst['pris_pp']} {a.valuta} pp, "
              f"{billigst['pris_gruppe']} for gruppen.")


if __name__ == "__main__":
    main()
