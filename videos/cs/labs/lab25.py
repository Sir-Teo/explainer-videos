"""Lab 25: search Post's dominoes with a budget, turn a Turing machine into dominoes, and run PRIMEGAME."""

from videos.coursekit import labs

import numpy as np

from explainer.cs.algo import computability as C

TITLE = "Dominoes that compute: bounded search, a reduction, and PRIMEGAME"
GOAL = ("Find the shortest match of the film's four-domino set (206 dominoes) by breadth-first search over overhangs, "
        "check that a match of the dominoes built from a Turing machine spells its accepting history, and check that "
        "Conway's PRIMEGAME reaches the powers 2^p for exactly the primes p, in order.")
TASKS = [
    "Lower max_len for the 206 instance to 150. Which status comes back, and why is it not a proof that no match exists?",
    "Change the machine's input from '10' to '11'. It rejects: what does pcp_search(D, 60, first=0) report now, and what does that say about no-match instances?",
    "Raise STEPS to 400,000 and predict the next primes before you run it. Then fit the step at which 2^p appears against p on log-log axes.",
]
FOUR = [("1000", "0"), ("01", "0"), ("1", "101"), ("00", "001")]            # chapter 5: shortest match 206
SIPSER = [("b", "ca"), ("a", "ab"), ("ca", "a"), ("abc", "c")]              # chapter 5: 2, 1, 3, 2, 4
RULES = {("q", "1"): ("p", "1", "R"), ("p", "0"): ("a", "0", "R"), ("q", "0"): ("r", "0", "R"),
         ("p", "1"): ("r", "1", "R"), ("q", "_"): ("r", "_", "R"), ("p", "_"): ("r", "_", "R")}
STEPS = 60_000


def rows(dominoes, match):
    return "".join(dominoes[i][0] for i in match), "".join(dominoes[i][1] for i in match)


def primes_below(n):
    return [p for p in range(2, n) if all(p % d for d in range(2, int(p ** 0.5) + 1))]


def run(seed=0):
    rng = np.random.default_rng(seed)
    lab = labs.Lab()

    # 1. Sipser's four dominoes, and random small sets: every reported match is checked on the full strings
    s = C.pcp_search(SIPSER, 10)
    assert [i + 1 for i in s["match"]] == [2, 1, 3, 2, 4]
    words = ["0", "1", "00", "01", "10", "11", "001", "010", "011", "100", "101", "110"]
    tally = {"matched": 0, "exhausted": 0, "depth-limit": 0, "node-limit": 0}
    for _ in range(300):
        inst = [(words[rng.integers(12)], words[rng.integers(12)]) for _ in range(3)]
        r = C.pcp_search(inst, 40, max_nodes=5000)
        tally[r["status"]] += 1
        if r["match"]:
            top, bottom = rows(inst, r["match"])
            assert top == bottom and len(r["match"]) <= 40
    lab.row("Sipser's set, shortest match", " ".join(str(i + 1) for i in s["match"]) + "   (the film: 2 1 3 2 4)")
    lab.row("300 random three-domino sets", "   ".join(f"{k} {v}" for k, v in tally.items()))
    assert tally["matched"] > 20 and tally["exhausted"] > 20, "both kinds of finite certificate occur"

    # 2. the four-domino set: nothing shorter than 206, by exhausting every shorter overhang
    f = C.pcp_search(FOUR, 300)
    top, bottom = rows(FOUR, f["match"])
    lab.row("four-domino set, shortest match", f"{len(f['match'])} dominoes, {len(top)} symbols   (the film: 206)")
    lab.row("overhang states dequeued", f"{f['nodes']:,}   (the film: 73,135)")
    assert top == bottom and len(f["match"]) == 206 and f["nodes"] == 73_135
    assert C.pcp_search(FOUR, 205)["status"] == "depth-limit", "a budget of 205 gives no verdict"
    over, t, b = [], 0, 0
    for i in f["match"]:
        t, b = t + len(FOUR[i][0]), b + len(FOUR[i][1])
        over.append(t - b)

    # 3. a machine becomes dominoes: the forced-first match is the accepting computation history
    D = C.tm_to_mpcp(RULES, "q", "a", "10", "01")
    m = C.pcp_search(D, 60, first=0)
    trace = C.run_tm_trace(RULES, "q", "a", "10")
    top, bottom = rows(D, m["match"])
    lab.row("machine on '10'", f"{trace['status']} in {trace['steps']} steps, history {trace['history']}")
    lab.row("its MPCP match", f"{len(D)} dominoes in the set, {len(m['match'])} used, spelling {top}")
    assert trace["status"] == "accepted" and top == bottom and top.startswith(trace["history"])

    # 4. PRIMEGAME: the exponents of the powers of two it reaches are the primes, in order
    out = C.fractran_run(C.PRIMEGAME, 2, STEPS)["outputs"]
    exps = [e for _, e in out]
    lab.row(f"PRIMEGAME, {STEPS:,} steps", "2^" + ", 2^".join(map(str, exps)))
    lab.row("first outputs at steps", ", ".join(str(step) for step, _ in out[:5]) + "   (the film: 19, 69, ...)")
    assert exps == primes_below(exps[-1] + 1) and len(exps) >= 10 and out[0] == (19, 2) and out[1] == (69, 3)
    lab.note = ("A match is a finite certificate and so is an exhausted overhang graph, but a search that hits its "
                "budget has proved nothing: the budget that would suffice is not computable in general.")

    fig, ax = labs.figure(2, size=(11, 4.4))
    k = np.arange(1, len(over) + 1)
    over = np.array(over)
    ax[0].fill_between(k, over, 0, color=labs.GOLD, alpha=0.6)
    ax[0].plot(k, over, color=labs.GOLD, lw=1.2)
    ax[0].axhline(0, color=labs.MUTED, lw=0.8)
    ax[0].set(title="The shortest match of the four-domino set: 206 dominoes", xlabel="dominoes placed",
              ylabel="top length minus bottom length (symbols)")
    steps = np.array([st for st, _ in out])
    ax[1].loglog(exps, steps, "o-", color=labs.GREEN, label="step at which 2^p first appears")
    ax[1].set_xticks(exps, [str(e) if e not in (17, 23, 29) else "" for e in exps])
    ax[1].set_xticks([], minor=True)
    ax[1].set(title="PRIMEGAME: fourteen fractions that list the primes", xlabel="prime p", ylabel="steps")
    ax[1].legend(loc="upper left")
    lab.fig = fig
    return lab
