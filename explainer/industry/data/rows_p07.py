"""Register rows for Part 7, *Sizing a Market*.  Checked 2026-11-24.

Uber's 2019 prospectus for an addressable market measured in trillions; three published sizes of the US bottled water
market (the Census Bureau's factory-gate shipments, Primo Brands' 10-K, the Beverage Marketing Corporation's volume);
the adoption curves are the Filing Room's ``owid_tech.csv`` and company revenue its ``sec_annual.csv``.
"""

from explainer.industry.register import Row, add

C = "2026-11-24"
P = (7,)
UBER = "https://www.sec.gov/Archives/edgar/data/1543151/000119312519103850/d647752ds1.htm"
PRMB = "https://www.sec.gov/Archives/edgar/data/2042694/000204269425000003/prmb-20241231.htm"
BMC = "https://www.beveragemarketing.com/news-detail.asp?id=825"


def r(key, value, unit, definition, source, url, fact, kind="filing", note="", **kw):
    return Row(key, value, unit, definition, source, url, fact, C, kind, note=note, parts=P, **kw)


def uber(key, value, unit, definition, fact="2017"):
    return r(key, value, unit, definition, "Uber Technologies, Form S-1, 11 April 2019 ('Market, Industry, and Other "
             "Data'; 'Our Market Opportunity')", UBER, fact)


add(
    # --- Uber's addressable market (S-1, April 2019) -------------------------------------------------------------------
    uber("uber.tam.mobility", 5.7, "USD tn", "Personal Mobility TAM: 11.9 trillion miles a year in 175 countries (7.5 "
         "trillion vehicle miles and 4.4 trillion public transport miles) at an estimated 23 cents a mile"),
    uber("uber.tam.miles", 11.9, "tn miles", "miles in the Personal Mobility TAM: every passenger-vehicle and public "
         "transport mile in 175 countries"),
    uber("uber.tam.eats", 2.8, "USD tn", "Uber Eats TAM: all consumer spending at restaurants (of which $795bn was home "
         "delivery, where Uber Eats' 2018 gross bookings of $7.9bn were 1.0%)"),
    uber("uber.tam.freight", 3.8, "USD tn", "Uber Freight TAM: the global market for freight trucking in 2017 "
         "(Armstrong & Associates)"),
    uber("uber.sam.mobility", 2.5, "USD tn", "Personal Mobility current SAM: 3.9 trillion miles in 57 countries (trips "
         "under 30 miles)", "2018"),
    uber("uber.miles.2018", 26, "bn miles", "miles travelled on Uber's platform in 2018: less than 1% of the vehicle "
         "miles in trips under 30 miles in its 63 countries", "2018"),
    # --- three sizes of one market: US bottled water ---------------------------------------------------------------
    r("water.census.2023", 7.24, "USD bn", "shipments of US bottled water manufacturers (NAICS 312112), 2023: factory "
      "gate, US plants classified to bottled water only (2022: $8.69bn; 2024: $7.46bn)", "US Census Bureau, Annual "
      "Integrated Economic Survey, via FRED (AIES312112RCTUS)", "https://fred.stlouisfed.org/series/AIES312112RCTUS",
      "2023", kind="official"),
    r("water.primo.2023", 25, "USD bn", "'In 2023, the U.S. bottled water market, which includes still water, sparkling "
      "water and seltzer water, generated $25 billion in retail sales'", "Primo Brands Corp, Form 10-K for 2024 (filed 27 "
      "February 2025), Business", PRMB, "2023", note="the company does not name its source"),
    r("water.bmc.percap.2024", 47.3, "gallons", "US bottled water consumption per person, 2024 (2023: 46.4; carbonated "
      "soft drinks 2024: 34.8)", "Beverage Marketing Corporation, news release, May 2025", BMC, "2024", kind="tracker"),
    r("water.bmc.single.2024", 11.6, "bn gallons", "US single-serve bottled water volume, 2024: nearly 71% of the "
      "category's volume", "Beverage Marketing Corporation, news release, May 2025", BMC, "2024", kind="tracker"),
)
