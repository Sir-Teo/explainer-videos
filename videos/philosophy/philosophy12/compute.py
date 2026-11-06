"""Precompute everything in Part 12 of *Philosophy, Built* ("Knowledge Among Many").

    python -m videos.philosophy.philosophy12.compute            # everything missing (about a minute)

Items:
    cards       three cards dealt to Ann, Bob and Cath: six worlds, and what each knows about the others
    muddy       the muddy children: the cube's worlds after each announcement (n = 3); the counts for n = 8
    common      everyone knew 'someone is muddy' before the father spoke; nobody had common knowledge
    attack      the coordinated attack: depth of mutual knowledge after each delivered message; never common
    quorum      majorities of five intersect: all 45 pairs of the 10 three-member quorums share a member
    email       Rubinstein's email game: 'attack when informed' unravels, type by type, to 'never attack'
    agree       Geanakoplos and Polemarchakis: two posteriors announced in turn until they agree
    private     a private announcement as a product update
    moore       'p, but you don't know p': true before it is announced, false after
    fitch       K(p and not Kp) is unsatisfiable on reflexive frames, satisfiable without reflexivity
    fitchprice  Fitch's paradox as a Price List
    miracles    Hume on miracles, by Bayes's theorem
    peers       the restaurant bill: a Bayesian peer's disagreement, and an absurd answer
    crowds      the diversity prediction theorem on a toy fair, with and without a shared bias
    zollman     bandit-playing scientists on a cycle, a wheel and a complete network
"""

from __future__ import annotations

import itertools
from fractions import Fraction

from explainer.ai.cache import Cache
from explainer.philosophy.reasoner import epistemic as Ep
from explainer.philosophy.reasoner import prop

CACHE = Cache("philosophy12")
load = CACHE.load

FITCH = [("F1", r"every truth can be known", "a"),
         ("F2", r"some truth is not known by anyone", "b"),
         ("F3", r"knowledge is factive \ and distributes over `and' \ (classical logic)", "c")]


def compute_cards() -> dict:
    agents = ["a", "b", "c"]
    worlds = list(itertools.permutations([0, 1, 2]))
    acc = {ag: {w: {v for v in worlds if v[i] == w[i]} for w in worlds} for i, ag in enumerate(agents)}
    val = {w: {f"{ag}{w[i]}" for i, ag in enumerate(agents)} for w in worlds}
    M = Ep.Model(worlds, agents, acc, val)
    actual = (0, 1, 2)
    V, K, Not = Ep.V, Ep.K, Ep.Not
    checks = [
        (r"K_a\, a_0", K("a", V("a0"))),
        (r"K_a\, b_1", K("a", V("b1"))),
        (r"K_a\, \lnot b_0", K("a", Not(V("b0")))),
        (r"K_a (b_1 \lor c_1)", K("a", Ep.Or(V("b1"), V("c1")))),
        (r"K_b K_a\, \lnot a_1", K("b", K("a", Not(V("a1"))))),
        (r"K_b (K_a b_1 \lor K_a \lnot b_1)", K("b", Ep.Or(K("a", V("b1")), K("a", Not(V("b1")))))),
    ]
    after = Ep.announce(M, V("a0"))
    post = {"b_knows_c2": Ep.holds(after, actual, K("b", V("c2"))),
            "c_knows_b1": Ep.holds(after, actual, K("c", V("b1"))),
            "common_a0": Ep.holds(after, actual, ("C", agents, V("a0"))),
            "left": [list(w) for w in after.worlds]}
    return {"worlds": [list(w) for w in worlds], "actual": list(actual), "after_a0": post,
            "edges": {ag: [[list(u), list(v)] for u, v in sorted({tuple(sorted((u, v))) for u in worlds
                                                                     for v in acc[ag][u] if u != v})]
                      for ag in agents},
            "checks": [{"tex": t, "value": Ep.holds(M, actual, f)} for t, f in checks]}


def compute_muddy() -> dict:
    n8 = Ep.muddy_rounds(8, (1, 1, 1, 0, 0, 1, 0, 1))
    return {"cube": Ep.muddy_cube_rounds(3), "n3": Ep.muddy_rounds(3, (1, 1, 0)), "n8": n8,
            "n8_actual": [1, 1, 1, 0, 0, 1, 0, 1], "no_father": Ep.without_father(3)}


def compute_common() -> dict:
    out = {}
    for actual in [(1, 0, 0), (1, 1, 0), (1, 1, 1)]:
        M = Ep.muddy(3)
        s = Ep.Or(*[Ep.V(f"m{i}") for i in range(3)])
        out["".join(map(str, actual))] = {
            "depth": Ep.mutual_depth(M, actual, s, [0, 1, 2]), **Ep.everyone_knew_already(3, actual)}
    return out


def compute_attack() -> dict:
    return {"rows": Ep.attack_depth(6)}


def compute_quorum() -> dict:
    qs = list(itertools.combinations(range(5), 3))
    pairs = list(itertools.combinations(qs, 2))
    return {"quorums": len(qs), "pairs": len(pairs), "intersecting": sum(1 for a, b in pairs if set(a) & set(b))}


