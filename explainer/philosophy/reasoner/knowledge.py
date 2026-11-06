"""Knowledge, made checkable (Part 11): Gettier's cases as first-order models, the conditions an analysis might add
and a check for each, reliability and the generality problem, sensitivity and safety over a similarity ordering of
worlds, margins for error (anti-luminosity and the failure of KK), Lewis's relevant alternatives, coherence and the
Bovens--Hartmann impossibility, and Quine's web.

    from explainer.philosophy.reasoner import knowledge as Kn
    Kn.gettier("coins")                    # every JTB condition holds, the lemma is false, and a nearby world fails
    sc = Kn.SCENARIOS["biv"]
    Kn.sensitive(sc, "not_biv"), Kn.safe(sc, "not_biv")    # (False, ...), (True, ...): the checkers disagree
    Kn.luminosity_series()                 # the cold morning: the moments that are cold but not knowably cold
    Kn.iterate_k(range(31), lambda w: w <= 20, margin=1)     # K p, KK p, KKK p shrink one step at a time
    Kn.revisions(Kn.WEB)                   # Duhem--Quine: every maximal consistent subset of the web

A *scenario* is a finite set of worlds, each a dict of facts with a distance from the actual world (the similarity
ordering of Lewis's and Nozick's counterfactuals, coarsened to whole numbers), a belief-forming method (facts ->
the set of propositions the subject believes there), and named propositions (facts -> bool). Everything else is
computed from that.
"""

from __future__ import annotations

import itertools
from dataclasses import dataclass, field
from fractions import Fraction
from typing import Callable

from explainer.philosophy.reasoner import fol, prop


# ---------------------------------------------------------------------------
# Gettier (1963): justified true belief without knowledge
# ---------------------------------------------------------------------------
GETTIER_CASES = {
    # Case I. Smith has strong evidence that Jones will get the job (the president told him) and that Jones has ten
    # coins in his pocket (he counted them). He infers: the man who will get the job has ten coins in his pocket.
    # Unknown to him, Smith himself gets the job, and Smith too has ten coins in his pocket.
    "coins": {
        "evidence": ["Job(jones)", "Ten(jones)"],
        "belief": "exists x (Job(x) & Ten(x))",
        "domain": ["smith", "jones"],
        "actual": {"Job": {("smith",)}, "Ten": {("smith",), ("jones",)}},
        "nearby": {"Job": {("smith",)}, "Ten": {("jones",)}},          # Smith has nine coins
        "nearby_text": "Smith has nine coins in his pocket",
    },
    # Case II. Smith has strong evidence that Jones owns a Ford. He picks a place at random and infers: either Jones
    # owns a Ford, or Brown is in Barcelona. Jones does not own a Ford (he rents one), but by chance Brown is in
    # Barcelona.
    "ford": {
        "evidence": ["Ford(jones)"],
        "belief": "Ford(jones) | Barcelona(brown)",
        "domain": ["jones", "brown"],
        "actual": {"Ford": set(), "Barcelona": {("brown",)}},
        "nearby": {"Ford": set(), "Barcelona": set()},                    # Brown is in Boston
        "nearby_text": "Brown is in Boston",
    },
}


def _structure(case: dict, facts: dict) -> fol.Structure:
    return fol.Structure(case["domain"], facts, consts={d: d for d in case["domain"]})


def gettier(name: str) -> dict:
    """Check a Gettier case: the inference is valid (so justification is passed on, by Gettier's closure
    principle), the belief is true and believed, yet the premise it rests on is false, and in a nearby world with
    the same evidence the same inference yields a falsehood."""
    c = GETTIER_CASES[name]
    prem = [fol.parse(e) for e in c["evidence"]]
    goal = fol.parse(c["belief"])
    valid = fol.prove(prem, goal).closed
    act = _structure(c, c["actual"])
    near = _structure(c, c["nearby"])
    return {
        "evidence": c["evidence"], "belief": c["belief"],
        "valid": valid,
        "premises_true": [fol.holds(p, act) for p in prem],
        "true": fol.holds(goal, act),
        "believed": True, "justified": valid,
        "false_lemma": not all(fol.holds(p, act) for p in prem),
        "nearby_true": fol.holds(goal, near), "nearby_text": c["nearby_text"],
        "belief_tex": fol.show(goal, tex=True), "evidence_tex": [fol.show(p, tex=True) for p in prem],
    }


