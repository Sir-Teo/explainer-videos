"""Register rows for Part 16, *Electronics*.  Checked 2026-11-27.

Stan Shih's oral history at the Computer History Museum (2011); Hon Hai Precision Industry's audited 2025 statements and
its board-approved results, filed through the London Stock Exchange; the Forms 10-K of Apple (FY2026), Intel (2025), HP
(FY2025), Dell (FY2026), Jabil (FY2026) and Flex (FY2026); the Office of the US Trade Representative's Section 301
notices in the Federal Register, 2018-2019; and CBS News' transcript of the Commerce Secretary on *Face the Nation*, 6
April 2025.  Series are the Filing Room's SEC, UN Comtrade, BLS and FRED extracts.
"""

from explainer.industry.register import Row, add

C = "2026-11-27"
P = (16,)
SHIH = "https://archive.computerhistory.org/resources/access/text/2012/02/102746001-05-01-acc.pdf"
HH_FS = "http://www.rns-pdf.londonstockexchange.com/rns/9664O_1-2026-8-3.pdf"
HH_BOD = ("https://www.investegate.co.uk/announcement/rns/hon-hai-precision-industry-co-ltd--hhpd/"
          "2025-financial-report-has-been-approved-by-the-bod/9476191")
AAPL = "https://www.sec.gov/Archives/edgar/data/320193/000032019326000026/aapl-20260926.htm"
INTC = "https://www.sec.gov/Archives/edgar/data/50863/000005086326000011/intc-20251227.htm"
HPQ = "https://www.sec.gov/Archives/edgar/data/47217/000004721725000071/hpq-20251031.htm"
DELL = "https://www.sec.gov/Archives/edgar/data/1571996/000157199626000008/dell-20260130.htm"
JBL = "https://www.sec.gov/Archives/edgar/data/898293/000162828026067038/jbl-20260831.htm"
FLEX = "https://www.sec.gov/Archives/edgar/data/866374/000086637426000012/flex-20260331.htm"
CBS = ("https://www.cbsnews.com/news/transcript-commerce-secretary-howard-lutnick-on-face-the-nation-with-margaret-"
       "brennan-april-6-2025/")
FR = "https://www.federalregister.gov/d/"


def r(key, value, unit, definition, source, url, fact, kind="official", note="", **kw):
    return Row(key, value, unit, definition, source, url, fact, C, kind, note=note, parts=P, **kw)


def hh(key, value, unit, definition, fact="2025", **kw):
    return r(key, value, unit, definition, "Hon Hai Precision Industry Co., consolidated financial statements for 2025 "
             "(audited; filed via RNS, London Stock Exchange, 3 August 2026)", HH_FS, fact, "filing", **kw)


def k10(key, value, unit, definition, who, url, fact, **kw):
    return r(key, value, unit, definition, f"{who}, Form 10-K", url, fact, "filing", **kw)


def fr(key, value, unit, definition, cite, doc, fact):
    return r(key, value, unit, definition, f"Office of the US Trade Representative, {cite}", FR + doc, fact)


