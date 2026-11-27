"""Refresh the Filing Room's frozen extracts from their public sources (SOURCES.md).

    python -m explainer.industry.data.fetch bea_va       # BEA value added by industry, 2025, and its components
    python -m explainer.industry.data.fetch bea_hist     # BEA value added as a share of GDP, 1947-2025
    python -m explainer.industry.data.fetch bea_io       # BEA 2023 sector use table and direct requirements
    python -m explainer.industry.data.fetch fred_jobs    # FRED payroll employment by industry, annual
    python -m explainer.industry.data.fetch wb_shares    # World Bank: industry shares of GDP by country
    python -m explainer.industry.data.fetch wb_mfg_usd   # World Bank: manufacturing value added in dollars
    python -m explainer.industry.data.fetch census_susb  # Census: employer firms and jobs by firm size, 2022
    python -m explainer.industry.data.fetch fred_prices  # BLS: price indexes for services and goods, hourly pay
    python -m explainer.industry.data.fetch sec_annual   # SEC: annual 10-K figures of the companies in SEC_COMPANIES
    python -m explainer.industry.data.fetch bea_real     # BEA real value added and prices by industry
    python -m explainer.industry.data.fetch fred_pay     # BLS: average hourly earnings by industry
    python -m explainer.industry.data.fetch eia_power    # EIA: capacity, generation, fuel costs, heat rates
    python -m explainer.industry.data.fetch damodaran_roc  # Damodaran: return on capital by US industry, 2015-2025
    python -m explainer.industry.data.fetch census_conc  # Census: the four largest firms' share by industry, 2022
    python -m explainer.industry.data.fetch fred_cycle   # FRED: hogs since 1858, housing, oil, sales and orders
    python -m explainer.industry.data.fetch esef_maersk  # Maersk's annual results from its ESEF filings, 2019-2025
    python -m explainer.industry.data.fetch sec_quarterly  # SEC: quarterly revenue and operating income (Micron, Intel)
    python -m explainer.industry.data.fetch owid_tech    # Our World in Data: US households adopting 40 technologies
    python -m explainer.industry.data.fetch fred_market  # FRED: bottled water shipments and prices; US population
    python -m explainer.industry.data.fetch --all

Each extract is a small CSV in this folder, committed, with the source URL and the retrieval date in its first
comment lines; scenes and labs read the CSVs (``read(name)``), never the network.  BEA's, FRED's and the World
Bank's data are public; the extracts keep only the rows a film uses.
"""

from __future__ import annotations

import csv
import datetime as dt
import io
import json
import sys
import urllib.request
import zipfile
from pathlib import Path

HERE = Path(__file__).resolve().parent
UA = {"User-Agent": "explainer-videos research bot (education)"}
BEA = "https://apps.bea.gov/industry/"
TODAY = dt.date.today().isoformat()


def _get(url: str, tries: int = 4) -> bytes:
    import time

    if "fred.stlouisfed.org" in url:  # FRED drops urllib's connections here; curl is served
        import subprocess

        return subprocess.run(["curl", "-sL", "--max-time", "120", "--retry", "3", url], check=True,
                              capture_output=True).stdout
    for k in range(tries):
        try:
            with urllib.request.urlopen(urllib.request.Request(url, headers=UA), timeout=120) as r:
                return r.read()
        except Exception:  # a dropped connection: wait and try again, last with curl (some hosts refuse urllib)
            if k == tries - 1:
                import subprocess

                return subprocess.run(["curl", "-sL", "--max-time", "120", "-A", UA["User-Agent"], url], check=True,
                                      capture_output=True).stdout
            time.sleep(3 * (k + 1))


def _write(name: str, header: list, rows: list, sources: list[str]) -> Path:
    path = HERE / f"{name}.csv"
    with path.open("w", newline="") as f:
        for s in sources:
            f.write(f"# source: {s}\n")
        f.write(f"# retrieved: {TODAY}\n")
        w = csv.writer(f)
        w.writerow(header)
        w.writerows(rows)
    return path


def read(name: str) -> list[dict]:
    """The rows of an extract as dicts (numbers converted where they parse)."""
    lines = [ln for ln in (HERE / f"{name}.csv").read_text().splitlines() if not ln.startswith("#")]
    out = []
    for r in csv.DictReader(lines):
        d = {}
        for k, v in r.items():
            if k in ("code", "name", "sector", "country"):  # identifiers stay text ("11" is an industry code)
                d[k] = v
                continue
            try:
                d[k] = float(v) if v not in ("", None) else None
            except ValueError:
                d[k] = v
        out.append(d)
    return out


# BEA's sectors as this series groups them (line numbers of BEA's GDP-by-industry tables)
SECTORS = [
    (3, "Farms, forestry, fishing"), (6, "Mining"), (10, "Utilities"), (11, "Construction"), (12, "Manufacturing"),
    (34, "Wholesale trade"), (35, "Retail trade"), (40, "Transportation and warehousing"), (49, "Information"),
    (55, "Finance and insurance"), (60, "Real estate"), (66, "Professional and technical services"),
    (70, "Management of companies"), (71, "Administrative and waste services"), (75, "Educational services"),
    (76, "Health care and social assistance"), (82, "Arts and recreation"), (85, "Hotels and restaurants"),
    (88, "Other services"), (89, "Government"),
]


def _bea_tables() -> dict:
    import openpyxl

    wb = openpyxl.load_workbook(io.BytesIO(_get(BEA + "Release/XLS/GDPxInd/ValueAdded.xlsx")), read_only=True)

    def table(sheet):
        rows = list(wb[sheet].iter_rows(values_only=True))
        hdr = [r for r in rows if r and r[0] == "Line"][0]
        return {int(r[0]): (str(r[1]).strip(), dict(zip(hdr[2:], r[2:]))) for r in rows
                if r and r[0] and str(r[0]).strip().isdigit()}
    return {s: table(s) for s in ("TVA105-A", "TVA110-A", "TVA112-A")}


def bea_va():
    t = _bea_tables()
    va, pc, comp = t["TVA105-A"], t["TVA110-A"], t["TVA112-A"]
    # TVA112 lists, under each industry, its three components (its own line numbers differ): find them by name
    comp_rows = list(comp.values())
    KEYS = ("Compensation of employees", "Taxes on production and imports less subsidies", "Gross operating surplus")

    def components(line):
        target = va[line][0]
        for i, (name, d) in enumerate(comp_rows):
            if name == target:
                got = {}
                for n2, d2 in comp_rows[i + 1:]:
                    if n2 not in KEYS:
                        break
                    got[n2] = d2.get("2025")
                return tuple(got.get(k) for k in KEYS)
        return (None, None, None)
    rows = [[1, "All industries (GDP)", va[1][1]["2025"], 100, 100, *components(1)]]
    for line, name in SECTORS:
        rows.append([line, name, va[line][1]["2025"], pc[line][1]["2025"], pc[line][1]["1997"], *components(line)])
    return _write("bea_va_2025", ["line", "sector", "va_musd", "pct_gdp", "pct_gdp_1997", "comp_pct", "tax_pct",
                                  "gos_pct"], rows,
                  [BEA + "Release/XLS/GDPxInd/ValueAdded.xlsx (TVA105, TVA110, TVA112; published 2026-09-30)"])


HIST = [(3, "Farms, forestry, fishing"), (12, "Manufacturing"), (54, "Finance, insurance and real estate"),
        (65, "Professional and business services"), (76, "Health care and social assistance"), (49, "Information"),
        (89, "Government")]


def bea_hist():
    import openpyxl

    z = zipfile.ZipFile(io.BytesIO(_get(BEA + "iTables%20Static%20Files/AllTablesHist.zip")))
    old = openpyxl.load_workbook(io.BytesIO(z.read("GDPbyInd_VA_1947-1997.xlsx")), read_only=True)["VAPercentGDP"]
    rows = list(old.iter_rows(values_only=True))
    hdr = [r for r in rows if r and r[0] == "Line"][0]
    byname = {str(r[1]).strip(): dict(zip(hdr[2:], r[2:])) for r in rows if r and r[1]}
    new = _bea_tables()["TVA110-A"]
    out = []
    names = {3: "Agriculture, forestry, fishing, and hunting", 12: "Manufacturing",
             54: "Finance, insurance, real estate, rental, and leasing", 65: "Professional and business services",
             76: "Health care and social assistance", 49: "Information", 89: "Government"}
    for y in range(1947, 2026):
        row = [y]
        for line, _ in HIST:
            v = new[line][1].get(str(y)) if y >= 1998 else byname[names[line]].get(str(y))
            row.append(v)
        out.append(row)
    return _write("bea_va_history", ["year"] + [n for _, n in HIST], out,
                  [BEA + "iTables%20Static%20Files/AllTablesHist.zip (GDPbyInd_VA_1947-1997, VAPercentGDP)",
                   BEA + "Release/XLS/GDPxInd/ValueAdded.xlsx (TVA110, 1998-2025)"])


