"""Every number in Part 2 of *Industry, Built* ("The Economy on One Page"), from the Filing Room and the Register.

    python -m videos.industry.industry2.compute        # prints the film's numbers

Items:
    companies   the largest US-listed companies by sales, by operating income and by employees (10-Ks, 2025)
    va          value added by sector, 2025, its share of GDP then and in 1997, and its split into wages, taxes and
                operating surplus (BEA)
    jobs        payroll jobs by sector, 2025, and value added per job (BLS via FRED, BEA)
    pay         average hourly earnings by sector, 2025 (BLS via FRED), beside value added per job
    io          the 2023 sector table: direct requirements, the Leontief inverse, each sector's total requirements,
                upstreamness (BEA; Antras, Chor, Fally and Hillberry 2012)
    history     value added shares 1947-2025; manufacturing jobs and output since 1939 and 1987
    prices      consumer prices of services and goods and production workers' hourly pay, 2000-2025 (BLS)
    growth      real value added by industry, 2015 to 2025, every BEA line (chain-type quantity indexes)
    world       manufacturing and agriculture as shares of GDP by country (World Bank; the US from BEA)
    buyers      the final uses of the 2023 table: households, investment, government, exports less imports
    household   a dollar of household (and of investment and government) spending followed back through the table to
                each industry's value added and to imports
    firms       employer firms, jobs and receipts by firm size, 2022, and each sector's share of jobs in firms of
                20,000 or more (Census, Statistics of US Businesses)
    leontief    payroll jobs in 1983 and 2025, for Leontief's forecast
"""

from __future__ import annotations

import functools

import numpy as np

from explainer.industry.data.fetch import IO_CODES, read
from explainer.industry.register import get

IO_NAMES = {"11": "Farms", "21": "Mining", "22": "Utilities", "23": "Construction", "31G": "Manufacturing",
            "42": "Wholesale", "44RT": "Retail", "48TW": "Transport", "51": "Information",
            "FIRE": "Finance and real estate", "PROF": "Business services", "6": "Education and health",
            "7": "Leisure and hotels", "81": "Other services", "G": "Government"}

# BEA sectors (bea_va_2025.csv) against payroll series (fred_jobs.csv)
JOB_MAP = [("Manufacturing", ["Manufacturing"], "MANEMP"), ("Retail trade", ["Retail trade"], "USTRADE"),
           ("Wholesale trade", ["Wholesale trade"], "USWTRADE"), ("Construction", ["Construction"], "USCONS"),
           ("Transportation", ["Transportation and warehousing"], "CES4300000001"),
           ("Information", ["Information"], "USINFO"),
           ("Finance, insurance, real estate", ["Finance and insurance", "Real estate"], "USFIRE"),
           ("Professional and business services", ["Professional and technical services", "Management of companies",
                                                   "Administrative and waste services"], "USPBS"),
           ("Health care and social assistance", ["Health care and social assistance"], "CES6562000001"),
           ("Education (private)", ["Educational services"], "CES6561000001"),
           ("Leisure and hospitality", ["Arts and recreation", "Hotels and restaurants"], "USLAH"),
           ("Other services", ["Other services"], "USSERV"), ("Government", ["Government"], "USGOVT"),
           ("Mining", ["Mining"], "CES1021000001"), ("Utilities", ["Utilities"], "CES4422000001")]


