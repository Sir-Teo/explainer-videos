"""Every number in Part 1 of *Industry, Built* ("Where the Money Goes"), computed from the Register.

    python -m videos.industry.industry1.compute        # prints the film's numbers; writes .cache/industry1/computed.json

Nothing here is fitted or simulated: each figure is a register row, or arithmetic on register rows with the
assumptions named.  Scenes call :func:`results` (cached in memory); ``computed.json`` is a copy for inspection.

Items:
    ipod        the 2007 study's split of a $299 iPod
    dollar17    the Dollar of a 256GB iPhone 17 Pro at $1,099 (2025), central and low/high cases
    dollar18    the same for a 256GB iPhone 18 Pro at $1,199 (2026), with TrendForce's and the WSJ's memory costs
    added       sales against value added along a three-link chain (the phone, its chip, the wafer)
    perphone    revenue and gross profit per phone: Apple, Xiaomi, Transsion (2025)
    memory      what the memory makers kept per Pro phone, 2025 and 2026
    tiers       the 2026 price rise against the memory-cost rise, storage tier by storage tier (Pro Max)
    margins     the margin ladder: what each link keeps of what it is paid (latest filings)
    history     iPhone net sales and units by fiscal year (Apple's 10-Ks)
    market      2025 shipments by brand (IDC)
"""

from __future__ import annotations

import functools
import json
from pathlib import Path

from explainer.industry.register import get, span
from explainer.industry.works import chain

OUT = Path(__file__).resolve().parents[3] / ".cache" / "industry1"


def _dollar(price, bom, memory=None, channel=None, assembly=None, other=None):
    return chain.dollar(
        price, bom, memory=memory,
        indirect_share=get("apple.indirect_share.fy2026"),
        channel_margin=get("assume.channel_margin") if channel is None else channel,
        assembly=get("assume.assembly") if assembly is None else assembly,
        other_cogs=get("assume.other_cogs") if other is None else other,
        opex_ratio=get("apple.opex.fy2025") / get("apple.revenue.fy2025"),
        tax_rate=get("apple.taxrate.fy2025"))


def _slices(d):
    return [dict(key=s.key, label=s.label, amount=round(s.amount, 2), group=s.group, who=s.who) for s in d.slices]


