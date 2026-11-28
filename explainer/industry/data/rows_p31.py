"""Register rows for Part 31, *Grocery and Mass Retail*.  Checked 2026-11-28.

The Forms 10-K of Walmart (fiscal 2026, to 31 January 2026), Costco (fiscal 2026, to 30 August 2026), Kroger (fiscal 2025,
to 31 January 2026), Albertsons (fiscal 2025, to 28 February 2026), Dollar General (fiscal 2025) and Target; Kroger's 10-K
for fiscal 2020.  Series are the Filing Room's SEC and FRED extracts.
"""

from explainer.industry.register import Row, add

C = "2026-11-28"
P = (31,)
SEC = "https://www.sec.gov/Archives/edgar/data/"
WMT = SEC + "104169/000010416926000055/wmt-20260131.htm"
COST = SEC + "909832/000090983226000093/cost-20260830.htm"
KR = SEC + "56873/000110465926037723/kr-20260131x10k.htm"
KR20 = SEC + "56873/000155837021003706/kr-20210130x10k.htm"
ACI = SEC + "1646972/000164697226000032/aci-20260228.htm"
DG = SEC + "29534/000110465926032325/dg-20260130x10k.htm"


def r(key, value, unit, definition, source, url, fact, kind="filing", note="", **kw):
    return Row(key, value, unit, definition, source, url, fact, C, kind, note=note, parts=P, **kw)


def wmt(key, value, unit, definition, fact="FY2026 (to 2026-01-31)"):
    return r(key, value, unit, definition, "Walmart, Form 10-K for fiscal 2026", WMT, fact)


def cost(key, value, unit, definition, fact="FY2026 (to 2026-08-30)"):
    return r(key, value, unit, definition, "Costco Wholesale, Form 10-K for fiscal 2026", COST, fact)


def kr(key, value, unit, definition, fact="FY2025 (to 2026-01-31)"):
    return r(key, value, unit, definition, "Kroger, Form 10-K for fiscal 2025", KR, fact)


def wk(key, value, unit, definition, lo, hi):
    return r(key, value, unit, definition, "this series' assumption", "", "", kind="assumption", lo=lo, hi=hi)


