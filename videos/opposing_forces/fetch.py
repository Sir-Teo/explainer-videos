"""Download and process the real data behind "Opposing Forces".

    python -m videos.opposing_forces.fetch              # download every source, rebuild data.json
    python -m videos.opposing_forces.fetch --offline    # rebuild data.json from the cached raw files

Every chart in the video is drawn from public data, frozen as of ``AS_OF`` so a
re-render months later shows exactly what the note's readers saw:

* FRED (St. Louis Fed): Treasury yields, TIPS real yields, breakevens, the Fed's
  target range, mortgage rates, federal debt, interest outlays, GDP, CBO
  potential GDP, who holds Treasuries, French and German yields.
* NY Fed: the Adrian-Crump-Moench (ACM) 10-year term premium.
* Robert Shiller's monthly S&P 500 data: price, trailing earnings, dividends, CAPE.
* U.S. Treasury "Debt to the Penny".
* Nasdaq's public quote API: daily closes of SPY (cap-weighted S&P 500 ETF), RSP
  (equal-weighted S&P 500 ETF) and every current S&P 500 member, for breadth.

Raw downloads are cached in ``.cache/opposing_forces/raw``; the processed,
compact ``data.json`` next to this file is committed, so the video renders
offline.  Scenes never download anything.
"""

from __future__ import annotations

import argparse
import csv
import datetime as dt
import json
import os
import re
import sys
import time
import urllib.parse
import urllib.request
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parents[2]
RAW = Path(os.environ.get("EXPLAINER_CACHE", ROOT / ".cache")) / "opposing_forces" / "raw"
OUT = Path(__file__).with_name("data.json")

AS_OF = dt.date(2026, 10, 6)  # last trading day before the note's week was over; nothing later is used
UA = "explainer-videos/0.1 (+https://github.com/sir-teo/explainer-videos)"
BROWSER_UA = "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0 Safari/537.36"  # Nasdaq only

FRED = {
    "SP500": "S&P 500 index, daily close",
    "DGS10": "10-year Treasury yield, %",
    "DFII10": "10-year TIPS (real) yield, %",
    "T10YIE": "10-year breakeven inflation, %",
    "DGS2": "2-year Treasury yield, %",
    "DFEDTARU": "Fed funds target range, upper bound, %",
    "DFEDTARL": "Fed funds target range, lower bound, %",
    "MORTGAGE30US": "30-year fixed mortgage rate (Freddie Mac), %",
    "GFDEBTN": "Federal debt, total public debt, $ millions",
    "FYGFDPUN": "Federal debt held by the public, $ millions",
    "FDHBFRBN": "Federal debt held by Federal Reserve banks, $ billions",
    "FDHBFIN": "Federal debt held by foreign and international investors, $ billions",
    "A091RC1Q027SBEA": "Federal government interest payments, $ billions SAAR",
    "GDP": "Nominal GDP, $ billions SAAR",
    "GDPC1": "Real GDP, chained 2017 $ billions SAAR",
    "GDPPOT": "Real potential GDP (CBO), chained 2017 $ billions",
    "A679RC1Q027SBEA": "Private fixed investment in information processing equipment and software, $ billions SAAR",
    "FYFSGDA188S": "Federal surplus or deficit, % of GDP (fiscal years)",
    "IRLTLT01FRM156N": "France 10-year government bond yield (OECD), %",
    "IRLTLT01DEM156N": "Germany 10-year government bond yield (OECD), %",
}
SHILLER_HOME = "https://shillerdata.com/"
ACM_CSV = "https://www.newyorkfed.org/medialibrary/media/research/data_indicators/acmPlot_data.csv"
PENNY = ("https://api.fiscaldata.treasury.gov/services/api/fiscal_service/v2/accounting/od/debt_to_penny"
         "?fields=record_date,tot_pub_debt_out_amt&filter=record_date:gte:2019-12-01&sort=record_date&page%5Bsize%5D=2000")
