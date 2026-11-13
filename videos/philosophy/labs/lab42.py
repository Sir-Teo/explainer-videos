"""Lab 42: optimize a proxy until it bends, solve the off-switch game, and check Löb's axiom on every small frame."""


import numpy as np

from videos.coursekit import labs
from explainer.philosophy.reasoner import alignment

TITLE = "Goodhart's bend, the value of an off switch, and Löb's frames"
GOAL = ("Pick the best of N candidates by a noisy proxy and compare the pick's true value under Gaussian and "
        "heavy-tailed error; explain one random behaviour by four planner-reward pairs; compare the off-switch "
        "game's closed form with simulation; and count the frames of up to four worlds on which Löb's axiom holds.")
TASKS = [
    "Call alignment.goodhart with df=3 and then df=1.2. How heavy must the error's tail be before the true value "
    "of the pick falls back as N grows?",
    "In the off-switch simulation let the human err: allow the action with probability 1/(1 + exp(-beta u)). At "
    "which beta does waiting stop beating acting when mu = 0.5 and sigma = 1?",
    "Add a fourth option behind the hub in alignment.POWER_MDP. What share of random reward functions now avoid "
    "shutdown, against 4/5?",
]


def run(seed=0):
    rng = np.random.default_rng(seed)
    lab = labs.Lab()

    ns = (1, 2, 4, 8, 16, 32, 64, 128, 256, 512, 1024)
    g = alignment.goodhart(ns=ns, trials=1500, seed=1975 + seed)
    light, heavy = g["light"], g["heavy"]
    lab.row("Gaussian error, best of 1,024: true value, proxy", f"{light['last']:.2f}, {light['proxy'][-1]:.2f}   (theory: true = proxy / 2)")
    lab.row("heavy tails: the pick's true value peaks at N =", f"{heavy['peak_n']} with {heavy['peak']:.2f}   (film: N = 8, 0.59)")
    lab.row("heavy tails, best of 1,024: true value, proxy", f"{heavy['last']:.2f}, {heavy['proxy'][-1]:.0f}")
    assert abs(light["last"] - light["proxy"][-1] / 2) < 0.12, "E[V | U] = U / 2 with equal variances"
    assert light["last"] > 2.0 and light["peak_n"] >= 256, "with light tails more pressure keeps helping"
    assert heavy["peak_n"] <= 64 and heavy["last"] < 0.45 * heavy["peak"], "with heavy tails the curve bends over"
    assert heavy["proxy"][-1] > 20 * max(heavy["last"], 0.05), "while the proxy keeps climbing"
    q = alignment.quantilize(n=1024, qs=(1 / 1024, 1 / 64, 1 / 4, 1.0), trials=600, seed=2016 + seed)
    by_q = {r["q"]: r["true"] for r in q["rows"]}
    lab.row("quantilizer: argmax, a random pick from the top quarter", f"{by_q[1 / 1024]:.2f}, {by_q[0.25]:.2f}   (film, 4,096 candidates: nothing, 0.65)")
    assert q["best_q"] == 0.25 and by_q[0.25] > by_q[1 / 1024] + 0.3 and by_q[0.25] > by_q[1.0] + 0.3

    policy = rng.dirichlet(np.ones(4) * 2)
    policy = policy / policy.sum()
    nfl = alignment.no_free_lunch(policy=tuple(policy))["pairs"]
    worst = max(p["error"] for p in nfl)
    bests = {p["planner"]: p["best"] for p in nfl}
    lab.row("one random behaviour, four planner-reward pairs", f"largest mismatch {worst:.0e}; favourite: "
            f"{bests['rational']} or {bests['anti-rational']} or none")
    assert worst < 1e-12 and bests["rational"] != bests["anti-rational"] and bests["indifferent"] is None

    mu, sigma = round(float(rng.uniform(-1, 1)), 2), round(float(rng.uniform(0.5, 2)), 2)
    u = rng.normal(mu, sigma, 400000)
    game = alignment.off_switch_values(mu, sigma)
    sim_wait = float(np.maximum(u, 0).mean())
    lab.row(f"off-switch game at mu = {mu}, sigma = {sigma}: waiting", f"{sim_wait:.3f} simulated, {game['wait']:.3f} closed form; "
            f"acting {game['act']:.2f}, off 0")
    assert abs(sim_wait - game["wait"]) < 0.01 and game["incentive"] > 0
    film = alignment.off_switch()
    rational, noisy = np.array(film["grids"]["rational"]), np.array(film["grids"]["beta=0.5"])
    lab.row("incentive to defer negative: rational human, noisy human", f"{(rational < 0).mean():.0%}, {(noisy < 0).mean():.0%} of the grid   (film: never, 62%)")
    assert abs(film["example"]["wait"] - 0.70) < 0.005 and rational.min() >= 0 and abs((noisy < 0).mean() - 0.62) < 0.01

    power = alignment.power_seeking(seed=2021 + seed)
    lab.row("random rewards that avoid shutdown, 3 options", f"{power['to_hub']:.1%}   (limit k/(k+1) = 75%)")
    assert abs(power["to_hub"] - 0.75) < 0.03 and power["power"]["hub"] > power["power"]["off"] + 0.15
    assert all(abs(power["fraction_by_k"][k] - power["limit"][k]) < 0.035 for k in power["limit"])

    frames = alignment.lob_frames(4)["rows"]
    lab.row("frames with 1 to 4 worlds validating Löb's axiom", ", ".join(str(r["lob_valid"]) for r in frames) + "   (film: 1, 3, 19, 219)")
    assert [r["lob_valid"] for r in frames] == [1, 3, 19, 219]
    assert all(r["agree"] == r["frames"] for r in frames), "exactly the transitive irreflexive frames"
    combat = alignment.modal_combat()["table"]
    assert combat["FairBot|FairBot"] == "C" and combat["PrudentBot|CooperateBot"] == "D" and combat["FairBot|DefectBot"] == "D"
    lab.note = ("A proxy is safe to optimize only while its errors are light-tailed; behaviour does not fix "
                "values; and a machine has a reason to keep its off switch only while it is unsure what we want "
                "and trusts our judgment of it.")

    fig, ax = labs.figure(2, size=(11.5, 4.3))
    ax[0].plot(ns, light["true"], "o-", color=labs.GREEN, ms=4, label="Gaussian error")
    ax[0].plot(ns, heavy["true"], "o-", color=labs.RED, ms=4, label="heavy-tailed error (t, 1.5 df)")
    ax[0].set(title="True value of the candidate with the best proxy", xlabel="candidates searched, N", xscale="log",
              ylabel="mean true value of the pick")
    ax[0].legend(loc="upper left")
    sig = np.linspace(0, 3, 61)
    for beta, color, name in ((None, labs.GREEN, "rational human"), (2.0, labs.GOLD, "noisy human, beta = 2"),
                              (0.5, labs.RED, "noisy human, beta = 0.5")):
        ax[1].plot(sig, [alignment.off_switch_values(0.5, float(s), beta)["incentive"] for s in sig], color=color, label=name)
    ax[1].axhline(0, color=labs.MUTED, lw=1, ls="--")
    ax[1].set(title="Incentive to leave the off switch alone (robot expects 0.5)", xlabel="the robot's uncertainty, sigma",
              ylabel="value of waiting minus the best alternative")
    ax[1].legend(loc="upper left")
    lab.fig = fig
    return lab
