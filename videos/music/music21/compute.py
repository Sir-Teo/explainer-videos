"""Precompute everything numerical, and every sound, in Part 21 of *Music, Built* ("Form").

    python -m videos.music.music21.compute              # everything missing (a few minutes)
    python -m videos.music.music21.compute --force sonata

Numbers are cached in ``.cache/music21/<name>.json``, sounds in ``.cache/music21/audio/``.  The form tools are
Monochord's (``explainer/music/monochord/form.py``); the pieces are composed here from the Tune and played on Part 7's
piano; the looped phrase of the hook is spoken by the series' own narrator voice.  Published findings are cited in the
README.

Items:
    hook        a spoken phrase, looped (the speech-to-song illusion)
    phrase      a sentence and a period on the Tune (an ear question)
    forms       binary, ternary, rondo, variations, AABA and verse-chorus plans, as self-similarity matrices
    tune        the Tune with its harmony: chroma from the notes and from the sound, self-similarity, novelty
    rondo       a rondo on the Tune, heard
    sonata      a miniature sonata on the Tune (Variation 21): its keys over time, its sections found from the sound
    blues       a twelve-bar blues on the Tune's head
    segment     the segmenter scored on every piece of this part
    repetition  how much of each of Part 14's tunes repeats itself, against shuffled tunes
    golden      climaxes and the golden section; the base rate of a hit
    closure     two short pieces, one ending at home and one away (an ear question)
    variation   the Variations ledger, row 21
"""

from __future__ import annotations

import numpy as np

from explainer.ai.cache import Cache
from explainer.music.monochord import EXAMPLE_LEVEL, SR, Clip, ClipStore, concat, mix
from explainer.music.monochord import form as FM
from explainer.music.monochord import fourpart as F
from explainer.music.monochord import key as KY
from explainer.music.monochord import melody as M
from explainer.music.monochord.instruments import strings as STR
from explainer.music.monochord.partkit import saver, signoff
from explainer.music.monochord.physics.string import String

CACHE = Cache("music21")
CLIPS = ClipStore("music21")
load = CACHE.load

LEVEL = EXAMPLE_LEVEL - 2.5
save = saver(CLIPS, LEVEL, kind="physical model")
BOARD = STR.soundboard()
C4 = 261.6255653005986
_NOTES: dict = {}
BEAT = 0.36                                           # seconds to a beat
MAJ = (0, 2, 4, 5, 7, 9, 11)


def hz(m: float) -> float:
    return 440.0 * 2.0 ** ((m - 69) / 12.0)


def piano(m: float, seconds: float, velocity: float = 1.4) -> Clip:
    key = (round(m, 3), round(seconds, 3), velocity)
    if key not in _NOTES:
        f = hz(m)
        y = BOARD.play(STR.struck(String.tuned(f, L=0.62 * (C4 / f) ** 0.8, mu=6.34e-3, kappa=1.25, sigma0=0.6, sigma1=3.3e-4), velocity=velocity, seconds=seconds + 0.3))
        _NOTES[key] = Clip(np.asarray(y, dtype=float)).fade(0.001, 0.2).at_level(LEVEL)
    return _NOTES[key]


# ---------------------------------------------------------------------------
# Pieces: sections of melody (key numbers and beats) over chords (pitch classes and a bass), a chord every two beats
# ---------------------------------------------------------------------------
CH = {"C": ((0, 4, 7), 48), "Dm": ((2, 5, 9), 50), "Em": ((4, 7, 11), 52), "F": ((5, 9, 0), 53), "G": ((7, 11, 2), 43),
      "G7": ((7, 11, 2, 5), 43), "Am": ((9, 0, 4), 45), "D": ((2, 6, 9), 50), "D7": ((2, 6, 9, 0), 50), "E": ((4, 8, 11), 52),
      "Bb": ((10, 2, 5), 46), "Gm": ((7, 10, 2), 43), "A": ((9, 1, 4), 45), "C7": ((0, 4, 7, 10), 48), "F7": ((5, 9, 0, 3), 53)}


