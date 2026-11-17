"""Precompute everything numerical, and every sound, in Part 60 of *Music, Built* ("The Business of Music").

    python -m videos.music.music60.compute              # everything missing (a few minutes)
    python -m videos.music.music60.compute --force hook

Numbers are cached in ``.cache/music60/<name>.json``, sounds in ``.cache/music60/audio/``.  The tools are Monochord's
(``explainer/music/monochord/business.py``, with Part 14's melody model).  Every term, price and population is
illustrative and dated 2026; none of it is legal or financial advice.  The music is Part 56's session, Part 38's piano,
Part 8's voice and Part 9's bowed strings; no third-party recording is played.

Items:
    hook        an ear question: two melodies with the same eight-note opening, by Part 14's model, independently
    melodies    how many distinct melodies a melody model makes: collision probabilities, effective numbers, birthdays
    rights      one composition, two recordings: our session and a piano cover
    waterfall   one subscription and one million streams divided among their claimants, under two kinds of deal
    stream      the Tune by our session, past the 30 seconds after which a stream is counted
    deals       an advance recouped stream by stream, against a distribution deal
    pool        a month on a simulated service divided pro rata and user by user; a bot farm in each
    market      Salganik, Dodds and Watts's social-influence experiment, simulated; two worlds' hits heard
    intro       a long introduction against the voice at once
    live        the cost disease and a string quartet; three ways to sell a tour date's tickets
    similar     three pairs of melodies: the same notes, the same contour, the same tune in another key
    sample      a slice of our recording looped under a new beat, against the same notes re-played (an ear question)
    ai          an old folk song and a new melody by Part 14's model, trained without it (an ear question)
    tune60      Variation 60: the Tune's family of copyrights: our recording, a cover, a remix that samples it
    variation   the Variations ledger, row 60
"""

from __future__ import annotations

import math

import numpy as np

from explainer.ai.cache import Cache
from explainer.music.monochord import EXAMPLE_LEVEL, SR, Clip, ClipStore, concat, mix
from explainer.music.monochord import business as B
from explainer.music.monochord import melody as M
from explainer.music.monochord.instruments import choir as CH
from explainer.music.monochord.instruments import strings as STR
from explainer.music.monochord.partkit import saver, signoff
from videos.music.music38 import compute as P38
from videos.music.music40 import compute as P40
from videos.music.music56 import compute as P56

CACHE = Cache("music60")
CLIPS = ClipStore("music60")
load = CACHE.load
LEVEL = EXAMPLE_LEVEL - 2.5
save = saver(CLIPS, LEVEL, kind="physical model")
BEAT = P56.BEAT
FOLK = "Ach, du lieber Augustin"


def C(y) -> Clip:
    return Clip(np.asarray(y, float), SR)


def fade(y, a=0.005, r=0.08):
    y = np.array(y, float)
    ka, kr = max(int(a * SR), 1), max(int(r * SR), 1)
    y[:ka] *= np.linspace(0, 1, ka)[:, None] if y.ndim == 2 else np.linspace(0, 1, ka)
    y[len(y) - kr:] *= np.linspace(1, 0, kr)[:, None] if y.ndim == 2 else np.linspace(1, 0, kr)
    return y


def rms(y):
    return float(np.sqrt(np.mean(np.asarray(y, float) ** 2)) + 1e-20)


def at_db(y, db):
    return np.asarray(y, float) * 10 ** (db / 20) / rms(y)


_V: dict = {}


def session_mix(phrases=(0, 1), drop=()):
    """Part 56's session, mixed dry, in mono; ``drop`` leaves tracks out."""
    key = ("mix", phrases, drop)
    if key not in _V:
        s = P56.session(phrases)
        tr = {k: v for k, v in s["tracks"].items() if k in P56.TRACKS and k not in drop}
        y = sum(tr.values())
        _V[key] = y / np.max(np.abs(y))
    return _V[key]


