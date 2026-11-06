"""Induction, made computable (Part 15).

* Laplace's rule of succession and the sunrise problem.
* Dignāga's wheel of reasons (hetucakra): the nine ways a reason can be distributed over similar and dissimilar
  cases, and the two that are good, checked on small universes.
* Hempel's ravens: Bayesian confirmation by a black raven and by a white shoe in a realistic urn model.
* Confirmation measures (difference, ratio, likelihood ratio, Kemeny--Oppenheim, Carnap, Christensen) and some of
  Fitelson's desiderata, checked numerically.
* Grue: one learner, two encodings of the same observations, two projections.
* Popper's verisimilitude: the Miller--Tichý theorem checked over three atoms; Tichý's likeness and Miller's
  translation that reverses it.
* Inference to the best explanation as an update rule (Douven), against conditionalization.
* Merging of opinions: total-variation distance between two Bayesians' predictions, shrinking; and its failure when
  one prior gives zero to the truth.
* Gold (1967): an adversary that defeats any learner on finite languages plus one infinite language; Putnam's
  diagonal argument against any computable predictor.
* Kelly's Ockham efficiency: counting retractions.
* A Solomonoff-style mixture over a toy language of repeating programs; two-part MDL for polynomial degree.
* No free lunch (Wolpert 1996): off-training-set accuracy averaged over all Boolean targets.
* Reichenbach's straight rule; meta-induction as prediction with expert advice (exponential weights), with its
  worst-case regret bound.
"""

from __future__ import annotations

import itertools
import math
import random
from fractions import Fraction

import numpy as np


# ---------------------------------------------------------------------------
# Laplace
# ---------------------------------------------------------------------------
def succession(successes: int, trials: int) -> Fraction:
    """Laplace's rule: with a uniform prior on the chance, P(next success) = (s + 1) / (n + 2)."""
    return Fraction(successes + 1, trials + 2)


def sunrise(years: int = 5000) -> dict:
    """Laplace's own example: the sun has risen every day for about 5,000 years (1,826,213 days)."""
    days = round(years * 365.2426)
    p = succession(days, days)
    return {"days": days, "p_next": float(p), "odds_against": days + 1,
            "p_all_next_n": {n: float(Fraction(days + 1, days + n + 1)) for n in (1, 365, 365 * 5000)}}


def succession_beta(successes: int, trials: int, a: float, b: float) -> float:
    """The same with a Beta(a, b) prior: (s + a) / (n + a + b)."""
    return (successes + a) / (trials + a + b)


# ---------------------------------------------------------------------------
# Dignāga's wheel of reasons
# ---------------------------------------------------------------------------
HETU = ["all", "some", "none"]


def hetucakra() -> list[dict]:
    """For each way the reason (hetu) occurs in similar cases (sapakṣa, where the property holds) and in dissimilar
    cases (vipakṣa, where it does not), build a small universe and ask: does reason -> property hold (no dissimilar
    case has the reason), and is the reason ever found with the property (it is not empty)? Good reasons: both."""
    out = []
    for sim, dis in itertools.product(HETU, HETU):
        cases = []
        # three similar cases (property true) and three dissimilar (property false)
        def pattern(kind):
            return {"all": [True, True, True], "some": [True, False, True], "none": [False, False, False]}[kind]
        for has in pattern(sim):
            cases.append({"property": True, "reason": has})
        for has in pattern(dis):
            cases.append({"property": False, "reason": has})
        no_counter = not any(c["reason"] and not c["property"] for c in cases)
        found = any(c["reason"] and c["property"] for c in cases)
        if no_counter and found:
            verdict = "good"
        elif not found and any(c["reason"] for c in cases):
            verdict = "contradictory"
        else:
            verdict = "inconclusive"
        out.append({"similar": sim, "dissimilar": dis, "verdict": verdict, "no_counterexample": no_counter,
                    "found_with_property": found})
    return out


