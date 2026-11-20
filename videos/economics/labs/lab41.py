"""Lab 41: taxes: Laffer's curve and its peak, Harberger's incidence of a capital tax from a closed to an open
economy, the deadweight triangle against its approximation, Ramsey's inverse-elasticity rule against a uniform rate,
Diamond's optimal schedule, Saez's top rate from the Pareto parameter America's top shares imply, bunching at a kink,
and Allingham and Sandmo's evader."""

import numpy as np

from videos.coursekit import labs
from explainer.economics import data
from explainer.economics.agora import distribution as D
from explainer.economics.agora import tax as T
from explainer.economics.island import truths

TITLE = "Taxes"
GOAL = ("Find the revenue-maximizing rate for a constant elasticity; follow a capital tax's burden from owners to "
        "workers as capital becomes mobile; check Harberger's triangle against the exact loss; raise a fixed revenue "
        "by Ramsey's rule and by a uniform rate; compute an optimal income-tax schedule and the top rate from "
        "America's data; and estimate an elasticity from bunching.")
TASKS = [
    "Incidence: with alpha = 0.3, at what supply elasticity of capital do workers bear half of a 20% capital tax? "
    "And what elasticity puts the Laffer curve's top at 60%?",
    "The top rate: using a = 1.56, which elasticity makes 37% the revenue-maximizing top rate? Which welfare weight "
    "g on top earners makes it optimal when e = 0.25?",
    "Bunching: double the optimization frictions. What happens to the estimate, and why does widening the excluded "
    "window help?",
]


