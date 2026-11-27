"""Register rows for Part 24, *Construction*.  Checked 2026-11-27.

The Empire State Building's fact sheet; the California High-Speed Rail Authority's business plans of November 2008 and
2026; the National Audit Office's investigation of the collapse of Carillion (June 2018); Flyvbjerg (2014) on
megaprojects; Ferrovial's Form 20-F for 2025; the Forms 10-K of Fluor and Quanta Services for 2025 and Quanta's
third-quarter 2026 results (Form 8-K, Exhibit 99.1).  Series are the Filing Room's SEC, FRED and BEA extracts.
"""

from explainer.industry.register import Row, add

C = "2026-11-27"
P = (24,)
SEC = "https://www.sec.gov/Archives/edgar/data/"
FER = SEC + "1468522/000162828026011789/fer-20251231.htm"
FLR = SEC + "1124198/000112419826000007/flr-20251231.htm"
PWR = SEC + "1050915/000105091526000006/pwr-20251231.htm"
PWRQ = SEC + "1050915/000119312526436949/d77812dex991.htm"
ESB = "https://www.esbnyc.com/sites/default/files/esb_fact_sheet_final.pdf"
HSR08 = "https://hsr.ca.gov/wp-content/uploads/docs/about/business_plans/BPlan_2008_FullRpt.pdf"
HSR26 = "https://hsr.ca.gov/wp-content/uploads/2026/06/2026-Final-Business-Plan-060126-A11Y.pdf"
NAO = ("https://www.nao.org.uk/wp-content/uploads/2018/06/"
       "Investigation-into-the-governments-handling-of-the-collapse-of-Carillion.pdf")
FLY = "https://arxiv.org/abs/1409.0003"


def r(key, value, unit, definition, source, url, fact, kind="filing", note="", **kw):
    return Row(key, value, unit, definition, source, url, fact, C, kind, note=note, parts=P, **kw)


def esb(key, value, unit, definition, fact="1930-1931"):
    return r(key, value, unit, definition, "Empire State Building, fact sheet", ESB, fact)


def hsr(key, value, unit, definition, y=2026):
    if y == 2008:
        return r(key, value, unit, definition, "California High-Speed Rail Authority, Business Plan, November 2008", HSR08,
                 "2008-11", kind="official")
    return r(key, value, unit, definition, "California High-Speed Rail Authority, 2026 Business Plan", HSR26, "2026",
             kind="official")


def nao(key, value, unit, definition, fact="2017-2018"):
    return r(key, value, unit, definition, "National Audit Office, Investigation into the government's handling of the "
             "collapse of Carillion (HC 1002, 7 June 2018)", NAO, fact, kind="official")


def fly(key, value, unit, definition):
    return r(key, value, unit, definition, "Bent Flyvbjerg, 'What You Should Know about Megaprojects and Why: An Overview', "
             "Project Management Journal 45(2), 2014, pp. 6-19", FLY, "projects completed before 2014", kind="study")


def fer(key, value, unit, definition, fact="2025"):
    return r(key, value, unit, definition, "Ferrovial SE, Form 20-F for 2025", FER, fact)


def flr(key, value, unit, definition, fact="2025-12-31"):
    return r(key, value, unit, definition, "Fluor Corporation, Form 10-K for 2025", FLR, fact)


# Flyvbjerg (2014), Table 2: cost overruns of large projects (percent)
OVERRUNS = {"suez": ("Suez Canal", 1900), "scot": ("Scottish Parliament Building", 1600),
            "sydney": ("Sydney Opera House", 1400), "nhs": ("UK National Health Service IT system", 550),
            "bigdig": ("Boston's Big Dig", 220), "denver": ("Denver International Airport", 200),
            "brooklyn": ("Brooklyn Bridge", 100), "channel": ("Channel Tunnel", 80),
            "jubilee": ("London Jubilee Line extension", 80), "greatbelt": ("Great Belt east bridge", 50)}

