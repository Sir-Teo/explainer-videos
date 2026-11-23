"""Register rows for Part 3, *The Accounts*.  Checked 2026-11-23.

Six companies' latest annual accounts from their Forms 10-K (SEC EDGAR company facts and the filed documents), the
history the part opens with, and the Enron record its *Called it?* scores.  Amounts in billions of US dollars unless
the unit says otherwise.
"""

from explainer.industry.register import Row, add

C = "2026-11-23"
P = (3,)
CF = "https://data.sec.gov/api/xbrl/companyfacts/CIK{:010d}.json"
COST = "https://www.sec.gov/Archives/edgar/data/909832/000090983226000093/cost-20260830.htm"
MSFT = "https://www.sec.gov/Archives/edgar/data/789019/000119312526323660/msft-20260630.htm"
JPM = "https://www.sec.gov/Archives/edgar/data/19617/000162828026008131/jpm-20251231.htm"
NEE = "https://www.sec.gov/Archives/edgar/data/753308/000075330826000015/nee-20251231.htm"
DAL = "https://www.sec.gov/Archives/edgar/data/27904/000002790426000013/dal-20251231.htm"
LLY = "https://www.sec.gov/Archives/edgar/data/59478/000005947826000013/lly-20251231.htm"
ENE10K = "https://www.sec.gov/Archives/edgar/data/1024401/000102440101500010/ene10-k.txt"
ENE8K = "https://www.sec.gov/Archives/edgar/data/1024401/000095012901503835/h91831e8-k.txt"


def r(key, value, unit, definition, source, url, fact, kind="filing", note="", **kw):
    return Row(key, value, unit, definition, source, url, fact, C, kind, note=note, parts=P, **kw)


def co(prefix, src, url, fact, **items):
    """One company's figures: ``co("cost", "Costco Form 10-K FY2026", COST, "FY2026", rev=(303.154, "revenue"))``."""
    return [r(f"{prefix}.{k}", v, "USD bn" if not isinstance(d, tuple) else d[1], d if isinstance(d, str) else d[0],
              src, url, fact) for k, (v, d) in items.items()]


