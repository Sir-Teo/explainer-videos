"""Lab 20: growth and capital: the Solow model's steady state, golden rule and speed of convergence; Harrod and
Domar's knife edge; convergence regressions, growth accounting and development accounting on the Penn World Table;
Lucas's calculation; and the Ramsey model solved by shooting."""

import numpy as np

from videos.coursekit import labs
from explainer.economics import data
from explainer.economics.agora import growth as gr
from explainer.economics.island import truths

TITLE = "Growth I: Solow, convergence and the residual"
GOAL = ("Find the Solow island's steady state and its golden rule; measure how fast it converges, in theory and in a "
        "simulation; test convergence across countries with and without controls; take American growth apart into "
        "capital, schooling and the residual; split income gaps across countries the same way; redo Lucas's "
        "calculation; and find the Ramsey economy's saddle path by shooting.")
TASKS = [
    "Convergence: rerun the 1960-2019 regression with only investment as a control, then only schooling. Which "
    "control does most to turn the slope negative?",
    "Growth accounting: take the United States apart for 1995-2005 and 2005-2019. How much of the slowdown in output "
    "per hour is the residual, and how much capital deepening?",
    "Ramsey: raise theta from 2 to 4. What happens to the steady state's capital and the saving rate, and why does "
    "the saddle path start with lower consumption?",
]


