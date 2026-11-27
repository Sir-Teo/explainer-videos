"""Register rows for Part 26, *Property*.  Checked 2026-11-27.

The Forms 10-K for 2025 of Prologis, BXP, Simon Property Group, Realty Income, SL Green, Hudson Pacific, American Tower,
Equinix, Blackstone and CBRE; BXP's Forms 10-K for 2017-2024 and its third-quarter 2026 results (Form 8-K, Exhibit 99.1);
Realty Income's Forms 10-K for 2015-2024; WeWork's registration statement of 14 August 2019 (Form S-1) and its Form 8-K
of 7 November 2023; the Federal Reserve's Financial Stability Reports of October 2023 and November 2026; and Gupta,
Mittal and Van Nieuwerburgh, NBER Working Paper 30526 (September 2022).  Series are the Filing Room's SEC and FRED
extracts.
"""

from explainer.industry.register import Row, add

C = "2026-11-27"
P = (26,)
SEC = "https://www.sec.gov/Archives/edgar/data/"
PLD = SEC + "1045609/000119312526051453/pld-20251231.htm"
BXP = SEC + "1037540/000103754026000006/bxp-20251231.htm"
BXP_Q3 = SEC + "1037540/000103754026000041/q32026pressrelease.htm"
BXP_K = {2024: "000165642325000009/bxp-20241231.htm", 2023: "000165642324000007/bxp-20231231.htm",
         2022: "000165642323000013/bxp-20221231.htm", 2021: "000165642322000013/bxp-20211231.htm",
         2020: "000165642321000006/bxp-20201231.htm", 2019: "000165642320000007/bxpandbplp201910-k.htm",
         2018: "000165642319000006/bxpandbplp201810-k.htm", 2017: "000165642318000004/bxpandbplp201710-k.htm"}
SPG = SEC + "1063761/000110465926019419/spg-20251231x10k.htm"
O = SEC + "726728/000072672826000011/o-20251231.htm"
O_K = {2024: "000072672825000055/o-20241231.htm", 2023: "000072672824000047/o-20231231.htm",
       2022: "000072672823000044/o-20221231.htm", 2021: "000072672822000046/o-20211231.htm",
       2020: "000072672821000043/o-20201231.htm", 2019: "000072672820000033/realtyincome10k2019.htm",
       2018: "000072672819000038/realtyincome10k2018.htm", 2017: "000110465918011376/a18-1096_110k.htm",
       2016: "000110465917011170/a17-1163_110k.htm", 2015: "000110465916095923/a15-23382_110k.htm"}
SLG = SEC + "1040971/000162828026008669/slg-20251231.htm"
HPP = SEC + "1482512/000148251226000038/hpp-20251231.htm"
AMT = SEC + "1053507/000105350726000035/amt-20251231.htm"
EQIX = SEC + "1101239/000110123926000032/eqix-20251231.htm"
BX = SEC + "1393818/000119312526082531/d48618d10k.htm"
CBRE = SEC + "1138118/000113811826000005/cbre-20251231.htm"
WE_S1 = SEC + "1533523/000119312519220499/d781982ds1.htm"
WE_11 = SEC + "1813756/000119312523271902/d522028d8k.htm"
FSR26 = "https://www.federalreserve.gov/publications/files/financial-stability-report-20261113.pdf"
FSR23 = "https://www.federalreserve.gov/publications/files/financial-stability-report-20231020.pdf"
GMV = "https://www.nber.org/papers/w30526"


def r(key, value, unit, definition, source, url, fact, kind="filing", note="", **kw):
    return Row(key, value, unit, definition, source, url, fact, C, kind, note=note, parts=P, **kw)


def k10(name, url):
    def f(key, value, unit, definition, fact="2025", kind="filing"):
        return r(key, value, unit, definition, f"{name}, Form 10-K for 2025", url, fact, kind)
    return f


pld, bxp, spg, o_, slg, hpp, amt, eqix, bx, cbre = (k10(n, u) for n, u in (
    ("Prologis, Inc.", PLD), ("BXP, Inc.", BXP), ("Simon Property Group, Inc.", SPG), ("Realty Income Corporation", O),
    ("SL Green Realty Corp.", SLG), ("Hudson Pacific Properties, Inc.", HPP), ("American Tower Corporation", AMT),
    ("Equinix, Inc.", EQIX), ("Blackstone Inc.", BX), ("CBRE Group, Inc.", CBRE)))