# ---------------------------------------------------------------------------
# The ravens
# ---------------------------------------------------------------------------
def ravens(n_objects: float = 1e8, n_ravens: float = 1e4, nonblack_frac: float = 0.9, prior_h: float = 0.5,
           alt_white_ravens: int = 100) -> dict:
    """Two hypotheses about the world: H, all ravens are black; H', all but ``alt_white_ravens`` ravens are black.
    Sample (a) a random raven, find it black; (b) a random non-black object, find it is a non-raven (a white shoe).
    Bayes factors and the posterior of H after each (Good; Fitelson and Hawthorne 2010)."""
    nonblack = n_objects * nonblack_frac
    # (a) sample a raven
    lik_a_h, lik_a_alt = 1.0, (n_ravens - alt_white_ravens) / n_ravens
    # (b) sample a non-black object: under H none are ravens; under H', alt_white_ravens of them are
    lik_b_h, lik_b_alt = 1.0, (nonblack - alt_white_ravens) / nonblack

    def post(l1, l2):
        return prior_h * l1 / (prior_h * l1 + (1 - prior_h) * l2)
    pa, pb = post(lik_a_h, lik_a_alt), post(lik_b_h, lik_b_alt)
    return {"bayes_factor_raven": lik_a_h / lik_a_alt, "bayes_factor_shoe": lik_b_h / lik_b_alt,
            "posterior_raven": pa, "posterior_shoe": pb, "rise_raven": pa - prior_h, "rise_shoe": pb - prior_h}


# ---------------------------------------------------------------------------
# Confirmation measures
# ---------------------------------------------------------------------------
def measures(p_h: float, p_e_given_h: float, p_e_given_not_h: float) -> dict:
    p_e = p_h * p_e_given_h + (1 - p_h) * p_e_given_not_h
    p_h_given_e = p_h * p_e_given_h / p_e
    p_h_given_not_e = p_h * (1 - p_e_given_h) / (1 - p_e) if p_e < 1 else p_h
    return {
        "difference": p_h_given_e - p_h,
        "log ratio": math.log(p_h_given_e / p_h),
        "log likelihood ratio": math.log(p_e_given_h / p_e_given_not_h),
        "Kemeny-Oppenheim": (p_e_given_h - p_e_given_not_h) / (p_e_given_h + p_e_given_not_h),
        "Carnap": p_h * p_e_given_h - p_h * p_e,         # P(H & E) - P(H) P(E)
        "Christensen": p_h_given_e - p_h_given_not_e,
    }


def _measures_joint(a: float, b: float, c: float, d: float) -> dict:
    """The six measures from a joint distribution over (H, E): a = P(H E), b = P(H ~E), c = P(~H E), d = P(~H ~E)."""
    p_h, p_e = a + b, a + c
    return measures(p_h, a / p_h, c / (1 - p_h)), p_h, p_e


def desiderata(samples: int = 2000, seed: int = 2002) -> dict:
    """Which measures satisfy which symmetries (Eells and Fitelson 2002), checked on random joint distributions over
    H and E: hypothesis symmetry c(H, E) = -c(~H, E); evidence symmetry c(H, E) = -c(H, ~E); commutativity
    c(H, E) = c(E, H). A measure 'satisfies' a symmetry if it holds on every sample to 1e-9."""
    rng = np.random.default_rng(seed)
    names = ["difference", "log ratio", "log likelihood ratio", "Kemeny-Oppenheim", "Carnap", "Christensen"]
    ok = {n: {"hypothesis symmetry": True, "evidence symmetry": True, "commutativity": True} for n in names}
    for _ in range(samples):
        a, b, c, d = rng.dirichlet([1, 1, 1, 1]) * 0.98 + 0.005
        base, _, _ = _measures_joint(a, b, c, d)
        negh, _, _ = _measures_joint(c, d, a, b)          # swap H and ~H
        nege, _, _ = _measures_joint(b, a, d, c)          # swap E and ~E
        comm, _, _ = _measures_joint(a, c, b, d)          # swap the roles of H and E
        for n in names:
            if abs(base[n] + negh[n]) > 1e-9:
                ok[n]["hypothesis symmetry"] = False
            if abs(base[n] + nege[n]) > 1e-9:
                ok[n]["evidence symmetry"] = False
            if abs(base[n] - comm[n]) > 1e-9:
                ok[n]["commutativity"] = False
    return {"samples": samples, "table": ok}


