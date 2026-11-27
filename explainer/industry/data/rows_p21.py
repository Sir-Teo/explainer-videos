"""Register rows for Part 21, *Medical Technology*.  Checked 2026-11-27.

The Forms 10-K 2025 of Intuitive Surgical, Abbott, Boston Scientific, Stryker, Quest Diagnostics, GE HealthCare and
Edwards Lifesciences, Medtronic's Form 10-K for fiscal 2026 and Abbott's for 2022; Intuitive's Form 10-Q for the third
quarter of 2026 and its results releases (Forms 8-K, Exhibit 99.1) of January 2025, January 2026 and October 2026.  Series
are the Filing Room's SEC, FRED and openFDA extracts.
"""

from explainer.industry.register import Row, add

C = "2026-11-27"
P = (21,)
SEC = "https://www.sec.gov/Archives/edgar/data/"
ISRG25 = SEC + "1035267/000103526726000010/isrg-20251231.htm"
ISRGQ3 = SEC + "1035267/000103526726000071/isrg-20260930.htm"
ISRG_G25 = SEC + "1035267/000103526725000008/q424ex-991earningsrelease.htm"
ISRG_G26 = SEC + "1035267/000103526726000006/q425ex-991earningsrelease.htm"
ISRG_Q3R = SEC + "1035267/000103526726000067/q326ex-991earningsrelease.htm"
MDT26 = SEC + "1613103/000162828026044354/mdt-20260424.htm"
ABT25 = SEC + "1800/000162828026010185/abt-20251231.htm"
ABT22 = SEC + "1800/000162828023004026/abt-20221231.htm"
BSX25 = SEC + "885725/000088572526000010/bsx-20251231.htm"
SYK25 = SEC + "310764/000031076426000010/syk-20251231.htm"
DGX25 = SEC + "1022079/000102207926000015/dgx-20251231.htm"
GEHC25 = SEC + "1932393/000193239326000007/gehc-20251231.htm"
EW25 = SEC + "1099800/000109980026000009/ew-20251231.htm"


def r(key, value, unit, definition, source, url, fact, kind="filing", note="", **kw):
    return Row(key, value, unit, definition, source, url, fact, C, kind, note=note, parts=P, **kw)


def isrg(key, value, unit, definition, fact="2025"):
    return r(key, value, unit, definition, "Intuitive Surgical, Inc., Form 10-K 2025", ISRG25, fact)


def isrg_q(key, value, unit, definition, fact="2026 Q3"):
    return r(key, value, unit, definition, "Intuitive Surgical, Inc., Form 8-K of 20 October 2026 (Exhibit 99.1) and Form "
             "10-Q for the third quarter of 2026", ISRG_Q3R, fact)


def mdt(key, value, unit, definition, fact="FY2026"):
    return r(key, value, unit, definition, "Medtronic plc, Form 10-K for the fiscal year ended 24 April 2026", MDT26, fact)


def bsx(key, value, unit, definition, fact="2025"):
    return r(key, value, unit, definition, "Boston Scientific Corporation, Form 10-K 2025", BSX25, fact)


def dgx(key, value, unit, definition, fact="2025"):
    return r(key, value, unit, definition, "Quest Diagnostics Incorporated, Form 10-K 2025", DGX25, fact)


def gehc(key, value, unit, definition, fact="2025"):
    return r(key, value, unit, definition, "GE HealthCare Technologies Inc., Form 10-K 2025", GEHC25, fact)


