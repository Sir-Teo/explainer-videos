"""Lab 10: read Spinoza's Ethics I as a graph of proofs, and find the path of least time."""

import math

import numpy as np

from videos.coursekit import labs
from explainer.philosophy.reasoner import modern

TITLE = "Spinoza's proof graph and Leibniz's least time"
GOAL = ("Build the citation graph of Ethics Part I, check that it has no circles and measure its longest chain; then "
        "send light between two random points across a surface and check that the least-time crossing obeys "
        "Snell's law.")
TASKS = [
    "Call modern.ethics_graph(latin=True). Which axiom stops being idle, and does the longest chain change?",
    "Print sorted(modern.ancestors(g, 'P14')) and compare with Problem 1: fourteen items.",
    "Set v2 = v1 in least_time. Where does the light cross, and what does Snell's law reduce to?",
]


def run(seed=0):
    rng = np.random.default_rng(seed)
    lab = labs.Lab()
    g = modern.ethics_graph()
    depth, chain, idle = modern.depth(g), modern.longest_chain(g), modern.unused(g)
    lab.row("Ethics I", f"{len(g['nodes'])} items, {len(g['edges'])} citations; every proof cites only earlier items: "
                        f"{modern.forward_only(g)}")
    lab.row("longest chain", f"{len(chain) - 1} steps: {' → '.join(chain)}")
    lab.row("never cited (Elwes's English)", f"{', '.join(idle)}   (Latin text: {', '.join(modern.unused(modern.ethics_graph(latin=True)))})")
    lab.row("what P11 (God exists) rests on", f"{len(modern.ancestors(g, 'P11'))} items: {', '.join(sorted(modern.ancestors(g, 'P11')))}")
    assert len(g["nodes"]) == 51 and len(g["edges"]) == 102 and modern.forward_only(g)
    assert len(chain) - 1 == 10 == max(depth.values()) and chain[0] == "D3" and chain[-1] == "P32"
    assert all((a, b) in set(g["edges"]) for a, b in zip(chain, chain[1:])), "the chain follows real citations"
    assert idle == ["A2", "A7"] and modern.unused(modern.ethics_graph(latin=True)) == ["A2"]
    assert len(modern.ancestors(g, "P11")) == 9 and len(modern.ancestors(g, "P14")) == 14

    # a circular citation must be caught: let a random item cite one of its own descendants
    props = [v for v in g["nodes"] if v.startswith("P") and any(a.startswith("P") for a in modern.ancestors(g, v))]
    later = props[int(rng.integers(len(props)))]
    earlier = sorted(a for a in modern.ancestors(g, later) if a.startswith("P"))[0]
    broken = {"nodes": g["nodes"], "edges": g["edges"] + [(later, earlier)]}
    try:
        modern.depth(broken)
        caught = False
    except ValueError:
        caught = True
    assert caught and not modern.forward_only(broken)
    lab.row(f"if {earlier} also cited {later}", "the Reasoner reports a circle")

    # least time between two random points, against a fine grid and Snell's law
    a = (0.0, float(rng.uniform(0.5, 2.0)))
    b = (float(rng.uniform(1.5, 3.0)), -float(rng.uniform(0.5, 2.0)))
    v1, v2 = 1.0, float(rng.uniform(0.5, 0.9))
    r = modern.least_time(a, b, v1, v2)
    xs = np.linspace(a[0], b[0], 20001)
    times = np.hypot(xs - a[0], a[1]) / v1 + np.hypot(b[0] - xs, b[1]) / v2
    assert abs(xs[times.argmin()] - r["x"]) < 3e-4 and r["time"] <= times.min() + 1e-12
    assert abs(r["sin_i_over_v1"] - r["sin_r_over_v2"]) < 1e-6 and r["time"] < r["straight_time"]
    lab.row("least-time crossing", f"x = {r['x']:.4f}   (grid search {xs[times.argmin()]:.4f}); time {r['time']:.4f} "
                                   f"against {r['straight_time']:.4f} on the straight line")
    lab.row("Snell's law there", f"sin i / v1 = {r['sin_i_over_v1']:.6f},   sin r / v2 = {r['sin_r_over_v2']:.6f}")

    rules = modern.rival_rules([1] * 8)
    assert all(x["fits"] for x in rules) and {x["tomorrow"] for x in rules} == {0, 1}
    excess = modern.spherical_excess(*modern.GAUSS_TRIANGLE.values())["excess_arcsec"]
    bend = modern.light_bending()
    assert abs(excess - 14.9) < 0.05 and abs(bend["einstein"] - 1.75) < 0.005 and math.isclose(bend["einstein"], 2 * bend["newton"])
    lab.row("four rules fit eight sunrises", "forecasts for day nine: " + ", ".join(str(x["tomorrow"]) for x in rules))
    lab.row("Gauss's triangle; starlight at the sun", f"excess {excess:.1f}″;  deflection {bend['einstein']:.2f}″ (Newtonian {bend['newton']:.2f}″)")
    lab.note = ("Spinoza's book really is ordered like Euclid's: no proof cites anything later, and the proof of "
                "God's existence rests on nine items. Light's quickest path is not the straight one, and at the "
                "quickest crossing the two sines stand in the ratio of the speeds.")

    fig, ax = labs.figure(2, size=(11, 4.6))
    cols = {}
    for v in g["nodes"]:
        cols.setdefault(depth[v], []).append(v)
    pos = {v: (d, (i + 0.5) / len(vs)) for d, vs in cols.items() for i, v in enumerate(vs)}
    on_chain = set(zip(chain, chain[1:]))
    for e in g["edges"]:
        (x0, y0), (x1, y1) = pos[e[0]], pos[e[1]]
        ax[0].plot([x0, x1], [y0, y1], color=labs.GOLD if e in on_chain else labs.GRID, lw=2 if e in on_chain else 0.7,
                   zorder=3 if e in on_chain else 1)
    for kind, color, name in (("D", labs.BLUE, "definitions"), ("A", labs.GREEN, "axioms"), ("P", labs.INK, "propositions")):
        vs = [v for v in g["nodes"] if v[0] == kind]
        ax[0].scatter([pos[v][0] for v in vs], [pos[v][1] for v in vs], s=22, color=color, zorder=4, label=name)
    for v in chain:
        ax[0].annotate(v, pos[v], xytext=(0, 6), textcoords="offset points", ha="center", fontsize=7.5, color=labs.GOLD)
    ax[0].plot([], [], color=labs.GOLD, lw=2, label="the longest chain")
    ax[0].set(title="Ethics I: each item one column right of the deepest it cites", xlabel="depth (longest chain of citations)",
              yticks=[], xticks=range(11), ylim=(-0.12, 1.05))
    ax[0].grid(False)
    ax[0].legend(loc="lower center", ncols=4, fontsize=8)
    ax[1].plot(xs, times, color=labs.BLUE, label="travel time by crossing point")
    ax[1].scatter([r["x"]], [r["time"]], color=labs.GOLD, zorder=3, label="least time: Snell's law holds")
    straight = a[0] + (b[0] - a[0]) * a[1] / (a[1] - b[1])
    ax[1].scatter([straight], [r["straight_time"]], color=labs.RED, zorder=3, label="the straight line")
    ax[1].set(title=f"Light from ({a[0]:.0f}, {a[1]:.2f}) to ({b[0]:.2f}, {b[1]:.2f}); speeds 1 and {v2:.2f}",
              xlabel="where the path crosses the surface, x", ylabel="travel time")
    ax[1].legend()
    lab.fig = fig
    return lab
