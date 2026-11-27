"""Lab 16: Shih's smile, a brand's order that needs a plant, a device's dollar, the contract manufacturers' margins and
Hon Hai's returns, its products and customer, Apple's products and services, the component makers, seventy-five years of
television prices, the PC, servers, where the plants are, tariffs and the move out of China, the landscape, and the
Commerce Secretary's forecast."""

import numpy as np

from explainer.industry.works import device  # noqa: F401  (the tasks use it)
from videos.coursekit import labs
from videos.industry.industry16.compute import results

TITLE = "Electronics: the smile, the assembler and the move"
GOAL = ("Draw Shih's smile from a device's dollar; decide whether to build the plant a brand asks for; see why turnkey "
        "revenue makes an assembler's margin thin and how fast capital makes up for it; read Hon Hai's own accounts; compare "
        "a brand's products and services; follow component makers through their cycles; measure seventy-five years of "
        "cheaper televisions; compare Intel with HP and Dell; see servers overtake phones; map where the plants are; follow "
        "phones and laptops out of China; and score a forecast that assembly would come to America.")
TASKS = [
    "With device.play(plan, p), find the renewal probability at which building the plant breaks even. Then let the "
    "brand pay half the plant (device.play('build', p, a=device.Assembler(plant=400e6))): how far does the break-even "
    "fall, and why do brands often "
    "pay for an assembler's tooling?",
    "With device.Device and device.Assembler, find the assembler's fee per device at which its profit on the Works' "
    "order, 20 million devices a year with turnkey revenue, is 5% of revenue. How large is that fee as a share of the "
    "device's $900 price?",
    "From the chapter's numbers (India's US smartphone sales of $18.5bn of $32.2bn from January to August 2026, and "
    "September-December 2025's $8.0bn of $20.7bn), find the share India needs in September-December 2026 for the year to "
    "pass one half. Is the series' 55% too high or too low?",
]