add(
    # Intuitive: the robot, its instruments and its installed base
    isrg("isrg.procs.2025", 3153000, "procedures", "'Approximately 3,153,000 da Vinci procedures were performed during the "
         "year ended December 31, 2025, an increase of 18%'"),
    isrg("isrg.procs.2024", 2683000, "procedures", "approximately 2,683,000 da Vinci procedures in 2024", "2024"),
    isrg("isrg.base.2025", 11106, "systems", "da Vinci installed base of approximately 11,106 systems at 31 December 2025 "
         "(6,364 in the US, 2,168 in Europe, 1,993 in Asia, 581 elsewhere)"),
    isrg("isrg.base.2024", 9902, "systems", "da Vinci installed base of approximately 9,902 systems at 31 December 2024", "2024"),
    isrg("isrg.ion.procs", 144100, "procedures", "'Approximately 144,100 Ion procedures were performed during the year ended "
         "December 31, 2025, an increase of 51%'"),
    isrg("isrg.base.us", 6364, "systems", "da Vinci systems installed in the US at 31 December 2025"),
    isrg("isrg.base.eu", 2168, "systems", "da Vinci systems installed in Europe at 31 December 2025"),
    isrg("isrg.base.asia", 1993, "systems", "da Vinci systems installed in Asia at 31 December 2025"),
    isrg("isrg.base.row", 581, "systems", "da Vinci systems installed in the rest of the world at 31 December 2025"),
    isrg("isrg.ia.growth", 19, "percent", "'Instruments and accessories revenue increased by 19% to $6.02 billion' in 2025"),
    isrg_q("isrg.q3.ia", 1.80, "US$ billion", "'Third quarter 2026 instruments and accessories revenue increased by 18% to $1.80 "
           "billion'"),
    isrg_q("isrg.q3.ia.growth", 18, "percent", "growth of instruments and accessories revenue, third quarter of 2026"),
    isrg("isrg.placed.2025", 1721, "systems", "da Vinci systems placed in 2025 (870 of them da Vinci 5); 1,526 in 2024"),
    isrg("isrg.util", 3, "percent", "'Utilization of da Vinci surgical systems, measured in terms of procedures per system per "
         "year, increased 3% relative to 2024'"),
    isrg("isrg.rev.2025", 10064.7, "US$ million", "total revenue, 2025 (2024: 8,352.1; 2023: 7,124.1)"),
    *[isrg(f"isrg.ia.{y}", v, "US$ million", f"instruments and accessories revenue, {y}", str(y))
      for y, v in ((2023, 4276.6), (2024, 5079.0), (2025, 6018.9))],
    *[isrg(f"isrg.sys.{y}", v, "US$ million", f"systems revenue, {y}", str(y))
      for y, v in ((2023, 1679.7), (2024, 1966.0), (2025, 2473.7))],
    *[isrg(f"isrg.svc.{y}", v, "US$ million", f"service revenue, {y}", str(y))
      for y, v in ((2023, 1167.8), (2024, 1307.1), (2025, 1572.1))],
    *[isrg(f"isrg.lease.{y}", v, "US$ million", f"operating lease revenue (within systems revenue), {y}", str(y))
      for y, v in ((2023, 500.5), (2024, 654.2), (2025, 874.3))],
    isrg("isrg.recurring", 84, "percent", "recurring revenue (instruments and accessories, service, operating leases) as a "
         "percentage of total revenue, 2025 (2024: 84%; 2023: 83%)"),
    isrg("isrg.price.lo", 0.7, "US$ million", "'The da Vinci surgical system generally sells for between $0.7 million and $3.1 "
         "million (generally inclusive of one year of service)'"),
    isrg("isrg.price.hi", 3.1, "US$ million", "upper end of the da Vinci system's selling price"),
    isrg("isrg.ia.lo", 900, "US$", "'We generally earn between $900 and $3,700 of instruments and accessories revenue per "
         "surgical procedure performed'"),
    isrg("isrg.ia.hi", 3700, "US$", "upper end of instruments and accessories revenue per procedure"),
    isrg("isrg.svc.lo", 95000, "US$ a year", "service contracts 'at an annual fee between $95,000 and $225,000'"),
    isrg("isrg.svc.hi", 225000, "US$ a year", "upper end of the annual service fee"),
    isrg("isrg.leased", 3210, "systems", "da Vinci installed base under operating leases at 31 December 2025 (1,400 "
         "fixed-payment, 1,810 usage-based; 2023: 2,227 of which 1,023 usage-based)"),
    isrg("isrg.usage", 1810, "systems", "da Vinci installed base under usage-based operating leases, 31 December 2025"),
    isrg("isrg.usage.2023", 1023, "systems", "da Vinci installed base under usage-based operating leases, 31 December 2023",
         "2023"),
    isrg("isrg.gm", 66.0, "percent", "'Gross profit as a percentage of revenue was 66.0%' in 2025"),
    isrg("isrg.quota", 559, "robots", "China's 2023 quota for major medical equipment 'will allow for the sale of 559 new "
         "surgical robots into China'", "2023"),
    isrg("isrg.benign", 50, "percent", "'More than half of da Vinci procedures performed are for benign conditions'; US benign "
         "volumes are 'typically seasonally higher in the fourth quarter when more patients have met annual deductibles'"),
    isrg_q("isrg.q3.procs", 906000, "procedures", "'Approximately 906,000 da Vinci procedures were performed during the three "
           "months ended September 30, 2026, a growth of 14%'"),
    isrg("isrg.growth.2025", 18, "percent", "da Vinci procedures 'increased by 18%' in 2025 ('Worldwide da Vinci procedure "
         "growth was 17% in 2024')"),
    isrg_q("isrg.q3.growth", 14, "percent", "third-quarter 2026 da Vinci procedure growth, 'approximately 14%' (US 10%, "
           "outside the US 20%)"),
    isrg_q("isrg.guide2026.oct.hi", 15, "percent", "upper end of the October 2026 procedure growth guidance", "2026 (forecast)"),
    isrg_q("isrg.9m.growth", 15, "percent", "da Vinci procedures 'grew approximately 15% for the nine months ended September "
           "30, 2026'"),
    isrg_q("isrg.base.q3", 12094, "systems", "da Vinci installed base of 12,094 systems at 30 September 2026, up 12%"),
    isrg_q("isrg.settle", 450, "US$ million", "'a pre-tax charge of $450 million in connection with the settlement of "
           "previously disclosed antitrust class action litigation' (complaints by hospitals 'relating to the service and "
           "repair of certain instruments')"),
    r("isrg.guide2025.lo", 13, "percent", "23 January 2025: 'The Company expects worldwide da Vinci procedures to increase "
      "approximately 13% to 16% in 2025'", "Intuitive Surgical, Inc., Form 8-K of 23 January 2025 (Exhibit 99.1)", ISRG_G25,
      "2025 (forecast)"),
    r("isrg.guide2025.hi", 16, "percent", "upper end of the 2025 procedure growth guidance",
      "Intuitive Surgical, Inc., Form 8-K of 23 January 2025 (Exhibit 99.1)", ISRG_G25, "2025 (forecast)"),
    r("isrg.guide2026.lo", 13, "percent", "22 January 2026: 'Worldwide da Vinci procedure growth of approximately 13% to 15% "
      "in 2026, compared to 18% in 2025'", "Intuitive Surgical, Inc., Form 8-K of 22 January 2026 (Exhibit 99.1)", ISRG_G26,
      "2026 (forecast)"),
    r("isrg.guide2026.hi", 15, "percent", "upper end of the January 2026 procedure growth guidance",
      "Intuitive Surgical, Inc., Form 8-K of 22 January 2026 (Exhibit 99.1)", ISRG_G26, "2026 (forecast)"),
    isrg_q("isrg.guide2026.oct", 14, "percent", "20 October 2026: 'Worldwide da Vinci procedure growth of approximately 14% to "
           "15% in 2026. The Company expects to be closer to the midpoint of this range.'", "2026 (forecast)"),

    # openFDA: one year's Class I recalls by event
    r("fda21.c1.events.2023", 80, "recall events", "Class I device recall enforcement reports dated 2023, counted by recall "
      "event: 80 events covering 495 products; the largest named 123 products", "US Food and Drug Administration via openFDA, "
      "device enforcement reports", "https://api.fda.gov/device/enforcement.json?search=classification:%22Class+I%22+AND+"
      "report_date:[20230101+TO+20231231]&count=event_id", "2023", "official"),
    r("fda21.c1.max.2023", 123, "products", "products named in the largest Class I device recall event reported in 2023",
      "US Food and Drug Administration via openFDA, device enforcement reports", "https://api.fda.gov/device/enforcement.json?"
      "search=classification:%22Class+I%22+AND+report_date:[20230101+TO+20231231]&count=event_id", "2023", "official"),

    # Medtronic
    mdt("mdt.rev", 36364, "US$ million", "net sales, fiscal 2026 (fiscal 2025: 33,537)"),
    mdt("mdt.cv", 13976, "US$ million", "Cardiovascular net sales, fiscal 2026 (12% growth)"),
    mdt("mdt.neuro", 10287, "US$ million", "Neuroscience net sales, fiscal 2026"),
    mdt("mdt.medsurg", 8815, "US$ million", "Medical Surgical net sales, fiscal 2026"),
    mdt("mdt.diab", 3112, "US$ million", "Diabetes net sales, fiscal 2026 (to be separated as MiniMed)"),
    mdt("mdt.founded", 1949, "year", "'Medtronic was founded in 1949'"),
    mdt("mdt.crhf", 17, "percent", "Cardiac Rhythm & Heart Failure net sales growth in fiscal 2026, with 'strong growth in "
        "the pulsed ablation portfolio'"),

    # Boston Scientific: pulsed field ablation
    *[bsx(f"bsx.ep.{y}", v, "US$ million", f"Electrophysiology net sales, {y}", str(y))
      for y, v in ((2023, 800), (2024, 1904), (2025, 3325))],
    *[bsx(f"bsx.watchman.{y}", v, "US$ million", f"Watchman net sales, {y}", str(y))
      for y, v in ((2023, 1274), (2024, 1516), (2025, 1958))],
    bsx("bsx.impair", 386, "US$ million", "intangible asset impairment charges in 2024, 'primarily associated with' Cryterion "
        "and Devoro, cryoablation impaired 'due to strong commercial adoption of our Farapulse PFA System'", "2024"),

    # Abbott: the testing boom
    *[r(f"abt.covid.{y}", v, "US$ billion", f"Abbott's COVID-19 testing-related sales, {y}", "Abbott Laboratories, Form 10-K "
        "2022", ABT22, str(y)) for y, v in ((2020, 3.9), (2021, 7.7), (2022, 8.4))],
    *[r(f"abt.covid.{y}", v, "US$ billion", f"Abbott's COVID-19 testing-related sales, {y}", "Abbott Laboratories, Form 10-K "
        "2025", ABT25, str(y)) for y, v in ((2023, 1.6), (2024, 0.747), (2025, 0.297))],

    # GE HealthCare: products and services
    gehc("gehc.products", 13661, "US$ million", "sales of products, 2025 (cost of products 8,942)"),
    gehc("gehc.services", 6964, "US$ million", "sales of services, 2025 (cost of services 3,436)"),
    gehc("gehc.cost.products", 8942, "US$ million", "cost of products, 2025"),
    gehc("gehc.cost.services", 3436, "US$ million", "cost of services, 2025"),

    # Quest: the laboratory
    dgx("dgx.reqs", 244, "million requisitions", "'Processed approximately 244 million test requisitions in 2025'"),
    *[dgx(f"dgx.rpr.{y}", v, "percent", f"revenue per requisition change, {y}", str(y))
      for y, v in ((2023, -5.9), (2024, 1.3), (2025, 0.1))],
    *[dgx(f"dgx.vol.{y}", v, "percent", f"requisition volume change, {y}", str(y))
      for y, v in ((2023, -0.6), (2024, 5.5), (2025, 12.3))],
    *[dgx(f"dgx.org.{y}", v, "percent", f"organic requisition volume change, {y}", str(y))
      for y, v in ((2023, -1.0), (2024, 0.7), (2025, 3.4))],
    dgx("dgx.acq", 6.7, "percent", "'recent acquisitions contributed approximately 6.7% to DIS revenues' in 2025"),
    dgx("dgx.dis", 10785, "US$ million", "diagnostic information services revenues, 2025"),
    *[dgx(f"dgx.mix.{k}.{m}", v, "percent", f"{name}: share of DIS requisition volume" if m == "vol" else
          f"{name}: share of consolidated net revenues")
      for k, name, vol, rev in (("ins", "healthcare insurers", 43, 39), ("gov", "government payers", 17, 16),
                                ("client", "client payers", 37, 31), ("pat", "patients", 1, 12))
      for m, v in (("vol", vol), ("rev", rev))],

    # Edwards and Stryker
    *[r(f"ew.tavr.{y}", v, "US$ million", f"transcatheter aortic valve replacement net sales, {y}", "Edwards Lifesciences "
        "Corporation, Form 10-K 2025", EW25, str(y)) for y, v in ((2023, 3879.8), (2024, 4106.1), (2025, 4487.7))],
    r("syk.mako", 2, "million procedures", "'more than two million robotic procedures across Mako Total Knee, Mako Total Hip, "
      "and Mako Partial Knee' (over one million Mako Total Knee procedures)", "Stryker Corporation, Form 10-K 2025", SYK25,
      "2025"),
)
