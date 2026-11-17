"""Precompute everything numerical, and every sound, in Part 42 of *Music, Built* ("Composing").

    python -m videos.music.music42.compute              # everything missing (about two minutes)
    python -m videos.music.music42.compute --force search

Numbers are cached in ``.cache/music42/<name>.json``, sounds in ``.cache/music42/audio/``.  The tools are Monochord's
(``explainer/music/monochord/composer.py``).  The instruments are Part 38's: Part 7's piano (a struck string on a
soundboard) and a plucked bass, both physical models.  Every motive, minuet table and melody is ours or was generated
here; the Ode to Joy (Beethoven, 1824) and the Tune are in the public domain.

Items:
    hook        an ear question: the searcher's first draft and the draft it kept (which was kept?)
    ode         the Ode to Joy's theme: steps and leaps counted
    motive      our motive and its operations, each heard
    quiz        an ear question: the motive, then the same played backwards or turned upside down?
    develop     a sentence built by developing variation: statement, repetition, fragments, cadence
    kinds       the Tune's first phrase varied four ways: ornamental, rhythmic, harmonic, character
    funnel      how many 8-note melodies obey a growing list of rules (exact counts)
    dice        our minuet dice game: its table, two minuets, the count of distinct pieces
    illiac      Hiller and Isaacson's method: a line drawn note by note, rejections counted
    chains      Markov chains of order 1 and 4 over the series' tune corpus, and how much they copy
    tension     the searcher aiming at two tension plans (climax late, climax early)
    search      the searcher: 2,000 drafts, the critics' rejections, rejected drafts heard, the best heard
    evolve      the same critics as a fitness for a genetic algorithm
    tune        Variation 42: a variation on the Tune's first four notes, composed by the searcher
    variation   the Variations ledger, row 42
"""

from __future__ import annotations

import numpy as np

from explainer.ai.cache import Cache
from explainer.music.monochord import EXAMPLE_LEVEL, SR, Clip, ClipStore, concat, mix
from explainer.music.monochord import composer as K
from explainer.music.monochord import melody as M
from explainer.music.monochord.partkit import saver, signoff
from videos.music.music38 import compute as P38

CACHE = Cache("music42")
CLIPS = ClipStore("music42")
load = CACHE.load
LEVEL = EXAMPLE_LEVEL - 2.5
save = saver(CLIPS, LEVEL, kind="physical model")
arr = P38.arr
piano, bass = P38.piano, P38.bass

PLAN = ["I", "IV", "V", "I", "vi", "ii", "V", "I"]                # the searcher's chords, one a bar
ARCH = [1.0, 1.5, 2.0, 1.5, 2.5, 3.0, 2.5, 0.5]                  # its tension plan: climax in bar 6
EARLY = [2.5, 3.0, 2.5, 2.0, 1.5, 1.5, 1.0, 0.5]                 # the other plan: climax in bar 2
EARLY_CHORDS = ["I", "V7", "ii", "V", "I", "IV", "V", "I"]      # with its harmony: the dominant seventh in bar 2
BEAT = 0.42                                                      # seconds a beat


def tl(notes):
    return [[int(m), float(a), float(d)] for m, a, d in notes]


def render(mel, bass_notes=(), beat=BEAT, tail=1.2, vel=0.9, bass_gain=-5.0):
    parts = [(arr(piano(m, d * beat * 1.05, vel)), a * beat, 0.0) for m, a, d in mel]
    parts += [(arr(bass(m, d * beat * 0.9)), a * beat, bass_gain) for m, a, d in bass_notes]
    end = max(a + d for _, a, d in list(mel) + list(bass_notes)) * beat + tail
    return Clip(mix(parts, duration=end).y, SR)


def search_run(seed=0, plan=ARCH, drafts=2000, tension_weight=1.0):
    return K.compose(K.MOTIVE, PLAN, K.bass_line(PLAN), np.random.default_rng(seed), drafts=drafts, plan=plan,
                     tension_weight=tension_weight)


