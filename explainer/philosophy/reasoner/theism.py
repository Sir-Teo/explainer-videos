"""God and the philosophers, built (Part 23).

* Plantinga's modal ontological argument checked on every small Kripke frame: valid on S5 frames, not on S4 or T
  frames; its mirror image is valid too.
* Gödel's ontological proof in a finite higher-order modal logic: properties are sets of (world, individual) pairs,
  positiveness a set of properties. The Reasoner searches every model with up to two worlds and two individuals:
  Gödel's original axioms have no model at all (Benzmüller and Woltzenlogel Paleo, 2014), and every model of Scott's
  variant has a single world, i.e. modal collapse.
* Van Inwagen's argument that the principle of sufficient reason collapses modality, on a finite space of worlds.
* Fine-tuning: likelihoods for design, a single chance universe and a multiverse, on the evidence that some
  universe permits life and on the evidence that this one does (White, 2000).
* Pascal's wager with infinite utilities; Hájek's (2003) mixed strategies and the many-gods problem.
* Rowe's evidential argument as a Bayesian update, and how skeptical theism blocks it.
* Hume on miracles as a Bayesian question: one witness against a tiny prior, and many independent witnesses
  (Price, 1767; Babbage, 1837; Earman, 2000).
* Branching time: Prior's Peircean and Ockhamist semantics on Aristotle's sea battle.
"""

from __future__ import annotations

import itertools
import math

from explainer.philosophy.reasoner import modal


# ---------------------------------------------------------------------------
# Plantinga's modal ontological argument
# ---------------------------------------------------------------------------
def plantinga(max_worlds: int = 3) -> dict:
    """g: a maximally great being exists. Maximal greatness includes necessary existence, so the possibility premise
    is <>[]g. Check, on every frame up to ``max_worlds`` worlds, whether <>[]g -> []g (and -> g) holds, and the mirror
    argument <>~g -> ~<>[]g. Frames are grouped by the systems they satisfy."""
    forms = {"argument": modal.parse("<>[]g -> []g"), "conclusion": modal.parse("<>[]g -> g"),
             "mirror": modal.parse("<>~g -> ~<>[]g")}
    tally = {s: {k: [0, 0] for k in forms} for s in ("S5", "S4", "B", "T")}
    for n in range(1, max_worlds + 1):
        pairs = [(i, j) for i in range(n) for j in range(n)]
        for bits in range(2 ** len(pairs)):
            R = {p for k, p in enumerate(pairs) if bits >> k & 1}
            refl = modal.reflexive(R, n)
            if not refl:
                continue
            sym, tr = modal.symmetric(R, n), modal.transitive(R, n)
            systems = ["T"] + (["S4"] if tr else []) + (["B"] if sym else []) + (["S5"] if sym and tr else [])
            for k, f in forms.items():
                ok = modal.valid_on_frame(f, R, n)
                for s in systems:
                    tally[s][k][0] += 1
                    tally[s][k][1] += ok
    return {s: {k: {"frames": v[0], "valid_on": v[1]} for k, v in d.items()} for s, d in tally.items()}