# ---------------------------------------------------------------------------
# Scenarios: worlds ordered by similarity, a method, and propositions
# ---------------------------------------------------------------------------
@dataclass
class Scenario:
    title: str
    worlds: dict                      # name -> facts
    dist: dict                        # name -> distance from the actual world (0 for the actual world)
    method: Callable                  # facts -> set of proposition names believed there
    props: dict                       # name -> facts -> bool
    text: dict = field(default_factory=dict)    # name -> a short description of the world

    @property
    def actual(self) -> str:
        return next(w for w, d in self.dist.items() if d == 0)

    def true(self, p: str, w: str) -> bool:
        return self.props[p](self.worlds[w])

    def believes(self, p: str, w: str) -> bool:
        return p in self.method(self.worlds[w])


def jtb(sc: Scenario, p: str) -> dict:
    a = sc.actual
    return {"true": sc.true(p, a), "believed": sc.believes(p, a)}


def sensitive(sc: Scenario, p: str) -> tuple[bool, list]:
    """Nozick's third condition: if p were false, S would not believe p. True when, in the closest worlds where p is
    false, S does not believe p. Returns (verdict, those closest not-p worlds)."""
    notp = [w for w in sc.worlds if not sc.true(p, w)]
    if not notp:
        return True, []
    d = min(sc.dist[w] for w in notp)
    closest = [w for w in notp if sc.dist[w] == d]
    return all(not sc.believes(p, w) for w in closest), closest


def adherent(sc: Scenario, p: str) -> tuple[bool, list]:
    """Nozick's fourth condition: if p were true, S would believe it (in the closest p-worlds other than actuality)."""
    pw = [w for w in sc.worlds if sc.true(p, w) and sc.dist[w] > 0]
    if not pw:
        return True, []
    d = min(sc.dist[w] for w in pw)
    closest = [w for w in pw if sc.dist[w] == d]
    return all(sc.believes(p, w) for w in closest), closest


def safe(sc: Scenario, p: str, radius: int = 2) -> tuple[bool, list]:
    """Safety (Sosa 1999; Williamson 2000): in every nearby world (distance <= radius) where S believes p, p is
    true. Returns (verdict, the nearby worlds where S believes p falsely)."""
    bad = [w for w in sc.worlds if sc.dist[w] <= radius and sc.believes(p, w) and not sc.true(p, w)]
    return not bad, bad


def verdicts(sc: Scenario, ps, radius: int = 2) -> list[dict]:
    out = []
    for p in ps:
        s, sw = sensitive(sc, p)
        f, fw = safe(sc, p, radius)
        out.append({"p": p, **jtb(sc, p), "sensitive": s, "closest_not_p": sw, "safe": f, "unsafe_worlds": fw})
    return out


def _barns() -> Scenario:
    # Goldman (1976), after Ginet: Barn County is full of papier-mache facades, indistinguishable from the road.
    # Kripke's twist: every facade is green; the one real barn Henry looks at is red.
    worlds = {
        "red barn": {"shape": True, "real": True, "red": True},
        "green facade": {"shape": True, "real": False, "red": False},
        "green barn": {"shape": True, "real": True, "red": False},
        "empty field": {"shape": False, "real": False, "red": False},
        "red facade": {"shape": True, "real": False, "red": True},
    }
    dist = {"red barn": 0, "green facade": 1, "green barn": 1, "empty field": 2, "red facade": 4}

    def method(f):
        b = set()
        if f["shape"]:
            b.add("barn")
            if f["red"]:
                b.add("red barn")
        return b
    props = {"barn": lambda f: f["real"], "red barn": lambda f: f["real"] and f["red"]}
    text = {"red barn": "Henry looks at the one real barn, which is red",
            "green facade": "he looks at one of the facades (all are green)",
            "green barn": "he looks at a green barn",
            "empty field": "he looks at an empty field",
            "red facade": "someone paints a facade red (no one ever has)"}
    return Scenario("Barn County", worlds, dist, method, props, text)


def _biv() -> Scenario:
    worlds = {
        "normal": {"vat": False, "hands": True},
        "lost hands": {"vat": False, "hands": False},
        "envatted": {"vat": True, "hands": False},
    }
    dist = {"normal": 0, "lost hands": 2, "envatted": 9}

    def method(f):
        b = {"not_biv"}                  # experience is the same either way: S always believes she is not envatted
        if f["vat"] or f["hands"]:       # a vat delivers hand-experiences; a handless person sees no hands
            b.add("hands")
        return b
    props = {"hands": lambda f: f["hands"], "not_biv": lambda f: not f["vat"]}
    text = {"normal": "you, as you are", "lost hands": "an accident took your hands",
            "envatted": "a brain in a vat, fed the same experiences"}
    return Scenario("Hands and the vat", worlds, dist, method, props, text)


