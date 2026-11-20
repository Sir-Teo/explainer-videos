"""Lab 35: comparative advantage: Ricardo's world and the Island's, the chain and the Dornbusch-Fischer-Samuelson
continuum, Bernhofen and Brown's test on Japan, the Heckscher-Ohlin world with Stolper-Samuelson and Rybczynski,
Trefler's factor-content statistics from his data, specific factors, tariffs and the optimal tariff, protection for
sale, a tariff war, and the gains-from-trade formula of Arkolakis, Costinot and Rodriguez-Clare."""

import numpy as np

from videos.coursekit import labs
from explainer.economics import data
from explainer.economics.agora import trade
from explainer.economics.data import tables
from explainer.economics.island import truths

TITLE = "Comparative advantage: who trades what, and who gains"
GOAL = ("Solve Ricardo's model and find the world price and the wage band; move the continuum with growth and "
        "shipping costs; run Bernhofen and Brown's test; solve the Heckscher-Ohlin world and its theorems; recompute "
        "Trefler's missing trade; follow a price change through specific factors; price a tariff, a quota and the "
        "optimal tariff; and play the tariff war.")
TASKS = [
    "Ricardo: give Portugal twice England's workers instead of 0.8 times. What is the world price, and who gains?",
    "Continuum: make shipping lose a third of every cargo (g = 0.67). What share of goods is no longer traded?",
    "Trefler: drop the two land factors (cropland and pasture). Does the sign test improve?",
]


