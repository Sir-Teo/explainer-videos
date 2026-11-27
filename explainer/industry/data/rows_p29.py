"""Register rows for Part 29, *Rail, Trucks and Parcels*.  Checked 2026-11-27.

The Forms 10-K for 2025 of Union Pacific, UPS, Old Dominion, Knight-Swift, J.B. Hunt and Aurora, Union Pacific's 10-Q for
the third quarter of 2026, FedEx's 10-K for fiscal 2026, Aurora's 10-K for 2021 and its third-quarter 2026 letter, Yellow's
10-K for 2022 and Form 8-K of 7 August 2023; the Postal Service's report on Form 10-K for fiscal 2025; the Staggers Rail
Act of 1980; and FMCSA's Company Census File.  Series are the Filing Room's SEC and FRED extracts.
"""

from explainer.industry.register import Row, add

C = "2026-11-27"
P = (29,)
SEC = "https://www.sec.gov/Archives/edgar/data/"
UNP = SEC + "100885/000010088526000037/unp-20251231.htm"
UNPQ = SEC + "100885/000010088526000321/unp-20260930.htm"
UPS = SEC + "1090727/000162828026008432/ups-20251231.htm"
FDX = SEC + "1048911/000104891126000105/fdx-20260531.htm"
ODFL = SEC + "878927/000119312526067161/odfl-20251231.htm"
KNX = SEC + "1492691/000149269126000016/knx-20251231.htm"
JBHT = SEC + "728535/000143774926005294/jbht20251231_10k.htm"
AUR = SEC + "1828108/000182810826000016/aur-20251231.htm"
AUR21 = SEC + "1828108/000162828022005886/aur-20211231.htm"
AURQ3 = SEC + "1828108/000182810826000092/aurora26q3shareholderlet.htm"
YELL = SEC + "716006/000095017023002332/yell-20221231.htm"
YELL8K = SEC + "716006/000119312523204370/d483482d8k.htm"
USPS = "https://about.usps.com/what/financials/10k-reports/fy2025.pdf"
STAGGERS = "https://www.govinfo.gov/content/pkg/STATUTE-94/pdf/STATUTE-94-Pg1895.pdf"
FMCSA = "https://data.transportation.gov/resource/az4n-8mr2.json"


def r(key, value, unit, definition, source, url, fact, kind="filing", note="", **kw):
    return Row(key, value, unit, definition, source, url, fact, C, kind, note=note, parts=P, **kw)


def unp(key, value, unit, definition, fact="2025"):
    return r(key, value, unit, definition, "Union Pacific, Form 10-K for 2025", UNP, fact)


def ups(key, value, unit, definition, fact="2025"):
    return r(key, value, unit, definition, "United Parcel Service, Form 10-K for 2025", UPS, fact)


def fdx(key, value, unit, definition, fact="FY2026 (to 2026-05-31)"):
    return r(key, value, unit, definition, "FedEx, Form 10-K for fiscal 2026", FDX, fact)


def od(key, value, unit, definition, fact="2025"):
    return r(key, value, unit, definition, "Old Dominion Freight Line, Form 10-K for 2025", ODFL, fact)


def kx(key, value, unit, definition, fact="2025"):
    return r(key, value, unit, definition, "Knight-Swift Transportation, Form 10-K for 2025", KNX, fact)


def jb(key, value, unit, definition, fact="2025"):
    return r(key, value, unit, definition, "J.B. Hunt Transport Services, Form 10-K for 2025", JBHT, fact)


def usps(key, value, unit, definition, fact="FY2025 (to 2025-09-30)"):
    return r(key, value, unit, definition, "United States Postal Service, report on Form 10-K for fiscal 2025", USPS, fact,
             kind="official")


def fm(key, value, definition):
    return r(key, value, "carriers", definition + "; active, interstate, authorized for hire, by power units reported",
             "FMCSA Company Census File (data.transportation.gov), counted by this series", FMCSA, "2026-11-27",
             kind="official")


def wk(key, value, unit, definition, lo, hi):
    return r(key, value, unit, definition, "this series' assumption", "", "", kind="assumption", lo=lo, hi=hi)