def voice(prev, pcs, bass, lo=50, hi=67):
    keys = [m for m in range(max(lo, bass + 1), hi + 1) if m % 12 in pcs]
    best, bc = None, 1e9
    for t in keys:
        for a in keys:
            if a <= t or a - t > 9:
                continue
            for s in keys:
                if s <= a or s - a > 9:
                    continue
                if not {s % 12, a % 12, t % 12, bass % 12} >= set(pcs[:3]):
                    continue
                cand = (s, a, t, bass)
                c = sum(abs(x - y) for x, y in zip(cand[:3], prev[:3])) + 30 * len(F.parallels(prev, cand))
                if c < bc:
                    best, bc = cand, c
    return best


def section(name, melody, chords):
    """A section: melody [(midi, beats)], chords one per two beats (names in ``CH``)."""
    total = sum(d for _, d in melody)
    assert abs(total - 2 * len(chords)) < 1e-9, (name, total, len(chords))
    return {"name": name, "melody": [(int(p), float(d)) for p, d in melody], "chords": list(chords)}


def deg(seq, tonic: int, base: int = 72):
    """Scale degrees (1-7, '+' an octave up, '-' down; '#'/'b' alterations) with durations -> (midi, beats)."""
    out = []
    for item in seq.split():
        tok, _, dur = item.partition("*")
        octave = tok.count("+") - tok.count("-")
        alter = tok.count("#") - tok.count("b")
        d = int(tok.strip("+-#b"))
        out.append((base + tonic + MAJ[d - 1] + 12 * octave + alter, float(dur) if dur else 1.0))
    return out


def render(sections, beat: float = BEAT, tail: float = 1.4) -> tuple[Clip, list, list]:
    """Play sections in order: the melody over block chords voiced the shortest way.  Returns the clip, the note events
    (midi, onset, duration in beats) and the section starts in beats."""
    placed, events, starts, t, prev = [], [], [], 0.0, (64, 60, 55, 48)
    ev = {}
    for s in sections:
        starts.append(t)
        ev[f"s{len(starts) - 1}"] = t * beat
        a = t
        for p, d in s["melody"]:
            placed.append((piano(p, d * beat * 1.05), a * beat, 0.0))
            events.append((p, a, d))
            a += d
        for k, c in enumerate(s["chords"]):
            pcs, bass = CH[c]
            v = voice(prev, list(pcs), bass) or (64, 60, 55, bass)
            prev = v
            for j, m in enumerate(v):
                placed.append((piano(m, 2 * beat * 1.05, velocity=1.1), (t + 2 * k) * beat, -6.0))
                events.append((m, t + 2 * k, 2.0))
        t += 2 * len(s["chords"])
    ev["end"] = t * beat
    return Clip(mix(placed, duration=t * beat + tail).y, SR, ev, []), events, starts


def tune_sections():
    """The Tune with harmony: its six phrases."""
    A = section("A", deg("1 1 5 5 6 6 5*2", 0), ["C", "C", "F", "G"])
    A2 = section("A'", deg("4 4 3 3 2 2 1*2", 0), ["F", "C", "G", "C"])
    B = section("B", deg("5 5 4 4 3 3 2*2", 0), ["C", "F", "C", "G"])
    return [A, A2, B, dict(B, name="B"), dict(A, name="A"), dict(A2, name="A'")]


