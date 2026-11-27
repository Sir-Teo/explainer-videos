"""Register rows for Part 27, *Shipping and Ports*.  Checked 2026-11-27.

ZIM's Forms 20-F for 2020, 2021, 2023 and 2025 and its results and guidance releases of 2026 (Forms 6-K, Exhibit 99.1);
Frontline's Form 20-F for 2025 and third-quarter 2026 report (Form 6-K, Exhibit 1); Matson's Form 10-K for 2025; E2open's
Form 10-K of May 2021.  The industry statistics ZIM quotes are Alphaliner's.  Series are the Filing Room's SEC, FRED,
World Bank and IMF PortWatch extracts.
"""

from explainer.industry.register import Row, add

C = "2026-11-27"
P = (27,)
SEC = "https://www.sec.gov/Archives/edgar/data/"
ZIM25 = SEC + "1654126/000117891326000784/zk2634463.htm"
ZIM23 = SEC + "1654126/000117891324000920/zk2431081.htm"
ZIM21 = SEC + "1654126/000141057822000304/tmb-20211231x20f.htm"
ZIM20 = SEC + "1654126/000110465921039375/tm217869d3_20f.htm"
ZIM_Q4 = SEC + "1654126/000117891326000776/exhibit_99-1.htm"
ZIM_Q1 = SEC + "1654126/000117891326002824/exhibit_99-1.htm"
ZIM_Q2 = SEC + "1654126/000117891326004191/exhibit_99-1.htm"
ZIM_OCT = SEC + "1654126/000117891326004724/exhibit_99-1.htm"
ZIM_Q3 = SEC + "1654126/000117891326005268/exhibit_99-1.htm"
FRO = SEC + "913290/000162828026021774/fro-20251231.htm"
FRO_Q3 = SEC + "913290/000091957426008221/p15160196_exh-1.htm"
MATX = SEC + "3453/000110465926020944/matx-20251231x10k.htm"
E2 = SEC + "1800347/000156459021029113/etwo-10k_20210228.htm"


def r(key, value, unit, definition, source, url, fact, kind="filing", note="", **kw):
    return Row(key, value, unit, definition, source, url, fact, C, kind, note=note, parts=P, **kw)


def zim(key, value, unit, definition, fact="2025", url=ZIM25, source="ZIM Integrated Shipping Services, Form 20-F for 2025"):
    return r(key, value, unit, definition, source, url, fact)


def alpha(key, value, unit, definition, fact="2025-12-31", url=ZIM25, year=2025):
    return r(key, value, unit, definition + " (Alphaliner, as quoted by ZIM)",
             f"ZIM Integrated Shipping Services, Form 20-F for {year}", url, fact, kind="tracker")


def rate(y, v, url, year):
    return zim(f"zim.rate.{y}", v, "US$ per TEU", f"ZIM's average freight rate per TEU carried, {y} (revenue from containerized "
               "cargo over TEUs carried)", str(y), url, f"ZIM Integrated Shipping Services, Form 20-F for {year}")


def qrate(q, v, url, src):
    return zim(f"zim.rate.{q}", v, "US$ per TEU", f"ZIM's average freight rate per TEU, {q}", q, url, src)


def fro(key, value, unit, definition, fact="Q3 2026", url=FRO_Q3, source="Frontline plc, third-quarter 2026 report (Form 6-K of 20 "
        "November 2026, Exhibit 1)"):
    return r(key, value, unit, definition, source, url, fact)