# ---------------------------------------------------------------------------
# Gödel's ontological proof, in finite models
# ---------------------------------------------------------------------------
def _godel_check(W, D, P, version: str):
    """P: a set of properties (frozensets of (w, d) pairs). Return None if the axioms fail, else a dict with G, NE
    and whether modal collapse holds."""
    cells = [(w, d) for w in W for d in D]
    full = frozenset(cells)

    def neg(phi):
        return full - phi

    def entails_nec(phi, psi):           # [] forall y (phi(y) -> psi(y)), S5 with universal access
        return phi <= psi

    # A1: P(~phi) <-> ~P(phi)
    props = [frozenset(s) for k in range(len(cells) + 1) for s in itertools.combinations(cells, k)]
    for phi in props:
        if (neg(phi) in P) == (phi in P):
            return None
    # A2: P(phi) and [](phi -> psi) => P(psi)
    for phi in P:
        for psi in props:
            if entails_nec(phi, psi) and psi not in P:
                return None
    # G(x) at w iff every positive property holds of x at w
    G = frozenset((w, d) for w, d in cells if all((w, d) in phi for phi in P))
    if G not in P:                       # A3
        return None

    def ess(phi, w, d):
        base = all(entails_nec(phi, psi) for psi in props if (w, d) in psi)
        return base if version == "godel" else ((w, d) in phi and base)

    # NE(x) at w iff every essence of x at w is necessarily exemplified
    NE = frozenset((w, d) for w, d in cells
                   if all(all(any((v, e) in phi for e in D) for v in W) for phi in props if ess(phi, w, d)))
    if NE not in P:                      # A5
        return None
    worlds_with_god = {w for w, d in G}
    # modal collapse: every true proposition (any set of worlds) is necessary, i.e. true at every world
    wprops = [set(s) for k in range(len(W) + 1) for s in itertools.combinations(W, k)]
    collapse = all(p_ == set(W) for p_ in wprops for w in W if w in p_)
    gods = max(len({d for w2, d in G if w2 == w}) for w in W)
    return {"G": sorted(G), "NE": sorted(NE), "god_everywhere": worlds_with_god == set(W), "collapse": collapse,
            "gods": gods}


def godel(max_cells: int = 4) -> dict:
    """Search every finite model (rigid positiveness P; S5) for Gödel's original axioms and for Scott's, with any
    number of worlds and individuals whose product is at most ``max_cells``. A1 forces P to pick exactly one of each
    complementary pair of properties, so the search runs over those choices."""
    out = {}
    sizes = [(nw, nd) for nw in range(1, max_cells + 1) for nd in range(1, max_cells + 1) if nw * nd <= max_cells]
    for version in ("godel", "scott"):
        rows = []
        for nw, nd in sizes:
            if True:
                W, D = list(range(nw)), list(range(nd))
                cells = [(w, d) for w in W for d in D]
                full = frozenset(cells)
                props = [frozenset(s) for k in range(len(cells) + 1) for s in itertools.combinations(cells, k)]
                pairs, seen = [], set()
                for phi in props:
                    if phi not in seen:
                        seen |= {phi, full - phi}
                        pairs.append((phi, full - phi))
                models, collapse, god_everywhere, unique = 0, 0, 0, 0
                for pick in itertools.product([0, 1], repeat=len(pairs)):
                    P = frozenset(pr[b] for pr, b in zip(pairs, pick))
                    r = _godel_check(W, D, P, version)
                    if r:
                        models += 1
                        collapse += r["collapse"]
                        god_everywhere += r["god_everywhere"]
                        unique += r["gods"] == 1
                rows.append({"worlds": nw, "individuals": nd, "candidates": 2 ** len(pairs), "models": models,
                             "collapse": collapse, "god_everywhere": god_everywhere, "one_god": unique})
        out[version] = rows
    return out


# ---------------------------------------------------------------------------
# The principle of sufficient reason and modal collapse (van Inwagen 1983)
# ---------------------------------------------------------------------------
def psr_collapse(n_worlds: int = 4) -> dict:
    """Propositions are sets of worlds; the actual world is 0. The big conjunctive contingent fact p is {0}. An
    explanation q of p must be true, must entail p, and must not be p itself (nothing explains itself). Count the
    candidates: with more than one world there are none, so PSR forces a single world: every truth necessary."""
    rows = []
    for n in range(1, n_worlds + 1):
        W = list(range(n))
        p = frozenset({0})
        props = [frozenset(s) for k in range(n + 1) for s in itertools.combinations(W, k)]
        truths = [q for q in props if 0 in q]
        explainers = [q for q in truths if q <= p and q != p]
        contingent_truths = [q for q in truths if q != frozenset(W)]
        rows.append({"worlds": n, "true_propositions": len(truths), "contingent_truths": len(contingent_truths),
                     "explainers_of_bccf": len(explainers)})
    return {"rows": rows}