def sonata_sections():
    """A miniature sonata on the Tune: exposition (first theme in C, transition, second theme in G: the first phrase
    inverted, closing), development (the head sequenced through A minor, F and D minor, then the dominant), and
    recapitulation (everything in C)."""
    T1 = [section("first theme", deg("1 1 5 5 6 6 5*2", 0) + deg("4 4 3 3 2 2 1*2", 0), ["C", "C", "F", "G", "F", "C", "G", "C"])]
    TR = [section("transition", deg("5 5 #4 #4 3 3 2*2", 0), ["C", "D7", "C", "D"])]
    T2 = [section("second theme", [(79, 1.0), (79, 1.0), (72, 1.0), (72, 1.0), (71, 1.0), (71, 1.0), (72, 2.0),
                                   (74, 1.0), (74, 1.0), (76, 1.0), (76, 1.0), (78, 1.0), (78, 1.0), (79, 2.0)],
                  ["G", "C", "G", "C", "G", "C", "D", "G"])]
    CL = [section("closing", [(83, 1.0), (83, 1.0), (81, 1.0), (81, 1.0), (79, 2.0), (79, 2.0)], ["G", "D7", "G", "G"])]
    DEV = [section("development: A minor", [(81, 1.0), (81, 1.0), (76, 1.0), (76, 1.0), (77, 1.0), (77, 1.0), (76, 2.0)], ["Am", "Am", "Dm", "E"]),
           section("development: F major", [(77, 1.0), (77, 1.0), (72, 1.0), (72, 1.0), (74, 1.0), (74, 1.0), (72, 2.0)], ["F", "F", "Bb", "C"]),
           section("development: D minor", [(74, 1.0), (74, 1.0), (81, 1.0), (81, 1.0), (82, 1.0), (82, 1.0), (81, 2.0)], ["Dm", "Dm", "Gm", "A"]),
           section("retransition", [(79, 1.0), (79, 1.0), (77, 1.0), (77, 1.0), (76, 1.0), (76, 1.0), (74, 2.0)], ["G7", "G7", "G7", "G7"])]
    R1 = [section("first theme", T1[0]["melody"], T1[0]["chords"])]
    RTR = [section("transition", deg("5 5 4 4 3 3 2*2", 0), ["C", "G7", "C", "G"])]
    R2 = [section("second theme", [(72, 1.0), (72, 1.0), (77, 1.0), (77, 1.0), (76, 1.0), (76, 1.0), (77, 2.0), (67, 1.0), (67, 1.0), (69, 1.0), (69, 1.0), (71, 1.0), (71, 1.0), (72, 2.0)],
                  ["C", "F", "C", "F", "C", "F", "G", "C"])]
    RCL = [section("closing", [(76, 1.0), (76, 1.0), (74, 1.0), (74, 1.0), (72, 2.0), (72, 2.0)], ["C", "G7", "C", "C"])]
    return T1 + TR + T2 + CL + DEV + R1 + RTR + R2 + RCL


# ---------------------------------------------------------------------------
def compute_hook() -> dict:
    from scipy.signal import resample_poly
    from explainer import tts
    phrase = "sometimes behave so strangely"
    u = tts.synthesize(phrase)
    import soundfile as sf
    y, sr = sf.read(str(u.audio_path))
    if y.ndim == 2:
        y = y.mean(axis=1)
    y = resample_poly(y, SR, sr) if sr != SR else y
    y = y / (np.max(np.abs(y)) + 1e-9) * 0.5
    n = 10
    gap = 0.55
    placed, ev = [], {}
    L = len(y) / SR
    for k in range(n):
        placed.append((Clip(y).fade(0.005, 0.03), k * (L + gap), 0.0))
        ev[f"r{k}"] = k * (L + gap)
    c = Clip(mix(placed, duration=n * (L + gap) + 0.5).y, SR, ev, [])
    s = save("hook.speech", c, kind="synthesized", detail="a spoken phrase, the series' narrator's synthesized voice, repeated ten times")
    return {"phrase": phrase, "repeats": n, "seconds_each": L + gap, "clips": {"speech": s}}


def compute_phrase() -> dict:
    sentence = section("sentence", deg("1 1 5 5 1 1 5 5 6 5 4 3 2*2 1*2", 0), ["C", "C", "C", "G", "F", "C", "G", "C"])
    period = section("period", deg("1 1 5 5 6 6 5*2 4 4 3 3 2 2 1*2", 0), ["C", "C", "F", "G", "F", "C", "G", "C"])
    cs, evs, _ = render([sentence])
    cp, evp, _ = render([period])
    s = concat([cs.at_level(LEVEL), cp.at_level(LEVEL)], gap=1.4, names=["A", "B"])
    return {"A": {"melody": sentence["melody"], "chords": sentence["chords"], "name": "sentence"},
            "B": {"melody": period["melody"], "chords": period["chords"], "name": "period"},
            "starts": {k: float(s.events[k]) for k in "AB"}, "beat": BEAT,
            "clips": {"two": save("phrase.two", s, level=None, detail="a sentence, then a period, on the Tune's opening: Part 7's piano")}}


def plan_events(plan: str, material: dict):
    secs = [material[x] for x in plan.split()]
    _, ev, starts = render(secs)
    return ev, starts