def ordinal_disagreement() -> dict:
    """Two pieces of evidence that the difference and the log-ratio measures rank oppositely (Fitelson: the choice of
    measure matters). E1 makes a long shot eight times likelier; E2 lifts an even bet by a seventh."""
    s1 = measures(0.01, 0.9, 0.1)
    s2 = measures(0.5, 0.9, 0.5)
    return {"E1": s1, "E2": s2,
            "difference_prefers": "E1" if s1["difference"] > s2["difference"] else "E2",
            "ratio_prefers": "E1" if s1["log ratio"] > s2["log ratio"] else "E2"}


# ---------------------------------------------------------------------------
# Grue
# ---------------------------------------------------------------------------
def grue(T: int = 10, horizon: int = 20, seed: int = 0) -> dict:
    """Emeralds examined at times 0..T-1 are all green. Encode an emerald's colour either as (green/blue) or as
    (grue/bleen), where grue = green if examined before T, else blue. Fit the same learner, logistic regression on
    time, to the observations in each encoding, and project to times T..horizon-1. Then translate both projections
    back into green/blue."""
    rng = np.random.default_rng(seed)
    t = np.arange(T, dtype=float)
    # both encodings of the same observations: every examined emerald is green, and examined before T, so grue
    y_green = np.ones(T)
    y_grue = np.ones(T)

    def fit_predict(y):
        # logistic regression with an intercept and a slope, by gradient descent; all-ones labels drive it to 1
        w = rng.normal(scale=0.01, size=2)
        X = np.stack([np.ones_like(t), t / horizon], axis=1)
        for _ in range(2000):
            p = 1 / (1 + np.exp(-X @ w))
            w -= 0.5 * X.T @ (p - y) / len(y)
        tf = np.arange(T, horizon, dtype=float)
        Xf = np.stack([np.ones_like(tf), tf / horizon], axis=1)
        return 1 / (1 + np.exp(-Xf @ w))
    p_green = fit_predict(y_green)        # probability 'green' after T
    p_grue = fit_predict(y_grue)          # probability 'grue' after T, i.e. 'blue' after T
    return {"T": T, "horizon": horizon, "green_encoding_says_green": float(p_green.mean()),
            "grue_encoding_says_blue": float(p_grue.mean())}


# ---------------------------------------------------------------------------
# Popper's verisimilitude: Miller and Tichý (1974)
# ---------------------------------------------------------------------------
def miller_tichy(n_atoms: int = 3) -> dict:
    """Popper (1963): theory A (a set of worlds, as a bitmask) is closer to the truth than B iff B's true
    consequences are among A's and A's false consequences among B's, at least one inclusion strict. A consequence
    of A is any proposition (set of worlds) containing A; it is true iff it contains the actual world (here, all
    atoms true). Check every ordered pair of distinct theories over ``n_atoms`` atoms: a false theory is never
    closer to the truth than any other theory (Miller 1974, Tichý 1974), while true theories often are."""
    nw = 1 << n_atoms
    actual = nw - 1
    theories = range(1, 1 << nw)
    false = [T for T in theories if not T >> actual & 1]
    true = [T for T in theories if T >> actual & 1]
    props = range(1 << nw)
    tc = {T: {X for X in props if X & T == T and X >> actual & 1} for T in theories}
    fc = {T: {X for X in props if X & T == T and not X >> actual & 1} for T in theories}

    def closer(A, B):
        return tc[B] <= tc[A] and fc[A] <= fc[B] and (tc[B] < tc[A] or fc[A] < fc[B])
    false_closer = sum(closer(A, B) for A in false for B in theories if A != B)
    true_closer = sum(closer(A, B) for A in true for B in true if A != B)
    return {"n_theories": len(theories), "false_theories": len(false), "pairs_checked": len(false) * (len(theories)
            - 1), "false_closer": false_closer, "true_pairs_ordered": true_closer}


