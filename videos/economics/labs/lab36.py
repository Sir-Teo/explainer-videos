"""Lab 36: scale, firms and gravity: Krugman's gains from variety and the home-market effect, gravity on CEPII's 2019
data by least squares and PPML with fixed effects, Melitz's cutoffs and a population of firms, Eaton and Kortum's
shares by formula and simulation, the gains-from-trade formula and an exact-hat-algebra counterfactual on 2019 trade,
and the shift-share design of the China shock on the Island's zones."""

import numpy as np

from videos.coursekit import labs
from explainer.economics import data
from explainer.economics.agora import trade
from explainer.economics.island import truths

TITLE = "Scale, firms and gravity"
GOAL = ("Compute the gains from variety and the home-market effect; estimate gravity on real 2019 trade by least "
        "squares and by PPML with fixed effects; solve Melitz's model and simulate its firms; check Eaton and "
        "Kortum's formula against a simulation; compute the gains from trade and a counterfactual by exact hat "
        "algebra; and see why the China shock needs an instrument.")
TASKS = [
    "Gravity: add the colonial tie and the trade agreement to the PPML regressors. How much does distance's "
    "coefficient move?",
    "Melitz: halve the fixed cost of exporting. What happens to the share of exporters and the gain from opening?",
    "Hat algebra: raise trade costs between America and Mexico instead of China. Who gains from diversion?",
]


def _gravity():
    G = data.gravity()
    g = {k: np.array(v, float) if k not in ("iso3_o", "iso3_d") else np.array(v) for k, v in G.items()}
    ok = (np.isfinite(g["tradeflow_baci"]) & np.isfinite(g["gdp_o"]) & np.isfinite(g["gdp_d"]) &
          np.isfinite(g["distw_harmonic"]) & (g["distw_harmonic"] > 0) & np.isfinite(g["contig"]) &
          np.isfinite(g["comlang_off"]))
    return {k: v[ok] for k, v in g.items()}


def run(seed=0):
    lab = labs.Lab()
    T = truths(36)

    K = T["krugman"]
    g2 = trade.krugman_variety(K["L"], K["f"], K["sigma"], 2)["welfare_gain"]
    lab.row("Krugman: real-wage gain from trading with one identical country; the home-market effect at 55%",
            f"{100 * g2:.1f}%; {100 * trade.home_market([0.55], K['phi'])[0]:.1f}% of firms")
    assert abs(g2 - (2 ** (1 / (K["sigma"] - 1)) - 1)) < 1e-12

    g = _gravity()
    X = np.column_stack([np.log(g["gdp_o"]), np.log(g["gdp_d"]), np.log(g["distw_harmonic"]), g["contig"],
                         g["comlang_off"]])
    R = trade.gravity_ols(g["tradeflow_baci"], X)
    oc = {c: i for i, c in enumerate(sorted(set(g["iso3_o"])))}
    dc = {c: i for i, c in enumerate(sorted(set(g["iso3_d"])))}
    P = trade.ppml_fe(g["tradeflow_baci"], X[:, 2:], np.array([oc[c] for c in g["iso3_o"]]),
                      np.array([dc[c] for c in g["iso3_d"]]))
    lab.row("gravity, 2019: OLS elasticities on GDPs and distance; R-squared",
            f"{R['beta'][0]:.2f}, {R['beta'][1]:.2f}, {R['beta'][2]:.2f}; {R['r2']:.2f} ({R['n']:,} pairs)")
    lab.row("PPML with exporter and importer effects: distance, border, language", ", ".join(f"{b:.2f}" for b in
                                                                                            P["beta"]))
    assert -1.6 < R["beta"][2] < -0.6 and -1.2 < P["beta"][0] < -0.4

    Mt = T["melitz"]
    kw = {k: Mt[k] for k in ("sigma", "k", "f", "fx", "fe", "tau", "delta")}
    M = trade.melitz(**kw)
    F = trade.melitz_firms(n=Mt["n"], seed=Mt["seed"] + seed, **kw)
    alive, ex = F["alive_trade"], F["exporter"] & F["alive_trade"]
    lab.row("Melitz: exporters among survivors (formula, simulation); exit on opening; the gain",
            f"{100 * M['export_share']:.1f}%, {100 * ex.sum() / alive.sum():.1f}%; {100 * M['exit_share']:.1f}%; "
            f"{100 * M['welfare_gain']:.2f}%")
    assert M["phi_export"] > M["phi_trade"] > M["phi_autarky"]

    E = T["ek"]
    a = trade.eaton_kortum_shares(E["T"], np.ones(3), E["d"], E["theta"])
    s = trade.eaton_kortum_simulate(E["T"], np.ones(3), E["d"], E["theta"], E["goods"], E["seed"] + seed)
    lab.row("Eaton and Kortum: largest gap between formula and simulation", f"{np.abs(a - s).max():.4f}")
    assert np.abs(a - s).max() < 0.02

    X3 = np.array([[80, 10, 10], [10, 85, 5], [10, 5, 80.]])
    aut = np.ones((3, 3)) * 1e3
    np.fill_diagonal(aut, 1)
    H = trade.hat_algebra(X3, aut, 4.0)
    acr = [-trade.acr_gains(X3[i, i] / X3[i].sum(), 4.0) for i in range(3)]
    lab.row("hat algebra to autarky against the ACR formula (three islands)",
            ", ".join(f"{100 * h:.2f}% / {100 * c:.2f}%" for h, c in zip(H["welfare"], acr)))
    assert np.allclose(H["welfare"], acr, atol=1e-4)

    S = trade.shift_share(**{**T["shock"], "seed": T["shock"]["seed"] + seed})
    lab.row("the China shock on the Island: planted effect; OLS; IV", f"{S['beta']:.2f}; {S['ols']:.3f}; "
            f"{S['iv']:.3f}")
    assert abs(S["iv"] - S["beta"]) < abs(S["ols"] - S["beta"])

    lab.note = ("Variety and scale make similar countries trade similar goods; distance and borders shape how much; "
                "only the best firms export, and opening moves output to them; Ricardo with a distribution gives "
                "gravity, and three models give one formula for the gains. A shift-share design needs an instrument "
                "because demand shocks raise imports and jobs together.")

    fig, ax = labs.figure(2, size=(11, 4.4))
    de = g["iso3_o"] == "DEU"
    ax[0].scatter(np.log(g["distw_harmonic"][de]), np.log(g["tradeflow_baci"][de] / g["gdp_d"][de]), s=8,
                  color=labs.ORANGE)
    ax[0].set(title="Germany's exports per dollar of partner GDP, 2019", xlabel="log distance", ylabel="log")
    tau = np.linspace(1, 2.5, 31)
    ax[1].plot(tau, [100 * trade.melitz(**{**kw, "tau": t})["welfare_gain"] for t in tau], color=labs.BLUE,
               label="gain from opening, %")
    ax[1].plot(tau, [100 * trade.melitz(**{**kw, "tau": t})["export_share"] for t in tau], color=labs.ORANGE,
               label="exporters, % of firms")
    ax[1].set(title="Melitz: gains and exporters against shipping costs", xlabel="tau")
    ax[1].legend()
    lab.fig = fig
    return lab