SP500_LIST = "https://en.wikipedia.org/wiki/List_of_S%26P_500_companies"
NASDAQ = "https://api.nasdaq.com/api/quote/{sym}/historical?assetclass={cls}&fromdate={start}&todate={end}&limit=9999"


# ---------------------------------------------------------------------------
# Downloading
# ---------------------------------------------------------------------------
def get(url: str, dest: Path, refresh: bool, accept: str = "*/*", tries: int = 4, ua: str = UA) -> Path:
    if dest.exists() and dest.stat().st_size > 0 and not refresh:
        return dest
    dest.parent.mkdir(parents=True, exist_ok=True)
    req = urllib.request.Request(url, headers={"User-Agent": ua, "Accept": accept})
    for k in range(tries):
        try:
            with urllib.request.urlopen(req, timeout=60) as r:
                body = r.read()
            tmp = dest.with_suffix(dest.suffix + ".tmp")
            tmp.write_bytes(body)
            tmp.replace(dest)
            return dest
        except Exception as e:  # network hiccups: back off and retry
            if k == tries - 1:
                raise RuntimeError(f"download failed: {url}: {e}") from e
            time.sleep(2 ** (k + 1))
    return dest


def sp500_members(refresh: bool) -> list[str]:
    html = get(SP500_LIST, RAW / "sp500_list.html", refresh).read_text()
    i = html.index('id="constituents"')
    table = html[i:html.index("</table>", i)]
    syms = []
    for row in re.findall(r"<tr[^>]*>(.*?)</tr>", table, re.S):
        cells = re.findall(r"<td[^>]*>(.*?)</td>", row, re.S)
        if cells:
            syms.append(re.sub(r"<[^>]+>", "", cells[0]).strip())
    return syms


def nasdaq(sym: str, cls: str, start: str, refresh: bool) -> Path | None:
    dest = RAW / "nasdaq" / f"{sym}.json"
    for s in (sym, sym.replace(".", "/"), sym.replace(".", "-")):
        url = NASDAQ.format(sym=urllib.parse.quote(s, safe=""), cls=cls, start=start, end=AS_OF.isoformat())
        try:
            get(url, dest, refresh, accept="application/json", ua=BROWSER_UA)
            rows = ((json.loads(dest.read_text()).get("data") or {}).get("tradesTable") or {}).get("rows")
            if rows:
                return dest
        except RuntimeError:
            pass
        dest.unlink(missing_ok=True)
    return None


def download(refresh: bool) -> None:
    for sid in FRED:
        get(f"https://fred.stlouisfed.org/graph/fredgraph.csv?id={sid}", RAW / "fred" / f"{sid}.csv", refresh)
    home = get(SHILLER_HOME, RAW / "shillerdata.html", refresh).read_text()
    link = next(h for h in re.findall(r'href="([^"]+)"', home) if h.split("?")[0].endswith("/ie_data.xls"))
    get(("https:" + link) if link.startswith("//") else link, RAW / "ie_data.xls", refresh)
    get(ACM_CSV, RAW / "acm.csv", refresh)
    get(PENNY, RAW / "debt_to_penny.json", refresh, accept="application/json")
    for etf in ("SPY", "RSP"):
        if not nasdaq(etf, "etf", "2015-01-01", refresh):
            sys.exit(f"no data for {etf}")
    members = sp500_members(refresh)
    with ThreadPoolExecutor(4) as pool:
        got = list(pool.map(lambda s: nasdaq(s, "stocks", "2024-03-01", refresh), members))
    missing = [s for s, p in zip(members, got) if p is None]
    print(f"S&P 500 members: {len(members)}, downloaded {len(members) - len(missing)}, missing {missing}")


# ---------------------------------------------------------------------------
# Parsing helpers.  Times are stored as decimal years (2026.76 ~ Oct 5, 2026).
# ---------------------------------------------------------------------------
def year_frac(d: dt.date) -> float:
    start = dt.date(d.year, 1, 1)
    n = (dt.date(d.year + 1, 1, 1) - start).days
    return d.year + (d - start).days / n


