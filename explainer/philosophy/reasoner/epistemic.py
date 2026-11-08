"""Knowledge among many agents, made computable (Part 12): multi-agent epistemic models, public and private
announcements, common knowledge, the muddy children, the coordinated attack, Rubinstein's email game, Aumann's
agreement theorem and the Geanakoplos--Polemarchakis dialogue, Fitch's knowability paradox, the diversity prediction
theorem, and Zollman's networks of bandit-playing scientists.

    from explainer.philosophy.reasoner import epistemic as Ep
    M = Ep.muddy(3)                                 # 8 worlds; child i cannot tell worlds differing only at i
    Ep.muddy_rounds(3, actual=(1, 1, 0))            # who knows, round by round, after "at least one of you is muddy"
    Ep.attack_depth(6)                              # after n delivered messages: mutual knowledge to depth n, never C
    Ep.agreement_dialogue(...)                      # posteriors announced back and forth until they agree

Formulas are tuples: ("var", p), ("top",), ("not", A), ("and", A, B), ("or", A, B), ("imp", A, B), ("K", i, A),
("E", G, A) (everyone in G knows), ("C", G, A) (common knowledge in G), ("ann", A, B) (after the public announcement
of A, B). A model is a set of worlds, one equivalence relation per agent (given as a function: which worlds the agent
cannot tell from w), and a valuation.
"""

from __future__ import annotations

import itertools
import math
import random
from dataclasses import dataclass, field
from fractions import Fraction


# ---------------------------------------------------------------------------
# Multi-agent S5 models
# ---------------------------------------------------------------------------
@dataclass
class Model:
    worlds: list
    agents: list
    access: dict            # agent -> {w: set of worlds the agent considers possible at w}
    val: dict               # w -> set of true atoms
    names: dict = field(default_factory=dict)

    def restrict(self, keep) -> "Model":
        keep = [w for w in self.worlds if w in set(keep)]
        ks = set(keep)
        acc = {a: {w: {v for v in self.access[a][w] if v in ks} for w in keep} for a in self.agents}
        return Model(keep, self.agents, acc, {w: self.val[w] for w in keep}, self.names)


def holds(M: Model, w, f) -> bool:
    op = f[0]
    if op == "var":
        return f[1] in M.val[w]
    if op == "top":
        return True
    if op == "not":
        return not holds(M, w, f[1])
    if op == "and":
        return holds(M, w, f[1]) and holds(M, w, f[2])
    if op == "or":
        return holds(M, w, f[1]) or holds(M, w, f[2])
    if op == "imp":
        return (not holds(M, w, f[1])) or holds(M, w, f[2])
    if op == "K":
        return all(holds(M, v, f[2]) for v in M.access[f[1]][w])
    if op == "E":
        return all(holds(M, v, f[2]) for a in f[1] for v in M.access[a][w])
    if op == "C":
        return all(holds(M, v, f[2]) for v in reachable(M, f[1], w))
    if op == "ann":
        if not holds(M, w, f[1]):
            return True
        return holds(announce(M, f[1]), w, f[2])
    raise ValueError(op)


def reachable(M: Model, group, w) -> set:
    """Worlds reachable from w in one or more steps along any group member's relation: where common knowledge looks."""
    seen, todo = set(), [w]
    while todo:
        u = todo.pop()
        for a in group:
            for v in M.access[a][u]:
                if v not in seen:
                    seen.add(v)
                    todo.append(v)
    return seen


def announce(M: Model, f) -> Model:
    """Public announcement of f: delete the worlds where f is false."""
    return M.restrict([w for w in M.worlds if holds(M, w, f)])


def K(i, f):
    return ("K", i, f)


def Not(f):
    return ("not", f)


def And(*fs):
    out = fs[0]
    for g in fs[1:]:
        out = ("and", out, g)
    return out


def Or(*fs):
    out = fs[0]
    for g in fs[1:]:
        out = ("or", out, g)
    return out


def V(p):
    return ("var", p)


def knows_whether(i, f):
    return Or(K(i, f), K(i, Not(f)))


