"""Register rows for Part 2, *The Economy on One Page*.  Checked 2026-11-23.

The industry tables (value added, its components, the input-output table, employment, countries' shares) are frozen
extracts in this folder (``bea_va_2025.csv``, ``bea_va_history.csv``, ``bea_io_2023.csv``, ``fred_jobs.csv``,
``wb_shares.csv``), written by ``fetch.py`` with their sources; the rows below are the figures that come from company
filings and documents, and the headline numbers the narration states.
"""

from explainer.industry.register import Row, add

C = "2026-11-23"
P = (2,)
FR = "https://data.sec.gov/api/xbrl/frames/us-gaap/{}/USD/CY2025.json"
BEA_VA = "https://apps.bea.gov/industry/Release/XLS/GDPxInd/ValueAdded.xlsx"


def co(key, value, unit, definition, source, url, fact, kind="filing", note=""):
    return Row(key, value, unit, definition, source, url, fact, C, kind, note=note, parts=P)


add(
    # --- Leontief --------------------------------------------------------------------------------------------------
    co("leontief.1936", 44, "sectors", "Wassily Leontief, Quantitative Input and Output Relations in the Economic "
       "System of the United States, Review of Economic Statistics 18(3), August 1936: a table of the 1919 economy in "
       "44 sectors (41 of them producing)", "Leontief (1936); Bjerkholt (2016), Memorandum 18/2016, University of "
       "Oslo", "https://www.sv.uio.no/econ/english/research/publications/Memoranda/pdf-files/2016/memo-18-2016-"
       "versjon-2.pdf", "1936", "study"),
    co("leontief.1983", 0, "quote", "\"The role of humans as the most important factor of production is bound to "
       "diminish in the same way that the role of horses in agricultural production was first diminished and then "
       "eliminated by the introduction of tractors.\"", "Leontief (1983), National perspective: the definition of "
       "problems and opportunities, in The Long-Term Impact of Technology on Employment and Unemployment, National "
       "Academy of Engineering, p. 3", "https://onwork.edu.au/bibitem/1983-Leontief,Wassily-The+Long-Term+Impact+of+"
       "Technology+on+Employment+and+Unemployment-excerpt+p.3", "1983", "study"),
    co("leontief.nobel", 1973, "year", "Leontief's Nobel memorial prize in economics, for the input-output method",
       "The Nobel Prize, Wassily Leontief, biographical", "https://www.nobelprize.org/prizes/economic-sciences/1973/"
       "leontief/biographical/", "1973", "official"),

    # --- the biggest companies, 2025 (SEC frames: periods mostly in calendar 2025) -----------------------------------
    co("rev.amazon.2025", 716.924, "USD bn", "Amazon net sales, 2025 (North America $426.3bn, International $161.9bn, "
       "AWS $128.7bn; advertising $56.2bn)", "Amazon Form 10-K 2025", FR.format("RevenueFromContractWithCustomer"
       "ExcludingAssessedTax"), "2025"),
    co("oi.amazon.2025", 80.0, "USD bn", "Amazon operating income, 2025", "Amazon Form 10-K 2025 (SEC frames)",
       FR.format("OperatingIncomeLoss"), "2025"),
    co("oi.aws.2025", 45.606, "USD bn", "AWS operating income, 2025 (on net sales of $128.725bn)", "Amazon Form 10-K "
       "2025, segment information", "https://www.sec.gov/cgi-bin/browse-edgar?action=getcompany&CIK=0001018724&type="
       "10-K", "2025"),
    co("emp.amazon.2025", 1_576_000, "people", "Amazon full-time and part-time employees, 31 December 2025", "Amazon "
       "Form 10-K 2025", "https://www.sec.gov/cgi-bin/browse-edgar?action=getcompany&CIK=0001018724&type=10-K",
       "2025-12-31"),
    co("rev.walmart.fy2026", 713.2, "USD bn", "Walmart revenue, fiscal year to 31 January 2026 (gross margin 24.9%, "
       "operating margin 4.2%)", "Walmart Form 10-K FY2026 (SEC frames)", FR.format("Revenues"), "FY2026"),
    co("oi.walmart.fy2026", 29.8, "USD bn", "Walmart operating income, FY2026", "Walmart Form 10-K FY2026 (SEC "
       "frames)", FR.format("OperatingIncomeLoss"), "FY2026"),
    co("emp.walmart.fy2026", 2_100_000, "people", "Walmart associates, approximately, 31 January 2026", "Walmart Form "
       "10-K FY2026", "https://www.sec.gov/cgi-bin/browse-edgar?action=getcompany&CIK=0000104169&type=10-K",
       "2026-01-31"),
    co("rev.unitedhealth.2025", 447.6, "USD bn", "UnitedHealth Group revenue, 2025 (operating margin 4.2%)",
       "UnitedHealth Form 10-K 2025 (SEC frames)", FR.format("Revenues"), "2025"),
    co("emp.unitedhealth.2025", 390_000, "people", "UnitedHealth employees (\"more than 390,000\"), 31 December 2025",
       "UnitedHealth Form 10-K 2025", "https://www.sec.gov/cgi-bin/browse-edgar?action=getcompany&CIK=0000731766&type="
       "10-K", "2025-12-31"),
    co("rev.mckesson.fy2026", 403.43, "USD bn", "McKesson revenues, fiscal year to 31 March 2026", "McKesson Form "
       "10-K FY2026", "https://www.sec.gov/cgi-bin/browse-edgar?action=getcompany&CIK=0000927653&type=10-K", "FY2026"),
    co("gp.mckesson.fy2026", 14.55, "USD bn", "McKesson gross profit, FY2026 (gross margin 3.61%; operating expenses "
       "$8.34bn)", "McKesson Form 10-K FY2026", "https://www.sec.gov/cgi-bin/browse-edgar?action=getcompany&CIK="
       "0000927653&type=10-K", "FY2026"),
    co("emp.mckesson.fy2026", 43_000, "people", "McKesson employees (\"more than 43,000\"), 31 March 2026", "McKesson "
       "Form 10-K FY2026", "https://www.sec.gov/cgi-bin/browse-edgar?action=getcompany&CIK=0000927653&type=10-K",
       "2026-03-31"),
    co("rev.apple.fy2025", 416.161, "USD bn", "Apple net sales, FY2025 (gross profit $195.2bn; operating income "
       "$133.1bn)", "Apple Form 10-K FY2025", "https://www.sec.gov/Archives/edgar/data/320193/000032019325000079/"
       "aapl-20250927.htm", "FY2025"),
    co("emp.apple.fy2025", 166_000, "people", "Apple full-time equivalent employees, September 2025 (167,000 a year "
       "later)", "Apple Form 10-K FY2025", "https://www.sec.gov/Archives/edgar/data/320193/000032019325000079/"
       "aapl-20250927.htm", "2025-09-27", note="FY2026's 167,000 is in the FY2026 10-K"),
    co("rev.nvidia.fy2026", 215.9, "USD bn", "NVIDIA revenue, fiscal year to 25 January 2026 (gross margin 71.1%)",
       "NVIDIA Form 10-K FY2026 (SEC frames)", FR.format("Revenues"), "FY2026"),
    co("oi.nvidia.fy2026", 130.4, "USD bn", "NVIDIA operating income, FY2026", "NVIDIA Form 10-K FY2026 (SEC frames)",
       FR.format("OperatingIncomeLoss"), "FY2026"),
    co("emp.nvidia.fy2026", 42_000, "people", "NVIDIA employees, approximately, end of fiscal 2026", "NVIDIA Form 10-K "
       "FY2026", "https://www.sec.gov/cgi-bin/browse-edgar?action=getcompany&CIK=0001045810&type=10-K", "2026-01"),
    co("oi.apple.fy2025", 133.1, "USD bn", "Apple operating income, FY2025", "Apple Form 10-K FY2025 (SEC frames)",
       FR.format("OperatingIncomeLoss"), "FY2025"),
    co("oi.alphabet.2025", 129.0, "USD bn", "Alphabet operating income, 2025 (revenue $402.8bn)", "Alphabet Form 10-K "
       "2025 (SEC frames)", FR.format("OperatingIncomeLoss"), "2025"),
    co("emp.alphabet.2025", 190_820, "people", "Alphabet employees, 31 December 2025", "Alphabet Form 10-K 2025",
       "https://www.sec.gov/cgi-bin/browse-edgar?action=getcompany&CIK=0001652044&type=10-K", "2025-12-31"),
    co("oi.microsoft.fy2025", 128.5, "USD bn", "Microsoft operating income, fiscal year to 30 June 2025 (revenue "
       "$281.7bn)", "Microsoft Form 10-K FY2025 (SEC frames)", FR.format("OperatingIncomeLoss"), "FY2025"),
    co("emp.microsoft.fy2026", 223_000, "people", "Microsoft full-time employees, 30 June 2026", "Microsoft Form 10-K "
       "FY2026", "https://www.sec.gov/cgi-bin/browse-edgar?action=getcompany&CIK=0000789019&type=10-K", "2026-06-30"),
    co("rev.alphabet.2025", 402.836, "USD bn", "Alphabet revenues, 2025", "Alphabet Form 10-K 2025 (SEC company "
       "facts, accession 0001652044-26-000018)", FR.format("Revenues"), "2025"),
    co("rev.microsoft.fy2025", 281.724, "USD bn", "Microsoft revenue, fiscal year to 30 June 2025", "Microsoft Form "
       "10-K FY2025 (SEC company facts)", "https://data.sec.gov/api/xbrl/companyfacts/CIK0000789019.json", "FY2025"),
    co("rev.meta.2025", 200.966, "USD bn", "Meta Platforms revenue, 2025", "Meta Form 10-K 2025 (SEC company facts, "
       "accession 0001628280-26-003942)", "https://data.sec.gov/api/xbrl/companyfacts/CIK0001326801.json", "2025"),
    co("oi.unitedhealth.2025", 18.964, "USD bn", "UnitedHealth Group earnings from operations, 2025 (2024: $32.3bn)",
       "UnitedHealth Form 10-K 2025 (SEC company facts, accession 0000731766-26-000062)",
       "https://data.sec.gov/api/xbrl/companyfacts/CIK0000731766.json", "2025"),
    co("oi.mckesson.fy2026", 6.212, "USD bn", "McKesson operating income, fiscal year to 31 March 2026", "McKesson "
       "Form 10-K FY2026 (SEC company facts, accession 0000927653-26-000069)",
       "https://data.sec.gov/api/xbrl/companyfacts/CIK0000927653.json", "FY2026"),
    co("oi.meta.2025", 83.3, "USD bn", "Meta Platforms operating income, 2025 (revenue $201.0bn)", "Meta Form 10-K "
       "2025 (SEC frames)", FR.format("OperatingIncomeLoss"), "2025"),

    # --- headline figures from the extracts -------------------------------------------------------------------
    co("gdp.2025", 30.861, "USD tn", "US gross domestic product, 2025, the sum of value added by industry", "BEA, GDP "
       "by Industry, TVA105 (published 2026-09-30)", BEA_VA, "2025", "official"),
    co("jobs.2025", 158.4, "million", "US nonfarm payroll employment, 2025 average (PAYEMS)", "BLS Current Employment "
       "Statistics via FRED", "https://fred.stlouisfed.org/series/PAYEMS", "2025", "official"),
    co("jobs.1983", 90.3, "million", "US nonfarm payroll employment, 1983 average (PAYEMS)", "BLS Current Employment "
       "Statistics via FRED", "https://fred.stlouisfed.org/series/PAYEMS", "1983", "official"),
)

add(
    co("rev.aws.2025", 128.725, "USD bn", "AWS net sales, 2025 (18% of Amazon's)", "Amazon Form 10-K 2025, segment "
       "information", "https://www.sec.gov/cgi-bin/browse-edgar?action=getcompany&CIK=0001018724&type=10-K", "2025"),
)

add(
    co("gp.apple.fy2025", 195.201, "USD bn", "Apple gross margin (gross profit), FY2025", "Apple Form 10-K FY2025",
       "https://www.sec.gov/Archives/edgar/data/320193/000032019325000079/aapl-20250927.htm", "FY2025"),
)
