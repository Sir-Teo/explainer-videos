"""Models of people at a computer (Part 44): pointing as a noisy channel (Fitts's law emerging from corrected
submovements), choice as entropy (Hick–Hyman), the keystroke-level model, and how many users a usability test
needs."""

from __future__ import annotations

import math
import random


def fit_line(xs, ys):
    n = len(xs)
    mx, my = sum(xs) / n, sum(ys) / n
    sxx = sum((x - mx) ** 2 for x in xs)
    sxy = sum((x - mx) * (y - my) for x, y in zip(xs, ys))
    b = sxy / sxx
    a = my - b * mx
    ss_tot = sum((y - my) ** 2 for y in ys)
    ss_res = sum((y - a - b * x) ** 2 for x, y in zip(xs, ys))
    return a, b, 1 - ss_res / ss_tot


# ---------------------------------------------------------------- pointing

def point(D, W, rng, t_sub=0.25, t_react=0.15, noise=0.2):
    """One aimed movement as a sequence of submovements (Crossman and Goodeve; Meyer et al. 1988): each aims at the
    target centre and lands with an error whose spread is proportional to the distance it covers; corrections
    continue until the hand is inside the target.  Returns the time and the number of submovements."""
    x, k = 0.0, 0
    while True:
        k += 1
        d = D - x
        x = x + d + rng.gauss(0, noise * abs(d))
        if abs(D - x) <= W / 2:
            return t_react + k * t_sub + rng.gauss(0, 0.015), k


def fitts_experiment(seed=0, trials=400):
    """A grid of distances and widths; mean movement time against the index of difficulty log2(D/W + 1)."""
    rng = random.Random(seed)
    rows = []
    for D in (64, 128, 256, 512, 1024):
        for W in (8, 16, 32, 64):
            ts = [point(D, W, rng)[0] for _ in range(trials)]
            rows.append({"D": D, "W": W, "ID": math.log2(D / W + 1), "MT": sum(ts) / trials})
    a, b, r2 = fit_line([r["ID"] for r in rows], [r["MT"] for r in rows])
    return {"rows": rows, "a": a, "b": b, "r2": r2, "throughput_bits_per_s": 1 / b}


def edge_target(D=512, W=16, seed=1, trials=2000):
    """A target at the screen edge: the pointer stops at the edge, so overshoot is impossible and the effective
    width along the movement is unbounded."""
    rng = random.Random(seed)
    normal = [point(D, W, rng)[0] for _ in range(trials)]
    edge = []
    for _ in range(trials):
        x, k = 0.0, 0
        while True:
            k += 1
            d = D + 400 - x                     # aim past the edge: it is free
            x = min(D, x + d + rng.gauss(0, 0.2 * abs(d)))
            if x >= D - W:
                break
        edge.append(0.15 + k * 0.25 + rng.gauss(0, 0.015))
    return {"normal": sum(normal) / trials, "edge": sum(edge) / trials}


# ---------------------------------------------------------------- choice

def hick_experiment(seed=2, trials=2000, a=0.20, b=0.15):
    """Choose one of n equally likely lights (or none): a chooser who halves the candidates with each comparison of
    b seconds needs about log2(n + 1) comparisons on average (Hick's n + 1 counts the possibility of no signal).
    With unequal probabilities, a chooser who checks the likely ones first needs about the entropy (Hyman 1953)."""
    rng = random.Random(seed)
    rows = []
    for n in (1, 2, 3, 4, 6, 8, 10):
        ts = []
        for _ in range(trials):
            target = rng.randrange(n + 1)
            lo, hi, steps = 0, n, 0
            while lo < hi:                  # binary search over the n + 1 possibilities
                mid = (lo + hi) // 2
                steps += 1
                if target <= mid:
                    hi = mid
                else:
                    lo = mid + 1
            ts.append(a + b * steps + rng.gauss(0, 0.03))
        rows.append({"n": n, "H": math.log2(n + 1), "RT": sum(ts) / trials})
    A, B, r2 = fit_line([r["H"] for r in rows], [r["RT"] for r in rows])
    skew = [0.7, 0.1, 0.1, 0.05, 0.05]
    H = -sum(p * math.log2(p) for p in skew)
    huff = _huffman_mean(skew)
    return {"rows": rows, "a": A, "b": B, "r2": r2,
            "skewed": {"p": skew, "H": H, "uniform_H": math.log2(5), "questions": huff}}


def _huffman_mean(ps):
    """Mean number of yes/no questions with the best questioning strategy (a Huffman code, AI, Built Part 1)."""
    import heapq
    h = [(p, i, 0.0) for i, p in enumerate(ps)]
    heapq.heapify(h)
    total, k = 0.0, len(ps)
    while len(h) > 1:
        p1, _, _ = heapq.heappop(h)
        p2, _, _ = heapq.heappop(h)
        total += p1 + p2
        heapq.heappush(h, (p1 + p2, k, 0.0))
        k += 1
    return total


# ---------------------------------------------------------------- keystroke-level model

KLM = {"K": 0.28, "P": 1.1, "B": 0.1, "H": 0.4, "M": 1.35}
"""Operator times in seconds from Card, Moran and Newell (1980): K a keystroke (an average typist of 40 words a
minute), P pointing with a mouse, B a button press, H homing between keyboard and mouse, M mental preparation."""


def klm(ops: str) -> float:
    return sum(KLM[c] for c in ops if c in KLM)


def klm_cases():
    cases = {
        "delete a file: menu": "HMPBMPB",          # home to mouse, think, point at file, click, think, menu item
        "delete a file: keyboard shortcut": "MPBHMKK",
        "rename: dialog": "HMPBBMPB" + "MKKKKKKKK" + "K",
        "rename: inline (F2)": "HMPB" + "HMK" + "MKKKKKKKK" + "K",
    }
    return {k: {"ops": v, "seconds": klm(v)} for k, v in cases.items()}


# ---------------------------------------------------------------- how many users?

def nielsen_landauer(L=0.31, n_max=15):
    """Share of problems found by n users if each finds each problem with probability L: 1 - (1 - L)^n."""
    return [{"n": n, "found": 1 - (1 - L) ** n} for n in range(n_max + 1)]


def heterogeneous(n_problems=60, mean=0.31, n_max=15, seed=3, conc=1.2, trials=400):
    """Problems differ in how visible they are: detection probabilities drawn from a Beta distribution with the same
    mean.  The rare, hard-to-find problems pull the curve down."""
    rng = random.Random(seed)
    a = conc
    b = a * (1 - mean) / mean                  # mean a / (a + b) = mean
    curve = [0.0] * (n_max + 1)
    for _ in range(trials):
        ps = [rng.betavariate(a, b) for _ in range(n_problems)]
        for n in range(n_max + 1):
            curve[n] += sum(1 - (1 - p) ** n for p in ps) / n_problems
    return [{"n": n, "found": c / trials} for n, c in enumerate(curve)]
