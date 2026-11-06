"""Byzantine agreement and Nakamoto consensus (Part 38).

    om(n, m, commander_value, traitors, strategy)   Lamport, Shostak and Pease's oral-messages algorithm OM(m): the
        value each loyal lieutenant decides, given which generals are traitors and how they lie
    om_exhaustive(n, m, traitors)   every lying strategy of the traitors (each relayed message chosen freely): does
        every loyal lieutenant always agree, and follow a loyal commander?
    bft_messages(n, protocol)       messages per decision: OM(m), PBFT's three phases, HotStuff's linear phases
    rosenfeld(q, z)                 the exact value, which Nakamoto's Poisson approximation underestimates
    nakamoto_p(q, z)                Nakamoto's 2008 probability that an attacker with hash share q ever catches up
        from z blocks behind; ``double_spend_mc`` the same by simulation
    selfish(alpha, gamma)           Eyal and Sirer's selfish-mining revenue, by formula and by simulation
"""
from __future__ import annotations

import itertools
import math
import random
from collections import Counter


def _majority(vals, default=0):
    c = Counter(vals).most_common()
    if not c:
        return default
    if len(c) > 1 and c[0][1] == c[1][1]:
        return default
    return c[0][0]


def om(n: int, m: int, value, traitors=frozenset(), lie=None, commander: int = 0, path=()):
    """Returns {lieutenant: decided value} for OM(m) with the given commander and lieutenants range(n) minus
    commander.  ``lie(path, sender, receiver, true_value)`` gives what a traitor sends."""
    lie = lie or (lambda path, s, r, v: 1 - v if isinstance(v, int) else v)
    generals = [g for g in range(n) if g != commander and g not in path]
    sent = {}
    for g in generals:
        v = value
        if commander in traitors:
            v = lie(path + (commander,), commander, g, value)
        sent[g] = v
    if m == 0:
        return sent
    decided = {}
    sub = {}
    for g in generals:
        # g acts as commander of OM(m - 1), relaying what it received to the others
        sub[g] = om(n, m - 1, sent[g], traitors, lie, commander=g, path=path + (commander,))
    for g in generals:
        vals = [sent[g]] + [sub[h][g] for h in generals if h != g]
        decided[g] = _majority(vals)
    return decided


def om_exhaustive(n: int, m: int, traitors, value: int = 1, limit: int = 200000):
    """Enumerate every assignment of lies: each message a traitor sends (identified by path and receiver) is 0 or
    1.  Agreement: all loyal lieutenants decide the same; validity: if the commander is loyal, they decide its
    value."""
    traitors = frozenset(traitors)
    # collect the message slots traitors control by a dry run
    slots = []

    def record(path, s, r, v):
        slots.append((path, s, r))
        return v

    om(n, m, value, traitors, record)
    slots = sorted(set(slots))
    bad = None
    tried = 0
    for bits in itertools.product((0, 1), repeat=len(slots)):
        tried += 1
        if tried > limit:
            break
        table = dict(zip(slots, bits))
        res = om(n, m, value, traitors, lambda path, s, r, v: table[(path, s, r)])
        loyal = {g: v for g, v in res.items() if g not in traitors}
        ok = len(set(loyal.values())) <= 1 and (0 in traitors or all(v == value for v in loyal.values()))
        if not ok:
            bad = {"lies": {f"{''.join(map(str, p))}:{s}->{r}": b for (p, s, r), b in table.items()},
                   "decisions": loyal}
            break
    return {"n": n, "m": m, "traitors": sorted(traitors), "slots": len(slots), "strategies": tried,
            "always_agree": bad is None, "counterexample": bad}


def bft_messages(n: int, protocol: str) -> int:
    f = (n - 1) // 3
    if protocol == "om":
        # OM(f): (n-1) + (n-1)(n-2) + ... , f + 1 levels
        total = 0
        prod = 1
        for lvl in range(f + 1):
            prod *= (n - 1 - lvl)
            total += prod
        return total
    if protocol == "pbft":
        return (n - 1) + (n - 1) * (n - 1) + n * (n - 1)       # pre-prepare, prepare, commit
    if protocol == "hotstuff":
        return 3 * 2 * (n - 1)                                 # three phases, leader to all and back
    raise ValueError(protocol)


def nakamoto_p(q: float, z: int) -> float:
    """The calculation in section 11 of the Bitcoin paper."""
    p = 1 - q
    lam = z * q / p
    s = 1.0
    for k in range(z + 1):
        poisson = math.exp(-lam) * lam ** k / math.factorial(k)
        s -= poisson * (1 - (q / p) ** (z - k))
    return s


def rosenfeld(q: float, z: int) -> float:
    """The exact probability (Rosenfeld 2014; Grunspan and Perez-Marco 2017): the attacker's blocks while the
    merchant waits for z are negative-binomial, not Poisson."""
    p = 1 - q
    if z == 0:
        return 1.0
    return 1 - sum(math.comb(m + z - 1, m) * (p ** z * q ** m - q ** z * p ** m) for m in range(z + 1))


def double_spend_mc(q: float, z: int, trials: int = 20000, seed: int = 0, horizon: int = 400) -> float:
    """The attacker mines in secret while the merchant waits for z confirmations; afterwards it wins if it ever
    gets ahead.  (Blocks are a race: each next block is the attacker's with probability q.)"""
    rng = random.Random(seed)
    wins = 0
    for _ in range(trials):
        honest = attacker = 0
        while honest < z:                                     # until the merchant sees z confirmations
            if rng.random() < q:
                attacker += 1
            else:
                honest += 1
        lead = attacker - honest                              # attacker relative position
        steps = 0
        while lead < 0 and steps < horizon and lead > -60:   # Nakamoto's criterion: the attacker draws level
            lead += 1 if rng.random() < q else -1
            steps += 1
        if lead >= 0:
            wins += 1
    return wins / trials


def selfish(alpha: float, gamma: float = 0.0, blocks: int = 200000, seed: int = 0):
    """Eyal and Sirer (2014): the pool's share of the main chain when it withholds blocks, against its share
    alpha of the hash power; gamma is the share of honest miners who build on the pool's block in a tie."""
    a, g = alpha, gamma
    formula = (a * (1 - a) ** 2 * (4 * a + g * (1 - 2 * a)) - a ** 3) / (1 - a * (1 + (2 - a) * a))
    rng = random.Random(seed)
    pool = honest = 0
    private = 0          # the pool's lead
    tie = False
    for _ in range(blocks):
        if rng.random() < a:                                  # the pool finds a block
            if tie:
                pool += 2
                tie = False
                private = 0
            else:
                private += 1
        else:                                                 # honest miners find a block
            if tie:
                if rng.random() < g:
                    pool += 1
                    honest += 1
                else:
                    honest += 2
                tie = False
                private = 0
            elif private == 0:
                honest += 1
            elif private == 1:
                tie = True                                    # the pool publishes: a race
                private = 0
            elif private == 2:
                pool += 2
                private = 0
            else:
                pool += 1
                private -= 1
    return {"alpha": a, "gamma": g, "formula": formula, "simulated": pool / (pool + honest)}
