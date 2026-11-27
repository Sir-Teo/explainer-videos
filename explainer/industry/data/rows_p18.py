"""Register rows for Part 18, *Aerospace and Defence*.  Checked 2026-11-27.

The Forms 10-K of Boeing (2025, 2013, 2011, 2005), GE Aerospace, RTX, Lockheed Martin and TransDigm, and the 20-F of
AerCap; Airbus SE's 2025 annual report in its ESEF filing; the WTO's summaries of disputes DS316 and DS353.  Series are
the Filing Room's SEC, FRED and SIPRI extracts.
"""

from explainer.industry.register import Row, add

C = "2026-11-27"
P = (18,)
SEC = "https://www.sec.gov/Archives/edgar/data/"
BA25 = SEC + "12927/000162828026004357/ba-20251231.htm"
BA13 = SEC + "12927/000001292714000004/a201312dec3110k.htm"
BA11 = SEC + "12927/000119312512048565/d255574d10k.htm"
BA05 = SEC + "12927/000119312506040952/d10k.htm"
BAQ3 = SEC + "12927/000162828026067508/ba-20260930.htm"
GE25 = SEC + "40545/000004054526000008/ge-20251231.htm"
RTX25 = SEC + "101829/000010182926000006/rtx-20251231.htm"
LMT25 = SEC + "936468/000162828026004195/lmt-20251231.htm"
TDG26 = SEC + "1260221/000126022126000077/tdg-20260930.htm"
AER25 = SEC + "1378789/000162828026007513/aer-20251231.htm"
AB25 = ("https://filings.xbrl.org/MINO79WLOO247M1IL051/2025-12-31/ESEF/NL/0/MINO79WLOO247M1IL051-2025-12-31-1-en/"
        "reports/MINO79WLOO247M1IL051-2025-12-31-1-en.xhtml")
WTO = "https://www.wto.org/english/tratop_e/dispu_e/cases_e/"


def r(key, value, unit, definition, source, url, fact, kind="filing", note="", **kw):
    return Row(key, value, unit, definition, source, url, fact, C, kind, note=note, parts=P, **kw)


def ba(key, value, unit, definition, fact="2025", url=BA25, form="10-K 2025"):
    return r(key, value, unit, definition, f"The Boeing Company, Form {form}", url, fact)


def bq(key, value, unit, definition, fact="2026-09-30"):
    return r(key, value, unit, definition, "The Boeing Company, Form 10-Q for the third quarter of 2026", BAQ3, fact)


def ab(key, value, unit, definition, fact="2025"):
    return r(key, value, unit, definition, "Airbus SE, Annual Report 2025 (ESEF filing, via filings.xbrl.org)", AB25, fact)


def ge(key, value, unit, definition, fact="2025"):
    return r(key, value, unit, definition, "General Electric Company (GE Aerospace), Form 10-K 2025", GE25, fact)