@functools.lru_cache(maxsize=None)
def results() -> dict:
    R = {}
    # --- companies -----------------------------------------------------------------------------------------------
    R["companies"] = dict(
        by_sales=[("Amazon", get("rev.amazon.2025")), ("Walmart", get("rev.walmart.fy2026")),
                  ("UnitedHealth", get("rev.unitedhealth.2025")), ("Apple", get("rev.apple.fy2025")),
                  ("McKesson", get("rev.mckesson.fy2026"))],
        by_profit=[("Apple", get("oi.apple.fy2025")), ("NVIDIA", get("oi.nvidia.fy2026")),
                   ("Alphabet", get("oi.alphabet.2025")), ("Microsoft", get("oi.microsoft.fy2025")),
                   ("Meta", get("oi.meta.2025")), ("Amazon", get("oi.amazon.2025"))],
        by_jobs=[("Walmart", get("emp.walmart.fy2026")), ("Amazon", get("emp.amazon.2025")),
                 ("UnitedHealth", get("emp.unitedhealth.2025")), ("Microsoft", get("emp.microsoft.fy2026")),
                 ("Alphabet", get("emp.alphabet.2025")), ("Apple", get("emp.apple.fy2025")),
                 ("McKesson", get("emp.mckesson.fy2026")), ("NVIDIA", get("emp.nvidia.fy2026"))],
        mck=dict(rev=get("rev.mckesson.fy2026"), gp=get("gp.mckesson.fy2026")),
        aws=dict(sales=get("rev.aws.2025"), oi=get("oi.aws.2025"), amzn_sales=get("rev.amazon.2025"), amzn_oi=get("oi.amazon.2025")),
        per_worker=dict(nvidia=get("oi.nvidia.fy2026") * 1e9 / get("emp.nvidia.fy2026"),
                        walmart=get("oi.walmart.fy2026") * 1e9 / get("emp.walmart.fy2026")),
    )

    # --- value added by sector, 2025 ------------------------------------------------------------------------------
    va = read("bea_va_2025")
    R["va"] = [dict(sector=r["sector"], va=r["va_musd"] / 1e3, pct=r["pct_gdp"], pct97=r["pct_gdp_1997"],
                    comp=r["comp_pct"], tax=r["tax_pct"], gos=r["gos_pct"]) for r in va]
    R["gdp"] = R["va"][0]["va"] / 1e3  # $ trillions
    assert abs(R["gdp"] - get("gdp.2025")) < 0.01
    sectors = {d["sector"]: d for d in R["va"][1:]}

    # --- jobs, 2025, and value added per job -----------------------------------------------------------------
    jobs = {int(r["year"]): r for r in read("fred_jobs")}
    j25 = jobs[2025]
    R["jobs"] = []
    for name, secs, series in JOB_MAP:
        v = sum(sectors[s]["va"] for s in secs)
        n = j25[series] / 1e3  # millions
        R["jobs"].append(dict(sector=name, jobs=n, va=v, per_job=v * 1e9 / (n * 1e6)))
    R["jobs_total"] = j25["PAYEMS"] / 1e3

    # --- what each job pays: average hourly earnings, 2025 (BLS via FRED), beside value added per job ------------------
    from explainer.industry.data.fetch import FRED_PAY
    pay = {int(r["year"]): r for r in read("fred_pay")}[2025]
    PAY_MAP = {"Mining": "CES1000000003", "Construction": "CES2000000003", "Manufacturing": "CES3000000003",
               "Wholesale trade": "CES4142000003", "Retail trade": "CES4200000003",
               "Transportation": "CES4300000003", "Utilities": "CES4422000003", "Information": "CES5000000003",
               "Finance, insurance, real estate": "CES5500000003",
               "Professional and business services": "CES6000000003",
               "Health care and social assistance": "CES6500000003", "Leisure and hospitality": "CES7000000003",
               "Other services": "CES8000000003"}
    per_job = {d["sector"]: d["per_job"] for d in R["jobs"]}
    R["pay"] = dict(total=pay["CES0500000003"], series={k: FRED_PAY[v] for k, v in PAY_MAP.items()},
                    rows=sorted(([k, pay[v], per_job[k]] for k, v in PAY_MAP.items()), key=lambda t: -t[1]))

    # --- the input-output table, 2023 ------------------------------------------------------------------------------
    rows = read("bea_io_2023")
    Z = np.array([[r[c] for c in IO_CODES] for r in rows if r["code"] in IO_CODES])
    X = np.array([sum((r[c] or 0) for r in rows) for c in IO_CODES])  # industry output: the column sums
    io_rows = {r["code"]: r for r in rows if r["code"] in IO_CODES}
    rows_by = {r["code"]: r for r in rows}
    A = Z / X
    L = np.linalg.inv(np.eye(len(IO_CODES)) - A)
    Y = np.array([io_rows[c]["commodity_output"] for c in IO_CODES])
    ex = np.array([io_rows[c]["exports"] for c in IO_CODES])
    im = np.array([io_rows[c]["imports"] for c in IO_CODES])
    inv = np.array([io_rows[c]["inventories"] for c in IO_CODES])
    D = Z / (Y - ex - im - inv)[:, None]  # Antras et al.: the share of each commodity's domestic use by each industry
    U = np.linalg.solve(np.eye(len(IO_CODES)) - D, np.ones(len(IO_CODES)))
    R["io"] = dict(codes=IO_CODES, names=[IO_NAMES[c] for c in IO_CODES], A=A.tolist(), L=L.tolist(),
                   total=L.sum(axis=0).tolist(), direct=A.sum(axis=0).tolist(), upstream=U.tolist(),
                   output=(X / 1e6).tolist(),  # $ trillions
                   output_total=X.sum() / 1e6,
                   va_total=sum(sum((r[c] or 0) for c in IO_CODES) for r in rows if r["code"] in ("V001", "V002",
                                                                                                 "V003")) / 1e6)

    # --- who buys: the final uses of the 2023 table ----------------------------------------------------------------
    FIN = ("pce", "investment", "government", "exports", "imports", "inventories")
    every = [r for r in rows if r["code"] in IO_CODES + ["Used", "Other"]]
    fin_tot = {k: sum(r[k] or 0 for r in every) / 1e6 for k in FIN}  # $ trillions
    by_sector = {IO_NAMES[c]: {k: (io_rows[c][k] or 0) / 1e6 for k in FIN} for c in IO_CODES}
    R["buyers"] = dict(total=fin_tot, gdp=sum(fin_tot.values()), by_sector=by_sector)

    # --- a household's dollar, followed back through the table ------------------------------------------------------
    # Each commodity's imports are a share m of its domestic supply, the same for every user (BEA's convention for
    # domestic requirements); the domestic part of each purchase sets off rounds of domestic buying, and every
    # industry's value added is its value-added coefficient times its output.
    VA = np.array([sum(rows_by[v][c] for v in ("V001", "V002", "V003")) for c in IO_CODES])
    vcoef = VA / X
    supply = Y + (-im) - ex
    m = np.clip(-im / supply, 0, 1)

    def follow(key):
        c = np.array([io_rows[k][key] for k in IO_CODES])
        c = c / c.sum()
        xd = np.linalg.solve(np.eye(len(IO_CODES)) - (1 - m)[:, None] * A, (1 - m) * c)
        va = vcoef * xd
        return dict(bought=c.tolist(), va=va.tolist(), imports=float((m * (c + A @ xd)).sum()),
                    other=float(1 - va.sum() - (m * (c + A @ xd)).sum()))
    R["household"] = dict(names=[IO_NAMES[c] for c in IO_CODES], import_share=m.tolist(), pce=follow("pce"),
                          investment=follow("investment"), government=follow("government"))

    # --- firms by size, 2022 (Census, Statistics of US Businesses) ------------------------------------------------
    sz = read("census_susb_2022")
    us = {r["size"]: r for r in sz if r["naics"] == "--"}
    BINS = [("1 to 4", ["02: <5 employees"]), ("5 to 19", ["03: 5-9 employees", "04:10-14 employees",
                                                           "05: 15-19 employees"]),
            ("20 to 99", ["07: 20-24 employees", "08: 25-29 employees", "09: 30-34 employees",
                          "10: 35-39 employees", "11: 40-49 employees", "12: 50-74 employees", "13: 75-99 employees"]),
            ("100 to 499", ["14: 100-149 employees", "15: 150-199 employees", "16: 200-299 employees",
                            "17: 300-399 employees", "18: 400-499 employees"]),
            ("500 to 4,999", ["20: 500-749 employees", "21: 750-999 employees", "22: 1,000-1,499 employees",
                              "23: 1,500-1,999 employees", "24: 2,000-2,499 employees", "25: 2,500-4,999 employees"]),
            ("5,000 or more", ["26: 5,000+ employees"])]
    T0 = us["01: Total"]
    bins = [dict(label=lab, firms=sum(us[k]["firms"] for k in ks), jobs=sum(us[k]["employment"] for k in ks),
                 receipts=sum(us[k]["receipts_k"] for k in ks)) for lab, ks in BINS]
    assert abs(sum(b["firms"] for b in bins) - T0["firms"]) < 10 and abs(sum(b["jobs"] for b in bins) -
                                                                         T0["employment"]) < 10
    giants = us["11: 20,000+ employees"]
    sectors_sz = {}
    for r in sz:
        if r["naics"] != "--":
            sectors_sz.setdefault(r["sector"], {})[r["size"][:2]] = r
    R["firms"] = dict(total=dict(firms=T0["firms"], jobs=T0["employment"], receipts=T0["receipts_k"]), bins=bins,
                      giants=dict(firms=giants["firms"], jobs=giants["employment"], receipts=giants["receipts_k"]),
                      small=dict(firms=us["19: <500 employees"]["firms"], jobs=us["19: <500 employees"]["employment"]),
                      sectors=sorted(([n, d["11"]["employment"] / d["01"]["employment"],
                                       d["02"]["employment"] / d["01"]["employment"], d["01"]["employment"]]
                                      for n, d in sectors_sz.items() if "11" in d and n != "Industries not classified"),
                                     key=lambda t: -t[1]))

    # --- history -------------------------------------------------------------------------------------------------
    h = read("bea_va_history")
    keys = [k for k in h[0] if k != "year"]
    R["history"] = dict(years=[int(r["year"]) for r in h], series={k: [r[k] for r in h] for k in keys})
    yrs = sorted(jobs)
    R["mfg_jobs"] = dict(years=yrs, share=[100 * jobs[y]["MANEMP"] / jobs[y]["PAYEMS"] for y in yrs],
                         jobs=[jobs[y]["MANEMP"] / 1e3 for y in yrs], health=[jobs[y]["USEHS"] / 1e3 for y in yrs],
                         output={y: jobs[y]["OUTMS"] for y in yrs if jobs[y]["OUTMS"]})

    # --- prices: services against goods, 2000-2025 (BLS via FRED) ---------------------------------------------------
    from explainer.industry.data.fetch import FRED_PRICES
    pr = {int(r["year"]): r for r in read("fred_prices")}
    y0, y1 = 2000, max(pr)
    R["prices"] = dict(y0=y0, y1=y1, change={FRED_PRICES[k]: pr[y1][k] / pr[y0][k] - 1 for k in FRED_PRICES})

    # --- who is growing: real value added by industry, 2015-2025 (BEA) ---------------------------------------------
    q = {r["industry"]: r for r in read("bea_real") if r["measure"] == "quantity"}
    R["growth"] = dict(y0=2015, y1=2025, change={k: q[k]["2025"] / q[k]["2015"] - 1 for k in q
                                                   if q[k]["2015"] and q[k]["2025"]})

    # --- the world --------------------------------------------------------------------------------------------
    latest = {}
    for r in read("wb_shares"):
        if r["manufacturing"] is not None and (r["country"] not in latest or r["year"] > latest[r["country"]]["year"]):
            latest[r["country"]] = r
    latest["United States"] = dict(country="United States", year=2025, manufacturing=sectors["Manufacturing"]["pct"],
                                   agriculture=sectors["Farms, forestry, fishing"]["pct"], services=None)
    R["world"] = sorted(([c, int(r["year"]), r["manufacturing"], r["agriculture"]] for c, r in latest.items()),
                        key=lambda t: -t[2])
    R["world_services"] = sorted(([c, int(r["year"]), r["services"]] for c, r in latest.items()
                                  if r.get("services") is not None), key=lambda t: -t[2])

    usd = read("wb_mfg_usd")
    world = {r["year"]: r["mfg_usd"] for r in usd if r["country"] == "World"}
    share = {}
    for c in ("China", "Japan", "Germany", "Korea, Rep.", "India", "Mexico", "Italy"):
        r = max((x for x in usd if x["country"] == c), key=lambda x: x["year"])
        share[c] = 100 * r["mfg_usd"] / world[r["year"]]
    share["United States"] = 100 * sectors["Manufacturing"]["va"] * 1e9 / world[2025]  # BEA 2025 / World Bank 2025
    R["world_mfg"] = dict(share=share, world=world[2025] / 1e12)

    # --- Leontief, 1983 ----------------------------------------------------------------------------------------
    R["leontief"] = dict(j1983=jobs[1983]["PAYEMS"] / 1e3, j2025=j25["PAYEMS"] / 1e3)
    return R


def main():
    R = results()
    print(f"GDP 2025 ${R['gdp']:.2f}tn; jobs {R['jobs_total']:.1f}m")
    for d in sorted(R["jobs"], key=lambda d: -d["per_job"]):
        print(f"   {d['sector']:<38} {d['jobs']:5.1f}m jobs  ${d['va']:6.0f}bn  ${d['per_job'] / 1e3:5.0f}k per job")
    io = R["io"]
    for n, t, u in sorted(zip(io["names"], io["total"], io["upstream"]), key=lambda x: -x[2]):
        print(f"   {n:<24} total requirements {t:.2f}  upstreamness {u:.2f}")
    print("world:", [(c, y, round(m, 1)) for c, y, m, a in R["world"]])
    print("per worker:", {k: round(v) for k, v in R["companies"]["per_worker"].items()})


if __name__ == "__main__":
    main()