IO_CODES = ["11", "21", "22", "23", "31G", "42", "44RT", "48TW", "51", "FIRE", "PROF", "6", "7", "81", "G"]


def bea_io():
    import openpyxl

    z = zipfile.ZipFile(io.BytesIO(_get(BEA + "iTables%20Static%20Files/AllTablesIO.zip")))
    use = openpyxl.load_workbook(io.BytesIO(z.read("IOUse_After_Redefinitions_PRO_1997-2023_Sector.xlsx")),
                                 read_only=True)["2023"]
    rows = list(use.iter_rows(values_only=True))
    hdr = list(rows[5])
    idx = [hdr.index(c) for c in IO_CODES]
    num = lambda v: float(v) if isinstance(v, (int, float)) else 0.0  # noqa: E731  ("..." = suppressed: 0)
    finals = ("F010", "F030", "F040", "F050", "F020", "F100")  # PCE, inventories, exports, imports, investment, govt
    cols = {k: hdr.index(k) for k in finals}
    out = []
    for r in rows[7:]:
        if r[0] in IO_CODES + ["Used", "Other"]:
            out.append([r[0], r[1]] + [num(r[i]) for i in idx] + [num(r[cols[k]]) for k in finals[:4]] + [num(r[-1])]
                       + [num(r[cols[k]]) for k in finals[4:]])
    # value added rows: an industry's output is its column's sum
    for r in rows[7:]:
        if r[0] in ("V001", "V002", "V003"):
            out.append([r[0], r[1]] + [num(r[i]) for i in idx] + [0] * 7)
    return _write("bea_io_2023", ["code", "name"] + IO_CODES + ["pce", "inventories", "exports", "imports",
                                                                "commodity_output", "investment", "government"], out,
                  [BEA + "iTables%20Static%20Files/AllTablesIO.zip (IOUse_After_Redefinitions_PRO_1997-2023_Sector, "
                         "2023, producers' prices, $ millions)"])


FRED_JOBS = ["PAYEMS", "MANEMP", "USEHS", "OUTMS", "USCONS", "USTRADE", "USWTRADE", "CES4300000001", "USINFO",
             "USFIRE", "USPBS", "CES6562000001", "USLAH", "USGOVT", "CES1021000001", "CES4422000001",
             "CES6561000001", "USSERV"]


def fred_jobs():
    data = {}
    for s in FRED_JOBS:
        txt = _get(f"https://fred.stlouisfed.org/graph/fredgraph.csv?id={s}&fq=Annual&fam=avg").decode()
        for line in txt.splitlines()[1:]:
            d, v = line.split(",")
            if v not in ("", "."):
                data.setdefault(int(d[:4]), {})[s] = float(v)
    rows = [[y] + [data[y].get(s) for s in FRED_JOBS] for y in sorted(data) if y >= 1939]
    return _write("fred_jobs", ["year"] + FRED_JOBS, rows,
                  ["https://fred.stlouisfed.org (BLS Current Employment Statistics, thousands, annual averages; "
                   "OUTMS: manufacturing sector real output index, 2017=100)"])


WB = {"NV.IND.MANF.ZS": "manufacturing", "NV.AGR.TOTL.ZS": "agriculture", "NV.SRV.TOTL.ZS": "services"}
WB_COUNTRIES = "USA;CHN;DEU;JPN;KOR;IND;GBR;FRA;BRA;MEX;VNM;IDN;NGA;SAU"


def wb_shares():
    vals = {}
    for code, name in WB.items():
        url = (f"https://api.worldbank.org/v2/country/{WB_COUNTRIES}/indicator/{code}?format=json&date=2015:2025"
               "&per_page=500")
        for x in json.loads(_get(url))[1]:
            if x["value"] is not None:
                vals.setdefault((x["country"]["value"], int(x["date"])), {})[name] = x["value"]
    rows = [[c, y, v.get("manufacturing"), v.get("agriculture"), v.get("services")] for (c, y), v in sorted(vals.items())]
    return _write("wb_shares", ["country", "year", "manufacturing", "agriculture", "services"], rows,
                  ["https://api.worldbank.org (World Development Indicators: NV.IND.MANF.ZS, NV.AGR.TOTL.ZS, "
                   "NV.SRV.TOTL.ZS, % of GDP)"])


def wb_mfg_usd():
    """Manufacturing value added in current US dollars: each country's share of the world's."""
    url = ("https://api.worldbank.org/v2/country/WLD;CHN;USA;JPN;DEU;KOR;IND;MEX;GBR;FRA;ITA;VNM/indicator/"
           "NV.IND.MANF.CD?format=json&date=2020:2025&per_page=500")
    rows = [[x["country"]["value"], int(x["date"]), x["value"]] for x in json.loads(_get(url))[1]
            if x["value"] is not None]
    return _write("wb_mfg_usd", ["country", "year", "mfg_usd"], sorted(rows),
                  ["https://api.worldbank.org (World Development Indicators: NV.IND.MANF.CD, current US$)"])


def bea_real():
    """Real value added (chain-type quantity index, 2017 = 100) and its price index by industry, every BEA line,
    1997-2025 (TVA103-A, TVA104-A)."""
    import openpyxl

    wb = openpyxl.load_workbook(io.BytesIO(_get(BEA + "Release/XLS/GDPxInd/ValueAdded.xlsx")), read_only=True)
    out, years = [], None
    for sheet, measure in (("TVA103-A", "quantity"), ("TVA104-A", "price")):
        for r in wb[sheet].iter_rows(values_only=True):
            if r and r[0] == "Line":
                years = [int(y) for y in r[3:] if y]
            elif r and r[0] and str(r[0]).isdigit() and r[1]:
                name = str(r[1])
                depth = (len(name) - len(name.lstrip())) // 2
                out.append([measure, int(r[0]), depth, name.strip()] + [x if isinstance(x, (int, float)) else None
                                                                       for x in r[3:3 + len(years)]])
    return _write("bea_real", ["measure", "line", "depth", "industry"] + [str(y) for y in years], out,
                  [BEA + "Release/XLS/GDPxInd/ValueAdded.xlsx (TVA103-A quantity and TVA104-A price indexes, "
                         "2017=100; published 2026-09-30)"])


EIA_TABLES = {"epa_04_03": "capacity by energy source, 2025 (MW)", "epa_03_01_a": "net generation by energy source "
              "(thousand MWh)", "epa_07_04": "average cost of fossil fuels ($/MMBtu)", "epa_08_01": "average operating "
              "heat rate (Btu/kWh)", "epa_08_02": "average tested heat rates by prime mover (Btu/kWh)",
              "epa_08_04": "operating expenses of major investor-owned utilities (mills/kWh)",
              "epa_02_04": "average retail price of electricity (cents/kWh)",
              "epa_04_08_a": "capacity factors of fossil-fuelled generators by technology",
              "epa_04_08_b": "capacity factors of generators not primarily using fossil fuels"}


def eia_power():
    """EIA Electric Power Annual tables, flattened: one row per (table, row label, column label, value)."""
    import openpyxl

    out = []
    for t, what in EIA_TABLES.items():
        ws = openpyxl.load_workbook(io.BytesIO(_get(f"https://www.eia.gov/electricity/annual/xls/{t}.xlsx")),
                                    read_only=True).worksheets[0]
        header, block = None, ""
        for r in ws.iter_rows(values_only=True):
            cells = list(r)
            if not any(c is not None for c in cells):
                continue
            first = cells[0]
            nums = [c for c in cells[1:] if isinstance(c, (int, float))]
            if not nums and any(isinstance(c, str) and c.strip() for c in cells[1:]):
                header = [str(c).strip().replace("\n", " ") if c is not None else "" for c in cells]
                continue
            if not nums and isinstance(first, (str, int)) and str(first).strip():
                block = str(first).strip()
                continue
            if header and nums:
                for j, c in enumerate(cells[1:], start=1):
                    if isinstance(c, (int, float)) and j < len(header):
                        out.append([t, block, str(first).strip(), header[j], c])
    return _write("eia_power", ["table", "block", "row", "column", "value"], out,
                  ["https://www.eia.gov/electricity/annual/ (Electric Power Annual 2025): " +
                   "; ".join(f"{k} {v}" for k, v in EIA_TABLES.items())])


