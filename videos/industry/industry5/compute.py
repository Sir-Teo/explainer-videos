"""Every number in Part 5 of *Industry, Built* ("The Moat"), from the Register and the Filing Room.

    python -m videos.industry.industry5.compute        # prints the film's numbers; writes .cache/industry5/computed.json

Items:
    three       Berkshire's three businesses (2007 letter): See's, FlightSafety, airlines; return on extra capital
    roc         Damodaran's return on capital against the cost of capital by US industry, January 2026
    persist     the same industries' returns, 2015-2019 against 2022-2026: rank correlation, quartiles, survivors
    variance    McGahan and Porter's split of the variance in profitability
    conc        the Census's four-firm concentration ratios for 897 industries, 2022: the spread and the extremes
    match       a few industries matched by hand between the two sources (Damodaran's names, Census codes)
    visa        Visa's operating margin, fiscal 2026
    network     links in a network of n users: n(n-1)/2
    drained     newspapers' advertising and Kodak's sales
"""

from __future__ import annotations

import functools
import json

from pathlib import Path

import numpy as np

from explainer.industry.data.fetch import read
from explainer.industry.register import get

OUT = Path(__file__).resolve().parents[3] / ".cache" / "industry5"
EARLY, LATE = (2015, 2016, 2017, 2018, 2019), (2022, 2023, 2024, 2026)

# Damodaran's industry -> the Census six-digit industry closest to it (by hand; this film's match, shown as such)
MATCH = [("Tobacco", "312230", "Tobacco manufacturing"),
         ("Retail (Building Supply)", "444110", "Home centers"),
         ("Beverage (Soft)", "312111", "Soft drink manufacturing"),
         ("Household Products", "325611", "Soap and other detergent manufacturing"),
         ("Air Transport", "481111", "Scheduled passenger air transportation"),
         ("Restaurant/Dining", "722511", "Full-service restaurants"),
         ("Trucking", "484121", "General freight trucking, long-distance, truckload"),
         ("Auto & Truck", "336110", "Automobile and light duty motor vehicle manufacturing")]


def _rank(v):
    order = np.argsort(v)
    r = np.empty(len(v))
    r[order] = np.arange(len(v))
    return r


def spearman(a, b) -> float:
    return float(np.corrcoef(_rank(np.asarray(a)), _rank(np.asarray(b)))[0, 1])