def material():
    tA = tune_sections()
    A = section("A", tA[0]["melody"] + tA[1]["melody"], tA[0]["chords"] + tA[1]["chords"])
    B = section("B", deg("3 3 4 4 5 5 3*2 2 2 3 3 4 4 2*2", 7, base=60), ["G", "C", "G", "G", "D", "G", "D7", "D"])   # in G
    C = section("C", deg("3 3 4 5 5 4 3 2 1 1 2 3 3*1.5 2*.5 2*2", 5, base=60), ["F", "C7", "F", "C7", "F", "F", "C7", "C7"])
    A1 = section("A1", deg("1 3 5 3 6 4 5*2 4 2 3 1 2 7- 1*2", 0), A["chords"])
    A2 = section("A2", deg("1*.5 1*.5 1 5*.5 5*.5 5 6*.5 6*.5 6 5*2", 0) + deg("4*.5 4*.5 4 3*.5 3*.5 3 2*.5 2*.5 2 1*2", 0), A["chords"])
    return {"A": A, "B": B, "C": C, "A1": A1, "A2": A2}


PLANS = {"binary": "A A B B", "ternary": "A B A", "rondo": "A B A C A", "variations": "A A1 A2 A1",
         "AABA": "A A B A", "verse-chorus": "C A C A B A"}


HEARD = {"binary": "forms.binary", "ternary": "forms.ternary", "variations": "forms.variations", "AABA": "forms.aaba"}


def compute_forms() -> dict:
    mat = material()
    out, clips = {}, {}
    for name, plan in PLANS.items():
        clip, ev, starts = render([mat[x] for x in plan.split()])
        C = FM.smooth(FM.chroma_notes(ev, step=1.0), 4)
        S = FM.ssm(C)
        out[name] = {"plan": plan, "starts": starts, "ssm": np.round(S, 3).tolist(), "beats": int(C.shape[1]), "beat": BEAT}
        if name in HEARD:
            clips[name] = save(HEARD[name], concat([clip.at_level(LEVEL)], gap=0.0, names=[name]), level=None,
                               detail=f"a {name} piece on the Tune ({plan}): Part 7's piano")
    out["clips"] = clips
    return out


def audio_form(clip: Clip, beat: float = BEAT, L: int = 8, threshold: float = 0.15, min_gap: int = 6):
    """Chroma from the sound, a column a beat (frames averaged), its self-similarity, novelty and boundaries (beats)."""
    t, Ca = FM.chroma_audio(clip.y, SR, hop=beat / 4)
    nb = int(round(clip.events["end"] / beat))
    C = np.zeros((12, nb))
    for b in range(nb):
        cols = (t >= b * beat) & (t < (b + 1) * beat)
        if cols.any():
            C[:, b] = Ca[:, cols].mean(axis=1)
    S = FM.ssm(C)
    nov = FM.novelty(S, L=L)
    found = FM.peaks(nov, min_gap=min_gap, threshold=threshold)
    return S, nov, found


def compute_tune() -> dict:
    secs = tune_sections()
    clip, ev, starts = render(secs)
    Cn = FM.smooth(FM.chroma_notes(ev, step=1.0), 2)
    Sn = FM.ssm(Cn)
    mel, t = [], 0.0
    for s_ in secs:
        for p_, d_ in s_["melody"]:
            mel.append((p_, t, d_))
            t += d_
    Sm = FM.ssm(FM.chroma_notes(mel, step=1.0))
    S, nov, found = audio_form(clip, L=4, threshold=0.25, min_gap=4)
    truth = [int(round(x)) for x in starts[1:]]
    labels = FM.label_sections(Sn, truth, threshold=0.9)
    nov_wide = FM.novelty(S, L=12)
    s = save("tune.harmony", concat([clip.at_level(LEVEL)], gap=0.0, names=["tune"]), level=None, detail="the Tune with its harmony: Part 7's piano")
    return {"ssm_melody": np.round(Sm, 3).tolist(), "ssm_notes": np.round(Sn, 3).tolist(), "ssm_audio": np.round(S, 3).tolist(), "novelty": np.round(nov, 4).tolist(), "novelty_wide": np.round(nov_wide, 4).tolist(),
            "found": found, "truth": truth, "labels": labels, "letters": [x["name"] for x in secs], "beat": BEAT,
            "score": FM.boundary_score(found, truth, tol=2), "clips": {"harmony": s}}


