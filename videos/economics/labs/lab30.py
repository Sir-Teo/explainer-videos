"""Lab 30: sticky prices: Mankiw's menu-cost arithmetic, Calvo's slope, the Taylor rule on FRED's data, determinacy and
the Taylor principle, impulse responses of the three-equation model, discretion against commitment, the selection
effect among simulated price setters, the zero lower bound with forward guidance, and the hump with habits and
indexation."""

import numpy as np

from videos.coursekit import labs
from explainer.economics import data
from explainer.economics.agora import nk
from explainer.economics.island import truths

TITLE = "Sticky prices: the New Keynesian model, built and solved"
GOAL = ("Compute the private and social cost of a sticky price; derive the slope of the New Keynesian Phillips curve "
        "from Calvo's theta; fit Taylor's rule; check determinacy over policy rules; solve the three-equation model "
        "for three shocks; compare discretion and commitment; race Calvo against menu costs with simulated firms; and "
        "put the economy in a liquidity trap and get it out with promises.")
TASKS = [
    "Menu costs: with an elasticity of 3 instead of 6, how much profit does a 5% error cost, and how many sales?",
    "Determinacy: with phi_x = 0.5, what is the smallest phi_pi that gives a unique equilibrium, and why below one?",
    "Selection: double the idiosyncratic drift of firms' best prices. Does the menu-cost economy get closer to "
    "Calvo's or further away?",
]