def piano_line(pitches, beats, base=60, beat=BEAT, vel=0.9):
    """A melody (semitones above the tonic, beats) on Part 38's piano."""
    placed, t = [], 0.0
    for p, b in zip(pitches, beats):
        placed.append((P38.arr(P38.piano(base + p, b * beat * 0.95, vel)), t, 0.0))
        t += b * beat
    return mix(placed, duration=t + 1.0).y


def sung(pitches, beats, base=60, beat=BEAT, seed=1):
    notes, t = [], 0.0
    for p, b in zip(pitches, beats):
        notes.append((base + p, t, b * beat))
        t += b * beat
    v = CH.sing(notes, "soprano", "a", seed=seed)
    return v / np.max(np.abs(v))


def rhythm(n):
    """A plain rhythm for generated melodies: quarters, with a half note closing every eighth note."""
    return [2.0 if (i + 1) % 8 == 0 else 1.0 for i in range(n)]


_M: dict = {}


def model(exclude=()):
    key = tuple(exclude)
    if key not in _M:
        tunes = [m for m in M.corpus() if m.name not in exclude]
        _M[key] = M.NGram(2).fit(tunes)
    return _M[key]


def quartet(phrases=(0, 1), beat=BEAT * 1.15):
    """The Tune by a string quartet (Part 9's bowed string, four times): melody, a diatonic third below, the chord's
    fifth, the root."""
    key = ("quartet", phrases, round(beat, 3))
    if key in _V:
        return _V[key]
    notes = P56.tune_notes(phrases, base=72, beat=beat)
    scale = [0, 2, 4, 5, 7, 9, 11]
    placed = []
    for m, t, d in notes:
        placed.append((C(STR.bowed_note(440 * 2 ** ((m - 69) / 12), d * 0.98)), t, -2.0))
        pc = (m - 72) % 12
        i = scale.index(pc) if pc in scale else 0
        below = 72 + scale[(i - 2) % 7] - (12 if i < 2 else 0) + (m - 72) // 12 * 12
        placed.append((C(STR.bowed_note(440 * 2 ** ((below - 69) / 12), d * 0.98)), t, -7.0))
    syms = "".join(P56.CHORDS[p] for p in phrases)
    for i, sym in enumerate(syms):
        t0 = 2 * i * beat
        r = P56.ROOT[sym]
        for m_, g in ((55 + (r + 7 - 55) % 12, -8.0), (36 + r, -5.0)):
            placed.append((C(STR.bowed_note(440 * 2 ** ((m_ - 69) / 12), 2 * beat * 0.97)), t0, g))
    y = mix(placed).y
    _V[key] = y / np.max(np.abs(y))
    return _V[key]


def beat_track(seconds, bpm=100.0, four=True):
    """A new beat: kick on every beat, snare on 2 and 4, hats in eighths (Part 40's kit)."""
    b = 60.0 / bpm
    placed = []
    k = 0
    while k * b < seconds:
        placed.append((P38.arr(P40.kick()), k * b, 0.0 if k % 2 == 0 or four else -60.0))
        if k % 2 == 1:
            placed.append((P38.arr(P40.snare(k % 3)), k * b, -2.0))
        for h in range(2):
            placed.append((P38.arr(P40.hat()), k * b + h * b / 2, -8.0 if h else -5.0))
        k += 1
    return mix(placed, duration=seconds).y


# ---------------------------------------------------------------------------------------------- items
def compute_hook() -> dict:
    mdl = model()
    rng_seeds = range(4000)
    seen: dict = {}
    pair = None
    for s in rng_seeds:
        mel = mdl.generate(16, start=(), seed=s)
        key = tuple(mel[:8])
        if key in seen and seen[key][8:] != mel[8:] and len(set(key)) >= 4:
            pair = (seen[key], mel)
            break
        seen.setdefault(key, mel)
    a, b = pair
    r = rhythm(16)
    ya, yb = piano_line(a, r), piano_line(b, r)
    c = concat([C(fade(ya)), C(fade(yb))], gap=1.0, names=["first", "second"])
    return {"a": a, "b": b, "shared": 8, "tried": len(seen), "answer": "neither",
            "starts": {"first": float(c.events["first"]), "second": float(c.events["second"])},
            "clips": {"two": save("hook.two", c, detail="two melodies drawn independently from Part 14's model of folk melody (an order-2 n-gram), sharing their first eight notes by chance, on Part 38's piano")}}