def compute_rondo() -> dict:
    mat = material()
    secs = [mat[x] for x in PLANS["rondo"].split()]
    clip, ev, starts = render(secs)
    s = concat([clip.at_level(LEVEL)], gap=0.0, names=["rondo"])
    return {"plan": PLANS["rondo"], "starts": [float(x) for x in starts], "events": [[int(p), float(a), float(d)] for p, a, d in ev], "beat": BEAT,
            "clips": {"rondo": save("rondo.five", s, level=None, detail="a rondo on the Tune: A B A C A (C is Ode to Joy's opening, in F): Part 7's piano")}}


def compute_sonata() -> dict:
    secs = sonata_sections()
    clip, ev, starts = render(secs)
    S, nov, found = audio_form(clip, L=8, threshold=0.25, min_gap=8)
    truth = change_bounds(secs, starts)
    total = int(round(clip.events["end"] / BEAT))
    # keys over time from the notes: Part 15's key finder on a sliding window of eight beats
    keys = []
    for t0 in range(0, total, 2):
        d = np.zeros(12)
        for p, a, du in ev:
            ov = min(a + du, t0 + 8) - max(a, t0)
            if ov > 0:
                d[p % 12] += ov
        r = KY.ranking(d / d.sum())
        keys.append({"t": t0, "key": KY.key_name(r[0][0]), "r": float(r[0][1])})
    big = {"exposition": [0, starts[4]], "development": [starts[4], starts[8]], "recapitulation": [starts[8], total]}
    s = concat([clip.at_level(LEVEL)], gap=0.0, names=["sonata"])
    return {"names": [x["name"] for x in secs], "starts": [float(x) for x in starts], "total": total, "big": big,
            "events": [[int(p), float(a), float(d)] for p, a, d in ev], "keys": keys,
            "ssm": np.round(S, 3).tolist(), "novelty": np.round(nov, 4).tolist(), "found": found, "truth": truth,
            "score": FM.boundary_score(found, truth, tol=2), "score_big": FM.boundary_score(found, [int(starts[4]), int(starts[8])], tol=2),
            "golden": {"exposition": starts[4] / total, "rest": 1 - starts[4] / total},
            "beat": BEAT, "seconds": clip.duration,
            "clips": {"sonata": save("sonata.whole", s, level=None, detail="a miniature sonata on the Tune, its second theme the first phrase inverted: Part 7's piano")}}


def compute_blues() -> dict:
    bars = ["C", "C", "C", "C", "F", "F", "C", "C", "G", "F", "C", "C"]
    shift = {"C": 0, "F": 5, "G": 7}
    secs = []
    for k, b in enumerate(bars):
        riff = [(72 + shift[b] + x, d) for x, d in ((0, 1), (0, 1), (7, 1), (10, 1))] if k % 2 == 0 else [(72 + shift[b] + 9, 1.0), (72 + shift[b] + 7, 1.0), (72 + shift[b] + 3, 2.0)]
        riff = [(p - 12 if p > 84 else p, d) for p, d in riff]
        ch = {"C": "C7", "F": "F7", "G": "G7"}[b]
        secs.append(section(f"bar {k + 1}", riff, [ch, ch]))
    clip, ev, starts = render(secs, beat=0.3)
    s = concat([clip.at_level(LEVEL)], gap=0.0, names=["blues"])
    return {"bars": bars, "starts": [float(x) for x in starts], "beat": 0.3,
            "clips": {"twelve": save("blues.twelve", s, level=None, detail="a twelve-bar blues on the Tune's head: Part 7's piano")}}


def change_bounds(secs, starts):
    """Boundaries where the material changes (a section unlike the one before), in beats."""
    names = [x["name"] for x in secs]
    return [int(round(starts[i])) for i in range(1, len(secs)) if names[i] != names[i - 1]]


