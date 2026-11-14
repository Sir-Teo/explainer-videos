"""Precompute everything numerical, and every sound, in Part 16 of *Music, Built* ("Two Voices").

    python -m videos.music.music16.compute              # everything missing (about a minute)
    python -m videos.music.music16.compute --force species

Numbers are cached in ``.cache/music16/<name>.json`` (+ ``.npz``), sounds in ``.cache/music16/audio/``.  The
counterpoint module is Monochord's (``explainer/music/monochord/counterpoint.py``); published findings are cited in
the README.

Items:
    hook        the Tune with a second voice a fifth below it, and with a counterpoint above it
    organum     parallel organum at the fifth, and with octave doublings, as in the ninth century
    fusion      how strongly each interval fuses into one pitch (Part 4's ear model); one to name by ear
    motions     the four kinds of motion, heard; how often each occurs
    onsets      two notes starting together, and thirty milliseconds apart
    fux         Fux's cantus firmus; the best first-species line over it; the rules
    counting    how many lines obey the rules, as the rules are added; over the Tune
    damage      each rule removed: how many more lines, and what goes wrong in them
    species     species two to five over Fux's cantus
    independence  how independent the voices are, from organum to the fifth species
    tune        Variation 16: the Tune as a cantus firmus, in organum and then through the five species
    variation   the Variations ledger, row 16
    more        organum's three stages, heard; counting by hand on a five-note cantus; a line below the cantus; how
                much delay separates two notes; an ear question on suspensions
"""

from __future__ import annotations

import numpy as np

from explainer.ai.cache import Cache
from explainer.music.monochord import EXAMPLE_LEVEL, SR, Clip, ClipStore, concat, mix
from explainer.music.monochord import consonance as CONS
from explainer.music.monochord import counterpoint as K
from explainer.music.monochord import melody as M
from explainer.music.monochord.instruments import strings as STR
from explainer.music.monochord.partkit import organ_tone, saver
from explainer.music.monochord.physics.string import String

CACHE = Cache("music16")
CLIPS = ClipStore("music16")
load = CACHE.load

LEVEL = EXAMPLE_LEVEL - 2.5
save = saver(CLIPS, LEVEL, kind="physical model")
C4 = 261.6255653005986
BOARD = STR.soundboard()
_NOTES: dict = {}
TUNE = [60 + p for p in M.corpus()[0].pitches]
CF = K.FUX_DORIAN


def clip(y, fade=(0.001, 0.05)) -> Clip:
    return Clip(np.asarray(y, dtype=np.float64)).fade(*fade)


def hz(m: float) -> float:
    return 440.0 * 2.0 ** ((m - 69) / 12.0)


def piano(m: float, seconds: float) -> Clip:
    key = (round(m, 3), round(seconds, 3))
    if key not in _NOTES:
        f = hz(m)
        y = BOARD.play(STR.struck(String.tuned(f, L=0.62 * (C4 / f) ** 0.8, mu=6.34e-3, kappa=1.25, sigma0=0.6, sigma1=3.3e-4), velocity=1.6, seconds=seconds + 0.25))
        _NOTES[key] = clip(y, (0.001, 0.18)).at_level(LEVEL)
    return _NOTES[key]


def organ(m: float, seconds: float) -> Clip:
    return clip(organ_tone(hz(m), seconds, partials=6, rolloff=0.7), (0.03, 0.08)).at_level(LEVEL)


def voices(parts, beat: float, voice=piano, gains=None, tail: float = 1.2, delays=None) -> Clip:
    """Several voices, each a list of (pitch, start beat, beats) events, played together.  Events: ``v{j}n{k}``."""
    placed, ev, end = [], {}, 0.0
    for j, part in enumerate(parts):
        g = 0.0 if gains is None else gains[j]
        dl = 0.0 if delays is None else delays[j]
        for k, (p, a, d) in enumerate(part):
            t = a * beat + dl
            placed.append((voice(p, d * beat), t, g))
            ev[f"v{j}n{k}"] = t
            end = max(end, t + d * beat)
    ev["end"] = end
    return Clip(mix(placed, duration=end + tail).y, SR, ev, [])


