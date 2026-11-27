"""Every number in Part 21 of *Industry, Built* ("Medical Technology"), from the Register, the Filing Room and the Works.

    python -m videos.industry.industry21.compute        # prints the film's numbers; writes .cache/industry21/computed.json

Items:
    hook        Intuitive's robots, operations and instruments
    run         the Run it decision: sell the robot, or place it for a fee an operation (the Works); Intuitive's leases
    kinds       four businesses: implants and therapies (Medtronic), equipment and service (GE HealthCare), consumables
                (Dexcom, Intuitive's instruments), diagnostics (Quest, Abbott)
    fda         510(k) clearances, original premarket approvals, De Novo decisions and Class I recalls (openFDA)
    customers   who pays a laboratory (Quest's payer mix); seasonality and deductibles (Intuitive)
    base        Intuitive's revenue by kind; GE HealthCare's products and services; a hospital's five years with one robot
    diag        Quest's requisitions; Abbott's COVID-19 testing
    history     device producer prices and output (FRED); 510(k)s since 1976
    boom        pulsed field ablation at Boston Scientific and Medtronic; Watchman; Edwards' valves
    tools       the tools and contract research companies; Illumina
    landscape   the companies by revenue and margin; a dollar of the device makers' revenue
    called      Intuitive's procedure guidance against outcomes; this series' call
"""

from __future__ import annotations

import collections
import datetime as dt
import functools
import json
from pathlib import Path

import numpy as np

from explainer.industry.data.fetch import read
from explainer.industry.register import get
from explainer.industry.works import medtech

OUT = Path(__file__).resolve().parents[3] / ".cache" / "industry21"

NAMES = {"MDT": ("Medtronic", "devices"), "ABT": ("Abbott", "devices"), "BSX": ("Boston Scientific", "devices"),
         "SYK": ("Stryker", "devices"), "ISRG": ("Intuitive", "devices"), "EW": ("Edwards", "devices"),
         "BDX": ("BD", "devices"), "ZBH": ("Zimmer Biomet", "devices"), "BAX": ("Baxter", "devices"),
         "DXCM": ("Dexcom", "devices"), "PODD": ("Insulet", "devices"), "RMD": ("ResMed", "devices"),
         "ALGN": ("Align", "devices"), "STE": ("Steris", "devices"), "GEHC": ("GE HealthCare", "imaging"),
         "DHR": ("Danaher", "tools"), "TMO": ("Thermo Fisher", "tools"), "ILMN": ("Illumina", "tools"),
         "A": ("Agilent", "tools"), "LH": ("Labcorp", "labs"), "DGX": ("Quest", "labs"), "IQV": ("IQVIA", "labs")}


def _fy(end: str) -> int:
    """The fiscal year a period ending on ``end`` belongs to (a year ending in the first week of January is the year
    before)."""
    d = dt.date.fromisoformat(str(end)[:10])
    return d.year - 1 if d.month == 1 and d.day <= 7 else d.year


def _annual(monthly: dict, need: int = 12) -> dict:
    by: dict = collections.defaultdict(list)
    for m, v in monthly.items():
        by[int(str(m)[:4])].append(v)
    return {y: float(np.mean(v)) for y, v in by.items() if len(v) >= need}