# Companies and XBRL tags for the annual SEC extract: (CIK, ticker, [tags]); the first tag present wins for each item
SEC_ITEMS = {"revenue": ["RevenueFromContractWithCustomerExcludingAssessedTax", "Revenues", "SalesRevenueNet",
                         "RegulatedAndUnregulatedOperatingRevenue"],
             "operating_income": ["OperatingIncomeLoss"], "net_income": ["NetIncomeLoss"],
             "operating_cash": ["NetCashProvidedByUsedInOperatingActivities"],
             "capex": ["PaymentsToAcquirePropertyPlantAndEquipment", "PaymentsToAcquireProductiveAssets",
                       "PaymentsToAcquireOilAndGasPropertyAndEquipment", "PaymentsToExploreAndDevelopOilAndGasProperties",
                       "PaymentsToAcquireOilAndGasProperty"],
             "assets": ["Assets"], "equity": ["StockholdersEquity"],
             "depreciation": ["DepreciationDepletionAndAmortization", "DepreciationAmortizationAndAccretionNet",
                              "DepreciationAndAmortization", "Depreciation"],
             "inventory": ["InventoryNet"]}
SEC_COMPANIES = [(789019, "MSFT"), (909832, "COST"), (19617, "JPM"), (753308, "NEE"), (27904, "DAL"), (59478, "LLY"),
                 (1403161, "V"), (723125, "MU"), (34088, "XOM"), (882184, "DHI"), (50863, "INTC"),
                 (1141391, "MA"), (104169, "WMT"), (1652044, "GOOGL"), (1018724, "AMZN"), (1326801, "META"),
                 (1543151, "UBER"), (2042694, "PRMB"), (354950, "HD"), (60667, "LOW"),
                 (93410, "CVX"), (1163165, "COP"), (821189, "EOG"), (797468, "OXY"), (1090012, "DVN"),
                 (1035002, "VLO"), (1510295, "MPC"), (87347, "SLB"), (45012, "HAL"), (3570, "LNG"),
                 (831259, "FCX"), (1164727, "NEM"), (1001838, "SCCO"), (915913, "ALB"),
                 (7084, "ADM"), (1996862, "BG"), (1755672, "CTVA"), (315189, "DE"), (100493, "TSN"), (1324404, "CF"),
                 (1285785, "MOS"), (802481, "PPC"), (48465, "HRL"), (40704, "GIS"), (1637459, "KHC"), (77476, "PEP"),
                 (1103982, "MDLZ"), (47111, "HSY"), (56873, "KR")]


# where a company's first-choice tag means something else: Mastercard tagged its gross revenue, before rebates and
# incentives to customers, as revenue from contracts in 2018-2021; its net revenue is "Revenues"
SEC_OVERRIDES = {"MA": {"revenue": ["Revenues", "SalesRevenueNet",
                                  "RevenueFromContractWithCustomerExcludingAssessedTax"]},
                 # Valero and Halliburton tag revenue including excise taxes they collect; Occidental reports profit
                 # including its non-controlling interests as ProfitLoss when it has no NetIncomeLoss for the year
                 "VLO": {"revenue": ["RevenueFromContractWithCustomerIncludingAssessedTax", "Revenues", "SalesRevenueNet"]},
                 "HAL": {"revenue": ["RevenueFromContractWithCustomerIncludingAssessedTax", "Revenues", "SalesRevenueNet",
                                     "RevenueFromContractWithCustomerExcludingAssessedTax"]},
                 "OXY": {"net_income": ["NetIncomeLoss", "ProfitLoss"]},
                 # Freeport and Southern Copper tag profit to common shareholders, not NetIncomeLoss, in most years
                 "FCX": {"net_income": ["NetIncomeLoss", "NetIncomeLossAvailableToCommonStockholdersBasic"]},
                 "SCCO": {"net_income": ["NetIncomeLoss", "NetIncomeLossAvailableToCommonStockholdersBasic"]},
                 # ADM and Bunge tag only part of their sales as revenue from contracts with customers (the rest is
                 # commodity trading revenue); their total is Revenues.  Hormel and Kraft Heinz tag revenue including
                 # the excise taxes they collect; CF tags profit to common shareholders, not NetIncomeLoss
                 "ADM": {"revenue": ["Revenues", "SalesRevenueNet"]},
                 "BG": {"revenue": ["Revenues", "SalesRevenueNet"]},
                 "HRL": {"revenue": ["RevenueFromContractWithCustomerIncludingAssessedTax", "Revenues", "SalesRevenueNet"]},
                 "KHC": {"revenue": ["RevenueFromContractWithCustomerIncludingAssessedTax", "Revenues", "SalesRevenueNet"]},
                 "CF": {"net_income": ["NetIncomeLoss", "NetIncomeLossAvailableToCommonStockholdersBasic"]}}


def sec_annual():
    """Annual figures from each company's Forms 10-K (SEC company facts): the latest filing's value for every fiscal
    year, for the items in SEC_ITEMS.  Duration items need a year-long period; balance items are taken at year end."""
    import time

    out = []
    for cik, tic in SEC_COMPANIES:
        facts = json.loads(_get(f"https://data.sec.gov/api/xbrl/companyfacts/CIK{cik:010d}.json"))["facts"]["us-gaap"]
        time.sleep(0.5)
        years: dict = {}
        for item, tags in SEC_ITEMS.items():
            tags = SEC_OVERRIDES.get(tic, {}).get(item, tags)
            for tag in tags:
                best: dict = {}
                for v in facts.get(tag, {}).get("units", {}).get("USD", []):
                    if v.get("form") not in ("10-K", "10-K/A"):
                        continue
                    if "start" in v:
                        d = (dt.date.fromisoformat(v["end"]) - dt.date.fromisoformat(v["start"])).days
                        if not 350 <= d <= 380:
                            continue
                    if v["end"] not in best or v["filed"] > best[v["end"]]["filed"]:
                        best[v["end"]] = v
                for end, v in best.items():
                    years.setdefault(end, {}).setdefault(item, v["val"] / 1e9)
        for end in sorted(years):
            if end >= "2009":
                out.append([tic, end] + [years[end].get(k) for k in SEC_ITEMS])
    return _write("sec_annual", ["ticker", "year_end"] + list(SEC_ITEMS), out,
                  ["https://data.sec.gov/api/xbrl/companyfacts/ (Forms 10-K, US$ billions; tags: " +
                   "; ".join(f"{k}: {'/'.join(v)}" for k, v in SEC_ITEMS.items()) + ")"])


FRED_PAY = {"CES0500000003": "Total private", "CES1000000003": "Mining", "CES2000000003": "Construction",
            "CES3000000003": "Manufacturing", "CES4142000003": "Wholesale trade", "CES4200000003": "Retail trade",
            "CES4300000003": "Transportation", "CES4422000003": "Utilities", "CES5000000003": "Information",
            "CES5500000003": "Finance, insurance, real estate", "CES6000000003": "Professional and business services",
            "CES6500000003": "Education and health care", "CES7000000003": "Leisure and hospitality",
            "CES8000000003": "Other services"}


def fred_pay():
    """Average hourly earnings of all employees by industry, annual averages since 2006 (BLS CES via FRED)."""
    data = {}
    for sid in FRED_PAY:
        txt = _get(f"https://fred.stlouisfed.org/graph/fredgraph.csv?id={sid}&fq=Annual&fam=avg").decode()
        for line in txt.splitlines()[1:]:
            d, v = line.split(",")
            if v not in (".", ""):
                data.setdefault(int(d[:4]), {})[sid] = float(v)
    years = sorted(y for y in data if y <= dt.date.today().year - 1)
    return _write("fred_pay", ["year"] + list(FRED_PAY), [[y] + [data[y].get(k) for k in FRED_PAY] for y in years],
                  ["https://fred.stlouisfed.org (BLS Current Employment Statistics, average hourly earnings of all "
                   "employees, dollars, annual averages: " + "; ".join(f"{k} {v}" for k, v in FRED_PAY.items()) + ")"])


