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
                 (1103982, "MDLZ"), (47111, "HSY"), (56873, "KR"),
                 (73309, "NUE"), (1022671, "STLD"), (764065, "CLF"), (1163302, "X"), (22444, "CMC"),
                 (849395, "CRH"), (2035989, "AMRZ"), (1396009, "VMC"), (916076, "MLM"), (918646, "EXP"),
                 (1675149, "AA"), (949157, "CENX"), (51434, "IP"), (2005951, "SW"), (75677, "PKG"), (9389, "BALL"),
                 (1219601, "CCK"), (812074, "OI"),
                 (1751788, "DOW"), (1489393, "LYB"), (1262823, "WLK"), (1707925, "LIN"), (2969, "APD"), (89800, "SHW"),
                 (31462, "ECL"), (79879, "PPG"), (915389, "EMN"), (1306830, "CE"), (1666700, "DD"), (1307954, "HUN"),
                 (74303, "OLN"), (51253, "IFF"), (1627223, "CC"),
                 (1326160, "DUK"), (92122, "SO"), (4904, "AEP"), (715957, "D"), (1109357, "EXC"), (72903, "XEL"),
                 (1047862, "ED"), (1004980, "PCG"), (1032208, "SRE"), (65984, "ETR"), (1692819, "VST"), (1868275, "CEG"),
                 (1013871, "NRG"), (874761, "AES"), (1996810, "GEV"),
                 (823768, "WM"), (1060391, "RSG"), (1318220, "WCN"), (911177, "CWST"), (822818, "CLH"),
                 (1410636, "AWK"), (78128, "WTRG"), (1056903, "AWR"), (1035201, "CWT"), (766829, "HTO"),
                 (1045810, "NVDA"), (1730168, "AVGO"), (2488, "AMD"), (804328, "QCOM"), (97476, "TXN"), (6951, "AMAT"),
                 (707549, "LRCX"), (6281, "ADI"), (319201, "KLAC"), (1835632, "MRVL"), (813672, "CDNS"), (883241, "SNPS"),
                 (1413447, "NXPI"), (827054, "MCHP"), (1097864, "ON"), (1047127, "AMKR"),
                 (320193, "AAPL"), (1571996, "DELL"), (47217, "HPQ"), (866374, "FLEX"), (898293, "JBL"), (897723, "SANM"),
                 (785786, "PLXS"), (863436, "BHE"), (1030894, "CLS"), (1375365, "SMCI"), (820313, "APH"), (24741, "GLW"),
                 (1385157, "TEL"), (1032975, "LOGI")]


# where a company's first-choice tag means something else: Mastercard tagged its gross revenue, before rebates and
# incentives to customers, as revenue from contracts in 2018-2021; its net revenue is "Revenues"
_UTIL = {"revenue": ["Revenues", "RevenueFromContractWithCustomerExcludingAssessedTax", "RegulatedAndUnregulatedOperatingRevenue"],
         "net_income": ["NetIncomeLoss", "NetIncomeLossAvailableToCommonStockholdersBasic"]}