def run(seed=0):
    lab = labs.Lab()
    T = truths(20)
    kw = {k: T["solow"][k] for k in ("n", "g", "delta", "alpha")}

    st = gr.solow_steady(T["solow"]["s0"], **kw)
    assert abs(st["ky"] - T["solow"]["s0"] / (kw["n"] + kw["g"] + kw["delta"])) < 1e-12
    lab.row("island at s = 15%: k*, y*, c*, capital-output ratio",
            f"{st['k']:.3f}, {st['y']:.3f}, {st['c']:.3f}, {st['ky']:.3f}")
    gold = gr.golden_rule(**kw)
    assert abs(gold["s_gold"] - kw["alpha"]) < 2e-3                       # s = alpha under Cobb-Douglas
    lab.row("golden rule: saving rate, steady-state consumption", f"{gold['s_gold']:.3f}, {gold['c_gold']:.3f}")
    sp = gr.convergence_speed(**kw)
    lab.row("speed of convergence: lambda, half-life (linear), half-life (simulated from k*/4)",
            f"{100 * sp['lambda']:.2f}% a year, {sp['half_life']:.1f}, {sp['half_life_simulated']} years")
    p = gr.solow_path(lambda t: 0.30 if t >= 10 else 0.15, 200, k0=st["k"], **kw)
    gain = p["y"][-1] / p["y"][0]
    assert abs(gain - 2 ** (kw["alpha"] / (1 - kw["alpha"]))) < 1e-3        # a level effect of 2^(alpha/(1-alpha))
    lab.row("doubling saving: output per effective worker, long run", f"x{gain:.3f}")

    hd = gr.harrod_domar(0.2, 3.5, delta=0.03, labour=0.01)
    lab.row("Harrod-Domar at s = 20%, v = 3.5: growth; saving needed for 7%",
            f"{100 * hd['growth']:.2f}%; {100 * hd['needed_for_target'](0.07):.0f}%")

    by = {}
    for r in data.pwt():
        by.setdefault(r["countrycode"], {})[r["year"]] = r
    rows = []
    for c, d in by.items():
        a, b = d.get(1960), d.get(2019)
        if not (a and b) or not all(np.isfinite([a["rgdpna"], a["pop"], b["rgdpna"], b["pop"], a["hc"]])):
            continue
        if a["pop"] < 1:
            continue
        inv = [d[y]["csh_i"] for y in range(1960, 2020) if y in d and np.isfinite(d[y]["csh_i"]) and d[y]["csh_i"] > 0]
        if len(inv) < 48:
            continue
        rows.append((a["rgdpna"] / a["pop"], b["rgdpna"] / b["pop"], np.mean(inv),
                     np.log(b["pop"] / a["pop"]) / 59, a["hc"]))
    y0, y1, s_, n_, h_ = map(np.array, zip(*rows))
    ab = gr.convergence(y0, y1, 59)
    co = gr.convergence(y0, y1, 59, controls=[np.log(s_), np.log(n_ + 0.05), np.log(h_)])
    assert co["slope"] < ab["slope"]
    lab.row(f"convergence 1960-2019 ({len(rows)} countries): absolute slope (s.e.); conditional slope (s.e.), lambda",
            f"{ab['slope']:+.4f} ({ab['se']:.4f}); {co['slope']:+.4f} ({co['se']:.4f}), {100 * co['lambda']:.2f}%")

    us = gr.growth_accounting(data.pwt("USA"), 1950, 2019)
    assert abs(us["deepening"] + us["human_capital"] + us["tfp"] - us["per_hour"]) < 1e-12
    lab.row("United States 1950-2019, per hour: growth = deepening + schooling + residual",
            f"{100 * us['per_hour']:.2f} = {100 * us['deepening']:.2f} + {100 * us['human_capital']:.2f} + "
            f"{100 * us['tfp']:.2f} (residual {100 * us['tfp_share_per_hour']:.0f}%)")

    dev = gr.development_accounting([r for r in data.pwt(year=2019) if np.isfinite(r["pop"]) and r["pop"] >= 1])
    lab.row("development accounting 2019: variance share of the factors (Hall-Jones form; Caselli's)",
            f"{dev['share_factors']:.2f}; {dev['success']:.2f}")

    lu = gr.mpk_ratio(1.0, 15.0, alpha=0.4, h_rich=5.0)
    lab.row("Lucas: return ratio for a fifteenfold gap, raw and with a fivefold skill gap",
            f"{lu['raw']:.1f}, {lu['with_human_capital']:.1f}")

    rt = T["ramsey"]
    rm = gr.ramsey(alpha=kw["alpha"], delta=kw["delta"], rho=rt["rho"], theta=rt["theta"], n=kw["n"], g=kw["g"],
                   k0_share=rt["k0_share"])
    assert rm["k_ss"] < (kw["alpha"] / (kw["n"] + kw["g"] + kw["delta"])) ** (1 / (1 - kw["alpha"]))
    lab.row("Ramsey: k* (golden rule's), saving rate, c0 on the saddle path",
            f"{rm['k_ss']:.3f} ({(kw['alpha'] / 0.08) ** 1.5:.3f}), {100 * (1 - rm['c_ss'] / rm['k_ss'] ** kw['alpha']):.1f}%, "
            f"{rm['c0']:.4f}")

    lab.note = ("Saving sets the level of income, not its long-run growth: doubling the island's saving raises output "
                "by 41% for good. The textbook speed of convergence is 5% a year; across countries, holding saving and "
                "schooling fixed, it is about 1.3%, and without controls there is none. The residual is about half of "
                "American growth per hour and most of the gap between rich and poor countries. An optimizing economy "
                "saves less than the golden rule.")

    fig, ax = labs.figure(2, size=(11, 4.4))
    g = gr.golden_rule(**kw)
    ax[0].plot(g["s"], g["c"], color=labs.BLUE)
    ax[0].axvline(kw["alpha"], color=labs.ORANGE, ls="--")
    ax[0].set(title="Steady-state consumption and the golden rule", xlabel="saving rate", ylabel="c*")
    ax[1].plot(rm["kdot0_k"], rm["kdot0_c"], color=labs.ORANGE, label="k' = 0")
    ax[1].axvline(rm["k_ss"], color=labs.BLUE, ls="--", label="c' = 0")
    ax[1].plot(rm["path_k"], rm["path_c"], color="black", label="saddle path")
    ax[1].set(title="The Ramsey phase diagram", xlabel="k", ylabel="c", ylim=(0, 2))
    ax[1].legend()
    lab.fig = fig
    return lab