def _chute() -> Scenario:
    # Sosa (1999): on the way to the elevator, I release a trash bag down the chute from my high-rise condo.
    worlds = {"falls": {"basement": True}, "snags": {"basement": False}}
    dist = {"falls": 0, "snags": 5}
    return Scenario("The garbage chute", worlds, dist, lambda f: {"basement"}, {"basement": lambda f: f["basement"]},
                    {"falls": "the bag falls to the basement", "snags": "it snags on the way down (it never has)"})


def _coins() -> Scenario:
    worlds = {"actual": {"smith_job": True, "smith_ten": True},
              "nine coins": {"smith_job": True, "smith_ten": False},
              "jones hired": {"smith_job": False, "smith_ten": True}}
    dist = {"actual": 0, "nine coins": 1, "jones hired": 1}
    props = {"p": lambda f: (f["smith_job"] and f["smith_ten"]) or (not f["smith_job"])}   # Jones has ten coins
    return Scenario("Smith's coins", worlds, dist, lambda f: {"p"}, props,
                    {"actual": "Smith gets the job; Smith has ten coins", "nine coins": "Smith has nine coins",
                     "jones hired": "Jones gets the job, as the president said"})


def _clock() -> Scenario:
    # Russell, Human Knowledge (1948): a clock that stopped at eight, looked at by chance at exactly eight.
    worlds = {"8:00": {"t": 0}, "7:58": {"t": -2}, "8:03": {"t": 3}}
    dist = {"8:00": 0, "7:58": 1, "8:03": 1}
    return Scenario("Russell's clock", worlds, dist, lambda f: {"eight"}, {"eight": lambda f: f["t"] == 0},
                    {"8:00": "you glance at eight", "7:58": "two minutes earlier", "8:03": "three minutes later"})


def _lottery() -> Scenario:
    worlds = {"loses": {"win": False}, "wins": {"win": True}}
    dist = {"loses": 0, "wins": 1}          # the winning ball is one roll of a drum away
    return Scenario("A lottery ticket", worlds, dist, lambda f: {"lose"}, {"lose": lambda f: not f["win"]},
                    {"loses": "your ticket loses", "wins": "a different ball drops: it wins"})


SCENARIOS = {"barns": _barns(), "biv": _biv(), "chute": _chute(), "coins": _coins(), "clock": _clock(),
             "lottery": _lottery()}


# ---------------------------------------------------------------------------
# Zagzebski (1994): the recipe
# ---------------------------------------------------------------------------
def zagzebski(radius: int = 1) -> dict:
    """Run Zagzebski's two-step recipe on her doctor. Step one: a case of justified false belief (Dr Jones's
    belief that her patient has virus X, from symptoms that virus X reliably produces; in fact virus Y causes them).
    Step two: add luck, independent of the evidence, that makes the belief true (the patient has just caught X as
    well, too recently for symptoms). Every condition that does not entail truth survives both steps; safety fails."""
    rel = Fraction(95, 100)              # the diagnostic method is right 95% of the time in the population
    step1 = {"x": False, "y": True, "symptoms": True}
    step2 = {"x": True, "y": True, "symptoms": True}

    def conds(f):
        return {"believes": f["symptoms"], "justified": f["symptoms"], "reliable": rel >= Fraction(9, 10),
                "true": f["x"]}
    sc = Scenario("Dr Jones", {"lucky": step2, "unlucky": step1}, {"lucky": 0, "unlucky": radius},
                  lambda f: {"x"} if f["symptoms"] else set(), {"x": lambda f: f["x"]})
    return {"step1": conds(step1), "step2": conds(step2), "reliability": float(rel),
            "safe": safe(sc, "x", radius)[0], "sensitive": sensitive(sc, "x")[0]}


# ---------------------------------------------------------------------------
# Reliabilism and the generality problem
# ---------------------------------------------------------------------------
# A toy population of barn-judgments made by eye from the road: (region, light, real barn?, count). Every judgment
# is "that is a barn"; it is true just when the object is a real barn.
BARN_POPULATION = [
    ("farmland", "day", True, 940), ("farmland", "day", False, 10),
    ("farmland", "dusk", True, 180), ("farmland", "dusk", False, 20),
    ("Barn County", "day", True, 3), ("Barn County", "day", False, 27),
    ("Barn County", "dusk", True, 1), ("Barn County", "dusk", False, 9),
]