def compute_melodies() -> dict:
    mdl = model()
    alphabet = len(mdl.alphabet)
    ks = list(range(3, 13))
    q = {k: B.collision(mdl, k) for k in ks}
    songs = 1e8
    windows = 60 - 8 + 1
    return {"alphabet": alphabet, "ks": ks, "q": {str(k): v for k, v in q.items()},
            "effective": {str(k): 1 / v for k, v in q.items()}, "uniform": {str(k): float(alphabet) ** k for k in ks},
            "pair_share8": B.shared_window_prob(q[8], windows, windows), "windows": windows,
            "birthday8": B.birthday(q[8], songs), "birthday12": B.birthday(q[12], songs), "songs": songs,
            "corpus": len(M.corpus())}


def compute_rights() -> dict:
    rec = session_mix((0, 1))
    tune = M.corpus([M.THE_TUNE])[0]
    k = sum(1 for e in P56.T.events(BEAT, [0, 1]))
    cover = piano_line(tune.pitches[:k], tune.beats[:k], base=60, beat=BEAT * 1.25)
    c = concat([C(fade(rec)), C(fade(cover))], gap=1.0, names=["recording", "cover"])
    return {"starts": {"recording": float(c.events["recording"]), "cover": float(c.events["cover"])},
            "clips": {"two": save("rights.two", c, detail="the Tune's first two phrases as recorded by Part 56's session, then the same composition played on Part 38's piano: one composition, two sound recordings")}}


def rate() -> float:
    p = B.population()
    return float(p.fees.sum() / p.plays.sum())


def compute_waterfall() -> dict:
    t = B.Terms()
    r = rate()
    indie = B.Terms(distributor=0.15, artist_royalty=0.97)
    return {"terms": t.__dict__, "month": B.waterfall(t.price, t), "rate": r,
            "million_label": B.per_million(r, t), "million_indie": B.per_million(r, indie),
            "per_stream_writer": B.per_million(r, t)["each songwriter"] / 1e6}


def compute_stream() -> dict:
    y = session_mix((0, 1, 2, 3, 4, 5))
    c = C(fade(y))
    c = Clip(c.y, SR, {"start": 0.0, "thirty": 30.0, "end": c.duration})
    return {"seconds": c.duration,
            "clips": {"thirty": save("stream.thirty", c, detail="the whole Tune by Part 56's session, about half a minute: a stream is counted after 30 seconds")}}


def compute_deals() -> dict:
    t = B.Terms()
    r = rate()
    label_rate = r * t.recording() / (1 - t.service)          # what the label receives per stream
    streams = np.linspace(0, 150e6, 151)
    deal = B.recoup(100_000.0, streams, label_rate, royalty=0.18, costs=50_000.0)
    indie_rate = label_rate * 0.85
    return {"label_rate": label_rate, "streams": streams.tolist(), "balance": deal["balance"].tolist(), "need": deal["need"],
            "label": deal["label"].tolist(), "indie": (streams * indie_rate).tolist(), "indie_rate": indie_rate,
            "advance": 100_000.0, "costs": 50_000.0, "royalty": 0.18,
            "label_breakeven": float((100_000.0 + 50_000.0) / (label_rate * (1 - 0.18)))}


