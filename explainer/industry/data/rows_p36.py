"""Register rows for Part 36, *Software*.  Checked 2026-11-28.

The Forms 10-K of Microsoft and Atlassian (fiscal 2026, to June), Oracle (to May 2026), Salesforce, Snowflake, CrowdStrike
and Workday (to January 2026), Adobe (to November 2025), ServiceNow and Datadog (2025); Microsoft's 10-Q for the first
quarter of fiscal 2027 and Salesforce's for the second quarter of fiscal 2027; Adobe's 10-K for fiscal 2013; Salesforce's
investor-day exhibits of September 2021 and September 2022 (Forms 8-K).  Series are the Filing Room's SEC and FRED extracts.
"""

from explainer.industry.register import Row, add

C = "2026-11-28"
P = (36,)
SEC = "https://www.sec.gov/Archives/edgar/data/"
MSFT = SEC + "789019/000119312526323660/msft-20260630.htm"
MSFTQ = SEC + "789019/000119312526436133/msft-20260930.htm"
ORCL = SEC + "1341439/000119312526277521/orcl-20260531.htm"
CRM = SEC + "1108524/000110852426000060/crm-20260131.htm"
CRMQ = SEC + "1108524/000110852426000190/crm-20260731.htm"
CRM21 = SEC + "1108524/000119312521280853/d233992dex991.htm"
CRM22 = SEC + "1108524/000110852422000047/vfinal_investordayxfy23x.htm"
ADBE = SEC + "796343/000079634326000003/adbe-20251128.htm"
ADBE13 = SEC + "796343/000079634314000004/adbe10kfy13.htm"
NOW = SEC + "1373715/000137371526000007/now-20251231.htm"
SNOW = SEC + "1640147/000164014726000008/snow-20260131.htm"
TEAM = SEC + "1650372/000165037226000036/team-20260630.htm"
DDOG = SEC + "1561550/000162828026008819/ddog-20251231.htm"
CRWD = SEC + "1535527/000153552726000010/crwd-20260131.htm"


def r(key, value, unit, definition, source, url, fact, kind="filing", note="", **kw):
    return Row(key, value, unit, definition, source, url, fact, C, kind, note=note, parts=P, **kw)


def ms(key, value, unit, definition, fact="FY2026"):
    return r(key, value, unit, definition, "Microsoft, Form 10-K for fiscal 2026 (year to 30 June 2026)", MSFT, fact)


def crm(key, value, unit, definition, fact="FY2026"):
    return r(key, value, unit, definition, "Salesforce, Form 10-K for fiscal 2026 (year to 31 January 2026)", CRM, fact)


def ad(key, value, unit, definition, fact="FY2025"):
    return r(key, value, unit, definition, "Adobe, Form 10-K for fiscal 2025 (year to 28 November 2025)", ADBE, fact)


def ad13(key, value, unit, definition, fact="FY2013"):
    return r(key, value, unit, definition, "Adobe Systems, Form 10-K for fiscal 2013", ADBE13, fact)


def wk(key, value, unit, definition, lo, hi):
    return r(key, value, unit, definition, "this series' assumption", "", "", kind="assumption", lo=lo, hi=hi)