@functools.lru_cache(maxsize=None)
def results() -> dict:
    R = {}
    # --- the iPod, 2005-07 --------------------------------------------------------------------------------------
    R["ipod"] = dict(price=get("ipod.price"), inputs=get("ipod.inputs"), drive=get("ipod.drive"),
                     display=get("ipod.display"), broadcom=get("ipod.broadcom"), assembly=get("ipod.assembly"),
                     kept=get("ipod.assembly_kept"), apple=get("ipod.apple"), retail=get("ipod.retail"),
                     distribution=get("ipod.distribution"))
    R["ipod"]["other_inputs"] = round(R["ipod"]["inputs"] - R["ipod"]["drive"] - R["ipod"]["display"]
                                      - R["ipod"]["broadcom"] - R["ipod"]["assembly"], 2)

    # --- the Dollar of a 256GB iPhone 17 Pro ------------------------------------------------------------------
    p17, bom17 = get("price.17pro.256"), get("bom.17pro")
    d17 = _dollar(p17, bom17)
    lo_b, hi_b = span("bom.17pro")
    lo_c, hi_c = span("assume.channel_margin")
    lo_a, hi_a = span("assume.assembly")
    lo_o, hi_o = span("assume.other_cogs")
    best = _dollar(p17, lo_b, channel=lo_c, assembly=lo_a, other=lo_o)
    worst = _dollar(p17, hi_b, channel=hi_c, assembly=hi_a, other=hi_o)
    R["dollar17"] = dict(price=p17, bom=bom17, slices=_slices(d17), revenue=p17 - d17.get("channel").amount,
                         gross=p17 - d17.get("channel").amount - bom17 - d17.get("assembly").amount
                         - d17.get("other_cogs").amount,
                         profit=d17.get("profit").amount, profit_range=(worst.get("profit").amount,
                                                                         best.get("profit").amount),
                         memory=d17.get("memory").amount)
    R["dollar17"]["gross_margin"] = R["dollar17"]["gross"] / R["dollar17"]["revenue"]

    # --- the same phone a year later: the iPhone 18 Pro --------------------------------------------------------------
    p18 = get("price.18pro.256")
    bom18_tf = bom17 * (1 + get("bom.rise.18pro"))                     # TrendForce: +38%
    mem18_tf = get("bom.memory_share.2026") * bom18_tf                   # TrendForce: 34% of it
    mem17_wsj = get("memory.dram.2025") + get("memory.nand256.2025")
    mem18_wsj = get("memory.dram.2026") + get("memory.nand256.2026")
    bom18_wsj = bom17 - mem17_wsj + mem18_wsj                            # the WSJ's memory, other parts unchanged
    d18 = _dollar(p18, bom18_tf, memory=mem18_tf)
    d18w = _dollar(p18, bom18_wsj, memory=mem18_wsj)
    R["dollar18"] = dict(price=p18, bom=bom18_tf, bom_wsj=bom18_wsj, memory=mem18_tf, memory_wsj=mem18_wsj,
                         memory17_wsj=mem17_wsj, slices=_slices(d18), profit=d18.get("profit").amount,
                         profit_wsj=d18w.get("profit").amount, memory_multiple=mem18_tf / d17.get("memory").amount)
    R["dollar18"]["gross"] = p18 - d18.get("channel").amount - bom18_tf - d18.get("assembly").amount \
        - d18.get("other_cogs").amount
    R["dollar18"]["gross_margin"] = R["dollar18"]["gross"] / (p18 - d18.get("channel").amount)

    # --- sales against value added ------------------------------------------------------------------------------
    chip = [s for s in d17.slices if s.key == "chip"][0].amount
    links = [("Wafer and materials", round(0.12 * chip)), ("TSMC: the chip", round(chip)),
             ("Apple: the phone", round(R["dollar17"]["revenue"])), ("The shop", p17)]
    R["added"] = dict(chain=[dict(firm=f, sales=s, added=a) for f, s, a in chain.value_added(links)],
                      sales_total=sum(s for _, s in links))

    # --- per phone: three brands, 2025 -----------------------------------------------------------------------
    units_fy25 = get("share.apple.units.2025") - get("share.apple.units.q4_2025") + get("share.apple.units.q4_2024")
    a_rev, a_gp = chain.per_unit(get("apple.iphone_sales.fy2025") * 1e3, units_fy25, get("apple.gm_products.fy2025"))
    fx = get("fx.cny.2025")
    x_rev, x_gp = chain.per_unit(get("xiaomi.phone_rev.2025") * 1e3 / fx, get("xiaomi.phone_units.2025"),
                                 get("xiaomi.phone_gm.2025"))
    t_rev, t_gp = chain.per_unit(get("transsion.revenue.2025") * get("transsion.phone_rev_share") * 1e3 / fx,
                                 get("transsion.units.2025"), get("transsion.gm.2025"))
    R["perphone"] = dict(apple=dict(units=units_fy25, rev=a_rev, gp=a_gp, gm=get("apple.gm_products.fy2025")),
                         xiaomi=dict(units=get("xiaomi.phone_units.2025"), rev=x_rev, gp=x_gp,
                                     gm=get("xiaomi.phone_gm.2025")),
                         transsion=dict(units=get("transsion.units.2025"), rev=t_rev, gp=t_gp,
                                        gm=get("transsion.gm.2025")))
    R["perphone"]["ratio"] = a_gp / x_gp
    R["perphone"]["pool"] = {k: v["units"] * v["gp"] / 1e3 for k, v in R["perphone"].items() if isinstance(v, dict)}

    # --- what the memory makers kept per Pro phone ---------------------------------------------------------------
    R["memory"] = dict(m17=d17.get("memory").amount, gm17=get("micron.gm.fy2025"),
                       m18=mem18_tf, gm18=get("micron.gm.fy2026"))
    R["memory"]["kept17"] = R["memory"]["m17"] * R["memory"]["gm17"]
    R["memory"]["kept18"] = R["memory"]["m18"] * R["memory"]["gm18"]

    # --- storage tiers: Pro Max, 2025 -> 2026 -----------------------------------------------------------------------
    sizes = (256, 512, 1024, 2048)
    old, new = (1199, 1399, 1599, 1999), (1299, 1499, 1899, 2499)
    dram0, dram1 = get("memory.dram.2025"), get("memory.dram.2026")
    gb0 = get("memory.nand256.2025") / 256
    gb1_wsj = get("memory.nand256.2026") / 256
    gb1_cp = get("memory.nand1tb.2026") / 1024
    wsj = chain.tier_passthrough(sizes, old, new, dram0, dram1, gb0, gb1_wsj)
    cp = chain.tier_passthrough(sizes, old, new, dram0, dram1, gb0, gb1_cp)
    R["tiers"] = [dict(gb=g, price_up=dp, mem_up_lo=m1, mem_up_hi=m2, old=o, new=n)
                  for (g, dp, m1, _), (_, _, m2, _), o, n in zip(wsj, cp, old, new)]

    # --- margins: what each link keeps of what it is paid ---------------------------------------------------------
    R["margins"] = [
        ("Micron (memory), FY2026", get("micron.gm.fy2026"), "gross"),
        ("SK hynix (memory), Q3 2026", get("skhynix.opm.q3_2026"), "operating"),
        ("Apple, services, FY2026", get("apple.gm_services.fy2026"), "gross"),
        ("Qualcomm, patent licensing, FY2026", get("qcom.qtl_ebt.fy2026"), "pre-tax"),
        ("TSMC (chips), Q3 2026", get("tsmc.gm.q3_2026"), "gross"),
        ("Micron (memory), FY2025", get("micron.gm.fy2025"), "gross"),
        ("Skyworks (radio chips), FY2026", get("skyworks.gm.fy2026"), "gross"),
        ("Apple, products, FY2026", get("apple.gm_products.fy2026"), "gross"),
        ("Corning (glass), 2025", get("corning.gm.2025"), "gross"),
        ("Qualcomm, chips, FY2026", get("qcom.qct_ebt.fy2026"), "pre-tax"),
        ("Transsion (phones), 2025", get("transsion.gm.2025"), "gross"),
        ("Sony, image sensors, FY2025", get("sony.iss_opm.fy2025"), "operating"),
        ("Xiaomi, smartphones, 2025", get("xiaomi.phone_gm.2025"), "gross"),
        ("Samsung, mobile, 2025", get("samsung.mx_opm.2025"), "operating"),
        ("Foxconn (assembly), 2025", get("foxconn.gm.2025"), "gross"),
    ]

    # --- iPhone history (Apple's 10-Ks; units reported until FY2018) -----------------------------------------------
    R["history"] = dict(
        years=list(range(2008, 2027)),
        sales=[6.742, 13.033, 25.179, 45.998, 78.692, 91.279, 101.991, 155.041, 136.700, 139.337, 164.888, 142.381,
               137.781, 191.973, 205.489, 200.583, 201.183, 209.586, 254.098],
        units=[11.627, 20.731, 39.989, 72.293, 125.046, 150.257, 169.219, 231.218, 211.884, 216.756, 217.722] +
              [None] * 8)

    # --- the market, 2025 -------------------------------------------------------------------------------------
    R["market"] = dict(total=get("market.units.2025"), brands=[
        ("Apple", get("share.apple.units.2025")), ("Samsung", get("share.samsung.units.2025")),
        ("Xiaomi", get("share.xiaomi.units.2025")), ("vivo", get("share.vivo.units.2025")),
        ("OPPO", get("share.oppo.units.2025")), ("Others", get("share.others.units.2025"))])
    return R