def run(seed=0):
    lab = labs.Lab()
    T = truths(30)
    p = T["nk"]
    kw = {k: p[k] for k in ("beta", "sigma", "phi", "alpha", "eps", "theta", "phi_pi", "phi_x")}

    m = nk.menu_cost(T["menu"]["eps"], T["menu"]["gaps"])
    for r in m["rows"]:
        lab.row(f"a fare {100 * r['gap']:.0f}% too high: profit lost, sales lost",
                f"{100 * r['profit_loss']:.2f}%, {100 * r['output_loss']:.1f}% ({r['ratio']:.0f} to 1)")

    for th in (0.5, 2 / 3, 0.75):
        k = nk.kappa(th, p["beta"], p["sigma"], p["phi"], p["alpha"], p["eps"])
        d = nk.calvo_durations(th)
        lab.row(f"Calvo theta {th:.2f}: mean life (months), monthly frequency, kappa",
                f"{d['mean_months']:.1f}, {d['monthly_frequency']:.3f}, {k:.3f}")

    D, Y, P = (dict((x, v) for x, v in zip(data.fred(k)["date"], data.fred(k)["value"]) if np.isfinite(v))
               for k in ("GDPDEF", "GDPC1", "GDPPOT"))
    F = data.fred("FEDFUNDS")
    ff: dict = {}
    for x, v in zip(F["date"], F["value"]):
        if np.isfinite(v):
            ff.setdefault(f"{x[:4]}-{3 * ((int(x[5:7]) - 1) // 3) + 1:02d}-01", []).append(v)
    rows = []
    for d in sorted(D):
        prev = f"{int(d[:4]) - 1}{d[4:]}"
        if prev in D and d in Y and d in P and d in ff and "1987-07-01" <= d <= "2005-10-01":
            pi = 100 * (D[d] / D[prev] - 1)
            rows.append((pi, 100 * (Y[d] / P[d] - 1), float(np.mean(ff[d]))))
    R = np.array(rows)
    X = np.column_stack([np.ones(len(R)), R[:, 0], R[:, 1]])
    b, *_ = np.linalg.lstsq(X, R[:, 2], rcond=None)
    lab.row("Taylor's rule fitted, 1987-2005: constant, inflation, gap", f"{b[0]:.2f}, {b[1]:.2f}, {b[2]:.2f}")

    k = nk.kappa(p["theta"], p["beta"], p["sigma"], p["phi"], p["alpha"], p["eps"])
    for fp in (0.8, 0.99, 1.01, 1.5):
        d = nk.determinacy(fp, p["phi_x"], p["beta"], p["sigma"], k)
        lab.row(f"phi_pi = {fp}: unique equilibrium?", f"{d['unique']} (roots {d['moduli'][0]:.3f}, "
                f"{d['moduli'][1]:.3f})")

    for s in ("monetary", "demand", "cost"):
        r = nk.irf_ar1(s, rho_s=p["rho_shock"], size=p["size"], **kw)
        lab.row(f"a {s} shock on impact: gap, inflation, policy rate", f"{r['x'][0]:+.3f}%, {r['pi'][0]:+.3f}, "
                f"{r['i'][0]:+.3f}")

    o = nk.optimal_policy(rho_u=p["rho_shock"], size=p["size"], **kw)
    lab.row("a cost-push shock: loss under discretion and commitment; the price level at the end",
            f"{o['loss_d']:.4f}, {o['loss_c']:.4f}; {o['price_d'][-1]:.3f}% and {o['price_c'][-1]:.3f}%")

    S = T["setters"]
    c = nk.price_setters("calvo", n=S["n"] // 2, freq=S["freq"], shock=S["shock"], sigma_a=S["sigma_a"],
                         months=S["months"], seed=S["seed"] + seed)
    mm = nk.price_setters("menu", n=S["n"] // 2, freq=S["freq"], shock=S["shock"], sigma_a=S["sigma_a"],
                          months=S["months"], seed=S["seed"] + seed)
    lab.row("money up 5%: share passed into prices after 1, 3 and 6 months, Calvo",
            ", ".join(f"{100 * c['pass_through'][i]:.0f}%" for i in (0, 2, 5)))
    lab.row("the same, menu costs", ", ".join(f"{100 * mm['pass_through'][i]:.0f}%" for i in (0, 2, 5)))

    Z = T["zlb"]
    for e in Z["extras"]:
        z = nk.zlb(T=Z["T"], rn_low=Z["rn_low"], extra=e, **kw)
        lab.row(f"the trap with {e} extra quarters at zero: gap and inflation on impact",
                f"{z['x'][0]:+.2f}%, {z['pi'][0]:+.2f}")

    H = T["hybrid"]
    h = nk.hybrid_irf(habit=H["habit"], index=H["index"], smooth=H["smooth"], rho_v=p["rho_shock"], size=p["size"],
                      **kw)
    lab.row("habits, indexation and smoothing: the trough of output after a tightening",
            f"quarter {h['peak_x']}, {min(h['x']):.3f}%")

    lab.note = ("A price error costs its setter a second-order amount and the economy a first-order one, so small "
                "menu costs can make money matter. Calvo's theta sets the Phillips curve's slope; the Federal Reserve "
                "of the Greenspan years responded more than one for one to inflation, which is what makes the "
                "model's equilibrium unique. Demand shocks can be offset completely, cost shocks cannot; commitment "
                "beats discretion by bringing the price level back. Menu costs with idiosyncratic shocks pass money "
                "into prices far faster than Calvo at the same frequency. At the zero bound, promises are enormously "
                "powerful in the model, which is the forward-guidance puzzle.")

    fig, ax = labs.figure(2, size=(11, 4.4))
    months = np.arange(1, len(c["pass_through"]) + 1)
    ax[0].plot(months, c["pass_through"], color=labs.BLUE, label="Calvo")
    ax[0].plot(months, mm["pass_through"], color=labs.ORANGE, label="menu costs")
    ax[0].set(title="Money up 5%: pass-through", xlabel="months", ylabel="share")
    ax[0].legend()
    q = np.arange(len(o["pi_d"]))
    ax[1].plot(q, o["pi_d"], color=labs.ORANGE, label="discretion")
    ax[1].plot(q, o["pi_c"], color=labs.BLUE, label="commitment")
    ax[1].set(title="A cost-push shock: inflation", xlabel="quarters", ylabel="% a year")
    ax[1].legend()
    lab.fig = fig
    return lab