def bars(notes, beats: float = 4.0) -> list[tuple[int, float, float]]:
    return [(p, beats * k, beats) for k, p in enumerate(notes)]


def evrows(events) -> list[list[float]]:
    return [[int(p), float(a), float(d)] for p, a, d in events]


def times(c: Clip, j: int, n: int, prefix: str = "") -> list[float]:
    return [float(c.events[f"{prefix}v{j}n{k}"]) for k in range(n)]


TUNE_BEATS = [b for b in M.corpus()[0].beats]


def tune_events(notes, beats=None):
    beats = TUNE_BEATS[: len(notes)] if beats is None else beats
    out, t = [], 0.0
    for p, b in zip(notes, beats):
        out.append((p, t, b))
        t += b
    return out


# ---------------------------------------------------------------------------
def compute_hook() -> dict:
    ph = TUNE[:14]
    top = tune_events(ph)
    org = tune_events(K.organum(ph, -7))
    cp = K.best(ph, tries=1500, seed=3)                       # a first-species line above the Tune's two phrases
    cpe = tune_events(cp)
    a = voices([top, org], beat=0.5)
    b = voices([cpe, top], beat=0.5)
    seq = concat([a.at_level(LEVEL), b.at_level(LEVEL)], gap=1.0, names=["organum", "counterpoint"])
    ia = K.independence(top, org)
    ib = K.independence(cpe, top)
    return {"tune": ph, "organum": K.organum(ph, -7), "counterpoint": cp, "beats": TUNE_BEATS[:14],
            "times": {"organum": [times(seq, 0, 14, "organum."), times(seq, 1, 14, "organum.")], "counterpoint": [times(seq, 0, 14, "counterpoint."), times(seq, 1, 14, "counterpoint.")]},
            "starts": {"organum": float(seq.events["organum"]), "counterpoint": float(seq.events["counterpoint"])},
            "independence": {"organum": ia, "counterpoint": ib}, "violations": K.check(ph, cp),
            "clips": {"two": save("hook.two", seq, level=None, detail="the Tune with a voice a fifth below it; then with a counterpoint above it")}}


def compute_organum() -> dict:
    ph = TUNE[:7]
    top = tune_events(ph)
    fifth = tune_events(K.organum(ph, -7))
    plain = voices([top, fifth], beat=0.6, voice=organ)
    composite = voices([tune_events([p + 12 for p in ph]), top, fifth, tune_events(K.organum(ph, -19))], beat=0.6, voice=organ, gains=[-6.0, 0.0, 0.0, -4.0])
    seq = concat([organ(60, 0.01).gain(-60), plain.at_level(LEVEL), composite.at_level(LEVEL)], gap=0.9, names=["x", "simple", "composite"])
    return {"tune": ph, "fifth": K.organum(ph, -7), "composite": [[p + 12 for p in ph], ph, K.organum(ph, -7), K.organum(ph, -19)], "beats": TUNE_BEATS[:7],
            "times": {"simple": times(seq, 0, 7, "simple."), "composite": times(seq, 1, 7, "composite.")}, "starts": {k: float(seq.events[k]) for k in ("simple", "composite")},
            "clips": {"organum": save("organum.two", seq, level=None, kind="synthesized", detail="the Tune in parallel fifths; then doubled at the octave above and below: organ tones")}}