# ---------------------------------------------------------------------------
# Fine-tuning
# ---------------------------------------------------------------------------
def fine_tuning(eps: float = 1e-3, q_design: float = 0.5, universes: int = 10_000) -> dict:
    """A constant is uniform on [0, 1] by chance; life needs it in a window of width eps. A designer would make it
    life-permitting with probability q. A multiverse of N independent universes. Likelihoods of two pieces of
    evidence: E_some, `some universe permits life', and E_this, `this universe, alpha, permits life'."""
    p_some_multi = 1 - (1 - eps) ** universes
    lik = {
        "single chance": {"some": eps, "this": eps},
        "multiverse": {"some": p_some_multi, "this": eps},
        "design": {"some": q_design, "this": q_design},
    }
    prior = {"single chance": 1 / 3, "multiverse": 1 / 3, "design": 1 / 3}

    def post(key):
        z = sum(prior[h] * lik[h][key] for h in prior)
        return {h: round(prior[h] * lik[h][key] / z, 4) for h in prior}

    return {"eps": eps, "q_design": q_design, "universes": universes, "likelihoods": lik,
            "posterior_some": post("some"), "posterior_this": post("this"),
            "lr_design_vs_chance": q_design / eps}


# ---------------------------------------------------------------------------
# Pascal's wager
# ---------------------------------------------------------------------------
INF = math.inf


def pascal(p_god: float = 0.01, finite_cost: float = 10.0) -> dict:
    """Utilities: wager for God and God exists: infinite; otherwise finite. Expected utility of each strategy, with
    extended reals. Hájek's mixed strategies: wager with probability r (flip a coin; or follow a lottery): any r > 0
    gives infinite expected utility, so wagering does not beat them. Many gods: two jealous gods, each rewarding only
    its own worshippers, give infinite expected utility to both wagers."""
    def eu(r):
        # with probability r you end up wagering for God
        if r > 0 and p_god > 0:
            return INF
        return -finite_cost * r + 0.0

    strategies = [("wager for God", 1.0), ("do not wager", 0.0), ("flip a coin", 0.5), ("wager if a die shows six", 1 / 6),
                  ("wager if a lottery is won", 1e-6)]
    rows = [{"strategy": s, "eu": eu(r)} for s, r in strategies]
    many = [{"strategy": f"worship god {k}", "eu": INF} for k in ("A", "B")]
    return {"p_god": p_god, "rows": rows, "many_gods": many}


# ---------------------------------------------------------------------------
# Rowe's evidential argument
# ---------------------------------------------------------------------------
def rowe(prior: float = 0.5, p_e_given_not: float = 0.9) -> dict:
    """E: an evil such as the fawn's suffering, with no good we can see that it serves. P(E | no God) is high. The
    posterior for God depends on P(E | God): Rowe takes it to be low; the skeptical theist (Wykstra, 1984) says we
    are in no position to judge it low, since goods beyond our ken would be invisible to us either way."""
    rows = []
    for p_e_g in (0.05, 0.1, 0.3, 0.6, 0.9):
        post = prior * p_e_g / (prior * p_e_g + (1 - prior) * p_e_given_not)
        rows.append({"p_e_given_god": p_e_g, "posterior": round(post, 3)})
    return {"prior": prior, "p_e_given_not": p_e_given_not, "rows": rows}


# ---------------------------------------------------------------------------
# Hume on miracles
# ---------------------------------------------------------------------------
def hume(prior: float = 1e-6, hit: float = 0.99, false_alarm: float = 0.01, max_witnesses: int = 6) -> dict:
    """A reported miracle M with a tiny prior. Each witness reports M with probability `hit' if it happened and
    `false_alarm' if it did not, independently. One witness leaves M very improbable (Hume's maxim); several truly
    independent witnesses can make it probable (Price, 1767; Babbage, 1837; Earman, 2000)."""
    rows = []
    for k in range(0, max_witnesses + 1):
        num = prior * hit ** k
        den = num + (1 - prior) * false_alarm ** k
        rows.append({"witnesses": k, "posterior": num / den})
    first_over_half = next((r["witnesses"] for r in rows if r["posterior"] > 0.5), None)
    return {"prior": prior, "hit": hit, "false_alarm": false_alarm, "rows": rows,
            "first_over_half": first_over_half}


