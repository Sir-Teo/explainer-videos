"""Register rows for Part 15, *Semiconductors*.  Checked 2026-11-27.

Gordon Moore's articles of 1965 and 1975; TSMC's Form 20-F for 2025 and its Forms 6-K of March 2025 and October 2026;
ASML's Form 20-F for 2025; Intel's, Nvidia's and General Motors' Forms 10-K; the World Semiconductor Trade Statistics'
forecasts and releases of 2023-2026 and the Semiconductor Industry Association's release of November 2026; the Bureau of
Industry and Security's rules in the Federal Register, 2022-2026.  Series are the Filing Room's FRED, Our World in Data
and SEC extracts.
"""

from explainer.industry.register import Row, add

C = "2026-11-27"
P = (15,)
MOORE65 = "https://archive.computerhistory.org/resources/access/text/2017/03/102770822-05-01-acc.pdf"
MOORE75 = "https://www.eng.auburn.edu/~agrawvd/COURSE/E7770_Spr07/READ/Gordon_Moore_1975_Speech.pdf"
TSM20F = "https://www.sec.gov/Archives/edgar/data/1046179/000162828026025362/tsm-20251231.htm"
TSMQ3 = "https://www.sec.gov/Archives/edgar/data/1046179/000104617926000726/a3q26e_withguidancexfinal.htm"
TSMQ3P = "https://www.sec.gov/Archives/edgar/data/1046179/000104617926000726/a3q26presentatione006.jpg"
TSMUS = "https://www.sec.gov/Archives/edgar/data/1046179/000104617925000024/tsmcexpandinvestmentintheu.htm"
ASML = "https://www.sec.gov/Archives/edgar/data/937966/000162828026011378/asml-20251231.htm"
INTC = "https://www.sec.gov/Archives/edgar/data/50863/000005086326000011/intc-20251227.htm"
NVDA = "https://www.sec.gov/Archives/edgar/data/1045810/000104581026000021/nvda-20260125.htm"
GM = "https://www.sec.gov/Archives/edgar/data/1467858/000146785822000034/gm-20211231.htm"
WSTS26 = "https://www.wsts.org/esraCMS/extension/media/f/WST/7618/WSTS_FC-Release-2026-May.pdf"
WSTS25 = "https://www.wsts.org/esraCMS/extension/media/f/WST/7310/WSTS_FC-Release-2025_11.pdf"
WSTS23 = "https://www.wsts.org/esraCMS/extension/media/f/WST/6254/WSTS_nr-2023_11.pdf"
WSTSQ2 = "https://www.wsts.org/76/Global-Semiconductor-Market-records-exceptional-growth-in-Q2-2026"
WSTSQ4 = "https://www.wsts.org/76/103/Global-Semiconductor-Market-grows-26-in-2025-to-796B"
SIA = "https://www.semiconductors.org/global-semiconductor-sales-increase-24-1-from-q2-2026-to-q3-2026/"
FR = "https://www.federalregister.gov/d/"


def r(key, value, unit, definition, source, url, fact, kind="official", note="", **kw):
    return Row(key, value, unit, definition, source, url, fact, C, kind, note=note, parts=P, **kw)


def tsm(key, value, unit, definition, fact="2025", **kw):
    return r(key, value, unit, definition, "Taiwan Semiconductor Manufacturing Co., Form 20-F 2025", TSM20F, fact, "filing", **kw)


def tq3(key, value, unit, definition, **kw):
    return r(key, value, unit, definition, "TSMC, Form 6-K of 15 October 2026 (third quarter 2026 results)", TSMQ3, "3Q 2026",
             "filing", **kw)


def asml(key, value, unit, definition, fact="2025", **kw):
    return r(key, value, unit, definition, "ASML Holding N.V., Form 20-F 2025", ASML, fact, "filing", **kw)


def wsts(key, value, unit, definition, fact, url=WSTS26, src="WSTS, Spring 2026 forecast (May 2026)", **kw):
    return r(key, value, unit, definition, f"World Semiconductor Trade Statistics, {src}", url, fact, "tracker", **kw)


def fr(key, value, unit, definition, cite, doc, fact):
    return r(key, value, unit, definition, f"Bureau of Industry and Security, {cite}", FR + doc, fact)