add(
    esb("esb.ground", 1930.21, "date", "'Groundbreaking of the building commenced on March 17, 1930'", "1930-03-17"),
    esb("esb.open", 1931.33, "date", "'On May 1, 1931, then President Herbert Hoover pressed a button in Washington, D.C., to "
        "officially open the Empire State Building'", "1931-05-01"),
    esb("esb.days", 410, "days", "from groundbreaking (17 March 1930) to the official opening (1 May 1931): one year and 45 "
        "days; the fact sheet counts its 'one year and 45 days' from the first steel columns (7 April 1930) to completion (31 "
        "March 1931)", "1930-03-17 to 1931-05-01"),
    esb("esb.stories", 4.5, "stories a week", "'Framework rose at a rate of 4 1/2 stories per week'"),
    esb("esb.hours", 7, "million hours", "'More than 7 million man hours were logged in the Empire State Building's "
        "construction'"),
    esb("esb.floors", 102, "floors", "'The Empire State Building has 102 floors'"),
    esb("esb.height", 1454, "feet", "'The total height of the building is 1,454 feet ... from the base to the top of the building's "
        "antenna'"),
    esb("esb.sqft", 2.8, "million square feet", "'2.8 million square feet of office space'"),

    hsr("hsr08.cost", 33, "US$ billion (2008)", "'The high-speed train system's backbone Los Angeles/Anaheim to San Francisco "
        "link is expected to cost about $33 billion, in 2008 dollars'", 2008),
    hsr("hsr08.bond", 9, "US$ billion", "'Proposition 1A provides $9 billion in bond' funds for the system (on the November "
        "2008 ballot)", 2008),
    hsr("hsr26.phase1", 126.1, "US$ billion", "'Phase 1 will require a total capital investment of $126.1 billion, with "
        "completion set for 2039 and full service to start in 2040' (an optimized approach using existing lines)"),
    hsr("hsr26.full", 231.3, "US$ billion (2026)", "'re-estimate the full Phase 1 buildout at approximately $231.3 billion in "
        "today's dollars'"),
    hsr("hsr26.mb", 35.7, "US$ billion", "Merced to Bakersfield: 'The estimated M-B capital costs have been revised to $35.7 "
        "billion'"),
    hsr("hsr26.mb.done", 2032, "year", "'The updated completion date for the M-B early operating segment is 2032. This "
        "one-year extension accounts for additional time for optimization and pending policy changes'; the plan's revenue "
        "outlook takes 2033 as the first full year of service"),
    hsr("hsr26.phase1.done", 2039, "year", "Phase 1 'completion set for 2039 and full service to start in 2040'"),
    hsr("hsr26.cvs", 119, "miles", "the Central Valley segment between Merced and Bakersfield"),
    hsr("hsr26.cvs.done", 81, "miles", "'Guideway miles completed and ready for rail' on the 119-mile Central Valley segment (38 "
        "remaining, 27 underway); 61 structures completed, 31 remaining"),
    hsr("hsr26.track", 3.5, "US$ billion", "'In November 2025, the Authority released a Request for Bid ... up to $3.5 billion to "
        "deliver track, electrification, train control, communications, and safety systems across the 119-mile Central Valley "
        "Segment'"),
    fly("fly.schedule", 10, "percent", "'approximately one out of ten megaprojects is on budget, one out of ten is on schedule, and "
        "one out of ten is on benefits'"),
    hsr("hsr26.spent", 14.6, "US$ billion", "'From 2006 through 2025, the Authority invested $14.6 billion statewide'"),

    nao("nao.date", 2018.04, "date", "'On 15 January 2018 the Carillion group of companies (Carillion) declared insolvency'",
        "2018-01-15"),
    nao("nao.staff", 45000, "people", "Carillion 'employed around 45,000 people' (around 18,200 in the UK at liquidation)"),
    nao("nao.contracts", 420, "contracts", "'around 420 contracts with the UK public sector'"),
    nao("nao.revenue", 5.2, "GBP billion", "Carillion's global revenue in 2016 (£5,214m)", "2016"),
    nao("nao.warn1", 845, "GBP million", "'on 10 July Carillion announced a £845 million provision for losses on its "
        "contracts'", "2017-07-10"),
    nao("nao.warn2", 1050, "GBP million", "'on 29 September it increased this to £1.05 billion'", "2017-09-29"),
    nao("nao.cash", 655, "GBP million", "Carillion 'reported losing £655 million of cash from operations in 2017' "
        "(its business plan to creditors, 10 January 2018)", "2017"),
    nao("nao.pension", 2.6, "GBP billion", "'the £2.6 billion pension liabilities'"),
    nao("nao.paydays", 45, "days", "'on average, it was paying its suppliers 45 days after the invoice date in the first five "
        "months of 2017 ... Almost one third of invoices were paid more than 60 days later'", "2017-01 to 2017-05"),
    nao("nao.advance", 1, "flag", "among practices an FTI review said 'enhanced reported financial performance above "
        "underlying operating performance': 'securing large advance payments on new contracts at the expense of future "
        "profitability'"),

    fly("fly.share", 90, "percent", "'Nine out of ten such projects have cost overruns'"),
    fly("fly.brown", 1, "flag", "Willie Brown, former mayor of San Francisco, in his San Francisco Chronicle column of 28 July 2013, "
        "as quoted by Flyvbjerg: 'In the world of civic projects, the first budget is really just a down payment. If people "
        "knew the real cost from the start, nothing would ever be approved.'"),
    fly("fly.vietnam", 1, "flag", "the 'break-fix model': 'Typically lock-in and escalation make it impossible to drop projects "
        "altogether ... \"easy to begin and difficult and expensive to stop\"'; explanations: 'optimism bias, the planning "
        "fallacy, strategic misrepresentation, and principal-agent behavior'; the cure: 'to get projects right from the outset "
        "so they don't break, through proper front-end management'"),
    fly("fly.rail", 44.7, "percent", "rail projects: 'an average cost overrun of 44.7 percent combines with an average demand "
        "shortfall of 51.4 percent'"),
    fly("fly.rail.demand", 51.4, "percent", "rail projects: average demand shortfall"),
    fly("fly.road", 20.4, "percent", "roads: 'an average cost overrun of 20.4 percent combines with a fifty-fifty risk that "
        "demand is also wrong by more than 20 percent'"),
    *[fly(f"fly.over.{k}", v, "percent", f"cost overrun of the {name} (Table 2)") for k, (name, v) in OVERRUNS.items()],

    fer("fer.con.rev", 7653, "EUR million", "Construction segment revenues, 2025"),
    fer("fer.con.op", 357, "EUR million", "Construction segment operating profit, 2025"),
    fer("fer.hwy.rev", 1374, "EUR million", "Highways segment revenues, 2025 (consolidated toll roads)"),
    fer("fer.hwy.op", 719, "EUR million", "Highways segment operating profit, 2025"),
    fer("fer.407.rev", 2009, "CAD million", "407 ETR's revenues, 2025, 'driven largely by the increase in toll rates on "
        "February 1, 2025 coupled with higher traffic'"),
    fer("fer.407.net", 811, "CAD million", "407 ETR's net result, 2025"),
    fer("fer.407.stake", 48.3, "percent", "Ferrovial's interest in the 407 ETR after buying a further 5.06% for CAD 1.99 "
        "billion in June 2025"),
    fer("fer.407.buy", 1.99, "CAD billion", "price of the additional 5.06% of 407 ETR, June 2025", "2025-06-06"),
    fer("fer.book", 17.4, "EUR billion", "Ferrovial Construction's order book at 31 December 2025", "2025-12-31"),
    fer("fer.public", 84, "percent", "share of the construction order book from public-sector clients", "2025-12-31"),

    flr("flr.reimb", 20713, "US$ million", "backlog under reimbursable contracts (81% of the total)"),
    flr("flr.lump", 4823, "US$ million", "backlog under lump-sum and guaranteed maximum contracts (19%)"),
    flr("flr.reimb.2024", 22589, "US$ million", "backlog under reimbursable contracts, 31 December 2024 (79%)", "2024-12-31"),
    flr("flr.lump.2024", 5895, "US$ million", "backlog under lump-sum and guaranteed maximum contracts, 31 December 2024 (21%)",
        "2024-12-31"),
    flr("flr.adj", 108, "US$ million", "Urban Solutions: 'forecast adjustments for cost growth on 3 infrastructure projects "
        "related to subcontracted design errors, price escalation, schedule impacts', 2025", "2025"),
    flr("flr.santos", 643, "US$ million", "revenue reversed in 2025 for a judgment on the Santos project in Australia, "
        "completed in 2015", "2025"),
    flr("flr.lossbook", 255, "US$ million", "backlog for legacy projects in a loss position ($702 million a year earlier)"),
    flr("flr.lumpsum", 1, "flag", "'Under lump-sum contracts, we may bid based upon preliminary engineering drawings and "
        "specifications provided by the client ... it requires us to predetermine the work to be performed, the project "
        "execution schedule and all costs associated with the work based on incomplete information'"),
    r("mlm.distance", 1, "flag", "'Generally, the distance shipments travel by truck from a given quarry is limited because the cost "
      "of transporting processed aggregates to customers is high relative to the price of the product itself'",
      "Martin Marietta Materials, Inc., Form 10-K for 2025", SEC + "916076/000119312526059193/mlm-20251231.htm", "2025"),
    r("pwr.backlog.2025", 43.98, "US$ billion", "Quanta Services' total backlog at 31 December 2025 (up 27.3%)",
      "Quanta Services, Inc., Form 10-K for 2025", PWR, "2025-12-31"),
    r("pwr.msa", 44, "percent", "share of Quanta's total backlog under master service agreements at 31 December 2025 (37% of the "
      "12-month backlog)", "Quanta Services, Inc., Form 10-K for 2025", PWR, "2025-12-31"),
    r("pwr.demand", 1, "flag", "'load growth expectations, which have accelerated based on demand for electricity driven by data "
      "centers, manufacturing and reshoring'; Quanta designs and installs 'electrical systems for large load centers, such as "
      "data center, advanced manufacturing and industrial facilities'", "Quanta Services, Inc., Form 10-K for 2025", PWR,
      "2025"),
    r("pwr.backlog", 63.7, "US$ billion", "Quanta Services' total backlog at 30 September 2026, 'a record'",
      "Quanta Services, Inc., Form 8-K of 29 October 2026 (Exhibit 99.1)", PWRQ, "2026-09-30"),
    r("pwr.q3", 12.01, "US$ billion", "Quanta's revenues in the third quarter of 2026 ($7.63 billion a year before)",
      "Quanta Services, Inc., Form 8-K of 29 October 2026 (Exhibit 99.1)", PWRQ, "Q3 2026"),
    r("pwr.q3.prev", 7.63, "US$ billion", "Quanta's revenues in the third quarter of 2025",
      "Quanta Services, Inc., Form 8-K of 29 October 2026 (Exhibit 99.1)", PWRQ, "Q3 2025"),
)