def compute_fusion() -> dict:
    names = ["unison", "m2", "M2", "m3", "M3", "P4", "tritone", "P5", "m6", "M6", "m7", "M7", "octave"]
    full = ["unison", "minor second", "major second", "minor third", "major third", "fourth", "tritone", "fifth", "minor sixth", "major sixth",
            "minor seventh", "major seventh", "octave"]
    # of the upper note's harmonics, the share that are also harmonics of the lower note: 1/q for the just ratio p:q
    ratios = [CONS.JUST[n] for n in full]
    strength = [1.0 / q for p_, q in ratios]
    # an ear question: a phrase in parallel octaves, and in parallel thirds below (diatonic)
    ph = TUNE[:7]
    third = []
    for p in ph:
        q = p - 3
        while q % 12 not in K.WHITE:
            q -= 1
        q = p - 4 if (p - 4) % 12 in K.WHITE and (p - 4) % 12 != (p - 3) % 12 and (p % 12) in (0, 5, 7) else q
        third.append(q)
    third = []
    for p in ph:                                                   # the white key two letters below: a third
        third.append(K._step(p, -2))
    A = voices([tune_events(ph), tune_events([p - 12 for p in ph])], beat=0.5, voice=organ)
    B = voices([tune_events(ph), tune_events(third)], beat=0.5, voice=organ)
    q = concat([A.at_level(LEVEL), B.at_level(LEVEL)], gap=0.9, names=["A", "B"])
    return {"names": names, "strength": strength, "ratios": [list(r) for r in ratios], "quiz": {"A": "octaves", "B": "thirds", "answer": "B", "third": third},
            "times": {"A": times(q, 0, 7, "A."), "B": times(q, 0, 7, "B.")}, "starts": {k: float(q.events[k]) for k in "AB"},
            "clips": {"quiz": save("fusion.quiz", q, level=None, kind="synthesized", detail="one phrase doubled two ways: organ tones")}}


def compute_motions() -> dict:
    demos = {"parallel": [(64, 60), (67, 64), (69, 65), (72, 69)], "similar": [(67, 60), (72, 62), (74, 67), (77, 69)],
             "contrary": [(64, 60), (62, 59), (60, 57), (59, 55)], "oblique": [(64, 60), (65, 60), (67, 60), (69, 60)]}
    parts = []
    for name, pairs in demos.items():
        up = [(u, 2.0 * k, 2.0) for k, (u, l) in enumerate(pairs)]
        lo = [(l, 2.0 * k, 2.0) for k, (u, l) in enumerate(pairs)]
        parts.append(voices([up, lo], beat=0.45).at_level(LEVEL))
    seq = concat(parts, gap=0.7, names=list(demos))
    best = K.best(CF, tries=2000)
    ind_best = K.independence(*K.first_species_events(CF, best))
    rng = np.random.default_rng(5)
    lines = [K.sample(CF, rng=rng) for _ in range(400)]
    ind_all = {k: float(np.mean([K.independence(*K.first_species_events(CF, l))[k] for l in lines])) for k in ("parallel", "similar", "contrary", "oblique")}
    # notes drawn with no rules at all over the same cantus (consonant only)
    rand = [K.sample(CF, rules=("consonance", "spacing"), rng=rng) for _ in range(400)]
    ind_rand = {k: float(np.mean([K.independence(*K.first_species_events(CF, l))[k] for l in rand])) for k in ("parallel", "similar", "contrary", "oblique")}
    return {"demos": {k: [list(x) for x in v] for k, v in demos.items()}, "starts": {k: float(seq.events[k]) for k in demos},
            "times": {k: times(seq, 0, 4, f"{k}.") for k in demos}, "valid": ind_all, "consonant_only": ind_rand, "best": ind_best,
            "clips": {"four": save("motions.four", seq, level=None, detail="parallel, similar, contrary and oblique motion: Part 7's piano")}}


def compute_onsets() -> dict:
    together = voices([[(72, 0.0, 4.0)], [(60, 0.0, 4.0)]], beat=0.5, voice=organ, tail=0.4)
    apart = voices([[(72, 0.0, 4.0)], [(60, 0.0, 4.0)]], beat=0.5, voice=organ, tail=0.4, delays=[0.035, 0.0])
    q = concat([together.at_level(LEVEL), apart.at_level(LEVEL)], gap=1.0, names=["A", "B"])
    # in the species, how many notes begin with a note of the other voice
    rng = np.random.default_rng(9)
    shares = {}
    for n in (1, 2, 3, 4, 5):
        line = K.species(CF, n, rng, tries=60)
        shares[str(n)] = K.independence(line, K.first_species_events(CF, [0] * len(CF))[1])["together"]
    return {"starts": {k: float(q.events[k]) for k in "AB"}, "delay_ms": 35, "answer": "B", "together_by_species": shares,
            "clips": {"quiz": save("onsets.quiz", q, level=None, kind="synthesized", detail="an octave, its notes starting together; then the upper 35 ms late")}}


