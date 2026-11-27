"""Register rows for Part 28, *Airlines*.  Checked 2026-11-27.

Delta's Form 10-K for 2025 and its 2026 results releases (Forms 8-K, Exhibit 99.1); the Forms 10-K for 2025 of Southwest,
American and Spirit Aviation Holdings; the Airline Deregulation Act of 1978 (Public Law 95-504); Berkshire Hathaway's
letter to shareholders for 2007.  Series are the Filing Room's SEC and FRED extracts.
"""

from explainer.industry.register import Row, add

C = "2026-11-27"
P = (28,)
SEC = "https://www.sec.gov/Archives/edgar/data/"
DAL = SEC + "27904/000002790426000013/dal-20251231.htm"
DAL_JAN = SEC + "27904/000002790426000008/deltaairlinesannouncesdece.htm"
DAL_APR = SEC + "27904/000002790426000020/deltaairlinesannouncesmarc.htm"
DAL_JUL = SEC + "27904/000002790426000029/deltaairlinesannouncesjune.htm"
DAL_OCT = SEC + "27904/000002790426000035/deltaairlinesannouncessept.htm"
LUV = SEC + "92380/000009238026000004/luv-20251231.htm"
AAL = SEC + "6201/000000620126000014/aal-20251231.htm"
SAVE = SEC + "1498710/000162828026018265/flyy-20251231.htm"
ADA = "https://www.govinfo.gov/content/pkg/STATUTE-92/pdf/STATUTE-92-Pg1705.pdf"
BRK = "https://www.berkshirehathaway.com/letters/2007ltr.pdf"
CARES = "https://www.govinfo.gov/content/pkg/PLAW-116publ136/html/PLAW-116publ136.htm"


def r(key, value, unit, definition, source, url, fact, kind="filing", note="", **kw):
    return Row(key, value, unit, definition, source, url, fact, C, kind, note=note, parts=P, **kw)


def dal(key, value, unit, definition, fact="2025"):
    return r(key, value, unit, definition, "Delta Air Lines, Form 10-K for 2025", DAL, fact)


def dal8(key, value, unit, definition, when, url):
    return r(key, value, unit, definition, f"Delta Air Lines, results release of {when} (Form 8-K, Exhibit 99.1)", url, "2026")


def luv(key, value, unit, definition, fact="2025"):
    return r(key, value, unit, definition, "Southwest Airlines, Form 10-K for 2025", LUV, fact)


def save(key, value, unit, definition, fact="2025"):
    return r(key, value, unit, definition, "Spirit Aviation Holdings, Form 10-K for 2025", SAVE, fact)


DAL_COSTS = {"salaries": 17520, "fuel": 9819, "ancillary": 5987, "contracted": 4617, "landing": 3564, "regional": 2553,
             "selling": 2485, "depreciation": 2443, "maintenance": 2432, "service": 1855, "profitsharing": 1337, "rent": 542,
             "other": 2388, "total": 57542}