FRED_PRICES = {"CPIAUCSL": "All items", "CUSR0000SAS": "Services", "CUSR0000SAD": "Durable goods",
               "CUSR0000SAM2": "Medical care services", "CUSR0000SEEB": "Tuition, school fees and childcare",
               "CUSR0000SEFV": "Food away from home", "CUSR0000SEHA": "Rent of primary residence",
               "CUSR0000SETA01": "New vehicles", "CPIAPPSL": "Apparel", "CUSR0000SERE01": "Toys",
               "CUUR0000SEEE01": "Computers, peripherals and smart home assistants",
               "AHETPI": "Average hourly earnings of production and nonsupervisory employees"}


def fred_prices():
    """Consumer price indexes for services and goods, and production workers' hourly pay, annual averages since 2000
    (BLS via FRED)."""
    data = {}
    for sid in FRED_PRICES:
        txt = _get(f"https://fred.stlouisfed.org/graph/fredgraph.csv?id={sid}&fq=Annual&fam=avg").decode()
        for line in txt.splitlines()[1:]:
            d, v = line.split(",")
            if v not in (".", "") and int(d[:4]) >= 2000:
                data.setdefault(int(d[:4]), {})[sid] = float(v)
    years = sorted(y for y in data if y <= dt.date.today().year - 1)
    return _write("fred_prices", ["year"] + list(FRED_PRICES), [[y] + [data[y].get(k) for k in FRED_PRICES]
                                                               for y in years],
                  ["https://fred.stlouisfed.org (BLS consumer price indexes, US city average, and average hourly "
                   "earnings; annual averages: " + "; ".join(f"{k} {v}" for k, v in FRED_PRICES.items()) + ")"])


SUSB = "https://www2.census.gov/programs-surveys/susb/tables/2022/"


def census_susb():
    """Employer firms, establishments, jobs and receipts by enterprise size, 2022: the US by detailed size class and
    every sector's total, under-500 and 20,000+ rows (Statistics of US Businesses)."""
    import openpyxl

    out = []
    wb = openpyxl.load_workbook(io.BytesIO(_get(SUSB + "us_state_naics_detailedsizes_2022.xlsx")), read_only=True)
    for r in wb.worksheets[0].iter_rows(values_only=True):
        if r and r[0] == "00" and r[2] == "--":
            out.append(["--", "Total", r[4], r[5], r[6], r[7], r[11]])
        elif r and r[0] not in ("00", "State", None) and len(out) > 5:
            break
    wb = openpyxl.load_workbook(io.BytesIO(_get(SUSB + "us_naicssector_large_emplsize_2022.xlsx")), read_only=True)
    for r in wb.worksheets[0].iter_rows(values_only=True):
        if r and r[0] not in ("NAICS", None) and (r[2] in ("01: Total", "02: <500 employees", "11: 20,000+ employees")
                                                  and (r[0] != "--" or r[2].startswith("11"))):
            out.append([r[0], r[1], r[2], r[3], r[4], r[5], r[9]])
    return _write("census_susb_2022", ["naics", "sector", "size", "firms", "establishments", "employment",
                                       "receipts_k"], out,
                  [SUSB + "us_state_naics_detailedsizes_2022.xlsx and us_naicssector_large_emplsize_2022.xlsx "
                          "(Statistics of US Businesses, 2022, released 2025-04-10; receipts in $1,000)"])


DAMODARAN = "https://pages.stern.nyu.edu/~adamodar/pc/"


def damodaran_roc():
    """Aswath Damodaran's 'EVA' tables for US industries: number of firms, return on capital, cost of capital and book
    capital.  Each table is published in January for the year before: the archive's EVA15.xls (updated 5 January 2016)
    holds 2015, and so on to EVA24.xls; the current file (updated 7 January 2026) holds 2025.  ``year`` is the year
    the figures describe.  Industries are his; their names are stable from 2015."""
    import xlrd

    files = {y: DAMODARAN + f"archives/EVA{y % 100:02d}.xls" for y in range(2015, 2025)}
    files[2025] = DAMODARAN + "datasets/EVA.xls"
    out = []
    for year, url in files.items():
        book = xlrd.open_workbook(file_contents=_get(url))
        sheet = book.sheet_by_index(book.nsheets - 1)
        cols = None
        for r in range(sheet.nrows):
            row = [str(sheet.cell_value(r, c)).strip() for c in range(sheet.ncols)]
            if cols is None:
                if row and row[0].lower().startswith("industry"):
                    cols = {k: row.index(k) for k in row if k}
                continue
            if not row[0] or row[0].lower().startswith(("total market", "total")):
                continue
            def val(name):
                key = next((k for k in cols if k.startswith(name)), None)
                v = sheet.cell_value(r, cols[key]) if key else ""
                return v if isinstance(v, float) else ""
            out.append([year, row[0], val("Number of Firms"), val("ROC"), val("Cost of Capital"), val("BV of Capital")])
    return _write("damodaran_roc", ["year", "name", "firms", "roc", "wacc", "capital_musd"], out,
                  [DAMODARAN + "archives/EVA15.xls ... EVA24.xls (years 2015-2024) and datasets/EVA.xls (2025, "
                   "published January 2026): Aswath Damodaran, NYU Stern, 'Excess Returns (EVA) by industry, US "
                   "companies'"])


ECN = "https://www2.census.gov/programs-surveys/economic-census/data/2022/API_Datasets/ECNSIZE2022.zip"


def census_conc():
    """2022 Economic Census, concentration of the largest firms: for every six-digit NAICS industry with a published
    figure, the share of sales of its 4, 8, 20 and 50 largest firms, the number of firms and total sales ($1,000)."""
    z = zipfile.ZipFile(io.BytesIO(_get(ECN)))
    name = next(n for n in z.namelist() if n.endswith(".dat"))
    rows = {}
    with z.open(name) as f:
        reader = csv.reader(io.TextIOWrapper(f, encoding="latin-1"), delimiter="|")
        hdr = next(reader)
        hdr[0] = hdr[0].lstrip("#")
        for x in reader:
            d = dict(zip(hdr, x))
            code = d["NAICS2022"]
            if d["GEOTYPE"] != "01" or len(code) != 6 or not code.isdigit() or d["TYPOP"] != "00":
                continue
            if any(d[k] != "001" for k in ("EMPSZFE", "EMPSZFF", "LFO", "RCPSZFE", "RCPSZFF", "SUMUFI")):
                continue  # only the all-firms, all-sizes row of each industry
            r = rows.setdefault(code, {"label": d["NAICS2022_LABEL"]})
            if d["CONCENFI"] == "001":
                r["firms"], r["sales_k"] = d["FIRM"], d["RCPTOT"]
            elif d["CONCENFI"] in ("604", "608", "620", "650") and d["VAL_PCT"] not in ("", "0"):
                r[d["CONCENFI"]] = d["VAL_PCT"]
    out = [[c, r["label"], r.get("firms", ""), r.get("sales_k", ""), r["604"], r.get("608", ""), r.get("620", ""),
            r.get("650", "")] for c, r in sorted(rows.items()) if "604" in r]
    return _write("census_conc_2022", ["code", "name", "firms", "sales_k", "cr4", "cr8", "cr20", "cr50"], out,
                  [ECN + " (2022 Economic Census, Selected Sectors: Concentration of Largest Firms for the U.S., "
                         "released 2025-04-24; shares in percent of sales, value of shipments or revenue)"])


FRED_MARKET = {"AIES312112RCTUS": "Bottled water manufacturing: shipments (thousands of dollars; Census AIES)",
               "AIES312112EMPUS": "Bottled water manufacturing: employees (Census AIES)",
               "PCU312112312112": "Producer price index: bottled water manufacturing (index)",
               "POPTHM": "US population (thousands, monthly average)",
               "ECOMPCTSA": "E-commerce retail sales as a percent of total retail sales (Census, quarterly, seasonally "
                            "adjusted)",
               "TTLHH": "US households (thousands; Census Bureau, Current Population Survey)"}