# ---------------------------------------------------------------------------
# The muddy children
# ---------------------------------------------------------------------------
def muddy(n: int) -> Model:
    """n children; a world says which are muddy (a tuple of 0s and 1s). Child i sees every forehead but its own, so
    it cannot tell apart worlds that differ only at i."""
    worlds = list(itertools.product((0, 1), repeat=n))
    agents = list(range(n))
    acc = {i: {w: {w, w[:i] + (1 - w[i],) + w[i + 1:]} for w in worlds} for i in agents}
    val = {w: {f"m{i}" for i in agents if w[i]} for w in worlds}
    return Model(worlds, agents, acc, val)


def muddy_rounds(n: int, actual=None, max_rounds: int | None = None) -> dict:
    """The father announces 'at least one of you is muddy'; then, round after round, every child says whether it
    knows if it is muddy, and while nobody knows, 'nobody knows' is publicly announced. Returns the number of worlds
    left after each announcement, and the round in which each child (in ``actual``) first knows."""
    M = muddy(n)
    actual = tuple(actual) if actual is not None else tuple([1] * n)
    someone = Or(*[V(f"m{i}") for i in range(n)])
    sizes = [len(M.worlds)]
    M = announce(M, someone)
    sizes.append(len(M.worlds))
    knows_at = {}
    nobody = And(*[Not(knows_whether(i, V(f"m{i}"))) for i in range(n)])
    rnd = 0
    while True:
        rnd += 1
        for i in range(n):
            if i not in knows_at and holds(M, actual, knows_whether(i, V(f"m{i}"))):
                knows_at[i] = rnd
        if len(knows_at) == n or (max_rounds and rnd >= max_rounds) or rnd > n + 1:
            break
        if holds(M, actual, nobody):
            M = announce(M, nobody)
            sizes.append(len(M.worlds))
        else:
            # some children know and say so: announce exactly who knows (the muddy ones, in the standard telling)
            who = [i for i in range(n) if holds(M, actual, knows_whether(i, V(f"m{i}")))]
            f = And(*[knows_whether(i, V(f"m{i}")) if i in who else Not(knows_whether(i, V(f"m{i}")))
                      for i in range(n)])
            M = announce(M, f)
            sizes.append(len(M.worlds))
    return {"sizes": sizes, "knows_at": [knows_at.get(i) for i in range(n)], "muddy": sum(actual)}


def muddy_cube_rounds(n: int = 3) -> list[list]:
    """For the n-cube drawing: the worlds remaining after the father's announcement and each 'nobody knows' (with
    every child muddy)."""
    M = announce(muddy(n), Or(*[V(f"m{i}") for i in range(n)]))
    out = [[list(w) for w in muddy(n).worlds], [list(w) for w in M.worlds]]
    nobody = And(*[Not(knows_whether(i, V(f"m{i}"))) for i in range(n)])
    while True:
        M2 = announce(M, nobody)
        if len(M2.worlds) == len(M.worlds) or not M2.worlds:
            break
        M = M2
        out.append([list(w) for w in M.worlds])
    return out


def without_father(n: int = 3) -> bool:
    """Without the father's announcement, 'nobody knows' changes nothing: return whether the model is unchanged."""
    M = muddy(n)
    nobody = And(*[Not(knows_whether(i, V(f"m{i}"))) for i in range(n)])
    return len(announce(M, nobody).worlds) == len(M.worlds)


def everyone_knew_already(n: int = 3, actual=None) -> dict:
    """With at least two muddy children, everyone already knew 'at least one is muddy' before the father spoke. What
    the announcement adds is common knowledge."""
    M = muddy(n)
    actual = tuple(actual) if actual is not None else tuple([1] * n)
    s = Or(*[V(f"m{i}") for i in range(n)])
    G = list(range(n))
    return {"everyone_knows": holds(M, actual, ("E", G, s)), "common": holds(M, actual, ("C", G, s)),
            "after": holds(announce(M, s), actual, ("C", G, s))}


