"""Register rows for Part 19, *Machinery*.  Checked 2026-11-27.

The Forms 10-K of Caterpillar, Otis, United Rentals, Honeywell and 3M (2025) and Deere (fiscal 2025); the 10-Qs of
Caterpillar and Honeywell for the third quarter of 2026; GE Aerospace's 10-K (Part 18); the International Federation of
Robotics' press releases of 2022, 2024 and 2026.  Series are the Filing Room's SEC, FRED, robot and Comtrade extracts.
"""

from explainer.industry.register import Row, add

C = "2026-11-27"
P = (19,)
SEC = "https://www.sec.gov/Archives/edgar/data/"
CAT25 = SEC + "18230/000001823026000008/cat-20251231.htm"
CATQ3 = SEC + "18230/000001823026000057/cat-20260930.htm"
DE25 = SEC + "315189/000110465925122321/de-20251102x10k.htm"
OTIS25 = SEC + "1781335/000178133526000011/otis-20251231.htm"
URI25 = SEC + "1067701/000106770126000007/uri-20251231.htm"
HON25 = SEC + "773840/000077384026000013/hon-20251231.htm"
HONQ3 = SEC + "773840/000077384026000143/hon-20260930.htm"
MMM25 = SEC + "66740/000006674026000014/mmm-20251231.htm"
GE25 = SEC + "40545/000004054526000008/ge-20251231.htm"
IFR = "https://ifr.org/ifr-press-releases/news/"
IFR26 = IFR + "five-million-robots-now-operate-in-factories-globally"
IFRD = IFR + "robot-density-highest-in-south-korea-singapore-and-germany"
IFR22 = IFR + "wr-report-all-time-high-with-half-a-million-robots-installed"
IFR24 = IFR + "record-of-4-million-robots-working-in-factories-worldwide"


def r(key, value, unit, definition, source, url, fact, kind="filing", note="", **kw):
    return Row(key, value, unit, definition, source, url, fact, C, kind, note=note, parts=P, **kw)


def cat(key, value, unit, definition, fact="2025"):
    return r(key, value, unit, definition, "Caterpillar Inc., Form 10-K 2025", CAT25, fact)


def catq(key, value, unit, definition, fact="2026-09-30"):
    return r(key, value, unit, definition, "Caterpillar Inc., Form 10-Q for the third quarter of 2026", CATQ3, fact)


def otis(key, value, unit, definition, fact="2025"):
    return r(key, value, unit, definition, "Otis Worldwide Corporation, Form 10-K 2025", OTIS25, fact)


def de(key, value, unit, definition, fact="fiscal 2025"):
    return r(key, value, unit, definition, "Deere & Company, Form 10-K fiscal 2025", DE25, fact)


def uri(key, value, unit, definition, fact="2025"):
    return r(key, value, unit, definition, "United Rentals, Inc., Form 10-K 2025", URI25, fact)


def ifr(key, value, unit, definition, url=IFR26, fact="2025", source="International Federation of Robotics, press "
        "release of 24 September 2026 (World Robotics 2026)"):
    return r(key, value, unit, definition, source, url, fact, "study")