def fred_market():
    """Annual series for sizing a market (Part 7): the Census Bureau's shipments and employment of US bottled water
    manufacturers, the producer price index of bottled water, the US population, e-commerce's share of retail sales and
    the number of US households (FRED)."""
    out = []
    for sid in FRED_MARKET:
        txt = _get(f"https://fred.stlouisfed.org/graph/fredgraph.csv?id={sid}&fq=Annual&fam=avg").decode()
        for line in txt.splitlines()[1:]:
            d, v = line.split(",")
            if v not in (".", ""):
                out.append([sid, int(d[:4]), float(v)])
    return _write("fred_market", ["series", "year", "value"], out,
                  ["https://fred.stlouisfed.org (annual averages; " + "; ".join(f"{k} {v}" for k, v in FRED_MARKET.items())
                   + ")"])


def owid_tech():
    """The share of US households (or people) using each of some forty technologies, year by year, as compiled by
    Our World in Data from Comin and Hobijn (2004) and later sources (CC BY 4.0)."""
    txt = _get("https://ourworldindata.org/grapher/technology-adoption-by-households-in-the-united-states.csv"
               "?v=1&csvType=full&useColumnShortNames=true").decode()
    rows = []
    for k, line in enumerate(txt.splitlines()):
        if k == 0:
            continue
        name, year, val = line.rsplit(",", 2)
        if val not in ("", "."):
            rows.append([name.strip('"'), int(year), float(val)])
    return _write("owid_tech", ["name", "year", "share"], rows,
                  ["https://ourworldindata.org/grapher/technology-adoption-by-households-in-the-united-states "
                   "(Comin and Hobijn (2004) and others, via Our World in Data; CC BY 4.0; percent of households)"])


SEC_QUARTERLY = [(723125, "MU"), (50863, "INTC")]


def sec_quarterly():
    """Quarterly revenue and operating income from Forms 10-Q and 10-K (SEC company facts): three-month values as
    filed (the latest filing wins), and each fiscal year's fourth quarter as the year less its first three quarters."""
    import time

    out = []
    for cik, tic in SEC_QUARTERLY:
        facts = json.loads(_get(f"https://data.sec.gov/api/xbrl/companyfacts/CIK{cik:010d}.json"))["facts"]["us-gaap"]
        time.sleep(0.5)
        rows: dict = {}
        for item, tags in (("revenue", SEC_ITEMS["revenue"]), ("operating_income", ["OperatingIncomeLoss"])):
            q: dict = {}
            ann: dict = {}
            for tag in tags:
                for v in facts.get(tag, {}).get("units", {}).get("USD", []):
                    if "start" not in v or v.get("form") not in ("10-Q", "10-K", "10-Q/A", "10-K/A"):
                        continue
                    d = (dt.date.fromisoformat(v["end"]) - dt.date.fromisoformat(v["start"])).days
                    if 80 <= d <= 100 and (v["end"] not in q or v["filed"] > q[v["end"]][1]):
                        q[v["end"]] = (v["val"] / 1e9, v["filed"])
                    elif 350 <= d <= 380 and (v["end"] not in ann or v["filed"] > ann[v["end"]][2]):
                        ann[v["end"]] = (v["val"] / 1e9, v["start"], v["filed"])
            for end, (val, start, _) in ann.items():
                inside = [x[0] for e, x in q.items() if start < e < end]
                if end not in q and len(inside) == 3:
                    q[end] = (val - sum(inside), "derived")
            for end, (val, how) in q.items():
                rows.setdefault(end, {})[item] = (val, how == "derived")
        for end in sorted(rows):
            r = rows[end]
            rv, oi = r.get("revenue", (None,))[0], r.get("operating_income", (None,))[0]
            out.append([tic, end, None if rv is None else round(rv, 4), None if oi is None else round(oi, 4),
                        int(any(x[1] for x in r.values() if len(x) > 1))])
    return _write("sec_quarterly", ["ticker", "quarter_end", "revenue", "operating_income", "q4_derived"], out,
                  ["https://data.sec.gov/api/xbrl/companyfacts/ (Forms 10-Q and 10-K; US$ billions; three-month "
                   "values; a fiscal fourth quarter is the year less its first three, marked q4_derived)"])


FRED_CYCLE = {"M04008US16980M275NNBR": "Wholesale price of hogs, Chicago (dollars per 100 lb, NBER)",
              "M01038US16980M562NNBR": "Live hog receipts, Chicago (thousands, NBER)",
              "M01039USM566NNBR": "Hogs slaughtered, United States (thousands, NBER)",
              "HOUST": "Housing starts, total (thousands, annual rate, SA)",
              "UNDCONTSA": "New privately owned housing units under construction (thousands, SA)",
              "COMPUTSA": "Housing units completed (thousands, annual rate, SA)",
              "MSACSR": "Monthly supply of new houses (months, SA)",
              "DCOILWTICO": "Crude oil, West Texas Intermediate (dollars a barrel, monthly average)",
              "RSXFS": "Retail sales excluding food services (millions of dollars, SA)",
              "AMTMNO": "Manufacturers' new orders, total manufacturing (millions of dollars, SA)",
              "IPG3344S": "Industrial production: semiconductors and related components (index, SA)",
              "IPG3361T3S": "Industrial production: motor vehicles and parts (index, SA)",
              "CUSR0000SETA02": "Consumer price index: used cars and trucks (index, SA)"}


def fred_cycle():
    """Monthly series for the cycle (Part 6): the NBER's hog prices and numbers from 1858, housing starts and the
    houses under construction, completed and for sale, oil, retail sales and factory orders (FRED)."""
    out = []
    for sid in FRED_CYCLE:
        txt = _get(f"https://fred.stlouisfed.org/graph/fredgraph.csv?id={sid}&fq=Monthly&fam=avg").decode()
        for line in txt.splitlines()[1:]:
            d, v = line.split(",")
            if v not in (".", ""):
                out.append([sid, d[:7], float(v)])
    return _write("fred_cycle", ["series", "month", "value"], out,
                  ["https://fred.stlouisfed.org (monthly; " + "; ".join(f"{k} {v}" for k, v in FRED_CYCLE.items()) +
                   ")"])


MAERSK_LEI = "549300D2K6PKKKXVNN73"
MAERSK_FILINGS = ["2020-12-31/ESEF/DK/0/549300D2K6PKKKXVNN73-2020-12-31_en", "2022-12-31/ESEF/DK/0/APMM-2022-12-31-en",
                  "2024-12-31/ESEF/DK/0/APMM-2024-12-31-en", "2025-12-31/ESEF/DK/0/APMM-2025-12-31-en"]
MAERSK_ITEMS = {"revenue": "ifrs-full:Revenue", "ebit": "ifrs-full:ProfitLossFromOperatingActivities",
                "depreciation": "ifrs-full:DepreciationAmortisationAndImpairmentLossReversalOfImpairmentLossRecognised"
                                "InProfitOrLoss"}


def esef_maersk():
    """A.P. Moller - Maersk's group revenue, operating profit (EBIT) and depreciation for each calendar year, 2019-2025,
    from its annual reports' ESEF (inline XBRL) filings as converted to xBRL-JSON by filings.xbrl.org."""
    vals: dict = {}
    for f in MAERSK_FILINGS:
        facts = json.loads(_get(f"https://filings.xbrl.org/{MAERSK_LEI}/{f}.json"))["facts"]
        for fact in facts.values():
            dim = fact.get("dimensions", {})
            item = next((k for k, c in MAERSK_ITEMS.items() if dim.get("concept") == c), None)
            per = dim.get("period", "")
            if item is None or len(dim) > 4 or "/" not in per:
                continue
            a, b = per.split("/")
            if a[5:10] == "01-01" and b[5:10] == "01-01" and int(b[:4]) - int(a[:4]) == 1:
                vals.setdefault(int(a[:4]), {})[item] = float(fact["value"]) / 1e9
    rows = [[y] + [vals[y].get(k) for k in MAERSK_ITEMS] for y in sorted(vals)]
    return _write("esef_maersk", ["year"] + list(MAERSK_ITEMS), rows,
                  ["https://filings.xbrl.org/ (A.P. Moller - Maersk A/S annual reports 2020, 2022, 2024, 2025, ESEF; "
                   "US$ billions; " + "; ".join(f"{k}: {v}" for k, v in MAERSK_ITEMS.items()) + ")"])



