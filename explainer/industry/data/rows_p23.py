"""Register rows for Part 23, *Fashion and Luxury*.  Checked 2026-11-27.

Inditex's FY2025 results (to 31 January 2026) and interim 1H2026 results (to 31 July 2026); Hermès's full-year results releases
for 2023, 2024 and 2025; LVMH's 2025 results release; Kering's full-year results releases for 2023 and 2025; the Forms
10-K of NIKE (fiscal 2026, to 31 May 2026), TJX (fiscal 2026, to 31 January 2026), Tapestry (fiscal 2026, to 27 June
2026), Capri (fiscal 2026, to 28 March 2026), Lululemon (fiscal 2025, to 1 February 2026) and Levi Strauss (fiscal 2025,
to 30 November 2025).  Series are the Filing Room's SEC, FRED and UN Comtrade extracts.
"""

from explainer.industry.register import Row, add

C = "2026-11-27"
P = (23,)
SEC = "https://www.sec.gov/Archives/edgar/data/"
NKE = SEC + "320187/000032018726000088/nke-20260531.htm"
TJX = SEC + "109198/000010919826000008/tjx-20260131.htm"
TPR = SEC + "1116132/000111613226000018/tpr-20260627.htm"
CPRI = SEC + "1530721/000153072126000047/cpri-20260328.htm"
LULU = SEC + "1397187/000139718726000020/lulu-20260201.htm"
LEVI = SEC + "94845/000009484526000008/lvis-20251130.htm"
ITX25 = ("https://www.inditex.com/itxcomweb/api/media/1da2c9d1-dbca-49fb-9563-982a8a27fae6/INDITEXFullYear2025.pdf")
ITX26 = "https://www.inditex.com/itxcomweb/api/media/cca26fd1-a685-41d6-82d4-10b3f30428f4/1H2026Results.pdf"
RMS23 = ("https://assets-finance.hermes.com/s3fs-public/node/pdf_file/2024-02/1707422069/"
         "hermes_20240209_pr_2023fullyearresults_va.pdf")
RMS24 = ("https://assets-finance.hermes.com/s3fs-public/node/pdf_file/2025-02/1739475049/"
         "hermes_20250214_pr_2024fullyearresults_va.pdf")
RMS25 = "https://mfn.se/one/a/hermes/hermes-international-2025-full-year-results-a01f2a5e.iframe"
MC25 = ("https://www.lvmh.com/en/publications/"
        "solid-performance-in-a-disrupted-global-economic-and-geopolitical-environment")
KER23 = "https://www.kering.com/api/download-file/?path=Kering_Press_release_2023_Full_year_results_3388f09c4c.pdf"
KER25 = "https://www.kering.com/api/download-file/?path=Kering_2025_Results_Press_Release_bd7165a4ea.pdf"


def r(key, value, unit, definition, source, url, fact, kind="filing", note="", **kw):
    return Row(key, value, unit, definition, source, url, fact, C, kind, note=note, parts=P, **kw)


def itx(key, value, unit, definition, half=False):
    if half:
        return r(key, value, unit, definition, "Industria de Diseño Textil (Inditex), interim 1H2026 results",
                 ITX26, "1H2026 (1 February to 31 July 2026)")
    return r(key, value, unit, definition, "Industria de Diseño Textil (Inditex), FY2025 results", ITX25,
             "FY2025 (1 February 2025 to 31 January 2026)")


def nke(key, value, unit, definition):
    return r(key, value, unit, definition, "NIKE, Inc., Form 10-K for fiscal 2026", NKE, "FY2026 (to 2026-05-31)")


def tjx(key, value, unit, definition):
    return r(key, value, unit, definition, "The TJX Companies, Inc., Form 10-K for fiscal 2026", TJX,
             "FY2026 (to 2026-01-31)")


def tpr(key, value, unit, definition, fact="FY2026 (to 2026-06-27)"):
    return r(key, value, unit, definition, "Tapestry, Inc., Form 10-K for fiscal 2026", TPR, fact)