add(
    # Otis: the factory and the service business
    otis("otis.ne.sales", 4989, "US$ million", "New Equipment net sales (2024: 5,367; 2023: 5,812)"),
    otis("otis.ne.sales.2023", 5812, "US$ million", "New Equipment net sales, 2023", fact="2023"),
    otis("otis.sv.sales.2023", 8397, "US$ million", "Service net sales, 2023", fact="2023"),
    otis("otis.ne.op", 240, "US$ million", "New Equipment operating profit (margin 4.8%; 2024: 6.1%)"),
    otis("otis.sv.sales", 9442, "US$ million", "Service net sales (2024: 8,894; 2023: 8,397)"),
    otis("otis.sv.op", 2374, "US$ million", "Service operating profit (margin 25.1%; 2024: 24.6%)"),
    otis("otis.sv.share", 65, "percent", "Service's share of net sales (New Equipment 35%); of segment operating profit, "
         "Service 91% and New Equipment 9%"),
    otis("otis.units", 2.5, "million units", "'a maintenance portfolio of approximately 2.5 million units globally, which "
         "includes Otis equipment ... as well as equipment from other original equipment manufacturers'"),
    otis("otis.largest", 1, "flag", "Otis is 'the world's largest elevator and escalator manufacturing, installation and "
         "service company'"),
    otis("otis.rivals", 1, "flag", "'there are hundreds of participants that offer New Equipment solutions and several "
         "thousand participants that offer maintenance and service solutions'; major competitors 'include KONE Oyj, "
         "Schindler Group and TK Elevator'; in Service, 'independent service providers and other smaller' firms compete"),
    otis("otis.china", 50, "percent", "China: about a fifth of Otis's New Equipment net sales 'and over half of our global "
         "New Equipment unit volume'"),
    # Caterpillar
    cat("cat.rev", 67.589, "US$ billion", "total sales and revenues (2024: 64.809)"),
    cat("cat.op", 11.151, "US$ billion", "operating profit (2024: 13.072), down on 'unfavorable manufacturing costs of $2.148 "
        "billion and unfavorable price realization of $817 million'"),
    cat("cat.op.2024", 13.072, "US$ billion", "operating profit, 2024", fact="2024"),
    cat("cat.volume", 1.218, "US$ billion", "profit impact of higher sales volume, 2025"),
    cat("cat.mfg", -2.148, "US$ billion", "unfavorable manufacturing costs, 2025: 'Unfavorable manufacturing costs largely "
        "reflected the impact of higher tariffs'"),
    cat("cat.price", -817, "US$ million", "price realization, 2025 (unfavorable)"),
    cat("cat.backlog.2024", 30.0, "US$ billion", "order backlog believed to be firm, end of 2024", fact="2024-12-31"),
    cat("cat.backlog", 51.2, "US$ billion", "order backlog believed to be firm, end of 2025; the largest increase in Power & "
        "Energy", fact="2025-12-31"),
    cat("cat.dealers", 150, "dealers", "'a worldwide organization of dealers ... 41 located in the United States and 109 "
        "located outside the United States, serving 190 countries'; the large majority independently owned"),
    cat("cat.dealer.inv", 0.9, "US$ billion", "increase in total dealer inventory during 2025 (2024: about 0.4)"),
    cat("cat.ci.sales", 25.060, "US$ billion", "Construction Industries: total sales (profit 4.675)"),
    cat("cat.ci.profit", 4.675, "US$ billion", "Construction Industries: segment profit"),
    cat("cat.ri.sales", 12.474, "US$ billion", "Resource Industries: total sales (profit 1.988)"),
    cat("cat.ri.profit", 1.988, "US$ billion", "Resource Industries: segment profit"),
    cat("cat.pe.sales", 32.201, "US$ billion", "Power & Energy: total sales, up 12%; large reciprocating engines 'primarily "
        "data center applications'"),
    cat("cat.fp.dealers", 1, "flag", "Cat Financial's 'Dealer portfolio segment has not historically experienced large "
        "increases or decreases in credit losses based on changes in economic conditions due to its close working "
        "relationships with the dealers and their financial strength'"),
    cat("cat.fp.rev", 3.609, "US$ billion", "Financial Products revenues"),
    cat("cat.leading", 1, "flag", "'the world's leading manufacturer of construction and mining equipment, off-highway "
        "diesel and natural gas engines, industrial gas turbines and diesel-electric locomotives'"),
    cat("cat.founded", 1925, "year", "'Originally organized as Caterpillar Tractor Co. in 1925'"),
    cat("cat.pe.2024", 28.854, "US$ billion", "Power & Energy: total sales, 2024", fact="2024"),
    cat("cat.outlook", 7, "percent", "outlook for 2026 sales and revenues: 'to grow around the top end of our 5 to 7 percent "
        "compound annual growth rate (CAGR) target'", fact="2026 (forecast, made February 2026)"),
    catq("catq.outlook", 15, "percent", "'We continue to expect sales and revenues growth in the mid-to-high teens for 2026 "
         "as compared to 2025'", fact="2026 (forecast, made October 2026)"),
    catq("catq.pe", 8.784, "US$ billion", "Power & Energy: total sales in the third quarter of 2026, up 18%, 'mainly in "
         "turbines and turbine-related services and in large reciprocating engines, primarily in data center applications'"),
    catq("catq.sales", 20.682, "US$ billion", "total sales and revenues in the third quarter of 2026, up 17% (third quarter "
         "of 2025: 17.638)"),
    catq("catq.backlog", 78.1, "US$ billion", "order backlog believed to be firm at the end of the third quarter of 2026, "
         "$6.0bn above the second quarter; the largest increase in Power & Energy"),
    catq("catq.ieepa", 1.0, "US$ billion", "total IEEPA tariff costs during 2025 and until collection ceased in 2026, after "
         "the Supreme Court ruled on 20 February 2026 that the IEEPA tariffs were unauthorized"),
    catq("catq.tariff2026", 2.2, "US$ billion", "expected full-year 2026 tariff costs, excluding about $520m of IEEPA "
         "recoveries"),
    # Deere
    de("de.rev", 45.684, "US$ billion", "net sales and revenues, fiscal 2025 (production agriculture 16.960, small "
       "agriculture 7.215, turf 2.731, construction 4.570, compact construction 1.922, roadbuilding 3.552, forestry 1.124, "
       "financial products 6.296)"),
    de("de.fin", 6.296, "US$ billion", "revenue from financial products, fiscal 2025"),
    de("de.dealers", 2050, "dealer locations", "'approximately 2,050 independent dealer locations' in the US and Canada "
       "(about 1,600 agricultural, 450 construction and forestry)"),
    de("de.since", 1837, "year", "'John Deere has manufactured agricultural equipment since 1837'; parts, 'many of which "
       "are proprietary'"),
    # United Rentals
    uri("uri.rev", 16.099, "US$ billion", "total revenues (equipment rental 86%)"),
    uri("uri.oec", 22.48, "US$ billion", "fleet original equipment cost"),
    uri("uri.units", 1095000, "units", "equipment units in the fleet; fleet age 49.5 months"),
    uri("uri.age", 49.5, "months", "average fleet age (2024: 51.3)"),
    uri("uri.locations", 1768, "locations", "rental locations"),
    uri("uri.share", 15, "percent", "estimated North American market share; 'the largest equipment rental company in the "
        "world'"),
    # the conglomerates come apart
    r("ge.hc", 2023, "year", "GE HealthCare separated on 3 January 2023", "General Electric Company (GE Aerospace), Form "
      "10-K 2025", GE25, "2023-01-03"),
    r("ge.vernova", 2024, "year", "GE Vernova separated on 2 April 2024", "General Electric Company (GE Aerospace), Form "
      "10-K 2025", GE25, "2024-04-02"),
    r("mmm.solventum", 2024, "year", "3M 'completed the planned spin-off of its health care business, which is known as "
      "Solventum Corporation' on 1 April 2024", "3M Company, Form 10-K 2025", MMM25, "2024-04-01"),
    r("hon.solstice", 2025, "year", "Honeywell completed the spin-off of its Advanced Materials business, Solstice, on 30 "
      "October 2025", "Honeywell International, Form 10-K 2025", HON25, "2025-10-30"),
    r("hon.aero", 2026, "year", "Honeywell 'completed the previously announced separation of its Aerospace Technologies "
      "business into an independent, publicly traded company named Honeywell Aerospace Inc.' on 29 June 2026; the rest now "
      "operates as Honeywell Technologies", "Honeywell, Form 10-Q for the third quarter of 2026", HONQ3, "2026-06-29"),
    # robots (IFR)
    ifr("ifr.stock", 5.0, "million units", "operational stock of industrial robots, end of 2025, up 9%: 'more than double "
        "the number seven years ago'"),
    ifr("ifr.inst", 600000, "units", "industrial robots installed in 2025, 'more than 600,000', up 11%"),
    ifr("ifr.china", 354000, "units", "installed in China in 2025, up 20%: 59% of the world's installations"),
    ifr("ifr.china.dom", 55, "percent", "Chinese makers' share of China's installations, 2025 (195,000 units; 57% in 2024)"),
    ifr("ifr.china.dom.2024", 57, "percent", "Chinese makers' share of China's installations, 2024", fact="2024"),
    ifr("ifr.china.dom.2023", 47, "percent", "'The share of Chinese manufacturers in the domestic market has grown "
        "considerably since 2022, reaching 47% in 2023. It has fluctuated around 28% over the past decade.'", url=IFR24,
        fact="2023", source="International Federation of Robotics, press release of 24 September 2024"),
    ifr("ifr.china.dom.past", 28, "percent", "Chinese makers' share of China's installations, around which it 'fluctuated ... "
        "over the past decade' before 2022", url=IFR24, fact="about 2013-2022",
        source="International Federation of Robotics, press release of 24 September 2024"),
    ifr("ifr.us", 38500, "units", "installed in the United States in 2025, up 12%, now the second-largest market"),
    ifr("ifr.japan", 36219, "units", "installed in Japan in 2025, down 19%"),
    ifr("ifr.korea", 30000, "units", "installed in South Korea in 2025, down 1%"),
    ifr("ifr.germany", 25000, "units", "installed in Germany in 2025, 'fewer than 25,000', down 8%"),
    ifr("ifr.fc2026", 655000, "units", "forecast of world installations in 2026: 'rise by 9% to 655,000 units'"),
    ifr("ifr.fc2029", 806000, "units", "forecast of world installations in 2029"),
    ifr("ifr.d.kr", 1066, "robots per 10,000 manufacturing employees", "robot density, South Korea, 2025", url=IFRD,
        source="International Federation of Robotics, press release of 12 November 2026"),
    ifr("ifr.d.sg", 873, "robots per 10,000 manufacturing employees", "robot density, Singapore, 2025", url=IFRD,
        source="International Federation of Robotics, press release of 12 November 2026"),
    ifr("ifr.d.de", 469, "robots per 10,000 manufacturing employees", "robot density, Germany, 2025", url=IFRD,
        source="International Federation of Robotics, press release of 12 November 2026"),
    ifr("ifr.d.jp", 452, "robots per 10,000 manufacturing employees", "robot density, Japan, 2025", url=IFRD,
        source="International Federation of Robotics, press release of 12 November 2026"),
    ifr("ifr.d.us", 323, "robots per 10,000 manufacturing employees", "robot density, United States, 2025 (8th)", url=IFRD,
        source="International Federation of Robotics, press release of 12 November 2026"),
    ifr("ifr.d.eu", 240, "robots per 10,000 manufacturing employees", "robot density, the EU-27, 2025", url=IFRD,
        source="International Federation of Robotics, press release of 12 November 2026"),
    ifr("ifr.d.cn", 193, "robots per 10,000 manufacturing employees", "robot density, China, 2025 (19th; up 147% from "
        "2020)", url=IFRD, source="International Federation of Robotics, press release of 12 November 2026"),
    ifr("ifr.fc2022", 570000, "units", "October 2022: 'global robot installations are expected to grow by 10% to almost "
        "570,000 units in 2022'; 'From 2022 to 2025, average annual growth rates in the medium to upper single-digit range "
        "are forecast'", url=IFR22, fact="2022 (forecast)",
        source="International Federation of Robotics, press release of 13 October 2022"),
    ifr("ifr.japan.maker", 186102, "units", "'Japan is the world's predominant robot manufacturing country: Exports of "
        "Japanese industrial robots achieved a new peak level at 186,102 units in 2021'", url=IFR22, fact="2021",
        source="International Federation of Robotics, press release of 13 October 2022"),
    ifr("ifr.act2022", 552946, "units", "world installations in 2022 (the record until 2025)", url=IFR24, fact="2022",
        source="International Federation of Robotics, press release of 24 September 2024"),
    ifr("ifr.fc2024", 541000, "units", "September 2024: 'Global robot installations are expected to level off at 541,000 "
        "units' in 2024", url=IFR24, fact="2024 (forecast)",
        source="International Federation of Robotics, press release of 24 September 2024"),
    ifr("ifr.act2023", 541302, "units", "world installations in 2023", url=IFR24, fact="2023",
        source="International Federation of Robotics, press release of 24 September 2024"),
)
