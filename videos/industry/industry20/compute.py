"""Every number in Part 20 of *Industry, Built* ("Pharmaceuticals"), from the Register, the Filing Room and the Works.

    python -m videos.industry.industry20.compute        # prints the film's numbers; writes .cache/industry20/computed.json

Items:
    hook        Lipitor's cliff; Lilly's tirzepatide; Keytruda's share of Merck
    run         the Run it decision: pay for Phase III once the market's size is known (the Works)
    odds        BIO's phase success rates, durations and likelihood of approval by disease area
    cost        the cost of one approved drug, the failures and the years counted (the Works)
    drug        a drug's sales from launch to the cliff, and its value (the Works)
    cliff       generic prices against the number of makers (FDA); Lipitor
    rnd         research and development against revenue, by company (SEC)
    approvals   the FDA's novel drug approvals, 2021-2025
    prices      drug makers' producer prices against all consumer prices (FRED)
    medicare    the first negotiated Medicare prices (CMS)
    landscape   the companies by revenue and margin
    called      Lilly's own revenue guidance against outcomes; this series' call
"""

from __future__ import annotations

import collections
import functools
import json
from pathlib import Path

import numpy as np

from explainer.industry.data.fetch import read
from explainer.industry.register import get
from explainer.industry.works import pharma

OUT = Path(__file__).resolve().parents[3] / ".cache" / "industry20"


def _annual(monthly: dict, need: int = 12) -> dict:
    by: dict = collections.defaultdict(list)
    for m, v in monthly.items():
        by[int(str(m)[:4])].append(v)
    return {y: float(np.mean(v)) for y, v in by.items() if len(v) >= need}