# ---------------------------------------------------------------------------------------------------------- items
def compute_hook() -> dict:
    r = search_run(0)
    bl = K.bass_line(PLAN)
    first = r["shown"][0]
    a = render(first["melody"], bl)
    b = render(r["best"]["melody"], bl)
    c = concat([a, b], gap=1.0, names=["first", "kept"])
    return {"first": {"draft": first["draft"] + 1, "why": first["why"], "melody": tl(first["melody"])},
            "kept": {"draft": r["best"]["draft"] + 1, "melody": tl(r["best"]["melody"])}, "drafts": r["drafts"],
            "rejected": sum(r["rejected"].values()), "answer": "second",
            "starts": {k: float(c.events[k]) for k in ("first", "kept")},
            "clips": {"two": save("hook.two", c, detail="the searcher's first draft, which its critics rejected, then the draft it kept; Part 7's piano and a plucked bass")}}


def compute_ode() -> dict:
    t = [x for x in M.corpus() if x.name == "Ode to Joy"][0]
    p = [60 + x for x in t.pitches]
    iv = np.diff(p)
    steps = int(np.sum(np.abs(iv) <= 2) - np.sum(iv == 0))
    reps = int(np.sum(iv == 0))
    leaps = int(np.sum(np.abs(iv) > 2))
    on, mel = 0.0, []
    for m, d in zip(p, t.beats):
        mel.append((m, on, d))
        on += d
    c = render(mel, beat=0.45)
    return {"melody": tl(mel), "moves": len(iv), "steps": steps, "repeats": reps, "leaps": leaps,
            "clips": {"theme": save("ode.theme", c, detail="the Ode to Joy's first two phrases (Beethoven, 1824); Part 7's piano")}}


SHOW_OPS = ["invert", "retrograde", "augment", "diminish", "fragment", "expand an interval", "new rhythm", "embellish"]


def compute_motive() -> dict:
    figs = {"motive": K.MOTIVE}
    for name in SHOW_OPS:
        figs[name] = K.OPS[name](K.MOTIVE)
    clips = [render(f, beat=0.4, tail=0.5) for f in figs.values()]
    c = concat(clips, gap=0.6, names=list(figs))
    return {"figures": {k: tl(v) for k, v in figs.items()}, "starts": {k: float(c.events[k]) for k in figs},
            "clips": {"ops": save("motive.ops", c, detail="our motive, then inverted, backwards, augmented, diminished, fragmented, with an interval widened, in a new rhythm, embellished; Part 7's piano")}}


def compute_quiz() -> dict:
    a = K.MOTIVE
    b = K.retrograde(K.MOTIVE)
    c = concat([render(a, beat=0.45, tail=0.6), render(b, beat=0.45, tail=0.6)], gap=0.9, names=["motive", "changed"])
    return {"motive": tl(a), "changed": tl(b), "answer": "backwards", "upside": tl(K.invert(a)),
            "starts": {k: float(c.events[k]) for k in ("motive", "changed")},
            "clips": {"two": save("quiz.two", c, detail="our motive, then a transformation of it; Part 7's piano")}}


def sentence():
    """Schoenberg's sentence, built by hand from the motive: the basic idea, its repetition a step higher, then the
    first three notes in a falling sequence (fragmentation), then the whole motive at double speed, falling again
    (liquidation), and a cadence.  Returns the melody and, for each figure, its operations and transposition."""
    f3, dim = K.fragment(K.MOTIVE, 3), K.diminish(K.MOTIVE)
    figs = [([], K.MOTIVE, 0, 0.0), ([], K.MOTIVE, 1, 4.0),
            (["first three notes"], f3, 3, 8.0), (["first three notes"], f3, 2, 10.0), (["first three notes"], f3, 1, 12.0), (["first three notes"], f3, 0, 14.0),
            (["diminish"], dim, 1, 16.0), (["diminish"], dim, 0, 18.0), (["diminish"], dim, -2, 20.0), (["diminish"], dim, -3, 22.0)]
    mel, parts = [], []
    for ops, f, k, t in figs:
        mel += K.shift_time(K.transpose(f, k), t)
        parts.append({"ops": ops, "k": k, "t": t})
    mel += [(67, 24.0, 1.0), (65, 25.0, 0.5), (64, 25.5, 0.5), (62, 26.0, 2.0), (60, 28.0, 4.0)]
    return mel, parts