def fred(sid: str) -> list[tuple[dt.date, float]]:
    out = []
    with open(RAW / "fred" / f"{sid}.csv") as f:
        r = csv.reader(f)
        next(r)
        for d, v in r:
            if v not in ("", "."):
                day = dt.date.fromisoformat(d)
                if day <= AS_OF:
                    out.append((day, float(v)))
    return out


def resample(rows, key, how="last"):
    """Group (date, value) rows by key(date); keep the last value or the mean."""
    groups: dict = {}
    for d, v in rows:
        groups.setdefault(key(d), []).append((d, v))
    out = []
    for k in sorted(groups):
        g = groups[k]
        out.append((g[-1][0], g[-1][1] if how == "last" else float(np.mean([v for _, v in g]))))
    return out


def monthly(rows, how="last"):
    return resample(rows, lambda d: (d.year, d.month), how)


def weekly(rows):
    return resample(rows, lambda d: d.isocalendar()[:2])


def series(rows, digits=4) -> dict:
    return {"t": [round(year_frac(d), 4) for d, _ in rows], "v": [round(v, digits) for _, v in rows],
            "last_date": rows[-1][0].isoformat(), "last": rows[-1][1]}


def shiller() -> list[dict]:
    import xlrd

    sh = xlrd.open_workbook(RAW / "ie_data.xls").sheet_by_name("Data")
    rows = []
    for i in range(8, sh.nrows):
        r = sh.row_values(i)
        if not isinstance(r[0], float):
            continue
        year = int(r[0] + 1e-9)
        month = int(round((r[0] - year) * 100))
        num = lambda v: float(v) if isinstance(v, float) and v == v else None  # noqa: E731
        rows.append({"date": dt.date(year, month, 1), "P": num(r[1]), "D": num(r[2]), "E": num(r[3]),
                     "CPI": num(r[4]), "GS10": num(r[6]), "CAPE": num(r[12]), "ECY": num(r[16])})
    return rows


def closes(path: Path) -> list[tuple[dt.date, float]]:
    rows = json.loads(path.read_text())["data"]["tradesTable"]["rows"]
    out = []
    for r in rows:
        m, d, y = (int(x) for x in r["date"].split("/"))
        out.append((dt.date(y, m, d), float(r["close"].replace("$", "").replace(",", ""))))
    return sorted(o for o in out if o[0] <= AS_OF)


# ---------------------------------------------------------------------------
# Processing
# ---------------------------------------------------------------------------
def breadth() -> dict:
    """Share of current S&P 500 members trading above their 50- and 200-day averages."""
    files = sorted((RAW / "nasdaq").glob("*.json"))
    members = set(sp500_members(False))
    px: dict[str, dict] = {}
    for f in files:
        if f.stem in members:
            px[f.stem] = dict(closes(f))
    days = sorted({d for p in px.values() for d in p})
    start = dt.date(2025, 1, 2)
    snap_day = dt.date(2026, 10, 2)  # the Friday before the note (week of 10/5/26)
    snapshot = {}
    out50, out200, t = [], [], []
    hist = {s: sorted(p.items()) for s, p in px.items()}
    idx = {s: {d: i for i, (d, _) in enumerate(h)} for s, h in hist.items()}
    vals = {s: np.array([v for _, v in h]) for s, h in hist.items()}
    for day in days:
        if day < start:
            continue
        a50 = a200 = n50 = n200 = 0
        for s in hist:
            i = idx[s].get(day)
            if i is None:
                continue
            v = vals[s]
            if i >= 49:
                n50 += 1
                a50 += v[i] > v[i - 49:i + 1].mean()
                if day == snap_day:
                    snapshot[s] = bool(v[i] > v[i - 49:i + 1].mean())
            if i >= 199:
                n200 += 1
                a200 += v[i] > v[i - 199:i + 1].mean()
        if n50 > 400 and n200 > 400:
            t.append(day)
            out50.append(100 * a50 / n50)
            out200.append(100 * a200 / n200)
    return {"above50": series(list(zip(t, out50)), 1), "above200": series(list(zip(t, out200)), 1),
            "n_members": len(px), "n_listed": len(members), "snapshot_date": snap_day.isoformat(),
            "snapshot_above50": [snapshot[k] for k in sorted(snapshot)]}