def run(seed=0):
    lab = labs.Lab()
    R = results()

    h = R["hook"]
    lab.row("Shih's smile: the year he drew it", f"{h['shih']:.0f}")
    lab.row("Hon Hai 2025: revenue (NT$ trillion, US$ billion); kept per dollar; operating margin",
            f"{h['hh_rev_twd'] / 1000:.2f}tn, ${h['hh_rev_usd']:.0f}bn; {100 * h['hh_kept']:.1f}%; {100 * h['hh_op']:.1f}%")
    lab.row("Apple FY2026: products and services gross margin", f"{h['aapl_gm_products']:.1f}% / {h['aapl_gm_services']:.1f}%")

    g = R["run"]["games"]
    lab.row("Run it, $m today: build / abroad / decline, if not renewed",
            " / ".join(f"{g[k]['no']:,.0f}" for k in ("build", "abroad", "decline")))
    lab.row("Run it, $m today: build / abroad, if renewed", " / ".join(f"{g[k]['yes']:,.0f}" for k in ("build", "abroad")))
    lab.row("renewal probability at which building breaks even; at which abroad beats home",
            f"{100 * g['build']['even']:.0f}%; about {100 * R['run']['cross']:.0f}%")
    assert g["build"]["no"] < 0 < g["build"]["yes"]

    d = R["dollar"]
    lab.row("the Works' $900 device: parts / parts makers' profit / assembler / brand costs / brand profit",
            " / ".join(f"${v:.0f}" for v in d["split"].values()))

    c = R["contract"]
    lab.row("net margin 2025: Jabil / Flex / Sanmina / Plexus / Benchmark / Celestica / Hon Hai",
            " / ".join(f"{100 * c['margins'][k].get(2025, float('nan')):.1f}%" for k in ("JBL", "FLEX", "SANM", "PLXS", "BHE", "CLS", "HONHAI")))
    lab.row("the Works' assembler: margin turnkey / consigned (same profit)",
            f"{100 * c['turnkey']['margin']:.1f}% / {100 * c['consigned']['margin']:.0f}%")
    lab.row("Hon Hai 2025: margin x turnover x leverage = return on equity",
            f"{100 * h['hh_kept']:.1f}% x {c['hh_turnover']:.2f} x {c['hh_leverage']:.2f} = {100 * c['hh_roe']:.1f}%")
    lab.row("Hon Hai 2025: inventory (days of costs); R&D (share of revenue)", f"{c['hh_inv_days']:.0f}; {100 * c['hh_rd']:.1f}%")

    hh = R["honhai"]
    lab.row("Hon Hai revenue by product, 2024 -> 2025 (NT$ tn)",
            " / ".join(f"{k} {a / 1000:.2f}->{b / 1000:.2f}" for k, (a, b) in hh["prod"].items()))
    lab.row("Hon Hai: largest customer's share 2024 / 2025; operating margin of servers arm / rest",
            f"{100 * hh['client_e'][0]:.0f}% / {100 * hh['client_e'][1]:.0f}%; {100 * hh['fii_margin']:.1f}% / {100 * hh['parent_margin']:.1f}%")

    b = R["brand"]
    lab.row("Apple FY2026: revenue; net income; Hon Hai's profit in dollars", f"${b['rev']:.0f}bn; ${b['ni']:.0f}bn; ${b['hh_ni_usd']:.1f}bn")

    comp = R["components"]["margins"]
    lab.row("net margin, latest: Amphenol / TE / Corning / ASE / LG Display",
            " / ".join(f"{100 * comp[k][max(comp[k])]:.1f}%" for k in ("APH", "TEL", "GLW", "ASX", "LPL")))

    hs = R["history"]
    lab.row("price indexes: TVs since 1951 (nominal, real); computers since 1998; smartphones since 2021",
            f"-{100 * hs['tv_fall']:.1f}%, -{100 * hs['real_tv_fall']:.2f}%; -{100 * hs['comp_fall']:.0f}%; -{100 * hs['phone_fall']:.0f}%")

    pc = R["pc"]
    lab.row("operating margin: Intel PC chips 2025 / HP PCs FY2025 / Dell PCs FY2026 / HP printing FY2025",
            f"{100 * pc['intel'][2025][1] / pc['intel'][2025][0]:.0f}% / {100 * pc['hp'][2025][1] / pc['hp'][2025][0]:.1f}% / "
            f"{100 * pc['dell'][2026][1] / pc['dell'][2026][0]:.1f}% / {100 * pc['hp_print'][1] / pc['hp_print'][0]:.1f}%")

    sv = R["servers"]["imports"]
    lab.row("US imports of processing units 2017 -> 2025 ($bn): world; Mexico; Taiwan; China",
            f"{sv['World'][2017]:.0f}->{sv['World'][2025]:.0f}; {sv['Mexico'][2017]:.0f}->{sv['Mexico'][2025]:.0f}; "
            f"{sv['Taiwan'][2017]:.1f}->{sv['Taiwan'][2025]:.0f}; {sv['China'][2017]:.1f}->{sv['China'][2025]:.1f}")

    nca = R["cluster"]["nca"]
    lab.row("Hon Hai's non-current assets 2024 -> 2025 (NT$bn): China / Vietnam / USA / India / Mexico",
            " / ".join(f"{nca[k][0]:.0f}->{nca[k][1]:.0f}" for k in ("cn", "vn", "us", "in", "mx")))
    j = R["cluster"]["jobs"]
    lab.row("US jobs making computers and electronics: 1990 / 2025 (thousands)", f"{j[1990]:,.0f} / {j[2025]:,.0f}")

    t = R["tariffs"]["china_share"]
    lab.row("China's share of US imports, 2018 / 2024 / 2025: phones; laptops",
            f"{100 * t['phones'][2018]:.0f}% / {100 * t['phones'][2024]:.0f}% / {100 * t['phones'][2025]:.0f}%; "
            f"{100 * t['laptops'][2018]:.0f}% / {100 * t['laptops'][2024]:.0f}% / {100 * t['laptops'][2025]:.0f}%")

    cl = R["called"]
    lab.row("India's share of US smartphone imports: January-August 2026; if Sep-Dec repeats 2025",
            f"{100 * cl['ytd_share']:.1f}%; {100 * cl['proj_share']:.1f}%")
    lab.row("this series' call: India above half in 2026", f"{100 * cl['prob']:.0f}%")

    fig, (ax1, ax2) = labs.figure(2)
    cv = R["run"]["curve"]
    ps = sorted(cv)
    for k, col in (("build", labs.GOLD), ("abroad", labs.PURPLE), ("decline", labs.BLUE)):
        ax1.plot([100 * p for p in ps], [cv[p][k] for p in ps], color=col, lw=1.8, label=k)
    ax1.axhline(0, color="grey", lw=0.8)
    ax1.set_xlabel("chance the brand renews, %")
    ax1.set_ylabel("$m today")
    ax1.set_title("The order that needs a plant (the Works)")
    ax1.legend(fontsize=7)
    P = R["tariffs"]["phones"]
    ys = sorted(P["World"])
    for p, col in (("China", labs.RED), ("India", labs.GOLD), ("Vietnam", labs.GREEN)):
        ax2.plot(ys, [100 * P[p].get(y, 0) / P["World"][y] for y in ys], color=col, lw=1.6, label=p)
    ax2.set_ylabel("share of US phone imports, %")
    ax2.set_title("Where America's phones come from (UN Comtrade)")
    ax2.legend(fontsize=7)
    lab.fig = fig
    lab.note = ("The assembler's thin margin comes from passing other people's parts through its revenue, from customers "
                "big enough to set its price and able to take the work elsewhere, and from a plant that stays when the order "
                "leaves; the ends of the smile keep more where they own something that cannot be swapped.")
    return lab