def compute_segment() -> dict:
    mat = material()
    out = {}
    for name, plan in list(PLANS.items()) + [("sonata", None)]:
        secs = sonata_sections() if name == "sonata" else [mat[x] for x in plan.split()]
        clip, ev, starts = render(secs)
        truth = change_bounds(secs, starts)
        res = {}
        for L in (4, 8, 12):
            _, nov, found = audio_form(clip, L=L, threshold=0.25, min_gap=L)
            res[str(L)] = {"found": found, **FM.boundary_score(found, truth, tol=2)}
        out[name] = {"truth": truth, "by_width": res}
    summary = {}
    for L in ("4", "8", "12"):
        hits = sum(v["by_width"][L]["hits"] for v in out.values())
        nf = sum(len(v["by_width"][L]["found"]) for v in out.values())
        nt = sum(len(v["truth"]) for v in out.values())
        summary[L] = {"precision": hits / nf, "recall": hits / nt, "f": 2 * hits / (nf + nt), "hits": hits, "found": nf, "truth": nt}
    best = max(summary, key=lambda k: summary[k]["f"])
    return {"pieces": out, "summary": summary, "best_width": best}


def compute_repetition() -> dict:
    ts = M.corpus()
    rows_ = []
    for m in ts:
        rows_.append({"name": m.name, "share": FM.repeated_share(m.pitches, m.beats), "shuffled": FM.shuffled_share(m.pitches, m.beats, trials=100),
                      "letters": FM.form_letters(m)})
    real = [r["share"] for r in rows_]
    shuf = [r["shuffled"] for r in rows_]
    return {"tunes": rows_, "mean": float(np.mean(real)), "mean_shuffled": float(np.mean(shuf)), "median": float(np.median(real)),
            "tune": next(r for r in rows_ if r["name"] == M.THE_TUNE)}


def compute_golden() -> dict:
    ts = M.corpus()
    cp = FM.climax_positions(ts)
    hits = FM.golden_hits(cp, tol=0.02)
    rng = np.random.default_rng(21)
    sim = rng.uniform(0.5, 0.75, size=200_000)
    return {"positions": cp, "hits": hits, "n": len(cp), "expected_uniform": len(cp) * 0.04,
            "base_rate": FM.golden_base_rate(0.5, 0.75, 0.02), "base_rate_sim": float(np.mean(np.abs(sim - FM.PHI) <= 0.02)),
            "phi": FM.PHI, "in_first_half": sum(1 for x in cp if x < 0.5)}


def compute_closure() -> dict:
    home = [section("A", deg("1 1 5 5 6 6 5*2", 0), ["C", "C", "F", "G"]), section("B", deg("5 5 #4 #4 3 3 2*2", 0), ["C", "D7", "C", "D"]),
            section("C", deg("4 4 3 3 2 2 1*2", 0), ["F", "C", "G", "C"])]
    away = [home[0], home[1], section("C", [(79, 1.0), (79, 1.0), (78, 1.0), (78, 1.0), (76, 1.0), (74, 1.0), (79, 2.0)], ["G", "D", "D7", "G"])]
    ch, _, _ = render(home)
    ca, _, _ = render(away)
    s = concat([ca.at_level(LEVEL), ch.at_level(LEVEL)], gap=1.4, names=["A", "B"])
    return {"A": "away (ends in G)", "B": "home (ends in C)", "starts": {k: float(s.events[k]) for k in "AB"}, "beats": 24,
            "clips": {"two": save("closure.two", s, level=None, detail="two short pieces on the Tune: one ends in G, one returns to C: Part 7's piano")}}


def compute_variation() -> dict:
    s = load("sonata")
    sc = s["score"]
    return {"part": 21, "title": r"as a miniature sonata whose second theme is its own first phrase, inverted", "seconds": round(s["seconds"], 2),
            "measure": rf"its {len(s['truth'])} section boundaries found from the sound alone: {sc['hits']} within two beats",
            "clip": "sonata.whole"}


def compute_signoff() -> dict:
    """The part's last sound: the opening of its Variation, under the next part's title."""
    load("variation")
    return signoff(CLIPS, "sonata.whole", 21)


ITEMS = {"hook": compute_hook, "phrase": compute_phrase, "forms": compute_forms, "tune": compute_tune, "rondo": compute_rondo,
         "sonata": compute_sonata, "blues": compute_blues, "segment": compute_segment, "repetition": compute_repetition,
         "golden": compute_golden, "closure": compute_closure, "variation": compute_variation,
         "signoff": compute_signoff}


if __name__ == "__main__":
    CACHE.main(ITEMS, __doc__)