SEC_OVERRIDES = {**{t: _UTIL for t in ("DUK", "SO", "AEP", "D", "EXC", "XEL", "ED", "PCG", "SRE", "ETR",
                                      "WTRG", "AWR", "HTO")},
                 # American Water tags its total operating revenue (with alternative revenue programmes) as
                 # RegulatedAndUnregulatedOperatingRevenue; California Water tags equity with its small
                 # non-controlling interests after 2020
                 "AWK": {"revenue": ["RegulatedAndUnregulatedOperatingRevenue",
                                     "RevenueFromContractWithCustomerExcludingAssessedTax"]},
                 "CWT": {"equity": ["StockholdersEquity",
                                    "StockholdersEquityIncludingPortionAttributableToNoncontrollingInterest"]},
                 # utilities: total revenue (Revenues) includes alternative revenue programmes; several tag profit to
                 # common shareholders rather than NetIncomeLoss in recent years
                 "MA": {"revenue": ["Revenues", "SalesRevenueNet",
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
                 "CF": {"net_income": ["NetIncomeLoss", "NetIncomeLossAvailableToCommonStockholdersBasic"]},
                 # US Steel tags part of its sales (2017-2021) as revenue from contracts; its total is Revenues.
                 # Commercial Metals, Ball and O-I tag revenue including the taxes they collect; Steel Dynamics and
                 # Ball tag profit to common shareholders, not NetIncomeLoss, in most years; Commercial Metals tags
                 # ProfitLoss before 2019
                 "X": {"revenue": ["Revenues", "SalesRevenueNet"]},
                 "CMC": {"revenue": ["RevenueFromContractWithCustomerIncludingAssessedTax", "Revenues",
                                     "SalesRevenueGoodsNet"], "net_income": ["NetIncomeLoss", "ProfitLoss"]},
                 "BALL": {"revenue": ["RevenueFromContractWithCustomerIncludingAssessedTax", "SalesRevenueNet"],
                          "net_income": ["NetIncomeLoss", "NetIncomeLossAvailableToCommonStockholdersBasic"]},
                 "OI": {"revenue": ["RevenueFromContractWithCustomerIncludingAssessedTax", "Revenues",
                                    "SalesRevenueGoodsNet"]},
                 "STLD": {"net_income": ["NetIncomeLoss", "NetIncomeLossAvailableToCommonStockholdersBasic"]},
                 # Dow, Ecolab and IFF tag profit to common shareholders in the years they do not tag NetIncomeLoss;
                 # LyondellBasell tags only ProfitLoss (with its small non-controlling interests) after 2019
                 "DOW": {"net_income": ["NetIncomeLoss", "NetIncomeLossAvailableToCommonStockholdersBasic"]},
                 "ECL": {"net_income": ["NetIncomeLoss", "NetIncomeLossAvailableToCommonStockholdersBasic"]},
                 "IFF": {"net_income": ["NetIncomeLoss", "NetIncomeLossAvailableToCommonStockholdersBasic"]},
                 "LYB": {"net_income": ["NetIncomeLoss", "ProfitLoss"]},
                 # Broadcom tags its fiscal 2025 profit only as ProfitLoss
                 "AVGO": {"net_income": ["NetIncomeLoss", "ProfitLoss"]}}


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


IFRS_COMPANIES = [(811809, "BHP"), (863064, "RIO"), (917851, "VALE"), (1243429, "MT"), (1076378, "CX"), (941221, "ICL")]
# ArcelorMittal tags revenue as revenue from contracts with customers since 2018, and its capital spending with
# intangibles and other non-current assets
IFRS_OVERRIDES = {"MT": {"revenue": ["Revenue", "RevenueFromContractsWithCustomers"],
                         "capex": ["PurchaseOfPropertyPlantAndEquipmentClassifiedAsInvestingActivities",
                                   "PurchaseOfPropertyPlantAndEquipmentIntangibleAssetsOtherThanGoodwillInvestment"
                                   "PropertyAndOtherNoncurrentAssets"]}}
IFRS_ITEMS = {"revenue": ["Revenue"], "profit": ["ProfitLossAttributableToOwnersOfParent", "ProfitLoss"],
              "operating_cash": ["CashFlowsFromUsedInOperatingActivities"],
              "capex": ["PurchaseOfPropertyPlantAndEquipmentClassifiedAsInvestingActivities"]}


def sec_ifrs():
    """Annual figures of the three big diversified miners (Part 9), ArcelorMittal and Cemex (Part 11) and ICL (Part 12)
    from their Forms 20-F (SEC company facts, IFRS tags, US dollars): BHP's fiscal years end in June, the others' in
    December."""
    import time

    out = []
    for cik, tic in IFRS_COMPANIES:
        facts = json.loads(_get(f"https://data.sec.gov/api/xbrl/companyfacts/CIK{cik:010d}.json"))["facts"]
        ifrs = facts.get("ifrs-full", {})
        time.sleep(0.5)
        years: dict = {}
        for item, tags in IFRS_ITEMS.items():
            tags = IFRS_OVERRIDES.get(tic, {}).get(item, tags)
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



DS140_HEAVY = {"cement": "ds140-cement-2021", "steel": "ds140-iron-steel-2021", "scrap": "ds140-iron-steel-scrap-2021",
               "aluminum": "ds140-aluminum-2021", "crushed_stone": "ds140-crushed_stone-2022",
               "sand_gravel": "ds140-construction_sand_and%20gravel_2022", "nitrogen": "ds140-nitrogen-2022"}
DS140_COLS = {"production": ("production", "raw steel production", "primary production"),
              "consumption": ("apparent consumption", "reported consumption"),
              "unit_value": ("unit value ($/t)",), "unit_value_98": ("unit value (98$/t)",),
              "world_production": ("world production",)}


def usgs_heavy():
    """US Geological Survey, Data Series 140, for the heavy materials of Part 11: US production, apparent consumption,
    unit value (dollars a metric ton, of the year and of 1998) and world production of cement, raw steel, iron and
    steel scrap, aluminium, crushed stone and construction sand and gravel, every year since 1900 (or the first year
    recorded) to 2021 or 2022.  Long format: one row per (material, year, item)."""
    import io

    import openpyxl

    out = []
    for mat, f in DS140_HEAVY.items():
        wb = openpyxl.load_workbook(io.BytesIO(_get(DS140_BASE + f + ".xlsx")), data_only=True, read_only=True)
        ws = wb["Steel"] if mat == "steel" else wb[wb.sheetnames[0]]
        data = list(ws.iter_rows(values_only=True))
        hi = next(i for i, r in enumerate(data) if r[0] == "Year")
        hdr = [" ".join(str(c or "").split()).lower() for c in data[hi]]
        cols = {item: next(j for j, h in enumerate(hdr) if h in names) for item, names in DS140_COLS.items()
                if any(h in names for h in hdr)}
        for r in data[hi + 1:]:
            if isinstance(r[0], (int, float)) and 1800 < r[0] < 2100:
                for item, j in cols.items():
                    v = r[j]
                    if isinstance(v, (int, float)):
                        out.append([mat, int(r[0]), item, float(v)])
    return _write("usgs_heavy", ["material", "year", "item", "value"], out,
                  ["https://www.usgs.gov/centers/national-minerals-information-center/historical-statistics-mineral-and-"
                   "material-commodities (USGS Data Series 140; " + ", ".join(f.replace("%20", " ") + ".xlsx"
                                                                              for f in DS140_HEAVY.values()) +
                   "; metric tons; unit values in dollars a metric ton and in 1998 dollars; for steel, production is "
                   "raw steel; for aluminium, primary production)"])


FRED_HEAVY = {"WPU1017": "PPI steel mill products (1982=100)", "WPU101704": "PPI hot-rolled steel sheet and strip",
              "WPU1012": "PPI iron and steel scrap", "PCU327310327310": "PPI cement manufacturing",
              "PCU327320327320": "PPI ready-mix concrete", "WPU1321": "PPI construction sand, gravel and crushed stone",
              "PCU212312212312": "PPI crushed and broken limestone", "WPU102502": "PPI aluminium mill shapes",
              "PCU322211322211": "PPI corrugated and solid fiber boxes", "PCU322130322130": "PPI paperboard mills",
              "PCU327213327213": "PPI glass containers", "PCU332431332431": "PPI metal cans",
              "IPG3311A2S": "industrial production: iron and steel products", "CAPUTLG3311A2S":
              "capacity utilization: iron and steel products", "IPG3313S": "industrial production: alumina and "
              "aluminum", "IPN32731S": "industrial production: cement (not seasonally adjusted)",
              "IPG3221S": "industrial production: pulp, paper and paperboard mills", "TTLCONS": "total US construction "
              "spending ($m, annual rate)", "APU0000711211": "average price, bananas ($ a pound)",
              "CPIAUCSL": "CPI, all items"}


def fred_heavy():
    """Monthly series for Part 11 (via FRED): producer prices of steel, scrap, cement, concrete, stone, aluminium,
    boxes, glass and cans (BLS), industrial production and capacity utilization (Federal Reserve G.17), construction
    spending (Census), the average price of bananas and the CPI (BLS)."""
    out = []
    for sid in FRED_HEAVY:
        txt = _get(f"https://fred.stlouisfed.org/graph/fredgraph.csv?id={sid}").decode()
        for line in txt.splitlines()[1:]:
            d, v = line.split(",")
            if v not in (".", ""):
                out.append([sid, d[:7], float(v)])
    return _write("fred_heavy", ["series", "month", "value"], out,
                  ["https://fred.stlouisfed.org (" + "; ".join(f"{k} {v}" for k, v in FRED_HEAVY.items()) + ")"])


OWID_CO2 = ["annual-co2-cement", "annual-co2-emissions-per-country"]
OWID_CO2_ENTITIES = ("World", "China", "India", "United States")


def owid_co2():
    """The Global Carbon Budget's CO2 from cement (the chemistry of the kiln, not its fuel) and all fossil and industrial
    CO2, by year, for the world, China, India and the US (tonnes; via Our World in Data, CC BY 4.0)."""
    out = []
    for slug in OWID_CO2:
        txt = _get(f"https://ourworldindata.org/grapher/{slug}.csv?v=1&csvType=full&useColumnShortNames=true").decode()
        rows = list(csv.reader(io.StringIO(txt)))
        col = len(rows[0]) - 1
        for r in rows[1:]:
            if r[0] in OWID_CO2_ENTITIES and r[col] not in ("", None) and int(r[2]) >= 1900:
                out.append([slug, r[0], int(r[2]), float(r[col])])
    return _write("owid_co2", ["series", "entity", "year", "value"], out,
                  ["https://ourworldindata.org/grapher/" + s for s in OWID_CO2] +
                  ["Global Carbon Budget (2025), Friedlingstein et al.; cement: Andrew (2019)"])



FRED_CHEM = {"WPU06": "PPI chemicals and allied products", "PCU325110325110": "PPI petrochemical manufacturing",
             "PCU325211325211": "PPI plastics material and resins", "PCU325120325120": "PPI industrial gases",
             "PCU325510325510": "PPI paints and coatings", "PCU325412325412": "PPI pharmaceutical preparations",
             "PCU325311325311": "PPI nitrogenous fertilizers", "IPG325S": "industrial production: chemicals",
             "CAPUTLG325S": "capacity utilization: chemicals", "IPG3251S": "industrial production: basic chemicals",
             "IPG3252S": "industrial production: resins, synthetic rubber, fibers",
             "PNGASEUUSDM": "natural gas, Europe (IMF; $ per million Btu)",
             "PNGASUSUSDM": "natural gas, US Henry Hub (IMF; $ per million Btu)",
             "PNGASJPUSDM": "LNG, Asia (IMF; $ per million Btu)", "POILBREUSDM": "Brent crude (IMF; $ a barrel)",
             "CPIAUCSL": "CPI, all items"}


def fred_chem():
    """Monthly series for Part 12 (via FRED): producer prices of chemicals, petrochemicals, resins, industrial gases,
    paints, medicines and nitrogen fertilizer (BLS); industrial production and capacity utilization of chemicals
    (Federal Reserve G.17); the IMF's gas prices in Europe, the US and Asia and the Brent price; the CPI."""
    out = []
    for sid in FRED_CHEM:
        txt = _get(f"https://fred.stlouisfed.org/graph/fredgraph.csv?id={sid}").decode()
        for line in txt.splitlines()[1:]:
            d, v = line.split(",")
            if v not in (".", ""):
                out.append([sid, d[:7], float(v)])
    return _write("fred_chem", ["series", "month", "value"], out,
                  ["https://fred.stlouisfed.org (" + "; ".join(f"{k} {v}" for k, v in FRED_CHEM.items()) + ")"])


EIA_NGL = {"PET.M_EPLLEA_FPF_NUS_MBBLD.M": "US field production of ethane (thousand barrels a day)",
           "PET.M_EPLLPA_FPF_NUS_MBBLD.M": "US field production of propane (thousand barrels a day)",
           "PET.M_EPL2_FPF_NUS_MBBLD.M": "US field production of natural gas liquids (thousand barrels a day)",
           "PET.M_EPLLEA_EEX_NUS-Z00_2.M": "US exports of ethane (thousand barrels a day)",
           "PET.MPAEX_NUS-Z00_2.M": "US exports of propane (thousand barrels a day)",
           "PET.EER_EPLLPA_PF4_Y44MB_DPG.M": "Mont Belvieu propane spot price (dollars a gallon)"}


def eia_ngl():
    """US natural gas liquids from EIA's petroleum bulk file: field production of ethane, propane and all NGLs,
    exports of ethane and propane, and the Mont Belvieu propane price, month by month."""
    got = _eia_bulk("PET", lambda sid: sid in EIA_NGL)
    rows = []
    for sid in EIA_NGL:
        for per, v in sorted(got[sid]["data"]):
            if v is not None:
                rows.append([sid, f"{per[:4]}-{per[4:6]}", float(v)])
    return _write("eia_ngl", ["series", "month", "value"], rows,
                  ["https://api.eia.gov/bulk/PET.zip (" + "; ".join(f"{k} {v}" for k, v in EIA_NGL.items()) + ")"])


def eurostat_chem():
    """Eurostat's monthly index of production in the chemical industry (NACE C20), seasonally and calendar adjusted,
    2021 = 100, for Germany and the EU (dataset sts_inpr_m)."""
    url = ("https://ec.europa.eu/eurostat/api/dissemination/statistics/1.0/data/sts_inpr_m?geo=DE&geo=EU27_2020"
           "&nace_r2=C20&s_adj=SCA&unit=I21&format=JSON&lang=EN")
    d = json.loads(_get(url))
    t = d["dimension"]["time"]["category"]["index"]
    g = d["dimension"]["geo"]["category"]["index"]
    nt = len(t)
    rows = []
    for geo, gi in g.items():
        for month, ti in sorted(t.items(), key=lambda kv: kv[1]):
            v = d["value"].get(str(gi * nt + ti))
            if v is not None:
                rows.append([geo, month, float(v)])
    return _write("eurostat_chem", ["geo", "month", "value"], rows, [url + " (Eurostat, CC BY 4.0)"])



OWID_CHEM = ["global-plastics-production", "plastic-fate", "population",
             "nitrogen-fertilizer-application-per-hectare-of-cropland"]


def owid_chem():
    """Our World in Data, for Part 12: world plastics production since 1950 and what became of 2000-2019's plastic
    waste (OECD, Global Plastics Outlook), the world's population, and nitrogen fertilizer per hectare of cropland
    (FAO).  World only (CC BY 4.0)."""
    out = []
    for slug in OWID_CHEM:
        txt = _get(f"https://ourworldindata.org/grapher/{slug}.csv?v=1&csvType=full&useColumnShortNames=true").decode()
        rows = list(csv.reader(io.StringIO(txt)))
        head = rows[0]
        for r in rows[1:]:
            if r[0] == "World" and int(r[2]) >= 1800:
                for j in range(3, len(head)):
                    if r[j] not in ("", None):
                        out.append([slug, head[j], int(r[2]), float(r[j])])
    return _write("owid_chem", ["series", "column", "year", "value"], out,
                  ["https://ourworldindata.org/grapher/" + s for s in OWID_CHEM] +
                  ["OECD Global Plastics Outlook (2022); HYDE and UN WPP (population); FAO (fertilizer)"])



# Part 13 -----------------------------------------------------------------------------------------------------------
# EIA-930 six-month balance files: (balancing authority, first date, last date exclusive) to keep from each
EIA930 = {
    "EIA930_BALANCE_2019_Jan_Jun": [("CISO", "2019-04-01", "2019-05-01")],
    "EIA930_BALANCE_2021_Jan_Jun": [("ERCO", "2021-02-01", "2021-03-01")],
    "EIA930_BALANCE_2025_Jan_Jun": [("ERCO", "2025-01-01", "2025-07-01")],
    "EIA930_BALANCE_2025_Jul_Dec": [("ERCO", "2025-07-01", "2026-01-01")],
    "EIA930_BALANCE_2026_Jan_Jun": [("CISO", "2026-04-01", "2026-05-01")],
}
# our column: the EIA-930 columns that add up to it (the "(Adjusted)" version is used where the file has one)
EIA930_COLS = {
    "forecast": ["Demand Forecast (MW)"],
    "demand": ["Demand (MW)"],
    "net_gen": ["Net Generation (MW)"],
    "coal": ["Net Generation (MW) from Coal"],
    "gas": ["Net Generation (MW) from Natural Gas"],
    "nuclear": ["Net Generation (MW) from Nuclear"],
    "oil": ["Net Generation (MW) from All Petroleum Products"],
    "hydro": ["Net Generation (MW) from Hydropower and Pumped Storage",
              "Net Generation (MW) from Hydropower Excluding Pumped Storage", "Net Generation (MW) from Pumped Storage"],
    "solar": ["Net Generation (MW) from Solar", "Net Generation (MW) from Solar without Integrated Battery Storage",
              "Net Generation (MW) from Solar with Integrated Battery Storage"],
    "wind": ["Net Generation (MW) from Wind", "Net Generation (MW) from Wind without Integrated Battery Storage",
             "Net Generation (MW) from Wind with Integrated Battery Storage"],
    "battery": ["Net Generation (MW) from Battery Storage"],
    "other": ["Net Generation (MW) from Other Fuel Sources", "Net Generation (MW) from Unknown Fuel Sources",
              "Net Generation (MW) from Geothermal", "Net Generation (MW) from Other Energy Storage",
              "Net Generation (MW) from Unknown Energy Storage"],
}


def eia_930():
    """EIA's Hourly Electric Grid Monitor (Form EIA-930), from its six-month balance files: hourly demand, the day-ahead
    demand forecast and net generation by source for ERCOT (February 2021 and all of 2025) and the California ISO
    (April 2019 and April 2026).  Megawatts, each hour ending at the local time given."""
    import datetime as _dt
    out = []
    for f, wants in EIA930.items():
        txt = _get(f"https://www.eia.gov/electricity/gridmonitor/sixMonthFiles/{f}.csv").decode("utf-8", "replace")
        rd = csv.reader(io.StringIO(txt))
        head = [h.strip() for h in next(rd)]

        def pick(name):
            a = name + " (Adjusted)"
            return head.index(a) if a in head else (head.index(name) if name in head else None)
        cols = {k: [i for i in (pick(n) for n in v) if i is not None] for k, v in EIA930_COLS.items()}
        for r in rd:
            if not r or len(r) < len(head) - 1:
                continue
            for ba, lo, hi in wants:
                if r[0] != ba:
                    continue
                d = _dt.datetime.strptime(r[1], "%m/%d/%Y").date().isoformat()
                if not lo <= d < hi:
                    continue
                row = [ba, d, int(r[2])]
                for k in EIA930_COLS:
                    vals = [r[i].replace(",", "") for i in cols[k] if i < len(r) and r[i].strip() not in ("",)]
                    row.append(sum(float(v) for v in vals) if vals else None)
                out.append(row)
    return _write("eia_930", ["ba", "date", "hour"] + list(EIA930_COLS), out,
                  ["https://www.eia.gov/electricity/gridmonitor/ (six-month balance files: " + ", ".join(EIA930) + ")"])


# Monthly Energy Review: electricity retail sales and end use (Table 7.6), average retail prices (Table 9.8)
MER_TABLES = {"T07.06": "electricity end use", "T09.08": "average retail prices of electricity"}


def eia_mer():
    """EIA's Monthly Energy Review, Tables 7.6 (electricity end use, million kWh, since 1949) and 9.8 (average retail
    prices of electricity, cents per kWh, since 1960): annual (month 13) and monthly values."""
    out = []
    for t in MER_TABLES:
        txt = _get(f"https://www.eia.gov/totalenergy/data/browser/csv.php?tbl={t}").decode("utf-8", "replace")
        for r in csv.DictReader(io.StringIO(txt)):
            try:
                v = float(r["Value"])
            except (TypeError, ValueError):
                continue
            ym = r["YYYYMM"]
            out.append([t, r["MSN"], r["Description"], int(ym[:4]), int(ym[4:]), v, r["Unit"]])
    return _write("eia_mer", ["table", "msn", "description", "year", "month", "value", "unit"], out,
                  [f"https://www.eia.gov/totalenergy/data/browser/csv.php?tbl={t} ({d})" for t, d in MER_TABLES.items()])


FRED_POWER = {"APU000072610": "average price of electricity per kWh, US city average (BLS, dollars)",
              "CUSR0000SEHF01": "CPI, electricity (seasonally adjusted)", "CPIAUCSL": "CPI, all items",
              "PNGASUSUSDM": "natural gas, US Henry Hub (IMF; $ per million Btu)",
              "PNGASEUUSDM": "natural gas, Europe (IMF; $ per million Btu)",
              "IPG2211S": "industrial production: electric power generation, transmission and distribution",
              "PCU221122221122": "PPI electric power distribution"}


def fred_power():
    """Monthly series for Part 13 (via FRED): the BLS's average price of a kWh and the CPI for electricity, the CPI,
    the IMF's gas prices in the US and Europe, the Federal Reserve's output of electric power, and the PPI for
    electric power distribution."""
    out = []
    for sid in FRED_POWER:
        txt = _get(f"https://fred.stlouisfed.org/graph/fredgraph.csv?id={sid}").decode()
        for line in txt.splitlines()[1:]:
            d, v = line.split(",")
            if v not in (".", ""):
                out.append([sid, d[:7], float(v)])
    return _write("fred_power", ["series", "month", "value"], out,
                  ["https://fred.stlouisfed.org (" + "; ".join(f"{k} {v}" for k, v in FRED_POWER.items()) + ")"])


OWID_ELEC = ["electricity-generation", "per-capita-electricity-generation", "share-electricity-solar",
             "share-electricity-wind", "share-electricity-coal"]
OWID_ELEC_ENTITIES = ("World", "China", "United States", "India", "European Union (27)", "Japan", "Russia", "Brazil",
                      "Africa", "France", "Germany", "United Kingdom")


def owid_elec():
    """Our World in Data (Ember and the Energy Institute): electricity generation, generation per person, and the
    shares of solar, wind and coal, for the world, the largest users and a few others (CC BY 4.0)."""
    out = []
    for slug in OWID_ELEC:
        txt = _get(f"https://ourworldindata.org/grapher/{slug}.csv?v=1&csvType=full&useColumnShortNames=true").decode()
        rows = list(csv.reader(io.StringIO(txt)))
        head = rows[0]
        for r in rows[1:]:
            if r[0] in OWID_ELEC_ENTITIES:
                for j in range(3, len(head)):
                    if r[j] not in ("", None):
                        out.append([slug, r[0], int(r[2]), float(r[j])])
    return _write("owid_elec", ["series", "entity", "year", "value"], out,
                  ["https://ourworldindata.org/grapher/" + s for s in OWID_ELEC] +
                  ["Ember (2026); Energy Institute, Statistical Review of World Energy (2025)"])


BLS_CPI = {"SA0": "All items", "SEHG01": "Water and sewerage maintenance", "SEHG02": "Garbage and trash collection",
           "SEHF01": "Electricity", "SEHF02": "Utility (piped) gas service", "SEHA": "Rent of primary residence"}
BLS_CU = "https://download.bls.gov/pub/time.series/cu/"


def bls_water():
    """Consumer price indexes, US city average, all urban consumers, not seasonally adjusted: annual averages of all
    items, water and sewerage maintenance (since 1953), garbage and trash collection (since 1984), electricity, piped
    gas and rent (BLS CPI flat files)."""
    want = {f"CUUR0000{k}": v for k, v in BLS_CPI.items()}
    out = []
    for f in ("cu.data.1.AllItems", "cu.data.12.USHousing"):
        for line in _get(BLS_CU + f).decode().splitlines()[1:]:
            p = [x.strip() for x in line.split("\t")]
            if len(p) >= 4 and p[0] in want and p[2] == "M13":
                out.append([p[0][8:], want[p[0]], int(p[1]), float(p[3])])
    out.sort()
    return _write("bls_water", ["item", "name", "year", "value"], out,
                  [BLS_CU + "cu.data.1.AllItems", BLS_CU + "cu.data.12.USHousing",
                   "CPI-U, US city average, not seasonally adjusted, annual average (period M13)"])


FRED_WASTE = {"PCU562111562111": "PPI solid waste collection (Dec 2003 = 100)",
              "WPU0912": "PPI recyclable paper (1982 = 100)",
              "WPU091201": "PPI news and other low grade recyclable paper",
              "WPU1012": "PPI iron and steel scrap (1982 = 100)",
              "CUSR0000SEHG": "CPI water and sewer and trash collection services (Dec 1997 = 100)",
              "CPIAUCSL": "CPI, all items"}


def fred_waste():
    """Monthly series for Part 14 (via FRED): the PPI for solid waste collection, recyclable paper, low-grade
    recyclable paper and iron and steel scrap, and the CPI for water, sewer and trash services and all items."""
    out = []
    for sid in FRED_WASTE:
        txt = _get(f"https://fred.stlouisfed.org/graph/fredgraph.csv?id={sid}").decode()
        for line in txt.splitlines()[1:]:
            d, v = line.split(",")
            if v not in (".", ""):
                out.append([sid, d[:7], float(v)])
    return _write("fred_waste", ["series", "month", "value"], out,
                  ["https://fred.stlouisfed.org (" + "; ".join(f"{k} {v}" for k, v in FRED_WASTE.items()) + ")"])


EPA_MSW = "https://www.epa.gov/sites/default/files/2021-01/historical_ff_data_1960-2018_12312020.xlsx"


def epa_msw():
    """EPA, Advancing Sustainable Materials Management: Facts and Figures, municipal solid waste 1960-2018 (thousand
    short tons): landfilled, combusted with energy recovery, composted, other food management, recycled, generated,
    and pounds per person per day.  EPA's national series ends in 2018."""
    import openpyxl

    wb = openpyxl.load_workbook(io.BytesIO(_get(EPA_MSW)), read_only=True, data_only=True)
    out = []
    for r in wb.worksheets[0].iter_rows(values_only=True):
        if isinstance(r[0], int) and 1960 <= r[0] <= 2030 and r[8] is not None:
            out.append([r[0], r[1], r[3], r[4], r[5], r[6], r[7], r[8], None if r[9] is None else round(r[9], 3)])
        if r[0] and isinstance(r[0], str) and r[0].startswith("Population"):
            break
    return _write("epa_msw", ["year", "landfill", "combustion_er", "combustion_total", "food_other", "composting",
                              "recycling", "generation", "lb_per_person_day"], out,
                  [EPA_MSW, "thousand US short tons; landfill includes combustion without energy recovery in "
                   "1960, 1970, 1980 and 1990; combustion series incomplete before 2000"])



FRED_CHIPS = {"IPG3344S": "Industrial production: semiconductors and other electronic components (2017 = 100)",
              "CAPUTLG3344S": "Capacity utilization: semiconductors and other electronic components (%)",
              "PCU334413334413": "PPI: semiconductor and related device manufacturing (Dec 1998 = 100)",
              "PCU33443344": "PPI: semiconductor and other electronic component manufacturing (Dec 1984 = 100)",
              "CPIAUCSL": "CPI, all items"}


def fred_chips():
    """Monthly series for Part 15 (via FRED): the Federal Reserve's output and capacity utilization of semiconductors
    and other electronic components since 1972, the BLS's producer price indexes for semiconductors, and the CPI."""
    out = []
    for sid in FRED_CHIPS:
        txt = _get(f"https://fred.stlouisfed.org/graph/fredgraph.csv?id={sid}").decode()
        for line in txt.splitlines()[1:]:
            d, v = line.split(",")
            if v not in (".", ""):
                out.append([sid, d[:7], float(v)])
    return _write("fred_chips", ["series", "month", "value"], out,
                  ["https://fred.stlouisfed.org (" + "; ".join(f"{k} {v}" for k, v in FRED_CHIPS.items()) + ")"])


def owid_chips():
    """Transistors per microprocessor, 1971-2021 (Karl Rupp's compilation via Our World in Data, CC BY 4.0)."""
    txt = _get("https://ourworldindata.org/grapher/transistors-per-microprocessor.csv?v=1&csvType=full"
               "&useColumnShortNames=true").decode()
    rows = list(csv.reader(io.StringIO(txt)))
    out = [[int(r[2]), float(r[3])] for r in rows[1:] if r[0] == "World" and r[3]]
    return _write("owid_chips", ["year", "transistors"], out,
                  ["https://ourworldindata.org/grapher/transistors-per-microprocessor (Karl Rupp, 'Microprocessor "
                   "Trend Data' (2022), via Our World in Data, CC BY 4.0)"])


FOREIGN_CHIPS = [(1046179, "TSM", "ifrs-full", "TWD"), (1033767, "UMC", "ifrs-full", "TWD"), (1709048, "GFS", "ifrs-full", "USD"),
                 (937966, "ASML", "us-gaap", "EUR"), (932787, "STM", "us-gaap", "USD"),
                 # Part 16: electronics
                 (313838, "SONY", "ifrs-full", "JPY"), (1290109, "LPL", "ifrs-full", "KRW"), (1122411, "ASX", "ifrs-full", "TWD")]
FOREIGN_ITEMS = {"ifrs-full": {"revenue": ["Revenue", "RevenueFromContractsWithCustomers"],
                               "operating_income": ["ProfitLossFromOperatingActivities"],
                               "profit": ["ProfitLossAttributableToOwnersOfParent", "ProfitLoss"],
                               "capex": ["PurchaseOfPropertyPlantAndEquipmentClassifiedAsInvestingActivities"],
                               "depreciation": ["DepreciationExpense", "DepreciationAndAmortisationExpense"]},
                 "us-gaap": {"revenue": ["Revenues", "RevenueFromContractWithCustomerExcludingAssessedTax", "SalesRevenueNet"],
                             "operating_income": ["OperatingIncomeLoss"],
                             "profit": ["NetIncomeLoss", "NetIncomeLossAvailableToCommonStockholdersBasic"],
                             "capex": ["PaymentsToAcquirePropertyPlantAndEquipment", "PaymentsToAcquireProductiveAssets"],
                             "depreciation": ["DepreciationDepletionAndAmortization", "DepreciationAndAmortization",
                                              "Depreciation"]}}


def sec_foreign():
    """Annual figures of the foreign chip and electronics makers that file Forms 20-F with the SEC, in their reporting
    currency (billions): TSMC and UMC (IFRS, NT dollars), GlobalFoundries (IFRS, US dollars), ASML (US GAAP, euros) and
    STMicroelectronics (US GAAP, US dollars) for Part 15; Sony (IFRS, yen), LG Display (IFRS, won) and ASE (IFRS, NT
    dollars) for Part 16."""
    import time

    out = []
    for cik, tic, tax, cur in FOREIGN_CHIPS:
        facts = json.loads(_get(f"https://data.sec.gov/api/xbrl/companyfacts/CIK{cik:010d}.json"))["facts"].get(tax, {})
        time.sleep(0.5)
        years: dict = {}
        for item, tags in FOREIGN_ITEMS[tax].items():
            for tag in tags:
                best: dict = {}
                for v in facts.get(tag, {}).get("units", {}).get(cur, []):
                    if v.get("form") not in ("20-F", "20-F/A", "10-K", "10-K/A") or "start" not in v:
                        continue
                    d = (dt.date.fromisoformat(v["end"]) - dt.date.fromisoformat(v["start"])).days
                    if not 350 <= d <= 380:
                        continue
                    if v["end"] not in best or v["filed"] > best[v["end"]]["filed"]:
                        best[v["end"]] = v
                for end, v in best.items():
                    years.setdefault(end, {}).setdefault(item, v["val"] / 1e9)
        for end in sorted(years):
            out.append([tic, end, cur] + [years[end].get(k) for k in FOREIGN_ITEMS["ifrs-full"]])
    return _write("sec_foreign", ["ticker", "year_end", "currency"] + list(FOREIGN_ITEMS["ifrs-full"]), out,
                  ["https://data.sec.gov/api/xbrl/companyfacts/ (Forms 20-F and 10-K of foreign issuers; billions of the "
                   "reporting currency; IFRS tags: " + "; ".join(f"{k}: {'/'.join(v)}" for k, v in FOREIGN_ITEMS["ifrs-full"].items())
                   + "; US GAAP tags: " + "; ".join(f"{k}: {'/'.join(v)}" for k, v in FOREIGN_ITEMS["us-gaap"].items()) + ")"])


WB_WATER = {"SH.H2O.SMDW.ZS": "safely managed drinking water", "SH.STA.SMSS.ZS": "safely managed sanitation",
            "SH.H2O.BASW.ZS": "at least basic drinking water", "SH.STA.BASS.ZS": "at least basic sanitation"}
WB_WATER_COUNTRIES = "WLD;USA;GBR;FRA;DEU;JPN;BRA;MEX;CHN;IND;IDN;PAK;BGD;NGA;ETH;ZAF;EGY;SSF;SAS"


def wb_water():
    """The share of people using safely managed (and at least basic) drinking water and sanitation, 2000-2024, for
    the world, its regions and a set of countries (WHO/UNICEF Joint Monitoring Programme via the World Bank's World
    Development Indicators)."""
    out = []
    for code, name in WB_WATER.items():
        url = (f"https://api.worldbank.org/v2/country/{WB_WATER_COUNTRIES}/indicator/{code}?format=json"
               "&date=2000:2025&per_page=2000")
        for x in json.loads(_get(url))[1]:
            if x["value"] is not None:
                out.append([code, name, x["country"]["value"], int(x["date"]), round(x["value"], 2)])
    out.sort()
    return _write("wb_water", ["indicator", "name", "country", "year", "value"], out,
                  ["https://api.worldbank.org (World Development Indicators: " + ", ".join(WB_WATER) +
                   "; WHO/UNICEF Joint Monitoring Programme, % of population)"])


# ---------------------------------------------------------------------------------------------------------- Part 16
BLS_ELEC = {"SA0": "All items", "SERA01": "Televisions (Dec 2024 = 100)",
            "SEEE01": "Computers, peripherals, and smart home assistants (Dec 2007 = 100)",
            "SEEE04": "Telephone hardware, calculators, and other consumer information items (Dec 2024 = 100)",
            "SSEE041": "Smartphones (Dec 2019 = 100)"}


def bls_elec():
    """Consumer price indexes for electronics, US city average, all urban consumers, not seasonally adjusted, annual
    averages (BLS CPI flat files): televisions since 1951, computers and telephone hardware since 1998, smartphones since
    2020, and all items.  The indexes are quality-adjusted."""
    want = {f"CUUR0000{k}": v for k, v in BLS_ELEC.items()}
    out = []
    files = ("cu.data.1.AllItems", "cu.data.16.USRecreation", "cu.data.17.USEducationAndCommunication")
    for f in files:
        for line in _get(BLS_CU + f).decode().splitlines()[1:]:
            p = [x.strip() for x in line.split("\t")]
            if len(p) >= 4 and p[0] in want and p[2] == "M13":
                out.append([p[0][8:], want[p[0]], int(p[1]), float(p[3])])
    out.sort()
    return _write("bls_elec", ["item", "name", "year", "value"], out,
                  [BLS_CU + f for f in files] + ["CPI-U, US city average, not seasonally adjusted, annual average (period M13)"])


FRED_ELEC = {"IPG3341S": "Industrial production: computers and peripheral equipment (2017 = 100)",
             "IPG3342S": "Industrial production: communications equipment (2017 = 100)",
             "IPG3343S": "Industrial production: audio and video equipment (2017 = 100)",
             "CEU3133400001": "All employees, computer and electronic products manufacturing (thousands, not seasonally adjusted)",
             "PCU334111334111": "PPI: electronic computer manufacturing (Dec 1990 = 100)",
             "AEXTAUS": "Taiwan dollars to one US dollar, annual average (Federal Reserve H.10)",
             "AEXJPUS": "Japanese yen to one US dollar, annual average (Federal Reserve H.10)",
             "AEXKOUS": "South Korean won to one US dollar, annual average (Federal Reserve H.10)"}


def fred_elec():
    """Monthly series for Part 16 (via FRED): the Federal Reserve's output of computers, communications equipment and
    audio and video equipment since 1972, employment in computer and electronic products manufacturing since 1990, and
    the producer price index for computers."""
    out = []
    for sid in FRED_ELEC:
        txt = _get(f"https://fred.stlouisfed.org/graph/fredgraph.csv?id={sid}").decode()
        for line in txt.splitlines()[1:]:
            d, v = line.split(",")
            if v not in (".", ""):
                out.append([sid, d[:7], float(v)])
    return _write("fred_elec", ["series", "month", "value"], out,
                  ["https://fred.stlouisfed.org (" + "; ".join(f"{k} {v}" for k, v in FRED_ELEC.items()) + ")"])


COMTRADE_PARTNERS = {0: "World", 156: "China", 704: "Vietnam", 699: "India", 484: "Mexico", 490: "Taiwan",
                     458: "Malaysia", 764: "Thailand", 410: "South Korea", 392: "Japan"}
COMTRADE_HS = {"851712": "telephones for cellular networks (to 2021: all mobile phones; from 2022: other than smartphones)",
               "851713": "smartphones (from 2022)", "847130": "portable computers of 10 kg or less (laptops)",
               "847150": "processing units (servers and other computer units)", "852872": "colour television receivers"}


def comtrade_us(years=range(2015, 2026)):
    """US imports by partner of phones, laptops, servers and televisions, 2015-2025, as reported by the United States
    to UN Comtrade (annual, HS six-digit, US dollars; UN Comtrade's public preview API).  Taiwan is 'Other Asia, nes'
    (code 490) in Comtrade."""
    import time

    out = []
    partners = ",".join(str(k) for k in COMTRADE_PARTNERS)
    for y in years:
        url = ("https://comtradeapi.un.org/public/v1/preview/C/A/HS?reporterCode=842&period={}&partnerCode={}&cmdCode={}"
               "&flowCode=M").format(y, partners, ",".join(COMTRADE_HS))
        j = json.loads(_get(url))
        for r in j.get("data", []):
            if r.get("customsCode") != "C00" or r.get("motCode") != 0 or r.get("partner2Code") != 0:
                continue
            out.append([y, r["cmdCode"], COMTRADE_PARTNERS.get(r["partnerCode"], r["partnerCode"]),
                        round(r["primaryValue"] / 1e9, 4), r.get("qty")])
        time.sleep(1.5)
    out.sort(key=lambda r: (r[0], r[1], str(r[2])))
    return _write("comtrade_us", ["year", "hs", "partner", "imports_usd_bn", "qty"], out,
                  ["https://comtradeapi.un.org/public/v1/preview/C/A/HS (UN Comtrade, reporter United States (842), "
                   "imports, annual; " + "; ".join(f"{k} {v}" for k, v in COMTRADE_HS.items()) + ")"])



def comtrade_us_m(start="2025-01", end=None):
    """US imports of smartphones (HS 851713) and laptops (847130) by month from the world, China, India and Vietnam,
    as reported by the United States to UN Comtrade (public preview API), from ``start`` to the latest month published."""
    import time

    y, m = map(int, start.split("-"))
    today = dt.date.today()
    out = []
    partners = {0: "World", 156: "China", 699: "India", 704: "Vietnam"}
    while (y, m) <= (today.year, today.month):
        per = f"{y}{m:02d}"
        url = ("https://comtradeapi.un.org/public/v1/preview/C/M/HS?reporterCode=842&period={}&partnerCode={}"
               "&cmdCode=851713,847130&flowCode=M").format(per, ",".join(str(k) for k in partners))
        j = json.loads(_get(url))
        for r in j.get("data", []):
            if r.get("customsCode") != "C00" or r.get("motCode") != 0 or r.get("partner2Code") != 0:
                continue
            out.append([f"{y}-{m:02d}", r["cmdCode"], partners[r["partnerCode"]], round(r["primaryValue"] / 1e9, 4)])
        time.sleep(1.5)
        y, m = (y + 1, 1) if m == 12 else (y, m + 1)
    out.sort()
    return _write("comtrade_us_m", ["month", "hs", "partner", "imports_usd_bn"], out,
                  ["https://comtradeapi.un.org/public/v1/preview/C/M/HS (UN Comtrade, reporter United States (842), "
                   "imports, monthly; 851713 smartphones, 847130 laptops)"])


# Part 17: automobiles
AUTO_COMPANIES = [(1467858, "GM", "USD"), (37996, "F", "USD"), (1318605, "TSLA", "USD"), (1874178, "RIVN", "USD"),
                  (1811210, "LCID", "USD"), (1094517, "TM", "JPY"), (715153, "HMC", "JPY"), (1605484, "STLA", "EUR"),
                  (1648416, "RACE", "EUR"), (75362, "PCAR", "USD"), (1736541, "NIO", "CNY"), (1791706, "LI", "CNY"),
                  (1810997, "XPEV", "CNY"),
                  (908255, "BWA", "USD"), (1521332, "APTV", "USD"), (842162, "LEA", "USD"), (1034670, "ALV", "USD"),
                  (42582, "GT", "USD"), (749098, "MGA", "USD"),
                  (350698, "AN", "USD"), (1023128, "LAD", "USD"), (1019849, "PAG", "USD"), (1170010, "KMX", "USD"),
                  (1690820, "CVNA", "USD")]
AUTO_ITEMS = {"revenue": [("ifrs-full", "Revenue"), ("us-gaap", "Revenues"),
                          ("us-gaap", "RevenueFromContractWithCustomerExcludingAssessedTax"), ("us-gaap", "SalesRevenueNet"),
                          ("us-gaap", "SalesRevenueGoodsNet")],
              "cost": [("ifrs-full", "CostOfSales"), ("us-gaap", "CostOfRevenue"), ("us-gaap", "CostOfGoodsAndServicesSold"),
                       ("us-gaap", "CostOfGoodsSold")],
              "operating_income": [("ifrs-full", "ProfitLossFromOperatingActivities"), ("us-gaap", "OperatingIncomeLoss")],
              "profit": [("ifrs-full", "ProfitLossAttributableToOwnersOfParent"), ("ifrs-full", "ProfitLoss"),
                         ("us-gaap", "NetIncomeLoss"), ("us-gaap", "ProfitLoss")],
              "rnd": [("ifrs-full", "ResearchAndDevelopmentExpense"), ("us-gaap", "ResearchAndDevelopmentExpense"),
                      ("us-gaap", "ResearchAndDevelopmentExpenseExcludingAcquiredInProcessCost")],
              "capex": [("ifrs-full", "PurchaseOfPropertyPlantAndEquipmentClassifiedAsInvestingActivities"),
                        ("us-gaap", "PaymentsToAcquirePropertyPlantAndEquipment"),
                        ("us-gaap", "PaymentsToAcquireProductiveAssets")],
              "inventory": [("ifrs-full", "Inventories"), ("us-gaap", "InventoryNet")],
              "assets": [("ifrs-full", "Assets"), ("us-gaap", "Assets")]}


def _sec_table(companies, items):
    """Rows [ticker, year_end, currency, item...] from SEC company facts for (cik, ticker, currency) companies: for each
    item the first (taxonomy, tag) present in a year wins; duration items need a year-long period."""
    import time

    out = []
    for cik, tic, cur in companies:
        facts = json.loads(_get(f"https://data.sec.gov/api/xbrl/companyfacts/CIK{cik:010d}.json"))["facts"]
        time.sleep(0.5)
        years: dict = {}
        for item, tags in items.items():
            for tax, tag in tags:
                best: dict = {}
                for v in facts.get(tax, {}).get(tag, {}).get("units", {}).get(cur, []):
                    if v.get("form") not in ("10-K", "10-K/A", "20-F", "20-F/A", "40-F", "40-F/A"):
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
                out.append([tic, end, cur] + [years[end].get(k) for k in items])
    return out


def _sec_source(items) -> str:
    return ("https://data.sec.gov/api/xbrl/companyfacts/ (Forms 10-K, 20-F and 40-F; billions of the reporting "
            "currency; tags in order of preference: " + "; ".join(f"{k}: {'/'.join(t for _, t in v)}"
                                                                 for k, v in items.items()) + ")")


def sec_auto():
    """Annual figures of carmakers, suppliers and dealers from their Forms 10-K, 20-F and 40-F (SEC company facts), in
    their reporting currency (billions): for each item the first tag present in a year wins, IFRS before US GAAP (Toyota
    and Honda moved from US GAAP to IFRS).  Duration items need a year-long period; balance items are taken at year end.
    Profit is attributable to the parent where tagged (Stellantis tags only profit including non-controlling interests;
    Ford tags only that in 2016-2020 and 2025)."""
    return _write("sec_auto", ["ticker", "year_end", "currency"] + list(AUTO_ITEMS),
                  _sec_table(AUTO_COMPANIES, AUTO_ITEMS), [_sec_source(AUTO_ITEMS)])


FRED_AUTO = {"TOTALSA": "Total vehicle sales (millions, seasonally adjusted annual rate; BEA)",
             "LAUTOSA": "Light weight vehicle sales: autos (millions, SAAR; BEA)",
             "LTRUCKSA": "Light weight vehicle sales: light trucks (millions, SAAR; BEA)",
             "MVAAUTLTTS": "Motor vehicle assemblies: autos and light trucks (millions of units, SAAR; Federal Reserve G.17)",
             "CAPUTLG3361T3S": "Capacity utilization: motor vehicles and parts (percent of capacity; Federal Reserve G.17)",
             "IPG3361S": "Industrial production: motor vehicles (2017 = 100; Federal Reserve G.17)",
             "AISRSA": "Auto inventory/sales ratio (months of supply, seasonally adjusted; BEA)",
             "CES3133600101": "All employees, motor vehicles and parts manufacturing (thousands, SA; BLS)",
             "CUUR0000SETA01": "CPI-U: new vehicles (1982-84 = 100, NSA; BLS)",
             "CUUR0000SETA02": "CPI-U: used cars and trucks (1982-84 = 100, NSA; BLS)",
             "CUUR0000SETD": "CPI-U: motor vehicle maintenance and repair (1982-84 = 100, NSA; BLS)",
             "CPIAUCNS": "CPI-U: all items (1982-84 = 100, NSA; BLS)",
             "TERMCBAUTO48NS": "Finance rate on consumer installment loans at commercial banks, new autos, 48 months "
                               "(percent; Federal Reserve G.19)",
             "AEXUSEU": "US dollars to one euro, annual average (Federal Reserve H.10)",
             "AEXJPUS": "Japanese yen to one US dollar, annual average (Federal Reserve H.10)",
             "AEXCHUS": "Chinese yuan to one US dollar, annual average (Federal Reserve H.10)"}


def fred_auto():
    """Monthly and quarterly series for Part 17 (via FRED): US light vehicle sales since 1976 and assemblies since 1977,
    the industry's capacity utilization since 1948, dealers' months of supply, employment, the consumer prices of new
    and used cars and of repairs against all items, the rate on a new-car loan, and the dollar's annual rates against the
    euro, yen and yuan."""
    out = []
    for sid in FRED_AUTO:
        txt = _get(f"https://fred.stlouisfed.org/graph/fredgraph.csv?id={sid}").decode()
        for line in txt.splitlines()[1:]:
            d, v = line.split(",")
            if v not in (".", ""):
                out.append([sid, d[:7], float(v)])
    return _write("fred_auto", ["series", "month", "value"], out,
                  ["https://fred.stlouisfed.org (" + "; ".join(f"{k} {v}" for k, v in FRED_AUTO.items()) + ")"])


OWID_EV = {"electric-car-sales-share": "ev_sales_share", "electric-car-sales": "ev_sales", "electric-car-stocks": "ev_stock"}
OWID_EV_ENTITIES = ("World", "China", "Europe", "United States", "Norway", "Germany", "France", "United Kingdom", "India",
                    "Japan", "Korea", "Brazil", "Rest of the world")


def owid_ev():
    """Electric cars (battery electric and plug-in hybrid): share of new car sales (percent), sales and stock, by
    country and region, from the IEA's Global EV Outlook via Our World in Data."""
    out = []
    for slug, col in OWID_EV.items():
        txt = _get(f"https://ourworldindata.org/grapher/{slug}.csv?v=1&csvType=full&useColumnShortNames=true").decode()
        rows = list(csv.DictReader(io.StringIO(txt)))
        for r in rows:
            if r["entity"] in OWID_EV_ENTITIES and r.get(col) not in (None, ""):
                out.append([col, r["entity"], int(r["year"]), float(r[col])])
    out.sort()
    return _write("owid_ev", ["series", "entity", "year", "value"], out,
                  ["https://ourworldindata.org/grapher/" + s for s in OWID_EV] +
                  ["IEA, Global EV Outlook 2026, via Our World in Data (CC BY 4.0); electric = battery electric and "
                   "plug-in hybrid cars"])


COMTRADE_CAR_REPORTERS = {156: "China", 392: "Japan", 276: "Germany", 410: "South Korea", 484: "Mexico", 842: "United States"}
COMTRADE_CAR_HS = {"8703": "motor cars and other passenger vehicles", "870380": "passenger cars with only an electric motor "
                   "(from HS 2017)"}


def comtrade_cars(years=range(2015, 2026)):
    """Exports of passenger cars (HS 8703) and battery electric cars (870380) to the world by six large exporters, as each
    reported them to UN Comtrade (annual; US dollars and units; UN Comtrade's public preview API)."""
    import time

    out = []
    for y in years:
        url = ("https://comtradeapi.un.org/public/v1/preview/C/A/HS?reporterCode={}&period={}&partnerCode=0&cmdCode={}"
               "&flowCode=X").format(",".join(str(k) for k in COMTRADE_CAR_REPORTERS), y, ",".join(COMTRADE_CAR_HS))
        j = json.loads(_get(url))
        for r in j.get("data", []):
            if r.get("customsCode") != "C00" or r.get("motCode") != 0 or r.get("partner2Code") != 0:
                continue
            out.append([y, r["cmdCode"], COMTRADE_CAR_REPORTERS[r["reporterCode"]], round(r["primaryValue"] / 1e9, 4),
                        r.get("qty")])
        time.sleep(1.5)
    out.sort(key=lambda r: (r[0], r[1], r[2]))
    return _write("comtrade_cars", ["year", "hs", "reporter", "exports_usd_bn", "qty"], out,
                  ["https://comtradeapi.un.org/public/v1/preview/C/A/HS (UN Comtrade; exports to the world as reported "
                   "by each country, annual; " + "; ".join(f"{k} {v}" for k, v in COMTRADE_CAR_HS.items()) + ")"])


AEO17 = "https://www.eia.gov/outlooks/archive/aeo17/supplement/excel/suptab_39.xlsx"


def eia_aeo17():
    """The EIA's Annual Energy Outlook 2017 (Reference case, released January 2017), supplement table 39: projected US
    sales of new light-duty vehicles by technology, 2015-2050 (thousands)."""
    import openpyxl

    wb = openpyxl.load_workbook(io.BytesIO(_get(AEO17)), read_only=True, data_only=True)
    ws = wb.worksheets[0]
    rows = list(ws.iter_rows(values_only=True))
    head = next(r for r in rows if r[1] and str(r[1]).strip() == "Technology Type")
    keep = {"Total New Car Sales": "cars", "Total New Light Truck Sales": "light_trucks", "   Electric": "electric",
            "   Plug-in Electric Hybrid": "plugin_hybrid", "   Conventional Gasoline": "gasoline"}
    out, section = [], ""
    for r in rows:
        if r[1] and str(r[1]).strip() == "Total Sales, Cars and Light Trucks":
            section = "total"
        lab = str(r[1]) if r[1] else ""
        name = keep.get(lab.rstrip()) if lab.rstrip() in keep else None
        if name in ("electric", "plugin_hybrid", "gasoline") and section != "total":
            continue
        if name:
            for y, v in zip(head[2:], r[2:]):
                if isinstance(y, int) and isinstance(v, (int, float)):
                    out.append([name, y, round(float(v), 3)])
    return _write("eia_aeo17", ["series", "year", "thousands"], out,
                  [AEO17 + " (EIA, Annual Energy Outlook 2017, Reference case, 'Light-Duty Vehicle Sales by Technology "
                   "Type'; electric = 100- and 200-mile battery electric; plug-in electric hybrid = PHEV10 and PHEV40)"])


ECN22 = "https://www2.census.gov/programs-surveys/economic-census/data/2022/API_Datasets/"
CENSUS_AUTO_NAICS = ("31-33", "336", "3361", "336110", "3362", "3363", "33631", "33632", "33633", "33634", "33635",
                     "33636", "33637", "33639", "4411", "441110", "441120")
# Census materials codes are the NAICS product codes of what is bought, plus two digits; names are read from them
AUTO_MATERIALS = {"00772000": "total materials, parts, containers and supplies", "33637000": "metal stampings",
                  "33635000": "transmissions and power-train parts", "33631000": "engines and engine parts",
                  "33639000": "other motor vehicle parts", "33636000": "seats and interior trim",
                  "33632000": "electrical and electronic equipment", "32721000": "glass",
                  "32610001": "plastics products", "33200091": "fabricated metal products",
                  "33633000": "steering and suspension parts", "33431000": "audio and video equipment",
                  "33441310": "semiconductors and related devices", "33451400": "instruments and gauges",
                  "32620100": "tyres", "33341500": "air-conditioning and refrigeration equipment",
                  "33211000": "forgings", "00970099": "all other materials and components"}


def census_auto():
    """The 2022 Economic Census for the car industry: firms, establishments, shipments or sales, payroll, employees,
    cost of materials and inventories for car and light-vehicle assembly (NAICS 336110), bodies, parts (3363 and its
    branches) and dealers (4411); and the materials car assemblers consumed, by kind (US totals, $ thousands)."""
    z = zipfile.ZipFile(io.BytesIO(_get(ECN22 + "ECNBASIC2022.zip")))
    out = []
    with z.open("ECNBASIC2022.dat") as f:
        head = f.readline().decode("latin-1").lstrip("#").strip().split("|")
        ix = {k: head.index(k) for k in ("NAICS2022", "NAICS2022_LABEL", "TAXSTAT", "TYPOP", "FIRM", "ESTAB",
                                         "RCPTOT", "PAYANN", "EMP", "CSTMTOT", "INVTOTE")}
        for b in f:
            if not b.startswith(b"0100000US|"):
                continue
            p = b.decode("latin-1").rstrip("\n").split("|")
            if p[ix["NAICS2022"]] in CENSUS_AUTO_NAICS and p[ix["TAXSTAT"]] == "00" and p[ix["TYPOP"]] == "00":
                out.append(["basic", p[ix["NAICS2022"]], p[ix["NAICS2022_LABEL"]]] +
                           [p[ix[k]] for k in ("FIRM", "ESTAB", "RCPTOT", "PAYANN", "EMP", "CSTMTOT", "INVTOTE")])
    z = zipfile.ZipFile(io.BytesIO(_get(ECN22 + "ECNMATFUEL2022.zip")))
    lines = z.read("ECNMATFUEL2022.dat").decode("latin-1").splitlines()
    head = lines[0].lstrip("#").split("|")
    for ln in lines[1:]:
        d = dict(zip(head, ln.split("|")))
        if d["GEOTYPE"] == "01" and d["NAICS2022"] == "336110" and d["MATFUEL"] in AUTO_MATERIALS:
            out.append(["materials", d["MATFUEL"], AUTO_MATERIALS[d["MATFUEL"]], "", "",
                        d["MATFUELCOST"] if d["MATFUELCOST_F"] != "D" else "", "", "", "", ""])
    return _write("census_auto", ["table", "code", "name", "firms", "establishments", "receipts", "payroll",
                                  "employees", "materials", "inventories"], out,
                  [ECN22 + "ECNBASIC2022.zip (2022 Economic Census, core statistics, United States, all firms; "
                   "$ thousands)", ECN22 + "ECNMATFUEL2022.zip (materials consumed by kind, NAICS 336110; delivered "
                   "cost in the 'receipts' column, $ thousands; names read from the materials codes, which are NAICS "
                   "product codes; withheld cells blank)"])


# Part 18: aerospace and defence
AERO_COMPANIES = [(12927, "BA", "USD"), (40545, "GE", "USD"), (101829, "RTX", "USD"), (936468, "LMT", "USD"),
                  (1133421, "NOC", "USD"), (40533, "GD", "USD"), (202058, "LHX", "USD"), (1501585, "HII", "USD"),
                  (4281, "HWM", "USD"), (1260221, "TDG", "USD"), (46619, "HEI", "USD"), (1364885, "SPR", "USD"),
                  (217346, "TXT", "USD"), (1378789, "AER", "USD"), (1355444, "ERJ", "USD")]


def sec_aero():
    """Annual figures of airframers, engine makers, defence primes, suppliers and a lessor from their Forms 10-K and
    20-F (SEC company facts), in US dollars (billions), with the same items and tag preferences as ``sec_auto``."""
    return _write("sec_aero", ["ticker", "year_end", "currency"] + list(AUTO_ITEMS),
                  _sec_table(AERO_COMPANIES, AUTO_ITEMS), [_sec_source(AUTO_ITEMS)])


def _fred_rows(series: dict) -> list:
    out = []
    for sid in series:
        txt = _get(f"https://fred.stlouisfed.org/graph/fredgraph.csv?id={sid}").decode()
        for line in txt.splitlines()[1:]:
            d, v = line.split(",")
            if v not in (".", ""):
                out.append([sid, d[:7], float(v)])
    return out


def _fred_write(name: str, series: dict) -> Path:
    return _write(name, ["series", "month", "value"], _fred_rows(series),
                  ["https://fred.stlouisfed.org (" + "; ".join(f"{k} {v}" for k, v in series.items()) + ")"])


MACH_COMPANIES = [(18230, "CAT", "USD"), (315189, "DE", "USD"), (1567094, "CNH", "USD"), (880266, "AGCO", "USD"),
                  (26172, "CMI", "USD"), (1781335, "OTIS", "USD"), (1783180, "CARR", "USD"), (1466258, "TT", "USD"),
                  (833444, "JCI", "USD"), (1024478, "ROK", "USD"), (32604, "EMR", "USD"), (773840, "HON", "USD"),
                  (49826, "ITW", "USD"), (76334, "PH", "USD"), (1551182, "ETN", "USD"), (29905, "DOV", "USD"),
                  (1067701, "URI", "USD"), (97216, "TEX", "USD"), (775158, "OSK", "USD"), (66740, "MMM", "USD"),
                  (1996810, "GEV", "USD"), (1699150, "IR", "USD"), (1524472, "XYL", "USD")]


def sec_mach():
    """Annual figures of machinery makers (construction, farm, engines, elevators, climate, automation, components), a
    rental company and the conglomerates from their Forms 10-K and 20-F (SEC company facts), in US dollars (billions),
    with the same items and tag preferences as ``sec_auto``."""
    return _write("sec_mach", ["ticker", "year_end", "currency"] + list(AUTO_ITEMS),
                  _sec_table(MACH_COMPANIES, AUTO_ITEMS), [_sec_source(AUTO_ITEMS)])


FRED_MACH = {"A33SNO": "New orders: machinery ($ million a month, SA; Census M3)",
             "A33SVS": "Shipments: machinery ($ million a month, SA; Census M3)",
             "NEWORDER": "New orders: nondefense capital goods excluding aircraft ($ million a month, SA; Census M3)",
             "IPG333S": "Industrial production: machinery (2017 = 100; Federal Reserve G.17)",
             "CAPUTLG333S": "Capacity utilization: machinery (percent of capacity; Federal Reserve G.17)",
             "PCU333111333111": "PPI: farm machinery and equipment manufacturing (1982 = 100; BLS)",
             "PCU333120333120": "PPI: construction machinery manufacturing (Dec 1976 = 100; BLS)",
             "CES3133300001": "All employees: machinery manufacturing (thousands, SA; BLS)",
             "Y033RC1Q027SBEA": "Private fixed investment in equipment ($ billion, SAAR; BEA)",
             "GDP": "Gross domestic product ($ billion, SAAR; BEA)",
             "CPIAUCNS": "CPI-U: all items (1982-84 = 100, NSA; BLS)"}


def fred_mach():
    return _fred_write("fred_mach", FRED_MACH)


OWID_ROBOTS = "https://ourworldindata.org/grapher/annual-industrial-robots-installed.csv"


def owid_robots():
    """New industrial robots installed per year by country (China, Germany, Japan, South Korea, the United States, the
    world), from the International Federation of Robotics via the AI Index Report 2026, as published by Our World in
    Data."""
    import csv as _csv
    rows = list(_csv.reader(io.StringIO(_get(OWID_ROBOTS).decode())))
    out = [[r[0], int(r[2]), float(r[3])] for r in rows[1:] if r[3]]
    return _write("owid_robots", ["entity", "year", "robots_installed"], out,
                  [OWID_ROBOTS + " (International Federation of Robotics via AI Index Report 2026; Our World in Data; "
                   "CC BY 4.0)"])


COMTRADE_MACH_REPORTERS = {156: "China", 392: "Japan", 276: "Germany", 410: "South Korea", 842: "United States"}
COMTRADE_MACH_HS = {"842952": "excavators and shovels with a 360-degree revolving superstructure",
                    "847950": "industrial robots, not elsewhere specified (from HS 2007)"}


def comtrade_mach(years=range(2010, 2026)):
    """Exports of excavators (HS 842952) and industrial robots (847950) to the world by five large exporters, as each
    reported them to UN Comtrade (annual; US dollars and units; UN Comtrade's public preview API)."""
    import time

    out = []
    for y in years:
        url = ("https://comtradeapi.un.org/public/v1/preview/C/A/HS?reporterCode={}&period={}&partnerCode=0&cmdCode={}"
               "&flowCode=X").format(",".join(str(k) for k in COMTRADE_MACH_REPORTERS), y, ",".join(COMTRADE_MACH_HS))
        j = json.loads(_get(url))
        for r in j.get("data", []):
            if r.get("customsCode") != "C00" or r.get("motCode") != 0 or r.get("partner2Code") != 0:
                continue
            out.append([y, r["cmdCode"], COMTRADE_MACH_REPORTERS[r["reporterCode"]], round(r["primaryValue"] / 1e9, 4),
                        r.get("qty")])
        time.sleep(1.5)
    out.sort(key=lambda r: (r[0], r[1], r[2]))
    return _write("comtrade_mach", ["year", "hs", "reporter", "exports_usd_bn", "qty"], out,
                  ["https://comtradeapi.un.org/public/v1/preview/C/A/HS (UN Comtrade; exports to the world as reported "
                   "by each country, annual; " + "; ".join(f"{k} {v}" for k, v in COMTRADE_MACH_HS.items()) + ")"])


PHARMA_COMPANIES = [(78003, "PFE", "USD"), (310158, "MRK", "USD"), (200406, "JNJ", "USD"), (59478, "LLY", "USD"),
                    (1551152, "ABBV", "USD"), (14272, "BMY", "USD"), (318154, "AMGN", "USD"), (882095, "GILD", "USD"),
                    (875320, "VRTX", "USD"), (872589, "REGN", "USD"), (875045, "BIIB", "USD"), (1682852, "MRNA", "USD"),
                    (818686, "TEVA", "USD"), (1792044, "VTRS", "USD"), (901832, "AZN", "USD"), (1114448, "NVS", "USD")]


def sec_pharma():
    """Annual figures of large drug makers, biotechs and generics makers from their Forms 10-K and 20-F (SEC company
    facts), in US dollars (billions), with the same items and tag preferences as ``sec_auto`` (research and development
    included)."""
    return _write("sec_pharma", ["ticker", "year_end", "currency"] + list(AUTO_ITEMS),
                  _sec_table(PHARMA_COMPANIES, AUTO_ITEMS), [_sec_source(AUTO_ITEMS)])


FRED_PHARMA = {"PCU325412325412": "PPI: pharmaceutical preparation manufacturing (June 1981 = 100; BLS)",
               "IPG3254S": "Industrial production: pharmaceutical and medicine manufacturing (2017 = 100; Federal Reserve G.17)",
               "CPIAUCNS": "CPI-U: all items (1982-84 = 100, NSA; BLS)"}


def fred_pharma():
    return _fred_write("fred_pharma", FRED_PHARMA)


MEDTECH_COMPANIES = [(1613103, "MDT", "USD"), (1800, "ABT", "USD"), (885725, "BSX", "USD"), (310764, "SYK", "USD"),
                     (1035267, "ISRG", "USD"), (1099800, "EW", "USD"), (1932393, "GEHC", "USD"), (10795, "BDX", "USD"),
                     (1136869, "ZBH", "USD"), (10456, "BAX", "USD"), (1093557, "DXCM", "USD"), (1145197, "PODD", "USD"),
                     (943819, "RMD", "USD"), (313616, "DHR", "USD"), (97745, "TMO", "USD"), (1110803, "ILMN", "USD"),
                     (920148, "LH", "USD"), (1022079, "DGX", "USD"), (1478242, "IQV", "USD"), (1090872, "A", "USD"),
                     (313216, "PHG", "EUR"), (1097149, "ALGN", "USD"), (1757898, "STE", "USD")]


def sec_medtech():
    """Annual figures of device, imaging, diagnostics, tools and contract research companies from their Forms 10-K and
    20-F (SEC company facts), in their reporting currency (billions; Philips in euros), with the same items and tag
    preferences as ``sec_auto``.  Medtronic's fiscal year ends in late April."""
    return _write("sec_medtech", ["ticker", "year_end", "currency"] + list(AUTO_ITEMS),
                  _sec_table(MEDTECH_COMPANIES, AUTO_ITEMS), [_sec_source(AUTO_ITEMS)])


FRED_MEDTECH = {"PCU339112339112": "PPI: surgical and medical instrument manufacturing (June 1985 = 100; BLS)",
                "PCU339113339113": "PPI: surgical appliance and supplies manufacturing (June 1983 = 100; BLS)",
                "IPN3391S": "Industrial production: medical equipment and supplies (2017 = 100, SA; Federal Reserve G.17)",
                "CES3133900001": "All employees: miscellaneous durable goods manufacturing, which includes medical "
                                 "equipment and supplies (thousands, SA; BLS)",
                "CPIAUCNS": "CPI-U: all items (1982-84 = 100, NSA; BLS)"}


def fred_medtech():
    return _fred_write("fred_medtech", FRED_MEDTECH)


OPENFDA = "https://api.fda.gov/device/"
FDA_DEVICE_COUNTS = {
    "k510_se": ("510k.json", 'decision_description:"Substantially Equivalent"', "decision_date",
                "510(k) decisions found substantially equivalent (cleared)"),
    "k510_all": ("510k.json", "", "decision_date", "all 510(k) decisions (including De Novo and not equivalent)"),
    "denovo": ("510k.json", "k_number:DEN*", "decision_date", "De Novo decisions (numbers beginning DEN)"),
    "pma_orig": ("pma.json", 'supplement_number:"" AND decision_code:APPR', "decision_date",
                 "original premarket approvals (PMA, not supplements) approved"),
    "pma_supp": ("pma.json", "decision_code:APPR AND _exists_:supplement_number", "decision_date",
                 "PMA records approved, originals and supplements"),
    "recall_c1": ("enforcement.json", 'classification:"Class I"', "report_date",
                  "Class I recall enforcement reports (the most serious class)"),
    "recall_all": ("enforcement.json", "", "report_date", "all device recall enforcement reports"),
}


def fda_devices():
    """Counts by year from openFDA's device endpoints (510(k), PMA and enforcement reports), each from a count query on
    the decision or report date, summed by calendar year.  openFDA's data are unvalidated by the FDA (its disclaimer)."""
    import time
    import urllib.parse

    years: dict = {}
    for key, (ep, search, field, _) in FDA_DEVICE_COUNTS.items():
        q = (f"search={urllib.parse.quote(search)}&" if search else "") + f"count={field}"
        res = json.loads(_get(f"{OPENFDA}{ep}?{q}"))["results"]
        time.sleep(0.5)
        for x in res:
            years.setdefault(int(x["time"][:4]), {}).setdefault(key, 0)
            years[int(x["time"][:4])][key] += x["count"]
    rows = [[y] + [years[y].get(k, 0) for k in FDA_DEVICE_COUNTS] for y in sorted(years) if y >= 1976]
    src = [OPENFDA + " (count queries; " + "; ".join(f"{k}: {v[3]}" for k, v in FDA_DEVICE_COUNTS.items()) + ")"]
    return _write("fda_devices", ["year"] + list(FDA_DEVICE_COUNTS), rows, src)


def fda_510k_panels(year: int = 2025):
    """510(k) clearances in one year by review panel (openFDA, advisory committee)."""
    import urllib.parse

    s = urllib.parse.quote(f'decision_description:"Substantially Equivalent" AND decision_date:[{year}0101 TO {year}1231]')
    res = json.loads(_get(f"{OPENFDA}510k.json?search={s}&count=advisory_committee_description.exact"))["results"]
    return _write("fda_510k_panels", ["panel", "count"], [[x["term"], x["count"]] for x in res],
                  [f"{OPENFDA}510k.json (510(k) clearances decided in {year}, by advisory committee)"])


CONSUMER_COMPANIES = [(80424, "PG", "USD"), (217410, "UL", "EUR"), (21665, "CL", "USD"), (55785, "KMB", "USD"),
                      (21076, "CLX", "USD"), (313927, "CHD", "USD"), (1001250, "EL", "USD"), (21344, "KO", "USD"),
                      (77476, "PEP", "USD"), (1103982, "MDLZ", "USD"), (1637459, "KHC", "USD"), (40704, "GIS", "USD"),
                      (47111, "HSY", "USD"), (764180, "MO", "USD"), (1413329, "PM", "USD"), (16918, "STZ", "USD"),
                      (14693, "BF-B", "USD"), (835403, "DEO", "USD"), (1668717, "BUD", "USD"), (1418135, "KDP", "USD"),
                      (23217, "CAG", "USD"), (91419, "SJM", "USD"), (16732, "CPB", "USD"), (865752, "MNST", "USD"),
                      (317540, "COKE", "USD")]
CONSUMER_ITEMS = dict(AUTO_ITEMS, advertising=[("us-gaap", "AdvertisingExpense"), ("us-gaap", "MarketingAndAdvertisingExpense"),
                                               ("us-gaap", "SellingAndMarketingExpense")])


HOME_COMPANIES = [(882184, "DHI", "USD"), (920760, "LEN", "USD"), (822416, "PHM", "USD"), (906163, "NVR", "USD"),
                  (794170, "TOL", "USD"), (795266, "KBH", "USD"), (833079, "MTH", "USD"), (1576940, "CCS", "USD"),
                  (799292, "MHO", "USD"), (1825088, "DFH", "USD"), (1580670, "LGIH", "USD"), (278166, "CVCO", "USD"),
                  (90896, "SKY", "USD"), (1316835, "BLDR", "USD"), (354950, "HD", "USD"), (60667, "LOW", "USD"),
                  (1805284, "RKT", "USD"), (1783398, "UWMC", "USD"), (310522, "FNMA", "USD"), (1026214, "FMCC", "USD"),
                  (1617640, "Z", "USD"), (1563190, "COMP", "USD"), (1801169, "OPEN", "USD"), (1687229, "INVH", "USD"),
                  (1562401, "AMH", "USD")]


def sec_homes():
    """Annual figures of homebuilders, manufactured-home makers, a building-products distributor, the home-improvement
    stores, mortgage lenders and the two government-sponsored enterprises, the portals and brokers, and single-family
    landlords, from their Forms 10-K (SEC company facts), with ``sec_fashion``'s items and tags."""
    return _write("sec_homes", ["ticker", "year_end", "currency"] + list(FASHION_ITEMS),
                  _sec_table(HOME_COMPANIES, FASHION_ITEMS), [_sec_source(FASHION_ITEMS)])


FRED_HOMES = {"CSUSHPINSA": "S&P CoreLogic Case-Shiller U.S. National Home Price Index (Jan 2000 = 100, NSA)",
              "MSPNHSUS": "Median sales price of new houses sold ($, NSA; Census and HUD)",
              "MSPUS": "Median sales price of houses sold, quarterly ($, NSA; Census and HUD)",
              "HOUST": "Housing starts: total (thousands of units, SAAR; Census)",
              "PERMIT": "New private housing units authorized by building permits (thousands, SAAR; Census)",
              "HSN1F": "New one-family houses sold (thousands, SAAR; Census)",
              "MSACSR": "Monthly supply of new houses (months' supply, SA; Census)",
              "MORTGAGE30US": "30-year fixed-rate mortgage average (percent, weekly; Freddie Mac PMMS)",
              "CUSR0000SEHA": "CPI-U: rent of primary residence (1982-84 = 100, SA; BLS)",
              "RHORUSQ156N": "Homeownership rate (percent, quarterly, NSA; Census HVS)",
              "RRVRUSQ156N": "Rental vacancy rate (percent, quarterly, NSA; Census HVS)",
              "HHMSDODNS": "Households and nonprofits: one-to-four-family residential mortgages, liability ($ billion, quarterly; Federal Reserve Z.1)",
              "MEHOINUSA646N": "Median household income ($, annual, current dollars; Census)",
              "DRSFRMACBS": "Delinquency rate on single-family residential mortgages, all commercial banks (percent, quarterly, SA)",
              "WPUIP2311001": "PPI: inputs to residential construction, goods (index, NSA; BLS)",
              "CPIAUCNS": "CPI-U: all items (1982-84 = 100, NSA; BLS)"}


def fred_homes():
    return _fred_write("fred_homes", FRED_HOMES)


AIR_COMPANIES = [(6201, "AAL", "USD"), (27904, "DAL", "USD"), (100517, "UAL", "USD"), (92380, "LUV", "USD"),
                 (1158463, "JBLU", "USD"), (766421, "ALK", "USD"), (1670076, "ULCC", "USD"), (1498710, "SAVE", "USD"),
                 (1362468, "ALGT", "USD"), (793733, "SKYW", "USD"), (1345105, "CPA", "USD"), (1038683, "RYAAY", "EUR"),
                 (1047716, "LTM", "USD"), (1378789, "AER", "USD"), (1487712, "AL", "USD"), (1597033, "SABR", "USD"),
                 (1172222, "HA", "USD")]


def sec_air():
    """Annual figures of American and other airlines, an aircraft lessor pair and a reservation system, from their Forms
    10-K and 20-F (SEC company facts), in their reporting currency (billions; Ryanair in euros, its fiscal year ending in
    March), with ``sec_fashion``'s items and tags.  Spirit's last filings are under Spirit Aviation Holdings from 2025."""
    return _write("sec_air", ["ticker", "year_end", "currency"] + list(FASHION_ITEMS),
                  _sec_table(AIR_COMPANIES, FASHION_ITEMS), [_sec_source(FASHION_ITEMS)])


FRED_AIR = {"ASM": "Available seat-miles, US air carriers, domestic and international, scheduled passenger flights (thousands, monthly, NSA; BTS)",
            "RPM": "Revenue passenger-miles, US air carriers, domestic and international (thousands, monthly, NSA; BTS)",
            "LOADFACTOR": "Load factor, US air carriers, domestic and international (percent, monthly, NSA; BTS)",
            "ENPLANE": "Enplanements, US air carriers, domestic and international (thousands, monthly, NSA; BTS)",
            "MJFUELUSGULF": "Kerosene-type jet fuel, US Gulf Coast ($ a gallon, monthly; EIA)",
            "CUUR0000SETG01": "CPI-U: airline fares (1982-84 = 100, NSA; BLS)",
            "CPIAUCNS": "CPI-U: all items (1982-84 = 100, NSA; BLS)",
            "CES4348100001": "All employees: air transportation (thousands, SA; BLS)",
            "PCU481111481111": "PPI by industry: scheduled passenger air transportation (Dec 1989 = 100, NSA; BLS)"}


def fred_air():
    return _fred_write("fred_air", FRED_AIR)


FREIGHT_COMPANIES = [(100885, "UNP", "USD"), (934612, "BNSF", "USD"), (277948, "CSX", "USD"), (702165, "NSC", "USD"),
                     (16868, "CNI", "CAD"), (16875, "CP", "CAD"), (1090727, "UPS", "USD"), (1048911, "FDX", "USD"),
                     (728535, "JBHT", "USD"), (1492691, "KNX", "USD"), (878927, "ODFL", "USD"), (1177702, "SAIA", "USD"),
                     (1166003, "XPO", "USD"), (1692063, "SNDR", "USD"), (793074, "WERN", "USD"), (1929561, "RXO", "USD"),
                     (853816, "LSTR", "USD"), (894405, "ARCB", "USD"), (1852244, "GXO", "USD"), (940942, "HUBG", "USD"),
                     (799233, "HTLD", "USD"), (1588823, "TFII", "USD"), (716006, "YELL", "USD"), (1677250, "ZTO", "CNY"),
                     (799167, "MRTN", "USD"), (1828108, "AUR", "USD")]


def sec_freight():
    """Annual figures of America's and Canada's freight railways (BNSF Railway's parent files its own 10-K), the parcel
    integrators, truckload, less-than-truckload and intermodal carriers, brokers, a contract-logistics firm, China's
    largest express firm and a driverless-truck developer, from their Forms 10-K, 40-F and 20-F (SEC company facts), in
    their reporting currency (billions; CN and CPKC in Canadian dollars, ZTO in yuan), with ``sec_fashion``'s items."""
    rows = _sec_table(FREIGHT_COMPANIES, FASHION_ITEMS)
    # BNSF tags only its related-party revenue as Revenues: take revenue as operating expenses plus operating income
    bnsf = _sec_table([(934612, "BNSF", "USD")], {"opex": [("us-gaap", "OperatingExpenses")],
                                                  "opinc": [("us-gaap", "OperatingIncomeLoss")]})
    fix = {r[1]: r[3] + r[4] for r in bnsf if r[3] is not None and r[4] is not None}
    k = 3 + list(FASHION_ITEMS).index("revenue")
    for r in rows:
        if r[0] == "BNSF":
            r[k] = fix.get(r[1])
    return _write("sec_freight", ["ticker", "year_end", "currency"] + list(FASHION_ITEMS), rows,
                  [_sec_source(FASHION_ITEMS) + "; BNSF's revenue is its operating expenses plus operating income"])


FRED_FREIGHT = {"RAILFRTCARLOADSD11": "Rail freight carloads (monthly, SA; BTS)",
                "RAILFRTINTERMODALD11": "Rail freight intermodal traffic, containers and trailers (monthly, SA; BTS)",
                "TRUCKD11": "Truck tonnage index (2015 = 100, SA; American Trucking Associations via BTS)",
                "FRGSHPUSM649NCIS": "Cass Freight Index: shipments (January 1990 = 1, NSA; Cass Information Systems)",
                "FRGEXPUSM649NCIS": "Cass Freight Index: expenditures (January 1990 = 1, NSA; Cass Information Systems)",
                "TSIFRGHT": "Transportation Services Index: freight (2000 = 100, SA; BTS)",
                "PCU484121484121": "PPI by industry: general freight trucking, long-distance truckload (Dec 2003 = 100, NSA; BLS)",
                "PCU484122484122": "PPI by industry: general freight trucking, long-distance less than truckload (Dec 2003 = 100, NSA; BLS)",
                "PCU482111482111": "PPI by industry: line-haul railroads (Dec 1996 = 100, NSA; BLS)",
                "PCU492110492110": "PPI by industry: couriers and express delivery services (Dec 2003 = 100, NSA; BLS)",
                "CES4348400001": "All employees: truck transportation (thousands, SA; BLS)",
                "CES4348200001": "All employees: rail transportation (thousands, SA; BLS)",
                "CES4349200001": "All employees: couriers and messengers (thousands, SA; BLS)",
                "GASDESW": "US No 2 diesel retail price ($ a gallon, weekly; EIA)",
                "CPIAUCNS": "CPI-U: all items (1982-84 = 100, NSA; BLS)",
                "ECOMSA": "E-commerce retail sales ($ million a quarter, SA; Census Bureau)"}


def fred_freight():
    return _fred_write("fred_freight", FRED_FREIGHT)


SHIP_COMPANIES = [(1654126, "ZIM", "USD"), (3453, "MATX", "USD"), (56047, "KEX", "USD"), (913290, "FRO", "USD"),
                  (1386716, "SBLK", "USD"), (1369241, "DAC", "USD"), (1430725, "GSL", "USD"), (1503584, "CMRE", "USD"),
                  (1483934, "STNG", "USD"), (1679049, "INSW", "USD"), (1326200, "GNK", "USD"), (1419945, "TNK", "USD"),
                  (1331284, "DHT", "USD"), (1772253, "FLNG", "USD"), (746515, "EXPD", "USD"), (1043277, "CHRW", "USD"),
                  (1604481, "CMBT", "USD"), (1000177, "NAT", "USD"), (1655891, "TRMD", "USD"), (1289877, "SFL", "USD"),
                  (1318885, "DSX", "USD"), (1415921, "NMM", "USD")]


def sec_ship():
    """Annual figures of container lines, shipowners (containerships let to the lines, crude and product tankers, dry
    bulk carriers, gas carriers), a barge operator and two freight forwarders, from their Forms 10-K and 20-F (SEC company
    facts), in US dollars (billions), with ``sec_fashion``'s items and tags (IFRS first, then US GAAP)."""
    return _write("sec_ship", ["ticker", "year_end", "currency"] + list(FASHION_ITEMS),
                  _sec_table(SHIP_COMPANIES, FASHION_ITEMS), [_sec_source(FASHION_ITEMS)])


FRED_SHIP = {"PCU483111483111": "PPI by industry: deep sea freight transportation (June 1988 = 100, NSA; BLS)",
             "PCU483483": "PPI by industry: water transportation (Dec 2003 = 100, NSA; BLS)",
             "MCOILBRENTEU": "Brent crude oil, Europe ($ a barrel, monthly average; EIA)",
             "BOPTIMP": "US imports of goods, balance of payments basis ($ million, monthly, SA; Census Bureau and BEA)",
             "CPIAUCNS": "CPI-U: all items (1982-84 = 100, NSA; BLS)"}


def fred_ship():
    return _fred_write("fred_ship", FRED_SHIP)


PORTWATCH = ("https://services9.arcgis.com/weJ1QsnbMYJlCHdG/arcgis/rest/services/Daily_Chokepoints_Data/FeatureServer/0/"
             "query")
CHOKEPOINTS = {"chokepoint1": "Suez Canal", "chokepoint2": "Panama Canal", "chokepoint4": "Bab el-Mandeb Strait",
               "chokepoint5": "Malacca Strait", "chokepoint6": "Strait of Hormuz", "chokepoint7": "Cape of Good Hope"}


def imf_portwatch():
    """IMF PortWatch's daily transit calls through six chokepoints (from AIS ship positions), averaged by month: all ships,
    container ships and tankers, and their capacity (deadweight tonnes); and every day for the Suez Canal from 10 March to
    10 April 2021, the week the Ever Given blocked it."""
    import urllib.parse

    out = []
    for pid, name in CHOKEPOINTS.items():
        rows, off = [], 0
        while True:
            q = urllib.parse.urlencode({"where": f"portid='{pid}'", "outFields": "date,n_total,n_container,n_tanker,capacity",
                                        "orderByFields": "date", "resultOffset": off, "resultRecordCount": 2000, "f": "json"})
            d = json.loads(_get(PORTWATCH + "?" + q))
            feats = d.get("features", [])
            rows += [f["attributes"] for f in feats]
            if len(feats) < 2000:
                break
            off += 2000
        by: dict = {}
        for r in rows:
            day = str(r["date"])[:10]
            by.setdefault(day[:7], []).append(r)
            if pid == "chokepoint1" and "2021-03-10" <= day <= "2021-04-10":
                for k in ("n_total", "n_container", "n_tanker"):
                    out.append([name, day, k, r[k]])
        for mth, rs in sorted(by.items()):
            for k in ("n_total", "n_container", "n_tanker", "capacity"):
                v = [r[k] for r in rs if r[k] is not None]
                if v:
                    out.append([name, mth, k + "_mean", round(sum(v) / len(v), 3)])
            out.append([name, mth, "days", len(rs)])
    return _write("imf_portwatch", ["chokepoint", "period", "measure", "value"], out,
                  ["https://portwatch.imf.org (IMF PortWatch, Daily Chokepoint Transit Calls; ArcGIS service "
                   "Daily_Chokepoints_Data; monthly means of daily values, daily values for the Suez Canal 10 March-10 April "
                   "2021; capacity in deadweight tonnes; estimates from AIS data)"])


def wb_ports():
    """Container port traffic (TEU: 20-foot equivalent units) for the world and selected countries, World Development
    Indicators IS.SHP.GOOD.TU (Lloyd's List Intelligence via the World Bank)."""
    url = ("https://api.worldbank.org/v2/country/WLD;CHN;USA;SGP;KOR;MYS;NLD;ARE;DEU;JPN;VNM;IND;BEL;ESP;GBR;EGY/indicator/"
           "IS.SHP.GOOD.TU?format=json&per_page=2000&date=2000:2025")
    d = json.loads(_get(url))
    out = [[r["country"]["value"], int(r["date"]), r["value"]] for r in d[1] if r["value"] is not None]
    return _write("wb_ports", ["country", "year", "teu"], sorted(out),
                  ["https://api.worldbank.org (World Development Indicators: IS.SHP.GOOD.TU, container port traffic, TEU)"])


PROPERTY_COMPANIES = [(1045609, "PLD", "USD"), (1571283, "REXR", "USD"), (49600, "EGP", "USD"), (1053507, "AMT", "USD"),
                      (1051470, "CCI", "USD"), (1034054, "SBAC", "USD"), (1101239, "EQIX", "USD"), (1297996, "DLR", "USD"),
                      (1063761, "SPG", "USD"), (726728, "O", "USD"), (879101, "KIM", "USD"), (910606, "REG", "USD"),
                      (912242, "MAC", "USD"), (34903, "FRT", "USD"), (1037540, "BXP", "USD"), (899689, "VNO", "USD"),
                      (1040971, "SLG", "USD"), (1025996, "KRC", "USD"), (1482512, "HPP", "USD"), (1364250, "DEI", "USD"),
                      (1035443, "ARE", "USD"), (915912, "AVB", "USD"), (906107, "EQR", "USD"), (912595, "MAA", "USD"),
                      (1393311, "PSA", "USD"), (1289490, "EXR", "USD"), (766704, "WELL", "USD"), (740260, "VTR", "USD"),
                      (1393818, "BX", "USD"), (1138118, "CBRE", "USD"), (1037976, "JLL", "USD"), (1628369, "CWK", "USD"),
                      (1465128, "STWD", "USD"), (1813756, "WE", "USD")]
PROPERTY_ITEMS = {"revenue": [("us-gaap", "Revenues"), ("us-gaap", "RevenueFromContractWithCustomerExcludingAssessedTax"),
                              ("us-gaap", "RealEstateRevenueNet"), ("us-gaap", "OperatingLeaseLeaseIncome")],
                  "operating_income": [("us-gaap", "OperatingIncomeLoss")],
                  "profit": [("us-gaap", "NetIncomeLoss"), ("us-gaap", "ProfitLoss")],
                  "interest": [("us-gaap", "InterestExpense"), ("us-gaap", "InterestExpenseNonoperating"),
                               ("us-gaap", "InterestExpenseDebt"), ("us-gaap", "InterestExpenseOperating")],
                  "depreciation": [("us-gaap", "DepreciationDepletionAndAmortization"), ("us-gaap", "DepreciationAndAmortization"),
                                   ("us-gaap", "DepreciationAmortizationAndAccretionNet")],
                  "impairment": [("us-gaap", "ImpairmentOfRealEstate"), ("us-gaap", "AssetImpairmentCharges")],
                  "real_estate": [("us-gaap", "RealEstateInvestmentPropertyNet")],
                  "assets": [("us-gaap", "Assets")]}


def sec_property():
    """Annual figures of property companies (logistics, towers, data centres, malls and shopping centres, net lease,
    offices, life-science campuses, flats, self-storage, senior housing), an alternative-asset manager, the services firms,
    a property lender and WeWork, from their Forms 10-K (SEC company facts), in US dollars (billions): revenue, operating
    income, net income, interest expense, depreciation, impairments, net real estate and assets.  REITs' revenue is
    mostly rent; interest and depreciation are tagged differently by different companies, so the first tag present wins."""
    return _write("sec_property", ["ticker", "year_end", "currency"] + list(PROPERTY_ITEMS),
                  _sec_table(PROPERTY_COMPANIES, PROPERTY_ITEMS), [_sec_source(PROPERTY_ITEMS)])


FRED_PROPERTY = {"BOGZ1FL075035503Q": "Commercial real estate price index, level (quarterly; Federal Reserve Z.1, Financial Accounts of the United States)",
                 "CREACBM027NBOG": "Commercial real estate loans, all commercial banks ($ billion, monthly, NSA; Federal Reserve H.8)",
                 "DRCRELEXFACBS": "Delinquency rate on commercial real estate loans excluding farmland, all commercial banks (percent, quarterly, SA; Federal Reserve)",
                 "GS10": "10-year Treasury constant maturity rate (percent, monthly average; Federal Reserve H.15)",
                 "BAA": "Moody's seasoned Baa corporate bond yield (percent, monthly average; via FRED)",
                 "TLOFCONS": "Construction spending: office, including data centres ($ million, SAAR; Census Bureau)",
                 "TLCOMCONS": "Construction spending: commercial, including warehouses and shops ($ million, SAAR; Census Bureau)",
                 "ECOMPCTSA": "E-commerce retail sales as a percent of total retail sales (quarterly, SA; Census Bureau)",
                 "PCU531120531120": "PPI by industry: lessors of nonresidential buildings (Dec 1995 = 100, NSA; BLS)",
                 "CPIAUCNS": "CPI-U: all items (1982-84 = 100, NSA; BLS)"}


def fred_property():
    return _fred_write("fred_property", FRED_PROPERTY)


CONSTRUCTION_COMPANIES = [(1124198, "FLR", "USD"), (52988, "J", "USD"), (868857, "ACM", "USD"), (1050915, "PWR", "USD"),
                          (105634, "EME", "USD"), (15615, "MTZ", "USD"), (861459, "GVA", "USD"), (77543, "TPC", "USD"),
                          (67215, "DY", "USD"), (1035983, "FIX", "USD"), (874238, "STRL", "USD"), (1357615, "KBR", "USD"),
                          (1361538, "PRIM", "USD"), (700923, "MYRG", "USD"), (100591, "AGX", "USD"),
                          (1796209, "APG", "USD"), (831641, "TTEK", "USD"), (1718227, "ROAD", "USD"),
                          (1396009, "VMC", "USD"), (916076, "MLM", "USD"), (849395, "CRH", "USD"), (918646, "EXP", "USD"),
                          (1364479, "HRI", "USD"), (1468522, "FER", "EUR")]


def sec_construction():
    """Annual figures of contractors, engineering firms, building-materials companies, an equipment renter and a
    concession owner (Ferrovial, in euros) from their Forms 10-K and 20-F (SEC company facts), with ``sec_fashion``'s
    items and tags."""
    return _write("sec_construction", ["ticker", "year_end", "currency"] + list(FASHION_ITEMS),
                  _sec_table(CONSTRUCTION_COMPANIES, FASHION_ITEMS), [_sec_source(FASHION_ITEMS)])


FRED_CONSTRUCTION = {"TTLCONS": "Total construction spending ($ million, SAAR; Census, value put in place)",
                     "TLRESCONS": "Construction spending: residential ($ million, SAAR; Census)",
                     "TLNRESCONS": "Construction spending: nonresidential ($ million, SAAR; Census)",
                     "TLPBLCONS": "Construction spending: public ($ million, SAAR; Census)",
                     "PRMFGCONS": "Construction spending: private manufacturing ($ million, SAAR; Census)",
                     "TLHWYCONS": "Construction spending: highway and street ($ million, SAAR; Census)",
                     "TLPWRCONS": "Construction spending: power ($ million, SAAR; Census)",
                     "TLCOMCONS": "Construction spending: commercial ($ million, SAAR; Census)",
                     "TLOFCONS": "Construction spending: office ($ million, SAAR; Census)",
                     "USCONS": "All employees: construction (thousands, SA; BLS)",
                     "MANEMP": "All employees: manufacturing (thousands, SA; BLS)",
                     "PAYEMS": "All employees: total nonfarm (thousands, SA; BLS)",
                     "AWHAECON": "Average weekly hours of all employees: construction (SA; BLS)",
                     "WPUSI012011": "PPI: inputs to construction industries, materials and components (1982 = 100, NSA; BLS)",
                     "PCU236221236221": "PPI: new warehouse building construction (Dec 2004 = 100, NSA; BLS)",
                     "WPU081": "PPI: lumber (1982 = 100, NSA; BLS)",
                     "CPIAUCNS": "CPI-U: all items (1982-84 = 100, NSA; BLS)"}


def fred_construction():
    return _fred_write("fred_construction", FRED_CONSTRUCTION)


def bea_long():
    """Real value added (chain-type quantity index) and its price index for construction, manufacturing and all
    industries, 1947-2025: BEA's historical tables (1947-1997) linked at 1997 to its current release (1997-2025, 2017 =
    100)."""
    import openpyxl

    z = zipfile.ZipFile(io.BytesIO(_get(BEA + "iTables%20Static%20Files/AllTablesHist.zip")))
    old = openpyxl.load_workbook(io.BytesIO(z.read("GDPbyInd_VA_1947-1997.xlsx")), read_only=True)
    new = openpyxl.load_workbook(io.BytesIO(_get(BEA + "Release/XLS/GDPxInd/ValueAdded.xlsx")), read_only=True)
    names = {"construction": "Construction", "manufacturing": "Manufacturing", "all": "Gross domestic product"}
    out = []
    for measure, osheet, nsheet in (("quantity", "ChainQtyIndexes", "TVA103-A"), ("price", "ChainPriceIndexes", "TVA104-A")):
        def series(ws, first_col):
            rows = list(ws.iter_rows(values_only=True))
            hdr = [r for r in rows if r and r[0] == "Line"][0]
            years = [int(y) for y in hdr[first_col:] if y]
            got = {}
            for r in rows:
                if r and r[1]:
                    nm = str(r[1]).strip()
                    for k, target in names.items():
                        if nm.startswith(target) and k not in got:
                            got[k] = {y: v for y, v in zip(years, r[first_col:first_col + len(years)])
                                      if isinstance(v, (int, float))}
            return got
        o, n = series(old[osheet], 2), series(new[nsheet], 3)
        for k in names:
            link = n[k][1997] / o[k][1997]
            for y in range(1947, 2026):
                v = n[k].get(y) if y >= 1997 else (o[k][y] * link if y in o[k] else None)
                out.append([measure, k, y, round(v, 4) if v is not None else None])
    return _write("bea_long", ["measure", "industry", "year", "index_2017"], out,
                  [BEA + "iTables%20Static%20Files/AllTablesHist.zip (GDPbyInd_VA_1947-1997: ChainQtyIndexes, "
                         "ChainPriceIndexes)", BEA + "Release/XLS/GDPxInd/ValueAdded.xlsx (TVA103-A, TVA104-A, 2017=100)"])


FASHION_COMPANIES = [(320187, "NKE", "USD"), (1397187, "LULU", "USD"), (103379, "VFC", "USD"), (78239, "PVH", "USD"),
                     (1037038, "RL", "USD"), (1116132, "TPR", "USD"), (1530721, "CPRI", "USD"), (94845, "LEVI", "USD"),
                     (39911, "GAP", "USD"), (109198, "TJX", "USD"), (745732, "ROST", "USD"), (1579298, "BURL", "USD"),
                     (1336917, "UAA", "USD"), (910521, "DECK", "USD"), (1050797, "COLM", "USD"), (1018840, "ANF", "USD"),
                     (919012, "AEO", "USD"), (912615, "URBN", "USD"), (832988, "SIG", "USD"), (1858985, "ONON", "CHF"),
                     (1977102, "BIRK", "EUR"), (794367, "M", "USD"), (885639, "KSS", "USD")]


FASHION_ITEMS = dict(AUTO_ITEMS,
                     revenue=AUTO_ITEMS["revenue"] + [("ifrs-full", "RevenueFromContractsWithCustomers"),
                                                      ("us-gaap", "RevenueFromContractWithCustomerIncludingAssessedTax")],
                     cost=AUTO_ITEMS["cost"] + [("us-gaap", "CostOfGoodsAndServiceExcludingDepreciationDepletionAndAmortization")])


def sec_fashion():
    """Annual figures of apparel, footwear, luxury and off-price companies from their Forms 10-K and 20-F (SEC company
    facts), in their reporting currency (billions; On in Swiss francs, Birkenstock in euros), with ``sec_auto``'s items and three
    more tags (On and Birkenstock tag revenue from contracts; TJX tags its sales including assessed taxes; Capri and
    Abercrombie tag the cost of goods excluding depreciation).
    Most of these companies' fiscal years end around the end of January or early February of the next calendar year."""
    return _write("sec_fashion", ["ticker", "year_end", "currency"] + list(FASHION_ITEMS),
                  _sec_table(FASHION_COMPANIES, FASHION_ITEMS), [_sec_source(FASHION_ITEMS)])


FRED_FASHION = {"CPIAPPNS": "CPI-U: apparel (1982-84 = 100, NSA; BLS)",
                "CES3231500001": "All employees: apparel manufacturing (thousands, SA; BLS)",
                "IPG315S": "Industrial production: apparel and leather goods (2017 = 100, SA; Federal Reserve G.17)",
                "CPIAUCNS": "CPI-U: all items (1982-84 = 100, NSA; BLS)",
                "EXUSEU": "US dollars to one euro (monthly average of noon buying rates in New York; Federal Reserve H.10)",
                "EXSZUS": "Swiss francs to one US dollar (monthly average of noon buying rates in New York; Federal Reserve H.10)"}


def fred_fashion():
    return _fred_write("fred_fashion", FRED_FASHION)


COMTRADE_APPAREL_REPORTERS = {156: "China", 50: "Bangladesh", 704: "Vietnam", 699: "India", 792: "Turkey", 380: "Italy",
                              116: "Cambodia"}
COMTRADE_APPAREL_HS = {"61": "articles of apparel, knitted or crocheted", "62": "articles of apparel, not knitted or crocheted"}


def comtrade_apparel(years=range(2010, 2026)):
    """Exports of clothing (HS chapters 61 and 62) to the world by seven large exporters, as each reported them to UN
    Comtrade (annual; US dollars; UN Comtrade's public preview API).  Bangladesh reports late and with gaps."""
    import time

    out = []
    for y in years:
        url = ("https://comtradeapi.un.org/public/v1/preview/C/A/HS?reporterCode={}&period={}&partnerCode=0&cmdCode={}"
               "&flowCode=X").format(",".join(str(k) for k in COMTRADE_APPAREL_REPORTERS), y, ",".join(COMTRADE_APPAREL_HS))
        j = json.loads(_get(url))
        for r in j.get("data", []):
            if r.get("customsCode") != "C00" or r.get("motCode") != 0 or r.get("partner2Code") != 0:
                continue
            out.append([y, r["cmdCode"], COMTRADE_APPAREL_REPORTERS[r["reporterCode"]], round(r["primaryValue"] / 1e9, 4)])
        time.sleep(1.5)
    out.sort(key=lambda r: (r[0], r[1], r[2]))
    return _write("comtrade_apparel", ["year", "hs", "reporter", "exports_usd_bn"], out,
                  ["https://comtradeapi.un.org/public/v1/preview/C/A/HS (UN Comtrade; exports to the world as reported "
                   "by each country, annual; " + "; ".join(f"HS {k}: {v}" for k, v in COMTRADE_APPAREL_HS.items()) + ")"])


FRED_CONSUMER = {"CUUR0000SAG1": "CPI-U: personal care (1982-84 = 100, NSA; BLS)",
                 "CUUR0000SEGA": "CPI-U: tobacco and smoking products (1982-84 = 100, NSA; BLS)",
                 "CUUR0000SAF11": "CPI-U: food at home (1982-84 = 100, NSA; BLS)",
                 "PCU32563256": "PPI: soap, cleaning compound and toilet preparation manufacturing (Dec 1984 = 100; BLS)",
                 "CPIAUCNS": "CPI-U: all items (1982-84 = 100, NSA; BLS)"}


def fred_consumer():
    return _fred_write("fred_consumer", FRED_CONSUMER)


def sec_consumer():
    """Annual figures of household, personal-care, food, drink and tobacco makers from their Forms 10-K and 20-F (SEC
    company facts), in their reporting currency (billions; Unilever in euros), with ``sec_auto``'s items and tag
    preferences and advertising (AdvertisingExpense, else MarketingAndAdvertisingExpense, else SellingAndMarketingExpense).
    Procter & Gamble's fiscal year ends in June, Clorox's in June, General Mills' in May, Constellation's in February,
    Brown-Forman's in April, Diageo's in June, Conagra's in May, Smucker's in April, Campbell's in July or August."""
    return _write("sec_consumer", ["ticker", "year_end", "currency"] + list(CONSUMER_ITEMS),
                  _sec_table(CONSUMER_COMPANIES, CONSUMER_ITEMS), [_sec_source(CONSUMER_ITEMS)])


FRED_AERO = {"ANAPNO": "New orders: nondefense aircraft and parts ($ million a month, SA; Census M3)",
             "ANAPVS": "Shipments: nondefense aircraft and parts ($ million a month, SA; Census M3)",
             "ADAPNO": "New orders: defense aircraft and parts ($ million a month, SA; Census M3)",
             "ADAPVS": "Shipments: defense aircraft and parts ($ million a month, SA; Census M3)",
             "IPG3364S": "Industrial production: aerospace products and parts (2017 = 100; Federal Reserve G.17)",
             "PCU336411336411": "PPI: aircraft manufacturing (Dec 1985 = 100; BLS)",
             "FDEFX": "Federal government: national defense consumption expenditures and gross investment ($ billion, "
                      "SAAR; BEA)",
             "CPIAUCNS": "CPI-U: all items (1982-84 = 100, NSA; BLS)"}


def fred_aero():
    """Monthly series for Part 18 (via FRED): orders and shipments of civil and defence aircraft since 1992, aerospace
    output since 1972, aircraft producer prices since 1985, and America's defence spending since 1947."""
    return _fred_write("fred_aero", FRED_AERO)


SIPRI = "https://www.sipri.org/sites/default/files/SIPRI-Milex-data-1949-2025_v1.2.xlsx"


def sipri_milex():
    """SIPRI's military expenditure by country, 1949-2025: constant (2024) US$ million, and share of GDP (sheets of the
    SIPRI Military Expenditure Database, release of April 2026, v1.2)."""
    import openpyxl

    wb = openpyxl.load_workbook(io.BytesIO(_get(SIPRI)), read_only=True, data_only=True)
    out = []
    for sheet, measure in (("Constant (2024) US$", "usd2024_m"), ("Share of GDP", "share_gdp")):
        ws = wb[sheet]
        years = None
        for r in ws.iter_rows(values_only=True):
            if r and r[0] == "Country":
                years = r
                continue
            if years is None or not r or not r[0] or not isinstance(r[0], str):
                continue
            for y, v in zip(years, r):
                if isinstance(y, int) and isinstance(v, (int, float)):
                    out.append([measure, r[0].strip(), y, round(float(v), 6)])
    ws = wb["Regional totals"]
    years = None
    for r in ws.iter_rows(values_only=True):
        if r and r[0] == "Region":
            years = r
            continue
        if years is not None and r and isinstance(r[0], str) and r[0].strip() == "World":
            for y, v in zip(years, r):
                if isinstance(y, int) and isinstance(v, (int, float)):
                    out.append(["usd2024_m", "World", y, round(float(v) * 1000, 3)])
            break
    return _write("sipri_milex", ["measure", "country", "year", "value"], out,
                  [SIPRI + " (SIPRI Military Expenditure Database; constant 2024 US$ m and share of GDP; SIPRI "
                   "estimates included as published)"])


JOBS = {"sec_freight": sec_freight, "fred_freight": fred_freight, "sec_air": sec_air, "fred_air": fred_air, "sec_ship": sec_ship, "fred_ship": fred_ship, "imf_portwatch": imf_portwatch, "wb_ports": wb_ports, "sec_property": sec_property, "fred_property": fred_property, "sec_homes": sec_homes, "fred_homes": fred_homes,
        "sec_construction": sec_construction, "fred_construction": fred_construction, "bea_long": bea_long,
        "sec_fashion": sec_fashion, "fred_fashion": fred_fashion, "comtrade_apparel": comtrade_apparel,
        "fred_consumer": fred_consumer, "sec_consumer": sec_consumer, "sec_medtech": sec_medtech, "fred_medtech": fred_medtech, "fda_devices": fda_devices, "fda_510k_panels": fda_510k_panels,
        "sec_aero": sec_aero, "fred_aero": fred_aero, "sipri_milex": sipri_milex, "census_auto": census_auto, "sec_auto": sec_auto, "fred_auto": fred_auto, "owid_ev": owid_ev, "comtrade_cars": comtrade_cars,
        "sec_pharma": sec_pharma, "fred_pharma": fred_pharma, "sec_mach": sec_mach, "fred_mach": fred_mach, "owid_robots": owid_robots, "comtrade_mach": comtrade_mach,
        "eia_aeo17": eia_aeo17, "comtrade_us_m": comtrade_us_m, "bls_elec": bls_elec, "fred_elec": fred_elec, "comtrade_us": comtrade_us, "fred_chips": fred_chips, "owid_chips": owid_chips, "sec_foreign": sec_foreign, "wb_water": wb_water, "bls_water": bls_water, "fred_waste": fred_waste, "epa_msw": epa_msw, "eia_930": eia_930, "eia_mer": eia_mer, "fred_power": fred_power, "owid_elec": owid_elec, "owid_chem": owid_chem, "fred_chem": fred_chem, "eia_ngl": eia_ngl, "eurostat_chem": eurostat_chem, "usgs_heavy": usgs_heavy, "fred_heavy": fred_heavy, "owid_co2": owid_co2, "ers_food_dollar": ers_food_dollar, "ers_costs": ers_costs, "ers_farm_income": ers_farm_income, "owid_ag": owid_ag, "fred_food": fred_food, "ne_land": ne_land, "usgs_ds140": usgs_ds140, "fred_metals": fred_metals, "sec_ifrs": sec_ifrs, "eia_gas": eia_gas, "eia_petroleum": eia_petroleum, "eia_intl": eia_intl, "eia_pump": eia_pump, "fred_energy": fred_energy, "fred_market": fred_market, "owid_tech": owid_tech, "sec_quarterly": sec_quarterly, "fred_cycle": fred_cycle, "esef_maersk": esef_maersk, "damodaran_roc": damodaran_roc, "census_conc": census_conc, "eia_power": eia_power, "fred_pay": fred_pay, "bea_real": bea_real, "sec_annual": sec_annual, "fred_prices": fred_prices, "census_susb": census_susb, "bea_va": bea_va, "wb_mfg_usd": wb_mfg_usd, "bea_hist": bea_hist, "bea_io": bea_io, "fred_jobs": fred_jobs, "wb_shares": wb_shares}

if __name__ == "__main__":
    names = list(JOBS) if "--all" in sys.argv else sys.argv[1:]
    for n in names:
        print("wrote", JOBS[n]())
