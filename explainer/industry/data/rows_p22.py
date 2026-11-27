"""Register rows for Part 22, *Consumer Goods*.  Checked 2026-11-27.

Procter & Gamble's Forms 10-K for fiscal 2020 to 2026 and its results releases (Forms 8-K, Exhibit 99.1) of July 2025,
July 2026 and October 2026; the Forms 10-K 2025 of Coca-Cola, Altria, Colgate-Palmolive, Church & Dwight, Kimberly-Clark
and Hershey; Clorox's for fiscal 2026, General Mills' for fiscal 2026 and Costco's for fiscal 2026.  Series are the Filing
Room's SEC and FRED extracts.
"""

from explainer.industry.register import Row, add

C = "2026-11-27"
P = (22,)
SEC = "https://www.sec.gov/Archives/edgar/data/"
PG = {2020: SEC + "80424/000008042420000053/pg-20200630.htm", 2021: SEC + "80424/000008042421000100/pg-20210630.htm",
      2022: SEC + "80424/000008042422000064/pg-20220630.htm", 2023: SEC + "80424/000008042423000073/pg-20230630.htm",
      2024: SEC + "80424/000008042424000083/pg-20240630.htm", 2025: SEC + "80424/000008042425000076/pg-20250630.htm",
      2026: SEC + "80424/000008042426000103/pg-20260630.htm"}
PG_R24 = SEC + "80424/000008042424000071/fy2324q4amj8-kexhibit991.htm"
PG_R25 = SEC + "80424/000008042425000067/fy2425q4amj8-kexhibit991.htm"
PG_R26 = SEC + "80424/000008042426000093/fy2526q4amj8-kexhibit991.htm"
PG_RQ1 = SEC + "80424/000008042426000250/fy2627q1jas8-kexhibit991.htm"
KO25 = SEC + "21344/000162828026010047/ko-20251231.htm"
MO25 = SEC + "764180/000076418026000017/mo-20251231.htm"
CL25 = SEC + "21665/000002166526000006/cl-20251231.htm"
CHD25 = SEC + "313927/000119312526048139/chd-20251231.htm"
KMB25 = SEC + "55785/000162828026007567/kmb-20251231.htm"
HSY25 = SEC + "47111/000162828026008586/hsy-20251231.htm"
CLX26 = SEC + "21076/000002107626000034/clx-20260630.htm"
GIS26 = SEC + "40704/000162828026046466/gis-20260531.htm"
COST26 = SEC + "909832/000090983226000093/cost-20260830.htm"
PM25 = SEC + "1413329/000162828026005939/pm-20251231.htm"


def r(key, value, unit, definition, source, url, fact, kind="filing", note="", **kw):
    return Row(key, value, unit, definition, source, url, fact, C, kind, note=note, parts=P, **kw)


def pg(key, value, unit, definition, fy=2026):
    return r(key, value, unit, definition, f"The Procter & Gamble Company, Form 10-K for fiscal {fy}", PG[fy], f"FY{fy}")


# P&G's net sales change drivers, total company (volume with acquisitions and divestitures, foreign exchange, price,
# mix, other, net sales growth), from each year's Form 10-K
DRIVERS = {2020: (4, -2, 1, 1, 1, 5), 2021: (3, 1, 1, 2, 0, 7), 2022: (2, -2, 4, 1, 0, 5), 2023: (-3, -5, 9, 1, 0, 2),
           2024: (0, -2, 4, 0, 0, 2), 2025: (0, -1, 1, 0, 0, 0), 2026: (0, 2, 1, 0, 0, 3)}
ADS = {2018: (7.1, 2020), 2019: (6.8, 2020), 2020: (7.3, 2022), 2021: (8.2, 2022), 2022: (7.9, 2024), 2023: (8.0, 2025),
       2024: (9.6, 2026), 2025: (9.2, 2026), 2026: (10.2, 2026)}
SALES = {2020: 70950, 2021: 76118, 2022: 80187, 2023: 82006, 2024: 84039}

