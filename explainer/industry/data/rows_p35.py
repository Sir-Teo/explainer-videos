"""Register rows for Part 35, *Travel and Hotels*.  Checked 2026-11-28.

The Forms 10-K for 2025 of Marriott International, Hilton, Host Hotels & Resorts, Booking Holdings, Expedia, Airbnb,
Royal Caribbean and Las Vegas Sands, Carnival's for the year to 30 November 2025 and Disney's for the year to 3 October
2026; the 10-Qs for the third quarter of 2026 of Marriott and Booking; Host Marriott's 10-K for 1993; Park Hotels'
10-K for 2020; Booking's 10-Ks for 2020 and 2023, Carnival's for 2020 and Las Vegas Sands' for 2019 and 2020; the Nevada
Gaming Control Board's gaming revenue report for December 2025.  Series are the Filing Room's SEC and FRED extracts.
"""

from explainer.industry.register import Row, add

C = "2026-11-28"
P = (35,)
SEC = "https://www.sec.gov/Archives/edgar/data/"
MAR = SEC + "1048286/000104828626000007/mar-20251231.htm"
MARQ = SEC + "1048286/000104828626000043/mar-20260930.htm"
HLT = SEC + "1585689/000158568926000007/hlt-20251231.htm"
HST = SEC + "1070750/000107075026000054/hst-20251231.htm"
HMC93 = SEC + "314733/0000950109-94-000600.txt"
PK20 = SEC + "1617406/000156459021009414/pk-10k_20201231.htm"
BKNG = SEC + "1075531/000107553126000009/bkng-20251231.htm"
BKNG20 = SEC + "1075531/000107553121000019/bkng-20201231.htm"
BKNG23 = SEC + "1075531/000107553124000014/bkng-20231231.htm"
BKNGQ = SEC + "1075531/000107553126000045/bkng-20260930.htm"
EXPE = SEC + "1324424/000132442426000008/expe-20251231.htm"
ABNB = SEC + "1559720/000155972026000004/abnb-20251231.htm"
CCL = SEC + "815097/000081509726000007/ccl-20251130.htm"
CCL20 = SEC + "815097/000081509721000027/ccl-20201130.htm"
RCL = SEC + "884887/000088488726000007/rcl-20251231.htm"
LVS = SEC + "1300514/000130051426000013/lvs-20251231.htm"
LVS19 = SEC + "1300514/000130051420000011/lvs-20191231x10k.htm"
LVS20 = SEC + "1300514/000130051421000033/lvs-20201231.htm"
DIS = SEC + "1744489/000174448926000066/dis-20261003.htm"
NV = "https://www.gaming.nv.gov/siteassets/content/about/gaming-revenue/december-2025-monthly-revenue-report.pdf"


def r(key, value, unit, definition, source, url, fact, kind="filing", note="", **kw):
    return Row(key, value, unit, definition, source, url, fact, C, kind, note=note, parts=P, **kw)


def mar(key, value, unit, definition, fact="2025"):
    return r(key, value, unit, definition, "Marriott International, Form 10-K for 2025", MAR, fact)


def hlt(key, value, unit, definition, fact="2025"):
    return r(key, value, unit, definition, "Hilton Worldwide, Form 10-K for 2025", HLT, fact)


def hst(key, value, unit, definition, fact="2025"):
    return r(key, value, unit, definition, "Host Hotels & Resorts, Form 10-K for 2025", HST, fact)


def bk(key, value, unit, definition, fact="2025"):
    return r(key, value, unit, definition, "Booking Holdings, Form 10-K for 2025", BKNG, fact)


def ccl(key, value, unit, definition, fact="FY2025"):
    return r(key, value, unit, definition, "Carnival Corporation & plc, Form 10-K for the year to 30 November 2025", CCL, fact)


def lvs(key, value, unit, definition, fact="2025"):
    return r(key, value, unit, definition, "Las Vegas Sands, Form 10-K for 2025", LVS, fact)