def compute_fux() -> dict:
    best = K.best(CF, tries=3000)
    cf_ev, cp_ev = bars(CF), bars(best)
    alone = voices([cf_ev], beat=0.3)
    both = voices([cp_ev, cf_ev], beat=0.3)
    seq = concat([alone.at_level(LEVEL), both.at_level(LEVEL)], gap=1.0, names=["cf", "both"])
    vert = [int(c - k) for c, k in zip(best, CF)]
    return {"cf": CF, "best": best, "verticals": vert, "motions": [K.motion(a0, a1, b0, b1) for a0, a1, b0, b1 in zip(best, best[1:], CF, CF[1:])],
            "rules": [{"name": r, "text": K.NAMES[r], "why": K.PRINCIPLE[r]} for r in K.RULES], "score": K.score(CF, best),
            "times": {"cf": times(seq, 0, len(CF), "cf."), "both": [times(seq, 0, len(CF), "both."), times(seq, 1, len(CF), "both.")]},
            "starts": {k: float(seq.events[k]) for k in ("cf", "both")},
            "clips": {"exercise": save("fux.exercise", seq, level=None, detail="Fux's cantus firmus alone; then with a first-species line above it")}}


ORDER = ["consonance", "start", "cadence", "unison", "spacing", "melodic", "repeat", "recovery", "direct", "parallel", "run", "climax"]


def compute_counting() -> dict:
    f = K.funnel(CF, ORDER)
    total = f[0][1]
    tune_all = K.count(TUNE)
    tune_seq = int(np.prod([len(c) for c in K.candidates(TUNE)], dtype=object))
    years = tune_all * 42 * 1.2 / (3600 * 24 * 365.25)
    return {"funnel": [[n, int(c)] for n, c in f], "total": int(total), "valid": int(f[-1][1]), "tune_count": int(tune_all), "tune_sequences": str(tune_seq),
            "tune_digits": len(str(tune_seq)), "years": float(years), "fraction": f[-1][1] / total}


def lines_measure(lines) -> dict:
    """Damage, measured on lines sampled uniformly: fused moments, dissonant verticals, mean move, leaps over a
    fifth, voice crossings."""
    out = {"fused": [], "dissonant": [], "move": [], "big": [], "unison": []}
    for l in lines:
        ind = K.independence(*K.first_species_events(CF, l))
        out["fused"].append(ind["fused"])
        v = [(a - c) for a, c in zip(l, CF)]
        out["dissonant"].append(np.mean([x % 12 not in K.CONSONANT for x in v]))
        mv = [abs(b - a) for a, b in zip(l, l[1:])]
        out["move"].append(np.mean(mv))
        out["big"].append(np.mean([m > 7 for m in mv]))
        out["unison"].append(np.mean([x == 0 for x in v[1:-1]]))
    return {k: float(np.mean(v)) for k, v in out.items()}