add(
    pg("pg.sales", 87.0, "US$ billion", "'Net sales increased 3% to $87.0 billion' in fiscal 2026 (organic sales up 1%)"),
    pg("pg.organic", 1, "percent", "organic sales growth, fiscal 2026 ('Organic sales ... increased 1%')"),
    pg("pg.gm", 50.2, "percent", "'Gross margin decreased 100 basis points to 50.2% of net sales' in fiscal 2026"),
    pg("pg.opm", 22.7, "percent", "operating margin, fiscal 2026 ('operating margin decreased 160 basis points to 22.7%')"),
    pg("pg.walmart", 16, "percent", "'Sales to Walmart Inc. and its affiliates represent approximately 16% of our total sales in "
       "2026, 2025 and 2024'"),
    pg("pg.top10", 43, "percent", "'Our top ten customers accounted for approximately 43% of our total net sales in 2026'"),
    pg("pg.rnd", 2.1, "US$ billion", "research and development costs, fiscal 2026"),
    *[pg(f"pg.ads.{y}", v, "US$ billion", f"advertising costs (television, print, radio, digital and in-store), fiscal {y}", fy)
      for y, (v, fy) in ADS.items()],
    *[pg(f"pg.sales.{y}", v, "US$ million", f"net sales, fiscal {y} (segment table, total company)", y)
      for y, v in SALES.items()],
    *[pg(f"pg.drv.{y}.{k}", v, "percent", f"net sales change driver, total company, fiscal {y}: {name}", y)
      for y, vals in DRIVERS.items()
      for k, name, v in zip(("vol", "fx", "price", "mix", "other", "net"),
                            ("volume with acquisitions and divestitures", "foreign exchange", "price", "mix", "other",
                             "net sales growth"), vals)],
    *[pg(f"pg.seg.{k}", v, "US$ billion", f"{name} net sales, fiscal 2026 (growth {g}%: {why})")
      for k, name, v, g, why in (("beauty", "Beauty", 16.0, 7, "volume +4%, foreign exchange +2%, price +1%"),
                                 ("grooming", "Grooming", 6.9, 4, "foreign exchange +3%, price +2%, volume -1%"),
                                 ("health", "Health Care", 12.5, 4, "foreign exchange +3%, price +2%, mix +1%, volume -2%"),
                                 ("fabric", "Fabric & Home Care", 30.3, 2, "foreign exchange +1%, price +1%, volume flat"),
                                 ("baby", "Baby, Feminine & Family Care", 20.4, 1, "foreign exchange +2%, volume -1%"))],
    *[pg(f"pg.seg.{k}.g", g, "percent", f"{name} net sales growth, fiscal 2026")
      for k, name, g in (("beauty", "Beauty", 7), ("grooming", "Grooming", 4), ("health", "Health Care", 4),
                         ("fabric", "Fabric & Home Care", 2), ("baby", "Baby, Feminine & Family Care", 1))],
    r("cl.abroad", 45, "percent", "Colgate-Palmolive: 'Approximately two-thirds of the Company's Net sales are generated from "
      "markets outside the United States, with approximately 45% of the Company's Net sales coming from emerging markets'",
      "Colgate-Palmolive Company, Form 10-K 2025", CL25, "2025"),
    pg("pg.beauty.price", 1, "percent", "Beauty: 'a unit volume increase of 4%, favorable foreign exchange of 2% and positive impact "
       "of higher pricing of 1%', fiscal 2026"),
    r("pg.guide25.lo", 3, "percent", "30 July 2024: 'The Company expects organic sales growth in the range of three to five "
      "percent' for fiscal 2025", "The Procter & Gamble Company, Form 8-K of 30 July 2024 (Exhibit 99.1)", PG_R24,
      "FY2025 (forecast)"),
    r("pg.guide25.hi", 5, "percent", "upper end of the fiscal 2025 organic sales growth guidance",
      "The Procter & Gamble Company, Form 8-K of 30 July 2024 (Exhibit 99.1)", PG_R24, "FY2025 (forecast)"),
    pg("pg.organic.2025", 2, "percent", "fiscal 2025: 'Organic sales, which exclude the impact of acquisitions and divestitures "
       "and foreign exchange, increased 2%'", 2025),
    r("pg.guide26.lo", 0, "percent", "29 July 2025: 'The Company expects organic sales growth in the range of flat to up four "
      "percent' for fiscal 2026", "The Procter & Gamble Company, Form 8-K of 29 July 2025 (Exhibit 99.1)", PG_R25,
      "FY2026 (forecast)"),
    r("pg.guide26.hi", 4, "percent", "upper end of the fiscal 2026 organic sales growth guidance",
      "The Procter & Gamble Company, Form 8-K of 29 July 2025 (Exhibit 99.1)", PG_R25, "FY2026 (forecast)"),
    r("pg.guide27.lo", 1, "percent", "29 July 2026: 'The Company also expects organic sales growth in the range of one to three "
      "percent' for fiscal 2027", "The Procter & Gamble Company, Form 8-K of 29 July 2026 (Exhibit 99.1)", PG_R26,
      "FY2027 (forecast)"),
    r("pg.guide27.hi", 3, "percent", "upper end of the fiscal 2027 organic sales growth guidance; it includes 'a headwind of 30 to "
      "50 basis points from brand, product form and go-to-market discontinuations' and about $1 billion after tax of higher "
      "raw material, energy and transport costs", "The Procter & Gamble Company, Form 8-K of 29 July 2026 (Exhibit 99.1)",
      PG_R26, "FY2027 (forecast)"),
    r("pg.q1fy27", 4, "percent", "22 October 2026: first-quarter fiscal 2027 organic sales 'increased four percent ... driven by a "
      "two percent increase from volume and a one percent increase from favorable mix'; it 'Maintains fiscal year organic "
      "sales ... guidance'", "The Procter & Gamble Company, Form 8-K of 22 October 2026 (Exhibit 99.1)", PG_RQ1,
      "FY2027 Q1"),

    pg("pg.brands", 1, "flag", "major brands by segment: Head & Shoulders, Pantene, Old Spice, Olay, SK-II (Beauty); Gillette, "
       "Braun, Venus (Grooming); Crest, Oral-B, Vicks (Health Care); Tide, Ariel, Downy, Gain, Dawn, Febreze, Mr. Clean "
       "(Fabric & Home Care); Pampers, Always, Bounty, Charmin (Baby, Feminine & Family Care)",
       ),
    *[pg(f"pg.segshare.{k}", v, "percent", f"{name}: share of net sales, fiscal 2026 (segment table, excluding Corporate)")
      for k, name, v in (("fabric", "Fabric & Home Care", 35), ("baby", "Baby, Feminine & Family Care", 24),
                         ("beauty", "Beauty", 19), ("health", "Health Care", 14), ("grooming", "Grooming", 8))],
    # Hershey: a brand meets cocoa
    r("hsy.gm.2024", 47.3, "percent", "'Gross margin was 33.5% in 2025 compared with 47.3% in 2024'", "The Hershey Company, Form "
      "10-K 2025", HSY25, "2024"),
    r("hsy.gm.2025", 33.5, "percent", "gross margin 2025, 'driven by higher commodity and tariff costs, unfavorable mark-to-market "
      "activity on our commodity derivative instruments and lower volume'", "The Hershey Company, Form 10-K 2025", HSY25, "2025"),
    r("hsy.price", 6, "percent", "2025 net sales 'reflects a favorable price realization of approximately 6% primarily due to "
      "higher list prices'", "The Hershey Company, Form 10-K 2025", HSY25, "2025"),
    r("hsy.size", 1, "flag", "'We may be able to pass some or all raw material, energy, and other input cost increases to "
      "customers by increasing the selling prices of our products or decreasing the size of our products; however, higher "
      "product prices or decreased product sizes have in the past and may in the future result in a reduction in sales volume'",
      "The Hershey Company, Form 10-K 2025", HSY25, "2025", note="a quotation, carried as a flag"),
    r("gis.trade", 493, "US$ million", "General Mills: revenues are 'reported net of ... trade promotion, consumer coupon "
      "redemption'; 'accrued trade and coupon promotion liabilities were $493 million as of May 31, 2026'", "General Mills, Inc., "
      "Form 10-K for fiscal 2026", GIS26, "FY2026"),
    r("gis.vol", -1, "percent", "'Organic pound volume in North America Retail declined 1 percent for the year'; 'On our priority "
      "of returning North America Retail to volume growth, we did not achieve our objective'", "General Mills, Inc., Form 10-K "
      "for fiscal 2026", GIS26, "FY2026"),
    r("chd.top4", 44, "percent", "Church & Dwight: 'A group of four customers accounted for approximately 44%' of net sales in "
      "2025", "Church & Dwight Co., Inc., Form 10-K 2025", CHD25, "2025"),
    # Philip Morris International: the smoke-free turn
    *[r(f"pm.sf.{y}", v, "US$ million", f"PMI smoke-free net revenues, {y} (total net revenues {tot:,})", "Philip Morris "
        "International Inc., Form 10-K 2025", PM25, str(y)) for y, v, tot in ((2023, 12840, 35174), (2024, 14660, 37878),
                                                                             (2025, 16854, 40648))],
    r("pm.markets", 106, "markets", "'As of December 31, 2025, our smoke-free products were available for sale in 106 markets'; "
      "IQOS, ZYN and VEEV the leading brands", "Philip Morris International Inc., Form 10-K 2025", PM25, "2025"),

    # Coca-Cola: concentrate and bottlers
    r("ko.cases", 33.8, "billion unit cases", "'The Coca-Cola system sold 33.8 billion and 33.7 billion unit cases of our products "
      "in 2025 and 2024'; a unit case is 192 US fluid ounces", "The Coca-Cola Company, Form 10-K 2025", KO25, "2025"),
    r("ko.conc.rev", 59, "percent", "concentrate operations' share of net operating revenues, 2025 (finished product operations "
      "41%)", "The Coca-Cola Company, Form 10-K 2025", KO25, "2025"),
    r("ko.conc.vol", 85, "percent", "concentrate operations' share of worldwide unit case volume, 2025 (finished product "
      "operations 15%)", "The Coca-Cola Company, Form 10-K 2025", KO25, "2025"),
    r("ko.coke.share", 47, "percent", "'Trademark Coca-Cola accounted for 47% of our worldwide unit case volume' in 2025; "
      "sparkling soft drinks 69%", "The Coca-Cola Company, Form 10-K 2025", KO25, "2025"),

    # Altria: the most profitable legal product
    r("mo.vol", 61.8, "billion cigarettes", "'Total smokeable products segment's cigarettes shipment volume in the United States "
      "was 61.8 billion units in 2025, a decrease of 10.0% from 2024'", "Altria Group, Inc., Form 10-K 2025", MO25, "2025"),
    r("mo.vol.fall", -10.0, "percent", "change in cigarette shipment volume, 2025", "Altria Group, Inc., Form 10-K 2025", MO25, "2025"),
    r("mo.price", 1680, "US$ million", "smokeable net revenues: 'lower shipment volume ($2,426 million), partially offset by higher "
      "pricing ($1,680 million)'", "Altria Group, Inc., Form 10-K 2025", MO25, "2025"),
    r("mo.volfx", -2426, "US$ million", "effect of lower shipment volume on smokeable net revenues, 2025",
      "Altria Group, Inc., Form 10-K 2025", MO25, "2025"),
    r("mo.margin", 63.0, "percent", "smokeable products segment's reported OCI margin, 2025 (OCI over revenues net of excise "
      "taxes; 61.0% in 2024)", "Altria Group, Inc., Form 10-K 2025", MO25, "2025"),
    r("mo.share", 40.5, "percent", "Marlboro's US cigarette retail share, 2025 (41.7% in 2024); 'Marlboro ... has been the "
      "largest-selling cigarette brand in the United States for over 50 years'", "Altria Group, Inc., Form 10-K 2025", MO25,
      "2025"),
    r("mo.discount", 31.8, "percent", "'Total cigarettes industry discount category retail share was 31.8%, an increase of 2.2 "
      "share points'", "Altria Group, Inc., Form 10-K 2025", MO25, "2025"),

    # the retailer
    r("clx.walmart", 26, "percent", "Clorox: 'Net sales to the Company's largest customer, Walmart ... were 26%, 27% and 25%' in "
      "fiscal 2026, 2025 and 2024", "The Clorox Company, Form 10-K for fiscal 2026", CLX26, "FY2026"),
    r("chd.walmart", 23, "percent", "Church & Dwight: Walmart 'approximately 23% of net sales in each of 2025, 2024, and 2023'; "
      "top four customers about 44%", "Church & Dwight Co., Inc., Form 10-K 2025", CHD25, "2025"),
    r("gis.walmart", 22, "percent", "General Mills: 'Walmart ... accounted for 22 percent of our consolidated net sales and 31 "
      "percent of net sales of our North America Retail segment' in fiscal 2026", "General Mills, Inc., Form 10-K for fiscal "
      "2026", GIS26, "FY2026"),
    r("kmb.walmart", 16, "percent", "Kimberly-Clark: Walmart 'represented approximately 16% in 2025 and 2024 and 15% in 2023 of "
      "our net sales from continuing operations'", "Kimberly-Clark Corporation, Form 10-K 2025", KMB25, "2025"),
    r("cl.walmart", 11, "percent", "Colgate-Palmolive: 'Our sales to Walmart, Inc. and its affiliates represented approximately "
      "11% of our Net sales in 2025'", "Colgate-Palmolive Company, Form 10-K 2025", CL25, "2025"),
    r("hsy.mclane", 27, "percent", "Hershey: 'approximately 27% of our consolidated net sales were made to McLane Company, Inc.', "
      "a wholesale distributor and 'the primary distributor of our products to Wal-Mart'", "The Hershey Company, Form 10-K 2025",
      HSY25, "2025"),
    r("kirk.margin", 1, "flag", "Costco: Kirkland Signature products 'generally carry higher margins than national brand products "
      "and represent a growing portion of our overall sales'", "Costco Wholesale Corporation, Form 10-K for fiscal 2026", COST26,
      "FY2026", note="a quotation, carried as a flag"),
)
