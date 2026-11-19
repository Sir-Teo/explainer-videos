"""Lab 12: competition among the few: Cournot and Bertrand, capacity, differentiation, location, variety,
commitment, collusion, price wars, concentration and mergers."""

import numpy as np

from videos.coursekit import labs
from explainer.economics.agora import oligopoly as ol
from explainer.economics.island import truths

TITLE = "Competition among the few: quantities, prices, commitment and collusion"
GOAL = ("Solve Cournot with one to twenty firms and check Cowling and Waterson's L = H/epsilon; solve Bertrand with "
        "equal and unequal costs, differentiated prices and Kreps and Scheinkman's capacities; compute Salop's free "
        "entry against the planner and Dixit and Stiglitz's markup; find Stackelberg's leader and Dixit's deterring "
        "capacity; compute the discount factor a cartel needs with N firms; simulate Green and Porter's price wars; "
        "and work out the merger paradox and the savings that keep a merger's price from rising.")
TASKS = [
    "Cournot with costs 8, 10, 12 and 14: which firm has the largest Lerner index, and does the identity "
    "sum s_i L_i = H/epsilon still hold? Now give the cheapest firm a cost of 2. Does anyone drop out?",
    "Dixit's game: lower the entrant's setup cost from 144 to 100 and then to 80. Where does strategic deterrence "
    "stop being possible, and what does the incumbent do instead?",
    "Green and Porter: raise the trigger from 3.5 to 4.0 and shorten the wars from six seasons to three. How does "
    "the share of time at war change, and what happens to the average price?",
]


def run(seed=0):
    lab = labs.Lab()
    T = truths(12)
    bt = T["boats"]
    a, b, c = bt["a"], bt["b"], bt["c"]

    # Cournot
    ns = np.arange(1, bt["n_max"] + 1)
    P = np.array([ol.cournot(a, b, [c] * n)["P"] for n in ns])
    assert np.allclose(P, (a + ns * c) / (ns + 1))
    lab.row("Cournot price with 1, 2, 3 and 20 yards", ", ".join(f"{P[k]:.2f}" for k in (0, 1, 2, -1)))
    asym = ol.cournot(a, b, [8.0, 10.0, 12.0, 14.0])
    assert abs(asym["lerner"] - asym["lerner_hhi"]) < 1e-9
    lab.row("four unequal yards: HHI, share-weighted Lerner index, H/epsilon",
            f"{10000 * asym['hhi']:.0f}, {asym['lerner']:.4f}, {asym['lerner_hhi']:.4f}")

    # prices
    eq, uneq = ol.bertrand(a, b, [c, c]), ol.bertrand(a, b, [c, 20.0])
    lab.row("Bertrand: equal costs, then costs 10 and 20 (price, profit)",
            f"{eq['P']:.2f}, {eq['profit']:.2f}; {uneq['P']:.2f}, {uneq['profit']:.2f}")
    d = T["diff"]
    db = ol.bertrand_differentiated(d["alpha"], d["beta"], d["gamma"], d["c"])
    ks = ol.kreps_scheinkman(a, b, c)
    assert ks["deviation_gain"] <= 1e-9
    lab.row("differentiated price; Kreps-Scheinkman capacity and price", f"{db['p']:.2f}; {ks['k']:.0f}, {ks['P']:.0f}")

    # space and variety
    be = T["beach"]
    sl = ol.salop(be["t"], be["F"], be["c"])
    v = T["variety"]
    dsx = ol.dixit_stiglitz(v["sigma"], v["f"], v["c"], v["L"])
    lab.row("Salop: free entry against the planner; Dixit-Stiglitz markup and varieties",
            f"{sl['n_free']:.0f} vs {sl['n_opt']:.0f}; {dsx['markup']:.3f}, {dsx['n']:.0f}")

    # commitment
    st = ol.stackelberg(a, b, c)
    de = T["deter"]
    dx = ol.dixit_entry(de["a"], de["b"], de["c"], de["r"], de["F"])
    assert dx["regime"] == "deter"
    lab.row("Stackelberg: leader and follower", f"{st['qL']:.1f}, {st['qF']:.1f} (profits {st['piL']:.2f}, "
            f"{st['piF']:.2f})")
    lab.row("Dixit: credible range, deterring capacity, deter vs accommodate",
            f"[{dx['S']:.0f}, {dx['T']:.0f}], {dx['deter_k']:.0f}, {dx['pi_deter']:.0f} vs {dx['pi_accommodate']:.0f}")

    # collusion
    nn = list(T["collusion"]["ns"])
    dc = [ol.collusion_threshold(n, "cournot")["delta"] for n in nn]
    dbt = [ol.collusion_threshold(n, "bertrand")["delta"] for n in nn]
    assert abs(dc[0] - 9 / 17) < 1e-12 and abs(dbt[0] - 0.5) < 1e-12
    lab.row("delta a cartel needs, 2 and 10 firms: quantities; prices", f"{dc[0]:.3f}, {dc[-1]:.3f}; {dbt[0]:.3f}, "
            f"{dbt[-1]:.3f}")
    gp = ol.green_porter(periods=T["collusion"]["periods"], seed=T["collusion"]["seed"] + seed)
    lab.row("Green and Porter: share of seasons at war (nobody cheats)", f"{gp['share_war']:.3f}")
    le = T["leniency"]
    lab.row("leniency: is confessing dominant with half, then full, forgiveness?",
            f"{ol.leniency_race(le['fine'], le['caught'], leniency=0.5)['dominant']}, "
            f"{ol.leniency_race(le['fine'], le['caught'], leniency=1.0)['dominant']}")

    # mergers
    m = ol.merger_cournot(T["merger"]["n"], a, b, c)
    lab.row("merger of two of three: the pair's gain; saving needed; price at zero cost",
            f"{m['merger_gain']:.2f}; {m['saving_needed']:.2f}; {m['price_if_free']:.2f}")
    w = ol.williamson(T["merger"]["eps"], T["merger"]["dp"], 0.0)
    lab.row("Williamson: cost cut (share of sales) that offsets a 10% price rise", f"{w['breakeven_dc']:.3f}")
    lab.note = ("Cournot's price falls from the monopoly's toward cost as firms are added, and the share-weighted "
                "Lerner index equals H/epsilon exactly; Bertrand reaches cost with two firms, and capacity chosen "
                "first gives Cournot's outcome; free entry brings twice the planner's number of sellers; a credible "
                "capacity of 36 keeps the entrant out; cartels need more patience as they grow; price wars happen "
                "with nobody cheating; and a merger of two of three Cournot firms loses money without savings, and "
                "raises the price unless it saves more than its whole cost.")

    fig, ax = labs.figure(2, size=(11, 4.4))
    ax[0].plot(ns, P, "o-", color=labs.BLUE, ms=4)
    ax[0].axhline(c, color="grey", ls="--")
    ax[0].set(title="Cournot: price with N yards", xlabel="yards", ylabel="price")
    ax[1].plot(dx["ks"], dx["entrant_profit"], color=labs.ORANGE, lw=2)
    ax[1].axhline(0, color="grey", ls="--")
    ax[1].axvspan(dx["S"], dx["T"], color="grey", alpha=0.15)
    ax[1].set(title="Dixit: the entrant's profit against the incumbent's capacity", xlabel="capacity",
              ylabel="entrant's profit")
    lab.fig = fig
    return lab