add(
    # Union Pacific
    unp("up29.or", 59.8, "percent", "operating ratio, 2025: operating expenses over operating revenues (59.9% in 2024)"),
    unp("up29.freightrev", 23.2, "US$ billion", "freight revenues, 2025"),
    unp("up29.rtm", 426.9, "billion", "revenue ton-miles, 2025 (409.7 in 2024)"),
    unp("up29.route", 32889, "miles", "route miles, of which 26,294 owned"),
    unp("up29.emp", 29287, "people", "average employees, 2025"),
    unp("up29.merger", 88.82, "US$ a share", "agreement of 28 July 2025 to acquire Norfolk Southern: one Union Pacific share and $88.82 "
        "in cash for each Norfolk Southern share; about $20bn of cash; 'America's first transcontinental railroad that spans over "
        "50,000 miles across 43 states'; either side may terminate if not completed by 28 January 2028", "2025-07-28"),
    r("up29.stb", 1, "flag", "the joint application of 19 December 2025 was not accepted as complete on 16 January 2026; a revised "
      "application of 30 April 2026 was accepted on 28 May 2026; a procedural schedule was adopted on 18 August 2026; motions to "
      "dismiss were denied on 18 September 2026; completion 'currently expected ... in the second half of 2027'",
      "Union Pacific, Form 10-Q for the third quarter of 2026", UNPQ, "2026-09-30"),
    r("up29.or.q3", 59.1, "percent", "operating ratio, third quarter of 2026 (59.2% a year before)",
      "Union Pacific, Form 10-Q for the third quarter of 2026", UNPQ, "2026Q3"),

    # Parcels
    ups("ups29.adv", 20847, "thousand packages a day", "average daily package volume, 2025 (22,418 in 2024)"),
    ups("ups29.rpp", 14.50, "US$", "average revenue per piece, 2025 ($13.60 in 2024)"),
    ups("ups29.us.adv", 17510, "thousand packages a day", "US Domestic Package average daily volume, 2025 (19,161 in 2024)"),
    ups("ups29.us.rpp", 13.21, "US$", "US Domestic Package average revenue per piece, 2025 ($12.34 in 2024)"),
    ups("ups29.amazon", 10.6, "percent", "Amazon.com and affiliates' share of consolidated revenue, 2025; 'a targeted reduction of 50% "
        "by June 2026 from 2024 levels'"),
    ups("ups29.buildings", 93, "buildings", "buildings whose daily operations were closed in 2025 (85 permanently); 24 more identified "
        "for the first half of 2026"),
    ups("ups29.positions", 48000, "positions", "reduction of the operational workforce in 2025, including 15,000 fewer seasonal positions"),
    ups("ups29.union", 80, "percent", "'Nearly 80% of our U.S. employees are represented by unions, primarily those employees handling or "
        "transporting packages'"),
    ups("ups29.hourly", 385000, "people", "approximately 385,000 hourly employees and 75,000 management employees"),
    fdx("fdx29.adv", 17558, "thousand packages a day", "total average daily package volume, fiscal 2026 (17,001 in fiscal 2025)"),
    fdx("fdx29.yield", 16.80, "US$", "composite package yield, fiscal 2026 ($15.86 in fiscal 2025)"),
    fdx("fdx29.ground", 12.49, "US$", "US ground revenue per package, fiscal 2026"),
    fdx("fdx29.spin", 1, "flag", "'On June 1, 2026, we completed the Spin-Off' of FedEx Freight; FedEx kept 19.9% of its shares",
        "2026-06-01"),

    # Less than truckload
    od("od29.or", 75.2, "percent", "operating ratio, 2025 (73.4% in 2024)"),
    od("od29.sc", 260, "service centers", "service centers at 31 December 2025"),
    od("od29.union", 1, "flag", "'a single integrated, union-free organization'; 'we opened a net 16 and 35 service centers over the past "
       "five and ten years, respectively'"),
    r("yell29.network", 1, "flag", "'one of the largest networks of LTL service centers'", "Yellow Corporation, Form 10-K for 2022", YELL,
      "2022"),
    od("od29.cwt", 33.31, "US$", "LTL revenue per hundredweight, 2025"),
    od("od29.wps", 1477, "pounds", "LTL weight per shipment, 2025"),
    od("od29.haul", 911, "miles", "average length of haul, 2025"),
    od("od29.rps", 492.01, "US$", "LTL revenue per shipment, 2025"),
    od("od29.spd", 43762, "shipments a day", "LTL shipments per day, 2025 (47,288 in 2024)"),
    r("yell29.ch11", 1, "flag", "on 6 August 2023 Yellow Corporation and subsidiaries filed voluntary petitions under Chapter 11",
      "Yellow Corporation, Form 8-K of 7 August 2023", YELL8K, "2023-08-06"),
    r("yell29.emp", 30000, "people", "'we employed approximately 30,000 people as of December 31, 2022'",
      "Yellow Corporation, Form 10-K for 2022", YELL, "2022-12-31"),

    # Truckload and intermodal
    kx("kx29.revpt", 199897, "US$", "Truckload segment average revenue per tractor, excluding fuel surcharge, 2025"),
    kx("kx29.miles", 83650, "miles", "Truckload segment total miles per tractor, 2025"),
    kx("kx29.empty", 13.9, "percent", "Truckload segment non-paid empty miles, 2025"),
    kx("kx29.or", 97.0, "percent", "Truckload segment operating ratio, 2025 (96.7% in 2024)"),
    kx("kx29.rev", 4865.034, "US$ million", "Truckload segment total revenue, 2025 (4,283.398 excluding fuel surcharge)"),
    kx("kx29.tractors", 21428, "tractors", "Truckload segment average tractors, 2025 (19,395 company, 2,033 independent contractor)"),
    kx("kx29.downcycle", 1, "flag", "'Beginning in 2023, the freight market entered a prolonged downcycle characterized by moderated "
       "consumer demand, inventory overhangs, and a shift in consumer spending from goods toward services'", "2023-2025"),
    kx("kx29.fsc", 1, "flag", "'we utilize a fuel surcharge program to pass a majority of increases in fuel costs to our customers'"),
    kx("kx29.fleet", 1, "flag", "'operating one of the country's largest truckload fleets'"),
    jb("jb29.int.rpl", 2795, "US$", "Intermodal (JBI) revenue per load, 2025"),
    jb("jb29.int.haul", 1643, "miles", "Intermodal (JBI) average length of haul, 2025"),
    jb("jb29.int.loads", 2138191, "loads", "Intermodal (JBI) loads, 2025"),
    jb("jb29.tl.rpl", 1695, "US$", "Truckload (JBT) revenue per load, 2025"),
    jb("jb29.tl.haul", 596, "miles", "Truckload (JBT) average length of haul, 2025"),
    jb("jb29.carriers", 126400, "carriers", "approximate third-party carriers in its brokerage network (ICS), end of 2025 (110,000 a year before)"),

    # Half a million firms
    fm("fm29.total", 533278, "all"),
    fm("fm29.zero", 44488, "reporting no power units"),
    fm("fm29.one", 272151, "with one power unit"),
    fm("fm29.k2_5", 145922, "with two to five power units"),
    fm("fm29.k6_10", 30681, "with six to ten power units"),
    fm("fm29.k11_100", 36154, "with 11 to 100 power units"),
    fm("fm29.k101_1000", 3569, "with 101 to 1,000 power units"),
    fm("fm29.k1000", 313, "with more than 1,000 power units"),

    # The post
    usps("usps29.rev", 80.453, "US$ billion", "total operating revenue, fiscal 2025"),
    usps("usps29.loss", 8.978, "US$ billion", "net loss, fiscal 2025 ($9.5bn in fiscal 2024)"),
    usps("usps29.pkgrev", 32.580, "US$ billion", "Shipping and Packages revenue, fiscal 2025"),
    usps("usps29.pkgvol", 6.837, "billion pieces", "Shipping and Packages volume, fiscal 2025 (7.252bn in fiscal 2024)"),
    usps("usps29.fcm", 42.049, "billion pieces", "First-Class Mail volume, fiscal 2025"),
    usps("usps29.ppd", 2.4, "pieces", "average pieces delivered per delivery point per day, 2025 (5.5 in 2007)"),
    usps("usps29.mission", 1, "flag", "'We serve the American people in all areas of our nation, and through the universal service "
         "mission, bind our nation together'"),
    usps("usps29.ppd07", 5.5, "pieces", "average pieces delivered per delivery point per day, 2007", "2007"),
    usps("usps29.dp", 1.8, "million", "growth in delivery points in 2025"),
    usps("usps29.career", 531000, "people", "career employees at 30 September 2025 (about 93,000 pre-career)"),

    # Driverless trucks
    r("aur29.plan", 2023, "year", "'We plan to initially launch Aurora Horizon, our driverless trucking product, in late 2023 in Texas'",
      "Aurora Innovation, Form 10-K for 2021", AUR21, "2022-03"),
    r("aur29.launch", 2025, "year", "'In April 2025, we launched driverless commercial operations with Hirschbach and Uber Freight'",
      "Aurora Innovation, Form 10-K for 2025", AUR, "2025-04"),
    r("aur29.miles", 500000, "miles", "'in September the Aurora Driver surpassed 500,000 commercial driverless miles'; '20+ driverless "
      "trucks already built and coming into the fleet'", "Aurora Innovation, third-quarter 2026 shareholder letter (Form 8-K)",
      AURQ3, "2026-09"),
    r("aur29.target", 1000, "trucks", "'we remain on track to exit 2027 with more than 1,000 driverless trucks in operation'; 'exceeding "
      "the 200-truck milestone by the end of February'; a production ramp 'about six weeks behind our prior plan'",
      "Aurora Innovation, third-quarter 2026 shareholder letter (Form 8-K)", AURQ3, "2026-10-28"),

    # The law
    r("stag.findings", 1, "flag", "Staggers Rail Act, section 2: 'earnings by the railroad industry are the lowest of any transportation "
      "mode and are insufficient to generate funds for necessary capital improvements'; 'by 1985, there will be a capital "
      "shortfall ... of between $16,000,000,000 and $20,000,000,000'", "Public Law 96-448, 94 Stat. 1895, 14 October 1980",
      STAGGERS, "1980-10-14", kind="official"),

    r("stag.goals", 1, "flag", "Staggers Rail Act, section 3: 'The purpose of this Act is to provide for the restoration, maintenance, "
      "and improvement of the physical facilities and financial stability of the rail system of the United States'",
      "Public Law 96-448, 94 Stat. 1895, 14 October 1980", STAGGERS, "1980-10-14", kind="official"),
    r("up29.stb.rates", 1, "flag", "'The STB has jurisdiction over rates charged on certain regulated rail traffic; common carrier "
      "service of regulated traffic; ... transfer, extension, or abandonment of rail lines; and acquisition of control of rail "
      "common carriers'", "Union Pacific, Form 10-K for 2025", UNP, "2025"),

    # The Works
    wk("wk29.nonfuel", 2.05, "US$ a mile", "a truck's cost per mile driven, loaded or empty, before fuel: driver, tractor and trailer, "
       "insurance, maintenance and overhead (Knight-Swift's 2025 Truckload segment: revenue of $2.71 a mile at a 97.0% operating "
       "ratio, about $2.63 a mile of cost including fuel)", 1.80, 2.30),
    wk("wk29.mpg", 6.5, "miles a gallon", "a loaded tractor-trailer's fuel economy", 6.0, 7.5),
    wk("wk29.back", 1.60, "US$ a loaded mile", "the rate for a load home from a city that sends out less freight than it receives",
       1.20, 2.00),
    wk("wk29.pback", 0.6, "probability", "the chance of finding a load home", 0.4, 0.8),
    wk("wk29.wait", 1.0, "days", "days spent waiting for a load home", 0.5, 2.0),
    wk("wk29.day", 450.0, "US$ a day", "the cost of a truck and driver standing idle for a day", 300.0, 600.0),
    wk("wk29.fixed", 0.40, "share", "the share of a railway's operating costs that is fixed with the network (track, signals, "
       "structures and their upkeep) rather than with the traffic", 0.30, 0.50),
    wk("wk29.hour", 65.0, "US$ an hour", "a delivery driver and van, all costs", 50.0, 80.0),
    wk("wk29.dwell", 1.5, "minutes", "time at each delivery stop", 1.0, 2.5),
    wk("wk29.speed", 20.0, "miles an hour", "average speed between stops", 12.0, 30.0),
    wk("wk29.pps", 1.4, "packages", "packages delivered at each stop", 1.1, 2.0),
)