PROCESS_TYPES = [
    ("vision", lambda r, l: True),
    ("vision in daylight", lambda r, l: l == "day"),
    ("vision at dusk", lambda r, l: l == "dusk"),
    ("vision from the road in Barn County", lambda r, l: r == "Barn County"),
    ("vision in daylight in Barn County", lambda r, l: r == "Barn County" and l == "day"),
]


def reliability(test, population=BARN_POPULATION) -> tuple[int, int]:
    """(true judgments, all judgments) among the population's judgments of a process type."""
    hit = sum(n for r, l, ok, n in population if test(r, l) and ok)
    tot = sum(n for r, l, ok, n in population if test(r, l))
    return hit, tot


def generality(token=("Barn County", "day")) -> list[dict]:
    """Henry's one judgment (in Barn County, by day, at the real barn) is a token of every type below; each type
    has its own reliability, and reliabilism has not said which is *the* process."""
    out = []
    for name, test in PROCESS_TYPES:
        if test(*token):
            h, t = reliability(test)
            out.append({"type": name, "true": h, "all": t, "rate": h / t})
    out.append({"type": "this very look, at this barn", "true": 1, "all": 1, "rate": 1.0})
    return out


# ---------------------------------------------------------------------------
# Margins for error: anti-luminosity and KK
# ---------------------------------------------------------------------------
def luminosity_series(n: int = 24, threshold: float = 0.5, margin: float = 0.1) -> dict:
    """Williamson's cold morning. At dawn (t = 0) one feels freezing; by noon (t = n) warm; the feeling changes
    gradually, by 1/n each step. One feels cold at t iff the feeling is above the threshold. Knowledge needs a
    margin for error: one knows one feels cold at t only if one feels cold at every moment whose feeling is within
    the margin of the feeling at t. Returns the feeling, cold and known-cold at each moment, the moments that are
    cold but not knowably so (where luminosity fails), and the sorites chain that luminosity plus the margin
    principle would force."""
    feel = [1 - t / n for t in range(n + 1)]
    cold = [f > threshold for f in feel]
    known = [cold[t] and all(cold[u] for u in range(n + 1) if abs(feel[u] - feel[t]) <= margin + 1e-12)
             for t in range(n + 1)]
    gap = [t for t in range(n + 1) if cold[t] and not known[t]]
    # Luminosity: cold(t) -> K cold(t). Margin: K cold(t) -> cold(t+1). From cold(0), these give cold(t) for all t.
    chain, t = [], 0
    while t < n and cold[t]:
        chain.append(t)
        t += 1
    return {"feel": feel, "cold": cold, "known": known, "gap": gap, "first_warm": cold.index(False),
            "chain_breaks_at": t}


def k_set(worlds, p_set, margin: int = 1) -> set:
    """In a margin model (worlds on a line, accessible when within `margin`), the worlds where p is known."""
    ws = list(worlds)
    return {w for w in ws if all(v in p_set for v in ws if abs(v - w) <= margin)}


def iterate_k(worlds, p, margin: int = 1, depth: int = 4) -> list[set]:
    """[p, Kp, KKp, ...] as sets of worlds. Each K strips a margin off the edge, so KK p is strictly harder than K p
    near the boundary: the KK principle fails."""
    ws = list(worlds)
    sets = [{w for w in ws if p(w)}]
    for _ in range(depth):
        sets.append(k_set(ws, sets[-1], margin))
    return sets


# ---------------------------------------------------------------------------
# Lewis, "Elusive Knowledge" (1996): eliminate every not-p possibility, except those properly ignored
# ---------------------------------------------------------------------------
BANK = {
    "p": "the bank is open on Saturday",
    "possibilities": [
        ("open, as I saw two weeks ago", True, False),
        ("closed: it changed its hours since", False, True),
        ("closed: a burst pipe on Saturday morning", False, True),
    ],
    "evidence": "I was there two Saturdays ago",
}


def lewis_knows(possibilities, eliminated: set, ignored: set) -> tuple[bool, list]:
    """S knows p iff every not-p possibility is eliminated by S's evidence or properly ignored in the context.
    ``possibilities`` lists (name, p true there?, ...). Returns (verdict, the not-p possibilities left open)."""
    open_ = [nm for nm, ptrue, *_ in possibilities if not ptrue and nm not in eliminated and nm not in ignored]
    return not open_, open_


