"""Lab 23: capital and asset prices: the Gordon formula, Hayashi's firm, the option to wait, the Island's coconut tree
priced by its discount factor, Mehra and Prescott's economy, the Hansen-Jagannathan bound on Shiller's century of data,
and rare disasters."""

import numpy as np

from videos.coursekit import labs
from explainer.economics import data
from explainer.economics.agora import assets as ast
from explainer.economics.island import truths

TITLE = "Capital and asset prices: the discount factor, the premium and the puzzle"
GOAL = ("Value a growing stream; follow a firm's capital after its prospects improve; price an irreversible project's "
        "option to wait; price the Island's trees with its discount factor; solve Mehra and Prescott's economy; "
        "measure the equity premium and the Hansen-Jagannathan bound on Shiller's data; and see what rare disasters do.")
TASKS = [
    "Gordon: with dividends growing 3%, how much does a share lose when the discount rate rises from 7% to 8%, and "
    "from 4% to 5%? Why is the second loss larger?",
    "Mehra and Prescott: raise the persistence of consumption growth from 0.43 to 0.8. Does the largest premium with "
    "a safe rate below 4% rise or fall?",
    "Disasters: halve the chance of a disaster. What risk aversion now gives a 5% premium, and what safe rate comes "
    "with it?",
]


def run(seed=0):
    lab = labs.Lab()
    T = truths(23)

    g = T["gordon"]
    gd = ast.gordon(g["D1"], g["r"], g["g"])
    assert abs(gd["price"] - g["D1"] / (g["r"] - g["g"])) < 1e-9
    lab.row("Gordon: price at 7%, at 8%; duration", f"{gd['price']:.0f}, {gd['price_up']:.0f}; {gd['duration']:.0f} "
            "years")

    f = T["firm"]
    q = ast.q_investment(**f)
    lab.row("Hayashi's firm: q on impact; capital from, to", f"{q['q0']:.2f}; {q['K_old']:.2f} -> {q['K_new']:.2f}")

    o = T["option"]
    lab.row("option to wait: build at a multiple of cost, volatility 10-40%",
            ", ".join(f"{ast.option_to_wait(r=o['r'], mu=o['mu'], sigma=s)['multiple']:.2f}" for s in o["sigmas"]))

    p = T["playit"]
    price = 0.5 * p["m_good"] * p["pay_good"] + 0.5 * p["m_bad"] * p["pay_bad"]
    insurance = 0.5 * p["m_good"] * p["pay_bad"] + 0.5 * p["m_bad"] * p["pay_good"]
    lab.row("the coconut tree; the insurance tree (expected harvest 10)", f"{price:g}; {insurance:g}")

    mp = T["mp"]
    reg = ast.mp_region(np.linspace(0.05, mp["gamma_max"], 50), np.linspace(mp["beta_min"], 0.999, 50),
                        mu=mp["mu"], delta=mp["delta"], phi=mp["phi"])
    pts = np.array(reg["points"])
    best = pts[pts[:, 2] <= mp["rf_max"]][:, 3].max()
    assert best < 0.005
    lab.row("Mehra-Prescott: largest premium with a safe rate below 4%", f"{100 * best:.2f}%")

    d = data.shiller()
    y, R, rf, C = (np.array(d[k], float) for k in ("year", "Return", "RealR", "C"))
    gC = np.r_[C[1:] / C[:-1] - 1, np.nan]
    m = (y >= 1889) & (y <= 2009) & np.isfinite(R) & np.isfinite(rf) & np.isfinite(gC)
    ex = R[m] - (rf[m] - 1)
    sharpe = ex.mean() / ex.std()
    hj = ast.hj_bound(sharpe, gC[m].std(), [1])
    lab.row("Shiller 1889-2009: premium; Sharpe ratio; consumption s.d.; gamma needed",
            f"{100 * ex.mean():.1f}%; {sharpe:.2f}; {100 * gC[m].std():.1f}%; {hj['needed_gamma']:.1f}")

    dd = T["disasters"]
    beta = float(np.exp(-dd["rho"]))
    kw = {"g": dd["g"], "sd": dd["sd"], "sizes": dd["sizes"], "weights": dd["weights"]}
    w = ast.disasters(beta, 3.5, p=dd["p"], **kw)
    wo = ast.disasters(beta, 3.5, p=0.0, **kw)
    lab.row("rare disasters, gamma 3.5: premium and safe rate, with and without",
            f"{100 * w['premium']:.1f}% and {100 * w['rf']:.1f}%; {100 * wo['premium']:.2f}% and {100 * wo['rf']:.1f}%")

    lab.note = ("A long-lived asset loses a fifth of its value when the discount rate rises a point. Firms build toward "
                "a target that q measures, and wait when value is volatile. An asset that pays in good times is worth "
                "less than its expected payoff. With consumption as smooth as the data, power utility needs a risk "
                "aversion above eight to price stocks, and then the safe rate is absurd; rare disasters fix both.")

    fig, ax = labs.figure(2, size=(11, 4.4))
    ax[0].scatter(pts[:, 2], 100 * pts[:, 3], s=4, color=labs.BLUE)
    ax[0].scatter([0.008], [6.18], color=labs.ORANGE, s=30, label="the record, 1889-1978")
    ax[0].set(title="Mehra and Prescott's economy", xlabel="risk-free rate", ylabel="premium, %", xlim=(0, 0.2),
              ylim=(0, 7))
    ax[0].legend()
    gam = np.linspace(0.5, 4.2, 50)
    ax[1].plot(gam, [100 * ast.disasters(beta, x, p=dd["p"], **kw)["premium"] for x in gam], color=labs.ORANGE,
               label="with disasters")
    ax[1].plot(gam, [100 * ast.disasters(beta, x, p=0.0, **kw)["premium"] for x in gam], color=labs.BLUE,
               label="without")
    ax[1].set(title="Rare disasters and the premium", xlabel="risk aversion", ylabel="premium, %")
    ax[1].legend()
    lab.fig = fig
    return lab
