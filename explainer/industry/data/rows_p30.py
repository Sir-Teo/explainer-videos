"""Register rows for Part 30, *Telecoms*.  Checked 2026-11-27.

The Forms 10-K for 2025 of Verizon, AT&T, T-Mobile, Charter, Comcast, American Tower and EchoStar; the 10-Qs for the third
quarter of 2026 of AT&T, Charter and Comcast; Verizon's 10-K for 2020 and AT&T's for 2021 on the C-band auction; DISH
Network's 10-K for 2019 on its network commitments.  Series are the Filing Room's SEC and FRED extracts.
"""

from explainer.industry.register import Row, add

C = "2026-11-27"
P = (30,)
SEC = "https://www.sec.gov/Archives/edgar/data/"
VZ = SEC + "732712/000073271226000007/vz-20251231.htm"
VZ20 = SEC + "732712/000073271221000012/vz-20201231.htm"
T = SEC + "732717/000073271726000120/t-20251231.htm"
TQ = SEC + "732717/000073271726000372/t-20260930.htm"
T21 = SEC + "732717/000073271722000015/t-20211231.htm"
TMUS = SEC + "1283699/000128369926000010/tmus-20251231.htm"
CHTR = SEC + "1091667/000109166726000017/chtr-20251231.htm"
CHTRQ = SEC + "1091667/000109166726000073/chtr-20260930.htm"
CMCSA = SEC + "1166691/000162828026004994/cmcsa-20251231.htm"
CMCSAQ = SEC + "1166691/000162828026066863/cmcsa-20260930.htm"
AMT = SEC + "1053507/000105350726000035/amt-20251231.htm"
SATS = SEC + "1415404/000110465926021817/tmb-20251231x10k.htm"
DISH = SEC + "1001082/000155837020000945/dish-20191231x10kce7e53.htm"


def r(key, value, unit, definition, source, url, fact, kind="filing", note="", **kw):
    return Row(key, value, unit, definition, source, url, fact, C, kind, note=note, parts=P, **kw)


def vz(key, value, unit, definition, fact="2025"):
    return r(key, value, unit, definition, "Verizon Communications, Form 10-K for 2025", VZ, fact)


def att(key, value, unit, definition, fact="2025"):
    return r(key, value, unit, definition, "AT&T, Form 10-K for 2025", T, fact)


def tm(key, value, unit, definition, fact="2025"):
    return r(key, value, unit, definition, "T-Mobile US, Form 10-K for 2025", TMUS, fact)


def amt(key, value, unit, definition, fact="2025"):
    return r(key, value, unit, definition, "American Tower, Form 10-K for 2025", AMT, fact)


def ech(key, value, unit, definition, fact="2025"):
    return r(key, value, unit, definition, "EchoStar, Form 10-K for 2025", SATS, fact)


def wk(key, value, unit, definition, lo, hi):
    return r(key, value, unit, definition, "this series' assumption", "", "", kind="assumption", lo=lo, hi=hi)