def compute_pool() -> dict:
    p = B.population()
    a, b = B.pro_rata(p), B.user_centric(p)
    ga, gb = B.by_group(p, a), B.by_group(p, b)
    kinds = np.array(p.kinds)
    bot_fees = float(p.fees[kinds == "bot"].sum())
    streams_by_kind = {k: float(p.plays[kinds == k].sum()) for k in ("free", "heavy", "light", "bot")}
    fees_by_kind = {k: float(p.fees[kinds == k].sum()) for k in ("free", "heavy", "light", "bot")}
    users = {k: int((kinds == k).sum()) for k in ("free", "heavy", "light", "bot")}
    star = int(np.argmax(a[:20]))
    niche_med = int(20 + np.argsort(a[20:220])[100])
    return {"pro_rata": ga, "user_centric": gb, "pool": float(p.fees.sum()), "rate": float(p.fees.sum() / p.plays.sum()),
            "bot_fees": bot_fees, "streams_by_kind": streams_by_kind, "fees_by_kind": fees_by_kind, "users": users,
            "star": {"pro_rata": float(a[star]), "user_centric": float(b[star])},
            "niche": {"pro_rata": float(a[niche_med]), "user_centric": float(b[niche_med])},
            "change": {g: 100 * (gb[g] / ga[g] - 1) for g in ga}}


def compute_market() -> dict:
    ml = B.musiclab()
    mdl = model()
    songs = [mdl.generate(16, start=(), seed=10_000 + i) for i in range(48)]
    q = ml["quality"]
    rank = {int(i): int(r) + 1 for r, i in enumerate(np.argsort(-q))}
    w = ml["winners"]
    a_w, b_w = w[0], next(x for x in w[1:] if x != w[0])
    r = rhythm(16)
    c = concat([C(fade(piano_line(songs[a_w], r))), C(fade(piano_line(songs[b_w], r)))], gap=1.0, names=["one", "two"])
    shares = [sorted((float(s) for s in sh), reverse=True) for sh in ml["social"]]
    return {"gini_social": ml["gini_social"], "gini_independent": ml["gini_independent"], "U_social": ml["U_social"],
            "U_independent": ml["U_independent"], "winners": w, "winner_quality_rank": [rank[x] for x in w],
            "top_share_social": float(np.mean([s[0] for s in shares])),
            "top_share_independent": float(np.mean([max(s) for s in ml["independent"]])),
            "social": [list(map(float, s)) for s in ml["social"]], "independent": [list(map(float, s)) for s in ml["independent"]],
            "quality": list(map(float, q)), "pair": [int(a_w), int(b_w)], "pair_rank": [rank[a_w], rank[b_w]],
            "starts": {"one": float(c.events["one"]), "two": float(c.events["two"])},
            "clips": {"two": save("market.two", c, detail="the most downloaded song in two worlds of a simulated social-influence experiment: two of 48 melodies by Part 14's model, on Part 38's piano")}}


def compute_intro() -> dict:
    inst = session_mix((0, 1), drop=("vox",))
    full = session_mix((0, 1))
    n8 = int(16 * BEAT * SR)
    long = np.r_[inst[:n8], full]
    c = concat([C(fade(long)), C(fade(full))], gap=1.0, names=["long", "short"])
    return {"intro_s": 16 * BEAT, "starts": {"long": float(c.events["long"]), "short": float(c.events["short"])},
            "clips": {"two": save("intro.two", c, detail="Part 56's session: the Tune after a long instrumental introduction, then with the voice from the first beat")}}


def compute_live() -> dict:
    years = np.arange(1790, 2027, 4)
    rel = B.baumol(years, 0.02, 1790)
    q = quartet((0, 1))
    c = C(fade(q))
    tk = B.tickets()
    return {"years": years.tolist(), "relative": rel.tolist(), "rise_1966": float(B.baumol([2026], 0.02, 1966)[0]),
            "rise_1790": float(rel[-1]), "tickets": tk,
            "clips": {"quartet": save("live.quartet", c, detail="the Tune's first two phrases by a string quartet of Part 9's bowed-string models: four players and the same half minute, as in 1790")}}