@functools.lru_cache(maxsize=None)
def results() -> dict:
    R: dict = {}
    sec: dict = collections.defaultdict(dict)
    for r in read("sec_medtech"):
        if r.get("revenue") and r["revenue"] > 0:
            sec[r["ticker"]][_fy(r["year_end"])] = r
    fred: dict = collections.defaultdict(dict)
    for r in read("fred_medtech"):
        fred[r["series"]][str(r["month"])] = r["value"]
    fda = {int(r["year"]): r for r in read("fda_devices")}

    def margins(tk, start=2021, end=2025):
        return {y: r["profit"] / r["revenue"] for y, r in sec[tk].items() if r.get("profit") is not None and start <= y <= end}

    procs, base, base24 = get("isrg.procs.2025"), get("isrg.base.2025"), get("isrg.base.2024")
    per_op = get("isrg.ia.2025") * 1e6 / (procs + get("isrg.ion.procs"))
    R["hook"] = dict(procs=procs, base=base, per_system=procs / ((base + base24) / 2), placed=get("isrg.placed.2025"),
                     price=(get("isrg.price.lo"), get("isrg.price.hi")), ia=(get("isrg.ia.lo"), get("isrg.ia.hi")),
                     svc=(get("isrg.svc.lo"), get("isrg.svc.hi")), per_op=per_op, rev=get("isrg.rev.2025"),
                     recurring=get("isrg.recurring"))

    m = medtech.Market()
    s, p = m.sell(), m.place()
    R["run"] = dict(sell={k: v for k, v in s.items() if k != "per"}, place={k: v for k, v in p.items() if k != "per"},
                    sell_per=s["per"], place_per=p["per"], volumes=list(m.volumes), match=m.fee_to_match(),
                    price=2.0e6, fee=1000.0, value=m.value, instrument=m.instrument,
                    leased=get("isrg.leased"), usage=get("isrg.usage"), usage23=get("isrg.usage.2023"),
                    lease_rev={y: get(f"isrg.lease.{y}") for y in (2023, 2024, 2025)})

    R["kinds"] = dict(mdt={"Cardiovascular": get("mdt.cv"), "Neuroscience": get("mdt.neuro"),
                           "Medical Surgical": get("mdt.medsurg"), "Diabetes": get("mdt.diab")},
                      mdt_rev=get("mdt.rev"), founded=get("mdt.founded"),
                      gehc={"products": get("gehc.products"), "services": get("gehc.services")},
                      dexcom={y: sec["DXCM"][y]["revenue"] for y in sorted(sec["DXCM"]) if y >= 2012},
                      quest=dict(reqs=get("dgx.reqs"), dis=get("dgx.dis")))

    k510 = {y: int(r["k510_se"]) for y, r in fda.items() if y <= 2025}
    R["fda"] = dict(k510=k510, pma={y: int(r["pma_orig"]) for y, r in fda.items() if 2000 <= y <= 2025},
                    denovo={y: int(r["denovo"]) for y, r in fda.items() if 2000 <= y <= 2025},
                    recall_c1={y: int(r["recall_c1"]) for y, r in fda.items() if 2012 <= y <= 2025},
                    panels={r["panel"]: int(r["count"]) for r in read("fda_510k_panels") if r["panel"] != "Unknown"},
                    c1_events=get("fda21.c1.events.2023"), c1_max=get("fda21.c1.max.2023"),
                    k510_5=float(np.mean([k510[y] for y in range(2021, 2026)])),
                    pma_5=float(np.mean([fda[y]["pma_orig"] for y in range(2021, 2026)])),
                    denovo_5=float(np.mean([fda[y]["denovo"] for y in range(2021, 2026)])))

    mix = {k: (get(f"dgx.mix.{k}.vol"), get(f"dgx.mix.{k}.rev")) for k in ("ins", "gov", "client", "pat")}
    R["customers"] = dict(mix=mix, benign=get("isrg.benign"))

    rev_kind = {y: {"instruments": get(f"isrg.ia.{y}"), "systems": get(f"isrg.sys.{y}") - get(f"isrg.lease.{y}"),
                    "leases": get(f"isrg.lease.{y}"), "service": get(f"isrg.svc.{y}")} for y in (2023, 2024, 2025)}
    gp, gs = get("gehc.products"), get("gehc.services")
    R["base"] = dict(isrg=rev_kind, recurring=get("isrg.recurring"), gm=get("isrg.gm"),
                     gehc_share=gs / (gp + gs), gehc_gm_products=1 - get("gehc.cost.products") / gp,
                     gehc_gm_services=1 - get("gehc.cost.services") / gs,
                     spend=medtech.hospital_spend(per_op=round(per_op, -1)), settle=get("isrg.settle"))

    R["pricevol"] = {y: dict(rpr=get(f"dgx.rpr.{y}"), vol=get(f"dgx.vol.{y}"), org=get(f"dgx.org.{y}")) for y in (2023, 2024, 2025)}
    R["pricevol_acq"] = get("dgx.acq")
    R["where"] = {"United States": get("isrg.base.us"), "Europe": get("isrg.base.eu"), "Asia": get("isrg.base.asia"),
                  "elsewhere": get("isrg.base.row")}
    R["diag"] = dict(reqs=get("dgx.reqs"), dis=get("dgx.dis"), per_req=get("dgx.dis") / get("dgx.reqs"),
                     covid={y: get(f"abt.covid.{y}") for y in range(2020, 2026)})

    ppi = _annual(fred["PCU339112339112"])
    cpi = _annual(fred["CPIAUCNS"], need=11)  # the BLS published no October 2025 CPI
    ip = _annual(fred["IPN3391S"])
    R["history"] = dict(ppi_x=ppi[2025] / ppi[1986], cpi_x=cpi[2025] / cpi[1986],
                        rel={y: (ppi[y] / ppi[1986]) / (cpi[y] / cpi[1986]) for y in ppi if y in cpi and y >= 1986},
                        ip={y: v / ip[1972] for y, v in ip.items()}, ip_x=ip[2025] / ip[1972],
                        ip_2009=ip[2009] / ip[2008] - 1, k510=k510)

    R["boom"] = dict(ep={y: get(f"bsx.ep.{y}") for y in (2023, 2024, 2025)},
                     watchman={y: get(f"bsx.watchman.{y}") for y in (2023, 2024, 2025)},
                     impair=get("bsx.impair"), crhf=get("mdt.crhf"),
                     tavr={y: get(f"ew.tavr.{y}") for y in (2023, 2024, 2025)},
                     bsx_rev={y: sec["BSX"][y]["revenue"] for y in (2023, 2024, 2025)}, mako=get("syk.mako"))

    tools = {NAMES[tk][0]: sec[tk][max(sec[tk])]["revenue"] for tk in ("TMO", "DHR", "IQV", "A", "ILMN")}
    R["tools"] = dict(rev=tools, ilmn={y: sec["ILMN"][y]["revenue"] for y in sorted(sec["ILMN"]) if y >= 2012},
                      ilmn_profit={y: sec["ILMN"][y]["profit"] for y in sorted(sec["ILMN"]) if y >= 2019},
                      tmo={y: sec["TMO"][y]["revenue"] for y in sorted(sec["TMO"]) if y >= 2017},
                      iqv={y: sec["IQV"][y]["revenue"] for y in sorted(sec["IQV"]) if y >= 2011})

    R["china"] = dict(quota=get("isrg.quota"))

    comp = []
    for tk, (nm, grp) in NAMES.items():
        r = sec[tk][max(sec[tk])]
        mm = list(margins(tk).values())
        comp.append(dict(name=nm, group=grp, rev=r["revenue"], margin=float(np.median(mm)) if mm else r["profit"] / r["revenue"],
                         fy=max(sec[tk])))
    dev = [tk for tk, (_, g) in NAMES.items() if g == "devices" and tk != "ABT"]
    latest = {tk: sec[tk][max(sec[tk])] for tk in dev}
    full = [tk for tk in dev if all(latest[tk].get(k) is not None for k in ("revenue", "cost", "rnd", "profit"))]
    tot = {k: sum(latest[tk][k] for tk in full) for k in ("revenue", "cost", "rnd", "profit")}
    R["landscape"] = dict(companies=comp)
    R["dollar"] = dict(n=len(full), names=[NAMES[tk][0] for tk in full], revenue=tot["revenue"],
                       make=tot["cost"] / tot["revenue"], research=tot["rnd"] / tot["revenue"],
                       profit=tot["profit"] / tot["revenue"],
                       rest=1 - (tot["cost"] + tot["rnd"] + tot["profit"]) / tot["revenue"])

    R["called"] = dict(g2025=(get("isrg.guide2025.lo"), get("isrg.guide2025.hi")), a2025=get("isrg.growth.2025"),
                       g2026=(get("isrg.guide2026.lo"), get("isrg.guide2026.hi")), g2026_oct=(get("isrg.guide2026.oct"), get("isrg.guide2026.oct.hi")),
                       ia_growth=get("isrg.ia.growth"), q3_ia=get("isrg.q3.ia"), q3_ia_growth=get("isrg.q3.ia.growth"),
                       q3=get("isrg.q3.procs"), q3_growth=get("isrg.q3.growth"), nine=get("isrg.9m.growth"), base_q3=get("isrg.base.q3"),
                       prob=0.45)
    return R