SENTENCE_CHORDS = ["I", "I", "ii", "ii", "IV", "I", "ii", "I", "ii", "I", "vi", "V", "V", "V", "I", "I"]    # a chord every two beats


def compute_develop() -> dict:
    mel, parts = sentence()
    bl = [(K.ROOT[c], 2.0 * i, 2.0) for i, c in enumerate(SENTENCE_CHORDS)]
    c = render(mel, bl)
    p = K.pitches(mel)
    return {"melody": tl(mel), "bass": tl(bl), "figures": parts, "chords": SENTENCE_CHORDS,
            "notes": len(mel), "from_motive": sum(len(x) for x in [K.MOTIVE] * 2) + 4 * 3 + 4 * 4,
            "widest_leap": int(max(abs(b - a) for a, b in zip(p, p[1:]))),
            "clips": {"sentence": save("develop.sentence", c, detail="a sentence of ours built from the motive: the idea, its repetition a step higher, fragments in sequence, the motive at double speed, a cadence; Part 7's piano and a plucked bass")}}


def _tune_phrase():
    t = [x for x in M.corpus() if x.name == M.THE_TUNE][0]
    on, out = 0.0, []
    for m, d in list(zip(t.pitches, t.beats))[:14]:
        out.append((72 + m, on, d))
        on += d
    return out


def compute_kinds() -> dict:
    A = _tune_phrase()                                            # two phrases, 16 beats
    ch = ["I", "I", "IV", "I", "IV", "I", "V", "I"]               # a chord every two beats
    def bassof(chs, step=2.0):
        return [(K.ROOT[s], i * step, step) for i, s in enumerate(chs)]
    plain_bass = bassof(ch)
    # ornamental: each beat note followed by an upper neighbour
    orn = []
    for m, a, d in A:
        if d == 1:
            orn += [(m, a, 0.5), (K.dstep(m, 1), a + 0.5, 0.25), (m, a + 0.75, 0.25)]
        else:
            orn.append((m, a, d))
    # rhythmic: long-short pairs (dotted)
    rhy = []
    for m, a, d in A:
        rhy += [(m, a, 0.75), (m, a + 0.75, 0.25)] if d == 1 else [(m, a, d)]
    # harmonic: same melody, new chords
    hch = ["vi", "iii", "ii", "V", "ii", "vi", "V", "I"]
    # character: minor, slower, low
    minor = {64: 63, 69: 68, 71: 70, 76: 75, 81: 80}
    car = [(minor.get(m, m) - 12, a * 1.5, d * 1.5) for m, a, d in A]
    cbass = [(m - 12 + (0 if m % 12 != 4 else -1), a * 1.5, d * 1.5) for m, a, d in plain_bass]
    versions = {"the theme": (A, plain_bass), "ornamental": (orn, plain_bass), "rhythmic": (rhy, plain_bass),
                "harmonic": (A, bassof(hch)), "character": (car, cbass)}
    clips = [render(m, b, beat=0.36, tail=0.6) for m, b in versions.values()]
    c = concat(clips, gap=0.8, names=list(versions))
    return {"versions": {k: {"melody": tl(m), "bass": tl(b)} for k, (m, b) in versions.items()}, "chords": ch, "harmonic_chords": hch,
            "starts": {k: float(c.events[k]) for k in versions},
            "clips": {"five": save("kinds.five", c, detail="the Tune's first two phrases, then four variations of ours: ornamental, rhythmic, harmonic, and in character (minor, slower, lower); Part 7's piano and a plucked bass")}}