def compute_damage() -> dict:
    rng = np.random.default_rng(11)
    full = K.count(CF)
    base = lines_measure([K.sample(CF, rng=rng) for _ in range(300)])
    rows = []
    for r in K.RULES:
        rest = tuple(x for x in K.RULES if x != r)
        n = K.count(CF, rest)
        m = lines_measure([K.sample(CF, rest, rng=rng) for _ in range(300)])
        rows.append({"rule": r, "text": K.NAMES[r], "count": int(n), "factor": n / full, **m})
    # two lines that break one rule each, heard against the cantus
    def breaking(rule, want):
        rest = tuple(x for x in K.RULES if x != rule)
        for _ in range(4000):
            l = K.sample(CF, rest, rng=rng)
            if want(l):
                return l
        return None

    def has_direct(l):
        return any((a - c) % 12 in (0, 7) and K.motion(p, a, pc, c) in ("similar", "parallel") for p, a, pc, c in zip(l, l[1:], CF, CF[1:]))

    def dissonant(l):
        return sum((a - c) % 12 not in K.CONSONANT for a, c in zip(l, CF)) >= 3

    d1 = breaking("direct", has_direct)
    d2 = breaking("consonance", dissonant)
    seq = concat([voices([bars(d1), bars(CF)], beat=0.3).at_level(LEVEL), voices([bars(d2), bars(CF)], beat=0.3).at_level(LEVEL)], gap=1.0, names=["direct", "dissonant"])
    return {"full": int(full), "base": base, "rows": rows, "direct_line": d1, "dissonant_line": d2,
            "direct_at": [i + 1 for i, (p, a, pc, c) in enumerate(zip(d1, d1[1:], CF, CF[1:])) if (a - c) % 12 in (0, 7) and K.motion(p, a, pc, c) in ("similar", "parallel")],
            "dissonant_at": [i for i, (a, c) in enumerate(zip(d2, CF)) if (a - c) % 12 not in K.CONSONANT],
            "times": {"direct": [times(seq, 0, len(CF), "direct."), times(seq, 1, len(CF), "direct.")], "dissonant": [times(seq, 0, len(CF), "dissonant."), times(seq, 1, len(CF), "dissonant.")]},
            "starts": {k: float(seq.events[k]) for k in ("direct", "dissonant")},
            "clips": {"broken": save("damage.broken", seq, level=None, detail="two lines over Fux's cantus, each breaking one rule")}}


