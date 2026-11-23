"""Refresh the Filing Room's frozen extracts from their public sources (SOURCES.md).

    python -m explainer.industry.data.fetch bea_va       # BEA value added by industry, 2025, and its components
    python -m explainer.industry.data.fetch bea_hist     # BEA value added as a share of GDP, 1947-2025
    python -m explainer.industry.data.fetch bea_io       # BEA 2023 sector use table and direct requirements
    python -m explainer.industry.data.fetch fred_jobs    # FRED payroll employment by industry, annual
    python -m explainer.industry.data.fetch wb_shares    # World Bank: industry shares of GDP by country
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
UA = {"User-Agent": "Mozilla/5.0 (explainer-videos research)"}
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

                return subprocess.run(["curl", "-sL", "--max-time", "120", url], check=True,
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
    cols = {k: hdr.index(k) for k in ("F010", "F030", "F040", "F050")}
    out = []
    for r in rows[7:]:
        if r[0] in IO_CODES:
            out.append([r[0], r[1]] + [num(r[i]) for i in idx] + [num(r[cols[k]]) for k in ("F010", "F030", "F040",
                                                                                          "F050")] + [num(r[-1])])
    # value added and total industry output rows
    for r in rows[7:]:
        if r[0] in ("Used", "Other", "V001", "V002", "V003"):  # an industry's output is its column's sum
            out.append([r[0], r[1]] + [num(r[i]) for i in idx] + [0, 0, 0, 0, 0])
    return _write("bea_io_2023", ["code", "name"] + IO_CODES + ["pce", "inventories", "exports", "imports",
                                                                "commodity_output"], out,
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


JOBS = {"bea_va": bea_va, "bea_hist": bea_hist, "bea_io": bea_io, "fred_jobs": fred_jobs, "wb_shares": wb_shares}

if __name__ == "__main__":
    names = list(JOBS) if "--all" in sys.argv else sys.argv[1:]
    for n in names:
        print("wrote", JOBS[n]())