# --- Part 8, oil and gas: EIA's bulk files (no key needed), its gasoline price components, FRED's energy prices ----
EIA_PET = {"PET.MCRFPUS1.A": "US field production of crude oil (thousand barrels, annual)",
           "PET.MCRFPUS2.M": "US field production of crude oil (thousand barrels a day, monthly)",
           "PET.MCRFPTX2.M": "Texas field production of crude oil (thousand barrels a day)",
           "PET.MCRFPND2.M": "North Dakota field production of crude oil (thousand barrels a day)",
           "PET.MCRFP3FM2.M": "Federal offshore Gulf of Mexico (Gulf of America) production of crude oil (thousand b/d)",
           "PET.E_ERTRRO_XR0_NUS_C.M": "US crude oil rotary rigs in operation (Baker Hughes, monthly average)",
           "PET.MCRSTUS1.M": "US ending stocks of crude oil, SPR included (thousand barrels)",
           "PET.RWTC.M": "WTI spot price, Cushing (dollars a barrel)",
           "PET.RBRTE.M": "Brent spot price, Europe (dollars a barrel)",
           "PET.EER_EPMRU_PF4_Y35NY_DPG.M": "New York Harbor conventional gasoline, regular, spot (dollars a gallon)",
           "PET.EER_EPD2F_PF4_Y35NY_DPG.M": "New York Harbor No. 2 heating oil, spot (dollars a gallon)",
           "PET.EMM_EPMR_PTE_NUS_DPG.M": "US regular gasoline, retail, all formulations (dollars a gallon)",
           "PET.MCREXUS2.A": "US exports of crude oil (thousand barrels a day)",
           "PET.MTTNTUS2.A": "US net imports of crude oil and petroleum products (thousand barrels a day)"}
EIA_INTL_AREAS = ["WORL", "OPEC", "OPNO", "USA", "SAU", "RUS", "IRQ", "IRN", "ARE", "KWT", "CAN", "CHN", "BRA", "NOR",
                  "GBR", "VEN", "MEX", "NGA", "KAZ", "QAT", "LBY", "AGO", "DZA", "GUY"]


def _eia_bulk(name: str, keep):
    """Series from one of EIA's bulk files (https://api.eia.gov/bulk/NAME.zip): JSON lines, one series each."""
    import io
    import zipfile

    z = zipfile.ZipFile(io.BytesIO(_get(f"https://api.eia.gov/bulk/{name}.zip")))
    out = {}
    with z.open(z.namelist()[0]) as f:
        for line in f:
            d = json.loads(line)
            if keep(d.get("series_id", "")):
                out[d["series_id"]] = d
    return out


def eia_petroleum():
    """US crude production (annual since 1859, monthly since 1920; Texas, North Dakota, the Gulf), oil rigs, crude
    stocks, crude and product spot prices, retail gasoline and trade, from EIA's petroleum bulk file."""
    got = _eia_bulk("PET", lambda sid: sid in EIA_PET)
    rows = []
    for sid in EIA_PET:
        for per, v in sorted(got[sid]["data"]):
            if v is not None:
                rows.append([sid.split(".")[1], per[:4] + ("-" + per[4:6] if len(per) >= 6 else ""), v])
    return _write("eia_petroleum", ["series", "period", "value"], rows,
                  ["https://api.eia.gov/bulk/PET.zip (US Energy Information Administration; " +
                   "; ".join(f"{k.split('.')[1]} {v}" for k, v in EIA_PET.items()) + ")"])


def eia_intl():
    """Crude oil (with lease condensate) production by country and group, 1973-2025, and world consumption of
    petroleum and other liquids, thousand barrels a day, from EIA's international bulk file."""
    want = {f"INTL.57-1-{a}-TBPD.A" for a in EIA_INTL_AREAS} | {"INTL.5-2-WORL-TBPD.A"}
    got = _eia_bulk("INTL", lambda sid: sid in want)
    rows = []
    for sid in sorted(got):
        what = "consumption" if sid.startswith("INTL.5-2") else "crude_production"
        area = sid.split("-")[2]
        for per, v in sorted(got[sid]["data"]):
            if v not in (None, "NA", "--"):
                try:
                    rows.append([area, what, int(per), round(float(v), 1)])
                except ValueError:
                    continue
    return _write("eia_intl", ["area", "series", "year", "kbd"], rows,
                  ["https://api.eia.gov/bulk/INTL.zip (US Energy Information Administration, International Energy "
                   "Statistics; crude oil including lease condensate production, and petroleum and other liquids "
                   "consumption, thousand barrels a day)"])


def eia_pump():
    """What a gallon of US regular gasoline paid for, month by month: the retail price and the shares of crude oil,
    refining, distribution and marketing, and taxes (EIA, Gasoline Pump Components History)."""
    import html as _html
    import re

    t = _get("https://www.eia.gov/petroleum/gasdiesel/gaspump_hist.php").decode("utf-8", "ignore")
    cells = [_html.unescape(re.sub(r"<[^>]+>", "", c)).strip() for c in re.findall(r"<td[^>]*>(.*?)</td>", t, re.S)]
    rows = []
    mon = {m: k + 1 for k, m in enumerate(["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov",
                                           "Dec"])}
    for k in range(len(cells) - 5):
        m = re.fullmatch(r"([A-Za-z]{3})[a-z]*-(\d\d)", cells[k])
        if m and m.group(1) in mon:
            try:
                vals = [float(c) for c in cells[k + 1:k + 6]]
            except ValueError:
                continue
            rows.append([f"20{m.group(2)}-{mon[m.group(1)]:02d}"] + vals)
    rows.sort()
    return _write("eia_pump", ["month", "retail", "refining_pct", "distribution_pct", "taxes_pct", "crude_pct"], rows,
                  ["https://www.eia.gov/petroleum/gasdiesel/gaspump_hist.php (EIA, Gasoline Pump Components History: "
                   "US regular gasoline, dollars a gallon, and each component's percentage)"])


EIA_GAS = {"N9133US2": "Liquefied US natural gas exports (million cubic feet, annual)",
           "N9070US2": "US dry natural gas production (million cubic feet, annual)"}


def eia_gas():
    """US LNG exports and dry gas production by year, from EIA's natural gas history workbooks (dnav)."""
    import xlrd

    rows = []
    for sid in EIA_GAS:
        b = xlrd.open_workbook(file_contents=_get(f"https://www.eia.gov/dnav/ng/hist_xls/{sid}a.xls"))
        sh = b.sheet_by_name("Data 1")
        for i in range(3, sh.nrows):
            d, v = sh.cell_value(i, 0), sh.cell_value(i, 1)
            if v not in ("", None):
                rows.append([sid, xlrd.xldate_as_tuple(d, b.datemode)[0], float(v)])
    return _write("eia_gas", ["series", "year", "mmcf"], rows,
                  ["https://www.eia.gov/dnav/ng/hist_xls/ (US Energy Information Administration; " +
                   "; ".join(f"{k} {v}" for k, v in EIA_GAS.items()) + ")"])


FRED_ENERGY = {"WTISPLC": "Spot crude oil price: West Texas Intermediate (dollars a barrel, monthly, since 1946)",
               "MHHNGSP": "Henry Hub natural gas spot price (dollars per million Btu)",
               "PNGASEUUSDM": "Global price of natural gas, EU (IMF; dollars per million Btu)",
               "PNGASJPUSDM": "Global price of LNG, Asia (IMF; dollars per million Btu)",
               "CPIAUCSL": "Consumer price index, all urban consumers (index 1982-84 = 100, SA)"}


def fred_energy():
    """Monthly energy prices for Part 8: WTI since 1946, Henry Hub, European gas and Asian LNG (IMF), and the CPI to
    put old prices in today's dollars (FRED)."""
    out = []
    for sid in FRED_ENERGY:
        txt = _get(f"https://fred.stlouisfed.org/graph/fredgraph.csv?id={sid}&fq=Monthly&fam=avg").decode()
        for line in txt.splitlines()[1:]:
            d, v = line.split(",")
            if v not in (".", ""):
                out.append([sid, d[:7], float(v)])
    return _write("fred_energy", ["series", "month", "value"], out,
                  ["https://fred.stlouisfed.org (monthly; " + "; ".join(f"{k} {v}" for k, v in FRED_ENERGY.items()) + ")"])



# --- Part 9, mining and metals: USGS's historical statistics, the IMF's metal prices, miners' 20-F filings ----------
DS140 = {"chromium": "ds140-chromium-2022", "copper": "ds140-copper-2020", "nickel": "ds140-nickel-2019",
         "tin": "ds140-tin-2021", "tungsten": "ds140-tungsten-2019"}