# Inditex's FY2025 quarters: net sales (EUR million) and gross margin (percent), Annex I of the FY2025 results
ITX_Q = {1: (8274, 60.6), 2: (10083, 56.4), 3: (9814, 62.2), 4: (11693, 54.8)}
# Inditex's net sales by concept, FY2025 (EUR million)
ITX_CONCEPT = {"zara": ("Zara (with Zara Home and Lefties)", 28051), "bershka": ("Bershka", 3286),
               "stradivarius": ("Stradivarius", 3002), "pullbear": ("Pull&Bear", 2546),
               "massimo": ("Massimo Dutti", 2019), "oysho": ("Oysho", 960)}
# Hermès revenue and recurring operating income (EUR million), each year's full-year results
RMS = {2022: (11602, 4697, RMS23), 2023: (13427, 5650, RMS24), 2024: (15170, 6150, RMS25), 2025: (16002, 6569, RMS25)}
# Gucci revenue and recurring operating income (EUR million), Kering's full-year results
GUCCI = {2022: (10487, 3732, KER23), 2023: (9873, 3264, KER23), 2024: (7650, 1605, KER25), 2025: (5992, 966, KER25)}
# LVMH 2025 revenue and profit from recurring operations by business group (EUR million)
MC = {"wines": ("Wines & Spirits", 5358, 1016), "fashion": ("Fashion & Leather Goods", 37770, 13209),
      "perfume": ("Perfumes & Cosmetics", 8174, 727), "watches": ("Watches & Jewelry", 10486, 1514),
      "retail": ("Selective Retailing", 18348, 1780)}
# NIKE's revenue by channel (US$ million): sales to wholesale customers and through NIKE Direct (NIKE Brand)
NKE_CH = {2024: (27758, 21519), 2025: (25883, 18783), 2026: (27453, 17720)}
# NIKE's gross margin (percent), fiscal 2024-2026
NKE_GM = {2024: 44.6, 2025: 42.7, 2026: 42.9}