def likeness(world: tuple, truth: tuple) -> Fraction:
    """Tichý's likeness for a complete theory: the fraction of atoms it gets wrong (0 = the truth)."""
    return Fraction(sum(a != b for a, b in zip(world, truth)), len(truth))


def miller_language() -> dict:
    """Tichý's weather: hot, rainy, windy, all true. T1 = not hot, rainy, windy; T2 = not hot, not rainy, not windy.
    Miller's translation into hot, Minnesotan (hot iff rainy), Arizonan (hot iff windy) flips the likeness order."""
    truth = (1, 1, 1)
    T1, T2 = (0, 1, 1), (0, 0, 0)

    def tr(w):
        h, r, wd = w
        return (h, int(h == r), int(h == wd))
    return {"truth": truth, "T1": T1, "T2": T2, "d1": str(likeness(T1, truth)), "d2": str(likeness(T2, truth)),
            "truth_m": tr(truth), "T1_m": tr(T1), "T2_m": tr(T2), "d1_m": str(likeness(tr(T1), tr(truth))),
            "d2_m": str(likeness(tr(T2), tr(truth)))}


# ---------------------------------------------------------------------------
# Inference to the best explanation, as an update rule (Douven 2013)
# ---------------------------------------------------------------------------
def explanationist(runs: int = 1000, n: int = 300, truth: int = 7, bonus: float = 0.1, seed: int = 2013) -> dict:
    """Eleven hypotheses about a coin's bias (0, 0.1, ..., 1), uniform prior, true bias ``truth``/10. The Bayesian
    conditionalizes. The explanationist does too, then adds ``bonus`` to the hypothesis that best explains the data
    so far (the bias nearest the observed frequency) and renormalizes. Over ``runs`` sequences of ``n`` tosses: the
    first time each gives the truth probability > 0.9 and > 0.99, the average Brier inaccuracy of the credences over
    the hypotheses, and how often each ever gives probability > 0.9 to a false hypothesis."""
    rng = np.random.default_rng(seed)
    biases = np.arange(11) / 10
    lik1 = np.clip(biases, 1e-12, 1)
    lik0 = np.clip(1 - biases, 1e-12, 1)
    onehot = np.zeros(11)
    onehot[truth] = 1
    stats = {k: {"t90": [], "t99": [], "brier": [], "false90": 0} for k in ("bayes", "ibe")}
    curve = {k: np.zeros(n) for k in ("bayes", "ibe")}
    for _ in range(runs):
        flips = rng.random(n) < biases[truth]
        P = {"bayes": np.full(11, 1 / 11), "ibe": np.full(11, 1 / 11)}
        seen = {k: {"t90": None, "t99": None, "false": False, "brier": 0.0} for k in P}
        heads = 0
        for t in range(n):
            f = flips[t]
            heads += f
            best = int(np.argmin(np.abs(biases - heads / (t + 1))))
            for k in P:
                q = P[k] * (lik1 if f else lik0)
                if k == "ibe":
                    q = q / q.sum()
                    q[best] += bonus
                P[k] = q / q.sum()
                st = seen[k]
                pt = P[k][truth]
                curve[k][t] += pt
                if st["t90"] is None and pt > 0.9:
                    st["t90"] = t + 1
                if st["t99"] is None and pt > 0.99:
                    st["t99"] = t + 1
                if (np.delete(P[k], truth) > 0.9).any():
                    st["false"] = True
                st["brier"] += float(((P[k] - onehot) ** 2).sum())
        for k in P:
            st = seen[k]
            stats[k]["t90"].append(st["t90"] or n)
            stats[k]["t99"].append(st["t99"] or n)
            stats[k]["brier"].append(st["brier"] / n)
            stats[k]["false90"] += st["false"]
    out = {"runs": runs, "n": n, "truth": truth / 10, "bonus": bonus}
    for k in stats:
        out[k] = {"t90": float(np.mean(stats[k]["t90"])), "t99": float(np.mean(stats[k]["t99"])),
                  "brier": float(np.mean(stats[k]["brier"])), "false90": stats[k]["false90"] / runs,
                  "curve": [float(v / runs) for v in curve[k]]}
    return out


