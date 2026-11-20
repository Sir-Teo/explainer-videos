"""Lab 37: cities and regions: Schelling's checkerboard and its tolerance curve, von Thünen's rings, the monocentric
city with the car and the lift, agglomeration and sorting with movers, Zipf's law on the Census Bureau's metropolitan
areas and Gibrat's growth with a floor, Krugman's core and periphery with its break and sustain points, a Rosen-Roback
system of towns read for quality of life, and a line city divided by a wall."""

import numpy as np

from videos.coursekit import labs
from explainer.economics import data
from explainer.economics.agora import city
from explainer.economics.island import truths

TITLE = "Cities and regions"
GOAL = ("Play Schelling's board; draw von Thünen's rings; solve a monocentric city and see what the car and the lift "
        "do; separate agglomeration from sorting with movers; fit Zipf's law to America's metropolitan areas and grow "
        "it from Gibrat's law; find the break point of the core and periphery; read amenities from wages and rents; "
        "and divide a city with a wall.")
TASKS = [
    "Schelling: make one kind of coin a fifth of the board instead of half. Does the minority end more or less "
    "segregated?",
    "The monocentric city: double the population instead of changing transport. What happens to the edge, the "
    "central rent and the height of buildings?",
    "Rosen-Roback: give Lagoon an inelastic housing supply (0.3). How does the same amenity gain split between rents "
    "and population?",
]


def run(seed=0):
    lab = labs.Lab()
    T = truths(37)

    S = T["schelling"]
    r = city.schelling(S["n"], S["empty"], S["threshold"], S["seed"] + seed, keep_frames=False)
    lab.row("Schelling: like neighbours at the start and the end; rounds; moves",
            f"{100 * r['like'][0]:.0f}% to {100 * r['final_like']:.0f}%; {r['rounds']} rounds; {r['moves']} moves")
    assert r["final_like"] > r["like"][0] + 0.15
    sw = city.schelling_sweep([0.2, 0.4, 0.6], seeds=(0, 1), n=24)
    lab.row("tolerance curve: final like-share wanting 20%, 40%, 60% alike",
            ", ".join(f"{100 * v:.0f}%" for v in sw["like"]))

    x = np.linspace(0, 110, 1101)
    th = city.thunen(list(T["thunen"]), x)
    lab.row("von Thünen's rings", "; ".join(f"{n} {a:.0f}-{b:.0f} km" for n, a, b in th["rings"]))

    M = T["mono"]
    kw = {k: M[k] for k in ("N", "y", "t", "alpha", "theta", "i")}
    base, car = city.monocentric(**kw), city.monocentric(**{**kw, "t": M["t"] * M["car"]})
    lift = city.monocentric(**{**kw, "i": M["i"] * M["lift"]})
    lab.row("monocentric city: edge (km) and central density, base / car / lift",
            f"{base['edge']:.0f} / {car['edge']:.0f} / {lift['edge']:.0f} km; {base['centre_density']:,.0f} / "
            f"{car['centre_density']:,.0f} / {lift['centre_density']:,.0f} households a km2")
    p, h = np.array(base["p"]), np.array(base["h"])
    xs = np.array(base["x"])
    k = 50
    slope = (p[k + 1] - p[k - 1]) / (xs[k + 1] - xs[k - 1])
    lab.row("Muth's condition at 2.5 km: p'(x) h(x) against -t", f"{slope * h[k]:.4f} vs {-M['t']:.4f}")
    assert abs(slope * h[k] + M["t"]) < 1e-2 * M["t"]

    A = T["agglo"]
    ag = city.agglomeration_panel(gamma=A["gamma"], sort=A["sort"], seed=A["seed"] + seed)
    lab.row("agglomeration: across towns, from movers, planted", f"{ag['naive']:.3f}, {ag['movers']:.3f}, "
                                                                 f"{ag['gamma']:.2f}")
    assert ag["naive"] > ag["movers"]

    m = data.cbsa()
    z100, zall = city.zipf_fit(m["pop2024"], top=100), city.zipf_fit(m["pop2024"])
    G = T["gibrat"]
    g = city.gibrat(5000, 2000, G["sigma"], G["floor"], G["seed"] + seed)
    lab.row("Zipf: America's top 100 and all metros; Gibrat's towns (theory)",
            f"{z100['zeta']:.2f} (se {z100['se']:.2f}), {zall['zeta']:.2f}; {g['zeta']:.2f} ({g['theory']:.2f})")

    P = T["cp"]
    b = city.cp_break(P["mu"], P["sigma"])
    gap = city.cp_gap(b, [0.49, 0.51], P["mu"], P["sigma"])
    lab.row("core and periphery: break and sustain points; slope of the gap at the break",
            f"{b:.3f}, {city.cp_sustain(P['mu'], P['sigma']):.3f}; {(gap[1] - gap[0]) / 0.02:.1e}")
    assert abs(gap[1] - gap[0]) < 1e-4

    t = T["towns"]
    R = city.roback(t["a"], t["q"], t["eta"], b=t["b"], alpha=t["alpha"])
    q = np.array(t["q"]) - np.mean(t["q"])
    lab.row("six towns: amenities read from prices against the planted ones (largest error)",
            f"{np.max(np.abs(np.array(R['qol']) - q)):.1e}")
    assert np.allclose(R["qol"], q, atol=1e-9)

    W = city.wall_experiment(**T["berlin"])
    lab.row("the line city divided: price change near the Wall and near the western centre (relative)",
            f"{100 * W['division'][-1]:+.0f}%, {100 * max(W['division']):+.0f}%")

    lab.note = ("Mild preferences sort a board; land goes to the highest bidder, so rents fall with distance; density "
                "raises productivity by less than the raw premium, because talent sorts; random proportional growth "
                "gives Zipf's law; falling transport costs can tip a country into a core and a periphery; and in "
                "spatial equilibrium prices, not welfare, differ across places.")

    fig, ax = labs.figure(2, size=(11, 4.4))
    for name, mm, col in (("base", base, labs.BLUE), ("car", car, labs.ORANGE), ("lift", lift, labs.GREEN)):
        ax[0].plot(mm["x"], np.array(mm["D"]) / 1000, color=col, label=name)
    ax[0].set(title="households per km2 (thousands)", xlabel="km from the centre", xlim=(0, 40))
    ax[0].legend()
    lams = np.linspace(0, 1, 41)
    for T_, col in ((2.1, labs.BLUE), (1.7, labs.ORANGE), (1.5, labs.GREEN)):
        ax[1].plot(lams, city.cp_gap(T_, lams, P["mu"], P["sigma"]), color=col, label=f"T = {T_}")
    ax[1].axhline(0, color="grey", lw=0.8)
    ax[1].set(title="core and periphery: the real-wage gap", xlabel="north's share of manufacturing")
    ax[1].legend()
    lab.fig = fig
    return lab