add(
    # Microsoft
    ms("ms36.rev", 331.839, "US$ billion", "total revenue, fiscal 2026 ($281,724m in fiscal 2025)"),
    ms("ms36.product", 64.696, "US$ billion", "product revenue (licences and devices), fiscal 2026"),
    ms("ms36.service", 267.143, "US$ billion", "service and other revenue, fiscal 2026 ($217,778m in fiscal 2025)"),
    ms("ms36.cost", 106.374, "US$ billion", "total cost of revenue, fiscal 2026"),
    ms("ms36.pcost", 12.098, "US$ billion", "cost of product revenue (licences and devices), fiscal 2026"),
    ms("ms36.scost", 94.276, "US$ billion", "cost of service and other revenue, fiscal 2026 ($74,330m in fiscal 2025)"),
    ms("ms36.rnd", 35.562, "US$ billion", "research and development, fiscal 2026"),
    ms("ms36.sm", 26.710, "US$ billion", "sales and marketing, fiscal 2026"),
    ms("ms36.cloud", 214.4, "US$ billion", "Microsoft Cloud revenue, fiscal 2026, up 27% (Microsoft 365 Commercial cloud, Azure and other "
       "cloud services, the commercial portion of LinkedIn, Dynamics 365)"),
    ms("ms36.cloudgm", 66, "percent", "Microsoft Cloud gross margin percentage, fiscal 2026, 'decreased to 66% driven by continued "
       "investments in AI infrastructure'"),
    ms("ms36.rpo", 678, "US$ billion", "commercial remaining performance obligation, up 84%, 30 June 2026", "2026-06-30"),
    ms("ms36.azure", 41, "percent", "growth of Azure and other cloud services revenue, fiscal 2026"),
    ms("ms36.seats", 6, "percent", "growth of Microsoft 365 Commercial seats, fiscal 2026"),
    ms("ms36.staff", 223000, "people", "full-time employees at 30 June 2026 (77,000 in product research and development)", "2026-06-30"),
    r("ms36.q1cloud", 63.9, "US$ billion", "Microsoft Cloud revenue in the first quarter of fiscal 2027 (to 30 September 2026), up 30%; "
      "commercial remaining performance obligation $677bn, up 73%", "Microsoft, Form 10-Q for the first quarter of fiscal 2027",
      MSFTQ, "2026-09-30"),

    # Salesforce
    crm("cr36.rev", 41.525, "US$ billion", "total revenues, fiscal 2026 ($37,895m in fiscal 2025)"),
    crm("cr36.sub", 39.388, "US$ billion", "subscription and support revenues, fiscal 2026 (95% of revenues)"),
    crm("cr36.prof", 2.137, "US$ billion", "professional services and other revenues, fiscal 2026"),
    crm("cr36.cost", 9.270, "US$ billion", "total cost of revenues, fiscal 2026 (gross profit $32,255m, 78%)"),
    crm("cr36.rnd", 5.993, "US$ billion", "research and development, fiscal 2026 (15% of revenues)"),
    crm("cr36.sm", 14.345, "US$ billion", "sales and marketing, fiscal 2026 (35% of revenues); 'Sales and marketing expenses make up the "
        "majority of our operating expenses'"),
    crm("cr36.ga", 3.000, "US$ billion", "general and administrative, fiscal 2026"),
    crm("cr36.restr", 0.586, "US$ billion", "restructuring, fiscal 2026"),
    crm("cr36.op", 8.331, "US$ billion", "income from operations, fiscal 2026 (20% of revenues)"),
    crm("cr36.rpo", 72.4, "US$ billion", "remaining performance obligation at 31 January 2026, up 14%; current (next twelve months) "
        "$35.1bn, up 16%", "2026-01-31"),
    crm("cr36.crpo", 35.1, "US$ billion", "current remaining performance obligation at 31 January 2026", "2026-01-31"),
    crm("cr36.ocf", 15.0, "US$ billion", "operating cash flow, fiscal 2026, up 15%"),
    crm("cr36.billing", 1, "flag", "'We generally invoice our customers in advance, in annual installments'; 'In general, we collect our "
        "billings in advance of the subscription service period'; founded in 1999"),
    r("cr36.target", 50, "US$ billion", "'$50B+ FY26 Target' (revenue for the year to January 2026), set at its investor day of "
      "September 2021", "Salesforce, investor-day presentation, Form 8-K exhibit 99.1, 24 September 2021", CRM21, "2021-09"),
    r("cr36.target22", 50, "US$ billion", "'$50B FY26 Target', '17% CAGR', restated at its investor day of September 2022 with a "
      "foreign-exchange headwind of about $2bn", "Salesforce, investor-day presentation, Form 8-K, 21 September 2022", CRM22, "2022-09"),
    r("cr36.h1", 22.478, "US$ billion", "total revenues in the first half of fiscal 2027 (to 31 July 2026), against $20,065m a year "
      "before", "Salesforce, Form 10-Q for the second quarter of fiscal 2027", CRMQ, "2026-07-31"),

    # Adobe
    ad("ad36.rev", 23.769, "US$ billion", "total revenue, fiscal 2025"),
    ad("ad36.sub", 22.904, "US$ billion", "subscription revenue, fiscal 2025 (96% of revenue)"),
    ad("ad36.product", 0.325, "US$ billion", "product revenue, fiscal 2025 (2%)"),
    ad("ad36.services", 0.540, "US$ billion", "services and other revenue, fiscal 2025"),
    ad("ad36.cost", 2.551, "US$ billion", "total cost of revenue, fiscal 2025"),
    ad("ad36.staff", 31360, "people", "employees at 28 November 2025", "2025-11-28"),
    ad13("ad36.r13", 4.0552, "US$ billion", "total revenue, fiscal 2013, down 8% from $4,403.7m in fiscal 2012"),
    ad13("ad36.r12", 4.4037, "US$ billion", "total revenue, fiscal 2012", "FY2012"),
    ad13("ad36.sub13", 1.1379, "US$ billion", "subscription revenue, fiscal 2013 (28% of revenue; $673.2m and 15% in 2012, 11% in 2011)"),
    ad13("ad36.prod13", 61, "percent", "product (licence) revenue, share of total, fiscal 2013 (76% in 2012, 81% in 2011)"),
    ad13("ad36.cc13", 1.4, "million", "paid Creative Cloud subscriptions at the end of fiscal 2013 (0.3 million a year before)"),
    ad13("ad36.arr13", 768.0, "US$ million", "Creative ARR exiting fiscal 2013 ($155.0m a year before)"),
    ad13("ad36.ratable", 1, "flag", "'We anticipate that our shift to a subscription model will increase the amount of our recurring "
         "revenue that is ratably reported'; 'we have focused on migrating existing users of our creative products from perpetual "
         "licenses to the subscription offering'"),

    # Oracle, ServiceNow, Snowflake, Datadog, CrowdStrike, Atlassian
    r("or36.rpo", 638, "US$ billion", "remaining performance obligations at 31 May 2026 ($138bn a year before), 'primarily attributable "
      "to certain significant cloud contracts'", "Oracle, Form 10-K for fiscal 2026", ORCL, "2026-05-31"),
    r("or36.rev", 67.357, "US$ billion", "total revenues, fiscal 2026 (+17%)", "Oracle, Form 10-K for fiscal 2026", ORCL, "FY2026"),
    r("nw36.big", 603, "customers", "customers with annual contract value above $5m at 31 December 2025 (502 a year before, 420 at the "
      "end of 2023)", "ServiceNow, Form 10-K for 2025", NOW, "2025-12-31"),
    r("sn36.nrr", 125, "percent", "net revenue retention rate at 31 January 2026 (126% a year before); 'we generally recognize revenue on "
      "consumption and not ratably over the term of the contract'", "Snowflake, Form 10-K for fiscal 2026", SNOW, "2026-01-31"),
    r("sn36.big", 733, "customers", "customers contributing more than $1m of trailing twelve-month product revenue at 31 January 2026 "
      "(576 a year before)", "Snowflake, Form 10-K for fiscal 2026", SNOW, "2026-01-31"),
    r("dd36.nrr", 120, "percent", "trailing twelve-month dollar-based net retention rate at 31 December 2025, 'about 120%' "
      "('high-110%'s' a year before)", "Datadog, Form 10-K for 2025", DDOG, "2025-12-31"),
    r("cw36.arr", 5.3, "US$ billion", "ARR at 31 January 2026, up 24%, of which $1.0bn net new ARR added in fiscal 2026",
      "CrowdStrike, Form 10-K for fiscal 2026", CRWD, "2026-01-31"),
    r("cw36.arr25", 4.2, "US$ billion", "ARR at 31 January 2025, up 23%", "CrowdStrike, Form 10-K for fiscal 2026", CRWD, "2025-01-31"),
    r("tm36.flywheel", 1, "flag", "'we've engineered a frictionless flywheel with an emphasis on self-service, making it easy for "
      "customers to try and get value first and foremost and then virally expand within an organization'", "Atlassian, Form 10-K "
      "for fiscal 2026", TEAM, "FY2026"),

    # The Works
    wk("wk36.arr", 200, "US$ million", "the Works' company's ARR at the start", 50, 1000),
    wk("wk36.gm", 0.78, "share", "gross margin after hosting, support and customer success (Salesforce: 78%)", 0.65, 0.85),
    wk("wk36.churn", 0.08, "a year", "share of ARR lost to customers leaving or cutting back", 0.04, 0.15),
    wk("wk36.exp", 0.10, "a year", "extra ARR from customers who stay", 0.05, 0.25),
    wk("wk36.reps", 100, "people", "ramped salespeople at the start", 50, 300),
    wk("wk36.prod", 0.45, "US$ million a year", "new ARR a ramped salesperson brings in", 0.3, 0.8),
    wk("wk36.repcost", 0.7, "US$ million a year", "sales and marketing cost per salesperson, with managers, engineers and marketing", 0.5, 1.0),
    wk("wk36.market", 300, "people", "salespeople at which crowding halves each one's productivity", 150, 600),
    wk("wk36.rnd", 40, "US$ million a year", "engineering at the start", 25, 70),
    wk("wk36.scale", 150, "US$ million", "extra product stock that doubles quality", 75, 300),
    wk("wk36.decay", 0.20, "a year", "yearly decay of the product stock", 0.1, 0.35),
)
