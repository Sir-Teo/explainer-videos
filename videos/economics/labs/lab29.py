"""Lab 29: the cycle as equilibrium: the business cycle by two filters, the cake by value function iteration with
its contraction, Markov chains by Tauchen and Rouwenhorst, Brock and Mirman's growth model on a grid, the Island's
real business cycle solved by the QZ decomposition with its impulse responses and simulated moments beside the data's,
the Frisch elasticity's effect on hours, and Gali's long-run VAR in two specifications."""

import numpy as np

from videos.coursekit import labs
from explainer.economics import data
from explainer.economics.agora import dp, rbc
from explainer.economics.island import truths

TITLE = "The cycle as equilibrium: dynamic programming and the real business cycle"
GOAL = ("Measure the American business cycle with two filters; solve the cake by value function iteration and "
        "watch the contraction; discretize a persistent AR(1); solve the stochastic growth model on a grid and check "
        "it against Brock and Mirman's formula; solve the Island's real business cycle by linearization, simulate "
        "it, and compare its moments with FRED's data; and re-estimate Gali's VAR with hours in growth rates and in "
        "levels.")
TASKS = [
    "The cake: set beta = 0.99. How many iterations does value function iteration need to reach 1e-10, and why?",
    "Rouwenhorst against Tauchen: with rho = 0.99 and 5 states, how far is Tauchen's chain from the true variance?",
    "Hansen: give the Island a Frisch elasticity of 1. Which moments get closer to the data, and which further?",
]


def _q(key):
    d = data.fred(key)
    return {x: v for x, v in zip(d["date"], d["value"]) if np.isfinite(v)}