@functools.lru_cache(maxsize=None)
def results() -> dict:
    R = {}

    # --- Berkshire's three businesses ------------------------------------------------------------------------------
    sees = dict(price=get("sees.price"), cap0=get("sees.capital.1972"), pre0=get("sees.pretax.1972"),
                sales1=get("sees.sales.2007"), pre1=get("sees.pretax.2007"), cap1=get("sees.capital.2007"),
                total=get("sees.total"))
    sees["roc0"] = sees["pre0"] / sees["cap0"]
    sees["roc1"] = sees["pre1"] / sees["cap1"]
    sees["incr"] = (sees["pre1"] - sees["pre0"]) / (sees["cap1"] - sees["cap0"])  # extra profit per extra $ of capital
    fsi = dict(pre0=get("fsi.pretax.1996"), capex=get("fsi.capex"), pre1=get("fsi.pretax.2007"))
    fsi["gain"] = fsi["pre1"] - fsi["pre0"]
    fsi["incr"] = fsi["gain"] / 509.0  # the letter's $509m of incremental investment
    assert get("brk.moat") == 0 and get("brk.airlines") == 0
    R["three"] = dict(sees=sees, fsi=fsi)

    # --- returns on capital by industry -------------------------------------------------------------------------------
    rows = [r for r in read("damodaran_roc") if isinstance(r["roc"], float) and isinstance(r["wacc"], float)]
    by = {}
    for r in rows:
        by.setdefault(r["name"], {})[int(r["year"])] = r
    now = sorted(((n, d[2026]["roc"], d[2026]["wacc"], d[2026]["capital_musd"]) for n, d in by.items() if 2026 in d),
                 key=lambda t: -t[1])
    R["roc"] = dict(industries=[dict(name=n, roc=a, wacc=w, capital=c) for n, a, w, c in now],
                    above=float(np.mean([a > w for _, a, w, _ in now])),
                    median=float(np.median([a for _, a, _, _ in now])),
                    wacc_median=float(np.median([w for _, _, w, _ in now])))

    # --- persistence --------------------------------------------------------------------------------------------------
    pairs = []
    for n, d in by.items():
        if all(y in d for y in EARLY + LATE):
            pairs.append((n, float(np.mean([d[y]["roc"] for y in EARLY])), float(np.mean([d[y]["roc"] for y in LATE]))))
    early = np.array([p[1] for p in pairs])
    late = np.array([p[2] for p in pairs])
    q1, q3 = np.quantile(early, [0.25, 0.75])
    top = [p for p in pairs if p[1] >= q3]
    bottom = [p for p in pairs if p[1] <= q1]
    top_names = {p[0] for p in top}
    still = sum(1 for p in sorted(pairs, key=lambda t: -t[2])[:len(top)] if p[0] in top_names)
    R["persist"] = dict(pairs=pairs, rho=spearman(early, late), n=len(pairs),
                        top_early=float(np.mean([p[1] for p in top])), top_late=float(np.mean([p[2] for p in top])),
                        bottom_early=float(np.mean([p[1] for p in bottom])),
                        bottom_late=float(np.mean([p[2] for p in bottom])), quartile=len(top), still_top=still)

    # --- how much is the industry ---------------------------------------------------------------------------------------
    v = dict(industry=get("mp.industry"), business=get("mp.business"), parent=get("mp.parent"), year=get("mp.year"))
    v["unexplained"] = 1 - sum(v.values())
    R["variance"] = v

    # --- concentration ------------------------------------------------------------------------------------------------
    cc = [r for r in read("census_conc_2022") if isinstance(r["cr4"], float)]
    cr4 = np.array([r["cr4"] for r in cc])
    hist, edges = np.histogram(cr4, bins=np.arange(0, 101, 10))
    srt = sorted(cc, key=lambda r: r["cr4"])
    named = {r["code"]: r for r in cc}
    R["conc"] = dict(n=len(cc), median=float(np.median(cr4)), hist=hist.tolist(), edges=edges.tolist(),
                     above50=float(np.mean(cr4 > 50)), below20=float(np.mean(cr4 < 20)),
                     low=[dict(code=r["code"], name=r["name"], cr4=r["cr4"], firms=r["firms"]) for r in srt[:6]],
                     high=[dict(code=r["code"], name=r["name"], cr4=r["cr4"], firms=r["firms"]) for r in srt[-12:]],
                     nails=named["812113"], homes=named["444110"], wireless=named["517112"], clubs=named["455211"],
                     tobacco=named["312230"])

    # --- the two sources side by side (this film's match) ----------------------------------------------------------------
    R["match"] = [dict(industry=d, code=c, census=lab, cr4=named[c]["cr4"], roc=by[d][2026]["roc"],
                       wacc=by[d][2026]["wacc"]) for d, c, lab in MATCH if c in named and d in by and 2026 in by[d]]
    R["match_rho"] = spearman([m["cr4"] for m in R["match"]], [m["roc"] for m in R["match"]])

    # --- Visa, networks, drained moats ------------------------------------------------------------------------------------
    R["visa"] = dict(rev=get("visa.rev"), oi=get("visa.oi"), margin=get("visa.oi") / get("visa.rev"))
    R["network"] = [(n, n * (n - 1) // 2) for n in (2, 3, 5, 10, 20)]
    R["drained"] = dict(news2005=get("news.ads.2005"), kodak2008=get("kodak.sales.2008"),
                        kodak2017=get("kodak.sales.2017"))
    return R


def main():
    R = results()
    OUT.mkdir(parents=True, exist_ok=True)
    (OUT / "computed.json").write_text(json.dumps(R, indent=1, default=float))
    s, f = R["three"]["sees"], R["three"]["fsi"]
    print(f"See's: {100 * s['roc0']:.0f}% pre-tax on capital in 1972, {100 * s['roc1']:.0f}% in 2007; each extra $ of "
          f"capital earned ${s['incr']:.2f} more a year; FlightSafety ${f['incr']:.2f}")
    r = R["roc"]
    print(f"Damodaran Jan 2026: {len(r['industries'])} industries, median ROC {100 * r['median']:.1f}% vs median cost "
          f"{100 * r['wacc_median']:.1f}%; {100 * r['above']:.0f}% above their cost")
    for d in r["industries"][:5] + r["industries"][-5:]:
        print(f"   {d['name']:<34} {100 * d['roc']:6.1f}%  cost {100 * d['wacc']:.1f}%")
    p = R["persist"]
    print(f"persistence ({p['n']} industries): Spearman {p['rho']:.2f}; top quartile {100 * p['top_early']:.1f}% -> "
          f"{100 * p['top_late']:.1f}%, bottom {100 * p['bottom_early']:.1f}% -> {100 * p['bottom_late']:.1f}%; "
          f"{p['still_top']} of {p['quartile']} still in the top quartile")
    c = R["conc"]
    print(f"Census 2022: {c['n']} industries; median CR4 {c['median']:.1f}%; {100 * c['above50']:.0f}% above 50, "
          f"{100 * c['below20']:.0f}% below 20; hist {c['hist']}")
    for m in R["match"]:
        print(f"   {m['industry']:<26} CR4 {m['cr4']:5.1f}%  ROC {100 * m['roc']:5.1f}%   ({m['census']})")
    print(f"   rank correlation across the matched eight: {R['match_rho']:.2f}")
    print(f"Visa margin {100 * R['visa']['margin']:.0f}%; network links {R['network']}")


if __name__ == "__main__":
    main()