def compute_species() -> dict:
    out, clips = {}, {}
    cf_ev = bars(CF)
    for n in (2, 3, 4, 5):
        line = K.species(CF, n, np.random.default_rng(100 + n), tries=150)
        c = voices([line, cf_ev], beat=0.32)
        name = f"species.{n}"
        clips[str(n)] = save(name, c, detail=f"species {n} over Fux's cantus firmus: Part 7's piano")
        diss, sus = [], []
        for p, a, d in line:
            cfn = CF[min(int(a // 4), len(CF) - 1)]
            if (p - cfn) % 12 not in K.CONSONANT:
                diss.append([int(p), float(a), float(d)])
            if a % 4 == 2 and a + d > 4 * (a // 4 + 1) + 0.5 and int(a // 4) + 1 < len(CF):
                nxt = CF[int(a // 4) + 1]
                if (p - nxt) % 12 not in K.CONSONANT:
                    sus.append([int(p), float(a), float(d), int((p - nxt) % 12)])
        out[str(n)] = {"events": evrows(line), "times": times(c, 0, len(line)), "cf_times": times(c, 1, len(CF)), "independence": K.independence(line, cf_ev),
                       "dissonances": diss, "suspensions": sus, "notes": len(line)}
    out["clips"] = clips
    return out


def compute_independence() -> dict:
    s = load("species")
    f = load("fux")
    cf_ev = bars(CF)
    rows = [{"name": "organum", **K.independence(bars(K.organum(CF, -7)), cf_ev)}, {"name": "first species", **K.independence(bars(f["best"]), cf_ev)}]
    for n in (2, 3, 4, 5):
        rows.append({"name": ["", "", "second species", "third species", "fourth species", "fifth species"][n], **s[str(n)]["independence"]})
    for r in rows:
        r["notes_up"] = None
    return {"rows": rows}


def compute_tune() -> dict:
    beat = 0.3                                                     # a cantus note (a bar) lasts four beats
    rng = np.random.default_rng(16)
    phrases = [TUNE[7 * k: 7 * k + 7] for k in range(6)]
    cf = TUNE
    # phrase 0: parallel organum a fifth below; phrases 1-5: species 1 to 5 above, one search over the rest of the Tune
    kinds = [1] * 7 + [2] * 7 + [3] * 7 + [4] * 7 + [5] * 7
    sub = cf[7:]
    best_line, best_s = None, -1e9
    for _ in range(200):
        ks = [k if k != 5 else int(rng.choice([2, 3, 3, 2])) for k in kinds]
        line = K._search(sub, ks, sub[-1], rng, budget=6000)
        if line is None:
            continue
        s = K._species_score(sub, line)
        if s > best_s:
            best_line, best_s = line, s
    line = [(p, a + 28.0, d) for p, a, d in best_line]
    org = [(p, 4.0 * k, 4.0) for k, p in enumerate(K.organum(cf[:7], -7))]
    cf_ev = bars(cf)
    c = voices([org + line, cf_ev], beat=beat, tail=1.8)
    out = Clip(c.y, SR, {**c.events, **{f"phrase{k}": 4.0 * 7 * k * beat for k in range(6)}}, []).at_level(LEVEL)
    names = ["organum, a fifth below", "first species", "second species", "third species", "fourth species", "fifth species"]
    upper = org + line
    stats = []
    for k in range(6):
        a, b = 28.0 * k, 28.0 * (k + 1)
        up = [e for e in upper if a <= e[1] < b]
        lo = [e for e in cf_ev if a <= e[1] < b]
        stats.append({"name": names[k], **K.independence(up, lo)})
    return {"clip": save("tune.variation16", out, level=None, detail="the Tune as a cantus firmus, with a second voice in organum and then in five species"), "seconds": out.duration,
            "upper": evrows(upper), "cf": cf, "names": names, "stats": stats, "beat": beat, "times_upper": times(c, 0, len(upper)), "times_cf": times(c, 1, len(cf)),
            "phrase_starts": [4.0 * 7 * k * beat for k in range(6)], "phrase_seconds": 28.0 * beat}


def compute_variation() -> dict:
    t = load("tune")
    st = t["stats"]
    return {"part": 16, "title": r"as a cantus firmus: in organum, then with a voice above it in each of the five species", "seconds": t["seconds"],
            "measure": rf"notes beginning together: {100 * st[0]['together']:.0f}\% in organum, {100 * st[4]['together']:.0f}\% in fourth species", "clip": "tune.variation16"}


# ---------------------------------------------------------------------------
TOY = [62, 65, 67, 64, 62]                                         # a five-note cantus for counting by hand: D F G E D
TOY_RULES = ("consonance", "start", "unison", "repeat", "melodic", "direct", "spacing", "cadence")


def toy_table() -> dict:
    """The counting of chapter 6 done in the open: for each bar and each note, the number of ways to finish the line
    from there (backward), and the number of ways to arrive there (forward); the rules here depend only on pairs of
    neighbouring notes, so a note is the whole state."""
    cands = K.candidates(TOY)
    ctx = K._Ctx(tuple(TOY), frozenset(TOY_RULES), False, ())
    ok = lambda i, p, q: K._allowed(ctx, i, p, 0, 0, q)[0]        # noqa: E731
    n = len(TOY)
    W = [dict() for _ in TOY]
    for q in cands[-1]:
        W[-1][q] = 1
    for i in range(n - 2, -1, -1):
        for p in cands[i]:
            W[i][p] = sum(W[i + 1][q] for q in cands[i + 1] if ok(i + 1, p, q))
    F = [dict() for _ in TOY]
    for p in cands[0]:
        F[0][p] = 1 if ok(0, None, p) else 0
    for i in range(1, n):
        for q in cands[i]:
            F[i][q] = sum(F[i - 1][p] for p in cands[i - 1] if F[i - 1][p] and ok(i, p, q))
    cells = [[[int(p), int(F[i][p]), int(W[i][p])] for p in cands[i] if F[i][p] and W[i][p]] for i in range(n)]
    edges = [[[int(p), int(q)] for p in cands[i] for q in cands[i + 1] if F[i][p] and W[i][p] and F[i + 1][q] and W[i + 1][q] and ok(i + 1, p, q)] for i in range(n - 1)]
    total = sum(W[0][p] for p in cands[0] if F[0][p])
    # every line, listed, and one drawn uniformly by walking forward with probabilities W(next) / W(here)
    lines = []

    def walk(i, prev, acc):
        if i == n:
            lines.append(acc)
            return
        for q in cands[i]:
            if (ok(i, prev, q) if i else F[0][q]) and W[i][q]:
                walk(i + 1, q, acc + [q])
    walk(0, None, [])
    rng = np.random.default_rng(2)
    first = [c for c in cells[0]]
    pick = [int(rng.choice([c[0] for c in first], p=np.array([c[2] for c in first]) / total))]
    probs = [[[c[0], c[2] / total] for c in first]]
    for i in range(1, n):
        nxt = [c for c in cells[i] if ok(i, pick[-1], c[0])]
        w = np.array([c[2] for c in nxt], dtype=float)
        probs.append([[c[0], float(x / w.sum())] for c, x in zip(nxt, w)])
        pick.append(int(rng.choice([c[0] for c in nxt], p=w / w.sum())))
    assert total == K.count(TOY, rules=TOY_RULES) == len(lines)
    return {"cf": TOY, "rules": list(TOY_RULES), "cells": cells, "edges": edges, "total": int(total), "lines": [[int(x) for x in l] for l in lines],
            "pick": pick, "probs": probs}


def free_organum(principal) -> list[int]:
    """A free organum below ``principal`` (as around 1100): a perfect consonance or unison at every note, chosen by
    dynamic programming to move against the principal voice as much as possible, small steps, unison or octave at
    the ends."""
    opts = (0, 5, 7, 12)
    n = len(principal)
    val = {o: (0.0 if o in (0, 12) else -1e9) for o in opts}
    back = []
    for i in range(1, n):
        new, bk = {}, {}
        for o in opts:
            if i == n - 1 and o not in (0, 12):
                new[o], bk[o] = -1e9, 0
                continue
            best, arg = -1e18, None
            for po in opts:
                a0, a1, b0, b1 = principal[i - 1], principal[i], principal[i - 1] - po, principal[i] - o
                m = K.motion(a0, a1, b0, b1)
                sc = {"contrary": 3.0, "oblique": 1.0, "parallel": -1.0, "similar": -1.0, "static": 0.0}[m]
                sc -= 3.0 if abs(b1 - b0) > 5 else 0.0
                sc -= 2.0 if (b1 % 12) not in K.WHITE else 0.0
                if val[po] + sc > best:
                    best, arg = val[po] + sc, po
            new[o], bk[o] = best, arg
        val = new
        back.append(bk)
    o = max(val, key=val.get)
    out = [o]
    for bk in reversed(back):
        o = bk[o]
        out.append(o)
    out.reverse()
    return [p - o for p, o in zip(principal, out)]


def oblique_organum(principal, interval: int = 5, floor: int = 60) -> list[int]:
    """Organum at the fourth below with a boundary note, as in the Musica enchiriadis and Guido: the organal voice
    may not go below ``floor``, so it holds there until the principal voice rises far enough, and the two meet in a
    unison at the end."""
    out = [max(p - interval, floor) for p in principal]
    out[-1] = principal[-1] if principal[-1] >= floor else out[-1]
    return out


def compute_more() -> dict:
    out, clips = {}, {}
    # 1. organum's three stages, heard on the whole Tune
    ph = TUNE[:14]
    stages = {"parallel": K.organum(ph, -7), "oblique": oblique_organum(ph), "free": free_organum(ph)}
    parts = [voices([tune_events(ph), tune_events(v)], beat=0.45, voice=organ).at_level(LEVEL) for v in stages.values()]
    seq = concat(parts, gap=1.0, names=list(stages))
    out["stages"] = {"tune": ph, "beats": TUNE_BEATS[:14], "voices": stages, "starts": {k: float(seq.events[k]) for k in stages},
                     "times": {k: [times(seq, 0, 14, f"{k}."), times(seq, 1, 14, f"{k}.")] for k in stages},
                     "independence": {k: K.independence(tune_events(ph), tune_events(v)) for k, v in stages.items()}}
    clips["stages"] = save("more.stages", seq, level=None, kind="synthesized", detail="the Tune in parallel, oblique and free organum: organ tones")
    # 2. counting by hand
    out["toy"] = toy_table()
    # 3. a line below the cantus
    below = K.best(CF, below=True, tries=3000)
    c = voices([bars(CF), bars(below)], beat=0.3)
    out["below"] = {"line": below, "count": int(K.count(CF, below=True)), "above": int(K.count(CF)), "verticals": [int(K.vertical(a, b, True)) for a, b in zip(CF, below)],
                    "violations": K.check(CF, below, below=True), "times": [times(c, 0, len(CF)), times(c, 1, len(CF))],
                    "start_rule": {"fifth": int(K.count(CF, rules=tuple(r for r in K.RULES if r != "start"), below=True))}}
    clips["below"] = save("more.below", c, detail="a first-species line below Fux's cantus: Part 7's piano")
    # 4. how much delay separates two notes
    delays = [0, 10, 20, 35, 60]
    lad = [voices([[(72, 0.0, 3.0)], [(60, 0.0, 3.0)]], beat=0.5, voice=organ, tail=0.3, delays=[d / 1000.0, 0.0]).at_level(LEVEL) for d in delays]
    seq = concat(lad, gap=0.8, names=[f"d{d}" for d in delays])
    out["ladder"] = {"delays": delays, "starts": [float(seq.events[f"d{d}"]) for d in delays]}
    clips["ladder"] = save("more.ladder", seq, level=None, kind="synthesized", detail="an octave five times, the upper note 0, 10, 20, 35 and 60 ms late")
    # 5. an ear question: the same notes, with the cantus and held over (a chain of 7-6 suspensions)
    cf5 = [67, 65, 64, 62, 60]
    A = [(76, 0.0, 4.0), (74, 4.0, 4.0), (72, 8.0, 4.0), (71, 12.0, 4.0), (72, 16.0, 4.0)]
    B = [(76, 2.0, 4.0), (74, 6.0, 4.0), (72, 10.0, 4.0), (71, 14.0, 2.0), (72, 16.0, 4.0)]
    qa, qb = voices([A, bars(cf5)], beat=0.34), voices([B, bars(cf5)], beat=0.34)
    seq = concat([qa.at_level(LEVEL), qb.at_level(LEVEL)], gap=1.0, names=["A", "B"])
    sus = [[int(p), float(a), int((p - cf5[int(a // 4) + 1]) % 12)] for p, a, d in B if a % 4 == 2 and a + d > 4 * (a // 4 + 1)]
    out["suspension"] = {"cf": cf5, "A": evrows(A), "B": evrows(B), "answer": "B", "suspensions": sus,
                         "times": {"A": [times(seq, 0, 5, "A."), times(seq, 1, 5, "A.")], "B": [times(seq, 0, 5, "B."), times(seq, 1, 5, "B.")]},
                         "starts": {k: float(seq.events[k]) for k in "AB"}}
    clips["suspension"] = save("more.suspension", seq, level=None, detail="the same notes over a falling cantus: with it, then held over: Part 7's piano")
    out["clips"] = clips
    return out


ITEMS = {"hook": compute_hook, "organum": compute_organum, "fusion": compute_fusion, "motions": compute_motions, "onsets": compute_onsets, "fux": compute_fux,
         "counting": compute_counting, "damage": compute_damage, "species": compute_species, "independence": compute_independence, "tune": compute_tune,
         "variation": compute_variation, "more": compute_more}


if __name__ == "__main__":
    CACHE.main(ITEMS, __doc__)