def compute_funnel() -> dict:
    rules = list(K.FUNNEL_RULES)
    counts = [K.count_funnel(8, rules=tuple(rules[:k])) for k in range(len(rules) + 1)]
    return {"rules": rules, "counts": counts, "notes": 15, "length": 8}


def compute_dice() -> dict:
    T = K.dice_table()
    cnt = K.dice_count(T)
    rng = np.random.default_rng(1757)
    rolls = [[int(rng.integers(1, 7) + rng.integers(1, 7)) for _ in range(16)] for _ in range(2)]
    pieces = [K.dice_piece(T, r) for r in rolls]
    clips = [render(m, b, beat=0.4, tail=0.8) for m, b in pieces]
    c = concat(clips, gap=1.2, names=["one", "two"])
    shared = sum(T[b][rolls[0][b]]["melody"] == T[b][rolls[1][b]]["melody"] for b in range(16))
    grid = [[list(T[b][s]["melody"]) for s in range(2, 13)] for b in range(16)]
    return {"count": {k: (int(v) if isinstance(v, (int, np.integer)) else v) for k, v in cnt.items()}, "rolls": rolls,
            "pieces": [{"melody": tl(m), "bass": tl(b)} for m, b in pieces], "shared_bars": int(shared), "joins": K.dice_joins(T),
            "plan": K.MINUET_PLAN, "grid": [[tl(o) for o in row] for row in grid], "p": {str(k): v for k, v in K.DICE_P.items()},
            "starts": {k: float(c.events[k]) for k in ("one", "two")},
            "clips": {"two": save("dice.two", c, detail="two minuets thrown with dice from our table of 176 bars; Part 7's piano and a plucked bass")}}


def compute_illiac() -> dict:
    rng = np.random.default_rng(1957)
    runs = [K.illiac(12, rng) for _ in range(200)]
    rej = {}
    for r in runs:
        for k, v in r["rejected"].items():
            rej[k] = rej.get(k, 0) + v
    # one line in detail, with every draw recorded
    rng = np.random.default_rng(4)
    line, draws, white = [60], [], [m for m in range(60, 73) if m % 12 in K.MAJOR]
    one = K.illiac(12, np.random.default_rng(4))
    # replay that run's first draws for the picture (same generator, same order)
    rng = np.random.default_rng(4)
    fails = [0]
    while len(line) < 12 and len(draws) < 400:
        x = int(rng.choice(white))
        why = K._illiac_ok(line, x, 12)
        draws.append([x, why, len(line)])
        if why is None:
            line.append(x)
            fails.append(0)
        else:
            fails[-1] += 1
            if fails[-1] >= 50 and len(line) > 1:
                line.pop()
                fails.pop()
                fails[-1] += 1
    assert line == one["line"]
    mel = [(m, float(i), 1.0) for i, m in enumerate(line)]
    mel[-1] = (mel[-1][0], mel[-1][1], 2.0)
    c = render(mel, beat=0.5)
    return {"line": line, "draws": draws, "one": {k: one[k] for k in ("rejected", "draws", "backtracks")},
            "runs": len(runs), "mean_draws": float(np.mean([r["draws"] for r in runs])), "rejected": rej,
            "rules": K.ILLIAC_RULES,
            "clips": {"line": save("illiac.line", c, detail="a twelve-note line made by drawing notes at random and rejecting those that break rules; Part 7's piano")}}