# ---------------------------------------------------------------------------
# Merging of opinions
# ---------------------------------------------------------------------------
def merging(n: int = 400, truth: float = 0.7, seed: int = 1962) -> dict:
    """Two Bayesians with Beta(1, 9) and Beta(9, 1) priors on a coin, and a third whose prior gives zero to chances
    above 1/2. Their predictive probabilities for the next toss, and the gap between the first two."""
    rnd = random.Random(seed)
    flips = [1 if rnd.random() < truth else 0 for _ in range(n)]
    grid = np.linspace(0.0005, 0.9995, 1000)
    prior_c = np.where(grid <= 0.5, 1.0, 0.0)
    out = {"a": [], "b": [], "c": [], "gap": []}
    h = 0
    logc = np.log(prior_c + 1e-300)
    for k in range(n + 1):
        pa = (h + 1) / (k + 10)
        pb = (h + 9) / (k + 10)
        w = np.exp(logc - logc.max())
        pc = float((w * grid).sum() / w.sum())
        out["a"].append(pa)
        out["b"].append(pb)
        out["c"].append(pc)
        out["gap"].append(abs(pa - pb))
        if k < n:
            f = flips[k]
            h += f
            logc = logc + (np.log(grid) if f else np.log(1 - grid))
    return {"truth": truth, "n": n, **out}


# ---------------------------------------------------------------------------
# Gold and Putnam
# ---------------------------------------------------------------------------
def gold_adversary(learner, steps: int = 40) -> dict:
    """The class: every finite set of natural numbers, plus N itself. Against any learner (a function from a finite
    sequence of data to a guess: a frozenset, or the string 'N'), build a text, in stages, on which it fails: present
    0, 1, 2, ... until the learner guesses N; then repeat the last number until it guesses the finite set seen so
    far; then continue. If the learner changes its mind forever, the text is for N and it never converges; if it
    stops at a finite set, the text for N defeats it; if it stops at N, a text for a finite set does."""
    data, guesses, mind_changes = [], [], 0
    nxt = 0
    phase = "climb"
    for _ in range(steps):
        if phase == "climb":
            data.append(nxt)
            nxt += 1
        else:
            data.append(data[-1])
        g = learner(tuple(data))
        if guesses and g != guesses[-1]:
            mind_changes += 1
        guesses.append(g)
        if phase == "climb" and g == "N":
            phase = "hold"
        elif phase == "hold" and g == frozenset(data):
            phase = "climb"
    return {"data": data, "guesses": [g if g == "N" else sorted(g) for g in guesses], "mind_changes": mind_changes}


def conservative_learner(n_switch: int = 5):
    """Guesses the finite set seen so far, unless the data have grown for ``n_switch`` new numbers in a row, when it
    guesses N."""
    def learn(seq):
        run = 0
        for i in range(len(seq) - 1, 0, -1):
            if seq[i] > max(seq[:i]):
                run += 1
            else:
                break
        return "N" if run >= n_switch else frozenset(seq)
    return learn


def putnam_diagonal(predictor, n: int = 30) -> dict:
    """Whatever computable predictor of the next bit, the sequence that always does the opposite defeats it every
    time."""
    seq, preds = [], []
    for _ in range(n):
        p = predictor(tuple(seq))
        preds.append(p)
        seq.append(0 if p >= 0.5 else 1)
    wrong = sum((p >= 0.5) != bool(b) for p, b in zip(preds, seq))
    return {"sequence": seq, "predictions": preds, "wrong": wrong, "n": n}


def laplace_predictor(seq):
    return float(succession(sum(seq), len(seq)))