def run(seed=0):
    lab = labs.Lab()
    T41 = truths(41)

    t = np.linspace(0, 0.99, 991)
    peaks = []
    for e in T41["laffer"]["e"]:
        r = T.laffer(t, e)
        peaks.append((e, float(t[int(np.argmax(r))]), T.laffer_peak(e)))
    lab.row("Laffer: elasticity, peak on the grid, 1 / (1 + e)",
            "; ".join(f"e = {e:g}: {100 * a:.1f}%, {100 * b:.1f}%" for e, a, b in peaks))
    assert all(abs(a - b) < 0.002 for _, a, b in peaks)

    H = T41["harberger"]
    rows = [(e, T.harberger(H["tau"], e, alpha=H["alpha"])) for e in H["eta"]]
    op = T.harberger(H["tau"], np.inf, alpha=H["alpha"])
    lab.row("Harberger: workers' share of the burden as capital's supply elasticity rises",
            ", ".join(f"{e:g}: {100 * r['worker_share']:.0f}%" for e, r in rows)
            + f"; open: {100 * op['worker_share']:.0f}%")
    lab.row("small open economy: workers' loss per dollar of revenue", f"{op['worker_per_revenue']:.2f}")
    assert rows[0][1]["worker_share"] < 1e-9 and op["worker_per_revenue"] > 1

    P = T41["triangle"]
    tr = [T.triangle(x, P["eps_d"], P["eps_s"]) for x in (0.1, 0.2, 0.4)]
    lab.row("the triangle: tax, exact loss per dollar of revenue, Harberger's approximation per dollar",
            "; ".join(f"{100 * r['t']:.0f}%: {100 * r['dwl'] / r['revenue']:.1f}%, "
                      f"{100 * r['approx'] / r['revenue']:.1f}%" for r in tr))
    lab.row("share of the tax borne by buyers (eps_s / (eps_d + eps_s))",
            f"{tr[0]['buyer_share']:.3f} vs {P['eps_s'] / (P['eps_d'] + P['eps_s']):.3f}")

    R = T41["ramsey"]
    rm = T.ramsey(R["eps"], R["revenue"])
    lab.row("Ramsey: rates on " + ", ".join(R["goods"]) + "; the uniform rate",
            ", ".join(f"{100 * x:.1f}%" for x in rm["ramsey"]) + f"; {100 * rm['uniform']:.1f}%")
    lab.row("deadweight loss: Ramsey, uniform", f"{rm['total_ramsey']:.4f}, {rm['total_uniform']:.4f} "
            f"({rm['total_uniform'] / rm['total_ramsey']:.1f} times)")
    assert rm["total_ramsey"] < rm["total_uniform"]

    M = T41["mirrlees"]
    ds = T.diamond_schedule(M["e"], M["nu"], M["mu"], M["sigma"], M["alpha"], M["tail"])
    at = {q: float(np.interp(q, ds["F"], ds["Tprime"])) for q in (0.1, 0.5, 0.9, 0.999)}
    lab.row("Diamond's schedule: marginal rate at the 10th, 50th, 90th and 99.9th percentiles; the limit",
            ", ".join(f"{100 * v:.0f}%" for v in at.values()) + f"; {100 * ds['top']:.0f}%")

    S = data.saez()
    k = S["year"].index(2022)
    a = D.pareto_alpha(S["top1"][k], S["top01"][k], 0.01, 0.001)
    lab.row("America's 2022 top shares: the Pareto exponent a (= z_m / (z_m - threshold))", f"{a:.3f}")
    rates = {e: T.top_rate(a, e) for e in T41["top"]["e"]}
    lab.row("the revenue-maximizing top rate for e = " + ", ".join(f"{e:g}" for e in rates),
            ", ".join(f"{100 * v:.0f}%" for v in rates.values()))
    taus = np.linspace(0, 0.99, 991)
    for e in (0.25, 1.0):
        rv = T.top_revenue(taus, a, e)
        assert abs(taus[int(np.argmax(rv))] - T.top_rate(a, e)) < 0.002

    B = T41["bunching"]
    bu = T.bunching(n=B["n"], e=B["e"], z_star=B["z_star"], t0=B["t0"], t1=B["t1"], friction=B["friction"],
                    seed=B["seed"] + seed)
    lab.row("bunching at a kink from 20% to 40%: the true elasticity, the estimate, the share bunched",
            f"{bu['e']:g}, {bu['e_hat']:.3f}, {100 * bu['share_bunched']:.1f}%")
    assert abs(bu["e_hat"] - bu["e"]) < 0.06

    Ev = T41["evasion"]
    ps = (0.01, 0.1, 0.2, 0.3, 0.5)
    lab.row("Allingham and Sandmo: share declared at audit rates " + ", ".join(f"{100 * p:.0f}%" for p in ps),
            ", ".join(f"{100 * T.allingham_sandmo(p, Ev['t'], Ev['theta'], Ev['rho']):.0f}%" for p in ps))
    lab.row("full honesty is a fair bet only when p (1 + theta) >= 1, an audit rate of at least",
            f"{100 / (1 + Ev['theta']):.0f}% (a risk-neutral taxpayer otherwise declares nothing)")

    lab.note = ("The revenue-maximizing rate falls with the elasticity: 80% at e = 0.25, 50% at e = 1. A capital tax "
                "falls on owners when capital cannot leave and on workers, more than one for one, when it can. "
                "Losses grow with the square of the rate, so many small taxes beat one large one, and Ramsey's rule "
                "taxes most what people buy regardless. With America's Pareto tail the top rate that raises the "
                "most is 72% at e = 0.25 and 39% at e = 1: the formula is simple, the elasticity is the argument.")

    fig, ax = labs.figure(2, size=(11, 4.4))
    for e in T41["laffer"]["e"]:
        ax[0].plot(t, T.laffer(t, e), label=f"e = {e:g}")
    ax[0].set(title="Laffer's curve", xlabel="tax rate", ylabel="revenue per unit of untaxed base")
    ax[0].legend()
    ax[1].plot(np.array(ds["F"]), 100 * np.array(ds["Tprime"]), color=labs.ORANGE)
    ax[1].set(title="Diamond's optimal marginal rates", xlabel="percentile of skill", ylabel="marginal rate, %",
              ylim=(0, 100))
    lab.fig = fig
    return lab