def compute_chains() -> dict:
    seqs = {t.name: t.pitches for t in M.corpus() if t.mode == "major"}
    out, clips = {}, []
    for order, seed in ((1, 5), (4, 5)):
        mod = K.markov(list(seqs.values()), order)
        best = None
        for s in range(seed, seed + 20):
            g = K.generate(mod, 24, np.random.default_rng(s))
            if g[-1] == 0 and 0 <= min(g) + 7 and max(g) <= 16:
                best = g
                break
        g = best or K.generate(mod, 24, np.random.default_rng(seed))
        cp = K.longest_copy(g, seqs)
        # typical copying over many walks
        runs = [K.longest_copy(K.generate(mod, 24, np.random.default_rng(100 + s)), seqs)["run"] for s in range(40)]
        out[str(order)] = {"notes": g, "copy": cp, "mean_copy": float(np.mean(runs)), "contexts": len(mod["T"])}
        mel = [(72 + x, float(i), 1.0) for i, x in enumerate(g)]
        mel[-1] = (mel[-1][0], mel[-1][1], 2.0)
        clips.append(render(mel, beat=0.32, tail=0.8))
    c = concat(clips, gap=1.0, names=["first", "second"])
    return {"orders": out, "tunes": len(seqs), "order_of": {"first": 1, "second": 4}, "answer": "second",
            "starts": {k: float(c.events[k]) for k in ("first", "second")},
            "clips": {"two": save("chains.two", c, detail="two melodies walked from Markov chains over the series' corpus of folk and public-domain tunes, remembering one note and four; Part 7's piano")}}


def compute_tension() -> dict:
    out, clips = {}, []
    for name, plan, chords in (("late", ARCH, PLAN), ("early", EARLY, EARLY_CHORDS)):
        bl = K.bass_line(chords)
        r = K.compose(K.MOTIVE, chords, bl, np.random.default_rng(2), drafts=2000, plan=plan, tension_weight=6.0)
        m = r["best"]["melody"]
        cur = K.tension(m, chords)
        out[name] = {"plan": plan, "chords": chords, "curve": cur, "fit": r["best"]["verdict"]["tension_fit"], "melody": tl(m),
                     "peak_bar": int(np.argmax(cur)) + 1}
        clips.append(render(m, bl))
    c = concat(clips, gap=1.0, names=["late", "early"])
    return {**out, "starts": {k: float(c.events[k]) for k in ("late", "early")},
            "clips": {"two": save("tension.two", c, detail="two melodies by the searcher from the same motive, aimed at a late climax and an early one; Part 7's piano and a plucked bass")}}


def compute_search() -> dict:
    r = search_run(0)
    bl = K.bass_line(PLAN)
    shown = r["shown"][:3]
    rej = concat([render(s["melody"][:], bl, tail=0.6) for s in shown], gap=0.9, names=[f"r{i}" for i in range(len(shown))])
    best = render(r["best"]["melody"], bl)
    figs = K.bar_figures(r["best"]["melody"])
    der = [list(K.derivation(f, K.MOTIVE)) if K.derivation(f, K.MOTIVE) is not None else None for f in figs]
    trace = [x for x in r["trace"]]
    improve = [[i + 1, x] for i, x in enumerate(trace) if x is not None and (i == 0 or all(y is None or y < x for y in trace[:i]))]
    return {"drafts": r["drafts"], "rejected": r["rejected"], "survivors": r["survivors"],
            "best": {"draft": r["best"]["draft"] + 1, "melody": tl(r["best"]["melody"]), "plan": [[o, k] for o, k in r["best"]["plan"]],
                     "verdict": {k: (float(v) if isinstance(v, (float, np.floating)) else v) for k, v in r["best"]["verdict"].items()},
                     "derivations": der},
            "shown": [{"draft": s["draft"] + 1, "why": s["why"], "melody": tl(s["melody"]), "verdict": {k: (float(v) if not isinstance(v, bool) else v) for k, v in s["verdict"].items()}} for s in shown],
            "improvements": improve, "bass": tl(bl), "chords": PLAN, "plan": ARCH,
            "starts": {f"r{i}": float(rej.events[f"r{i}"]) for i in range(len(shown))},
            "clips": {"rejected": save("search.rejected", rej, detail="three drafts the critics rejected, each for a different reason; Part 7's piano and a plucked bass"),
                      "best": save("search.best", best, detail="the draft the searcher kept; Part 7's piano and a plucked bass")}}