# ---------------------------------------------------------------------------
# The coordinated attack (Halpern and Moses 1990)
# ---------------------------------------------------------------------------
def attack_model(N: int) -> Model:
    """Worlds 0..N: the number of messengers who got through. A sends message 1 (the plan), B acknowledges (2), A
    acknowledges the acknowledgement (3), and so on; each may be lost, ending the exchange. A knows how many it sent
    and received: it cannot tell 2k from 2k+1 (did its last message arrive?). B cannot tell 2k-1 from 2k."""
    worlds = list(range(N + 1))
    accA = {w: {v for v in worlds if v // 2 == w // 2} for w in worlds}
    accB = {w: {v for v in worlds if (v + 1) // 2 == (w + 1) // 2} for w in worlds}
    val = {w: ({"plan"} if w >= 1 else set()) for w in worlds}
    return Model(worlds, ["A", "B"], {"A": accA, "B": accB}, val)


def mutual_depth(M: Model, w, f, group, cap: int = 50) -> int:
    """The largest k such that E^k f holds at w (everyone knows that everyone knows ... f, k times)."""
    g = f
    k = 0
    while k < cap:
        g = ("E", group, g)
        if not holds(M, w, g):
            return k
        k += 1
    return k


def attack_depth(N: int = 8) -> list[dict]:
    M = attack_model(N + 1)
    plan = V("plan")
    G = ["A", "B"]
    out = []
    for w in range(N + 1):
        out.append({"delivered": w, "depth": mutual_depth(M, w, plan, G) if holds(M, w, plan) else -1,
                    "common": holds(M, w, ("C", G, plan))})
    return out


# ---------------------------------------------------------------------------
# Rubinstein's email game (1989)
# ---------------------------------------------------------------------------
def email_game(eps: float = 0.1, p: float = 0.25, M_: float = 2.0, L: float = 4.0, T: int = 12) -> dict:
    """Two generals; with prior p the enemy is weak (game b, where both should attack), else strong (game a, where
    neither should). Only A learns which. In game b, computers exchange confirmations, each lost with probability
    eps; each player's type is the number of messages its computer sent. Payoffs: both attack in b: M each; attacking
    alone: -L; not attacking: 0; attacking in a: -L. Start from 'attack whenever informed' and iterate best responses
    on types 0..T: the strategy unravels to 'never attack'. Returns the attack sets at each iteration."""
    # States: t = number of messages sent in total in game b (0 means none got through... we follow the standard
    # encoding): state 0 is game a; state k >= 1 means the k-th message was the first lost (k-1 delivered).
    # A's type: messages A sent; B's type: messages B sent.
    states = list(range(0, 2 * T + 2))
    prior = {0: 1 - p}
    for k in range(1, len(states)):
        prior[k] = p * eps * (1 - eps) ** (k - 1)

    def typeA(s):          # A sends message 1, 3, 5, ...; in state s >= 1, messages 1..s were sent, s-th lost
        return 0 if s == 0 else (s + 1) // 2

    def typeB(s):
        return 0 if s == 0 else s // 2

    def game(s):
        return "a" if s == 0 else "b"

    attackA = {t for t in range(1, T + 1)}      # attack whenever informed of game b (types >= 1)
    attackB = {t for t in range(1, T + 1)}
    history = [(sorted(attackA), sorted(attackB))]
    for _ in range(4 * T):
        newA, newB = set(), set()
        for t in range(0, T + 1):
            ss = [s for s in states if typeA(s) == t]
            tot = sum(prior[s] for s in ss)
            if tot == 0:
                continue
            u = 0.0
            for s in ss:
                partner = typeB(s) in attackB
                if game(s) == "b":
                    u += prior[s] * (M_ if partner else -L)
                else:
                    u += prior[s] * (-L)
            if u / tot > 0:
                newA.add(t)
        for t in range(0, T + 1):
            ss = [s for s in states if typeB(s) == t]
            tot = sum(prior[s] for s in ss)
            if tot == 0:
                continue
            u = 0.0
            for s in ss:
                partner = typeA(s) in newA
                if game(s) == "b":
                    u += prior[s] * (M_ if partner else -L)
                else:
                    u += prior[s] * (-L)
            if u / tot > 0:
                newB.add(t)
        history.append((sorted(newA), sorted(newB)))
        if newA == attackA and newB == attackB:
            break
        attackA, attackB = newA, newB
    return {"history": history, "final": history[-1], "eps": eps}


# ---------------------------------------------------------------------------
# Agreeing to disagree (Aumann 1976; Geanakoplos and Polemarchakis 1982)
# ---------------------------------------------------------------------------
def posterior(event, cell, prior) -> Fraction:
    num = sum(prior[w] for w in cell if w in event)
    den = sum(prior[w] for w in cell)
    return Fraction(num) / Fraction(den)


def cell_of(partition, w):
    return next(c for c in partition if w in c)


def agreement_dialogue(states, prior, partA, partB, event, actual, max_rounds: int = 10) -> list[dict]:
    """A and B announce their posteriors for ``event`` in turn; each announcement refines what the other can rule
    out (the states where the speaker would have said something else). Returns the announcements until they agree;
    Geanakoplos and Polemarchakis proved this always ends, in agreement, on a finite space."""
    pA = [set(c) for c in partA]
    pB = [set(c) for c in partB]
    out = []
    speaker = "A"
    for _ in range(max_rounds):
        part = pA if speaker == "A" else pB
        q = posterior(event, cell_of(part, actual), prior)
        qa = posterior(event, cell_of(pA, actual), prior)
        qb = posterior(event, cell_of(pB, actual), prior)
        out.append({"speaker": speaker, "says": q, "A": qa, "B": qb})
        # public: the states where the speaker would have announced q
        said = {w for w in states if posterior(event, cell_of(part, w), prior) == q}
        pA = [c & said for c in pA if c & said] + [c - said for c in pA if c - said]
        pB = [c & said for c in pB if c & said] + [c - said for c in pB if c - said]
        qa2 = posterior(event, cell_of(pA, actual), prior)
        qb2 = posterior(event, cell_of(pB, actual), prior)
        if qa2 == qb2 and len(out) > 1:
            out.append({"speaker": "both", "says": qa2, "A": qa2, "B": qb2})
            break
        speaker = "B" if speaker == "A" else "A"
    return out


GP_EXAMPLE = {
    # Nine equally likely states; A learns the row, B learns a coarser cut; the event is {1, 5, 9}... chosen so the
    # dialogue takes several rounds.
    "states": list(range(1, 10)),
    "prior": {w: Fraction(1, 9) for w in range(1, 10)},
    "A": [{1, 2, 3}, {4, 5, 6}, {7, 8, 9}],
    "B": [{1, 2, 3, 4}, {5, 6, 7, 8}, {9}],
    "event": {3, 4},
    "actual": 1,
}


# ---------------------------------------------------------------------------
# Fitch's paradox (1963)
# ---------------------------------------------------------------------------
def fitch_check() -> dict:
    """In any reflexive frame (knowledge implies truth), K(p and not Kp) is unsatisfiable. So if every truth were
    knowable, the truth 'p, and p is not known' would be knowable, i.e. possibly K(p and not Kp): impossible. Hence
    if all truths are knowable, all truths are known."""
    from explainer.philosophy.reasoner import modal
    f = modal.parse("~[](p & ~[]p)")
    valid_T, steps, _ = modal.tableau(f, reflexive_=True)
    valid_K, _, cm = modal.tableau(f, reflexive_=False)
    return {"valid_in_T": valid_T, "valid_in_K": valid_K, "steps": len(steps)}


# ---------------------------------------------------------------------------
# Moore sentences: an announcement that makes itself false
# ---------------------------------------------------------------------------
def moore_update() -> dict:
    """Two worlds: p true (w1) or false (w0); b cannot tell them apart. 'p, but you (b) don't know p' is true at w1;
    once publicly announced, b knows p, and the sentence is false."""
    M = Model(["w1", "w0"], ["b"], {"b": {"w1": {"w1", "w0"}, "w0": {"w1", "w0"}}}, {"w1": {"p"}, "w0": set()})
    s = And(V("p"), Not(K("b", V("p"))))
    after = announce(M, s)
    return {"before": holds(M, "w1", s), "after": holds(after, "w1", s), "b_knows_after": holds(after, "w1",
                                                                                                 K("b", V("p")))}


# ---------------------------------------------------------------------------
# Private announcements: a product update (Baltag, Moss and Solecki 1998)
# ---------------------------------------------------------------------------
def private_update() -> dict:
    """a privately reads a letter saying p; b knows nothing of it. The product of the two-world model with a
    two-event action model (a sees 'read p'; b thinks 'nothing happened')."""
    worlds = ["p", "~p"]
    events = ["read", "skip"]                     # read: a learns p (precondition p); skip: nothing (precondition top)
    pre = {"read": V("p"), "skip": ("top",)}
    ev_acc = {"a": {"read": {"read"}, "skip": {"skip"}}, "b": {"read": {"skip"}, "skip": {"skip"}}}
    M = Model(worlds, ["a", "b"], {"a": {w: set(worlds) for w in worlds}, "b": {w: set(worlds) for w in worlds}},
              {"p": {"p"}, "~p": set()})
    prod = [(w, e) for w in worlds for e in events if holds(M, w, pre[e])]
    acc = {ag: {(w, e): {(v, f) for (v, f) in prod if v in M.access[ag][w] and f in ev_acc[ag][e]}
                for (w, e) in prod} for ag in M.agents}
    val = {(w, e): M.val[w] for (w, e) in prod}
    N = Model(prod, M.agents, acc, val)
    actual = ("p", "read")
    return {"worlds": [f"{w}/{e}" for w, e in prod],
            "a_knows_p": holds(N, actual, K("a", V("p"))),
            "b_knows_p": holds(N, actual, K("b", V("p"))),
            "b_thinks_a_ignorant": holds(N, actual, K("b", Not(K("a", V("p"))))),
            "common_p": holds(N, actual, ("C", ["a", "b"], V("p")))}


# ---------------------------------------------------------------------------
# The wisdom of crowds: the diversity prediction theorem (Page 2007)
# ---------------------------------------------------------------------------
def diversity(guesses, truth) -> dict:
    """(crowd - truth)^2 = mean (guess - truth)^2 - mean (guess - crowd)^2: crowd error = average error - diversity."""
    n = len(guesses)
    c = sum(guesses) / n
    avg_err = sum((g - truth) ** 2 for g in guesses) / n
    div = sum((g - c) ** 2 for g in guesses) / n
    return {"crowd": c, "crowd_error": (c - truth) ** 2, "average_error": avg_err, "diversity": div,
            "identity": abs((c - truth) ** 2 - (avg_err - div)) < 1e-6 * max(1.0, avg_err)}


def ox_guesses(n: int = 800, truth: float = 1198.0, seed: int = 1907) -> list[float]:
    """A toy fair: n guesses at an ox's weight, each with its own bias and noise (not Galton's data, which survive only
    as his summary)."""
    rnd = random.Random(seed)
    out = []
    for _ in range(n):
        bias = rnd.gauss(0, 40)
        out.append(round(truth + bias + rnd.gauss(0, 60)))
    return out


# ---------------------------------------------------------------------------
# Zollman (2007): bandit-playing scientists on networks
# ---------------------------------------------------------------------------
def network(kind: str, n: int) -> dict:
    if kind == "cycle":
        return {i: {(i - 1) % n, (i + 1) % n} for i in range(n)}
    if kind == "wheel":
        g = {i: {(i - 1) % (n - 1), (i + 1) % (n - 1), n - 1} for i in range(n - 1)}
        g[n - 1] = set(range(n - 1))
        return g
    if kind == "complete":
        return {i: set(range(n)) - {i} for i in range(n)}
    raise ValueError(kind)


def _p_better(a, b):
    """Credence that the new method is better (its chance exceeds 0.5) under a Beta(a, b) belief, by the normal
    approximation to the Beta."""
    m = a / (a + b)
    sd = math.sqrt(a * b / ((a + b) ** 2 * (a + b + 1)))
    return 0.5 * (1 + math.erf((m - 0.5) / (sd * math.sqrt(2))))


def zollman_run(kind: str, n: int = 10, eps: float = 0.01, trials: int = 100, rng=None,
                max_rounds: int = 5000) -> tuple[bool, int]:
    """One community. The old method succeeds with known chance 0.5; the new one with unknown chance 0.5 + eps. Each
    scientist holds a Beta belief about the new method's chance, and tests it (``trials`` times a round) only while
    she expects it to beat the old one; everyone updates on her own and her neighbours' results. The run ends when
    nobody tests the new method any more (the community has settled on the worse method), or when every scientist is
    99% sure the new method is better (the right answer). Returns (right?, rounds)."""
    import numpy as np
    rng = rng or np.random.default_rng(0)
    g = network(kind, n)
    p_new = 0.5 + eps
    a = rng.uniform(0, 4, n)
    b = rng.uniform(0, 4, n)
    nbrs = [sorted({i} | g[i]) for i in range(n)]
    for rounds in range(1, max_rounds + 1):
        testers = a / (a + b) > 0.5
        if not testers.any():
            return False, rounds
        if all(_p_better(a[i], b[i]) > 0.99 for i in range(n)):
            return True, rounds
        succ = np.where(testers, rng.binomial(trials, p_new, n), 0)
        tried = np.where(testers, trials, 0)
        da = np.array([succ[nb].sum() for nb in nbrs])
        dt = np.array([tried[nb].sum() for nb in nbrs])
        a = a + da
        b = b + (dt - da)
    return bool((a / (a + b) > 0.5).all()), max_rounds


def zollman(kinds=("cycle", "wheel", "complete"), runs: int = 200, n: int = 10, eps: float = 0.01,
            trials: int = 100, seed: int = 2007) -> dict:
    import numpy as np
    out = {}
    for kind in kinds:
        rng = np.random.default_rng(seed)
        right, times = 0, []
        for _ in range(runs):
            ok, t = zollman_run(kind, n, eps, trials, rng)
            right += ok
            if ok:
                times.append(t)
        out[kind] = {"right": right / runs, "mean_rounds": sum(times) / len(times) if times else math.nan}
    return out


# ---------------------------------------------------------------------------
# The Russian cards problem (Kirkman 1847; van Ditmarsch 2003)
# ---------------------------------------------------------------------------
FANO_HANDS = [(0, 1, 2), (0, 3, 4), (0, 5, 6), (1, 3, 5), (1, 4, 6), (2, 3, 6), (2, 4, 5)]


def russian_cards(announcement=FANO_HANDS, ann=(0, 1, 2)) -> dict:
    """Seven cards 0..6; Ann draws three, Bob three, Cath one; all know this, and each sees only her own hand. Ann
    announces publicly: 'my hand is one of these'. Check, over every deal in which Ann holds a hand in the
    announcement: (1) Bob can tell Ann's hand exactly; (2) Cath learns, of no card other than her own, who holds it.
    Then Bob announces Cath's card, after which Ann knows Bob's hand and Cath still learns nothing."""
    cards = set(range(7))
    deals = []
    for a in announcement:
        rest = cards - set(a)
        for c in rest:
            b = tuple(sorted(rest - {c}))
            deals.append((tuple(a), b, c))
    # Bob, holding b, considers every announced hand disjoint from b
    bob_ok = all(sum(1 for h in announcement if not set(h) & set(b)) == 1 for _, b, _ in deals)
    # Cath, holding c, considers every announced hand avoiding c; for each other card x, both 'Ann has x' and
    # 'Ann lacks x' must remain possible
    cath_ok = True
    for _, _, c in deals:
        hands = [h for h in announcement if c not in h]
        for x in cards - {c}:
            has = any(x in h for h in hands)
            lacks = any(x not in h for h in hands)
            if not (has and lacks):
                cath_ok = False
    # how many deals in all; how many Cath still considers after both announcements (holding card 6 in our deal)
    actual_c = 6 if 6 not in ann else min(cards - set(ann))
    cath_view = [h for h in announcement if actual_c not in h]
    return {"hands": [list(h) for h in announcement], "deals": len(deals), "bob_learns": bob_ok,
            "cath_learns_nothing": cath_ok, "cath_card": actual_c, "cath_view": [list(h) for h in cath_view],
            "all_deals": 140}


def russian_naive(ann=(0, 1, 2)) -> dict:
    """Two failed announcements: Ann says her hand outright (Cath learns everything), or offers just two hands
    (Bob may fail to learn, or Cath may learn a card)."""
    out = {}
    for name, ann_set in (("outright", [ann]), ("two hands", [ann, (3, 4, 5)])):
        r = russian_cards(ann_set, ann)
        out[name] = {"bob_learns": r["bob_learns"], "cath_learns_nothing": r["cath_learns_nothing"]}
    return out


# ---------------------------------------------------------------------------
# Nakamoto (2008): probabilistic finality
# ---------------------------------------------------------------------------
def nakamoto(q: float, z: int) -> float:
    """The chance that an attacker with a fraction q of the hashing power ever catches up from z blocks behind
    (Nakamoto, 'Bitcoin', section 11)."""
    p = 1 - q
    lam = z * (q / p)
    s = 1.0
    for k in range(z + 1):
        poisson = math.exp(-lam) * lam ** k / math.factorial(k)
        s -= poisson * (1 - (q / p) ** (z - k))
    return s


# ---------------------------------------------------------------------------
# Belief rivers: one Zollman run, recorded
# ---------------------------------------------------------------------------
def zollman_trajectory(kind: str, n: int = 10, eps: float = 0.01, trials: int = 100, seed: int = 3,
                       rounds: int = 120) -> list[list[float]]:
    """Each scientist's expected chance for the new method, round by round, in one run."""
    import numpy as np
    rng = np.random.default_rng(seed)
    g = network(kind, n)
    p_new = 0.5 + eps
    a = rng.uniform(0, 4, n)
    b = rng.uniform(0, 4, n)
    nbrs = [sorted({i} | g[i]) for i in range(n)]
    out = [list(a / (a + b))]
    for _ in range(rounds):
        testers = a / (a + b) > 0.5
        succ = np.where(testers, rng.binomial(trials, p_new, n), 0)
        tried = np.where(testers, trials, 0)
        da = np.array([succ[nb].sum() for nb in nbrs])
        dt = np.array([tried[nb].sum() for nb in nbrs])
        a = a + da
        b = b + (dt - da)
        out.append(list(a / (a + b)))
    return out


# ---------------------------------------------------------------------------
# Cheryl's birthday (Singapore and Asian Schools Math Olympiad, 2015)
# ---------------------------------------------------------------------------
CHERYL_DATES = [("May", 15), ("May", 16), ("May", 19), ("June", 17), ("June", 18), ("July", 14), ("July", 16),
                ("August", 14), ("August", 15), ("August", 17)]


def cheryl(dates=CHERYL_DATES) -> dict:
    """Albert is told the month, Bernard the day. Albert: 'I don't know, and I know Bernard doesn't know.'
    Bernard: 'Now I know.' Albert: 'Then I know too.' Each statement is a public announcement; return the dates left
    after each."""
    worlds = list(dates)
    acc = {"A": {w: {v for v in worlds if v[0] == w[0]} for w in worlds},
           "B": {w: {v for v in worlds if v[1] == w[1]} for w in worlds}}
    val = {w: {f"{w[0]}{w[1]}"} for w in worlds}
    M = Model(worlds, ["A", "B"], acc, val)

    def knows_date(i):
        return Or(*[K(i, V(f"{w[0]}{w[1]}")) for w in worlds])
    s1 = And(Not(knows_date("A")), K("A", Not(knows_date("B"))))
    M1 = announce(M, s1)
    M2 = announce(M1, knows_date("B"))
    M3 = announce(M2, knows_date("A"))
    return {"start": [list(w) for w in M.worlds], "after1": [list(w) for w in M1.worlds],
            "after2": [list(w) for w in M2.worlds], "after3": [list(w) for w in M3.worlds]}


# ---------------------------------------------------------------------------
# Common p-belief (Monderer and Samet 1989) in the email game
# ---------------------------------------------------------------------------
def email_beliefs(eps: float = 0.1) -> dict:
    """In the email game, each informed type assigns probability 1/(2 - eps) to the other having one fewer message:
    just over a half, however many messages were sent. So 'the enemy is weak' is never common p-belief for p above
    1 - 1/(2 - eps), however long the exchange, which is why coordination unravels."""
    q = 1 / (2 - eps)
    return {"eps": eps, "p_fewer": q, "max_common_p": 1 - q}