add(
    # ZIM's freight rate, the market's capacity and its forecasts
    rate(2016, 902, ZIM20, 2020), rate(2017, 995, ZIM20, 2020), rate(2018, 973, ZIM20, 2020), rate(2019, 1009, ZIM20, 2020),
    rate(2020, 1229, ZIM20, 2020), rate(2021, 2786, ZIM21, 2021), rate(2022, 3240, ZIM23, 2023), rate(2023, 1203, ZIM23, 2023),
    rate(2024, 1888, ZIM25, 2025), rate(2025, 1551, ZIM25, 2025),
    qrate("2025Q1", 1776, ZIM_Q1, "ZIM, first-quarter 2026 results (Form 6-K of 20 May 2026)"),
    qrate("2025Q2", 1479, ZIM_Q2, "ZIM, second-quarter 2026 results (Form 6-K of 19 August 2026)"),
    qrate("2025Q3", 1602, ZIM_Q3, "ZIM, third-quarter 2026 results (Form 6-K of 18 November 2026)"),
    qrate("2025Q4", 1333, ZIM_Q4, "ZIM, fourth-quarter 2025 results (Form 6-K of 9 March 2026)"),
    qrate("2026Q1", 1310, ZIM_Q1, "ZIM, first-quarter 2026 results (Form 6-K of 20 May 2026)"),
    qrate("2026Q2", 1590, ZIM_Q2, "ZIM, second-quarter 2026 results (Form 6-K of 19 August 2026)"),
    qrate("2026Q3", 2480, ZIM_Q3, "ZIM, third-quarter 2026 results (Form 6-K of 18 November 2026)"),
    zim("zim.zone.pacific", 1852, "US$ per TEU", "average freight rate per TEU carried, Pacific trade zone, 2025 (2,444 in 2024)"),
    zim("zim.zone.suez", 1965, "US$ per TEU", "average freight rate per TEU carried, Cross-Suez trade zone, 2025 (2,607 in 2024)"),
    zim("zim.zone.atl", 1343, "US$ per TEU", "average freight rate per TEU carried, Atlantic-Europe trade zone, 2025 (1,240 in 2024)"),
    zim("zim.zone.latam", 1490, "US$ per TEU", "average freight rate per TEU carried, Latin America trade zone, 2025 (1,646 in 2024)"),
    zim("zim.zone.asia", 960, "US$ per TEU", "average freight rate per TEU carried, Intra-Asia trade zone, 2025 (1,022 in 2024)"),
    zim("zim.zone.pacific.teu", 1577, "thousand TEU", "TEUs carried in the Pacific trade zone, 2025, of 3,663 thousand in all"),
    zim("zim.teu.2025", 3663, "thousand TEU", "TEUs carried, 2025 (3,751 thousand in 2024)"),
    zim("zim.teu.2019", 2821, "thousand TEU", "TEUs carried, 2019", "2019", ZIM20, "ZIM Integrated Shipping Services, Form 20-F for 2020"),
    zim("zim.ships", 128, "vessels", "vessels operated at 31 December 2025, 16 owned and 112 chartered in, 708,543 TEU", "2025-12-31"),
    zim("zim.owned", 16, "vessels", "vessels owned at 31 December 2025", "2025-12-31"),
    zim("zim.bunker", 25.7, "percent", "bunker (fuel) and energy expenses as a share of operating expenses and cost of services, "
        "2025 (28.5% in 2024, 28.3% in 2023)"),
    zim("zim.q3rev", 2.71, "US$ billion", "revenues, third quarter of 2026 (up 53%)", "Q3 2026", ZIM_Q3,
        "ZIM, third-quarter 2026 results (Form 6-K of 18 November 2026)"),
    zim("zim.q3ni", 830, "US$ million", "net income, third quarter of 2026 ($123m a year earlier)", "Q3 2026", ZIM_Q3,
        "ZIM, third-quarter 2026 results (Form 6-K of 18 November 2026)"),
    zim("zim.g.aug.lo", 2.0, "US$ billion", "full-year 2026 Adjusted EBITDA guidance, low end, 19 August 2026 ($2.0-2.4bn)", "2026-08-19",
        ZIM_Q2, "ZIM, second-quarter 2026 results (Form 6-K of 19 August 2026)"),
    zim("zim.g.aug.hi", 2.4, "US$ billion", "full-year 2026 Adjusted EBITDA guidance, high end, 19 August 2026", "2026-08-19",
        ZIM_Q2, "ZIM, second-quarter 2026 results (Form 6-K of 19 August 2026)"),
    zim("zim.g.oct.lo", 2.7, "US$ billion", "full-year 2026 Adjusted EBITDA guidance, low end, 6 October 2026 ($2.7-3.0bn)",
        "2026-10-06", ZIM_OCT, "ZIM, guidance release (Form 6-K of 6 October 2026)"),
    zim("zim.g.oct.hi", 3.0, "US$ billion", "full-year 2026 Adjusted EBITDA guidance, high end, 6 October 2026", "2026-10-06",
        ZIM_OCT, "ZIM, guidance release (Form 6-K of 6 October 2026)"),
    zim("zim.g.nov.lo", 3.3, "US$ billion", "full-year 2026 Adjusted EBITDA guidance, low end, 18 November 2026 ($3.3-3.5bn)",
        "2026-11-18", ZIM_Q3, "ZIM, third-quarter 2026 results (Form 6-K of 18 November 2026)"),
    zim("zim.g.nov.hi", 3.5, "US$ billion", "full-year 2026 Adjusted EBITDA guidance, high end, 18 November 2026", "2026-11-18",
        ZIM_Q3, "ZIM, third-quarter 2026 results (Form 6-K of 18 November 2026)"),
    zim("zim.noguide", 1, "flag", "'In light of the proposed transaction with Hapag-Lloyd, ZIM will not be providing full-year "
        "2026 financial guidance'", "2026-03-09", ZIM_Q4, "ZIM, fourth-quarter 2025 results (Form 6-K of 9 March 2026)"),
    zim("zim.hapag", 35.00, "US$ per share", "Hapag-Lloyd's cash price under the merger agreement of 16 February 2026; approved "
        "by ZIM's shareholders on 30 April 2026; subject to approvals including the State of Israel's under its Special State "
        "Share; the original application was terminated and a new one is to be submitted; targeted to close in the first "
        "quarter of 2027", "2026-02-16", ZIM_Q3, "ZIM, third-quarter 2026 results (Form 6-K of 18 November 2026)"),
    alpha("alpha.fleet", 33.3, "million TEU", "global container ship capacity, about 6,700 vessels"),
    alpha("alpha.ships", 6700, "vessels", "container ships in the global fleet"),
    alpha("alpha.order", 11.3, "million TEU", "container ships on order"),
    alpha("alpha.deliv26", 1.4, "million TEU", "expected deliveries of container ships in 2026", "2026 (expected)"),
    alpha("alpha.g24", 10.3, "percent", "growth of global container ship capacity in 2024", "2024"),
    alpha("alpha.g25", 7.3, "percent", "growth of global container ship capacity in 2025", "2025"),
    alpha("alpha.g26", 3.7, "percent", "expected growth of global container ship capacity in 2026", "2026 (expected)"),
    alpha("alpha.d25", 3.5, "percent", "growth in demand for container shipping in 2025", "2025"),
    alpha("alpha.d26", 2.5, "percent", "projected growth in demand for container shipping in 2026", "2026 (projected)"),
    alpha("alpha.top3", 47.8, "percent", "share of global capacity held by the top three carriers, MSC, Maersk and CMA CGM",
          "2025-12"),
    alpha("alpha.top3.2023", 46.7, "percent", "share of global capacity held by MSC, Maersk and CMA CGM", "2023-12", ZIM23, 2023),
    alpha("alpha.fleet.2021", 25.0, "million TEU", "global container ship capacity, about 5,515 vessels", "2021-12-31", ZIM21, 2021),
    alpha("alpha.g21", 4.5, "percent", "growth of global container ship capacity in 2021", "2021", ZIM21, 2021),
    alpha("alpha.d21", 6.7, "percent", "projected growth in demand for container shipping, as stated at the end of 2021",
          "2021-12-31", ZIM21, 2021),

    # Frontline: tankers
    fro("fro.vlcc.q3", 148500, "US$ a day", "average daily spot time charter equivalent earnings for VLCCs, third quarter of 2026 "
        "(Suezmax $102,500, LR2/Aframax $67,800)"),
    fro("fro.vlcc.q2", 152700, "US$ a day", "VLCC spot TCE, second quarter of 2026", "Q2 2026"),
    fro("fro.vlcc.q4", 562600, "US$ a day", "VLCC spot TCE contracted for the fourth quarter of 2026, 68% of its spot days covered",
        "Q4 2026 (68% booked)"),
    fro("fro.vlcc.be", 24100, "US$ a day", "estimated average daily cash breakeven for its VLCCs over the next twelve months",
        "next 12 months"),
    fro("fro.suez.q3", 102500, "US$ a day", "Suezmax spot TCE, third quarter of 2026"),
    fro("fro.tc", 76900, "US$ a day", "average rate on one-year time charters agreed in January 2026 for seven VLCCs built in "
        "2016-2018", "2026-01", FRO, "Frontline plc, Form 20-F for 2025"),
    fro("fro.order", 27.0, "percent", "tanker orderbook in Frontline's classes as a share of the existing fleet (332 VLCCs, 215 "
        "Suezmaxes and 216 Aframax/LR2s on order)"),
    fro("fro.hormuz", 1, "flag", "'The Strait of Hormuz remains substantially disrupted for commercial traffic, and attacks on "
        "tankers in and around the strait have intensified'"),
    fro("fro.sale", 270.0, "US$ million", "sale price of two VLCCs built in 2017"),

    # Matson: the Jones Act
    r("matx.jones", 51, "percent", "share of Matson's Ocean Transportation revenue from Hawaii and Alaska trades subject to the "
      "Jones Act, 2025 (50% in 2024, 55% in 2023)", "Matson, Inc., Form 10-K for 2025", MATX, "2025"),
    r("matx.rule", 1, "flag", "under the Jones Act, vessels carrying cargo between covered US ports must 'be built in the U.S., "
      "registered under the U.S. flag, be manned predominantly by U.S. crews, and owned and operated by U.S.-organized "
      "companies'", "Matson, Inc., Form 10-K for 2025", MATX, "current"),

    # The Ever Given
    r("e2.evergiven", 6, "days", "'In March 2021, the Suez Canal was blocked for six days after the grounding of Ever Given, a "
      "container ship'", "E2open Parent Holdings, Form 10-K for the year to 28 February 2021", E2, "2021-03"),

    # the study
    r("gh.waves", 1, "flag", "high current earnings in dry bulk shipping go with high ship prices and heavy investment, and are "
      "followed by low returns; firms appear to over-extrapolate demand and neglect competitors' supply response",
      "Robin Greenwood and Samuel G. Hanson, 'Waves in Ship Prices and Investment', NBER Working Paper 19246 (abstract)", "https://www.nber.org/papers/w19246", "dry bulk shipping, the paper's sample", kind="study"),

    # this series' assumption for the hook
    r("hook.pairs", 5000, "pairs of shoes", "pairs of trainers in boxes in one 40-foot container (two TEU), a round figure: a "
      "40-foot box holds about 67 cubic metres, a shoebox about a hundredth of one", "this series' assumption", "", "assumption",
      kind="assumption", lo=4000, hi=6000),
)
