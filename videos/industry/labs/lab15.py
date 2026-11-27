"""Lab 15: Moore's forecast, building a fab or booking a foundry, dies on a wafer and yield, TSMC's spending and
utilization, the toolmakers, fifty years of cheaper chips, the memory cycle, the trailing edge, where the chips go,
where they are made, the landscape and the industry's own forecast for 2026."""

import numpy as np

from explainer.industry.works import fab  # noqa: F401  (the tasks use it)
from videos.coursekit import labs
from videos.industry.industry15.compute import results

TITLE = "Semiconductors: the wafer, the fab, the split and the cycle"
GOAL = ("Follow Moore's 1965 forecast; choose between building a fab and booking a foundry; count dies and good dies on "
        "a wafer; read TSMC's spending, utilization and revenue per wafer; compare the toolmakers' margins; measure fifty "
        "years of cheaper chips; follow memory's boom and bust and the trailing edge's cycle; see where the chips go and "
        "where they are made; and score the industry's own forecast for 2026.")
TASKS = [
    "With fab.plan(volume, own=True) and fab.plan(volume, own=False), find the volume (wafers a month) at which owning "
    "the fab first earns more than booking the foundry. Then make the fab cost $30 billion (fab=fab.Fab(capex=30.0)): "
    "how far does the break-even move, and what does that say about who can afford the newest fabs?",
    "With fab.good_dies, find the die size (mm2) at which a wafer at 0.1 defects per cm2 gives half as many good dies as "
    "gross dies. Then compare a 600 mm2 die at 0.5 and at 0.1 defects per cm2: by what factor does a mature process "
    "multiply the good dies, and why do big AI chips arrive later on a new process than small phone chips?",
    "From the chapter's numbers (sales of $1,219.7 billion by September 2026 and a third quarter of $517.7 billion), "
    "find the fourth-quarter growth on the third that 2026 needs to pass $1.6, $1.7, $1.8 and $1.9 trillion. Which "
    "threshold would you give even odds, and how does your answer compare with the series' 65% on $1.8 trillion?",
]


