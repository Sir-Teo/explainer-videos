"""Lab 6: build a cycle out of a lead time, find it in sixty years of hogs, and read Micron's."""

import numpy as np

from explainer.industry.works import cycle
from videos.coursekit import labs
from videos.industry.industry6.compute import results

TITLE = "The cycle: lead times, the cobweb, the bullwhip and the accelerator"
GOAL = ("Run the Works' shipping market with lead times of one to four years and measure the swings; check the "
        "cobweb's stability rule; measure the hog cycle in the NBER's Chicago data; amplify noise through a supply "
        "chain; and find every peak in Micron's quarterly sales and the fall that followed.")
TASKS = [
    "Rerun the fleet model with a lead time of three years but owners who react half as strongly (k = 0.175). "
    "How much smaller is the swing, and what does that suggest about owners who order cautiously?",
    "Repeat the hog analysis for 1900-1940 only, and with a three-year instead of a five-year trend. Does the "
    "cycle's length change? Why might the trend you remove change the cycle you find?",
    "Change the bullwhip chain so each tier keeps four weeks of stock instead of two. Does the whip get worse or "
    "better, and why does holding more stock amplify orders?",
]


def run(seed=0):
    lab = labs.Lab()
    R = results()

    # 1. lead times: the same market, waits of one to four years
    sw = {L: cycle.swing(cycle.fleet(years=60, lead=L, k=0.35)["rate"], 15) for L in (1, 2, 3, 4)}
    assert all(sw[L + 1] > sw[L] for L in (1, 2, 3))
    assert abs(sw[3] - R["fleet"]["swing"][3]) < 1e-12
    lab.row("swing of the freight rate, lead time 1 / 2 / 3 / 4 years",
            " / ".join(f"{100 * sw[L]:.0f}%" for L in (1, 2, 3, 4)))

    # 2. the cobweb: converges when supply responds less than demand
    pe, _ = cycle.cobweb_eq(10, 1, 0, 0.8)
    p, _ = cycle.cobweb(10, 1, 0, 0.8, pe + 2.6, n=20)
    p2, _ = cycle.cobweb(10, 1, 0, 1.25, cycle.cobweb_eq(10, 1, 0, 1.25)[0] + 0.6, n=20)
    lab.row("cobweb, gap from equilibrium after 20 years: d = 0.8 / d = 1.25",
            f"{abs(p[-1] - pe):.3f} / {abs(p2[-1] - cycle.cobweb_eq(10, 1, 0, 1.25)[0]):.1f}")

    # 3. the hogs
    H = R["hogs"]
    lab.row("hogs, 1880-1940: same-month correlation of price and slaughter", f"{H['same']:.2f}")
    lab.row("hogs: lag (months) at which a high price best predicts more hogs, and the correlation",
            f"{H['best_lag']} months, {H['best']:.2f}")
    lab.row("hogs: length of one full swing (spectral peak of slaughter)", f"{H['period_slaughter']:.1f} years")

    # 4. the bullwhip
    rng = np.random.default_rng(seed)
    chain = cycle.bullwhip(100 + rng.normal(0, 4, 300), tiers=3)
    sds = [np.std(chain[i, 30:]) for i in range(4)]
    assert all(b > a for a, b in zip(sds, sds[1:]))
    lab.row("bullwhip: spread of sales and of each tier's orders", " / ".join(f"{s:.1f}" for s in sds))
    B = R["bullwhip"]
    lab.row("America, 1993-2026: typical monthly change of retail sales / factory orders",
            f"{100 * B['sd_retail']:.2f}% / {100 * B['sd_orders']:.2f}% (x{B['ratio']:.1f})")

    # 5. Micron's peaks
    for pk in R["micron"]["peaks"]:
        fall = "still open" if pk["fall"] is None else f"{100 * pk['fall']:+.0f}% by {pk['low_end']}"
        lab.row(f"Micron peak quarter {pk['end']}: ${pk['value']:.2f}bn", fall)
    rd = dict(R["reading"]["micron"])
    lab.row("Micron capital spending / depreciation, fiscal 2023 and 2026", f"{rd[2023]:.1f} and {rd[2026]:.1f}")

    fig, (ax1, ax2) = labs.figure(2)
    for L, col in ((1, labs.GREY), (3, labs.GOLD), (4, labs.RED)):
        f = cycle.fleet(years=60, lead=L, k=0.35)
        ax1.plot(f["rate"][10:50], color=col, label=f"lead {L} years")
    ax1.axhline(1.0, color=labs.GREY, lw=0.8, ls="--")
    ax1.set_xlabel("year")
    ax1.set_ylabel("freight rate / running cost")
    ax1.set_title("Same demand, longer waits, bigger swings")
    ax1.legend(fontsize=8)
    m = R["micron"]
    ax2.plot(range(len(m["q_revenue"])), m["q_revenue"], color=labs.BLUE)
    ticks = [i for i, q in enumerate(m["quarters"]) if q[5:7] in ("08", "09") and int(q[:4]) % 4 == 2]
    ax2.set_xticks(ticks)
    ax2.set_xticklabels([m["quarters"][i][:4] for i in ticks])
    ax2.set_yscale("log")
    ax2.set_ylabel("revenue a quarter, $bn (log scale)")
    ax2.set_title("Micron: four busts and a boom")
    lab.fig = fig
    lab.note = ("A lead time and a forecast made from today's price are enough to make a cycle; real hog farmers and "
                "memory makers show it, and the swings grow up a supply chain and in the makers of machines.")
    return lab