def compute_evolve() -> dict:
    e = K.evolve(K.MOTIVE, PLAN, K.bass_line(PLAN), np.random.default_rng(0), plan=ARCH)
    c = render(e["best"], K.bass_line(PLAN))
    return {"best_curve": e["best_curve"], "mean_curve": e["mean_curve"], "fitness": e["fitness"], "melody": tl(e["best"]),
            "clips": {"best": save("evolve.best", c, detail="the fittest melody after forty generations; Part 7's piano and a plucked bass")}}


TUNE_MOTIVE = [(72, 0.0, 1.0), (72, 1.0, 1.0), (79, 2.0, 1.0), (79, 3.0, 1.0)]     # the Tune's first four notes
TUNE_CHORDS = ["I", "IV", "I", "V", "vi", "IV", "V", "I"]


def compute_tune() -> dict:
    mot = K.transpose(TUNE_MOTIVE, -7)                            # in the searcher's register, C4
    bl = K.bass_line(TUNE_CHORDS)
    r = K.compose(mot, TUNE_CHORDS, bl, np.random.default_rng(42), drafts=3000, plan=ARCH)
    theme = _tune_phrase()[:7]
    a = render([(m - 12, a_, d) for m, a_, d in theme], [(48, 0.0, 4.0), (53, 4.0, 2.0), (48, 6.0, 2.0)], beat=0.42, tail=0.6)
    b = render(r["best"]["melody"], bl, tail=1.6)
    c = concat([a, b], gap=0.8, names=["theme", "variation"])
    figs = K.bar_figures(r["best"]["melody"])
    der = [list(K.derivation(f, mot)) if K.derivation(f, mot) is not None else None for f in figs]
    return {"drafts": r["drafts"], "rejected": r["rejected"], "survivors": r["survivors"], "kept": r["best"]["draft"] + 1,
            "melody": tl(r["best"]["melody"]), "derivations": der, "chords": TUNE_CHORDS, "bass": tl(bl), "motive": tl(mot),
            "score": float(r["best"]["verdict"]["score"]), "seconds": c.duration,
            "shown": [{"draft": s["draft"] + 1, "why": s["why"], "melody": tl(s["melody"])} for s in r["shown"][:4]],
            "starts": {k: float(c.events[k]) for k in ("theme", "variation")},
            "clips": {"variation42": save("tune.variation42", c, detail="the Tune's first phrase, then a variation on its first four notes composed by the searcher; Part 7's piano and a plucked bass")}}


def compute_variation() -> dict:
    t = load("tune")
    rej = sum(t["rejected"].values())
    return {"part": 42, "title": "composed by the searcher from its first four notes, with what it threw away", "seconds": round(t["seconds"], 1),
            "measure": f"draft {t['kept']} of {t['drafts']} kept; {rej} rejected by the critics, {t['survivors']} scored",
            "clip": "tune.variation42"}


def compute_signoff() -> dict:
    """The part's last sound: the opening of its Variation, under the next part's title."""
    load("variation")
    return signoff(CLIPS, "tune.variation42", 42)


ITEMS = {"hook": compute_hook, "ode": compute_ode, "motive": compute_motive, "quiz": compute_quiz, "develop": compute_develop,
         "kinds": compute_kinds, "funnel": compute_funnel, "dice": compute_dice, "illiac": compute_illiac, "chains": compute_chains,
         "tension": compute_tension, "search": compute_search, "evolve": compute_evolve, "tune": compute_tune,
         "variation": compute_variation,
         "signoff": compute_signoff}


if __name__ == "__main__":
    CACHE.main(ITEMS, __doc__)