DS140_BASE = "https://d9-wret.s3.us-west-2.amazonaws.com/assets/palladium/production/s3fs-public/media/files/"


def usgs_ds140():
    """US Geological Survey, Data Series 140 (historical statistics for mineral commodities in the United States): the
    unit value of each of the five metals of Simon and Ehrlich's 1980 wager, in dollars of the year and of 1998, and
    world production, every year since 1900."""
    import io

    import openpyxl

    rows = []
    for metal, f in DS140.items():
        wb = openpyxl.load_workbook(io.BytesIO(_get(DS140_BASE + f + ".xlsx")), data_only=True, read_only=True)
        ws = wb[wb.sheetnames[0]]
        data = list(ws.iter_rows(values_only=True))
        hi = next(i for i, r in enumerate(data) if any(isinstance(c, str) and "Unit value" in c for c in r if c))
        hdr = [str(c or "").replace("\n", " ") for c in data[hi]]
        cn = next(i for i, h in enumerate(hdr) if "Unit value" in h and "98" not in h)
        cr = next(i for i, h in enumerate(hdr) if "Unit value" in h and "98" in h)
        cw = next(i for i, h in enumerate(hdr) if "World production" in h)

        def num(v):
            return float(v) if isinstance(v, (int, float)) else None
        for r in data[hi + 1:]:
            if isinstance(r[0], (int, float)) and 1800 < r[0] < 2100:
                rows.append([metal, int(r[0]), num(r[cn]), num(r[cr]), num(r[cw])])
    return _write("usgs_ds140", ["metal", "year", "unit_value", "unit_value_98", "world_production"], rows,
                  ["https://www.usgs.gov/centers/national-minerals-information-center/historical-statistics-mineral-and-"
                   "material-commodities (USGS Data Series 140; " + ", ".join(f + ".xlsx" for f in DS140.values()) +
                   "; unit value in dollars a metric ton of apparent consumption, and in 1998 dollars by the CPI; world "
                   "production in metric tons)"])


FRED_METALS = {"PCOPPUSDM": "Copper, grade A cathode, LME (IMF; dollars a metric ton)",
               "PIORECRUSDM": "Iron ore, China import, 62% Fe (IMF; dollars a dry metric ton)",
               "PNICKUSDM": "Nickel, LME (IMF; dollars a metric ton)",
               "PALUMUSDM": "Aluminum, LME (IMF; dollars a metric ton)",
               "PZINCUSDM": "Zinc, LME (IMF; dollars a metric ton)",
               "PTINUSDM": "Tin, LME (IMF; dollars a metric ton)"}


def fred_metals():
    """The IMF's monthly metal prices since 1992 (via FRED): copper, iron ore, nickel, aluminium, zinc and tin."""
    out = []
    for sid in FRED_METALS:
        txt = _get(f"https://fred.stlouisfed.org/graph/fredgraph.csv?id={sid}&fq=Monthly&fam=avg").decode()
        for line in txt.splitlines()[1:]:
            d, v = line.split(",")
            if v not in (".", ""):
                out.append([sid, d[:7], float(v)])
    return _write("fred_metals", ["series", "month", "value"], out,
                  ["https://fred.stlouisfed.org (IMF Primary Commodity Prices, monthly; " +
                   "; ".join(f"{k} {v}" for k, v in FRED_METALS.items()) + ")"])


IFRS_COMPANIES = [(811809, "BHP"), (863064, "RIO"), (917851, "VALE")]
IFRS_ITEMS = {"revenue": ["Revenue"], "profit": ["ProfitLossAttributableToOwnersOfParent", "ProfitLoss"],
              "operating_cash": ["CashFlowsFromUsedInOperatingActivities"],
              "capex": ["PurchaseOfPropertyPlantAndEquipmentClassifiedAsInvestingActivities"]}


def sec_ifrs():
    """Annual figures of the three big diversified miners from their Forms 20-F (SEC company facts, IFRS tags): BHP's
    fiscal years end in June, Rio Tinto's and Vale's in December."""
    import time

    out = []
    for cik, tic in IFRS_COMPANIES:
        facts = json.loads(_get(f"https://data.sec.gov/api/xbrl/companyfacts/CIK{cik:010d}.json"))["facts"]
        ifrs = facts.get("ifrs-full", {})
        time.sleep(0.5)
        years: dict = {}
        for item, tags in IFRS_ITEMS.items():
            for tag in tags:
                best: dict = {}
                for v in ifrs.get(tag, {}).get("units", {}).get("USD", []):
                    if v.get("form") not in ("20-F", "20-F/A") or "start" not in v:
                        continue
                    d = (dt.date.fromisoformat(v["end"]) - dt.date.fromisoformat(v["start"])).days
                    if not 350 <= d <= 380:
                        continue
                    if v["end"] not in best or v["filed"] > best[v["end"]]["filed"]:
                        best[v["end"]] = v
                for end, v in best.items():
                    years.setdefault(end, {}).setdefault(item, v["val"] / 1e9)
        for end in sorted(years):
            out.append([tic, end] + [years[end].get(k) for k in IFRS_ITEMS])
    return _write("sec_ifrs", ["ticker", "year_end"] + list(IFRS_ITEMS), out,
                  ["https://data.sec.gov/api/xbrl/companyfacts/ (Forms 20-F, IFRS; US$ billions; tags: " +
                   "; ".join(f"{k}: {'/'.join(v)}" for k, v in IFRS_ITEMS.items()) + ")"])



NE_LAND = "https://raw.githubusercontent.com/nvkelso/natural-earth-vector/master/geojson/ne_110m_land.geojson"


def ne_land():
    """Natural Earth's 1:110m land outlines (public domain) for the series' schematic world map (``draw.world_map``):
    Antarctica and polygons smaller than two square degrees dropped, coordinates rounded to a tenth of a degree."""
    g = json.loads(_get(NE_LAND))
    polys = []
    for f in g["features"]:
        geom = f["geometry"]
        for poly in ([geom["coordinates"]] if geom["type"] == "Polygon" else geom["coordinates"]):
            ring = poly[0]
            xs, ys = [q[0] for q in ring], [q[1] for q in ring]
            if max(ys) < -60:
                continue
            if 0.5 * abs(sum(xs[i] * ys[i + 1] - xs[i + 1] * ys[i] for i in range(len(ring) - 1))) < 2.0:
                continue
            pts = [[round(q[0], 1), round(q[1], 1)] for q in ring]
            polys.append([pts[0]] + [q for a, q in zip(pts, pts[1:]) if q != a])
    path = HERE / "world_land.json"
    path.write_text(json.dumps({"source": "Natural Earth, 1:110m land (public domain), naturalearthdata.com, via " +
                                NE_LAND + "; polygons smaller than 2 square degrees and Antarctica dropped, coordinates "
                                "rounded to 0.1 degree", "retrieved": TODAY, "polygons": polys}, separators=(",", ":")))
    return path


ERS = "https://www.ers.usda.gov/media/"
ERS_FOOD_DOLLAR = ERS + "7052/food-dollar-nominal-data-in-machine-readable-format.zip"
ERS_FOOD_DOLLAR_OLD = ERS + "7055/food-dollar-nominal-data-2011-model-1993-2023.csv"