def build() -> dict:
    d: dict = {"as_of": AS_OF.isoformat(), "sources": {k: v for k, v in FRED.items()}}

    # --- rates ------------------------------------------------------------
    d["dgs10_monthly"] = series(monthly(fred("DGS10"), "mean"), 3)
    for sid, key in [("DGS10", "dgs10"), ("DFII10", "real10"), ("T10YIE", "breakeven10"), ("DGS2", "dgs2")]:
        rows = [r for r in fred(sid) if r[0] >= dt.date(2019, 1, 1)]
        d[key + "_weekly"] = series(weekly(rows), 3)
        d[key + "_daily"] = series([r for r in rows if r[0] >= dt.date(2025, 1, 1)], 3)
        d[key + "_last"] = {"date": rows[-1][0].isoformat(), "value": rows[-1][1]}
    d["real10_monthly"] = series(monthly(fred("DFII10"), "mean"), 3)
    fed_u = [r for r in fred("DFEDTARU") if r[0] >= dt.date(2015, 1, 1)]
    fed_l = dict(fred("DFEDTARL"))
    d["fed_upper_daily_changes"] = [(r[0].isoformat(), r[1], fed_l.get(r[0])) for i, r in enumerate(fed_u)
                                    if i == 0 or r[1] != fed_u[i - 1][1]]
    d["fed_upper_weekly"] = series(weekly(fed_u), 3)
    d["mortgage_weekly"] = series([r for r in fred("MORTGAGE30US") if r[0] >= dt.date(2019, 1, 1)], 3)

    acm = []
    with open(RAW / "acm.csv") as f:
        r = csv.DictReader(f)
        for row in r:
            day = dt.datetime.strptime(row["RunDates"], "%d-%b-%Y").date()
            if day <= AS_OF:
                acm.append((day, float(row["TERMYld"])))
    d["term_premium_monthly"] = series(acm, 3)

    # --- government debt -------------------------------------------------------
    gdp = dict(fred("GDP"))
    debt = fred("GFDEBTN")
    d["debt_quarterly"] = series([(q, v / 1e6) for q, v in debt if q >= dt.date(2000, 1, 1)], 3)  # $ trillions
    interest = fred("A091RC1Q027SBEA")
    d["interest_pct_gdp"] = series([(q, 100 * v / gdp[q]) for q, v in interest if q in gdp and q >= dt.date(1960, 1, 1)], 3)
    debt_q = dict(debt)
    d["avg_rate_on_debt"] = series([(q, 100 * v / (debt_q[q] / 1e3)) for q, v in interest
                                    if q in debt_q and q >= dt.date(2000, 1, 1)], 3)
    d["deficit_pct_gdp"] = series([r for r in fred("FYFSGDA188S") if r[0].year >= 1960], 2)  # fiscal years
    capex = fred("A679RC1Q027SBEA")
    d["ai_capex"] = series([(q, v / 1e3) for q, v in capex if q.year >= 2010], 3)  # $ trillions SAAR
    d["ai_capex_pct_gdp"] = series([(q, 100 * v / gdp[q]) for q, v in capex if q in gdp and q.year >= 1990], 3)
    pub = dict(fred("FYGFDPUN"))
    d["debt_public_pct_gdp"] = series([(q, 100 * (pub[q] / 1e3) / gdp[q]) for q in sorted(pub) if q in gdp and q.year >= 1960], 2)
    fed_h, for_h = dict(fred("FDHBFRBN")), dict(fred("FDHBFIN"))
    d["holders_share"] = {
        "fed": series([(q, 100 * fed_h[q] / (pub[q] / 1e3)) for q in sorted(pub) if q in fed_h and q.year >= 2000], 2),
        "foreign": series([(q, 100 * for_h[q] / (pub[q] / 1e3)) for q in sorted(pub) if q in for_h and q.year >= 2000], 2),
    }
    penny = json.loads((RAW / "debt_to_penny.json").read_text())["data"]
    penny = [(dt.date.fromisoformat(p["record_date"]), float(p["tot_pub_debt_out_amt"]) / 1e12) for p in penny]
    penny = [p for p in penny if p[0] <= AS_OF]
    pre = [p for p in penny if p[0] <= dt.date(2019, 12, 31)][-1]
    d["debt_penny"] = {"pre_covid_date": pre[0].isoformat(), "pre_covid": pre[1],
                       "last_date": penny[-1][0].isoformat(), "last": penny[-1][1]}

    # --- growth -------------------------------------------------------------------
    real = fred("GDPC1")
    d["real_gdp_growth"] = series([(q, 100 * (v / real[i - 4][1] - 1)) for i, (q, v) in enumerate(real)
                                   if i >= 4 and q.year >= 2000], 3)
    pot = _all_rows("GDPPOT")  # CBO's projection runs past AS_OF by design: it is a forecast
    d["potential_growth"] = series([(q, 100 * (v / pot[i - 4][1] - 1)) for i, (q, v) in enumerate(pot)
                                    if i >= 4 and 2000 <= q.year <= 2030], 3)

    fr, de = dict(fred("IRLTLT01FRM156N")), dict(fred("IRLTLT01DEM156N"))
    d["france10"] = series([(m, v) for m, v in sorted(fr.items()) if m.year >= 2000], 3)
    d["germany10"] = series([(m, v) for m, v in sorted(de.items()) if m.year >= 2000], 3)

    # --- stocks -------------------------------------------------------------------
    sh = shiller()
    d["shiller"] = {
        "t": [round(year_frac(r["date"]), 4) for r in sh],
        **{k: [None if r[k] is None else round(r[k], 4) for r in sh] for k in ("P", "D", "E", "CPI", "GS10", "CAPE", "ECY")},
        "dates": [r["date"].isoformat() for r in sh],
    }
    spy, rsp = closes(RAW / "nasdaq" / "SPY.json"), closes(RAW / "nasdaq" / "RSP.json")
    rsp_d = dict(rsp)
    both = [(day, v, rsp_d[day]) for day, v in spy if day in rsp_d]
    d["sp500_daily"] = series([r for r in fred("SP500") if r[0] >= dt.date(2025, 1, 1)], 2)
    d["spy_weekly"] = series(weekly([(day, a) for day, a, _ in both]), 3)
    d["rsp_weekly"] = series(weekly([(day, b) for day, _, b in both]), 3)
    d["spy_daily_2026"] = series([(day, a) for day, a, _ in both if day >= dt.date(2025, 6, 1)], 3)
    d["rsp_daily_2026"] = series([(day, b) for day, _, b in both if day >= dt.date(2025, 6, 1)], 3)
    d["breadth"] = breadth()
    return d


def _all_rows(sid: str) -> list[tuple[dt.date, float]]:
    """Like ``fred`` but keeps rows after AS_OF (for projections such as CBO's potential GDP)."""
    out = []
    with open(RAW / "fred" / f"{sid}.csv") as f:
        r = csv.reader(f)
        next(r)
        for day, v in r:
            if v not in ("", "."):
                out.append((dt.date.fromisoformat(day), float(v)))
    return out


def load() -> dict:
    return json.loads(OUT.read_text())


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--offline", action="store_true", help="only rebuild data.json from cached raw files")
    ap.add_argument("--refresh", action="store_true", help="re-download files that are already cached")
    args = ap.parse_args()
    if not args.offline:
        download(args.refresh)
    d = build()
    OUT.write_text(json.dumps(d, separators=(",", ":")))
    print(f"Wrote {OUT.relative_to(ROOT)} ({OUT.stat().st_size / 1e3:.0f} kB), data as of {d['as_of']}")


if __name__ == "__main__":
    main()