# ---------------------------------------------------------------------------
# Branching time: the sea battle
# ---------------------------------------------------------------------------
def sea_battle() -> dict:
    """Moments: m0 (today) branches to m1 (battle tomorrow) and m2 (no battle). Histories: h1 = (m0, m1), h2 = (m0,
    m2). Peircean: `F p' at a moment is true iff p holds at the next moment on every history through it. Ockhamist:
    truth is relative to a moment and a history; `F p' at (m, h) iff p holds at the next moment of h; `settled p' at
    m iff p at (m, h) for all h through m."""
    battle = {"m1": True, "m2": False}
    hist = {"h1": ["m0", "m1"], "h2": ["m0", "m2"]}

    def ock_F(p_true, h):
        return p_true(hist[h][1])

    B = lambda m: battle[m]  # noqa: E731
    notB = lambda m: not battle[m]  # noqa: E731
    peirce = {"F battle": all(ock_F(B, h) for h in hist), "F no battle": all(ock_F(notB, h) for h in hist)}
    peirce["F battle or F no battle"] = peirce["F battle"] or peirce["F no battle"]
    peirce["F (battle or no battle)"] = all(ock_F(lambda m: B(m) or notB(m), h) for h in hist)
    ock = {h: {"F battle": ock_F(B, h), "F no battle": ock_F(notB, h),
               "F battle or F no battle": ock_F(B, h) or ock_F(notB, h)} for h in hist}
    settled = {k: all(ock[h][k] for h in hist) for k in ("F battle", "F no battle", "F battle or F no battle")}
    return {"peircean": peirce, "ockhamist": ock, "settled": settled}


# ---------------------------------------------------------------------------
# The third way's quantifier shift
# ---------------------------------------------------------------------------
def third_way(n_things: int = 8, span: int = 3) -> dict:
    """Aquinas's third way reasons: each contingent thing at some time does not exist; so at some time nothing
    exists. A relay of overlapping lifetimes is a countermodel: thing k exists at times k .. k + span - 1, over the
    times 0 .. n_things + span - 2. Every thing fails to exist at some time, yet at every time something exists."""
    T = list(range(n_things + span - 1))
    life = {k: set(range(k, k + span)) for k in range(n_things)}
    each_absent_sometime = all(any(t not in life[k] for t in T) for k in life)
    some_time_empty = any(all(t not in life[k] for k in life) for t in T)
    return {"times": len(T), "things": n_things, "lives": {k: sorted(v) for k, v in life.items()},
            "each_absent_sometime": each_absent_sometime, "some_time_empty": some_time_empty}


def revolutions(years=(60, 600, 6000, 60000)) -> dict:
    """Al-Ghazālī: the sun goes round once a year, Jupiter once in twelve, Saturn once in thirty. Over any finite
    past the counts keep fixed ratios; over an infinite past each is countably infinite, and the three sets can be put
    in one-to-one correspondence (Part 6)."""
    rows = [{"years": y, "sun": y, "jupiter": y // 12, "saturn": y // 30} for y in years]
    return {"rows": rows}


def st_petersburg(max_games: int = 100_000, seed: int = 1738) -> dict:
    """Daniel Bernoulli's (1738) game: a fair coin is tossed until it lands heads; if that takes k tosses, the prize
    is 2^k. The expected prize is 1 + 1 + 1 + ... : infinite. Simulated running averages grow only like log2 of the
    number of games played, and nobody would pay much to play: infinite expectations misbehave, as in Pascal."""
    import random
    rng = random.Random(seed)
    total, out, checkpoints = 0, [], [10, 100, 1000, 10_000, 100_000]
    for n in range(1, max_games + 1):
        k = 1
        while rng.random() < 0.5:
            k += 1
        total += 2 ** k
        if n in checkpoints:
            out.append({"games": n, "average": round(total / n, 2), "log2": round(math.log2(n), 2)})
    partial = [sum(0.5 ** k * 2 ** k for k in range(1, m + 1)) for m in (5, 10, 20, 40)]
    return {"rows": out, "partial_expectations": partial}