def compute_similar() -> dict:
    tune = M.corpus([M.THE_TUNE])[0]
    k = 14
    p, r = tune.pitches[:k], tune.beats[:k]
    hook = load("hook")
    a, b = hook["a"][:8], hook["b"][:8]
    # the same contour, different intervals: every step kept in direction, sizes changed
    contour = [p[0]]
    rng = np.random.default_rng(3)
    for x, y in zip(p, p[1:]):
        d = y - x
        step = int(np.sign(d)) * int(rng.choice([1, 2, 3, 4])) if d else 0
        contour.append(contour[-1] + step)
    transposed = [x + 5 for x in p]
    segs = [piano_line(p, r), piano_line(transposed, r), piano_line(p, r), piano_line(contour, r)]
    c = concat([C(fade(s)) for s in segs], gap=0.7, names=["t1", "t2", "c1", "c2"])
    ints = lambda s: [y - x for x, y in zip(s, s[1:])]
    return {"tune": p, "transposed": transposed, "contour": contour,
            "match": {"transposed_notes": sum(x == y for x, y in zip(p, transposed)), "transposed_intervals": sum(x == y for x, y in zip(ints(p), ints(transposed))),
                      "contour_notes": sum(x == y for x, y in zip(p, contour)), "contour_intervals": sum(x == y for x, y in zip(ints(p), ints(contour))),
                      "contour_dirs": sum(np.sign(x) == np.sign(y) for x, y in zip(ints(p), ints(contour))), "n": k},
            "starts": {kk: float(c.events[kk]) for kk in ("t1", "t2", "c1", "c2")},
            "clips": {"pairs": save("similar.pairs", c, detail="the Tune's opening, then the same a fourth higher (every note different, every interval the same); the opening again, then a melody with its contour but other intervals; Part 38's piano")}}


def compute_sample() -> dict:
    rec = session_mix((1,))
    a, b = int(0 * BEAT * SR), int(4 * BEAT * SR)
    slice_ = rec[a:b] * np.r_[np.linspace(0, 1, 200), np.ones(b - a - 400), np.linspace(1, 0, 200)]
    bars = 4
    loop = np.tile(slice_, bars)
    secs = len(loop) / SR
    drums = beat_track(secs)
    sampled = 0.8 * loop / np.max(np.abs(loop)) + 0.5 * drums / np.max(np.abs(drums))
    # the same notes re-played: the phrase's chords and bass, by other hands (guitar and a new bass line, same harmony)
    syms = P56.CHORDS[1][:2]
    placed = []
    for rep in range(bars):
        for i, sym in enumerate(syms):
            t0 = rep * 4 * BEAT + 2 * i * BEAT
            tones = P56.chord_tones(sym)
            for kk in range(4):
                placed.append((P38.arr(P38.guitar(60 + tones[kk % 3], BEAT * 0.45)), t0 + kk * BEAT / 2, -3.0))
            placed.append((P38.arr(P38.bass(36 + P56.ROOT[sym], BEAT * 1.8)), t0, 0.0))
        tn = P56.tune_notes((1,), base=72)[:6]
        for m_, t_, d_ in tn:
            if t_ < 4 * BEAT:
                placed.append((P38.arr(P38.piano(m_, d_ * 0.95, 0.8)), rep * 4 * BEAT + t_, -3.0))
    replayed = mix(placed, duration=secs).y
    replayed = 0.8 * replayed / np.max(np.abs(replayed)) + 0.5 * drums / np.max(np.abs(drums))
    c = concat([C(fade(sampled)), C(fade(replayed))], gap=1.0, names=["first", "second"])
    return {"answer": "first", "loop_s": len(slice_) / SR, "starts": {"first": float(c.events["first"]), "second": float(c.events["second"])},
            "clips": {"two": save("sample.two", c, detail="a new beat (Part 40's kit) under four beats of Part 56's recording looped, then under the same harmony and melody re-played on guitar, bass and piano")}}