def main():
    R = results()
    OUT.mkdir(parents=True, exist_ok=True)
    (OUT / "computed.json").write_text(json.dumps(R, default=str, indent=1))
    print("hook", {k: v for k, v in R["hook"].items()})
    u = R["run"]
    print("run sell", {k: round(v, 1) for k, v in u["sell"].items()}, "place", {k: round(v, 1) for k, v in u["place"].items()},
          "match", round(u["match"]))
    f = R["fda"]
    print("fda 2021-25 means: 510k", round(f["k510_5"]), "PMA", round(f["pma_5"], 1), "De Novo", round(f["denovo_5"], 1))
    print("base", {k: (round(v, 3) if isinstance(v, float) else v) for k, v in R["base"].items() if k not in ("isrg", "spend")})
    print("spend", R["base"]["spend"])
    print("diag", {k: v for k, v in R["diag"].items()})
    h = R["history"]
    print("history ppi x", round(h["ppi_x"], 2), "cpi x", round(h["cpi_x"], 2), "rel", round(h["rel"][2025], 2), "ip x",
          round(h["ip_x"], 2), "2009", round(h["ip_2009"], 3))
    print("boom", R["boom"])
    print("tools", R["tools"]["rev"])
    print("landscape", [(c["name"], round(c["rev"], 1), round(100 * c["margin"], 1), c["fy"]) for c in R["landscape"]["companies"]])
    d = R["dollar"]
    print("dollar", d["n"], round(d["revenue"], 1), {k: round(100 * d[k]) for k in ("make", "research", "rest", "profit")})
    print("called", R["called"])


if __name__ == "__main__":
    main()