def bxp_occ(y, v):
    return r(f"bxp.occ.{y}", v, "percent", f"in-service portfolio occupancy at 31 December {y}",
             f"BXP, Inc. (Boston Properties), Form 10-K for {y}", SEC + "1037540/" + BXP_K[y], f"{y}-12-31")


def o_yield(y, v, inv, what="initial weighted average cash lease yield"):
    return r(f"o.yield.{y}", v, "percent", f"Realty Income: {what} on its investments in {y} (${inv:,.2f} billion invested)",
             f"Realty Income Corporation, Form 10-K for {y}", SEC + "726728/" + O_K[y], str(y),
             note="the yield on what a landlord paid: first-year contractual cash rent over the price; the 10-Ks for "
                  "2015-2018 call it the initial weighted average contractual lease rate")


def fsr(key, value, unit, definition, fact="2026", url=FSR26, source="Board of Governors of the Federal Reserve System, "
        "Financial Stability Report, November 2026"):
    return r(key, value, unit, definition, source, url, fact, kind="official")


add(
    # Prologis: warehouses
    pld("pld.sqft", 1.3, "billion square feet", "the owned and managed portfolio, about 6,500 customers"),
    pld("pld.customers", 6500, "customers", "customers in the owned and managed portfolio"),
    pld("pld.occ", 95.4, "percent", "consolidated operating portfolio occupied at 31 December 2025 (95.4% in 2024; 95.8% for "
        "the owned and managed portfolio)", "2025-12-31"),
    pld("pld.rentchange", 50, "percent", "increase in net effective rents on leases rolled over in 2025 ('approximately "
        "50%')"),
    pld("pld.mtm", 18, "percent", "remaining lease mark-to-market: the amount by which market rents exceed in-place rents "
        "('approximately 18%')", "2025-12-31"),
    pld("pld.amazon", 6.3, "percent", "Amazon's share of consolidated net effective rent, the largest customer (35 million "
        "square feet; Home Depot 2.8%, FedEx 1.8%)", "2025-12-31"),
    pld("pld.yield", 6.7, "percent", "weighted average stabilized yield on development buildings stabilized in 2025 (6.2% in "
        "2024): stabilized NOI over total expected investment"),
    pld("pld.margin", 25.4, "percent", "estimated weighted average development margin on buildings stabilized in 2025 "
        "(19.2% in 2024)"),
    pld("pld.rental", 8159, "US$ million", "rental revenues, 2025"),
    pld("pld.rentexp", 1964, "US$ million", "rental expenses, 2025"),
    pld("pld.noi", 6188, "US$ million", "real estate segment net operating income, 2025"),
    pld("pld.reit90", 90, "percent", "'To qualify as a REIT, we are required each year to distribute at least 90% of our "
        "REIT taxable income'", "rule"),

    # BXP: offices
    bxp("bxp.occ", 86.7, "percent", "total in-service portfolio occupancy at 31 December 2025 (89.4% leased)", "2025-12-31"),
    bxp("bxp.sqft", 52.6, "million square feet", "179 properties owned or in joint ventures, mostly premier workplaces in "
        "Boston, Los Angeles, New York, San Francisco, Seattle and Washington", "2025-12-31"),
    bxp("bxp.sf", 77.0, "percent", "San Francisco in-service occupancy at 31 December 2025 (Boston 91.9%, Washington 91.7%, "
        "New York 83.8%)", "2025-12-31"),
    bxp("bxp.renew", -5.46, "percent", "change in second-generation cash rents on leases commenced in 2025, net (San Francisco "
        "-30.5%, Boston +15.4%)"),
    bxp("bxp.occ.boston", 91.9, "percent", "Boston in-service occupancy at 31 December 2025", "2025-12-31"),
    bxp("bxp.occ.dc", 91.7, "percent", "Washington, DC in-service occupancy at 31 December 2025", "2025-12-31"),
    bxp("bxp.occ.la", 86.5, "percent", "Los Angeles in-service occupancy at 31 December 2025", "2025-12-31"),
    bxp("bxp.occ.ny", 83.8, "percent", "New York in-service occupancy at 31 December 2025", "2025-12-31"),
    bxp("bxp.occ.seattle", 79.8, "percent", "Seattle in-service occupancy at 31 December 2025", "2025-12-31"),
    bxp("bxp.renew.sf", -30.47, "percent", "change in second-generation cash rents, net, San Francisco, leases commenced in 2025"),
    bxp("bxp.renew.boston", 15.35, "percent", "change in second-generation cash rents, net, Boston, leases commenced in 2025"),
    bxp("bxp.halted", 1, "flag", "'On the supply side, new office construction has effectively halted'"),
    bxp("bxp.impair", 85.8, "US$ million", "impairment losses on consolidated properties approved for sale in 2025 (and "
        "$145.1m on the Gateway Commons joint venture)"),
    bxp_occ(2017, 90.7), bxp_occ(2018, 91.4), bxp_occ(2019, 93.0), bxp_occ(2020, 90.1), bxp_occ(2021, 88.8),
    bxp_occ(2022, 88.6), bxp_occ(2023, 88.4), bxp_occ(2024, 87.5),
    r("bxp.occ.2026q3", 89.4, "percent", "total portfolio occupancy at 30 September 2026, up 100 basis points on the quarter, "
      "the fourth consecutive quarterly gain (91.9% leased)", "BXP, Inc., Form 8-K of 27 October 2026 (Exhibit 99.1)",
      BXP_Q3, "2026-09-30"),
    r("bxp.leased.2026q3", 91.9, "percent", "total portfolio leased at 30 September 2026, including signed leases not yet "
      "commenced", "BXP, Inc., Form 8-K of 27 October 2026 (Exhibit 99.1)", BXP_Q3, "2026-09-30"),

    # SL Green, Hudson Pacific
    slg("slg.occ", 93.0, "percent", "Manhattan same-store office occupancy, inclusive of leases signed but not yet commenced",
        "2025-12-31"),
    hpp("hpp.occ", 76.3, "percent", "in-service office portfolio occupied at 31 December 2025 (77.0% leased; studios 67.1%)",
        "2025-12-31"),
    hpp("hpp.impair", 299.3, "US$ million", "impairment loss on goodwill and certain non-real estate assets, 2025"),

    # Simon: malls
    spg("spg.occ", 96.4, "percent", "ending occupancy, US malls and Premium Outlets (96.5% in 2024, 95.8% in 2023)", "2025-12-31"),
    spg("spg.rent", 60.97, "US$ per square foot", "average base minimum rent per square foot, US malls and Premium Outlets "
        "(up 4.7%)", "2025-12-31"),
    spg("spg.props", 212, "properties", "income-producing US properties: 108 malls, 70 Premium Outlets, 16 Mills, six "
        "lifestyle centres and 12 other", "2025-12-31"),

    # Realty Income: the net lease and what a landlord pays for rent
    o_("o.props", 15511, "properties", "properties in the portfolio, 173 of them available for lease or sale", "2025-12-31"),
    o_("o.occ", 98.9, "percent", "occupancy by number of properties", "2025-12-31"),
    o_("o.term", 10.7, "years", "weighted average lease term of the real estate it acquired or developed in 2025 (10.1 years "
       "for acquisitions)"),
    o_("o.net", 1, "flag", "'A net lease typically requires the client to be responsible for monthly rent and certain property "
       "operating expenses including property taxes, insurance, and maintenance'"),
    o_("o.divyield", 5.7, "percent", "annualized dividend yield on the share price of $56.37 at 31 December 2025", "2025-12-31"),
    r("o.yield.2025", 7.3, "percent", "Realty Income: initial weighted average cash yield on its investments in 2025 ($6.3 "
      "billion invested; acquisitions alone 7.0%)", "Realty Income Corporation, Form 10-K for 2025", O, "2025"),
    o_yield(2024, 7.4, 3.9, "initial weighted average cash yield"), o_yield(2023, 7.1, 9.5, "initial weighted average cash yield"),
    o_yield(2022, 5.9, 9.0), o_yield(2021, 5.5, 6.41), o_yield(2020, 5.9, 2.31), o_yield(2019, 6.4, 3.72),
    o_yield(2018, 6.4, 1.8, "initial weighted average contractual lease rate"),
    o_yield(2017, 6.4, 1.52, "initial weighted average contractual lease rate"),
    o_yield(2016, 6.3, 1.86, "initial weighted average contractual lease rate"),
    o_yield(2015, 6.6, 1.26, "initial weighted average contractual lease rate"),

    # Towers and data centres
    amt("amt.sites", 149686, "sites", "communications sites owned and operated, including 862 distributed antenna networks",
        "2025-12-31"),
    amt("amt.terms", 1, "flag", "tenant leases have 'non-cancellable terms of five to ten years with multiple renewal terms', "
        "with rent that rises periodically, typically each year"),
    eqix("eqix.dcs", 255, "data centres", "IBX data centres controlled and operated, in 75 markets", "2025-12-31"),

    # Owners and the services firms
    bx("bx.re", 319.3, "US$ billion", "Real Estate segment total assets under management", "2025-12-31"),
    bx("bx.breit", 1, "flag", "'market volatility drove a material increase in BREIT repurchase requests beginning in late 2022, "
       "and pursuant to the terms of the vehicle, BREIT began to prorate such requests beginning in November 2022'"),
    cbre("cbre.rev", 40.55, "US$ billion", "total revenue, 2025 ($35.77bn in 2024)"),
    cbre("cbre.fm", 50.9, "percent", "facilities management's share of revenue, 2025"),
    cbre("cbre.pm", 18.9, "percent", "project management's share of revenue, 2025"),
    cbre("cbre.lease", 11.1, "percent", "advisory leasing's share of revenue, 2025"),
    cbre("cbre.sales", 5.2, "percent", "advisory sales' (property sales brokerage) share of revenue, 2025"),
    cbre("cbre.passthrough", 41.3, "percent", "pass-through costs (mostly the wages of staff in clients' buildings) as a share "
         "of revenue, 2025"),

    # WeWork
    r("we.lease", 47.2, "US$ billion", "future undiscounted minimum lease payments under signed operating and finance leases",
      "The We Company, Form S-1 of 14 August 2019", WE_S1, "2019-06-30"),
    r("we.leaseterm", 14, "years", "weighted average remaining term of its operating leases (finance leases 11 years)",
      "The We Company, Form S-1 of 14 August 2019", WE_S1, "2019-06-30"),
    r("we.member", 15, "months", "average commitment of its membership agreements ('more than 15 months', from about eight "
      "months at 1 December 2017)", "The We Company, Form S-1 of 14 August 2019", WE_S1, "2019-06-01"),
    r("we.tam", 3.0, "US$ trillion", "'Among the approximately 255 million potential members across our 280 target cities "
      "globally, we estimate a total opportunity of $3.0 trillion'", "The We Company, Form S-1 of 14 August 2019", WE_S1,
      "2019-08"),
    r("we.ch11", 1, "flag", "WeWork Inc. and certain subsidiaries filed voluntary petitions under Chapter 11 on 6 November 2023",
      "WeWork Inc., Form 8-K of 7 November 2023", WE_11, "2023-11-06"),

    # The Federal Reserve
    fsr("fsr.cre", 22848, "US$ billion", "commercial real estate's market value, 2026:Q2 (nominal)", "2026-Q2"),
    fsr("fsr.real", -1.3, "percent", "real (CPI-deflated) growth of commercial real estate prices, June 2025 to June 2026 "
        "(average 2.6% a year since 1999)", "2025-06 to 2026-06"),
    fsr("fsr.capavg", 6.79, "percent", "average capitalization rate (income of newly purchased commercial properties over "
        "their prices), 2001-2026; rates 'have increased sizably from historical lows in 2022'", "2001-2026"),
    fsr("fsr.cmbs", 1, "flag", "'A substantial volume of non-agency commercial mortgage-backed securities (CMBS) debt is set to "
        "mature in late 2026 ... To date, lenders' willingness to extend or restructure maturing loans has helped mitigate "
        "this risk'"),
    fsr("fsr.office23", 1, "flag", "'Fundamentals in the market for office properties were especially weak, as vacancy rates "
        "have risen and rent growth slowed'", "2023", FSR23,
        "Board of Governors of the Federal Reserve System, Financial Stability Report, October 2023"),

    # the Census Bureau's categories
    r("census.dc", 1, "flag", "construction spending's 'office' category includes data centres ('buildings that contain the "
      "hardware needed for storing, processing, and transmitting digital information'); 'commercial' includes warehouses and "
      "shops", "Census Bureau, Construction Spending: definitions", "https://www.census.gov/construction/c30/definitions.html",
      "current", kind="official"),

    # Gupta, Mittal and Van Nieuwerburgh
    r("gmv.short", -44.8, "percent", "estimated change in the value of New York City office buildings in 2020, from remote "
      "work's effect on lease income and risk", "Gupta, Mittal and Van Nieuwerburgh, 'Work From Home and the Office Real Estate "
      "Apocalypse', NBER Working Paper 30526, September 2022", GMV, "2020", kind="study"),
    r("gmv.long", -39.2, "percent", "estimated long-run change in the value of New York City office buildings", "Gupta, Mittal "
      "and Van Nieuwerburgh, NBER Working Paper 30526, September 2022", GMV, "long run (model)", kind="study"),
    r("gmv.us", 453.6, "US$ billion", "their extrapolation of the long-run fall in the value of all US office buildings",
      "Gupta, Mittal and Van Nieuwerburgh, NBER Working Paper 30526, September 2022", GMV, "long run (model)", kind="study"),
)