def main():
    R = results()
    OUT.mkdir(parents=True, exist_ok=True)
    (OUT / "computed.json").write_text(json.dumps(R, indent=1, default=float))
    d = R["dollar17"]
    print(f"iPhone 17 Pro ${d['price']:.0f}: Apple revenue {d['revenue']:.0f}, gross {d['gross']:.0f} "
          f"({100 * d['gross_margin']:.1f}%), profit {d['profit']:.0f} (range {d['profit_range'][0]:.0f}-"
          f"{d['profit_range'][1]:.0f})")
    for s in d["slices"]:
        print(f"   {s['label']:<32} {s['amount']:8.1f}")
    e = R["dollar18"]
    print(f"iPhone 18 Pro ${e['price']:.0f}: BOM {e['bom']:.0f} (WSJ {e['bom_wsj']:.0f}), memory {e['memory']:.0f} "
          f"(WSJ {e['memory_wsj']:.0f}; x{e['memory_multiple']:.1f}), gross margin {100 * e['gross_margin']:.1f}%, "
          f"profit {e['profit']:.0f} (WSJ {e['profit_wsj']:.0f})")
    p = R["perphone"]
    for k in ("apple", "xiaomi", "transsion"):
        print(f"   {k:<10} {p[k]['units']:6.1f}m phones  revenue/phone ${p[k]['rev']:6.0f}  gross/phone ${p[k]['gp']:5.0f}"
              f"  pool ${p['pool'][k]:5.1f}bn")
    print(f"   Apple keeps {p['ratio']:.0f}x Xiaomi's gross profit per phone")
    m = R["memory"]
    print(f"memory makers per Pro phone: ${m['m17']:.0f} at {100*m['gm17']:.0f}% -> ${m['kept17']:.0f};  "
          f"${m['m18']:.0f} at {100*m['gm18']:.0f}% -> ${m['kept18']:.0f}")
    for t in R["tiers"]:
        print(f"   {t['gb']:>5}GB  price +{t['price_up']}  memory +{t['mem_up_lo']:.0f} to +{t['mem_up_hi']:.0f}")
    print("value added:", R["added"])


if __name__ == "__main__":
    main()