def run(seed=0):
    lab = labs.Lab()
    T = truths(29)

    y = _q("GDPC1")
    ds = sorted(y)
    ly = np.log([y[d] for d in ds])
    hp = np.array(dp.hp_filter(ly)["cycle"])
    ham = np.array(dp.hamilton_filter(ly)["cycle"])
    lab.row("US real GDP: the cycle's s.d., HP and Hamilton", f"{100 * hp.std():.2f}%, {100 * ham.std():.2f}%")

    c = T["cake"]
    k = dp.cake(beta=c["beta"], n=301, iters=c["iters"])
    g = np.array(k["gaps"])
    ratio = float(np.median(g[5:60] / g[4:59]))
    assert abs(ratio - c["beta"]) < 1e-6
    w = np.array(k["w"])
    share = float(np.median((np.array(k["c"]) / w)[len(w) // 5:]))
    lab.row("the cake: iterations, the contraction's ratio, and the share eaten (exact 1 - beta)",
            f"{k['iterations']}, {ratio:.4f}, {share:.3f}")

    ch = T["chains"]
    for rho in (ch["rho"], ch["rho_high"]):
        for name, f in (("Tauchen", dp.tauchen), ("Rouwenhorst", dp.rouwenhorst)):
            m = dp.chain_moments(**f(ch["n"], rho, ch["sigma"]))
            stay = float(np.min(np.diag(np.array(f(ch["n"], rho, ch["sigma"])["P"]))))
            lab.row(f"{name}, rho = {rho}: s.d. and autocorrelation (truth "
                    f"{ch['sigma'] / np.sqrt(1 - rho ** 2):.4f}, {rho}); least chance of staying put",
                    f"{m['sd']:.4f}, {m['rho']:.4f}; {stay:.4f}")

    gr = T["growth"]
    full = rbc.growth_vfi(alpha=gr["alpha"], beta=gr["beta"], delta=1.0, rho=gr["rho"], sigma=gr["sigma"], nk=101,
                          nz=gr["nz"])
    kk, zz = np.array(full["k"]), np.array(full["z"])
    exact = gr["alpha"] * gr["beta"] * zz[:, None] * kk[None, :] ** gr["alpha"]
    err = float(np.max(np.abs(np.array(full["kprime"]) - exact) / exact))
    lab.row("growth on a grid with full depreciation: largest error against Brock and Mirman", f"{100 * err:.2f}%")

    r = T["rbc"]
    m = rbc.RBC(alpha=r["alpha"], beta=r["beta"], delta=r["delta"], rho=r["rho"], sigma=r["sigma"], n_ss=r["n_ss"])
    sol = m.solve()
    assert sol["bk_ok"]
    lab.row("the Island's linear system: roots (moduli); Blanchard-Kahn satisfied",
            ", ".join(f"{x:.4f}" for x in sol["moduli"]) + f"; {sol['bk_ok']}")
    irf = m.irf(12, 0.01)
    lab.row("a 1% technology shock on impact: output, hours, consumption, investment",
            f"{irf['y'][0]:.2f}%, {irf['n'][0]:.2f}%, {irf['c'][0]:.2f}%, {irf['i'][0]:.2f}%")
    sim = m.simulate(r["T"], r["seed"] + seed)
    mo = rbc.moments(sim)
    lab.row("the Island, HP-filtered: s.d. of output; relative s.d. of consumption, investment, hours",
            f"{mo['y']['sd']:.2f}%; {mo['c']['rel']:.2f}, {mo['i']['rel']:.2f}, {mo['n']['rel']:.2f}")

    keys = {"y": "GDPC1", "c": "PCECC96", "i": "GPDIC1", "n": "HOANBS", "w": "OPHNFB"}
    S = {k_: _q(v) for k_, v in keys.items()}
    dd = sorted(d for d in S["y"] if all(d in S[k_] for k_ in S) and "1948-01-01" <= d <= "2019-10-01")
    md = rbc.moments({k_: np.log([S[k_][d] for d in dd]) for k_ in S})
    cn = np.array(dp.hp_filter(np.log([S["n"][d] for d in dd]))["cycle"])
    cw = np.array(dp.hp_filter(np.log([S["w"][d] for d in dd]))["cycle"])
    cb = np.array(dp.hp_filter(np.log([S["n"][d] * S["w"][d] for d in dd]))["cycle"])   # business output
    lab.row("US 1948-2019, HP-filtered: s.d. of output; relative s.d. of consumption, investment; hours relative "
            "to business output", f"{md['y']['sd']:.2f}%; {md['c']['rel']:.2f}, {md['i']['rel']:.2f}; "
            f"{cn.std() / cb.std():.2f}")
    sn = {k_: np.array(dp.hp_filter(np.array(v))["cycle"]) for k_, v in sim.items()}
    lab.row("hours with output per hour: correlation in the data and on the Island",
            f"{np.corrcoef(cn, cw)[0, 1]:.2f}, {np.corrcoef(sn['n'], sn['w'])[0, 1]:.2f}")

    for f in (0.5, 2.0):
        mf = rbc.RBC(alpha=r["alpha"], beta=r["beta"], delta=r["delta"], rho=r["rho"], sigma=r["sigma"],
                     n_ss=r["n_ss"], frisch=f)
        mf.solve()
        lab.row(f"Frisch elasticity {f}: hours' s.d. relative to output",
                f"{rbc.moments(mf.simulate(r['T'], r['seed'] + seed))['n']['rel']:.2f}")

    lp = np.log([S["w"][d] for d in dd])
    lh = np.log([S["n"][d] for d in dd])
    t = np.arange(len(lh))
    dg = rbc.gali(np.diff(lp), np.diff(lh), reps=200, seed=seed)
    lv = rbc.gali(np.diff(lp), (lh - np.polyval(np.polyfit(t, lh, 1), t))[1:], differenced=False, reps=200,
                  seed=seed)
    lab.row("Gali's VAR: hours on impact of a technology shock, hours in growth rates and in levels",
            f"{dg['hours'][0]:+.2f}%, {lv['hours'][0]:+.2f}%")

    lab.note = ("A cycle is a gap from a trend, and its size depends on the filter. Value function iteration "
                "converges because the Bellman operator is a contraction with modulus beta. Tauchen's chain fails "
                "for very persistent shocks; Rouwenhorst's does not. The Island's real business cycle, with one "
                "technology shock and Hansen's indivisible labour, gets the size of the cycle and the order of "
                "volatilities right, but moves hours and productivity together where the data do not; with a "
                "Frisch elasticity like those measured on workers, hours hardly move at all. Whether a technology "
                "shock raises hours in the data depends on how hours enter the VAR.")

    fig, ax = labs.figure(2, size=(11, 4.4))
    ax[0].semilogy(np.arange(1, len(g) + 1), g, color=labs.BLUE)
    ax[0].set(title="The cake: the contraction", xlabel="iteration", ylabel="largest change")
    q = np.arange(len(irf["y"]))
    for key, col, nm in (("y", labs.BLUE, "output"), ("n", labs.ORANGE, "hours"), ("c", "grey", "consumption")):
        ax[1].plot(q, irf[key], color=col, label=nm)
    ax[1].set(title="A 1% technology shock on the Island", xlabel="quarter", ylabel="% from steady state")
    ax[1].legend()
    lab.fig = fig
    return lab