add(
    # Walmart
    wmt("wm31.sales", 706.413, "US$ billion", "consolidated net sales, fiscal 2026 ($674.5bn in fiscal 2025)"),
    wmt("wm31.gp", 24.2, "percent", "gross profit as a percentage of net sales, fiscal 2026 (24.1 in fiscal 2025)"),
    wmt("wm31.opex", 20.9, "percent", "operating expenses as a percentage of net sales, fiscal 2026"),
    wmt("wm31.op", 4.2, "percent", "operating income as a percentage of net sales, fiscal 2026 ($29.8bn)"),
    wmt("wm31.units", 10955, "units", "retail units at 31 January 2026, with 1,057 million square feet"),
    wmt("wm31.us.sales", 482.975, "US$ billion", "Walmart U.S. net sales, fiscal 2026"),
    wmt("wm31.us.units", 4611, "units", "Walmart U.S. retail units at 31 January 2026, with 699 million square feet"),
    wmt("wm31.us.sqft", 699, "million square feet", "Walmart U.S. retail square feet at 31 January 2026"),
    wmt("wm31.us.op", 5.2, "percent", "Walmart U.S. operating income as a percentage of net sales, fiscal 2026 ($25.2bn)"),
    wmt("wm31.assoc", 2.1, "million", "approximately 2.1 million associates, 1.6 million of them in the U.S."),
    wmt("wm31.store", 1, "flag", "e-commerce growth 'was primarily driven by store-fulfilled pickup and delivery'"),
    wmt("wm31.edlp", 1, "flag", "'EDLP is our pricing philosophy under which we price items at a low price every day so our customers "
        "trust that our prices will not change under frequent promotional activity'"),

    # Costco
    cost("co31.fees", 5.907, "US$ billion", "membership fees, fiscal 2026 ($5.323bn in 2025, $4.828bn in 2024)"),
    cost("co31.sales", 297.247, "US$ billion", "net sales, fiscal 2026, up 10%"),
    cost("co31.members", 84.1, "million", "paid members at the end of fiscal 2026 (81.0 million in 2025, 76.2 million in 2024)"),
    cost("co31.members25", 81.0, "million", "paid members at the end of fiscal 2025"),
    cost("co31.members24", 76.2, "million", "paid members at the end of fiscal 2024"),
    cost("co31.renew", 92.3, "percent", "member renewal rate in the U.S. and Canada at the end of 2026 (89.8% worldwide)"),
    cost("co31.renew.ww", 89.8, "percent", "worldwide member renewal rate at the end of 2026"),
    cost("co31.exec", 42.3, "million", "Executive members, of 84.1 million paid members (38.7m in 2025); they earn 'generally 2% on "
         "qualified purchases'; their sales were 'approximately 75.2% of worldwide net sales'"),
    cost("co31.fee", 65, "US$ a year", "'Our annual fee for memberships is $65 in the U.S. ... and includes a free household card'"),
    wmt("wm31.intl.ecom", 6.3, "US$ billion", "International segment: 'strong eCommerce growth of $6.3 billion and $4.7 billion for fiscal "
        "2026 and 2025'"),
    cost("co31.wh", 939, "warehouses", "membership warehouses at 30 August 2026, 292 outside the U.S."),
    cost("co31.sqft", 148000, "square feet", "average warehouse space"),

    # Kroger, Albertsons, Dollar General
    kr("kr31.stores", 2697, "supermarkets", "supermarkets operated, with 2,250 pharmacies and 1,731 fuel centers in 35 states and D.C."),
    kr("kr31.ocado", 2.5, "US$ billion", "impairment and related charges in 2025 after closing automated fulfillment facilities in "
       "Pleasant Prairie, Frederick and Groveland in January 2026, which 'had not met operational or financial expectations', and "
       "cancelling the Charlotte site"),
    kr("kr31.merger", 1, "flag", "merger agreement with Albertsons of 13 October 2022; on 10 December 2024 the US District Court for the District of Oregon, at the FTC's request, issued a "
       "preliminary injunction enjoining the merger with Albertsons; Kroger delivered a termination notice on 11 December 2024; "
       "Albertsons sued for a $600m termination fee and further damages", "2024-12-10"),
    r("kr31.ocado2020", 1, "flag", "'The future success of the digital business will also depend on the efficiency and cost "
      "effectiveness of fulfilling orders across our modalities, whether in store, in pickup-only locations, and through customer "
      "fulfillment centers powered by Ocado'", "Kroger, Form 10-K for fiscal 2020", KR20, "2021-03"),
    r("aci31.stores", 2244, "stores", "stores operated at 28 February 2026 in 35 states and D.C., under 22 banners",
      "Albertsons Companies, Form 10-K for fiscal 2025", ACI, "2026-02-28"),
    r("dg31.stores", 20959, "stores", "'the largest discount retailer in the United States by number of stores, with 20,959 stores' at "
      "27 February 2026; 'approximately 75% of the U.S. population located within five miles of a Dollar General store'",
      "Dollar General, Form 10-K for fiscal 2025", DG, "2026-02-27"),

    # The Works
    wk("wk31.labour", 0.11, "share of sales", "a supermarket's store labour cost", 0.09, 0.13),
    wk("wk31.occupancy", 0.03, "share of sales", "rent and occupancy", 0.02, 0.05),
    wk("wk31.other", 0.07, "share of sales", "other costs that move with sales: distribution, cards, supplies, shrink above the gross margin",
       0.05, 0.09),
    wk("wk31.elasticity", -5.7, "elasticity", "how a store's customers respond to its overall price level against rivals nearby", -8.0, -4.0),
    wk("wk31.sales", 50.0, "US$ million a year", "a supermarket's sales", 30.0, 70.0),
)