add(
    # Verizon
    vz("vz30.arpa", 147.31, "US$ a month", "Consumer wireless retail postpaid ARPA, 2025 ($144.00 in 2024)"),
    vz("vz30.churn", 0.92, "percent a month", "Consumer wireless retail postpaid phone churn, 2025 (0.83 in 2024)"),
    vz("vz30.cpa", 2.95, "connections", "Consumer wireless retail postpaid connections per account, 2025"),
    vz("vz30.accounts", 32384, "thousand", "Consumer wireless retail postpaid accounts, end of 2025"),
    vz("vz30.conn", 115903, "thousand", "Consumer wireless retail connections, end of 2025"),
    vz("vz30.fwa", 3407, "thousand", "Consumer FWA broadband connections, end of 2025 (2,714 a year before; 693 thousand added)"),
    vz("vz30.fios", 7328, "thousand", "Consumer Fios internet connections, end of 2025"),
    vz("vz30.svcrev", 112.721, "US$ billion", "service revenues and other, 2025"),
    vz("vz30.equiprev", 25.470, "US$ billion", "wireless equipment revenues, 2025"),
    vz("vz30.equipcost", 28.976, "US$ billion", "cost of wireless equipment, 2025"),
    vz("vz30.costsvc", 27.789, "US$ billion", "cost of services, 2025"),
    vz("vz30.sga", 33.818, "US$ billion", "selling, general and administrative expense, 2025"),
    vz("vz30.da", 18.349, "US$ billion", "depreciation and amortization expense, 2025"),
    vz("vz30.union", 27, "percent", "two unions 'represented approximately 27% of our employees as of December 31, 2025'"),
    vz("vz30.bands", 1, "flag", "spectrum held includes 700 MHz, 850 MHz cellular, PCS (1900 MHz), AWS, the 3.7 GHz band (C-Band) and "
       "millimeter wave spectrum in the 28, Upper 37 and 39 GHz bands"),
    vz("vz30.capex", 17.0, "US$ billion", "capital expenditures including capitalized software, 2025 ($17.1bn in 2024)"),
    vz("vz30.emp", 89900, "people", "approximately 89,900 full-time-equivalent employees at 31 December 2025"),
    vz("vz30.frontier", 1, "flag", "'On January 20, 2026, we completed the acquisition of Frontier', expanding its fiber footprint to 31 "
       "states and Washington D.C.", "2026-01-20"),
    r("vz30.cband", 45.5, "US$ billion", "FCC Auction 107 (C-Band): 'Cellco was the winning bidder with respect to approximately $45.5 "
      "billion of licenses'; the auction began on 8 December 2020 and results were announced on 24 February 2021",
      "Verizon Communications, Form 10-K for 2020", VZ20, "2021-02-24"),

    # AT&T
    r("att30.media", 1, "flag", "'In July 2021, we closed our transaction with TPG ... we separated our Video business'; 'On May 17, "
      "2021, we entered into an agreement to combine our WarnerMedia segment ... with a subsidiary of Discovery'", "AT&T, Form 10-K "
      "for 2021", T21, "2021"),
    tm("tm30.sprint", 1, "flag", "the Sprint Merger date of April 1, 2020", "2020-04-01"),
    att("att30.lumen", 1, "flag", "'our pending acquisition of substantially all of Lumen's Mass Markets fiber business'"),
    att("att30.churn", 0.90, "percent a month", "Mobility postpaid phone churn, 2025 (0.76 in 2024)"),
    att("att30.fiber", 10.4, "million", "fiber broadband connections at 31 December 2025 (and 1.5 million AT&T Internet Air)"),
    att("att30.aia", 1.5, "million", "AT&T Internet Air (fixed wireless) connections at 31 December 2025, 875,000 added in 2025"),
    r("att30.echostar", 22.65, "US$ billion", "'On July 28, 2026, we completed the acquisition of 600 MHz and 3.45 GHz ... licenses from "
      "EchoStar Corporation for $22,650' million", "AT&T, Form 10-Q for the third quarter of 2026", TQ, "2026-07-28"),
    r("att30.cband", 25.453, "US$ billion", "2021 acquisitions of $25,453 million, 'which includes C-Band spectrum licenses won in Auction "
      "107, associated capitalized interest, clearing and compensable relocation costs'", "AT&T, Form 10-K for 2021", T21, "2021"),

    # T-Mobile
    tm("tm30.churn", 0.93, "percent a month", "postpaid phone churn, 2025 (0.86 in 2024)"),
    tm("tm30.arpa", 148.97, "US$ a month", "postpaid ARPA, 2025 ($143.85 in 2024)"),
    tm("tm30.customers", 142388, "thousand", "total customers at 31 December 2025 (129,528 a year before), including 85,594 thousand "
       "postpaid phone"),
    tm("tm30.uscc", 1, "flag", "'On August 1, 2025 ... we completed the acquisition of the UScellular Wireless Business'", "2025-08-01"),

    # Cable
    r("ch30.internet", 29680, "thousand", "Charter total Internet customers at 31 December 2025 (30,083 a year before)",
      "Charter Communications, Form 10-K for 2025", CHTR, "2025-12-31"),
    r("ch30.mobile", 11766, "thousand", "Charter total mobile lines at 31 December 2025 (9,858 a year before); Spectrum Mobile uses "
      "Verizon's cellular network", "Charter Communications, Form 10-K for 2025", CHTR, "2025-12-31"),
    r("ch30.arpu", 119.05, "US$ a month", "Charter monthly residential revenue per residential customer, 2025 ($118.71 in 2024)",
      "Charter Communications, Form 10-K for 2025", CHTR, "2025"),
    r("ch30.cox", 1, "flag", "'On August 19, 2026, the transactions contemplated by the Transaction Agreement, dated May 16, 2025, "
      "by and among Charter, Charter Holdings, and Cox Enterprises ... were completed'", "Charter Communications, Form 10-Q for the "
      "third quarter of 2026", CHTRQ, "2026-08-19"),
    r("cm30.broadband", 31255, "thousand", "Comcast total domestic broadband customers at 31 December 2025: 'decreased by 711,000 to "
      "31.3 million' (411,000 fewer in 2024)", "Comcast, Form 10-K for 2025", CMCSA, "2025-12-31"),
    r("cm30.q3", 1, "flag", "'Domestic broadband revenue decreased for the three and nine months ended September 30, 2026 ... due "
      "to decreases in average rates and declines in the number of domestic broadband customers'",
      "Comcast, Form 10-Q for the third quarter of 2026", CMCSAQ, "2026-09-30"),

    # Towers
    amt("amt30.sites", 149686, "sites", "communications sites at 31 December 2025, 42,224 of them in the U.S. & Canada"),
    amt("amt30.us.sites", 42224, "sites", "communications sites in the U.S. & Canada at 31 December 2025"),
    amt("amt30.us.rev", 5248.7, "US$ million", "U.S. & Canada property segment revenues, 2025"),
    amt("amt30.us.opex", 870.0, "US$ million", "U.S. & Canada property segment operating expenses, 2025"),
    amt("amt30.us.profit", 4212.1, "US$ million", "U.S. & Canada property segment operating profit, 2025"),
    amt("amt30.tmus", 18, "percent", "T-Mobile's share of total revenues, 2025 (a significant customer)"),
    amt("amt30.att", 17, "percent", "AT&T's share of total revenues, 2025"),
    amt("amt30.vz", 14, "percent", "Verizon Wireless's share of total revenues, 2025"),
    amt("amt30.abroad", 1, "flag", "property segment revenues, 2025: U.S. & Canada $5,248.7m; Africa & APAC $1,422.9m; Europe $937.7m; "
        "Latin America $1,642.6m; Data Centers $1,053.1m"),
    amt("amt30.churn", 2, "percent", "'churn was approximately 2% of our tenant billings' in 2025"),

    # EchoStar and DISH
    ech("ech30.spacex", 20, "US$ billion", "spectrum sale to SpaceX: $17bn agreed on 7 September 2025, raised to 'approximately $20 "
        "billion, with up to $11 billion to be paid in SpaceX's Class A Common Stock'"),
    ech("ech30.end", 1, "flag", "'In August 2025, following these transactions, we terminated our deployment of our 5G Network, after "
        "meeting certain interim and final build-out requirements established by the FCC, and we began the abandonment and "
        "decommission process'; customers moved to AT&T's network as a 'Hybrid MNO'", "2025-08"),
    r("dish30.promise", 70, "percent", "'we committed to offer 5G broadband service to at least 70% of the U.S. population and to have "
      "deployed a core network no later than June 14, 2023' (600 MHz licenses)", "DISH Network, Form 10-K for 2019", DISH, "2020-02"),

    r("asts30.what", 1, "flag", "a network 'expected to provide connectivity to standard, unmodified, off-the-shelf mobile phones ... "
      "from the Company's satellite network'", "AST SpaceMobile, Form 10-K for 2025",
      SEC + "1780312/000178031226000006/asts-20251231.htm", "2025"),

    # The Works
    wk("wk30.margin", 0.45, "share", "the share of a wireless account's monthly bill left after the costs of serving it", 0.35, 0.55),
    wk("wk30.cac", 600.0, "US$", "the cost of winning a new account: promotions, device subsidy, commissions and advertising", 300.0, 1000.0),
    wk("wk30.tower", 300000.0, "US$", "the cost of building a macro tower", 200000.0, 400000.0),
    wk("wk30.rent", 45000.0, "US$ a year", "rent a tenant pays for space on a tower", 30000.0, 60000.0),
)