def compute_ai() -> dict:
    folk = M.corpus([FOLK])[0]
    mdl = model(exclude=(FOLK,))
    n = 16
    new = mdl.generate(n, start=(folk.pitches[0],), seed=7)
    r = folk.beats[:n]
    old = folk.pitches[:n]
    ya, yb = sung(new, r, seed=3), sung(old, r, seed=3)
    c = concat([C(fade(ya)), C(fade(yb))], gap=1.0, names=["first", "second"])
    s_new = float(np.mean(mdl.surprise(new)))
    s_old = float(np.mean(mdl.surprise(old)))
    return {"answer": "first", "folk": FOLK, "new": new, "old": old, "surprise_new": s_new, "surprise_old": s_old,
            "starts": {"first": float(c.events["first"]), "second": float(c.events["second"])},
            "clips": {"two": save("ai.two", c, detail=f"Part 8's voice singing a new melody by Part 14's model (trained on the series' folk corpus without '{FOLK}'), then the opening of '{FOLK}' in the same rhythm")}}


def compute_tune60() -> dict:
    rec = session_mix((0, 1))
    cover = quartet((0, 1))
    rec1 = session_mix((1,))
    b = int(4 * BEAT * SR)
    sl = rec1[:b] * np.r_[np.linspace(0, 1, 200), np.ones(b - 400), np.linspace(1, 0, 200)]
    loop = np.tile(sl, 4)
    drums = beat_track(len(loop) / SR)
    remix = 0.75 * loop / np.max(np.abs(loop)) + 0.55 * drums / np.max(np.abs(drums))
    c = concat([C(fade(rec)), C(fade(cover)), C(fade(remix))], gap=0.9, names=["original", "cover", "remix"])
    r = rate()
    t = B.Terms()
    total = 1e6 * r
    rec_share = total * t.recording() / (1 - t.service)
    comp_share = total * t.publishing / (1 - t.service)
    rows = {
        "original": {"recording": rec_share, "composition": comp_share, "to_us": rec_share + comp_share, "melody": 0.0},
        "cover": {"recording": rec_share, "composition": comp_share, "to_us": 0.0, "melody": 0.0},
        "remix": {"recording": rec_share, "composition": comp_share, "to_us": 0.5 * rec_share + 0.5 * comp_share, "melody": 0.0},
    }
    return {"names": ["original", "cover", "remix"], "per_million": total, "rows": rows, "seconds": c.duration,
            "starts": {k: float(c.events[k]) for k in ("original", "cover", "remix")},
            "clips": {"variation60": save("tune.variation60", c, detail="Variation 60: the Tune as recorded by Part 56's session; covered by a string quartet of Part 9's bowed strings; and four beats of the recording sampled and looped under a new beat")}}


def compute_variation() -> dict:
    t = load("tune60")
    return {"part": 60, "title": "the Tune's family of copyrights: a recording, a cover, a remix",
            "seconds": round(t["seconds"], 1),
            "measure": f"a million streams each: {t['per_million']:,.0f} dollars to rights holders; the remix pays us half; the unknown composer of 1761, nothing",
            "clip": "tune.variation60"}


def compute_signoff() -> dict:
    """The part's last sound: the opening of its Variation, under the next part's title."""
    load("variation")
    return signoff(CLIPS, "tune.variation60", 60)


ITEMS = {"hook": compute_hook, "melodies": compute_melodies, "rights": compute_rights, "waterfall": compute_waterfall,
         "stream": compute_stream, "deals": compute_deals, "pool": compute_pool, "market": compute_market,
         "intro": compute_intro, "live": compute_live, "similar": compute_similar, "sample": compute_sample,
         "ai": compute_ai, "tune60": compute_tune60, "variation": compute_variation,
         "signoff": compute_signoff}

if __name__ == "__main__":
    CACHE.main(ITEMS, __doc__)
