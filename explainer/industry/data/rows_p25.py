"""Register rows for Part 25, *Homes*.  Checked 2026-11-27.

D.R. Horton's Form 10-K for fiscal 2026 (to 30 September 2026) and its results releases of 28 October 2025 and 29 October
2026 (Forms 8-K, Exhibit 99.1); Lennar's Form 10-K for fiscal 2025 (to 30 November 2025); NVR's, Fannie Mae's, Compass's
and Invitation Homes' Forms 10-K for 2025.  Series are the Filing Room's SEC and FRED extracts.
"""

from explainer.industry.register import Row, add

C = "2026-11-27"
P = (25,)
SEC = "https://www.sec.gov/Archives/edgar/data/"
DHI = SEC + "882184/000088218426000157/dhi-20260930.htm"
DHI_R26 = SEC + "882184/000088218426000119/a9302026exhibit991.htm"
DHI_R25 = SEC + "882184/000088218425000044/a9302025exhibit991.htm"
LEN = SEC + "920760/000162828026003870/len-20251130.htm"
NVR = SEC + "906163/000090616326000018/nvr-20251231.htm"
FNM = SEC + "310522/000031052226000015/fnm-20251231.htm"
COMP = SEC + "1563190/000156319026000057/comp-20251231.htm"
INVH = SEC + "1687229/000168722926000016/invh-20251231.htm"


def r(key, value, unit, definition, source, url, fact, kind="filing", note="", **kw):
    return Row(key, value, unit, definition, source, url, fact, C, kind, note=note, parts=P, **kw)


def dhi(key, value, unit, definition, fact="FY2026 (to 2026-09-30)", url=DHI_R26,
        source="D.R. Horton, Inc., Form 8-K of 29 October 2026 (Exhibit 99.1)"):
    return r(key, value, unit, definition, source, url, fact)


def len_(key, value, unit, definition, fact="FY2025 (to 2025-11-30)"):
    return r(key, value, unit, definition, "Lennar Corporation, Form 10-K for fiscal 2025", LEN, fact)


def nvr(key, value, unit, definition, fact="2025"):
    return r(key, value, unit, definition, "NVR, Inc., Form 10-K for 2025", NVR, fact)


def fnm(key, value, unit, definition, fact="2025"):
    return r(key, value, unit, definition, "Fannie Mae, Form 10-K for 2025", FNM, fact)