def ers_food_dollar():
    """USDA ERS's food dollar: where a dollar spent on food in the US goes.  The new Ag-FEDS model (released November
    2026, 2007-2025): the farm and marketing shares for all food, food at home and food away from home, and the bill of
    thirteen industry groups for all food, in cents per domestic food dollar and in millions; and the farm share from
    the 2011 model (1993-2023), which ERS says is not directly comparable."""
    z = zipfile.ZipFile(io.BytesIO(_get(ERS_FOOD_DOLLAR)))
    name = next(n for n in z.namelist() if n.endswith(".csv"))
    rows = csv.DictReader(io.StringIO(z.read(name).decode("utf-8-sig")))
    out = []
    for r in rows:
        if r["Type"] != "Food" or r["ValueTypeDesc"] != "Total":
            continue
        top = (r["Aggregation"] == "Type total" and r["Channel"] == "All") or r["Aggregation"] == "Channel total"
        if not top or r["Series"] not in ("Marketing bill", "Industry group bill", "Total spending by production source",
                                          "Industry group total"):
            continue
        unit = "cents" if r["Unit"].startswith("Cents") else "usd_m"
        try:
            v = float(r["Value"])
        except ValueError:
            continue
        out.append(["agfeds", int(r["Year"]), r["Channel"], r["Series"], r["CategoryName"], unit, v])
    old = csv.DictReader(io.StringIO(_get(ERS_FOOD_DOLLAR_OLD).decode("utf-8-sig")))
    for r in old:
        if r["Table_name"] == "Food dollar" and r["Category_desc"] in ("Farm production", "Total") and \
                r["Units"].startswith("Cents"):
            try:
                out.append(["model2011", int(r["Year"]), "All", "Industry group bill", r["Category_desc"], "cents",
                            float(r["Total"])])
            except ValueError:
                continue
    out.sort(key=lambda q: (q[0], q[1], q[2], q[3], q[4], q[5]))
    return _write("ers_food_dollar", ["model", "year", "channel", "series", "category", "unit", "value"], out,
                  [ERS_FOOD_DOLLAR, ERS_FOOD_DOLLAR_OLD])


ERS_COSTS = {"corn": ERS + "4962/corn.csv", "soybeans": ERS + "4976/soybeans.csv", "wheat": ERS + "4978/wheat.csv"}


def ers_costs():
    """USDA ERS's commodity costs and returns for corn, soybeans and wheat, US total, every item a year (dollars per
    planted acre, and the yield, price and size that go with them)."""
    out = []
    for crop, url in ERS_COSTS.items():
        for r in csv.DictReader(io.StringIO(_get(url).decode("utf-8-sig"))):
            if r["Region"] != "U.S. total" or r["Size"] != "No specific size":
                continue
            try:
                v = float(r["Value"])
            except ValueError:
                continue
            out.append([crop, int(r["Year"]), r["Category"].strip(), r["Item"].strip(), r["Units"].strip(), v])
    out.sort(key=lambda q: (q[0], q[1], q[2], q[3]))
    return _write("ers_costs", ["crop", "year", "category", "item", "units", "value"], out, list(ERS_COSTS.values()))


ERS_FIWS = ERS + "29517/september-3-2026-release.zip"
FIWS_KEEP = ("Net farm income", "Net cash farm income", "Gross cash income", "Cash receipts value, all commodities",
             "Value of government payments, total", "Dec. 31 value of real estate assets, excl. operator dwellings",
             "Dec. 31 value of farm assets, excl. operator dwellings", "Dec. 31 value of farm debt, all, excl.",
             "Dec. 31 value of farm equity, all", "Intermediate product expenses, fertilizer",
             "Rate of return on farm assets", "Net rent, nonoperator landlords, incl.")


def ers_farm_income():
    """USDA ERS's farm income and wealth statistics (release of 3 September 2026), US totals since 1910 for a few lines
    of the farm sector's accounts, in thousands of dollars, with the GDP deflator ERS supplies (2026 = 100)."""
    z = zipfile.ZipFile(io.BytesIO(_get(ERS_FIWS)))
    name = next(n for n in z.namelist() if n.lower().endswith(".csv"))
    out = []
    for r in csv.DictReader(io.StringIO(z.read(name).decode("latin-1"))):
        d = (r.get("VariableDescriptionTotal") or "").strip()
        if r.get("State") != "US" or not any(d.startswith(k) for k in FIWS_KEEP):
            continue
        try:
            v = float(r["Amount"])
            defl = float(r["ChainType_GDP_Deflator"]) if r.get("ChainType_GDP_Deflator") not in (None, "", "NA") else None
        except ValueError:
            continue
        out.append([d, int(r["Year"]), v, defl])
    out.sort(key=lambda q: (q[0], q[1]))
    return _write("ers_farm_income", ["variable", "year", "value_kusd", "gdp_deflator"], out, [ERS_FIWS])


OWID_AG = {"wheat-yields": "wheat_yield", "maize-yields": "maize_yield", "rice-yields": "rice_yield",
           "daily-per-capita-caloric-supply": None, "cereal-production": None}
OWID_ENTITIES = ("World", "India", "Mexico", "Pakistan", "United States", "China", "Brazil", "Africa", "Nigeria",
                 "Ethiopia", "Bangladesh", "Indonesia")


def owid_ag():
    """Our World in Data's crop yields, food supply per person and cereal output (from FAOSTAT), for a few countries
    and the world, every year (CC BY 4.0)."""
    out = []
    for slug in OWID_AG:
        txt = _get(f"https://ourworldindata.org/grapher/{slug}.csv?v=1&csvType=full&useColumnShortNames=true").decode()
        rows = list(csv.reader(io.StringIO(txt)))
        head = rows[0]
        col = len(head) - 1
        for r in rows[1:]:
            if r[0] in OWID_ENTITIES and r[col] not in ("", None):
                out.append([slug, r[0], int(r[2]), float(r[col])])
    return _write("owid_ag", ["series", "entity", "year", "value"], out,
                  ["https://ourworldindata.org/grapher/" + s for s in OWID_AG])


FRED_FOOD = {"PWHEAMTUSDM": "wheat ($/t)", "PMAIZMTUSDM": "maize ($/t)", "PSOYBUSDM": "soybeans ($/t)",
             "PRICENPQUSDM": "rice ($/t)", "PCOCOUSDM": "cocoa ($/t)", "PCOFFOTMUSDM": "coffee, other milds (c/lb)",
             "PBEEFUSDM": "beef (c/lb)", "PPOILUSDM": "palm oil ($/t)", "PSUGAISAUSDM": "sugar (c/lb)",
             "PCU325311325311": "PPI, nitrogenous fertilizer manufacturing (Dec 1979 = 100)",
             "PSMEAUSDM": "soybean meal ($/t)", "PSOILUSDM": "soybean oil ($/t)",
             "APU0000702111": "white bread, a pound (US city average, $)", "APU0000703112": "ground beef, a pound ($)",
             "APU0000708111": "eggs, a dozen ($)", "CUSR0000SAF11": "CPI food at home (1982-84 = 100)",
             "CPIAUCSL": "CPI, all items (1982-84 = 100)"}


def fred_food():
    """Monthly food and fertilizer prices: the IMF's world prices of grains, oilseeds, cocoa, coffee, beef, palm oil,
    sugar, urea and potash, the BLS's average retail prices of bread, ground beef and eggs, and the CPI for food at
    home and all items, via FRED."""
    out = []
    for sid in FRED_FOOD:
        txt = _get(f"https://fred.stlouisfed.org/graph/fredgraph.csv?id={sid}").decode()
        for line in txt.splitlines()[1:]:
            parts = line.split(",")
            if len(parts) == 2 and parts[1] not in (".", ""):
                try:
                    out.append([sid, parts[0][:7], float(parts[1])])
                except ValueError:
                    continue
    return _write("fred_food", ["series", "month", "value"], out,
                  ["https://fred.stlouisfed.org (" + "; ".join(f"{k} {v}" for k, v in FRED_FOOD.items()) + ")"])


JOBS = {"ers_food_dollar": ers_food_dollar, "ers_costs": ers_costs, "ers_farm_income": ers_farm_income, "owid_ag": owid_ag, "fred_food": fred_food, "ne_land": ne_land, "usgs_ds140": usgs_ds140, "fred_metals": fred_metals, "sec_ifrs": sec_ifrs, "eia_gas": eia_gas, "eia_petroleum": eia_petroleum, "eia_intl": eia_intl, "eia_pump": eia_pump, "fred_energy": fred_energy, "fred_market": fred_market, "owid_tech": owid_tech, "sec_quarterly": sec_quarterly, "fred_cycle": fred_cycle, "esef_maersk": esef_maersk, "damodaran_roc": damodaran_roc, "census_conc": census_conc, "eia_power": eia_power, "fred_pay": fred_pay, "bea_real": bea_real, "sec_annual": sec_annual, "fred_prices": fred_prices, "census_susb": census_susb, "bea_va": bea_va, "wb_mfg_usd": wb_mfg_usd, "bea_hist": bea_hist, "bea_io": bea_io, "fred_jobs": fred_jobs, "wb_shares": wb_shares}

if __name__ == "__main__":
    names = list(JOBS) if "--all" in sys.argv else sys.argv[1:]
    for n in names:
        print("wrote", JOBS[n]())