def compute_email() -> dict:
    # a long chain (types up to 40), shown for types 0..8, so that the truncation at the top never shows
    r = Ep.email_game(eps=0.1, p=0.25, M_=2.0, L=4.0, T=40)
    window = [[[t for t in a if t <= 8], [t for t in b if t <= 8]] for a, b in r["history"][:9]]
    return {"history": window, "final": r["final"], "eps": 0.1, "steps": len(r["history"])}


def compute_agree() -> dict:
    g = Ep.GP_EXAMPLE
    d = Ep.agreement_dialogue(g["states"], g["prior"], g["A"], g["B"], g["event"], g["actual"])
    return {"dialogue": [{"speaker": r["speaker"], "says": str(r["says"]), "A": str(r["A"]), "B": str(r["B"])}
                         for r in d],
            "A": [sorted(c) for c in g["A"]], "B": [sorted(c) for c in g["B"]], "event": sorted(g["event"]),
            "actual": g["actual"]}


def compute_private() -> dict:
    return Ep.private_update()


def compute_moore() -> dict:
    return Ep.moore_update()


def compute_fitch() -> dict:
    return Ep.fitch_check()


def compute_fitchprice() -> dict:
    claims = {k: prop.parse(f) for k, _, f in FITCH}
    res = prop.mus_mcs(claims, [prop.parse("(a & b & c) -> F"), prop.parse("~F")])
    return {"claims": [{"key": k, "text": t} for k, t, _ in FITCH], "mus": [sorted(x) for x in res["mus"]],
            "mcs": [sorted(x) for x in res["mcs"]]}


def compute_miracles() -> dict:
    """A witness who is right 99 times in 100 reports a miracle whose prior chance is one in a million."""
    out = []
    for prior, rel in [(Fraction(1, 10 ** 6), Fraction(99, 100)), (Fraction(1, 10 ** 6), Fraction(999999, 10 ** 6)),
                       (Fraction(1, 10 ** 6), Fraction(9999999, 10 ** 7))]:
        post = prior * rel / (prior * rel + (1 - prior) * (1 - rel))
        out.append({"prior": float(prior), "reliability": float(rel), "posterior": float(post)})
    return {"rows": out}


def compute_peers() -> dict:
    """Two diners split a bill; each gets the right share with chance 0.9, and two wrong answers almost never
    coincide. Given that they disagree, how likely is it that I am right?"""
    r = Fraction(9, 10)
    me_right = r * (1 - r)
    peer_right = (1 - r) * r
    both_wrong = (1 - r) * (1 - r)
    p = me_right / (me_right + peer_right + both_wrong)
    return {"reliability": float(r), "me_right": float(me_right), "peer_right": float(peer_right),
            "both_wrong": float(both_wrong), "posterior": float(p)}


def compute_crowds() -> dict:
    g = Ep.ox_guesses()
    d = Ep.diversity(g, 1198)
    import random
    rnd = random.Random(12)
    shared = [x + 60 for x in g]          # everyone at this fair shares a bias of +60 lb
    d2 = Ep.diversity(shared, 1198)
    hist = {}
    for x in g:
        b = int((x - 900) // 25)
        hist[b] = hist.get(b, 0) + 1
    del rnd
    return {"n": len(g), "plain": d, "shared": d2, "hist": sorted(hist.items()), "truth": 1198}


def compute_zollman() -> dict:
    return Ep.zollman(runs=500, n=10, eps=0.01, trials=100, seed=2007)


def compute_russian() -> dict:
    return {**Ep.russian_cards(), "naive": Ep.russian_naive()}


def compute_nakamoto() -> dict:
    return {"q": [0.1, 0.3], "rows": [{"z": z, "p10": Ep.nakamoto(0.1, z), "p30": Ep.nakamoto(0.3, z)}
                                     for z in (0, 1, 2, 4, 6, 10)]}


def compute_rivers() -> dict:
    return {"complete": Ep.zollman_trajectory("complete", seed=8, rounds=100),
            "cycle": Ep.zollman_trajectory("cycle", seed=8, rounds=100), "seed": 8}


def compute_cheryl() -> dict:
    return Ep.cheryl()


def compute_beliefs() -> dict:
    return Ep.email_beliefs(0.1)


ITEMS = {"cheryl": compute_cheryl, "beliefs": compute_beliefs, "cards": compute_cards, "russian": compute_russian, "nakamoto": compute_nakamoto, "rivers": compute_rivers, "muddy": compute_muddy, "common": compute_common, "attack": compute_attack,
         "quorum": compute_quorum, "email": compute_email, "agree": compute_agree, "private": compute_private,
         "moore": compute_moore, "fitch": compute_fitch, "fitchprice": compute_fitchprice,
         "miracles": compute_miracles, "peers": compute_peers, "crowds": compute_crowds,
         "zollman": compute_zollman}

if __name__ == "__main__":
    CACHE.main(ITEMS, __doc__)