# ---------------------------------------------------------------------------
# Ockham efficiency
# ---------------------------------------------------------------------------
def ockham(horizon: int = 24, patience: int = 3) -> dict:
    """Kelly's game. Nature reveals effects (new particles) one at a time and may withhold the next one as long as
    it likes; a learner must converge to the true count. The Ockham learner conjectures exactly the number seen. A
    bold learner, after ``patience`` quiet steps, anticipates one more; Nature then withholds it until the bold
    learner gives up, and reveals it the moment after. Count retractions: giving up a conjectured count."""
    seen, quiet = 0, 0
    ock, bold, effects = [], [], []
    b = 0
    waiting = False
    for t in range(horizon):
        reveal = False
        if waiting and b == seen:          # the bold learner just gave up its anticipation: now reveal
            reveal = True
            waiting = False
        if reveal:
            seen += 1
            effects.append(t)
            quiet = 0
        else:
            quiet += 1
        # the bold learner
        if b < seen:
            b = seen
        elif b == seen and quiet >= patience:
            b = seen + 1                      # anticipates one more
            quiet = 0
        elif b > seen and quiet >= patience:
            b = seen                          # gives up: a retraction
            quiet = 0
            waiting = True
        ock.append(seen)
        bold.append(b)

    def retractions(xs):
        return sum(1 for x, y in zip(xs, xs[1:]) if y < x)
    return {"effects": effects, "ockham": ock, "bold": bold, "ockham_retractions": retractions(ock),
            "bold_retractions": retractions(bold)}


# ---------------------------------------------------------------------------
# A Solomonoff-style mixture and MDL
# ---------------------------------------------------------------------------
def programs(max_len: int = 8):
    """A toy language: a program is a bit pattern p (length 1..max_len), which outputs p repeated forever. Its prior
    weight is 2^(-2|p|), a prefix-free code for the pattern."""
    for L in range(1, max_len + 1):
        for bits in itertools.product("01", repeat=L):
            yield "".join(bits), 2.0 ** (-2 * L)