add(
    dhi("dhi.rev", 33.0, "US$ billion", "consolidated revenues, fiscal 2026"),
    dhi("dhi.closed", 84202, "homes", "homes closed, fiscal 2026 (down 1%)"),
    dhi("dhi.price", 363.6, "US$ thousand", "average closing price, fiscal 2026 (down 2%)", url=DHI,
        source="D.R. Horton, Inc., Form 10-K for fiscal 2026"),
    dhi("dhi.gm", 20.2, "percent", "home sales gross margin, fiscal 2026 (21.5% in fiscal 2025)", url=DHI,
        source="D.R. Horton, Inc., Form 10-K for fiscal 2026"),
    dhi("dhi.gm.prev", 21.5, "percent", "home sales gross margin, fiscal 2025", url=DHI,
        source="D.R. Horton, Inc., Form 10-K for fiscal 2026", fact="FY2025"),
    dhi("dhi.pretax", 11.2, "percent", "homebuilding pre-tax profit margin, fiscal 2026"),
    dhi("dhi.owned", 130500, "lots", "land/lots owned at 30 September 2026 (23% of the total)", fact="2026-09-30"),
    dhi("dhi.controlled", 440100, "lots", "lots controlled through land and lot purchase contracts at 30 September 2026 (77%)",
        fact="2026-09-30"),
    dhi("dhi.owned.2025", 147000, "lots", "land/lots owned at 30 September 2025 (25%)", fact="2025-09-30"),
    dhi("dhi.controlled.2025", 444900, "lots", "lots controlled through purchase contracts at 30 September 2025 (75%)",
        fact="2025-09-30"),
    dhi("dhi.unsold", 17700, "homes", "unsold homes in inventory at fiscal year end, of 28,200 homes in inventory (8,800 "
        "completed)", fact="2026-09-30"),
    dhi("dhi.largest", 1, "flag", "'we have been the largest homebuilder in the United States by volume every year since 2002'",
        url=DHI, source="D.R. Horton, Inc., Form 10-K for fiscal 2026"),
    dhi("dhi.buydown", 1, "flag", "'We use a variety of incentives, including mortgage rate buydowns'; fiscal 2026 gross margin fell "
        "'reflecting a 2% decline in our average sales price and higher incentives, including mortgage rate buydowns'; 'We "
        "expect sales incentives to remain elevated during fiscal 2027'", url=DHI, source="D.R. Horton, Inc., Form 10-K for "
        "fiscal 2026"),
    dhi("dhi.inventory", 28200, "homes", "homes in inventory at the end of fiscal 2026", fact="2026-09-30"),
    dhi("dhi.finished", 8800, "homes", "unsold homes already completed at the end of fiscal 2026 (600 completed more than six "
        "months)", fact="2026-09-30"),
    dhi("dhi.forestar", 38400, "lots", "lots owned or controlled by Forestar, D.R. Horton's majority-owned lot developer, at 30 "
        "September 2026", fact="2026-09-30"),
    dhi("dhi.third", 68, "percent", "share of homes closed in fiscal 2026 that were on lots developed by Forestar or third "
        "parties (65% in fiscal 2025)"),
    dhi("dhi.quote", 1, "flag", "'Housing market conditions became more challenging during the fourth quarter as rising "
        "mortgage rates, affordability constraints and cautious consumer sentiment continued to pressure new home demand'"),
    dhi("dhi.g26.rev.lo", 33.5, "US$ billion", "28 October 2025: initial guidance for fiscal 2026, 'Consolidated revenues in "
        "the range of $33.5 billion to $35.0 billion'", fact="FY2026 (forecast)", url=DHI_R25,
        source="D.R. Horton, Inc., Form 8-K of 28 October 2025 (Exhibit 99.1)"),
    dhi("dhi.g26.rev.hi", 35.0, "US$ billion", "upper end of the fiscal 2026 revenue guidance", fact="FY2026 (forecast)",
        url=DHI_R25, source="D.R. Horton, Inc., Form 8-K of 28 October 2025 (Exhibit 99.1)"),
    dhi("dhi.g26.homes.lo", 86000, "homes", "fiscal 2026 guidance: 'Homes closed by homebuilding operations of 86,000 homes to "
        "88,000 homes'", fact="FY2026 (forecast)", url=DHI_R25,
        source="D.R. Horton, Inc., Form 8-K of 28 October 2025 (Exhibit 99.1)"),
    dhi("dhi.g26.homes.hi", 88000, "homes", "upper end of the fiscal 2026 closings guidance", fact="FY2026 (forecast)",
        url=DHI_R25, source="D.R. Horton, Inc., Form 8-K of 28 October 2025 (Exhibit 99.1)"),
    dhi("dhi.closed.2025", 84863, "homes", "homes closed, fiscal 2025", fact="FY2025", url=DHI_R25,
        source="D.R. Horton, Inc., Form 8-K of 28 October 2025 (Exhibit 99.1)"),
    dhi("dhi.g27.rev.lo", 30.0, "US$ billion", "29 October 2026: initial guidance for fiscal 2027, 'Consolidated revenues in "
        "the range of $30.0 billion to $32.0 billion'", fact="FY2027 (forecast)"),
    dhi("dhi.g27.rev.hi", 32.0, "US$ billion", "upper end of the fiscal 2027 revenue guidance", fact="FY2027 (forecast)"),
    dhi("dhi.g27.homes.lo", 79000, "homes", "fiscal 2027 guidance: 'Homes closed by homebuilding operations of 79,000 homes to "
        "84,000 homes'", fact="FY2027 (forecast)"),
    dhi("dhi.g27.homes.hi", 84000, "homes", "upper end of the fiscal 2027 closings guidance", fact="FY2027 (forecast)"),
    dhi("dhi.orders.q4", 18619, "homes", "net sales orders in the fourth quarter of fiscal 2026 (down 7%)", fact="Q4 FY2026"),

    len_("len.deliveries", 82583, "homes", "new home deliveries, fiscal 2025 (80,210 in fiscal 2024)"),
    len_("len.price", 391, "US$ thousand", "average sales price of homes delivered, fiscal 2025 ($423,000 in 2024, $445,000 in "
         "2023)"),
    len_("len.price.2024", 423, "US$ thousand", "average sales price, fiscal 2024", "FY2024"),
    len_("len.price.2023", 445, "US$ thousand", "average sales price, fiscal 2023", "FY2023"),
    len_("len.gm", 17.7, "percent", "gross margin on home sales, fiscal 2025 (22.3% in fiscal 2024)"),
    len_("len.gm.prev", 22.3, "percent", "gross margin on home sales, fiscal 2024", "FY2024"),
    len_("len.incent", 62.7, "US$ thousand", "average sales incentives per home delivered, fiscal 2025 ($48,800 in 2024)"),
    len_("len.incent.pct", 13.8, "percent", "sales incentives as a share of revenues, fiscal 2025 (10.3% in 2024)"),
    len_("len.incent.prev", 48.8, "US$ thousand", "average sales incentives per home delivered, fiscal 2024", "FY2024"),
    len_("len.controlled", 98, "percent", "'At November 30, 2025, 98% of our total homesites were controlled through options "
         "with land banks, land sellers and joint ventures compared to 82% at November 30, 2024'", "2025-11-30"),
    len_("len.controlled.prev", 82, "percent", "share of homesites controlled through options at 30 November 2024", "2024-11-30"),
    len_("len.walked", 15500, "homesites", "controlled homesites walked away from in fiscal 2025, with $23.1 million of deposit "
         "write-offs (6,300 and $5.1 million in 2024)"),
    len_("len.writeoff", 23.1, "US$ million", "deposit write-offs on homesites walked away from, fiscal 2025"),
    len_("len.subs", 1, "flag", "'We hire subcontractors for site improvements and virtually all of the work involved in the "
         "construction of homes'"),

    nvr("nvr.lpa", 1, "flag", "'We generally do not engage in land development ... Instead, we typically acquire finished "
        "building lots from various third-party land developers pursuant to fixed price lot purchase agreements (LPAs) "
        "that require deposits that may be forfeited'; the strategy 'avoids the financial requirements and risks associated "
        "with direct land ownership and land development'"),
    nvr("nvr.lots", 169250, "lots", "lots controlled under LPAs at 31 December 2025, 'through deposits in cash and letters of "
        "credit totaling approximately $920,100' thousand", "2025-12-31"),
    nvr("nvr.deposits", 920.1, "US$ million", "cash deposits on lots under LPAs at 31 December 2025", "2025-12-31"),
    nvr("nvr.price", 460.6, "US$ thousand", "average settlement price, 2025"),
    nvr("nvr.settle", 21915, "homes", "settlements, 2025"),
    nvr("nvr.gm", 21.2, "percent", "homebuilding gross profit margin, 2025 (23.7% in 2024, 24.3% in 2023)"),

    fnm("fnm.book", 4.1, "US$ trillion", "Fannie Mae's guaranty book of business, 2025"),
    fnm("fnm.share", 24, "percent", "share of total US residential mortgage debt outstanding Fannie Mae owned or guaranteed at "
        "30 September 2025 ('the largest guarantor')", "2025-09-30"),
    fnm("fnm.debt", 17.0, "US$ trillion", "total US residential mortgage debt outstanding, approximately, 30 September 2025 (per "
        "the Federal Reserve)", "2025-09-30"),
    fnm("fnm.lock", 6.15, "percent", "'most of our single-family conventional guaranty book of business as of December 31, "
        "2025 had an interest rate lower than' the 30-year rate of 6.15%; 'even if interest rates decline to 5%, most of the "
        "borrowers ... still would not be incentivized to refinance'", "2025-12-31"),
    fnm("fnm.orig.2025", 1.94, "US$ trillion", "estimated total US single-family mortgage originations in 2025"),
    fnm("fnm.orig.2026", 2.41, "US$ trillion", "Fannie Mae's forecast of total single-family originations in 2026 ('increase "
        "from 2025 levels by approximately 24%')", "2026 (forecast)"),
    fnm("fnm.refi.2025", 560, "US$ billion", "estimated refinance originations in 2025"),
    fnm("fnm.refi.2026", 917, "US$ billion", "forecast refinance originations in 2026", "2026 (forecast)"),

    r("comp.nar", 1, "flag", "'NAR agreed to implement certain industry-wide practice changes, including ... prohibiting buyer "
      "brokers' offers of compensation from being included in listings on Multiple Listing Services and requiring a buyer to "
      "enter into a written agreement with their agent that would set forth the buyer broker's fee before showing the buyer a "
      "property. These changes went into effect in August of 2024'", "Compass, Inc., Form 10-K for 2025", COMP, "2024-08"),
    r("comp.anywhere", 83.5, "US$ million", "monetary relief in the nationwide settlement of antitrust claims against Anywhere "
      "(acquired by Compass), with five years of injunctive relief", "Compass, Inc., Form 10-K for 2025", COMP, "2024"),
    r("invh.homes", 86192, "homes", "single-family homes for lease Invitation Homes wholly owned at 31 December 2025 (about 1,880 "
      "square feet, three to four bedrooms)", "Invitation Homes Inc., Form 10-K for 2025", INVH, "2025-12-31"),
)