add(
    itx("itx.sales", 39.864, "EUR billion", "net sales, FY2025 ('Sales were €39.9 billion')"),
    itx("itx.gm", 58.3, "percent", "gross margin, FY2025 ('The gross margin reached 58.3% (+42 bps)')"),
    itx("itx.ebit", 7.997, "EUR billion", "net operating profit (EBIT), FY2025 (EBIT margin 20.1%)"),
    itx("itx.ebit_margin", 20.1, "percent", "EBIT margin, FY2025"),
    itx("itx.net", 6.2, "EUR billion", "net income, FY2025 ('Net income increased 6.0% versus 2024 to €6.2 billion')"),
    itx("itx.stores", 5460, "stores", "stores at the end of FY2025 ('At the end of FY2025 Inditex operated 5,460 stores'), "
        "4,310 company-managed and 1,150 franchised"),
    itx("itx.markets", 214, "markets", "'Inditex operates in 214 markets. We enjoy a low market share in a sector which remains "
        "highly fragmented'"),
    itx("itx.inventory", 3.249, "EUR billion", "inventories at 31 January 2026 ('Inventory was 2% lower ... versus the same date "
        "in 2025')"),
    itx("itx.payables", 8.587, "EUR billion", "trade and other payables at 31 January 2026"),
    itx("itx.receivables", 1.166, "EUR billion", "trade and other receivables at 31 January 2026"),
    itx("itx.owc", -4.173, "EUR billion", "operating working capital at 31 January 2026 (inventories plus receivables less "
        "payables): negative"),
    itx("itx.cost", 16.641, "EUR billion", "cost of sales, FY2025 (sum of the four quarters in Annex I: 3,262 + 4,392 + 3,706 "
        "+ 5,281)"),
    itx("itx.proximity", 1, "flag", "'The business model we enjoy, characterised by flexibility, responsiveness and "
        "within-season proximity sourcing, permits us to react to fashion trends'"),
    itx("itx.space", 5, "percent", "'The growth of annual gross space in 2026 is expected to be around 5%'"),
    *[itx(f"itx.q{q}.sales", s, "EUR million", f"net sales, quarter {q} of FY2025 (Annex I)") for q, (s, g) in ITX_Q.items()],
    *[itx(f"itx.q{q}.gm", g, "percent", f"gross margin, quarter {q} of FY2025 (Annex I)") for q, (s, g) in ITX_Q.items()],
    *[itx(f"itx.concept.{k}", v, "EUR million", f"net sales of {name}, FY2025") for k, (name, v) in ITX_CONCEPT.items()],
    itx("itx.guide26", 0, "basis points", "'For 2026, Inditex expects a stable gross margin (+/-50 bps)', said with the FY2025 "
        "results and repeated with the 1H2026 results; the band is 50 basis points either side of FY2025's 58.3%"),
    itx("itx.spain", 15.9, "percent", "Spain's share of store and online sales, FY2025 (Europe excluding Spain 51.3%, Americas "
        "17.8%, Asia and rest of the world 15.0%)"),
    itx("itx.europe", 51.3, "percent", "Europe excluding Spain's share of store and online sales, FY2025"),
    itx("itx.formats", 8, "formats", "'our eight commercial formats' (Zara, Zara Home, Lefties, Pull&Bear, Massimo Dutti, Bershka, "
        "Stradivarius, Oysho)"),
    itx("itx.h1.cc", 9.2, "percent", "sales growth in constant currency, 1H2026 ('Sales in constant currency grew 9.2%')",
        half=True),
    itx("itx.h1.gm", 58.7, "percent", "gross margin, 1H2026 ('The gross margin reached 58.7% (+40 bps)')", half=True),
    itx("itx.h1.sales", 19.755, "EUR billion", "net sales, 1H2026 ('grew 7.6%, to reach €19.8 billion'; 9.2% in constant "
        "currency)", half=True),
    itx("itx.h1.sales_prev", 18.357, "EUR billion", "net sales, 1H2025 (the comparison column of the 1H2026 results)", half=True),
    itx("itx.h1.gm_prev", 58.3, "percent", "gross margin, 1H2025 (the comparison column of the 1H2026 results)", half=True),

    *[r(f"rms.rev.{y}", v, "EUR million", f"Hermès consolidated revenue, {y}", "Hermès International, full-year results release with "
        f"{y} figures", u, str(y)) for y, (v, o, u) in RMS.items()],
    *[r(f"rms.roi.{y}", o, "EUR million", f"Hermès recurring operating income, {y}",
        f"Hermès International, full-year results release with {y} figures", u, str(y)) for y, (v, o, u) in RMS.items()],
    r("rms.roi_margin", 41.0, "percent", "Hermès recurring operating income as a share of revenue, 2025 ('reached 41%, "
      "compared to 40.5% in 2024')", "Hermès International, 2025 full-year results", RMS25, "2025"),
    r("rms.gross", 11.379, "EUR billion", "Hermès gross margin (revenue less cost of sales of €4,623 million), 2025",
      "Hermès International, 2025 full-year results: consolidated statement of income", RMS25, "2025"),
    r("rms.net", 4.524, "EUR billion", "Hermès net profit, group share, 2025 (€4.86 billion adjusted for France's exceptional "
      "contribution on large companies' profits)", "Hermès International, 2025 full-year results", RMS25, "2025"),
    r("rms.leather", 7.070, "EUR billion", "Hermès Leather Goods and Saddlery revenue, 2025 (up 13.1% at constant exchange "
      "rates): bags, travel items, small leather goods, saddles and bridles", "Hermès International, 2025 full-year results",
      RMS25, "2025"),
    r("rms.leather.g", 13.1, "percent", "growth of Leather Goods and Saddlery at constant exchange rates, 2025, 'driven by the "
      "strong desirability of the collections and the increase in production capacities'",
      "Hermès International, 2025 full-year results", RMS25, "2025"),
    r("rms.workshops", 24, "workshops", "'The house's twenty-fourth leather goods workshop was inaugurated in September in "
      "L'Isle-d'Espagnac in Charente', with further openings planned in 2026, 2027 and 2028",
      "Hermès International, 2025 full-year results", RMS25, "2025"),
    r("rms.inhouse", 55, "percent", "share of objects 'manufactured in its in-house and exclusive workshops' (vertical "
      "integration)", "Hermès International, 2025 full-year results", RMS25, "2025"),
    r("rms.france", 75, "percent", "share of objects made in France", "Hermès International, 2025 full-year results", RMS25,
      "2025"),
    r("rms.staff", 26494, "employees", "Hermès workforce at the end of 2025", "Hermès International, 2025 full-year results",
      RMS25, "2025-12-31"),

    r("mc.rev", 80.807, "EUR billion", "LVMH revenue, 2025 (down 5% reported, 1% organic)", "LVMH, 2025 results (27 January "
      "2026)", MC25, "2025"),
    r("mc.pro", 17.755, "EUR billion", "LVMH profit from recurring operations, 2025 ('equating to an operating margin of 22%')",
      "LVMH, 2025 results (27 January 2026)", MC25, "2025"),
    r("mc.brands", 75, "brands", "'gathers more than 75 prestigious brands ... and a retail network of over 6,280 stores'",
      "LVMH, 2025 results (27 January 2026)", MC25, "2025"),
    *[r(f"mc.rev.{k}", v, "EUR million", f"LVMH revenue, {name}, 2025", "LVMH, 2025 results (27 January 2026)", MC25, "2025")
      for k, (name, v, p) in MC.items()],
    *[r(f"mc.pro.{k}", p, "EUR million", f"LVMH profit from recurring operations, {name}, 2025",
        "LVMH, 2025 results (27 January 2026)", MC25, "2025") for k, (name, v, p) in MC.items()],

    *[r(f"ker.gucci.{y}", v, "EUR million", f"Gucci revenue, {y}", "Kering, full-year results release with "
        f"{y} figures", u, str(y)) for y, (v, o, u) in GUCCI.items()],
    *[r(f"ker.gucci.roi.{y}", o, "EUR million", f"Gucci recurring operating income, {y}", "Kering, full-year results release "
        f"with {y} figures", u, str(y)) for y, (v, o, u) in GUCCI.items()],
    r("ker.rev", 14.675, "EUR billion", "Kering revenue, 2025 (down 13% reported and 10% on a comparable basis)",
      "Kering, 2025 full-year results (10 February 2026)", KER25, "2025"),
    r("ker.rev.2024", 16.874, "EUR billion", "Kering revenue, 2024 (the comparison column of the 2025 results)",
      "Kering, 2025 full-year results (10 February 2026)", KER25, "2024"),
    r("ker.net", 0.072, "EUR billion", "Kering net income attributable to the Group, 2025 (€1,133 million in 2024; net income "
      "from continuing operations attributable to the Group was a loss of €29 million)",
      "Kering, 2025 full-year results (10 February 2026)", KER25, "2025"),
    r("ker.roi", 1.631, "EUR billion", "Kering recurring operating income, 2025 (11.1% of revenue)",
      "Kering, 2025 full-year results (10 February 2026)", KER25, "2025"),
    r("mc.net", 10.878, "EUR billion", "LVMH net profit, Group share, 2025", "LVMH, 2025 results (27 January 2026)", MC25, "2025"),
    r("ker.gucci.retail", 92, "percent", "share of Gucci's 2025 revenue from its directly operated retail network (down 18% on a "
      "comparable basis; wholesale down 34%)", "Kering, 2025 full-year results (10 February 2026)", KER25, "2025"),
    r("ker.gucci.margin", 16.1, "percent", "Gucci recurring operating margin, 2025 ('down 4.9 points compared to 2024')",
      "Kering, 2025 full-year results (10 February 2026)", KER25, "2025"),

    nke("nke.rev", 46.398, "US$ billion", "total NIKE, Inc. revenues, fiscal 2026"),
    nke("nke.footwear", 29.525, "US$ billion", "NIKE Brand footwear revenues, fiscal 2026"),
    nke("nke.apparel", 13.449, "US$ billion", "NIKE Brand apparel revenues, fiscal 2026"),
    nke("nke.demand", 4.754, "US$ billion", "demand creation expense (brand and sports marketing: advertising, promotion, "
        "endorsement contracts), fiscal 2026"),
    nke("nke.inventory", 7.5, "US$ billion", "inventories at 31 May 2026 ('flat compared to the prior year')"),
    nke("nke.us", 44, "percent", "NIKE Brand and Converse sales in the United States as a share of total revenues, fiscal 2026"),
    *[nke(f"nke.wholesale.{y}", w, "US$ million", f"NIKE Brand sales to wholesale customers, fiscal {y}")
      for y, (w, d) in NKE_CH.items()],
    *[nke(f"nke.direct.{y}", d, "US$ million", f"NIKE Brand sales through NIKE Direct (its stores and digital), fiscal {y}")
      for y, (w, d) in NKE_CH.items()],
    *[nke(f"nke.gm.{y}", g, "percent", f"gross margin, fiscal {y}") for y, g in NKE_GM.items()],
    nke("nke.fw.factories", 95, "factories", "'contract manufacturers operated 95 finished goods footwear factories located in "
        "11 countries' (31 May 2026)"),
    nke("nke.fw.countries", 11, "countries", "countries with NIKE footwear factories (31 May 2026)"),
    nke("nke.fw.makers", 15, "contract manufacturers", "contract manufacturers of NIKE Brand footwear, fiscal 2026"),
    nke("nke.fw.top4", 60, "percent", "share of NIKE Brand footwear made by the four contract manufacturers that each made more "
        "than 10%, fiscal 2026"),
    nke("nke.fw.vn", 52, "percent", "share of NIKE Brand footwear made in Vietnam, fiscal 2026"),
    nke("nke.fw.id", 27, "percent", "share of NIKE Brand footwear made in Indonesia, fiscal 2026"),
    nke("nke.fw.cn", 16, "percent", "share of NIKE Brand footwear made in China, fiscal 2026"),
    nke("nke.ap.factories", 321, "factories", "'contract manufacturers operated 321 finished goods apparel factories located in "
        "34 countries' (31 May 2026)"),
    nke("nke.ap.countries", 34, "countries", "countries with NIKE apparel factories (31 May 2026)"),
    nke("nke.ap.makers", 64, "contract manufacturers", "contract manufacturers of NIKE Brand apparel, fiscal 2026"),
    nke("nke.ap.vn", 34, "percent", "share of NIKE Brand apparel made in Vietnam, fiscal 2026"),
    nke("nke.ap.kh", 15, "percent", "share of NIKE Brand apparel made in Cambodia, fiscal 2026"),
    nke("nke.ap.cn", 12, "percent", "share of NIKE Brand apparel made in China, fiscal 2026"),
    nke("nke.ap.top6", 54, "percent", "share of NIKE Brand apparel made by the top six contract manufacturers, fiscal 2026"),
    nke("nke.largest", 1, "flag", "'NIKE is the largest seller of athletic footwear and apparel in the world'; 'Nearly all of our "
        "products are manufactured by independent contractors'"),
    nke("nke.cos", 1, "flag", "cost of sales 'consists primarily of inventory costs, as well as warehousing costs (including the "
        "cost of warehouse labor), third-party royalties, certain foreign currency hedge gains and losses and product design "
        "costs'"),
    nke("nke.code", 1, "flag", "'We require the contractors that directly manufacture our products ... to comply with a code of "
        "conduct and other environmental, human rights, health and safety standards for the benefit of workers'; 'from time to "
        "time contractors may not comply with such standards or applicable local law'"),
    nke("nke.tier2", 205, "suppliers", "strategic Tier 2 (materials) suppliers, 31 May 2026"),
    nke("nke.ieepa", 986, "US$ million", "benefit recognized in cost of sales for the probable recovery of IEEPA tariffs paid, "
        "after the US Supreme Court ruled on 20 February 2026 that those tariffs were unauthorized"),
    nke("nke.markdown", 1, "flag", "'liquidating inventory through increased markdowns across NIKE Direct, and higher sales "
        "returns and discounts with our wholesale partners to reduce inventory and create capacity for new product'"),

    tjx("tjx.sales", 60.4, "US$ billion", "net sales, fiscal 2026 ('Net sales increased 7% to $60.4 billion')"),
    tjx("tjx.stores", 5214, "stores", "stores at the end of fiscal 2026 (TJ Maxx, Marshalls, HomeGoods, Homesense, Sierra, "
        "Winners, TK Maxx)"),
    tjx("tjx.potential", 7000, "stores", "estimated store growth potential in current markets"),
    tjx("tjx.vendors", 21000, "vendors", "'our expansive and changing universe of approximately 21,000 vendors across the globe, "
        "including thousands of new vendors in fiscal 2026'"),
    tjx("tjx.below.lo", 20, "percent", "prices 'generally 20% to 60% below full-price retailers' ... regular prices' (lower end)"),
    tjx("tjx.below.hi", 60, "percent", "upper end of the 20% to 60% range"),
    tjx("tjx.pretax", 12.1, "percent", "pre-tax profit margin, fiscal 2026"),
    tjx("tjx.cost", 69.0, "percent", "cost of sales, including buying and occupancy costs, as a share of net sales, fiscal 2026"),
    tjx("tjx.nopromo", 1, "flag", "'Our practice is to not engage in promotional pricing activity such as sales or coupons'"),

    tpr("tpr.coach", 6914.7, "US$ million", "Coach net sales, fiscal 2026"),
    tpr("tpr.coach.2025", 5598.5, "US$ million", "Coach net sales, fiscal 2025"),
    tpr("tpr.coach.2024", 5095.3, "US$ million", "Coach net sales, fiscal 2024"),
    tpr("tpr.coach.bags", 4016.3, "US$ million", "Coach handbag net sales, fiscal 2026 (58.1% of Coach's sales)"),
    tpr("tpr.kate", 1074.9, "US$ million", "Kate Spade net sales, fiscal 2026"),
    tpr("tpr.kate.2024", 1334.4, "US$ million", "Kate Spade net sales, fiscal 2024"),
    tpr("tpr.coach.gm", 78.8, "percent", "Coach gross margin excluding items affecting comparability, fiscal 2026"),
    tpr("tpr.kate.gm", 63.0, "percent", "Kate Spade gross margin excluding items affecting comparability, fiscal 2026"),
    tpr("tpr.capri", 1, "flag", "the merger agreement with Capri of 10 August 2023 was terminated on 13 November 2024",
        "2023-08-10 to 2024-11-13"),
    tpr("tpr.made", 1, "flag", "'During fiscal 2026, manufacturers of Coach products were primarily located in Vietnam, Cambodia, "
        "the Philippines and India'; Kate Spade's 'primarily in Vietnam, Cambodia, the Philippines and Bangladesh'; no vendor "
        "provided 10% or more of either brand's purchases"),
    tpr("tpr.audit", 1, "flag", "'Before directly partnering with a new manufacturing vendor for finished goods, the Company evaluates "
        "each facility by conducting a quality, business practice standards and social compliance review. We expect finished "
        "good manufacturers to undergo a social compliance audit before being approved as a Tapestry supplier.'"),
    tpr("tpr.pressure", 1, "flag", "risk factor: 'significant pricing pressure caused by many factors, including intense "
        "competition and a highly promotional environment, fragmentation in the retail industry, pressure from retailers to "
        "reduce the costs of products'"),
    tpr("tpr.genz", 1, "flag", "strategy: 'drive new customer acquisition, with a focus on Gen Z consumers entering the market'"),
    r("cpri.versace", 1.375, "US$ billion", "Capri agreed on 10 April 2025 to sell Versace to Prada 'for an aggregate purchase "
      "price of $1.375 billion in cash'; the sale was completed on 2 December 2025", "Capri Holdings Limited, Form 10-K for "
      "fiscal 2026", CPRI, "2025-04-10 to 2025-12-02"),
    r("cpri.mk", 2874, "US$ million", "Michael Kors revenue, fiscal 2026 (83% of Capri's revenue)",
      "Capri Holdings Limited, Form 10-K for fiscal 2026", CPRI, "FY2026 (to 2026-03-28)"),
    r("cpri.mk.2024", 3522, "US$ million", "Michael Kors revenue, fiscal 2024", "Capri Holdings Limited, Form 10-K for fiscal "
      "2026", CPRI, "FY2024 (to 2024-03-30)"),
    r("lulu.gm", 56.6, "percent", "gross margin, fiscal 2025 ('decreased 260 basis points to 56.6%'), 240 basis points of it "
      "'primarily from higher tariffs, as well as increased markdowns'", "lululemon athletica inc., Form 10-K for fiscal "
      "2025", LULU, "FY2025 (to 2026-02-01)"),
    r("lulu.gm.prev", 59.2, "percent", "gross margin, fiscal 2024", "lululemon athletica inc., Form 10-K for fiscal 2025", LULU,
      "FY2024"),
    r("lulu.taiwan", 34, "percent", "share of its fabric that originated in Taiwan, 2025 (29% China, 10% South Korea, 10% "
      "Vietnam)", "lululemon athletica inc., Form 10-K for fiscal 2025", LULU, "FY2025"),
    *[r(f"lulu.fabric.{k}", v, "percent", f"share of its fabric that originated in {name}, 2025",
        "lululemon athletica inc., Form 10-K for fiscal 2025", LULU, "FY2025")
      for k, name, v in (("cn", "China Mainland", 29), ("kr", "South Korea", 10), ("vn", "Vietnam", 10))],
    r("lulu.fabric.suppliers", 65, "suppliers", "'We work with a group of approximately 65 fabric suppliers'; the top five made "
      "48% of its fabric and the largest 20%", "lululemon athletica inc., Form 10-K for fiscal 2025", LULU, "FY2025"),
    r("lulu.tariff", 380, "basis points", "operating margin fell 380 basis points in 2025, 'mainly due to the impact from increased "
      "tariff rates in the United States, and the removal of the de minimis provision'", "lululemon athletica inc., Form "
      "10-K for fiscal 2025", LULU, "FY2025"),
    r("lulu.noown", 1, "flag", "'We obtain our fabrics and produce our products through a limited number of suppliers. We do not "
      "own or operate any manufacturing facilities.'", "lululemon athletica inc., Form 10-K for fiscal 2025", LULU, "FY2025"),
    r("lulu.china", 29, "percent", "net revenue growth in China Mainland, 2025 (Americas down 1%)",
      "lululemon athletica inc., Form 10-K for fiscal 2025", LULU, "FY2025"),
    r("levi.dtc", 49, "percent", "share of net revenues from Levi's own stores and e-commerce (direct to consumer), fiscal 2025 "
      "(47% in fiscal 2024; wholesale 51%)", "Levi Strauss & Co., Form 10-K for fiscal 2025", LEVI, "FY2025 (to 2025-11-30)"),
    r("levi.top10", 24, "percent", "share of net revenues from its top ten wholesale customers, fiscal 2025 (27% in 2023)",
      "Levi Strauss & Co., Form 10-K for fiscal 2025", LEVI, "FY2025"),
    r("wto.quota", 2005, "year", "Under the WTO's Agreement on Textiles and Clothing (in force from 1 January 1995), 'WTO Members "
      "have committed themselves to remove the quotas by 1 January 2005 by integrating the sector fully into GATT rules'; "
      "before it, quotas were negotiated bilaterally under the Multifibre Arrangement", "World Trade Organization, "
      "Textiles: the Agreement on Textiles and Clothing", "https://www.wto.org/english/tratop_e/texti_e/texintro_e.htm",
      "1995-01-01 to 2005-01-01", kind="official"),
    r("ilo.rana", 1132, "people", "'On 24 April 2013, the collapse of the Rana Plaza building in Dhaka, Bangladesh, which housed "
      "five garment factories, killed at least 1,132 people and injured more than 2,500'", "International Labour "
      "Organization, Employment injury insurance in Bangladesh: bridging social security in cases of tragedy",
      "https://www.ilo.org/resource/statement/employment-injury-insurance-bangladesh-bridging-social-security-cases",
      "2013-04-24", kind="official"),
    r("ilo.rana.injured", 2500, "people", "injured in the Rana Plaza collapse ('more than 2,500')", "International Labour "
      "Organization, Employment injury insurance in Bangladesh: bridging social security in cases of tragedy",
      "https://www.ilo.org/resource/statement/employment-injury-insurance-bangladesh-bridging-social-security-cases",
      "2013-04-24", kind="official"),
)