def solomonoff(data: str, max_len: int = 8) -> dict:
    """Mixture prediction: P(next = 1 | data) = sum of the weights of programs consistent with data that output 1
    next, over the sum of the weights of all consistent programs."""
    num = den = 0.0
    top = []
    for p, w in programs(max_len):
        out = (p * (len(data) // len(p) + 2))[:len(data) + 1]
        if out[:len(data)] == data:
            den += w
            if out[-1] == "1":
                num += w
            top.append((w, p))
    top.sort(reverse=True)
    return {"p_one": num / den if den else 0.5, "best": [p for _, p in top[:3]], "consistent": len(top)}


def solomonoff_run(target: str = "011", n: int = 18, max_len: int = 8) -> list[dict]:
    seq = (target * (n // len(target) + 2))[:n]
    out = []
    for k in range(n):
        r = solomonoff(seq[:k], max_len)
        out.append({"seen": seq[:k], "p_one": r["p_one"], "next": seq[k], "best": r["best"][0] if r["best"] else ""})
    return out


def mdl_degree(n: int = 30, degree: int = 2, noise: float = 0.3, seed: int = 4, max_deg: int = 8,
               precision: float = 0.01) -> dict:
    """Two-part code length for polynomial fits of each degree, with the data recorded to ``precision``:
    (k + 1)/2 log2 n bits for the k + 1 coefficients, plus the Gaussian code length of the residuals,
    n/2 log2(2 pi e RSS/n) + n log2(1/precision). The minimum is at the true degree."""
    rng = np.random.default_rng(seed)
    x = np.linspace(-1, 1, n)
    y = 1.0 - 2.0 * x + 1.5 * x ** degree + rng.normal(scale=noise, size=n)
    xf = np.linspace(-1, 1, 121)
    rows, fits = [], {}
    for k in range(max_deg + 1):
        coef = np.polyfit(x, y, k)
        rss = float(((np.polyval(coef, x) - y) ** 2).sum())
        model_bits = (k + 1) / 2 * math.log2(n)
        data_bits = n / 2 * math.log2(2 * math.pi * math.e * rss / n) + n * math.log2(1 / precision)
        rows.append({"degree": k, "model_bits": model_bits, "data_bits": data_bits, "total": model_bits + data_bits,
                     "rss": rss})
        fits[str(k)] = [float(v) for v in np.polyval(coef, xf)]
    best = min(rows, key=lambda r: r["total"])["degree"]
    raw = n * math.log2(1 / precision) + n * math.log2(float(y.max() - y.min()))   # each y spelled out in its range
    return {"true_degree": degree, "rows": rows, "best": best, "x": [float(v) for v in x], "y": [float(v) for v in y],
            "xf": [float(v) for v in xf], "fits": fits, "raw_bits": raw, "precision": precision}


# ---------------------------------------------------------------------------
# No free lunch
# ---------------------------------------------------------------------------
def no_free_lunch(n_bits: int = 3, train_size: int = 4) -> dict:
    """All 2^(2^n) Boolean targets on n-bit inputs; a fixed training set (the first ``train_size`` inputs); each
    learner sees the target on the training set and predicts the rest. Average off-training-set accuracy over all
    targets."""
    X = list(itertools.product([0, 1], repeat=n_bits))
    train, test = X[::2][:train_size], [x for x in X if x not in X[::2][:train_size]]

    def hamming(a, b):
        return sum(i != j for i, j in zip(a, b))

    learners = {
        "majority": lambda tr: (lambda x: int(sum(y for _, y in tr) * 2 >= len(tr))),
        "nearest neighbour": lambda tr: (lambda x: min(tr, key=lambda p: (hamming(p[0], x), p[0]))[1]),
        "always 0": lambda tr: (lambda x: 0),
        "anti-majority": lambda tr: (lambda x: 1 - int(sum(y for _, y in tr) * 2 >= len(tr))),
    }
    acc = {k: 0.0 for k in learners}
    targets = list(itertools.product([0, 1], repeat=len(X)))
    for f in targets:
        table = dict(zip(X, f))
        tr = [(x, table[x]) for x in train]
        for name, L in learners.items():
            h = L(tr)
            acc[name] += sum(h(x) == table[x] for x in test) / len(test)
    return {"targets": len(targets), "train": len(train), "test": len(test),
            "accuracy": {k: v / len(targets) for k, v in acc.items()}}


def nfl_slice(labels=(1, 1, 0, 1), n_bits: int = 3) -> dict:
    """The proof of no free lunch, for one training set: fix the labels on the training inputs; the targets that
    agree with them are all 2^|test| completions, and at every test input exactly half of them say 1. So any
    prediction there (here the nearest neighbour's) is right on exactly half of the consistent targets."""
    X = list(itertools.product([0, 1], repeat=n_bits))
    train, test = X[::2], X[1::2]
    tr = list(zip(train, labels))

    def hamming(a, b):
        return sum(i != j for i, j in zip(a, b))
    pred = [min(tr, key=lambda p: (hamming(p[0], x), p[0]))[1] for x in test]
    comps = [list(c) for c in itertools.product([0, 1], repeat=len(test))]
    correct = [sum(c[j] == pred[j] for c in comps) for j in range(len(test))]
    return {"train": ["".join(map(str, x)) for x in train], "labels": list(labels),
            "test": ["".join(map(str, x)) for x in test], "completions": comps, "pred": pred, "correct": correct}


def shattering(max_points: int = 4) -> dict:
    """VC dimension by brute force, for two classes on the line: thresholds (label 1 at x >= a) and intervals
    (label 1 on [a, b]). For k points 0..k-1, count the labellings each class can produce, out of 2^k. A class
    shatters k points if it produces all of them; its VC dimension is the largest such k."""
    out = {}
    for name in ("thresholds", "intervals"):
        rows = []
        for k in range(1, max_points + 1):
            cuts = [c - 0.5 for c in range(k + 1)]
            made = set()
            if name == "thresholds":
                for a in cuts:
                    made.add(tuple(int(x >= a) for x in range(k)))
            else:
                made.add(tuple([0] * k))
                for a in cuts:
                    for b in cuts:
                        if a < b:
                            made.add(tuple(int(a <= x <= b) for x in range(k)))
            missing = [lab for lab in itertools.product([0, 1], repeat=k) if lab not in made]
            rows.append({"k": k, "made": len(made), "all": 2 ** k, "missing": ["".join(map(str, m)) for m in
                                                                             missing[:3]]})
        vc = max(r["k"] for r in rows if r["made"] == r["all"])
        out[name] = {"rows": rows, "vc": vc}
    return out


def smooth_world_lunch(n_bits: int = 3, train_size: int = 4, seed: int = 3) -> dict:
    """Restrict the targets to 'smooth' ones (functions of the first bit only, or constant): now the learners differ."""
    X = list(itertools.product([0, 1], repeat=n_bits))
    train, test = X[::2][:train_size], [x for x in X if x not in X[::2][:train_size]]
    targets = [lambda x: 0, lambda x: 1, lambda x: x[0], lambda x: 1 - x[0]]

    def hamming(a, b):
        return sum(i != j for i, j in zip(a, b))
    learners = {
        "majority": lambda tr: (lambda x: int(sum(y for _, y in tr) * 2 >= len(tr))),
        "nearest neighbour": lambda tr: (lambda x: min(tr, key=lambda p: (hamming(p[0], x), p[0]))[1]),
        "always 0": lambda tr: (lambda x: 0),
        "anti-majority": lambda tr: (lambda x: 1 - int(sum(y for _, y in tr) * 2 >= len(tr))),
    }
    acc = {k: 0.0 for k in learners}
    for f in targets:
        tr = [(x, f(x)) for x in train]
        for name, L in learners.items():
            h = L(tr)
            acc[name] += sum(h(x) == f(x) for x in test) / len(test)
    return {"accuracy": {k: v / len(targets) for k, v in acc.items()}}


# ---------------------------------------------------------------------------
# Reichenbach's straight rule
# ---------------------------------------------------------------------------
def straight_rule(n: int = 2000, p: float = 0.3, seed: int = 1938) -> dict:
    rnd = random.Random(seed)
    s, est = 0, []
    for k in range(1, n + 1):
        s += rnd.random() < p
        est.append(s / k)
    return {"p": p, "estimates": est[::20], "final": est[-1]}


def meta_induction(T: int = 300, seed: int = 2008) -> dict:
    """Schurz's meta-induction as prediction with expert advice (Littlestone and Warmuth; Cesa-Bianchi and Lugosi).
    The world: bits with chance 0.85 of a 1 for the first third, 0.15 for the second, then strict alternation.
    Five object-level methods predict a probability of 1; loss is |p - y|. The exponentially weighted forecaster,
    eta = sqrt(8 ln N / T), is guaranteed for EVERY sequence: loss - best expert's loss <= sqrt(T ln N / 2)."""
    rnd = random.Random(seed)
    ys = []
    for t in range(T):
        if t < T // 3:
            ys.append(int(rnd.random() < 0.85))
        elif t < 2 * T // 3:
            ys.append(int(rnd.random() < 0.15))
        else:
            ys.append(t % 2)
    names = ["always 1", "always 0", "straight rule", "repeat last", "flip last"]

    def preds(t):
        h = ys[:t]
        freq = (sum(h) + 1) / (len(h) + 2)
        last = h[-1] if h else 0.5
        return [1.0, 0.0, freq, float(last), 1 - float(last)]
    N = len(names)
    eta = math.sqrt(8 * math.log(N) / T)
    L = [0.0] * N
    Lf = 0.0
    cum = {n: [] for n in names}
    cum_f, regret = [], []
    for t in range(T):
        p = preds(t)
        w = [math.exp(-eta * (l - min(L))) for l in L]
        pf = sum(wi * pi for wi, pi in zip(w, p)) / sum(w)
        y = ys[t]
        Lf += abs(pf - y)
        for i in range(N):
            L[i] += abs(p[i] - y)
            cum[names[i]].append(L[i])
        cum_f.append(Lf)
        regret.append(Lf - min(L))
    bound = math.sqrt(T * math.log(N) / 2)
    return {"T": T, "names": names, "cum": cum, "forecaster": cum_f, "regret": regret, "bound": bound,
            "final": {n: cum[n][-1] for n in names}, "final_forecaster": Lf, "eta": eta}