add(
    # Moore
    r("moore.1965.rate", 2, "x a year", "growth of 'the complexity for minimum component costs': 'roughly a factor of two "
      "per year'", "G. E. Moore, 'Cramming more components onto integrated circuits', Electronics 38 (8), 19 April 1965",
      MOORE65, "1965-04-19", "study"),
    r("moore.1965.target", 65000, "components", "'by 1975, the number of components per integrated circuit for minimum "
      "cost will be 65,000'", "G. E. Moore, Electronics, 19 April 1965", MOORE65, "forecast for 1975", "study"),
    r("moore.1975.years", 2, "years", "the revised slope: 'a doubling every two years, rather than every year, by the end "
      "of the decade'", "G. E. Moore, 'Progress in Digital Integrated Electronics', IEDM Technical Digest 1975, pp. 11-13",
      MOORE75, "1975", "study"),
    r("moore.1975.chip", 16384, "bits", "the device plotted for 1975: a 16,384-bit charge-coupled memory chip, at the "
      "complexity the annual doubling predicted", "G. E. Moore, IEDM 1975", MOORE75, "1975", "study"),
    r("moore.1961.line", 25, "micrometres", "line width of the first integrated circuits of 1961 ('1 mil (~25 "
      "micrometers)')", "G. E. Moore, IEDM 1975", MOORE75, "1961", "study"),
    r("moore.1975.line", 5, "micrometres", "line width of the 1975 device", "G. E. Moore, IEDM 1975", MOORE75, "1975", "study"),
    # TSMC
    tsm("tsm.founded", 1987, "year", "TSMC 'pioneered the pure-play foundry business model when it was founded in 1987'",
        fact="1987"),
    tsm("tsm.customers", 534, "customers", "customers served in 2025 (12,682 products, 305 process technologies)"),
    tsm("tsm.products", 12682, "products", "products manufactured in 2025"),
    tsm("tsm.capacity", 17, "million wafers", "annual capacity in 12-inch equivalent wafers ('exceeded 17 million')"),
    tsm("tsm.ship.2023", 12.002, "million wafers", "12-inch equivalent wafer shipments", fact="2023"),
    tsm("tsm.ship.2024", 12.910, "million wafers", "12-inch equivalent wafer shipments", fact="2024"),
    tsm("tsm.ship.2025", 15.022, "million wafers", "12-inch equivalent wafer shipments"),
    tsm("tsm.rev.2025.usd", 121.423, "$ billion", "net revenue (NT$3,809,054 million)"),
    tsm("tsm.rev.2025", 3809.054, "NT$ billion", "net revenue"),
    tsm("tsm.rev.2024", 2894.308, "NT$ billion", "net revenue", fact="2024"),
    tsm("tsm.rev.2023", 2161.736, "NT$ billion", "net revenue", fact="2023"),
    tsm("tsm.gm.2023", 54.4, "%", "gross margin", fact="2023"),
    tsm("tsm.gm.2024", 56.1, "%", "gross margin", fact="2024"),
    tsm("tsm.gm.2025", 59.9, "%", "gross margin"),
    tsm("tsm.ni.2025.usd", 54.116, "$ billion", "net income attributable to shareholders of the parent"),
    tsm("tsm.capex.2025.usd", 40.895, "$ billion", "capital expenditures (NT$1,272,411 million)"),
    tsm("tsm.capex.2026", 54, "$ billion", "capital expenditures expected in 2026", fact="2026 plan", lo=52, hi=56),
    tsm("tsm.top10", 78, "%", "share of net revenue from its ten largest customers (2023: 70%; 2024: 76%)"),
    tsm("tsm.top1", 19, "%", "share of net revenue from its largest customer (2023: 25%; 2024: 22%)"),
    tsm("tsm.top2", 17, "%", "share of net revenue from its second largest customer (2023: 11%; 2024: 12%)"),
    tsm("tsm.staff", 90557, "employees", "employees at 31 December 2025"),
    tsm("tsm.staff.2023", 76478, "employees", "employees at 31 December 2023", fact="2023"),
    tsm("tsm.staff.2024", 83825, "employees", "employees at 31 December 2024", fact="2024"),
    tsm("tsm.chips_grant", 6.6, "$ billion", "CHIPS Act direct funding the US Department of Commerce agreed to award TSMC "
        "Arizona (November 2024), with up to $5 billion of loans", fact="2024-11"),
    tsm("tsm.esmc_aid", 5, "€ billion", "state aid Germany agreed for ESMC, TSMC's Dresden subsidiary, under the European "
        "Chips Act (December 2024)", fact="2024-12"),
    r("tsm.us_invest", 165, "$ billion", "TSMC's expected total investment in the United States: $65 billion under way in "
      "Phoenix plus $100 billion for three more fabs, two advanced packaging facilities and an R&D centre",
      "TSMC, Form 6-K of 4 March 2025", TSMUS, "2025-03-04", "filing"),
    tq3("tsm.q3.rev", 46.72, "$ billion", "third quarter 2026 revenue (up 41.2% on a year earlier)"),
    tq3("tsm.q3.gm", 66.4, "%", "gross margin"),
    tq3("tsm.q3.om", 58.7, "%", "operating margin"),
    tq3("tsm.q3.n2", 8, "% of wafer revenue", "2-nanometer"),
    tq3("tsm.q3.n3", 33, "% of wafer revenue", "3-nanometer"),
    tq3("tsm.q3.n5", 28, "% of wafer revenue", "5-nanometer"),
    tq3("tsm.q3.n7", 10, "% of wafer revenue", "7-nanometer"),
    r("tsm.q3.hpc", 68, "% of revenue", "high-performance computing's share of revenue (smartphone 21%, IoT 4%, automotive "
      "4%, digital consumer electronics 1%, other 2%)", "TSMC, 3Q26 earnings conference presentation, slide 5", TSMQ3P,
      "3Q 2026", "filing"),
    r("tsm.q3.phone", 21, "% of revenue", "smartphones' share of revenue", "TSMC, 3Q26 earnings conference presentation, "
      "slide 5", TSMQ3P, "3Q 2026", "filing"),
    *[r(f"tsm.q3.{k}", v, "% of revenue", f"{name}'s share of revenue", "TSMC, 3Q26 earnings conference presentation, "
        "slide 5", TSMQ3P, "3Q 2026", "filing") for k, v, name in (("iot", 4, "the internet of things"), ("auto", 4, "automotive"),
                                                                    ("dce", 1, "digital consumer electronics"), ("other", 2, "other"))],
    *[tsm(f"tsm.plat.{k}.{y}", v, "% of revenue", f"{name}'s share of net revenue in {y} (20-F table of net revenue by "
          "platform)", fact=str(y))
      for k, name, vals in (("hpc", "high-performance computing", (43, 51, 58)), ("phone", "smartphones", (38, 35, 29)),
                            ("iot", "the internet of things", (8, 6, 5)), ("auto", "automotive", (6, 5, 5)),
                            ("dce", "digital consumer electronics", (2, 1, 1)), ("other", "other", (3, 2, 2)))
      for y, v in zip((2023, 2024, 2025), vals)],
    tsm("tsm.plat.hpc.twd.2023", 934.769, "NT$ billion", "net revenue from high-performance computing, 2023", fact="2023"),
    tsm("tsm.plat.hpc.twd.2025", 2192.931, "NT$ billion", "net revenue from high-performance computing, 2025 (up 48% on 2024)"),
    # ASML
    asml("asml.rev", 32.7, "€ billion", "total net sales (2024: €28.3 billion)"),
    asml("asml.gm", 52.8, "%", "gross margin"),
    asml("asml.ni", 9.6, "€ billion", "net income"),
    asml("asml.units", 327, "systems", "lithography systems sold (2024: 418; 2023: 449)"),
    asml("asml.euv", 48, "systems", "EUV systems recognized (2024: 44)"),
    asml("asml.only", 1, "maker", "'ASML is currently the world's only manufacturer of EUV lithography systems'"),
    # Intel
    r("intc.foundry.loss.2023", 7.1, "$ billion", "Intel Foundry segment operating loss", "Intel Corporation, Form 10-K 2025",
      INTC, "2023", "filing"),
    r("intc.foundry.loss.2024", 13.3, "$ billion", "Intel Foundry segment operating loss", "Intel Corporation, Form 10-K 2025",
      INTC, "2024", "filing"),
    r("intc.foundry.loss.2025", 10.3, "$ billion", "Intel Foundry segment operating loss", "Intel Corporation, Form 10-K 2025",
      INTC, "2025", "filing"),
    r("intc.foundry.ext", 0.307, "$ billion", "Intel Foundry's revenue from external customers (2024: $159 million)",
      "Intel Corporation, Form 10-K 2025", INTC, "2025", "filing"),
    r("intc.foundry.rev", 17.8, "$ billion", "Intel Foundry segment revenue, almost all from Intel's own products",
      "Intel Corporation, Form 10-K 2025", INTC, "2025", "filing"),
    r("intc.usg.shares", 275, "million shares", "Intel shares issued to the US Department of Commerce on 27 August 2025, "
      "with 159 million more in escrow and a warrant for 241 million", "Intel Corporation, Form 10-K 2025", INTC,
      "2025-08-27", "filing"),
    # Nvidia
    r("nvda.rev", 215.938, "$ billion", "revenue, fiscal year to 25 January 2026 (FY2025: $130.5 billion)",
      "NVIDIA Corporation, Form 10-K FY2026", NVDA, "FY2026", "filing"),
    r("nvda.dc", 193.737, "$ billion", "Data Center revenue, FY2026 (FY2025: $115.2 billion; FY2024: $47.5 billion)",
      "NVIDIA Corporation, Form 10-K FY2026", NVDA, "FY2026", "filing"),
    r("nvda.dc.2024", 47.525, "$ billion", "Data Center revenue, FY2024", "NVIDIA Corporation, Form 10-K FY2026", NVDA,
      "FY2024", "filing"),
    r("nvda.gm", 71.1, "%", "gross margin, FY2026 (FY2025: 75.0%)", "NVIDIA Corporation, Form 10-K FY2026", NVDA, "FY2026",
      "filing"),
    r("nvda.h20", 4.5, "$ billion", "charge in the first quarter of FY2026 for H20 inventory and purchase obligations after "
      "the US required a licence to export it to China", "NVIDIA Corporation, Form 10-K FY2026", NVDA, "2025-04", "filing"),
    # GM, the shortage
    r("gm.shortage", 2021, "year", "'The impact on production in 2021 due to the ongoing semiconductor supply shortage "
      "exceeded the impact of production suspensions in 2020 due to the COVID-19 pandemic'", "General Motors, Form 10-K 2021",
      GM, "2021", "filing"),
    # WSTS and SIA
    wsts("wsts.2022", 574.084, "$ billion", "world semiconductor sales", "2022", url=WSTS23, src="Fall 2023 forecast"),
    wsts("wsts.mem.2022", 129.767, "$ billion", "world memory sales", "2022", url=WSTS23, src="Fall 2023 forecast"),
    wsts("wsts.2024", 630.549, "$ billion", "world semiconductor sales", "2024", url=WSTS25, src="Autumn 2025 forecast"),
    wsts("wsts.mem.2024", 165.516, "$ billion", "world memory sales (+79.3% on 2023)", "2024", url=WSTS25, src="Autumn 2025 forecast"),
    wsts("wsts.2025", 795.640, "$ billion", "world semiconductor sales (+26.2%)", "2025"),
    wsts("wsts.mem.2025", 230.042, "$ billion", "world memory sales", "2025"),
    wsts("wsts.logic.2025", 299.547, "$ billion", "world logic sales", "2025"),
    wsts("wsts.analog.2025", 86.519, "$ billion", "world analog sales", "2025"),
    wsts("wsts.micro.2025", 84.867, "$ billion", "world microprocessor and microcontroller sales", "2025"),
    wsts("wsts.other.2025", 94.664, "$ billion", "discretes, optoelectronics and sensors", "2025"),
    wsts("wsts.2026f", 1511.248, "$ billion", "forecast world semiconductor sales, 2026 (+89.9%)", "2026 forecast (May 2026)"),
    wsts("wsts.mem.2026f", 803.941, "$ billion", "forecast memory sales, 2026 (+249.5%)", "2026 forecast (May 2026)"),
    wsts("wsts.2027f", 1913.683, "$ billion", "forecast world semiconductor sales, 2027", "2027 forecast (May 2026)"),
    wsts("wsts.am.2026f", 112.0, "%", "forecast growth of sales in the Americas, 2026", "2026 forecast (May 2026)"),
    wsts("wsts.aut.2026f", 975.460, "$ billion", "the Autumn 2025 forecast of 2026 world sales ('Global Semiconductor "
         "Market Approaches $1T in 2026')", "forecast made December 2025", url=WSTS25, src="Autumn 2025 forecast"),
    wsts("wsts.aut.mem.2026f", 294.821, "$ billion", "the Autumn 2025 forecast of 2026 memory sales", "forecast made December 2025",
         url=WSTS25, src="Autumn 2025 forecast"),
    wsts("wsts.h1.2026", 702, "$ billion", "world semiconductor sales in the first half of 2026 (+102% on a year earlier)",
         "2026 H1", url=WSTSQ2, src="Q2 2026 release"),
    wsts("wsts.q2calc.2026", 1655, "$ billion", "WSTS's recalculated 2026 total after the second quarter (+108%)",
         "2026 estimate (August 2026)", url=WSTSQ2, src="Q2 2026 release"),
    r("sia.q3.2026", 517.7, "$ billion", "world semiconductor sales in the third quarter of 2026 (+24.1% on the second)",
      "Semiconductor Industry Association, press release of 3 November 2026 (WSTS data)", SIA, "3Q 2026", "tracker"),
    r("sia.sep.2026", 172.6, "$ billion", "world semiconductor sales in September 2026 (three-month moving average, +146.8% on "
      "a year earlier)", "Semiconductor Industry Association, press release of 3 November 2026", SIA, "2026-09", "tracker"),
    wsts("wsts.q4.2025", 238.9, "$ billion", "world semiconductor sales in the fourth quarter of 2025 (+38.4% on a year "
         "earlier)", "4Q 2025", url=WSTSQ4, src="Q4 2025 release (6 March 2026)"),
    r("sia.q3.growth", 24.1, "%", "growth of world sales from the second to the third quarter of 2026; 'more than 20% "
      "quarter-to-quarter for the third consecutive quarter'", "Semiconductor Industry Association, press release of 3 "
      "November 2026 (WSTS data)", SIA, "3Q 2026", "tracker"),
    # export controls
    fr("bis.2022", 2022, "year", "controls on advanced computing chips, computers containing them and certain chipmaking "
       "equipment for China (87 FR 62186, effective 7 October 2022)", "87 FR 62186 (13 October 2022)", "2022-21658", "2022-10-07"),
    fr("bis.2025", 2025, "year", "Framework for Artificial Intelligence Diffusion (90 FR 4544)", "90 FR 4544 (15 January 2025)",
       "2025-00636", "2025-01-15"),
    fr("bis.2026h200", 2026, "year", "licence review for the Nvidia H200 and lesser chips to China and Macau changed from a "
       "presumption of denial to case by case (91 FR 1684)", "91 FR 1684 (15 January 2026)", "2026-00789", "2026-01-15"),
    fr("bis.2026remote", 2026, "year", "rules on overseas data centres supplying compute to companies headquartered in "
       "countries of concern; licences for advanced chips to Indonesia, Malaysia, Singapore, Thailand and Brazil; formal "
       "rescission of the AI Diffusion Rule, 'never enforced' (91 FR 74970)", "91 FR 74970 (19 November 2026)", "2026-23529", "2026-11-19"),
    fr("bis.2023", 2023, "year", "updated controls on advanced computing chips and the computers that use them (88 FR 73458)",
       "88 FR 73458 (25 October 2023)", "2023-23055", "2023-10-25"),
    fr("bis.2024", 2024, "year", "foreign-produced direct product rule additions and refinements to controls on advanced "
       "computing and chipmaking items (89 FR 96790)", "89 FR 96790 (5 December 2024)", "2024-28270", "2024-12-05"),
    r("nvda.memsup", 3, "suppliers", "'We purchase memory from SK Hynix Inc., Micron Technology, Inc., and Samsung'; wafers "
      "from foundries 'such as' TSMC and Samsung; CoWoS packaging; assembly, testing and packaging by Hon Hai, Wistron and "
      "Fabrinet; cost of revenue covers wafer fabrication, assembly, testing and packaging, boards, memory and components",
      "NVIDIA Corporation, Form 10-K FY2026", NVDA, "FY2026", "filing"),
    r("nvda.h20.lic", 2025, "year", "in August 2025 the US government granted licences to ship certain H20 chips to certain "
      "customers in China, after requiring a licence in April 2025", "NVIDIA Corporation, Form 10-K FY2026", NVDA, "2025-08",
      "filing"),
    *[wsts(f"wsts.reg.{k}.{y}", v, "$ billion", f"semiconductor sales to {name}", y if y == "2025" else "2026 forecast (May 2026)")
      for k, name, vals in (("am", "the Americas", (256.476, 543.654)), ("ap", "Asia Pacific", (439.747, 823.900)),
                            ("eu", "Europe", (54.694, 86.643)), ("jp", "Japan", (44.723, 57.050)))
      for y, v in zip(("2025", "2026f"), vals)],
    asml("asml.nm.iline", 365, "nm", "wavelength of i-line light (mercury vapour lamps)"),
    asml("asml.nm.krf", 248, "nm", "wavelength of krypton fluoride laser light"),
    asml("asml.nm.arf", 193, "nm", "wavelength of argon fluoride laser light (deep ultraviolet)"),
    asml("asml.nm.euv", 13.5, "nm", "wavelength of extreme ultraviolet (EUV) light"),
    asml("asml.res", 100, "x", "improvement in resolution 'for over 40 years ... by two orders of magnitude'"),
    tsm("tsm.tool_life", 5, "years", "useful life over which TSMC depreciates its machinery and equipment (buildings: "
        "10-20 years)"),
)
