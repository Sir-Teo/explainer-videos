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
WE = "https://www.sec.gov/Archives/edgar/data/1533523/000119312519220499/d781982ds1.htm"


def r(key, value, unit, definition, source, url, fact, kind="filing", note="", **kw):
    return Row(key, value, unit, definition, source, url, fact, C, kind, note=note, parts=P, **kw)


def uber(key, value, unit, definition, fact="2017"):
    return r(key, value, unit, definition, "Uber Technologies, Form S-1, 11 April 2019 ('Market, Industry, and Other "
             "Data'; 'Our Market Opportunity')", UBER, fact)


add(
    # --- Uber's addressable market (S-1, April 2019) -------------------------------------------------------------------
    uber("uber.tam.mobility", 5.7, "USD tn", "Personal Mobility TAM: 11.9 trillion miles a year in 175 countries: 7.5 "
         "trillion vehicle miles valued at $4.7tn (about 63 cents a mile) and 4.4 trillion public transport miles at "
         "an estimated 23 cents a mile ($1.0tn)"),
    uber("uber.tam.vehicle", 4.7, "USD tn", "the vehicle-mile part of the Personal Mobility TAM (7.5 trillion miles)"),
    uber("uber.tam.public", 1.0, "USD tn", "the public-transport part of the Personal Mobility TAM (4.4 trillion miles "
         "at about 23 cents)"),
    uber("uber.tam.miles", 11.9, "tn miles", "miles in the Personal Mobility TAM: every passenger-vehicle and public "
         "transport mile in 175 countries"),
    uber("uber.tam.eats", 2.8, "USD tn", "Uber Eats TAM: the entire global consumer spend on food services in 2017 "
         "(Euromonitor), eat-in included ($2,838bn in the S-1's table)"),
    uber("uber.eats.sam", 795, "USD bn", "Uber Eats SAM: consumer spending in 2017 on meals from home delivery ($161bn), "
         "takeaway ($472bn) and drive-through ($162bn), worldwide (Euromonitor)"),
    uber("uber.eats.delivery", 161, "USD bn", "home delivery's part of Uber Eats' SAM, 2017 (Euromonitor)"),
    uber("uber.eats.takeaway", 472, "USD bn", "takeaway's part of Uber Eats' SAM, 2017 (Euromonitor)"),
    uber("uber.eats.drive", 162, "USD bn", "drive-through's part of Uber Eats' SAM, 2017 (Euromonitor)"),
    uber("uber.eats.eatin", 2043, "USD bn", "eat-in restaurant spend, 2017, inside the Eats TAM (Euromonitor)"),
    uber("uber.eats.bookings", 7.9, "USD bn", "Uber Eats gross bookings in 2018 (what customers paid, food included), "
         "which the S-1 called 1.0% of the $795bn SAM", "2018"),
    uber("uber.tam.freight", 3.8, "USD tn", "Uber Freight TAM: the global market for freight trucking in 2017 "
         "(Armstrong & Associates)"),
    uber("uber.sam.mobility", 2.5, "USD tn", "Personal Mobility current SAM: 3.9 trillion miles in 57 countries (trips "
         "under 30 miles)", "2018"),
    uber("uber.miles.2018", 26, "bn miles", "miles travelled on Uber's platform in 2018: less than 1% of the vehicle "
         "miles in trips under 30 miles in its 63 countries", "2018"),
    uber("uber.mapcs.2018", 91, "m people", "monthly active platform consumers, average of 2018's fourth quarter",
         "2018"),
    uber("uber.trips.2018", 5220, "m trips", "trips on Uber's platform in 2018 (rides and meal deliveries)", "2018"),
    uber("uber.bookings.2018", 49.8, "USD bn", "gross bookings in 2018: what consumers paid for rides and meals, before "
         "drivers' and restaurants' shares ($49,799m)", "2018"),
    uber("uber.netrev.2018", 10.0, "USD bn", "core platform adjusted net revenue in 2018 ($10,025m): what Uber kept",
         "2018"),
    # --- WeWork's total opportunity (S-1, August 2019) -------------------------------------------------------------
    r("wework.cost", 11700, "USD", "weighted average occupancy cost per employee a year in 155 cities (CBRE and "
      "Cushman & Wakefield data)", "The We Company, Form S-1, 14 August 2019", WE, "2019"),
    r("wework.members", 255, "m people", "potential members in WeWork's 280 target cities", "The We Company, Form S-1, "
      "14 August 2019", WE, "2019"),
    r("wework.total", 3.0, "USD tn", "'total opportunity' in the 280 target cities (addressable market opportunity "
      "$1.6tn; in its existing 111 cities, $1.7tn and $945bn)", "The We Company, Form S-1, 14 August 2019", WE, "2019"),
    r("wework.addressable", 1.6, "USD tn", "'addressable market opportunity' in the 280 target cities", "The We "
      "Company, Form S-1, 14 August 2019", WE, "2019"),
    r("wework.rw", 2019, "year", "The We Company asked the SEC to withdraw its registration statement on 30 September "
      "2019", "The We Company, Form RW, 30 September 2019",
      "https://www.sec.gov/Archives/edgar/data/1533523/000119312519258913/d808793drw.htm", "2019-09-30"),
    r("wework.ch11", 2023, "year", "WeWork Inc. and some subsidiaries filed for Chapter 11 on 6 November 2023",
      "WeWork Inc., Form 8-K, 7 November 2023",
      "https://www.sec.gov/Archives/edgar/data/1813756/000119312523271902/d522028d8k.htm", "2023-11-06"),
    r("model.microwave.life", 10, "years", "how long a microwave oven stays in use before it is replaced, on average, "
      "in this film's model of first purchases and replacements", "This series' assumption, for a model; the film "
      "shows what changes if it is 8 or 12", "", "2025", kind="assumption", lo=8, hi=12),
    r("bass.1969", 1969, "year", "Frank M. Bass, 'A New Product Growth for Model Consumer Durables', Management "
      "Science 15(5), January 1969, pp. 215-227: adoption by innovators (p) and imitators (q)", "Management Science",
      "https://doi.org/10.1287/mnsc.15.5.215", "1969", kind="study"),
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
    r("water.bmc.percap.2023", 46.4, "gallons", "US bottled water consumption per person, 2023", "Beverage Marketing "
      "Corporation, news release, May 2025", BMC, "2023", kind="tracker"),
    r("water.bmc.forecast", 50, "gallons", "Beverage Marketing's expectation: per capita bottled water consumption to "
      "reach about 50 gallons, the level soft drinks regularly exceeded around 2000, 'by the end of this decade or the "
      "start of the next'", "Beverage Marketing Corporation, news release, May 2025", BMC, "2025-05", kind="tracker"),
    r("water.bmc.single.2024", 11.6, "bn gallons", "US single-serve bottled water volume, 2024: nearly 71% of the "
      "category's volume", "Beverage Marketing Corporation, news release, May 2025", BMC, "2024", kind="tracker"),
)