@functools.lru_cache(maxsize=None)
def results() -> dict:
    R: dict = {}
    sec: dict = collections.defaultdict(dict)
    for r in read("sec_pharma"):
        if r.get("revenue") and r["revenue"] > 0:
            sec[r["ticker"]][int(str(r["year_end"])[:4])] = r
    fred: dict = collections.defaultdict(dict)
    for r in read("fred_pharma"):
        fred[r["series"]][str(r["month"])] = r["value"]

    def margins(tk, start=2021, end=2025):
        return {y: r["profit"] / r["revenue"] for y, r in sec[tk].items() if r.get("profit") is not None and start <= y <= end}

    lip = {2010: get("pfe.lipitor.2010"), 2011: get("pfe.lipitor.2011"), 2012: get("pfe.lipitor.2012")}
    R["hook"] = dict(lipitor=lip, lip_fall=lip[2012] / lip[2011] - 1,
                     tirz={2024: get("lly20.mounjaro.2024") + get("lly20.zepbound.2024"),
                           2025: get("lly.mounjaro") + get("lly.zepbound")},
                     lly_share=get("lly20.share"), keytruda=get("mrk.keytruda"), key_share=get("mrk.keytruda.share"),
                     key_us=get("mrk.keytruda.us"), cidara=get("mrk.cidara"))

    o = pharma.Option()
    R["run"] = dict(o.summary(), p_big=o.p_big, peak_big=o.big.peak, peak_small=o.small.peak,
                    p3=pharma.PHASES[2][2], q3=pharma.PHASES[2][3], q4=pharma.PHASES[3][3])

    R["odds"] = dict(phases=[(n, y, q) for n, y, _, q in pharma.PHASES], loa=get("bio.loa"), years=get("bio.years"),
                     reach=pharma.reach(), onc_n=get("bio.onc.n"),
                     p2={nm: get(f"bio.p2.{k}") for k, nm in (("hem", "hematology"), ("met", "metabolic"),
                                                              ("inf", "infectious disease"), ("neu", "neurology"),
                                                              ("onc", "oncology"), ("cv", "cardiovascular"), ("uro", "urology"))},
                     areas={"hematology": get("bio.loa.hem"), "rare diseases": get("bio.loa.rare"),
                            "all candidates": get("bio.loa"), "chronic, common diseases": get("bio.loa.chronic"),
                            "oncology": get("bio.loa.onc")})

    c = pharma.cost_per_approval()
    R["cost"] = dict(c, costs=[(n, cst) for n, _, cst, _ in pharma.PHASES])

    d = pharma.Drug()
    R["drug"] = dict(sales=d.sales(), npv=d.npv(), peak=d.peak, ramp=d.ramp, excl=d.exclusivity, margin=d.margin,
                     cliff=list(d.cliff))

    R["cliff"] = dict(median=get("fda.median"), fda={1: get("fda.gen1"), 2: get("fda.gen2"), 4: get("fda.gen4"), 6: get("fda.gen6")},
                      lipitor=lip, loe=get("pfe.lipitor.loe"))

    names = {"REGN": "Regeneron", "VRTX": "Vertex", "MRK": "Merck", "AZN": "AstraZeneca", "BMY": "Bristol Myers Squibb",
             "LLY": "Eli Lilly", "AMGN": "Amgen", "GILD": "Gilead", "BIIB": "Biogen", "PFE": "Pfizer", "ABBV": "AbbVie",
             "VTRS": "Viatris", "TEVA": "Teva"}
    rnd = {}
    for tk, nm in names.items():
        r = sec[tk][max(sec[tk])]
        if r.get("rnd"):
            rnd[nm] = r["rnd"] / r["revenue"]
    R["rnd"] = dict(share=rnd, lly_rd=get("lly.rd"), lly_rev=get("lly.rev"))

    R["approvals"] = {y: get(f"fda.novel.{y}") for y in range(2021, 2026)}
    R["generics"] = {y: get(f"fda.generic.{y}") for y in range(2021, 2025)}
    ip = _annual(fred["IPG3254S"])
    R["output"] = dict(ip={y: ip[y] / ip[1972] for y in ip if y <= 2025}, x=ip[2025] / ip[1972])
    R["pfizer"] = {y: sec["PFE"][y]["revenue"] for y in sec["PFE"] if 2009 <= y <= 2025}
    R["build"] = dict(capex={y: get(f"lly20.capex.{y}") for y in (2023, 2024, 2025)}, sites=get("lly20.sites"),
                      commit=get("lly20.commit"),
                      inventory={y: sec["LLY"][y]["inventory"] for y in (2021, 2023, 2025)})
    R["mounjaro"] = dict(zep_us=get("lly20.zepbound.us"), zep=get("lly.zepbound"), us=get("lly20.mounjaro.us"), ex=get("lly20.mounjaro.ex"), ex24=get("lly20.mounjaro.ex2024"))
    d = pharma.Drug()
    disc = [s * d.margin / (1 + d.rate) ** (t + 1) for t, s in enumerate(d.sales())]
    reach = pharma.reach()
    # how many candidates must enter each stage, on average, for one approval
    R["pipeline"] = {n: reach[i] / reach[-1] for i, n in enumerate(["Phase I", "Phase II", "Phase III", "FDA review", "approved"])}
    rd = {}
    for tk in ("PFE", "MRK", "LLY", "ABBV", "BMY", "AMGN", "GILD", "VRTX", "REGN", "BIIB", "MRNA", "TEVA", "VTRS", "AZN"):
        r = sec[tk].get(2025)
        if r and r.get("rnd"):
            rd[tk] = r["rnd"]
    R["rd_total"] = dict(total=sum(rd.values()), n=len(rd), rev=sum(sec[tk][2025]["revenue"] for tk in rd))
    R["biotech"] = dict(mrna={y: sec["MRNA"][y]["revenue"] for y in sec["MRNA"] if y >= 2019},
                        margins={nm: float(np.median(list(margins(tk).values()))) for tk, nm in
                                 (("VRTX", "Vertex"), ("REGN", "Regeneron"), ("GILD", "Gilead"), ("AMGN", "Amgen"))},
                        rnd={nm: sec[tk][2025]["rnd"] / sec[tk][2025]["revenue"] for tk, nm in
                             (("VRTX", "Vertex"), ("REGN", "Regeneron"), ("GILD", "Gilead"), ("AMGN", "Amgen"))},
                        cidara=get("mrk.cidara"))
    R["drug_split"] = dict(before=sum(disc[:d.exclusivity]) / sum(disc), cap_factor=(1 + 0.105) ** pharma.cost_per_approval()["years"])

    ppi = _annual(fred["PCU325412325412"])
    cpi = _annual(fred["CPIAUCNS"], need=11)  # the BLS published no October 2025 CPI
    base = 1982
    R["prices"] = dict(rel={y: (ppi[y] / ppi[base]) / (cpi[y] / cpi[base]) for y in ppi if y in cpi and y >= base},
                       ppi_x=ppi[2025] / ppi[base], cpi_x=cpi[2025] / cpi[base])

    R["medicare"] = dict(saving=get("cms.saving"), pct=get("cms.pct"), users=get("cms.users"))

    groups = {"PFE": ("Pfizer", "large"), "MRK": ("Merck", "large"), "JNJ": ("Johnson & Johnson", "large"),
              "LLY": ("Eli Lilly", "large"), "ABBV": ("AbbVie", "large"), "BMY": ("Bristol Myers Squibb", "large"),
              "AZN": ("AstraZeneca", "large"), "AMGN": ("Amgen", "biotech"), "GILD": ("Gilead", "biotech"),
              "VRTX": ("Vertex", "biotech"), "REGN": ("Regeneron", "biotech"), "BIIB": ("Biogen", "biotech"),
              "MRNA": ("Moderna", "biotech"), "TEVA": ("Teva", "generics"), "VTRS": ("Viatris", "generics")}
    comp = []
    for tk, (nm, grp) in groups.items():
        r = sec[tk][max(sec[tk])]
        m = list(margins(tk).values())
        comp.append(dict(name=nm, group=grp, rev=r["revenue"], margin=float(np.median(m)) if m else r["profit"] / r["revenue"]))
    full = [tk for tk in sec if tk != "JNJ" and 2025 in sec[tk]
            and all(sec[tk][2025].get(k) is not None for k in ("revenue", "cost", "rnd", "profit"))]
    tot = {k: sum(sec[tk][2025][k] for tk in full) for k in ("revenue", "cost", "rnd", "profit")}
    R["dollar"] = dict(n=len(full), revenue=tot["revenue"], make=tot["cost"] / tot["revenue"], research=tot["rnd"] / tot["revenue"],
                       profit=tot["profit"] / tot["revenue"],
                       rest=1 - (tot["cost"] + tot["rnd"] + tot["profit"]) / tot["revenue"])
    R["landscape"] = dict(companies=comp, mrna={y: sec["MRNA"][y]["revenue"] for y in (2022, 2025)})

    R["called"] = dict(g2025=(58.0, get("lly.guide2025")), a2025=get("lly.rev"), g2026=(80.0, get("lly.guide2026")),
                       g2026_oct=(91.0, get("lly.guide2026.oct")), q3=get("lly.q3.2026"), prob=0.55)
    return R


def main():
    R = results()
    OUT.mkdir(parents=True, exist_ok=True)
    (OUT / "computed.json").write_text(json.dumps(R, default=str, indent=1))
    print("hook", R["hook"])
    print("run", {k: round(v, 1) for k, v in R["run"].items()})
    c = R["cost"]
    print("cost", round(c["p_approval"], 4), round(c["spend"]), round(c["per_approval"]), round(c["capitalized"]))
    print("drug", round(R["drug"]["npv"]))
    print("rnd", {k: round(100 * v, 1) for k, v in R["rnd"]["share"].items()})
    p = R["prices"]
    print("prices", round(p["rel"][2025], 2), round(p["ppi_x"], 2), round(p["cpi_x"], 2))
    print("landscape", [(x["name"], round(x["rev"], 1), round(100 * x["margin"], 1)) for x in R["landscape"]["companies"]])
    print("called", R["called"])


if __name__ == "__main__":
    main()
