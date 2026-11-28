"""Register rows for Part 34, *Restaurants and Franchising*.  Checked 2026-11-28.

The Forms 10-K for 2025 of McDonald's, Chipotle, Wingstop, Domino's, Yum! Brands and DoorDash and Darden's for fiscal 2026;
McDonald's 10-Q for the third quarter of 2026; Arcos Dorados's Form 20-F for 2025; DoorDash's prospectus of December 2020.
Series are the Filing Room's SEC and FRED extracts.
"""

from explainer.industry.register import Row, add

C = "2026-11-28"
P = (34,)
SEC = "https://www.sec.gov/Archives/edgar/data/"
MCD = SEC + "63908/000006390826000035/mcd-20251231.htm"
MCDQ = SEC + "63908/000006390826000083/mcd-20260930.htm"
CMG = SEC + "1058090/000105809026000009/cmg-20251231.htm"
WING = SEC + "1636222/000163622226000008/wing-20251227.htm"
DPZ = SEC + "1286681/000119312526062321/dpz-20251228.htm"
YUM = SEC + "1041061/000104106126000084/yum-20251231.htm"
DRI = SEC + "940944/000094094426000025/dri-20260531.htm"
ARCO = SEC + "1508478/000162828026028950/arco-20251231.htm"
DASH = SEC + "1792789/000179278926000013/dash-20251231.htm"
DASH_IPO = SEC + "1792789/000119312520313884/d752207d424b4.htm"


def r(key, value, unit, definition, source, url, fact, kind="filing", note="", **kw):
    return Row(key, value, unit, definition, source, url, fact, C, kind, note=note, parts=P, **kw)


def mcd(key, value, unit, definition, fact="2025"):
    return r(key, value, unit, definition, "McDonald's, Form 10-K for 2025", MCD, fact)


def cmg(key, value, unit, definition, fact="2025"):
    return r(key, value, unit, definition, "Chipotle Mexican Grill, Form 10-K for 2025", CMG, fact)


def wk(key, value, unit, definition, lo, hi):
    return r(key, value, unit, definition, "this series' assumption", "", "", kind="assumption", lo=lo, hi=hi)