add(
    # --- history --------------------------------------------------------------------------------------------------
    r("pacioli.1494", 1494, "year", "Luca Pacioli's Summa de arithmetica, geometria, proportioni et proportionalita, "
      "printed in Venice by Paganino Paganini in November 1494; its section Particularis de computis et scripturis is "
      "the first printed description of double-entry bookkeeping, which Pacioli called the method of Venice",
      "National Library of Scotland (ICAS collection); History of Information", "https://www.nls.uk/collections/"
      "rare-books/collections/icas/pacioli", "1494", "study"),
    r("brown.1914", 1914, "year", "Donaldson Brown, assistant treasurer of DuPont, combined earnings, working capital "
      "and investment in plant into one measure he called return on investment, as profit on sales times sales per "
      "dollar invested; he took the method to General Motors in 1921", "Hagley Museum and Library, The Father of "
      "ROI: Donaldson Brown", "https://www.hagley.org/node/452", "1914", "study"),
    # --- Costco, fiscal year to 30 August 2026 ---------------------------------------------------------------------
    *co("cost", "Costco Form 10-K FY2026 (SEC company facts and the filing)", COST, "FY2026",
        rev=(303.154, "total revenue, fiscal 2026 (net sales plus membership fees)"),
        fees=(5.907, "membership fees, fiscal 2026 (2025: $5.323bn)"),
        cogs=(264.279, "merchandise costs"), sga=(27.190, "selling, general and administrative expenses"),
        oi=(11.685, "operating income"), ni=(9.226, "net income attributable to Costco"),
        assets=(89.045, "total assets, 30 August 2026"), equity=(35.803, "total Costco stockholders' equity"),
        inventory=(19.324, "merchandise inventories"), payables=(22.591, "accounts payable"),
        ppe=(35.633, "property and equipment, net"), cash=(20.207, "cash and cash equivalents"),
        ocf=(15.817, "net cash provided by operating activities"), capex=(6.435, "payments for property and "
        "equipment"), da=(2.674, "depreciation and amortization"), sbc=(0.924, "stock-based compensation"),
        members=(84.1, ("paid members, end of fiscal 2026 (2025: 81.0 million)", "million")),
        warehouses=(939, ("warehouses in operation worldwide, 647 in the US", "warehouses"))),
    # --- Microsoft, fiscal year to 30 June 2026 ----------------------------------------------------------------------
    *co("msft", "Microsoft Form 10-K FY2026 (SEC company facts and the filing)", MSFT, "FY2026",
        rev=(331.839, "revenue"), cogs=(106.374, "cost of revenue"), rd=(35.562, "research and development"),
        oi=(155.237, "operating income"), ni=(133.749, "net income, including $6.5bn of net gains from investments "
        "in OpenAI"), assets=(758.376, "total assets, 30 June 2026"), equity=(442.387, "stockholders' equity"),
        ppe=(313.076, "property and equipment, net (2025: $205.0bn)"), goodwill=(119.651, "goodwill"),
        unearned=(72.965, "unearned revenue, current: customers' payments for services not yet delivered"),
        ocf=(182.935, "net cash from operations"), capex=(115.948, "additions to property and equipment"),
        sbc=(12.405, "stock-based compensation expense"), openai=(6.5, "net gains from investments in OpenAI in other "
        "income, mostly the dilution gain from OpenAI's October 2025 recapitalization (fiscal 2025: $4.8bn of net "
        "losses)"), cloud=(214.0, "Microsoft Cloud revenue, fiscal 2026, up 27% (the 10-K gives $214 billion)")),
    *co("msft", "Microsoft Form 10-K FY2026, segment results of operations", MSFT, "FY2026",
        pbp_rev=(139.996, "Productivity and Business Processes revenue (Microsoft 365, LinkedIn, Dynamics); "
                 "fiscal 2025: $120.810bn"), pbp_oi=(83.879, "Productivity and Business Processes operating income"),
        ic_rev=(137.791, "Intelligent Cloud revenue (Azure, server products); fiscal 2025: $106.265bn"),
        ic_oi=(56.972, "Intelligent Cloud operating income"),
        ic_cogs_growth=(0.44, ("Intelligent Cloud cost of revenue growth, fiscal 2026, 'driven by investments in AI "
                               "infrastructure'", "share")),
        azure_growth=(0.41, ("Azure and other cloud services revenue growth, fiscal 2026", "share")),
        mpc_rev=(54.052, "More Personal Computing revenue (Windows, devices, Xbox, search advertising); fiscal 2025: "
                 "$54.649bn"), mpc_oi=(14.386, "More Personal Computing operating income")),
    *co("msft", "Microsoft Form 10-K FY2025 (SEC company facts)", CF.format(789019), "FY2025",
        ocf25=(136.162, "net cash from operations, fiscal 2025"), capex25=(64.551, "additions to property and "
        "equipment, fiscal 2025"), oi25=(128.528, "operating income, fiscal 2025")),
    *co("msft", "Microsoft Forms 10-Q (SEC company facts): quarter to 30 September", CF.format(789019), "FY2027 Q1",
        ocf_q1fy27=(58.0, "net cash from operations, July-September 2026"), capex_q1fy27=(39.37, "additions to "
        "property and equipment, July-September 2026"), oi_q1fy27=(45.91, "operating income, July-September 2026"),
        ocf_q1fy26=(45.05, "net cash from operations, July-September 2025"), capex_q1fy26=(19.39, "additions to "
        "property and equipment, July-September 2025")),
    r("msft.capex_guide.fy2027", 170, "USD bn", "Microsoft's guidance for capital expenditures in fiscal 2027, "
      "including finance leases, about $170bn (some reports of the call give $175bn); it expects to stay free cash "
      "flow positive", "Microsoft FY2026 Q4 earnings call, 29 July 2026, as reported by Investing Live and Nasdaq",
      "https://investinglive.com/stocks/microsoft-sees-170bn-capex-in-fiscal-2027-but-says-it-will-stay-cash-flow-"
      "positive/", "2026-07-29", "press", lo=170, hi=175,
      note="Microsoft's own guidance on its earnings call, as two outlets reported it; not a filed figure"),
    # --- JPMorgan Chase, 2025 ----------------------------------------------------------------------------------------
    *co("jpm", "JPMorgan Chase Form 10-K 2025, selected financial data", JPM, "2025",
        rev=(182.447, "total net revenue"), nii=(95.443, "net interest income"), nonint=(87.004, "noninterest "
        "revenue"), opex=(95.640, "total noninterest expense"), provision=(14.212, "provision for credit losses"),
        pretax=(72.595, "income before income tax expense"), ni=(57.048, "net income"),
        assets=(4424.9, "total assets, 31 December 2025"), deposits=(2559.32, "deposits"),
        loans=(1493.429, "loans"), equity=(362.438, "total stockholders' equity"),
        roe=(0.17, ("return on common equity", "share")), roa=(0.0129, ("return on assets", "share")),
        employees=(318_512, ("employees, 31 December 2025", "people"))),
    # --- NextEra Energy, 2025 ------------------------------------------------------------------------------------------
    *co("nee", "NextEra Energy Form 10-K 2025", NEE, "2025",
        rev=(27.412, "operating revenues"), oi=(8.280, "operating income"), ni=(6.835, "net income attributable to "
        "NextEra Energy"), assets=(212.721, "total assets, 31 December 2025"), equity=(54.608, "common "
        "shareholders' equity"), ppe=(156.197, "property, plant and equipment, net"), debt=(89.556, "long-term "
        "debt"), ocf=(12.485, "net cash provided by operating activities"), capex_fpl=(8.719, "capital expenditures "
        "of FPL"), capex_neer=(15.332, "independent power and other investments of NEER"),
        accounts=(6, ("FPL customer accounts, more than 6 million (about 12 million people)", "million"))),
    # --- Delta Air Lines, 2025 -------------------------------------------------------------------------------------
    *co("dal", "Delta Air Lines Form 10-K 2025", DAL, "2025",
        rev=(63.364, "total operating revenue"), oi=(5.822, "operating income"), ni=(5.005, "net income"),
        assets=(81.317, "total assets, 31 December 2025"), equity=(20.853, "stockholders' equity"),
        ppe=(39.743, "property and equipment, net"), ocf=(8.342, "net cash provided by operating activities"),
        capex=(4.499, "payments for flight equipment, ground property and equipment"), fuel=(9.819, "aircraft fuel "
        "and related taxes"), labor=(17.520, "salaries, wages and benefits"), atl=(7.157, "air traffic liability: "
        "tickets sold, not yet flown"), loyalty=(9.262, "loyalty program deferred revenue, current $4.876bn and "
        "noncurrent $4.386bn: miles sold, not yet redeemed"), amex=(8.2, "remuneration from American Express for "
        "SkyMiles and the co-brand cards, up 11%"),
        asm=(298_045, ("available seat miles", "million")), trasm=(21.26, ("total revenue per available seat mile",
        "cents")), casm=(19.31, ("cost per available seat mile", "cents")), casm_ex=(13.86, ("CASM excluding fuel "
        "and other items (non-GAAP)", "cents")), load=(0.84, ("passenger load factor", "share")),
        employees=(103_000, ("full-time equivalent employees", "people"))),
    # --- Eli Lilly, 2025 -----------------------------------------------------------------------------------------
    *co("lly", "Eli Lilly Form 10-K 2025 (SEC company facts and the filing)", LLY, "2025",
        rev=(65.179, "revenue"), cogs=(11.052, "cost of sales"), rd=(13.337, "research and development"),
        sga=(11.094, "marketing, selling and administrative"), pretax=(25.731, "income before income taxes"),
        nonop=(-0.571, "other income (expense), net, including interest"), ni=(20.640, "net income"),
        assets=(112.476, "total assets, 31 December 2025"), equity=(26.535, "total Eli Lilly shareholders' equity"),
        inventory=(13.744, "inventories"), receivables=(17.760, "accounts receivable, net"),
        ocf=(16.813, "net cash provided by operating activities"), capex=(7.841, "purchases of property and "
        "equipment"), mounjaro=(22.965, "Mounjaro revenue (US $13.651bn)"), zepbound=(13.542, "Zepbound revenue")),
    # --- Enron -------------------------------------------------------------------------------------------------------
    r("mclean.2001", 0, "quote", "\"How exactly does Enron make its money?\" Bethany McLean, \"Is Enron Overpriced?\", "
      "Fortune, 5 March 2001: Enron traded at about 55 times trailing earnings; its return on invested capital was "
      "around 7%; its cash flow from operations fell from $1.6bn (1998) to $1.2bn (1999), and in the first nine "
      "months of 2000 it generated just $100 million", "Fortune, republished 30 December 2015",
      "https://fortune.com/2015/12/30/is-enron-overpriced-fortune-2001/", "2001-03-05", "press",
      note="the journalist's article, quoted; its figures are from Enron's filings and analysts"),
    r("enron.rev.2000", 100.789, "USD bn", "Enron total revenues, 2000 (1999: $40.1bn)", "Enron Form 10-K 2000",
      ENE10K, "2000"),
    r("enron.ni.2000", 0.979, "USD bn", "Enron net income as reported, 2000 (1999: $0.893bn; 1998: $0.703bn)",
      "Enron Form 10-K 2000", ENE10K, "2000"),
    r("enron.cfo.2000", 4.779, "USD bn", "Enron net cash provided by operating activities, 2000 (1999: $1.228bn; "
      "1998: $1.640bn)", "Enron Form 10-K 2000", ENE10K, "2000"),
    r("enron.cfo.1999", 1.228, "USD bn", "Enron net cash provided by operating activities, 1999", "Enron Form 10-K "
      "2000", ENE10K, "1999"),
    r("enron.restate", 0.591, "USD bn", "the reduction in Enron's net income for 1997-2000 in its restatement "
      "(reported $2,680m, restated $2,089m), with debt at the end of 2000 raised by $628m", "Enron Form 8-K, 8 "
      "November 2001, Table 1", ENE8K, "2001-11-08"),
    r("enron.ch11", 2001, "year", "Enron Corp. filed for relief under chapter 11 on 2 December 2001", "Enron Form "
      "8-K, filed 17 December 2001", "https://www.sec.gov/Archives/edgar/data/1024401/000102440101500046/"
      "ene8-k1214.txt", "2001-12-02"),
    r("levin.prepays", 8, "USD bn", "Enron used prepays to obtain approximately $8 billion of financing over about six "
      "years, reported as energy trading activity instead of debt", "Senator Carl Levin, statement at the hearing on "
      "the role of the financial institutions in Enron's collapse, Permanent Subcommittee on Investigations, 23 July "
      "2002", "https://www.hsgac.senate.gov/wp-content/uploads/imo/media/doc/levin072302.pdf", "2002-07-23",
      "official"),
)
