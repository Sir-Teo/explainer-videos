"""Lab 25: money: Kiyotaki and Wright's economy, the quantity theory across 146 countries, Cagan's inflation tax and its
two steady states, Baumol and Tobin's square-root rule, American money demand, the multiplier after 2008, and the cost of
inflation with cash in advance."""

import numpy as np

from videos.coursekit import labs
from explainer.economics import data
from explainer.economics.agora import money as mo
from explainer.economics.island import truths

TITLE = "Money: what becomes money, how much there is, and what too much does"
GOAL = ("Watch a medium of exchange emerge in a search economy; test the quantity theory on the world's data; find the "
        "inflation tax's peak and the two steady states of a printed deficit; derive the square-root rule; and price "
        "inflation in a cash-in-advance economy.")
TASKS = [
    "Kiyotaki-Wright: raise patience to 0.97. At what storage cost for fish does Ana start taking fish?",
    "The quantity theory: restrict the scatter to countries with average inflation below 10%. What happens to the "
    "slope and the correlation, and why?",
    "Cagan: with alpha = 5, what is the largest deficit the government can finance for ever when expectations adapt at "
    "10% a month, and at 30%?",
]


def run(seed=0):
    lab = labs.Lab()
    T = truths(25)

    k = T["kw"]
    fund = mo.kw_simulate(n=150, periods=300, speculative=False, seed=seed)
    spec = mo.kw_simulate(n=150, periods=300, speculative=True, seed=seed)
    assert fund["medium"][0] > 0.99
    fresh = mo.kw_best_response(fund["dist"], c=k["c"], u=k["u"], beta=k["beta"])
    smoked = mo.kw_best_response(spec["dist"], c=(k["c"][0], k["c"][1], k["c3_smoked"]), u=k["u"], beta=k["beta"],
                                 speculative=True)
    assert not fresh["accept_3"] and smoked["accept_3"]
    lab.row("Kiyotaki-Wright: media of exchange (salt, coconuts, fish), fresh; smoked",
            f"{np.round(fund['medium'], 2).tolist()}; {np.round(spec['medium'], 2).tolist()}")

    rows = data.wdi_money()
    by = {}
    for r in rows:
        if 1990 <= r["year"] <= 2024 and np.isfinite(r["money"]) and np.isfinite(r["cpi"]):
            by.setdefault(r["code"], []).append((np.log1p(r["money"] / 100), np.log1p(r["cpi"] / 100)))
    pts = np.array([np.mean(v, axis=0) for v in by.values() if len(v) >= 20])
    slope = np.polyfit(pts[:, 0], pts[:, 1], 1)[0]
    corr = np.corrcoef(pts[:, 0], pts[:, 1])[0, 1]
    assert 0.8 < slope < 1.1 and corr > 0.9
    lab.row("quantity theory, 1990-2024: countries; slope; correlation", f"{len(pts)}; {slope:.2f}; {corr:.2f}")

    c = T["cagan"]
    L = mo.cagan_laffer(c["alpha"])
    slow = mo.cagan_deficit(c["alpha"], c["deficit"], c["lam_slow"], periods=c["months"])
    fast = mo.cagan_deficit(c["alpha"], c["deficit"], c["lam_fast"], periods=c["months"])
    assert abs(L["best"] - 1 / c["alpha"]) < 0.01 and fast["exploded"] and not slow["exploded"]
    lab.row("Cagan: revenue-maximizing inflation; steady states for the deficit",
            f"{100 * L['best_exact']:.0f}% a month; {100 * slow['steady'][0]:.1f}% and {100 * slow['steady'][1]:.0f}%")

    b = T["baumol"]
    bt = mo.baumol_tobin(b["Y"], [0.005, 0.01, 0.02], b["b"])
    assert abs(bt["money"][0] / bt["money"][2] - 2.0) < 1e-9
    lab.row("Baumol-Tobin: money held at 0.5%, 1%, 2% a month", ", ".join(f"{m:.0f}" for m in bt["money"]))

    cia = mo.cia([0.0, 0.10], **T["cia"])
    lab.row("cash in advance: welfare cost of 0% and 10% inflation", ", ".join(f"{100 * x:.2f}%" for x in cia["loss"]))

    lab.note = ("A good that is cheap to keep becomes money without anyone deciding it; a costly one can too, if "
                "others accept it. Across countries inflation tracks money growth almost one for one. Printing to pay "
                "a deficit has a ceiling at one over the semi-elasticity, and with fast expectations even a payable "
                "deficit runs away. Money holdings fall with the square root of the interest rate, and inflation of "
                "ten percent costs about one percent of consumption.")

    fig, ax = labs.figure(2, size=(11, 4.4))
    ax[0].scatter(100 * np.expm1(pts[:, 0]), 100 * np.expm1(pts[:, 1]), s=10, color=labs.BLUE)
    ax[0].plot([0.5, 200], [0.5, 200], color="grey", lw=0.8)
    ax[0].set(xscale="log", yscale="log", xlim=(0.5, 200), ylim=(0.3, 200), title="Money growth and inflation, "
              "1990-2024", xlabel="broad money growth, % a year", ylabel="inflation, % a year")
    ax[1].plot(range(len(slow["path"])), 100 * np.array(slow["path"]), color=labs.BLUE, label="slow expectations")
    ax[1].plot(range(len(fast["path"])), np.minimum(100 * np.array(fast["path"]), 100), color=labs.ORANGE,
               label="fast expectations")
    ax[1].set(title="A printed deficit", xlabel="months", ylabel="inflation, % a month", ylim=(0, 100))
    ax[1].legend()
    lab.fig = fig
    return lab