add(
    # Delta: a seat-mile's arithmetic and a dollar's costs
    dal("dl28.rpm", 249578, "million", "revenue passenger miles, 2025 (246,145 in 2024)"),
    dal("dl28.asm", 298045, "million", "available seat miles, 2025 (288,394 in 2024)"),
    dal("dl28.yield", 20.74, "US cents", "passenger mile yield, 2025"),
    dal("dl28.prasm", 17.37, "US cents", "passenger revenue per available seat mile, 2025"),
    dal("dl28.trasm", 21.26, "US cents", "total revenue per available seat mile, 2025 (21.37 in 2024)"),
    dal("dl28.casm", 19.31, "US cents", "cost per available seat mile, 2025 (19.30 in 2024)"),
    dal("dl28.casmex", 13.86, "US cents", "CASM-Ex: cost per available seat mile excluding fuel and some other items, 2025"),
    dal("dl28.lf", 84, "percent", "passenger load factor, 2025 (85 in 2024)"),
    dal("dl28.gal", 4269, "million gallons", "fuel gallons consumed, 2025"),
    dal("dl28.fuel", 2.30, "US$ a gallon", "average price per fuel gallon, 2025 ($2.57 in 2024)"),
    dal("dl28.emp", 103000, "people", "approximate full-time equivalent employees, end of 2025"),
    *[dal(f"dl28.cost.{k}", v, "US$ million", f"operating expense, 2025: {k}") for k, v in DAL_COSTS.items()],
    dal("dl28.amex", 8.2, "US$ billion", "remuneration from American Express related to the SkyMiles program, 2025, up about 11%; "
        "'which we expect to grow to $10 billion over the next few years'"),
    dal("dl28.skymiles", 9.3, "US$ billion", "aggregate deferred revenue balance associated with the SkyMiles program, "
        "31 December 2025", "2025-12-31"),
    dal8("dl28.g.jan.lo", 6.50, "US$ a share", "full-year 2026 earnings per share guidance, low end ($6.50-7.50)", "13 January 2026", DAL_JAN),
    dal8("dl28.g.jan.hi", 7.50, "US$ a share", "full-year 2026 earnings per share guidance, high end", "13 January 2026", DAL_JAN),
    dal8("dl28.g.oct.lo", 5.10, "US$ a share", "full-year 2026 earnings per share outlook, low end ($5.10-5.60)", "9 October 2026", DAL_OCT),
    dal8("dl28.g.oct.hi", 5.60, "US$ a share", "full-year 2026 earnings per share outlook, high end", "9 October 2026", DAL_OCT),
    dal8("dl28.fuelhit", 6, "US$ billion", "'we expect to generate a pre-tax profit of roughly $4.5 billion, absorbing a $6 billion "
         "increase in fuel costs'", "9 October 2026", DAL_OCT),
    dal8("dl28.pretax26", 4.5, "US$ billion", "expected pre-tax profit for 2026", "9 October 2026", DAL_OCT),
    dal8("dl28.fuel.q2", 4.30, "US$ a gallon", "projected all-in fuel price for the second quarter of 2026", "8 April 2026", DAL_APR),
    dal8("dl28.fuel.q3", 3.15, "US$ a gallon", "projected all-in fuel price for the third quarter of 2026", "10 July 2026", DAL_JUL),
    dal8("dl28.fuel.q4", 4.25, "US$ a gallon", "projected all-in fuel price for the fourth quarter of 2026", "9 October 2026", DAL_OCT),
    dal8("dl28.refinery.q4", 0.40, "US$ a gallon", "refinery benefit included in the fourth-quarter 2026 fuel price outlook",
         "9 October 2026", DAL_OCT),
    dal8("dl28.loyalty.q3", 18, "percent", "growth of total loyalty revenue, third quarter of 2026", "9 October 2026", DAL_OCT),

    # Southwest
    luv("sw28.rasm", 15.59, "US cents", "operating revenues per available seat mile, 2025 (15.51 in 2024)"),
    luv("sw28.casm", 15.35, "US cents", "operating expenses per available seat mile, 2025 (15.32 in 2024)"),
    luv("sw28.lf", 77.4, "percent", "load factor, 2025 (80.4 in 2024)"),
    luv("sw28.fare", 190.41, "US$", "average passenger fare, 2025 ($178.40 in 2024)"),
    luv("sw28.stage", 780, "miles", "average aircraft stage length, 2025"),
    luv("sw28.planes", 803, "aircraft", "aircraft at the end of 2025"),
    luv("sw28.pax", 134110, "thousand", "revenue passengers carried, 2025"),
    luv("sw28.mpg", 83.0, "seat miles a gallon", "available seat miles per fuel gallon, 2025 (77.3 in 2022)"),
    luv("sw28.lf.2024", 80.4, "percent", "load factor, 2024", "2024"),
    luv("sw28.fare.2024", 178.40, "US$", "average passenger fare, 2024", "2024"),
    luv("sw28.pax.2024", 140023, "thousand", "revenue passengers carried, 2024", "2024"),
    luv("sw28.trips", 1415822, "trips", "trips flown, 2025 (1,443,866 in 2024)"),
    luv("sw28.seatspertrip", 161.2, "seats", "seats per trip, 2025 (159.4 in 2024)"),
    luv("sw28.bags", 1, "flag", "'For flights booked and ticketed or changed on or after May 28, 2025, Southwest introduced bag fees for "
        "most fare products'; 'Beginning January 27, 2026, the Company introduced an assigned seating model'", "2025-05-28"),
    luv("sw28.q4", 90, "percent", "on a GAAP basis, the share of 2025's operating income earned in the fourth quarter: 'in excess of "
        "90 percent'"),
    luv("sw28.mpg.2022", 77.3, "seat miles a gallon", "available seat miles per fuel gallon, 2022", "2022"),

    # Spirit
    save("spirit.trasm", 9.51, "US cents", "total revenue per available seat mile, 2025 (9.27 in 2024)"),
    save("spirit.casm", 11.43, "US cents", "cost per available seat mile, 2025 (11.35 in 2024)"),
    save("spirit.lf", 78.4, "percent", "load factor, 2025 (82.4 in 2024)"),
    save("spirit.planes", 131, "aircraft", "aircraft at the end of 2025 (213 a year before)", "2025-12-31"),
    save("spirit.planes.2024", 213, "aircraft", "aircraft at the end of 2024", "2024-12-31"),
    save("spirit.ch11", 1, "flag", "Spirit Airlines commenced a chapter 11 case in November 2024, emerged on 12 March 2025, and filed "
         "again on 29 August 2025", "2024-11 to 2025-08"),

    # American
    r("aal.cobrand25", 6.2, "US$ billion", "cash payments from co-branded credit card and other partners, 2025 ($6.1bn in 2024)",
      "American Airlines Group, Form 10-K for 2025", AAL, "2025"),

    # Alaska
    r("alk.hawaiian", 1, "flag", "Alaska Air Group's results include Hawaiian 'for the post-acquisition period from September 18, "
      "2024'", "Alaska Air Group, Form 10-K for 2025", SEC + "766421/000076642126000010/alk-20251231.htm", "2024-09-18"),

    # The rule
    r("littlewood", 1, "flag", "Littlewood's rule: protect a seat for the higher fare while the probability that higher-fare demand "
      "exceeds the seats already protected is above the ratio of the lower fare to the higher", "K. Littlewood, 'Forecasting "
      "and control of passenger bookings', AGIFORS Symposium Proceedings 12 (1972); reprinted in the Journal of Revenue and "
      "Pricing Management 4(2), 2005", "https://doi.org/10.1057/palgrave.rpm.5170134", "1972", kind="study"),

    # The rescue of 2020
    r("cares.psp", 25, "US$ billion", "CARES Act section 4112(a)(1): financial assistance 'exclusively ... for the continuation of "
      "payment of employee wages, salaries, and benefits' to passenger air carriers, 'in an aggregate amount up to "
      "$25,000,000,000' (cargo carriers up to $4bn, contractors up to $3bn)", "Public Law 116-136, the CARES Act, 27 March 2020, "
      "section 4112 (15 USC 9072)", CARES, "2020-03-27", kind="official"),

    # The law and the investor
    r("ada.law", 1, "flag", "the Airline Deregulation Act, Public Law 95-504, 24 October 1978: 'to encourage, develop, and attain an "
      "air transportation system which relies on competitive market forces to determine the quality, variety, and price of "
      "air services'", "Public Law 95-504, 92 Stat. 1705", ADA, "1978-10-24", kind="official"),
    r("brk.kittyhawk", 1, "flag", "'if a farsighted capitalist had been present at Kitty Hawk, he would have done his successors a "
      "huge favor by shooting Orville down'", "Berkshire Hathaway, letter to shareholders for 2007 (Warren Buffett)", BRK,
      "2008-02"),
)