def run(seed=0):
    lab = labs.Lab()
    R = results()

    h = R["hook"]
    lab.row("Moore, 1965: doubling a year; components forecast for 1975", f"x{h['rate']:.0f} a year; {h['target']:,.0f}")
    lab.row("TSMC, 2025: customers; products", f"{h['customers']:.0f}; {h['products']:,.0f}")

    g = R["run"]["games"]
    lab.row("Run it, cost per good die: foundry / own fab at 5k / 20k / 50k wafers a month",
            " / ".join(f"${g[f'{v}|foundry']['cost_die']:.0f} vs ${g[f'{v}|own']['cost_die']:.0f}" for v in (5000, 20000, 50000)))
    lab.row("Run it, profit a year ($bn): foundry / own at 5k / 20k / 50k",
            " / ".join(f"{g[f'{v}|foundry']['profit']:.2f} vs {g[f'{v}|own']['profit']:.2f}" for v in (5000, 20000, 50000)))
    lab.row("volume at which owning the fab first pays more (wafers a month)", f"{R['run']['even']:,.0f}")
    assert g["5000|foundry"]["profit"] > g["5000|own"]["profit"] and g["50000|own"]["profit"] > g["50000|foundry"]["profit"]

    y = R["yield"]
    lab.row("dies on a 300 mm wafer: 100 mm2 at 0.1/cm2 (gross, yield, good)",
            f"{y['small']['dpw']:.0f}, {100 * y['small']['y']:.0f}%, {y['small']['good']:.0f}")
    lab.row("dies on a 300 mm wafer: 800 mm2 at 0.1/cm2 (gross, yield, good)",
            f"{y['big']['dpw']:.0f}, {100 * y['big']['y']:.0f}%, {y['big']['good']:.0f}")

    f = R["fab"]
    lab.row("TSMC 2025: wafers shipped / capacity; utilization", f"{f['ship'][2025]:.1f}m / {f['capacity']:.0f}m+; {100 * f['util']:.0f}%")
    lab.row("TSMC: revenue per wafer 2023 / 2025 (NT$ thousand); 2025 in dollars",
            f"{f['per_wafer_twd'][2023] / 1000:.0f} / {f['per_wafer_twd'][2025] / 1000:.0f}; ${f['per_wafer_usd']:,.0f}")
    lab.row("TSMC: capital spending per dollar of revenue, lowest and highest year 2015-2025",
            f"{100 * min(f['capex_share'].values()):.0f}% / {100 * max(f['capex_share'].values()):.0f}%")

    t = R["tools"]
    lab.row("ASML 2025: revenue; gross margin; systems sold (EUV)", f"€{t['asml_rev']:.1f}bn; {t['asml_gm']:.1f}%; {t['asml_units']:.0f} ({t['asml_euv']:.0f})")
    lab.row("toolmakers and design software: profit kept, latest year",
            " / ".join(f"{k} {100 * v['net'] / v['revenue']:.0f}%" for k, v in t["companies"].items()))

    hs = R["history"]
    lab.row("US output of chips since 1972; real producer price since 1967; transistors double every",
            f"x{hs['ip_x']:,.0f}; -{100 * hs['real_fall']:.0f}%; {hs['doubling']:.2f} years")

    m = R["memory"]
    lab.row("world memory sales 2022 / 2023 / 2025 / 2026 forecast ($bn)",
            " / ".join(f"{m['wsts'][k]:.0f}" for k in (2022, 2023, 2025, "2026f")))
    lab.row("Micron: worst quarter's operating income; latest quarter's revenue and operating income ($bn)",
            f"{m['mu_low'][2]:.1f} ({m['mu_low'][0]}); {m['mu_last'][1]:.1f}, {m['mu_last'][2]:.1f} ({m['mu_last'][0]})")

    tr = R["trailing"]
    lab.row("TSMC 2025: wafer revenue from 28nm and older", f"{tr['mature']:.0f}%")
    lab.row("analog and power makers: net margin 2025",
            " / ".join(f"{k} {100 * v[2025]:.0f}%" for k, v in tr["margins"].items() if 2025 in v))

    mk = R["markets"]
    lab.row("world sales by product 2025 ($bn)", " / ".join(f"{k} {v:.0f}" for k, v in mk["products"].items()))
    py = mk["plat_years"]
    lab.row("TSMC: high-performance computing's share 2023 / 2024 / 2025 / 3Q 2026",
            " / ".join(f"{py[k]['hpc']:.0f}%" for k in ("2023", "2024", "2025", "3Q 2026")))

    ge = R["geography"]
    lab.row("TSMC's fabs: in operation / in Taiwan; best abroad", f"{ge['n_fabs']} / {ge['n_taiwan']}; {ge['best_abroad']:.0f}nm")
    lab.row("sales by buyer's region, 2025 -> 2026 forecast ($bn)",
            " / ".join(f"{k} {a:.0f} -> {b:.0f}" for k, (a, b) in ge["regions"].items()))

    c = R["called"]
    lab.row("WSTS's forecast for 2026: December 2025 / May 2026 / August 2026",
            f"${c['aut']:.0f}bn / ${c['spring']:.0f}bn / ${c['q2calc']:.0f}bn")
    lab.row("sold by September 2026; fourth quarter needed for $1.8tn (growth on the third)",
            f"${c['to_sep']:,.1f}bn; ${c['q4_needed']:.0f}bn (+{100 * c['q4_growth']:.0f}%)")
    lab.row("this series' call: 2026 above $1.8 trillion", f"{100 * c['prob']:.0f}%")

    fig, (ax1, ax2) = labs.figure(2)
    vols = np.arange(2_000, 50_001, 1_000)
    for own, col, name in ((False, labs.BLUE, "book the foundry"), (True, labs.GOLD, "build the fab")):
        ax1.plot(vols / 1000, [fab.plan(v, own)["profit"] for v in vols], color=col, lw=1.8, label=name)
    ax1.axhline(0, color="grey", lw=0.8)
    ax1.set_xlabel("wafers a month (thousand)")
    ax1.set_ylabel("profit a year, $bn")
    ax1.set_title("Build or book (the Works)")
    ax1.legend(fontsize=7)
    trn = R["history"]["transistors"]
    ys = sorted(trn)
    ax2.semilogy(ys, [trn[k] for k in ys], "o", color=labs.PURPLE, ms=3)
    ax2.semilogy(ys, [trn[ys[0]] * 2 ** ((k - ys[0]) / 2) for k in ys], color=labs.GOLD, lw=1.2, label="doubling every two years")
    ax2.set_ylabel("transistors on a microprocessor")
    ax2.set_title("Moore's law, 1971-2021 (Rupp)")
    ax2.legend(fontsize=7)
    lab.fig = fig
    lab.note = ("A chip is cheap because a fab is dear: the fixed cost of the newest factory is spread over the whole "
                "world's demand, so only the foundry with the most customers, the toolmaker with no rival and the "
                "designer with the best chip keep much of the dollar; memory and the trailing edge ride their own cycles.")
    return lab