add(
    # McDonald's
    mcd("md34.rest", 45356, "restaurants", "restaurants at 31 December 2025 (43,477 a year before, 41,822 at the end of 2023)", "2025-12-31"),
    mcd("md34.rest24", 43477, "restaurants", "restaurants at 31 December 2024", "2024-12-31"),
    mcd("md34.rest23", 41822, "restaurants", "restaurants at 31 December 2023", "2023-12-31"),
    r("md34.co13", 6738, "restaurants", "'Of the 35,429 restaurants in 119 countries at year-end 2013, 28,691 were franchised ... and 6,738 were "
      "operated by the Company'", "McDonald's, Form 10-K for 2013", SEC + "63908/000006390814000019/mcd-12312013x10k.htm", "2013-12-31"),
    r("md34.rest13", 35429, "restaurants", "restaurants at year-end 2013", "McDonald's, Form 10-K for 2013",
      SEC + "63908/000006390814000019/mcd-12312013x10k.htm", "2013-12-31"),
    mcd("md34.us", 13706, "restaurants", "restaurants in the U.S. at 31 December 2025", "2025-12-31"),
    mcd("md34.fr", 95, "percent", "'Franchised restaurants represented approximately 95% of McDonald's restaurants worldwide at December 31, 2025', "
        "including 95% in the U.S.; 'Franchised margins represented approximately 90% of restaurant margin dollars'", "2025-12-31"),
    mcd("md34.target", 50000, "restaurants", "'progressing toward the targeted expansion to 50,000 restaurants by the end of 2027, which would "
        "make it the fastest period of restaurant unit growth in Company history'"),
    mcd("md34.rents", 10.442, "US$ billion", "rents from franchised restaurants, 2025"),
    mcd("md34.royal", 6.018, "US$ billion", "royalties from franchised restaurants, 2025"),
    mcd("md34.frrev", 16.548, "US$ billion", "revenues from franchised restaurants (rents, royalties and $88m of initial fees), 2025"),
    mcd("md34.frmargin", 13.930, "US$ billion", "franchised restaurant margins, 2025 (franchised revenues less occupancy costs of $2,618m)"),
    mcd("md34.cosales", 9.690, "US$ billion", "sales by Company-owned and operated restaurants, 2025"),
    mcd("md34.food", 3.006, "US$ billion", "Company-operated food & paper, 2025"),
    mcd("md34.payroll", 2.905, "US$ billion", "Company-operated payroll & employee benefits, 2025"),
    mcd("md34.occ", 2.358, "US$ billion", "Company-operated occupancy & other operating expenses, 2025"),
    mcd("md34.comargin", 1.422, "US$ billion", "Company-owned and operated margins, 2025"),
    mcd("md34.frsales", 129.675, "US$ billion", "franchised sales, 2025 ($93,761m conventional franchised, $22,451m developmental licensed, $13,463m "
        "foreign affiliated); 'not recorded as revenues'"),
    mcd("md34.frsales.us", 51.946, "US$ billion", "franchised sales in the U.S., 2025"),
    mcd("md34.conv", 93.761, "US$ billion", "conventional franchised sales, 2025"),
    mcd("md34.land", 56, "percent", "'the Company owned approximately 56% of the land and approximately 80% of the buildings for restaurants in "
        "its consolidated markets'", "2025-12-31"),
    mcd("md34.bldg", 80, "percent", "share of buildings owned for restaurants in its consolidated markets", "2025-12-31"),
    mcd("md34.term", 20, "years", "franchise agreements 'generally have 20-year terms'; 'At the end of the 20-year franchise arrangement, the "
        "Company maintains control of the underlying real estate and building'"),
    mcd("md34.loyalty", 45.0, "US$ billion", "'the Company plans to grow its annual Systemwide sales to loyalty members to $45.0 billion by the end of "
        "2027' and 'to increase its 90-day active users to 250 million'; loyalty programs in 70 markets"),
    mcd("md34.initial", 0.088, "US$ billion", "initial fees from franchisees, 2025 ($92m in 2024)"),
    mcd("md34.delivery", 41000, "restaurants", "'The Company offers delivery from nearly 41,000 restaurants across approximately 100 markets, "
        "representing approximately 90% of McDonald's restaurants'"),
    r("md34.net26", 2100, "restaurants", "'The Company expects approximately 2,100 net restaurant additions in 2026'; 'Globally, the Company "
      "expects to open about 2,500 restaurants in 2026'", "McDonald's, Form 10-Q for the third quarter of 2026", MCDQ, "2026"),

    # Chipotle
    cmg("cm34.rev", 11.9256, "US$ billion", "total revenue, 2025 (food and beverage revenue $11,866.1m)"),
    cmg("cm34.ars", 3.104, "US$ million", "average restaurant sales, trailing twelve months, 2025 ($3.213m in 2024); comparable sales -1.7%"),
    cmg("cm34.units", 4042, "restaurants", "restaurants owned and operated at 31 December 2025; 334 opened in 2025, 257 with a Chipotlane"),
    cmg("cm34.food", 3.527, "US$ billion", "food, beverage and packaging costs, 2025"),
    cmg("cm34.labor", 2.9917, "US$ billion", "labor costs, 2025"),
    cmg("cm34.occ", 0.6249, "US$ billion", "occupancy costs, 2025"),
    cmg("cm34.other", 1.7558, "US$ billion", "other operating costs, 2025"),
    cmg("cm34.goal", 7000, "restaurants", "'working towards our long-term goal of 7,000 restaurants in the U.S. and Canada'"),

    # Wingstop, Domino's, Yum, Darden, Arcos Dorados
    r("wg34.auv", 2.0, "US$ million", "'Our domestic average unit volume (AUV) was approximately $2.0 million during fiscal year 2025'",
      "Wingstop, Form 10-K for 2025", WING, "2025"),
    r("wg34.royalty", 6.0, "percent", "'each franchisee is required to pay us a royalty of 6.0% of their gross sales net of discounts'; the national "
      "advertising fund contribution rate is 5.5%", "Wingstop, Form 10-K for 2025", WING, "2025"),
    r("wg34.ad", 5.5, "percent", "national advertising fund contribution rate", "Wingstop, Form 10-K for 2025", WING, "2025"),
    r("wg34.units", 3056, "restaurants", "restaurants at 27 December 2025, 2,999 of them run by franchisees", "Wingstop, Form 10-K for 2025",
      WING, "2025-12-27"),
    r("wg34.coc", 70, "percent", "'In year two of operation of a new restaurant, we target a franchisee unlevered cash-on-cash return of "
      "approximately 70%+'", "Wingstop, Form 10-K for 2025", WING, "2025"),
    r("wg34.digital", 73.2, "percent", "digital sales as a share of system-wide sales, fourth quarter of 2025", "Wingstop, Form 10-K for 2025",
      WING, "2025-Q4"),
    r("dp34.supply", 2.9895, "US$ billion", "supply chain revenues, 2025 (60.5% of revenues; segment income $320.1m); U.S. franchise royalties "
      "and fees $677.1m", "Domino's Pizza, Form 10-K for 2025", DPZ, "2025"),
    r("dp34.royal", 0.6771, "US$ billion", "U.S. franchise royalties and fees, 2025", "Domino's Pizza, Form 10-K for 2025", DPZ, "2025"),
    r("dp34.scinc", 0.3201, "US$ billion", "supply chain segment income, 2025", "Domino's Pizza, Form 10-K for 2025", DPZ, "2025"),
    r("dp34.units", 22100, "stores", "'more than 22,100 locations in over 90 markets'; 22 regional dough manufacturing and supply chain centers "
      "in the U.S.", "Domino's Pizza, Form 10-K for 2025", DPZ, "2025-12-28"),
    r("ym34.units", 63000, "restaurants", "'over 63,000 restaurants in 155 countries and territories'; 'Of the over 63,000 restaurants, 97% are "
      "operated by franchisees'", "Yum! Brands, Form 10-K for 2025", YUM, "2025-12-31"),
    r("ym34.china", 3, "percent", "'We are contractually entitled to receive a 3% sales-based license fee on all Yum China system sales related to "
      "our KFC, Taco Bell and Pizza Hut Concepts'", "Yum! Brands, Form 10-K for 2025", YUM, "2025"),
    r("ym34.fr", 97, "percent", "share of Yum's restaurants operated by franchisees", "Yum! Brands, Form 10-K for 2025", YUM, "2025-12-31"),
    r("dr34.sales", 13.2109, "US$ billion", "sales, fiscal 2026 (to 31 May 2026): food and beverage $4,038.8m, restaurant labor $4,182.4m, "
      "restaurant expenses $2,127.2m; 2,202 restaurants, all owned and operated", "Darden Restaurants, Form 10-K for fiscal 2026", DRI, "FY2026"),
    r("dr34.food", 4.0388, "US$ billion", "food and beverage costs, fiscal 2026", "Darden Restaurants, Form 10-K for fiscal 2026", DRI, "FY2026"),
    r("dr34.labor", 4.1824, "US$ billion", "restaurant labor, fiscal 2026", "Darden Restaurants, Form 10-K for fiscal 2026", DRI, "FY2026"),
    r("dr34.rexp", 2.1272, "US$ billion", "restaurant expenses, fiscal 2026", "Darden Restaurants, Form 10-K for fiscal 2026", DRI, "FY2026"),
    r("dr34.units", 2202, "restaurants", "restaurants owned and operated at 31 May 2026", "Darden Restaurants, Form 10-K for fiscal 2026", DRI,
      "2026-05-31"),
    r("ar34.units", 2520, "restaurants", "restaurants at 31 December 2025 in 21 countries and territories in Latin America and the Caribbean; 'the world's "
      "largest independent McDonald's franchisee'; it owned the land for 474 of them", "Arcos Dorados, Form 20-F for 2025", ARCO, "2025-12-31"),
    r("ar34.royalty", 6.0, "percent", "the master franchise agreements require it 'to pay monthly royalties commencing at a rate of 6.0% of gross "
      "sales of the restaurants during the first 10 years', rising to 6.25% and 6.5%, and to spend 'at least 5% of the Company's gross sales "
      "on advertising and promotion'", "Arcos Dorados, Form 20-F for 2025", ARCO, "2025"),

    # DoorDash
    r("da34.gov", 102.018, "US$ billion", "Marketplace GOV, 2025 ($80.2bn in 2024); 3,172 million total orders; revenue $13,717m; net revenue "
      "margin 13.4%; net income attributable to common stockholders $935m ($123m in 2024, -$558m in 2023)", "DoorDash, Form 10-K for 2025",
      DASH, "2025"),
    r("da34.orders", 3172, "million", "total orders, 2025", "DoorDash, Form 10-K for 2025", DASH, "2025"),
    r("da34.nrm", 13.4, "percent", "net revenue margin (revenue over Marketplace GOV), 2025", "DoorDash, Form 10-K for 2025", DASH, "2025"),
    r("da34.ipo", 1, "flag", "'We have a history of net losses, we anticipate increasing expenses in the future, and we may not be able to "
      "maintain or increase profitability in the future'; 'We incurred a net loss of $667 million ... in the year ended December 31, 2019'",
      "DoorDash, prospectus (Form 424B4), December 2020", DASH_IPO, "2020-12"),
    r("da34.loss19", 667, "US$ million", "net loss, 2019 (revenue $885m)", "DoorDash, prospectus (Form 424B4), December 2020", DASH_IPO, "2019"),

    # The Works
    wk("wk34.ad", 0.04, "share of sales", "a franchisee's advertising fund contribution", 0.03, 0.06),
    wk("wk34.other", 0.10, "share of sales", "utilities, repairs, insurance, card fees and other store costs", 0.07, 0.13),
    wk("wk34.delivery", 0.15, "share of sales", "sales through delivery apps", 0.05, 0.30),
    wk("wk34.commission", 0.20, "share", "the delivery apps' commission on those sales", 0.15, 0.30),
    wk("wk34.invest", 1.5, "US$ million", "a franchisee's own investment in equipment, seating, signs and decor", 1.0, 2.5),
    wk("wk34.fixed", 0.6, "share", "the part of a store's labour that does not move with sales", 0.4, 0.8),
    wk("wk34.patience", 5.0, "years", "the median would-be franchisee's longest acceptable payback", 3.0, 8.0),
    wk("wk34.pool", 400.0, "a year", "would-be franchisees who consider opening a store each year", 200.0, 800.0),
)