add(
    # the smile
    r("shih.year", 1992, "year", "the year Stan Shih analysed 'the value-add imparted by each segment of the entire "
      "industry' for Acer and drew the curve 'smile-shaped': 'The curve showed manufacturing is the lowest in terms of "
      "value'", "Computer History Museum, oral history of Stan (Chen-Jung) Shih, recorded 21 March 2011 (CHM X6261.2012), "
      "p. 31", SHIH, "1992", "study"),
    # Hon Hai
    hh("hh.rev", 8103.104763, "NT$ billion", "operating revenue, 2025"),
    hh("hh.rev.2024", 6859.615493, "NT$ billion", "operating revenue, 2024", fact="2024"),
    hh("hh.gp", 498.161036, "NT$ billion", "gross profit, 2025 (2024: 428.9)"),
    hh("hh.op", 259.222960, "NT$ billion", "operating profit, 2025 (2024: 200.6)"),
    hh("hh.op.2024", 200.607227, "NT$ billion", "operating profit, 2024", fact="2024"),
    hh("hh.ni", 189.353852, "NT$ billion", "profit attributable to owners of the parent, 2025 (2024: 152.7)"),
    hh("hh.rd", 121.705158, "NT$ billion", "research and development expenses, 2025"),
    hh("hh.assets", 5104.672223, "NT$ billion", "total assets, end of 2025"),
    hh("hh.inventory", 1095.574319, "NT$ billion", "inventories, end of 2025 (2024: 835.0)"),
    hh("hh.ppe", 543.392999, "NT$ billion", "property, plant and equipment, end of 2025"),
    hh("hh.equity", 1970.763355, "NT$ billion", "total equity, end of 2025"),
    *[hh(f"hh.prod.{k}", v, "NT$ billion", f"revenue from {name}, 2025 (2024: {v24:,.1f})")
      for k, name, v, v24 in (("sce", "smart consumer electronics (smartphones, TVs, game consoles)", 3081.686, 3169.936),
                              ("cloud", "cloud and networking products (servers, communication network)", 3255.827, 2001.817),
                              ("computing", "computing products (computers, tablets)", 1228.391, 1262.891),
                              ("components", "components and others (connectors, mechanical parts, services)", 537.201, 424.971))],
    hh("hh.prod.sce.2024", 3169.936, "NT$ billion", "revenue from smart consumer electronics, 2024", fact="2024"),
    hh("hh.prod.cloud.2024", 2001.817, "NT$ billion", "revenue from cloud and networking products, 2024", fact="2024"),
    hh("hh.ni.2024", 152.705066, "NT$ billion", "profit attributable to owners of the parent, 2024", fact="2024"),
    hh("hh.prod.computing.2024", 1262.891, "NT$ billion", "revenue from computing products, 2024", fact="2024"),
    hh("hh.prod.components.2024", 424.971, "NT$ billion", "revenue from components and others, 2024", fact="2024"),
    hh("hh.client_e", 3574.256, "NT$ billion", "revenue from its largest customer, 'Client E', 2025 (2024: 3,706.5)"),
    hh("hh.client_e.2024", 3706.464, "NT$ billion", "revenue from 'Client E', 2024", fact="2024"),
    hh("hh.fii.op", 184.293, "NT$ billion", "operating income of the FII subgroup (Foxconn Industrial Internet: servers and "
       "networking), 2025, on operating revenue of NT$3,908.1bn"),
    hh("hh.fii.rev", 3908.053, "NT$ billion", "operating revenue of the FII subgroup, 2025"),
    hh("hh.parent.op", 62.167, "NT$ billion", "segment operating income of the Hon Hai parent group (all but the listed "
       "subgroups), 2025 (2024: 73.1)"),
    hh("hh.parent.rev", 4340.740, "NT$ billion", "operating revenue of the Hon Hai parent group, 2025"),
    *[hh(f"hh.nca.{k}", v, "NT$ billion", f"non-current assets in {name}, end of 2025 (2024: {v24:,.1f})")
      for k, name, v, v24 in (("cn", "China", 281.423953, 294.957221), ("vn", "Vietnam", 97.966307, 66.047497),
                              ("us", "the USA", 76.931176, 55.239958), ("in", "India", 75.968853, 64.600070),
                              ("tw", "Taiwan", 53.649845, 44.633146), ("mx", "Mexico", 52.755459, 39.737545),
                              ("other", "Japan and other countries", 39.007313, 31.901721))],
    *[hh(f"hh.nca.{k}.2024", v, "NT$ billion", f"non-current assets in {name}, end of 2024", fact="2024")
      for k, name, v in (("cn", "China", 294.957221), ("vn", "Vietnam", 66.047497), ("us", "the USA", 55.239958),
                         ("in", "India", 64.600070), ("tw", "Taiwan", 44.633146), ("mx", "Mexico", 39.737545),
                         ("other", "Japan and other countries", 31.901721))],
    *[hh(f"hh.loc.{k}", v, "NT$ billion", f"revenue from customers registered in {name}, 2025 (by the customer's registered "
         "location)") for k, name, v in (("us", "the USA", 3643.566946), ("sg", "Singapore", 1800.080194),
                                           ("ie", "Ireland", 895.059041), ("cn", "China", 370.179531), ("tw", "Taiwan", 201.014630),
                                           ("jp", "Japan", 161.897484), ("in", "India", 147.082536),
                                           ("other", "Vietnam, Mexico and other countries", 884.224400))],
    # the brands and the PC
    k10("aapl.gm.products", 39.3, "%", "products gross margin, FY2026 (FY2025: 36.8%; FY2024: 37.2%)", "Apple Inc.", AAPL, "FY2026"),
    k10("aapl.gm.services", 76.2, "%", "services gross margin, FY2026 (FY2025: 75.4%)", "Apple Inc.", AAPL, "FY2026"),
    *[k10(f"aapl.gm.{k}.{y}", v, "%", f"{name} gross margin, fiscal {y}", "Apple Inc.", AAPL, f"FY{y}")
      for k, name, y, v in (("products", "products", 2025, 36.8), ("products", "products", 2024, 37.2),
                            ("services", "services", 2025, 75.4), ("services", "services", 2024, 73.9))],
    k10("aapl.gp.products", 139.659, "$ billion", "products gross margin in dollars, FY2026", "Apple Inc.", AAPL, "FY2026"),
    k10("aapl.gp.services", 93.943, "$ billion", "services gross margin in dollars, FY2026", "Apple Inc.", AAPL, "FY2026"),
    k10("aapl.staff", 167000, "full-time equivalent employees", "employees at 26 September 2026; 'Substantially all of the "
        "Company's hardware products are manufactured by outsourcing partners that are located primarily in China "
        "mainland, India, Japan, South Korea, Taiwan and Vietnam'", "Apple Inc.", AAPL, "2026-09-26"),
    k10("aapl.tariffs2025", 2025, "year", "'Beginning in the second quarter of 2025, new tariffs were announced on imports to "
        "the U.S., including additional tariffs on imports from China mainland, India, Japan, South Korea, Taiwan, Vietnam "
        "and the European Union'", "Apple Inc.", AAPL, "2025"),
    k10("aapl.s232", 2026, "year", "'On January 14, 2026, initial results were published' of the Section 232 investigation into "
        "semiconductors and their derivative products; they 'did not impose any additional tariffs affecting the Company's "
        "products'", "Apple Inc.", AAPL, "2026-01-14"),
    k10("aapl.scotus", 2026, "year", "'on February 20, 2026, the Supreme Court issued a ruling striking down certain "
        "tariffs previously imposed under the International Emergency Economic Powers Act'; Apple applied for refunds and "
        "booked them against products cost of sales", "Apple Inc.", AAPL, "2026-02-20"),
    *[k10(f"intc.ccg.{y}", v, "$ billion", f"Client Computing Group (PC processors) {what}, {y}", "Intel Corporation", INTC, str(y))
      for y, what, v in ((2025, "revenue", 32.228), (2024, "revenue", 33.346), (2023, "revenue", 32.305))],
    *[k10(f"intc.ccg.op.{y}", v, "$ billion", f"Client Computing Group operating income, {y} (margin {m}%)", "Intel Corporation",
          INTC, str(y)) for y, v, m in ((2025, 9.317, 29), (2024, 11.594, 35), (2023, 10.128, 31))],
    *[k10(f"hpq.ps.{y}", v, "$ billion", f"Personal Systems net revenue, fiscal {y}", "HP Inc.", HPQ, f"FY{y}")
      for y, v in ((2025, 38.532), (2024, 36.195), (2023, 35.684))],
    *[k10(f"hpq.ps.op.{y}", v, "$ billion", f"Personal Systems earnings from operations, fiscal {y} ({m}% of revenue)",
          "HP Inc.", HPQ, f"FY{y}") for y, v, m in ((2025, 2.054, 5.3), (2024, 2.253, 6.2), (2023, 2.129, 6.0))],
    k10("hpq.print", 16.702, "$ billion", "Printing net revenue, fiscal 2025 (earnings from operations $3.118bn, 18.7%)",
        "HP Inc.", HPQ, "FY2025"),
    k10("hpq.supplies", 10.916, "$ billion", "Printing: supplies (ink and toner) net revenue, fiscal 2025 (commercial printing "
        "$4.633bn, consumer printing $1.153bn)", "HP Inc.", HPQ, "FY2025"),
    k10("hpq.print.op", 3.118, "$ billion", "Printing earnings from operations, fiscal 2025", "HP Inc.", HPQ, "FY2025"),
    *[k10(f"dell.csg.{y}", v, "$ billion", f"Client Solutions Group (PCs) net revenue, fiscal {y}", "Dell Technologies",
          DELL, f"FY{y}") for y, v in ((2026, 50.984), (2025, 48.393), (2024, 48.916))],
    *[k10(f"dell.csg.op.{y}", v, "$ billion", f"Client Solutions Group operating income, fiscal {y} ({m}% of revenue)",
          "Dell Technologies", DELL, f"FY{y}") for y, v, m in ((2026, 2.833, 5.6), (2025, 2.972, 6.1), (2024, 3.712, 7.6))],
    *[k10(f"dell.ai.{y}", v, "$ billion", f"AI-optimized servers net revenue, fiscal {y}", "Dell Technologies", DELL, f"FY{y}")
      for y, v in ((2026, 24.683), (2025, 9.286), (2024, 1.873))],
    k10("dell.isg.2026", 60.826, "$ billion", "Infrastructure Solutions Group (servers, networking, storage) net revenue, fiscal "
        "2026 (fiscal 2025: 43.593)", "Dell Technologies", DELL, "FY2026"),
    k10("dell.isg.op.2026", 7.111, "$ billion", "Infrastructure Solutions Group operating income, fiscal 2026 (11.7% of revenue; "
        "fiscal 2025: 5.579, 12.8%)", "Dell Technologies", DELL, "FY2026"),
    # the assemblers
    k10("jbl.custa", 20, "% of net revenue", "Jabil's largest customer ('Customer A'), fiscal 2026 (fiscal 2025: 16%); five "
        "largest customers about 37%", "Jabil Inc.", JBL, "FY2026"),
    k10("flex.staff", 149686, "employees", "Flex's workforce at 31 March 2026 (Americas 61,841; Asia 60,870; Europe 26,975), "
        "in more than 100 facilities across about 30 countries", "Flex Ltd.", FLEX, "2026-03-31"),
    *[k10(f"flex.staff.{k}", v, "employees", f"Flex's workforce in {name} at 31 March 2026", "Flex Ltd.", FLEX, "2026-03-31")
      for k, name, v in (("am", "the Americas", 61841), ("asia", "Asia", 60870), ("eu", "Europe", 26975))],
    k10("flex.china", 16, "% of net sales", "share of Flex's net sales made in China, fiscal 2026 (North America 44%, "
        "Europe 20%, other 20%)", "Flex Ltd.", FLEX, "FY2026"),
    # tariffs
    fr("ustr.2018", 25, "%", "additional duty on the first list of Chinese products under Section 301 (83 FR 28710)",
       "83 FR 28710 (20 June 2018)", "2018-13248", "2018-06-20"),
    fr("ustr.2019.share", 75, "% of US imports", "the second part of the 2019 list, delayed to 15 December 2019, was the "
       "products where 'China's share of U.S. imports from the world is 75 percent or greater' (84 FR 43304)",
       "84 FR 43304 (20 August 2019)", "2019-17865", "2019-08-20"),
    fr("ustr.2019.rate", 15, "%", "the 2019 list's additional duty, raised from 10% (84 FR 45821)",
       "84 FR 45821 (30 August 2019)", "2019-18838", "2019-08-30"),
    fr("ustr.2019.suspend", 2019, "year", "the duty due on 15 December 2019 suspended 'until further notice' (84 FR 69447)",
       "84 FR 69447 (18 December 2019)", "2019-27306", "2019-12-18"),
    # called it
    r("lutnick.2025", 2025, "year", "'the army of millions and millions of human beings screwing in little- little screws "
      "to make iPhones, that kind of thing is going to come to America. It's going to be automated'", "CBS News, transcript "
      "of Commerce Secretary Howard Lutnick on Face the Nation with Margaret Brennan, 6 April 2025", CBS, "2025-04-06",
      "press", note="the Commerce Secretary's own words, as transcribed by CBS News; a forecast, not a figure"),
)