add(
    # Boeing
    ba("ba.deliv", 600, "airplanes", "commercial deliveries, including intercompany: 737 447, 767 30, 777 35, 787 88"),
    ba("ba.deliv.2024", 348, "airplanes", "commercial deliveries, 2024", fact="2024"),
    ba("ba.deliv.2023", 528, "airplanes", "commercial deliveries, 2023", fact="2023"),
    ba("ba.deliv.737", 447, "airplanes", "737 deliveries"),
    ba("ba.deliv.787", 88, "airplanes", "787 deliveries"),
    ba("ba.deliv.777", 35, "airplanes", "777 deliveries"),
    ba("ba.deliv.767", 30, "airplanes", "767 deliveries"),
    ba("ba.cum.737", 9240, "airplanes", "cumulative 737 deliveries"),
    ba("ba.cum.747", 1573, "airplanes", "cumulative 747 deliveries; 'delivery of the last aircraft occurred in February "
       "2023'"),
    ba("ba.bca.op", -7079, "US$ million", "Commercial Airplanes: loss from operations (margin -17.1%)"),
    ba("ba.bca.op.2024", -7969, "US$ million", "Commercial Airplanes: loss from operations, 2024 (margin -34.9%)", fact="2024"),
    ba("ba.bca.op.2023", -1635, "US$ million", "Commercial Airplanes: loss from operations, 2023 (margin -4.8%)", fact="2023"),
    ba("ba.bca.rnd", 2202, "US$ million", "Commercial Airplanes: research and development"),
    ba("ba.aq.737", 12400, "airplanes", "program accounting quantity: 737"),
    ba("ba.aq.787", 1900, "airplanes", "program accounting quantity: 787"),
    ba("ba.aq.777x", 650, "airplanes", "program accounting quantity: 777X (raised by 150 in 2025)"),
    ba("ba.aq.777", 1828, "airplanes", "program accounting quantity: 777"),
    ba("ba.undel.737", 4404, "airplanes", "undelivered 737s under firm orders"),
    ba("ba.undel.787", 1026, "airplanes", "undelivered 787s under firm orders"),
    ba("ba.undel.767", 94, "airplanes", "undelivered 767s under firm orders"),
    ba("ba.undel.777", 46, "airplanes", "undelivered 777s under firm orders"),
    ba("ba.undel.777x", 560, "airplanes", "undelivered 777Xs under firm orders (cumulative firm orders 560)"),
    ba("ba.backlog.bca", 567290, "US$ million", "Commercial Airplanes backlog"),
    ba("ba.backlog", 682207, "US$ million", "total backlog"),
    ba("ba.rate.737", 42, "airplanes a month", "737 production rate in the fourth quarter of 2025, from below 38 at the "
       "start of the year; 'plans to increase the production rate from 42 to 47 in 2026'"),
    ba("ba.rf.777x767.2024", 4079, "US$ million", "reach-forward losses on the 777X and 767 programs, 2024", fact="2024"),
    ba("ba.777x.first", 2027, "year", "'we ... delayed first delivery of the 777-9 to 2027'"),
    ba("ba.787.target", 2008, "year", "'In early 2004, we received the initial launch order for the 787 ... Entry into "
       "service is targeted for 2008.'", fact="2005", url=BA05, form="10-K 2005"),
    ba("ba.787.first", 2011, "year", "'We delivered the first 787-8 airplane in September 2011'", fact="2011", url=BA11,
       form="10-K 2011"),
    ba("ba.rf.777x.2025", 4.9, "US$ billion", "additional reach-forward losses on the 777X, 2025 ($3.5bn in 2024); 'the 777X "
       "program, which launched in 2013 and is currently expecting first delivery in 2027'"),
    ba("ba.rf.777x.2024", 3.5, "US$ billion", "additional reach-forward losses on the 777X, 2024", fact="2024"),
    ba("ba.spirit", 8371, "US$ million", "total consideration for Spirit AeroSystems, acquired 8 December 2025 ($4.7bn in "
       "Boeing shares): 'fuselages for the 737, P-8 and KC-46 Tanker programs, as well as major structures for the 767, 777 "
       "and 787'; Spirit employs about 15,000 people"),
    ba("ba.strike.2024", 53, "days", "IAM District 751, 'over 30,000 Boeing manufacturing employees primarily located in "
       "Washington state, went out on strike for 53 days' in 2024, 'halting production of most of our commercial aircraft'",
       fact="2024"),
    ba("ba.bds.fpd", 5.0, "US$ billion", "additional losses at Boeing Defense, Space & Security on 'its five most significant "
       "fixed-price development programs (KC-46A Tanker, T-7A Red Hawk, Commercial Crew, VC-25B Presidential Aircraft, and "
       "MQ-25)', 2024", fact="2024"),
    ba("ba.sole", 1, "flag", "'Many major components and product equipment items are procured or subcontracted on a "
       "sole-source basis'; for aluminium, titanium and composites, 'qualification of the sources could take a year or more'"),
    ba("ba.777x.target", 2020, "year", "'In November 2013 we launched the 777X and first delivery is expected in 2020.'",
       fact="2013", url=BA13, form="10-K 2013"),
    # Boeing in 2026
    bq("bq.deliv.9m", 475, "airplanes", "commercial deliveries in the first nine months of 2026 (737 367, 767 26, 777 20, "
       "787 62), against 440 a year earlier"),
    bq("bq.deliv.9m.2025", 440, "airplanes", "commercial deliveries in the first nine months of 2025", fact="2025-09-30"),
    bq("bq.bca.op.9m", -1582, "US$ million", "Commercial Airplanes: loss from operations, first nine months of 2026 (margin "
       "-5.0%; 2025's nine months -6,447, -21.4%)"),
    bq("bq.rate.737", 47, "airplanes a month", "'the 737 program began to transition from a production rate of 42 to 47 per "
       "month with the concurrence of the FAA' in the second quarter of 2026; 'now expect to stabilize in 2027'"),
    bq("bq.737.10", 2026, "year", "'In October 2026, we achieved certification of the 737-10' (the 737-7 in the third "
       "quarter)"),
    bq("bq.777x.first", 2027, "year", "'We continue to expect first delivery of the 777-9 to occur in 2027'; first delivery "
       "of the 777-8 passenger aircraft 'not expected to occur before 2030'"),
    bq("bq.backlog", 745431, "US$ million", "total backlog at 30 September 2026 (Commercial Airplanes 611,833)"),
    bq("bq.aq.737", 12800, "airplanes", "program accounting quantity: 737, raised by 400 in the first nine months of 2026"),
    bq("bq.cum.737", 9607, "airplanes", "cumulative 737 deliveries at 30 September 2026"),
    bq("bq.cum.787.2025", 1249, "airplanes", "cumulative 787 deliveries at 31 December 2025", fact="2025-12-31"),
    bq("bq.cum.777.2025", 1776, "airplanes", "cumulative 777 deliveries at 31 December 2025", fact="2025-12-31"),
    bq("bq.777x.dpc", 2731, "US$ million", "777X work in process includes deferred production costs of $2,731m at 30 "
       "September 2026 ($651m at 31 December 2025): early aircraft's costs above the program average, carried as inventory"),
    # Airbus
    ab("ab.deliv", 793, "airplanes", "commercial aircraft delivered: 93 A220, 607 A320 Family, 36 A330, 57 A350"),
    ab("ab.deliv.2024", 766, "airplanes", "commercial aircraft delivered, 2024", fact="2024"),
    ab("ab.deliv.a320", 607, "airplanes", "A320 Family deliveries"),
    ab("ab.deliv.a350", 57, "airplanes", "A350 deliveries"),
    ab("ab.deliv.a220", 93, "airplanes", "A220 deliveries"),
    ab("ab.deliv.a330", 36, "airplanes", "A330 deliveries"),
    ab("ab.rate.a320", 75, "airplanes a month", "the A320 Family's target rate: 'Due to continued tensions with one engine "
       "supplier, the Company expects to reach a rate of between 70 and 75 aircraft a month by the end of 2027, with the "
       "objective to stabilise at rate 75 thereafter'"),
    ab("ab.rate.a220", 13, "airplanes a month", "the A220's target: 'a rate of 13 aircraft a month for the A220 programme in "
       "2028'; rate 12 for the A350 in 2028, rate 5 for the A330 in 2029"),
    ab("ab.a220", 2018, "year", "Airbus Canada 'established on 1 July 2018 following the transaction between Airbus, Bombardier "
       "and Investment Quebec', the sale by Bombardier to Airbus of the A220 programme (formerly the C-series); Bombardier "
       "exited in February 2020"),
    ab("ab.fal", 5, "sites", "commercial final assembly lines in Toulouse, Hamburg, Mobile (Alabama), Tianjin (China) and "
       "Mirabel (Canada)"),
    ab("ab.tariff.charge", 0.1, "euro billion", "charges 'mainly related to the US tariffs pre-agreement period', 2025"),
    ab("ab.tariff", 2025, "year", "the US-EU trade agreement 'restored a tariff-free environment for trade in aircraft and "
       "parts on 1 September 2025'"),
    ab("ab.spirit.charge", 749, "euro million", "charge on acquiring Spirit AeroSystems businesses: a 500 impairment of A220 "
       "assets and 249 of onerous contracts, from 'the shift from contractual pricing (buy) to the underlying internal "
       "production costs (make)'"),
    ab("ab.backlog", 8754, "airplanes", "commercial order backlog at year end (a record)"),
    ab("ab.orders.net", 889, "airplanes", "net commercial orders (gross 1,000)"),
    ab("ab.orders.cum", 25510, "airplanes", "aircraft ordered since the start (455 customers)"),
    ab("ab.deliv.cum", 16756, "airplanes", "aircraft delivered since the start"),
    ab("ab.rev", 73420, "euro million", "revenue"),
    ab("ab.ebit", 6082, "euro million", "EBIT (reported); EBIT Adjusted 7,128"),
    ab("ab.ni", 5221, "euro million", "net income"),
    ab("ab.ca.rev", 52577, "euro million", "Airbus (commercial aircraft) segment revenue"),
    ab("ab.ca.ebit", 4555, "euro million", "Airbus (commercial aircraft) segment EBIT (reported)"),
    ab("ab.ds.rev", 13405, "euro million", "Airbus Defence and Space revenue"),
    ab("ab.ds.ebit", 639, "euro million", "Airbus Defence and Space EBIT (2024: -656)"),
    # engines
    ge("ge.base.commercial", 50000, "engines", "installed base of approximately 50,000 commercial engines (and 30,000 "
       "military), parked aircraft included"),
    ge("ge.services.share", 70, "percent", "aftermarket services 'approximately 70% of revenue'"),
    ge("ge.ces.equipment", 8304, "US$ million", "Commercial Engines & Services: equipment revenue"),
    ge("ge.ces.services", 25010, "US$ million", "Commercial Engines & Services: services revenue"),
    ge("ge.ces.profit", 8861, "US$ million", "Commercial Engines & Services: segment profit (margin 26.6%)"),
    ge("ge.engines", 2386, "engines", "commercial engines delivered (LEAP 1,802)"),
    ge("ge.leap", 1802, "engines", "LEAP engines delivered"),
    ge("ge.install", 1, "flag", "segment profit rose with spare parts and shop visits, 'partially offset by the impact of "
       "higher install engine deliveries'"),
    ge("ge.cfm", 50, "percent", "GE's share of CFM International, 'a 50-50 non-consolidated joint venture with Safran Aircraft "
       "Engines'; in the narrowbody market 'a significant ramp in production of the LEAP engine, which entered into service "
       "in 2016'"),
    r("rtx.gtf.fleet", 2600, "aircraft", "the GTF family 'now powers more than 2,600 aircraft for over 90 operators across "
      "three aircraft platforms: Airbus A320neo family, Airbus A220, and Embraer E-Jets E2'; the powder-metal inspections "
      "keep an 'elevated level of aircraft on ground' through the end of 2026", "RTX Corporation, Form 10-K 2025", RTX25,
      "2025"),
    r("rtx.pw.charge", 5.4, "US$ billion", "net sales charge for the 'Powder Metal Matter' (Pratt & Whitney's geared "
      "turbofan), third quarter of 2023", "RTX Corporation, Form 10-K 2025", RTX25, "2023"),
    # suppliers and lessors
    r("tdg.proprietary", 90, "percent", "share of net sales from proprietary products (about 55% from the aftermarket); "
      "aftermarket sales over an aircraft's life of 25 to 30 years, platforms produced for 20 to 30", "TransDigm Group, "
      "Form 10-K fiscal 2026", TDG26, "fiscal 2026"),
    r("tdg.acq", 1, "flag", "'a disciplined acquisition strategy focused on proprietary commercial aerospace component "
      "businesses with significant aftermarket content, where we see a clear path to create value and earn private "
      "equity-like returns'", "TransDigm Group, Form 10-K fiscal 2026", TDG26, "fiscal 2026"),
    r("tdg.aftermarket", 55, "percent", "share of net sales from the aftermarket", "TransDigm Group, Form 10-K fiscal "
      "2026", TDG26, "fiscal 2026"),
    r("aer.owned", 1501, "aircraft", "total owned aircraft at the end of the year: 1,340 held for operating leases, 126 "
      "in finance leases, 35 held for sale", "AerCap Holdings, Form 20-F 2025", AER25, "2025-12-31"),
    r("aer.leader", 1, "flag", "'AerCap is the global leader in aircraft leasing, with customers in every major geographical "
      "region'", "AerCap Holdings, Form 20-F 2025", AER25, "2025"),
    r("aer.order", 283, "aircraft", "new aircraft on order at 31 December 2025 (and 35 new engines, 12 new helicopters)", "AerCap Holdings, Form 20-F 2025", AER25, "2025"),
    r("aer.em", 45, "percent", "share of lease revenue from airlines in emerging-market countries (46% in 2024, 48% in 2023)", "AerCap Holdings, Form 20-F 2025", AER25, "2025"),
    r("aer.bought", 71, "aircraft", "new-technology aircraft purchased in 2025", "AerCap Holdings, Form 20-F 2025", AER25, "2025"),
    r("aer.sold", 108, "aircraft", "aircraft sold in 2025, 'primarily current technology aircraft with an average age of 15 "
      "years'", "AerCap Holdings, Form 20-F 2025", AER25, "2025"),
    r("aer.proceeds", 3.9, "US$ billion", "aggregate proceeds of flight equipment sales in 2025", "AerCap Holdings, Form 20-F 2025", AER25, "2025"),
    r("aer.gain", 819, "US$ million", "net gain on sale of assets in 2025", "AerCap Holdings, Form 20-F 2025", AER25, "2025"),
    r("aer.russia", 1.5, "US$ billion", "net recoveries related to the Ukraine Conflict in 2025, chiefly insurance settlements and "
      "a London Commercial Court judgment ($973m) on aircraft and engines lost in Russia, written off in 2022", "AerCap Holdings, Form 20-F 2025", AER25, "2025"),
    # defence
    r("lmt.usg", 72, "percent", "share of sales from the US Government (63% from the DoW, the filing's name for the Department of Defense)", "Lockheed "
      "Martin, Form 10-K 2025", LMT25, "2025"),
    r("lmt.costplus", 40, "percent", "cost-reimbursable contracts as a share of sales", "Lockheed Martin, Form 10-K 2025",
      LMT25, "2025"),
    r("lmt.f35", 27, "percent", "the F-35 program's share of total consolidated sales (67% of Aeronautics'); seven "
      "partner countries and twelve FMS customers", "Lockheed Martin, Form 10-K 2025", LMT25, "2025"),
    # the WTO
    r("wto.ds316", 7496, "US$ million a year", "countermeasures the arbitrator allowed the United States against EU "
      "subsidies to Airbus (launch aid among them): 'a level not exceeding, in total, USD 7,496 million'",
      "World Trade Organization, dispute DS316 (EC - Large Civil Aircraft), summary", WTO + "ds316_e.htm", "2019",
      "official"),
    r("wto.ds316.instances", 300, "instances", "'more than 300 separate instances of alleged subsidization, over a period of "
      "almost forty years', A300 to A380; the panel found that launch aid (LA/MSF) 'shifts a significant portion of the risk "
      "of launching an aircraft from the manufacturer to the governments supplying funding', and that Airbus 'would have "
      "been unable to bring to the market the LCA that it launched as and when it did but for the specific subsidies'",
      "World Trade Organization, dispute DS316 (EC - Large Civil Aircraft), summary", WTO + "ds316_e.htm", "2011",
      "official"),
    r("wto.ds353.nasa", 10.4, "US$ billion", "of the $19.1bn alleged, 'More than half of this amount was accounted for by the "
      "value of the alleged NASA R&D subsidies, which, according to the European Communities, was $10.4 billion'",
      "World Trade Organization, dispute DS353, summary", WTO + "ds353_e.htm", "2005", "official"),
    r("wto.ds353.panel", 5.3, "US$ billion", "the panel's estimate of the specific subsidies to Boeing, 1989-2006: 'at least "
      "$5.3 billion' (NASA and DOD aeronautics R&D, Washington State's B&O tax, FSC/ETI)", "World Trade Organization, "
      "dispute DS353, summary", WTO + "ds353_e.htm", "2011", "official"),
    r("wto.ds353", 3993.212564, "US$ million a year", "countermeasures the arbitrator allowed the EU against US subsidies "
      "to Boeing: 'USD 3,993,212,564 per annum'", "World Trade Organization, dispute DS353 (US - Large Civil Aircraft "
      "(2nd complaint)), summary", WTO + "ds353_e.htm", "2020", "official"),
    r("wto.ds353.claim", 19.1, "US$ billion", "the subsidies the European Communities alleged to Boeing, 1989-2006 ($10.4bn "
      "of them NASA R&D)", "World Trade Organization, dispute DS353, summary", WTO + "ds353_e.htm", "2005", "official"),
)