def nv(key, value, unit, definition):
    return r(key, value, unit, definition, "Nevada Gaming Control Board, gaming revenue report, December 2025 (twelve months)",
             NV, "2025", kind="official")


def dis(key, value, unit, definition, fact="FY2026"):
    return r(key, value, unit, definition, "The Walt Disney Company, Form 10-K for the year to 3 October 2026", DIS, fact)


def wk(key, value, unit, definition, lo, hi):
    return r(key, value, unit, definition, "this series' assumption", "", "", kind="assumption", lo=lo, hi=hi)


add(
    # Marriott
    mar("ma35.props", 9805, "properties", "properties in its system at year-end 2025 (1,779,936 rooms) in 145 countries and territories; "
        "'we own or lease very few of our lodging properties (less than one percent of our system)'", "2025-12-31"),
    mar("ma35.rooms", 1779936, "rooms", "rooms in its system at year-end 2025 (1,706,331 a year before)", "2025-12-31"),
    mar("ma35.fr.props", 7644, "properties", "franchised, licensed and other properties at year-end 2025", "2025-12-31"),
    mar("ma35.fr.rooms", 1183513, "rooms", "franchised, licensed and other rooms at year-end 2025", "2025-12-31"),
    mar("ma35.mg.props", 1966, "properties", "managed properties at year-end 2025", "2025-12-31"),
    mar("ma35.mg.rooms", 565764, "rooms", "managed rooms at year-end 2025", "2025-12-31"),
    mar("ma35.own.props", 51, "properties", "owned or leased properties at year-end 2025", "2025-12-31"),
    mar("ma35.own.rooms", 14406, "rooms", "owned or leased rooms at year-end 2025", "2025-12-31"),
    mar("ma35.res.rooms", 16253, "rooms", "residential units at year-end 2025 (144 properties)", "2025-12-31"),
    mar("ma35.franchise", 3.325, "US$ billion", "franchise fees, 2025 (including co-branded credit card and other brand fees)"),
    mar("ma35.base", 1.322, "US$ billion", "base management fees, 2025"),
    mar("ma35.incentive", 0.791, "US$ billion", "incentive management fees, 2025"),
    mar("ma35.fees", 5.438, "US$ billion", "gross fee revenues, 2025 ($5,170m in 2024)"),
    mar("ma35.owned", 1.679, "US$ billion", "owned, leased and other revenue, 2025"),
    mar("ma35.reimb", 19.204, "US$ billion", "cost reimbursement revenue, 2025: costs incurred for hotel owners, chiefly payroll at managed "
        "hotels, reimbursed 'with no added mark-up'"),
    mar("ma35.rev", 26.186, "US$ billion", "total revenues, 2025"),
    mar("ma35.roy.lo", 4, "percent", "franchise royalty fees 'typically range from four to seven percent of room revenues, plus for certain "
        "brands, up to four percent of food and beverage revenues'"),
    mar("ma35.roy.hi", 7, "percent", "the top of that range"),
    mar("ma35.imf", 69, "percent", "share of its managed hotels worldwide paying incentive management fees in 2025 (32% in the U.S. & Canada, "
        "85% internationally)"),
    mar("ma35.imf.us", 32, "percent", "share of its U.S. & Canada managed hotels paying incentive management fees, 2025"),
    mar("ma35.imf.intl", 85, "percent", "share of its international managed hotels paying incentive management fees, 2025"),
    mar("ma35.loyal.us", 75, "percent", "share of its U.S. hotel room nights booked by Loyalty Program members, 2025"),
    mar("ma35.loyal", 68, "percent", "share of its global hotel room nights booked by Loyalty Program members, 2025"),
    mar("ma35.revpar", 128.80, "US$", "worldwide comparable systemwide RevPAR, 2025 (+2.0%)"),
    mar("ma35.occ", 69.3, "percent", "worldwide comparable systemwide occupancy, 2025"),
    mar("ma35.adr", 185.81, "US$", "worldwide comparable systemwide average daily rate, 2025"),
    mar("ma35.pipe", 610000, "rooms", "rooms in its development pipeline at year-end 2025 ('nearly 610,000 rooms', about 4,100 properties)"),
    mar("ma35.card", 105, "US$ million", "increase in co-branded credit card and other brand-related fees, 2025"),
    r("ma35.q3", 1833801, "rooms", "rooms in its system at the end of the third quarter of 2026 (10,241 properties); it expects 2026 net "
      "rooms growth 'toward the low end of our 4.5 to 5.0 percent range'", "Marriott International, Form 10-Q for the third quarter "
      "of 2026", MARQ, "2026-09-30"),
    r("hm35.split", 1, "flag", "'Prior to October 8, 1993, the Company was named Marriott Corporation'; on 8 October 1993 it distributed "
      "Marriott International, which held 'all of the assets relating to the Management Business'; it kept the 'Ownership Business'. "
      "'The Distribution was designed to separate two types of businesses with distinct financial, investment and operating "
      "characteristics'", "Host Marriott Corporation, Form 10-K for 1993", HMC93, "1993-10-08"),

    # Hilton
    hlt("hl35.hotels", 9044, "hotels", "hotels in its system at 31 December 2025 (1,330,947 rooms), excluding timeshare", "2025-12-31"),
    hlt("hl35.rooms", 1330947, "rooms", "hotel rooms at 31 December 2025", "2025-12-31"),
    hlt("hl35.own.rooms", 15287, "rooms", "owned and leased hotel rooms (46 hotels)", "2025-12-31"),
    hlt("hl35.mg.rooms", 264760, "rooms", "managed hotel rooms (873 hotels)", "2025-12-31"),
    hlt("hl35.fr.rooms", 1050900, "rooms", "franchised and licensed hotel rooms (8,125 hotels)", "2025-12-31"),
    hlt("hl35.franchise", 2.780, "US$ billion", "franchise and licensing fees, 2025"),
    hlt("hl35.mgmt", 0.689, "US$ billion", "base and other ($376m) and incentive ($313m) management fees, 2025"),
    hlt("hl35.owned", 1.233, "US$ billion", "ownership revenues, 2025"),
    hlt("hl35.reimb", 7.085, "US$ billion", "cost reimbursement revenues, 2025"),
    hlt("hl35.rev", 12.039, "US$ billion", "total revenues, 2025"),
    hlt("hl35.honors", 243, "million", "Hilton Honors members at 31 December 2025, up 15% in a year", "2025-12-31"),
    hlt("hl35.revpar", 114.39, "US$", "system-wide comparable RevPAR, 2025 (occupancy 71.5%, ADR $159.89)"),
    hlt("hl35.occ", 71.5, "percent", "system-wide comparable occupancy, 2025"),
    hlt("hl35.adr", 159.89, "US$", "system-wide comparable average daily rate, 2025"),
    hlt("hl35.nug", 6.7, "percent", "net unit growth, 2025"),
    hlt("hl35.pipe", 520500, "rooms", "rooms in its development pipeline at 31 December 2025 (3,703 hotels)", "2025-12-31"),
    r("hl35.spin", 1, "flag", "'On January 3, 2017, Hilton Parent completed the spin-off that resulted in our establishment as an "
      "independent, publicly traded company' (Park Hotels & Resorts, the hotels Hilton owned)", "Park Hotels & Resorts, Form 10-K "
      "for 2020", PK20, "2017-01-03"),

    # Host
    hst("hs35.hotels", 76, "hotels", "consolidated hotels at 20 February 2026 (41,839 rooms at year-end 2025)", "2026-02-20"),
    hst("hs35.rooms", 41839, "rooms", "rooms in its 76 consolidated hotels, year-end 2025", "2025-12-31"),
    hst("hs35.marriott", 64, "percent", "share of its hotels, by 2025 hotel revenues, managed or franchised by Marriott International"),
    hst("hs35.rev.rooms", 60, "percent", "rooms revenues, share of 2025 hotel revenues"),
    hst("hs35.rev.fb", 30, "percent", "food and beverage revenues, share of 2025 hotel revenues"),
    hst("hs35.rev.other", 10, "percent", "other revenues, share of 2025 hotel revenues"),
    hst("hs35.c.rooms", 18, "percent", "rooms expenses, share of its 2025 operating costs and expenses"),
    hst("hs35.c.fb", 24, "percent", "food and beverage expenses, share of its 2025 operating costs and expenses"),
    hst("hs35.c.dept", 29, "percent", "other departmental and support expenses, share of its 2025 operating costs and expenses"),
    hst("hs35.c.mgmt", 5, "percent", "management fees, share of its 2025 operating costs and expenses"),
    hst("hs35.c.prop", 8, "percent", "other property-level expenses (property taxes, ground rent, insurance), share of 2025 costs"),
    hst("hs35.c.da", 16, "percent", "depreciation and amortization, share of its 2025 operating costs and expenses"),
    hst("hs35.wages", 58, "percent", "wages and benefits, share of its rooms, food and beverage, and other departmental and support expenses"),
    hst("hs35.fee.base", 2.5, "percent", "base management fee 'generally 2-3%' of annual gross revenues (midpoint)"),
    hst("hs35.fee.inc", 15, "percent", "incentive management fee 'generally 10-20%' of operating profit after the owner's priority return "
        "(midpoint)"),
    hst("hs35.margin", 28.9, "percent", "comparable hotel EBITDA margin, 2025 (29.3% in 2024)"),
    hst("hs35.revpar", 229.24, "US$", "comparable hotel RevPAR, 2025 (+3.8%)"),
    hst("hs35.trevpar", 382.83, "US$", "comparable hotel total RevPAR, 2025"),
    hst("hs35.opm", 14.0, "percent", "operating profit margin, 2025"),

    # Booking, Expedia, Airbnb
    bk("bk35.rev", 26.917, "US$ billion", "total revenues, 2025 ($23,739m in 2024)"),
    bk("bk35.merchant", 17.755, "US$ billion", "merchant revenues, 2025"),
    bk("bk35.agency", 7.968, "US$ billion", "agency revenues, 2025"),
    bk("bk35.ads", 1.194, "US$ billion", "advertising and other revenues, 2025 (KAYAK, OpenTable and others)"),
    bk("bk35.gb", 186.107, "US$ billion", "total gross bookings, 2025 (merchant $130,025m, agency $56,082m); revenues 14.5% of gross bookings"),
    bk("bk35.gb.merchant", 130.025, "US$ billion", "merchant gross bookings, 2025"),
    bk("bk35.gb.agency", 56.082, "US$ billion", "agency gross bookings, 2025 ($61,398m in 2024)"),
    bk("bk35.nights", 1235, "million", "room nights, 2025 (1,144 million in 2024)"),
    bk("bk35.mkt", 8.2, "US$ billion", "performance and brand marketing expenses, 2025 (up 12.5%)"),
    bk("bk35.op", 8.825, "US$ billion", "operating income, 2025"),
    bk("bk35.ni", 5.404, "US$ billion", "net income, 2025"),
    bk("bk35.props", 4.4, "million", "properties offered by Booking.com at 31 December 2025: about 500,000 hotels, motels and resorts and 3.9 "
       "million homes, apartments and other places", "2025-12-31"),
    bk("bk35.hotels", 0.5, "million", "hotels, motels and resorts on Booking.com at 31 December 2025", "2025-12-31"),
    bk("bk35.cnmc", 1, "flag", "'In 2024, the Comisión Nacional de los Mercados y la Competencia in Spain (the \"CNMC\") imposed a fine and "
       "restricted certain of Booking.com's business practices such as those relating to contractual parity provisions and the "
       "ranking criteria'; designated a gatekeeper under the EU Digital Markets Act"),
    r("bk35.n19", 845, "million", "room nights, 2019", "Booking Holdings, Form 10-K for 2020", BKNG20, "2019"),
    r("bk35.n20", 355, "million", "room nights, 2020", "Booking Holdings, Form 10-K for 2020", BKNG20, "2020"),
    r("bk35.r19", 15.066, "US$ billion", "total revenues, 2019", "Booking Holdings, Form 10-K for 2020", BKNG20, "2019"),
    r("bk35.r20", 6.796, "US$ billion", "total revenues, 2020", "Booking Holdings, Form 10-K for 2020", BKNG20, "2020"),
    r("bk35.n21", 591, "million", "room nights, 2021", "Booking Holdings, Form 10-K for 2023", BKNG23, "2021"),
    r("bk35.n22", 896, "million", "room nights, 2022", "Booking Holdings, Form 10-K for 2023", BKNG23, "2022"),
    r("bk35.n23", 1049, "million", "room nights, 2023 ('up about 24% versus 2019')", "Booking Holdings, Form 10-K for 2023", BKNG23, "2023"),
    r("bk35.r22", 17.090, "US$ billion", "total revenues, 2022", "Booking Holdings, Form 10-K for 2023", BKNG23, "2022"),
    r("bk35.r23", 21.365, "US$ billion", "total revenues, 2023", "Booking Holdings, Form 10-K for 2023", BKNG23, "2023"),
    r("bk35.n24", 1144, "million", "room nights, 2024", "Booking Holdings, Form 10-K for 2025", BKNG, "2024"),
    r("bk35.r24", 23.739, "US$ billion", "total revenues, 2024", "Booking Holdings, Form 10-K for 2025", BKNG, "2024"),
    r("bk35.warn", 1, "flag", "'We expect to continue to see severely reduced new travel and restaurant reservation bookings as compared to "
      "2019 levels for the foreseeable future'; in its goodwill test 'we expected that OpenTable and KAYAK would not return to the 2019 "
      "level of profitability within the next five years'", "Booking Holdings, Form 10-K for 2020", BKNG20, "2021-02"),
    r("bk35.q9", 1007, "million", "room nights in the first nine months of 2026 (951 million a year before, +6.0%; third quarter +6.7%)",
      "Booking Holdings, Form 10-Q for the third quarter of 2026", BKNGQ, "2026-09-30"),
    r("ex35.gb", 119.590, "US$ billion", "total gross bookings, 2025 (revenue margin 12.3%)", "Expedia Group, Form 10-K for 2025", EXPE, "2025"),
    r("ex35.rev", 14.733, "US$ billion", "total revenue, 2025", "Expedia Group, Form 10-K for 2025", EXPE, "2025"),
    r("ab35.gbv", 91.273, "US$ billion", "gross booking value, 2025 ($81,784m in 2024)", "Airbnb, Form 10-K for 2025", ABNB, "2025"),
    r("ab35.nights", 533, "million", "nights and seats booked, 2025 (492 million in 2024)", "Airbnb, Form 10-K for 2025", ABNB, "2025"),
    r("ab35.rev", 12.241, "US$ billion", "revenue, 2025", "Airbnb, Form 10-K for 2025", ABNB, "2025"),
    r("ab35.ni", 2.511, "US$ billion", "net income, 2025", "Airbnb, Form 10-K for 2025", ABNB, "2025"),
    r("ab35.hosts", 5, "million", "'a global community of over 5 million hosts who have welcomed over 2.5 billion guest arrivals'",
      "Airbnb, Form 10-K for 2025", ABNB, "2025"),
    r("ab35.nyc", 1, "flag", "'New York City passed regulations in 2023, which resulted in a de facto ban of short-term rental activities'",
      "Airbnb, Form 10-K for 2025", ABNB, "2023"),

    # Cruise lines
    ccl("cc35.ticket", 17.419, "US$ billion", "passenger ticket revenues, 2025 (65% of revenues)"),
    ccl("cc35.onboard", 9.202, "US$ billion", "onboard and other revenues, 2025"),
    ccl("cc35.rev", 26.622, "US$ billion", "total revenues, 2025"),
    ccl("cc35.c.comm", 3.331, "US$ billion", "commissions, transportation and other, 2025"),
    ccl("cc35.c.onboard", 2.816, "US$ billion", "onboard and other costs, 2025"),
    ccl("cc35.c.pay", 2.589, "US$ billion", "payroll and related, 2025"),
    ccl("cc35.c.fuel", 1.808, "US$ billion", "fuel, 2025"),
    ccl("cc35.c.food", 1.499, "US$ billion", "food, 2025"),
    ccl("cc35.c.other", 3.904, "US$ billion", "other ship operating, 2025"),
    ccl("cc35.c.sga", 3.402, "US$ billion", "selling and administrative, 2025"),
    ccl("cc35.c.da", 2.790, "US$ billion", "depreciation and amortization, 2025"),
    ccl("cc35.op", 4.483, "US$ billion", "operating income, 2025"),
    ccl("cc35.int", 1.349, "US$ billion", "interest expense net of capitalized interest, 2025"),
    ccl("cc35.ni", 2.760, "US$ billion", "net income, 2025"),
    ccl("cc35.occ", 105, "percent", "occupancy, 2025: passenger cruise days over available lower berth days (two to a cabin)"),
    ccl("cc35.pax", 13.6, "million", "passengers carried, 2025"),
    ccl("cc35.albd", 96.5, "million", "available lower berth days, 2025"),
    ccl("cc35.deposits", 6.831, "US$ billion", "customer deposits at 30 November 2025: 'substantially all of our passenger ticket receipts "
        "are collected in advance'", "2025-11-30"),
    ccl("cc35.debt", 26.640, "US$ billion", "long-term debt ($24,037m) and its current portion ($2,603m) at 30 November 2025", "2025-11-30"),
    ccl("cc35.berths", 272460, "berths", "its passenger capacity at 31 December 2025 (764,310 for the global industry, from Cruise Industry "
        "News); with Royal Caribbean, Norwegian and MSC 'approximately 80% of the cruise industry capacity'", "2025-12-31"),
    ccl("cc35.industry", 764310, "berths", "global cruise industry passenger capacity at 31 December 2025, as the 10-K quotes Cruise "
        "Industry News", "2025-12-31"),
    ccl("cc35.crew", 101000, "people", "average employees on board its ships, 2025; shipboard and shoreside employees "
        "'sourced from approximately 150 countries'"),
    ccl("cc35.debtcut", 10, "US$ billion", "'reduced total debt by over $10 billion since our peak in January 2023'"),
    ccl("cc35.orders", 7, "ships", "'a total of seven cruise ships expected to be delivered through 2033'", "2025-11-30"),
    r("cc35.r19", 20.825, "US$ billion", "total revenues, 2019 (ticket $14,104m, onboard $6,721m)", "Carnival, Form 10-K for 2020", CCL20, "FY2019"),
    r("cc35.ni19", 2.990, "US$ billion", "net income, 2019", "Carnival, Form 10-K for 2020", CCL20, "FY2019"),
    r("cc35.r20", 5.595, "US$ billion", "total revenues, 2020", "Carnival, Form 10-K for 2020", CCL20, "FY2020"),
    r("cc35.ni20", -10.236, "US$ billion", "net loss, 2020; 'we paused our guest cruise operations in mid-March' 2020, and 'As of January "
      "14, 2021, none of our ships were operating with guests onboard'", "Carnival, Form 10-K for 2020", CCL20, "FY2020"),
    r("rc35.ticket", 12.515, "US$ billion", "passenger ticket revenues, 2025", "Royal Caribbean Group, Form 10-K for 2025", RCL, "2025"),
    r("rc35.onboard", 5.419, "US$ billion", "onboard and other revenues, 2025", "Royal Caribbean Group, Form 10-K for 2025", RCL, "2025"),

    # Casinos
    lvs("lv35.casino", 9.789, "US$ billion", "net casino revenues, 2025"),
    lvs("lv35.rooms", 1.422, "US$ billion", "rooms revenues, 2025"),
    lvs("lv35.fb", 0.644, "US$ billion", "food and beverage revenues, 2025"),
    lvs("lv35.mall", 0.801, "US$ billion", "mall revenues, 2025"),
    lvs("lv35.other", 0.361, "US$ billion", "convention, retail and other revenues, 2025"),
    lvs("lv35.rev", 13.017, "US$ billion", "total net revenues, 2025"),
    lvs("lv35.macau", 2.310, "US$ billion", "adjusted property EBITDA of its Macao properties and ferries, 2025"),
    lvs("lv35.mbs", 2.922, "US$ billion", "adjusted property EBITDA of Marina Bay Sands, Singapore, 2025 ($2,052m in 2024)"),
    lvs("lv35.ggr25", 247.40, "MOP billion", "Macao's gross gaming revenues in 2025, from the DICJ (about $30.87bn; +9.1%)"),
    lvs("lv35.tax", 35, "percent", "Macao's special gaming tax on gross gaming revenues; concessionaires also contribute 5% of gross gaming "
        "revenue to designated public funds"),
    lvs("lv35.contrib", 5, "percent", "contributions of gross gaming revenue to entities designated by the Macao government"),
    lvs("lv35.rolling", 3.3, "percent", "expected Rolling Chip (VIP) win percentage in Macao"),
    lvs("lv35.lvsale", 6.25, "US$ billion", "aggregate price of 'the Las Vegas Sale' of The Venetian Resort Las Vegas and the Sands Expo, "
        "completed in 2022"),
    r("lv35.ggr19", 293.31, "MOP billion", "Macao's gaming revenues in 2019, from the DICJ (about $36.6bn)", "Las Vegas Sands, Form 10-K "
      "for 2019", LVS19, "2019"),
    r("lv35.ggr19.usd", 36.6, "US$ billion", "Macao's gaming revenues in 2019 in dollars, 'approximately $36.6 billion at exchange "
      "rates in effect on December 31, 2019'", "Las Vegas Sands, Form 10-K for 2019", LVS19, "2019"),
    r("lv35.sg", 2, "concessions", "'In 2006, the Singapore government awarded two concessions to develop and operate two Integrated "
      "Resorts'", "Las Vegas Sands, Form 10-K for 2025", LVS, "2006"),
    r("lv35.ggr20", 60.44, "MOP billion", "Macao's gross gaming revenues in 2020, from the DICJ (about $7.57bn), down 79.3%",
      "Las Vegas Sands, Form 10-K for 2020", LVS20, "2020"),
    nv("nv35.strip", 8.815212, "US$ billion", "Las Vegas Strip gaming win, 1 January to 31 December 2025, all nonrestricted locations"),
    nv("nv35.tables", 3.865039, "US$ billion", "Strip table, counter and card games win, 2025 (win percent 14.91)"),
    nv("nv35.tablepct", 14.91, "percent", "Strip table games win percent, 2025 (win over drop, adjusted for credit play)"),
    nv("nv35.bacc", 1.409598, "US$ billion", "Strip baccarat win, 2025 (win percent 16.27)"),
    nv("nv35.slots", 4.950173, "US$ billion", "Strip slot machine win, 2025 (win percent 7.83)"),
    nv("nv35.slotpct", 7.83, "percent", "Strip slot machines win percent, 2025 (win over the amount played)"),
    nv("nv35.state", 15.212050, "US$ billion", "Nevada statewide taxable gaming revenue, 2025 (+1.54%)"),

    # Disney
    dis("ds35.rev", 39.566, "US$ billion", "Experiences segment revenues, fiscal 2026"),
    dis("ds35.adm", 12.709, "US$ billion", "theme park admissions, fiscal 2026"),
    dis("ds35.resorts", 10.544, "US$ billion", "resorts and vacations (hotel nights, cruises, vacation club), fiscal 2026"),
    dis("ds35.merch", 9.124, "US$ billion", "Parks & Experiences merchandise, food and beverage, fiscal 2026"),
    dis("ds35.lic", 4.645, "US$ billion", "merchandise licensing, branded retail and publishing, fiscal 2026"),
    dis("ds35.plic", 2.544, "US$ billion", "parks licensing and other, including royalties on Tokyo Disney Resort revenues, fiscal 2026"),
    dis("ds35.op", 11.191, "US$ billion", "Experiences segment operating income, fiscal 2026 ($9,995m in fiscal 2025)"),
    dis("ds35.ent", 5.443, "US$ billion", "Entertainment segment operating income, fiscal 2026"),
    dis("ds35.sports", 3.094, "US$ billion", "Sports segment operating income, fiscal 2026"),
    dis("ds35.capex", 8.698, "US$ billion", "investments in parks, resorts and other property, fiscal 2026 (the company's total)"),
    dis("ds35.tokyo", 1, "flag", "'The Company earns royalties on revenues generated by the Tokyo Disney Resort, which is owned and operated "
        "by Oriental Land Co., Ltd. (OLC), a third-party Japanese corporation'; Disney Cruise Line 'operates eight ships'"),

    # The Works
    wk("wk35.base", 0.75, "share of rooms", "demand at $180 in an average month, the Works' hotel", 0.6, 0.85),
    wk("wk35.elast", 1.5, "elasticity", "fall in rooms wanted for each per cent on the rate", 0.8, 2.5),
    wk("wk35.spread", 0.22, "log s.d.", "night-to-night scatter of demand within a month", 0.1, 0.35),
    wk("wk35.lift", 0.15, "share", "how much less demand an independent hotel has at the same rate", 0.05, 0.3),
    wk("wk35.ota", 0.25, "share", "rooms sold through online agents, branded hotel", 0.1, 0.4),
    wk("wk35.ota.ind", 0.50, "share", "rooms sold through online agents, independent hotel", 0.3, 0.7),
    wk("wk35.comm", 0.17, "share", "the online agents' commission", 0.12, 0.25),
    wk("wk35.direct", 0.03, "share", "the cost of a direct booking: cards and booking engine", 0.02, 0.05),
    wk("wk35.royalty", 0.055, "share of room revenue", "the brand's royalty (Marriott: typically 4-7%)", 0.04, 0.07),
    wk("wk35.prog", 0.045, "share of room revenue", "the brand's loyalty, reservation and marketing fees", 0.02, 0.06),
    wk("wk35.var", 35.0, "US$ a room sold", "housekeeping, laundry and supplies for each room sold", 25.0, 50.0),
    wk("wk35.fixed", 45.0, "US$ a room a night", "minimum staff, utilities, property tax, insurance and upkeep per room available", 30.0, 70.0),
    wk("wk35.invest", 180.0, "US$ thousand a room", "the owner's cost of the hotel per room", 120.0, 300.0),
    wk("wk35.debt", 0.6, "share", "share of the hotel's cost borrowed", 0.4, 0.7),
    wk("wk35.rate", 0.065, "a year", "interest on the debt", 0.05, 0.08),
    wk("wk35.shift", 4.0, "per unit", "share of agent bookings moved to direct per unit of members' discount", 2.0, 8.0),
)