# ---------------------------------------------------------------------------
# Coherence (Shogenji 1999; Olsson 2002) and the Bovens--Hartmann impossibility (2003)
# ---------------------------------------------------------------------------
def shogenji(joint: dict) -> float:
    """C(A1..An) = P(all) / prod P(Ai), for a joint distribution {tuple of bools: prob}."""
    n = len(next(iter(joint)))
    pall = sum(pr for w, pr in joint.items() if all(w))
    marg = 1.0
    for i in range(n):
        marg *= sum(pr for w, pr in joint.items() if w[i])
    return pall / marg


def overlap(joint: dict) -> float:
    """Olsson's overlap measure: P(all) / P(any)."""
    pall = sum(pr for w, pr in joint.items() if all(w))
    pany = sum(pr for w, pr in joint.items() if any(w))
    return pall / pany


def posterior(joint: dict, x: float) -> float:
    """Probability that every report is true, given that independent witnesses each report their proposition and
    the likelihood ratio of a report (P(report | false) / P(report | true)) is x (Bovens and Hartmann 2003):
    a0 / sum_k a_k x^k, where a_k is the prior probability that exactly k of the propositions are false."""
    n = len(next(iter(joint)))
    a = [0.0] * (n + 1)
    for w, pr in joint.items():
        a[n - sum(w)] += pr
    return a[0] / sum(ak * x ** k for k, ak in enumerate(a))


def joint_from_profile(a: list) -> dict:
    """A joint distribution over n propositions whose chance of exactly k falsehoods is a[k], spread evenly over the
    worlds with k falsehoods."""
    n = len(a) - 1
    out = {}
    for w in itertools.product([True, False], repeat=n):
        k = n - sum(w)
        out[w] = a[k] / sum(1 for v in itertools.product([True, False], repeat=n) if n - sum(v) == k)
    return out


COHERENCE_PAIR = {"A": [0.1, 0.3, 0.0, 0.6], "B": [0.1, 0.0, 0.9, 0.0]}


def coherence_flip(pair=COHERENCE_PAIR, xs=None) -> dict:
    """Two sets of three reports with the same prior chance of all being true. Which is more likely true depends on
    how reliable the witnesses are, which no measure of the sets' coherence can see."""
    xs = xs or [i / 20 for i in range(1, 20)]
    ja, jb = joint_from_profile(pair["A"]), joint_from_profile(pair["B"])
    curve = [(x, posterior(ja, x), posterior(jb, x)) for x in xs]
    cross = None
    for (x0, a0, b0), (x1, a1, b1) in zip(curve, curve[1:]):
        if (a0 - b0) * (a1 - b1) < 0:
            cross = x0 + (x1 - x0) * (a0 - b0) / ((a0 - b0) - (a1 - b1))
    return {"shogenji": (shogenji(ja), shogenji(jb)), "overlap": (overlap(ja), overlap(jb)), "curve": curve,
            "cross": cross}


# ---------------------------------------------------------------------------
# Quine, "Two Dogmas" (1951): the web of belief
# ---------------------------------------------------------------------------
WEB = {
    "N": "Newton's laws of motion and gravitation",
    "K": "the known planets are all the planets",
    "T": "the telescopes and the tables are right",
    "L": "the mathematics of the prediction: N and K and T imply O",
    "notO": "the observed orbit is not the predicted one",
}


def web_formulas(web=WEB) -> dict:
    return {"N": prop.Var("N"), "K": prop.Var("K"), "T": prop.Var("T"),
            "L": prop.Imp(prop.And(prop.Var("N"), prop.Var("K"), prop.Var("T")), prop.Var("O")),
            "notO": prop.Not(prop.Var("O"))}


def revisions(web=WEB) -> list[list[str]]:
    """Every minimal way to restore consistency: the sets of beliefs whose removal leaves a satisfiable remainder,
    with no proper subset doing the same (the complements of the maximal consistent subsets)."""
    fs = web_formulas(web)
    names = list(web)
    out = []
    for k in range(len(names) + 1):
        for drop in itertools.combinations(names, k):
            if any(set(d) <= set(drop) for d in out):
                continue
            keep = [fs[n] for n in names if n not in drop]
            if prop.satisfiable(keep):
                out.append(list(drop))
    return out