def run(seed=0):
    lab = labs.Lab()
    T = truths(35)

    P = T["playit"]
    R = trade.ricardo_trade(P["island"], P["arch"], P["L_island"], P["L_arch"], P["beta"])
    lab.row("the Island and the Archipelago: world price (fish per bolt); gains", f"{R['p']:.2f}; "
            f"{100 * R['H']['gain']:.1f}%, {100 * R['F']['gain']:.1f}%")
    assert R["pH"] < R["p"] < R["pF"] and R["H"]["gain"] > 0 and R["F"]["gain"] > 0

    Ri = tables.RICARDO_1817.data
    aE, aP = (Ri["England"]["cloth"], Ri["England"]["wine"]), (Ri["Portugal"]["cloth"], Ri["Portugal"]["wine"])
    RR = trade.ricardo_trade(aE, aP, T["ricardo"]["L_england"], T["ricardo"]["L_portugal"])
    wp = RR["wage_ratio"]                 # Portugal's wage over England's (Portugal exports wine, good 2)
    lab.row("Ricardo: price of wine in cloth; Portugal's wage over England's (band 1.11 to 1.50)",
            f"{RR['p']:.3f}; {wp:.3f}")
    assert 100 / 90 <= wp <= 120 / 80

    D = T["dfs"]
    z = (np.arange(D["n"]) + 0.5) / D["n"]
    A = D["level"] * np.exp(D["k"] * (1 - 2 * z))
    f0, f1 = trade.dfs(A, L=D["L"], Lf=D["Lf"]), trade.dfs(A, L=D["L"], Lf=D["Lf"] * D["growth"])
    fs = trade.dfs(A, L=D["L"], Lf=D["Lf"], g=D["g"])
    lab.row("continuum: relative wage and share of goods; after the Archipelago grows; non-traded with shipping",
            f"{f0['omega']:.3f}, {f0['share_home']:.3f}; {f1['omega']:.3f}, {f1['share_home']:.3f}; "
            f"{fs['nontraded'].mean():.3f}")
    assert f1["omega"] > f0["omega"] and f1["share_home"] < f0["share_home"]

    B = tables.BERNHOFEN_BROWN_2004.data
    lab.row("Japan: the inner product at 1851-53 prices, 1868-75 (millions of ryo)",
            ", ".join(f"{v:.2f}" for v in B["total"]))
    assert all(v < 0 for v in B["total"])

    H = T["ho"]
    W = trade.ho_world(H["alphas"], {"island": H["island"], "arch": H["arch"]}, H["beta"])
    ss = trade.stolper_samuelson(H["alphas"], (1.0, W["p"]), 0.10, 0)
    ry = trade.rybczynski(H["alphas"], (1.0, W["p"]), *H["arch"], 0.10)
    lab.row("Heckscher-Ohlin: world price of machines; the Island's net exports of cloth and machines",
            f"{W['p']:.3f}; {W['island']['X'][0]:.1f}, {W['island']['X'][1]:.1f}")
    lab.row("Stolper-Samuelson (cloth +10%): wage, rent; Rybczynski (capital +10%): cloth, machines",
            f"{100 * ss['dw']:+.1f}%, {100 * ss['dr']:+.1f}%; {100 * ry['dQ'][0]:+.1f}%, {100 * ry['dQ'][1]:+.1f}%")
    assert W["island"]["X"][0] > 0 > W["island"]["X"][1] and ss["dw"] > 0.10 > 0 > ss["dr"]

    F = trade.factor_content(data.trefler())
    Lt = trade.leontief_ratio(tables.LEONTIEF_1953.data["exports"], tables.LEONTIEF_1953.data["imports"])
    lab.row("Leontief's ratio of capital per worker, imports to exports", f"{Lt['ratio']:.3f}")
    lab.row("Trefler's data: sign test; variance ratio; rank correlation",
            f"{F['sign_test']:.3f}; {F['variance_ratio']:.4f}; {F['rank']:.3f}")
    assert 0.45 < F["sign_test"] < 0.55 and F["variance_ratio"] < 0.05

    S = T["specific"]
    c = trade.specific_change(S["pM"], S["pA"], S["dpA"], L=S["L"], K=S["K"], T=S["T"], theta=S["theta"])
    lab.row("specific factors (food +10%): wage, capital, land", f"{100 * c['dw']:+.1f}%, {100 * c['drK']:+.1f}%, "
            f"{100 * c['drT']:+.1f}%")
    assert 0 < c["dw"] < S["dpA"] < c["drT"] and c["drK"] < 0

    t = T["tariff"]
    sm = trade.tariff_small(t["a"], t["b"], t["c"], t["d"], t["pw"], t["t"])
    op = trade.optimal_tariff(t["a"], t["b"], t["c"], t["d"], t["e"], t["f"])
    lab.row("a small tariff: consumers, producers, revenue, deadweight", f"{-sm['cs_loss']:.0f}, +{sm['ps_gain']:.0f}, "
            f"+{sm['revenue']:.0f}, {-(sm['dwl_production'] + sm['dwl_consumption']):.0f}")
    lab.row("the large country's optimal tariff: specific; ad valorem; 1/elasticity", f"{op['t']:.3f}; "
            f"{op['ad_valorem']:.3f}; {op['inverse_elasticity']:.3f}")
    assert abs(op["ad_valorem"] - op["inverse_elasticity"]) < 1e-3

    G = T["gh"]
    rng = np.random.default_rng(G["seed"] + seed)
    zz, ee = rng.uniform(0.5, 6.0, G["n"]), rng.uniform(1.0, 3.0, G["n"])
    tt = trade.protection_for_sale(zz, ee, G["organized"], G["a"], G["alpha_L"])
    lab.row("protection for sale (a = 50): highest organized tariff; lowest unorganized",
            f"{100 * tt[np.array(G['organized']) == 1].max():.1f}%, "
            f"{100 * tt[np.array(G['organized']) == 0].min():.2f}%")

    Wr = trade.tariff_war(**T["war"])
    pay = Wr["payoffs"]
    lab.row("the tariff war: Nash tariff; payoffs (free, tariff) and (tariff, tariff) against free trade",
            f"{Wr['nash']:.3f}; {pay[('free', 'tariff')][0]:+.3f}, {pay[('tariff', 'tariff')][0]:+.3f}")
    assert pay[("tariff", "free")][0] > 0 > pay[("tariff", "tariff")][0]

    A_ = tables.ACR_2012.data
    lab.row("gains from trade (ACR, lambda 0.93): eps 5 and 10", f"{100 * trade.acr_gains(A_['lambda'], 5):.2f}%, "
            f"{100 * trade.acr_gains(A_['lambda'], 10):.2f}%")

    lab.note = ("Relative, not absolute, costs decide who sells what, and both sides gain; endowments decide trade "
                "too, and inside each country the scarce or stuck factor loses. The tests pass where they can be run "
                "(Japan) and the factor-content prediction needs technology differences to fit. A small country's "
                "tariff costs it two triangles; a large one gains at its neighbour's expense, which is why agreements "
                "exist.")

    fig, ax = labs.figure(2, size=(11, 4.4))
    ax[0].plot(z, A, color=labs.BLUE, label="A(z): the Island's edge")
    ax[0].plot(z, trade.dfs_demand(z, D["L"], D["Lf"]), color=labs.ORANGE, label="B(z)")
    ax[0].plot(z, trade.dfs_demand(z, D["L"], D["Lf"] * D["growth"]), color=labs.ORANGE, ls="--",
               label="B(z), the Archipelago grown")
    ax[0].set(ylim=(0, 2), title="The continuum of goods", xlabel="goods, z", ylabel="relative wage")
    ax[0].legend()
    ax[1].scatter(F["predicted"], F["measured"], s=6, color=labs.BLUE)
    ax[1].plot([-8, 8], [-8, 8], color="grey", ls="--")
    ax[1].set(xlim=(-8, 8), ylim=(-8, 8), title="Trefler's missing trade", xlabel="predicted factor content",
              ylabel="measured")
    lab.fig = fig
    return lab
