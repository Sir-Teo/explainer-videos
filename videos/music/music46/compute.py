"""Precompute everything numerical, and every sound, in Part 46 of *Music, Built* ("Expectation and Emotion").

    python -m videos.music.music46.compute              # everything missing (about two minutes)
    python -m videos.music.music46.compute --force corpus

Numbers are cached in ``.cache/music46/<name>.json``, sounds in ``.cache/music46/audio/``.  The tools are Monochord's
(``explainer/music/monochord/listener.py``).  The listener is trained on the series' corpus of folk and public-domain
tunes (Part 14), leaving out whichever tune it is listening to.  Sounds: Part 7's piano and Part 38's bass (physical
models), the additive orchestra, Part 40's drums, sine tones.  Published findings (Salimpoor, Cheung, Witek, Juslin) are
quoted, not reproduced; the model's numbers are its own.

Items:
    hook        an ear question: three endings for the Tune's last phrase; which did the listener find most surprising?
    tune        the Tune note by note: surprise and uncertainty
    corpus      every note of the corpus, each tune heard by a model trained on the others
    compare     mean surprise and uncertainty across melodies: the Tune, Ode to Joy, Part 42's drafts and chains, random
    learn       an ear question: a stream of tone 'words', then a word and a part-word
    endings     Variation 46's three endings, note by note
    groove      four drum patterns of rising syncopation
    emotion     an ear question: the Tune in four expressive settings
    tune46      Variation 46: the Tune with three endings: expected, delayed, denied
    variation   the Variations ledger, row 46
"""

from __future__ import annotations

import json
from pathlib import Path

import numpy as np

from explainer.ai.cache import Cache
from explainer.music.monochord import EXAMPLE_LEVEL, SR, Clip, ClipStore, concat, mix
from explainer.music.monochord import listener as L
from explainer.music.monochord import melody as M
from explainer.music.monochord import orchestra as O
from explainer.music.monochord import tune as T
from explainer.music.monochord.partkit import saver, signoff
from videos.music.music38 import compute as P38
from videos.music.music40 import compute as P40

CACHE = Cache("music46")
CLIPS = ClipStore("music46")
load = CACHE.load
LEVEL = EXAMPLE_LEVEL - 2.5
save = saver(CLIPS, LEVEL, kind="physical model")
save_synth = saver(CLIPS, LEVEL, kind="synthesized")
arr = P38.arr
piano, bass = P38.piano, P38.bass
TUNES = [t for t in M.corpus() if t.mode == "major"]
THE = [t for t in TUNES if t.name == M.THE_TUNE][0]
MAJOR = {1: 0, 2: 2, 3: 4, 4: 5, 5: 7, 6: 9, 7: 11}


def listener_without(name=None, order=4):
    return L.Listener([t.pitches for t in TUNES if t.name != name], order)


def sine(m, seconds):
    t = np.arange(int(seconds * SR)) / SR
    return np.clip(t / 0.01, 0, 1) * np.clip((seconds - t) / 0.02, 0, 1) * np.sin(2 * np.pi * 440 * 2 ** ((m - 69) / 12) * t)


def play_line(notes, beat=0.42, base=60, vel=0.7, chords=None, tail=1.2):
    """notes: (pitch relative to the tonic, beats); chords: (root relative to tonic, beats) for a bass."""
    p, t = [], 0.0
    for m, b in notes:
        p.append((arr(piano(base + m, b * beat * 0.97, vel)), t, 0.0))
        t += b * beat
    if chords:
        tc = 0.0
        for r, b in chords:
            p.append((arr(bass(base - 12 + r, b * beat * 0.9)), tc, -4.0))
            tc += b * beat
    return Clip(mix(p, duration=t + tail).y, SR)


LAST_PHRASE = [(5, 1), (5, 1), (4, 1), (4, 1), (2, 1), (2, 1)]         # F F E E D D, then the ending
CHORDS_LAST = [(5, 2), (0, 2), (7, 2)]


# ---------------------------------------------------------------------------------------------------------- items
def compute_hook() -> dict:
    lis = listener_without(M.THE_TUNE)
    context = THE.pitches[:-1]
    ends = {"C": 0, "A": 9, "F sharp": 6}
    ics = {k: lis.listen(context + [v])["ic"][-1] for k, v in ends.items()}
    order = ["A", "C", "F sharp"]
    clips = []
    for k in order:
        notes = LAST_PHRASE + [(ends[k], 2)]
        ch = CHORDS_LAST + [({"C": 0, "A": 9, "F sharp": 2}[k], 2)]
        clips.append(play_line(notes, chords=ch))
    c = concat(clips, gap=0.9, names=order)
    top = lis.expect(context, 5)
    return {"order": order, "ics": ics, "endings": ends, "answer": max(ics, key=ics.get), "expected": [[int(a), float(b)] for a, b in top],
            "starts": {k: float(c.events[k]) for k in order},
            "clips": {"three": save("hook.three", c, detail="the Tune's last phrase with three endings: on A over A minor, on C over C, on F sharp over D; Part 7's piano and a plucked bass")}}


def compute_tune() -> dict:
    lis = listener_without(M.THE_TUNE)
    r = lis.listen(THE.pitches)
    ev = T.events(0.42)
    notes = [(MAJOR[e["degree"]], e["dur"]) for e in ev]
    c = play_line(notes)
    return {"pitches": THE.pitches, "beats": THE.beats, "ic": r["ic"], "entropy": r["entropy"], "mean_ic": r["mean_ic"],
            "mean_entropy": r["mean_entropy"], "onsets": [e["t"] for e in ev],
            "clips": {"tune": save("tune.plain", c, detail="the Tune; Part 7's piano")}}


def compute_corpus() -> dict:
    pts = []
    per = {}
    for t in TUNES:
        lis = listener_without(t.name)
        r = lis.listen(t.pitches)
        per[t.name] = {"mean_ic": r["mean_ic"], "mean_entropy": r["mean_entropy"], "n": len(t.pitches)}
        pts += list(zip(r["entropy"], r["ic"]))
    pts = np.array(pts)
    return {"tunes": len(TUNES), "notes": int(len(pts)), "entropy": pts[:, 0].tolist(), "ic": pts[:, 1].tolist(), "per": per,
            "corr": float(np.corrcoef(pts[:, 0], pts[:, 1])[0, 1]), "mean_ic": float(pts[:, 1].mean()), "mean_entropy": float(pts[:, 0].mean())}


def _rel(keys):
    """Key numbers in C to pitches relative to the tonic C, in the octave nearest the corpus's."""
    base = 60 if np.mean(keys) < 70 else 72
    return [int(k - base) for k in keys]


def compute_compare() -> dict:
    lis = listener_without(None)
    rows = {}
    rows["the Tune"] = listener_without(M.THE_TUNE).listen(THE.pitches)
    ode = [t for t in TUNES if t.name == "Ode to Joy"][0]
    rows["Ode to Joy"] = listener_without("Ode to Joy").listen(ode.pitches)
    p42 = Path(".cache/music42")
    try:
        s = json.loads((p42 / "search.json").read_text())
        rows["Part 42: the kept draft"] = lis.listen(_rel([n[0] for n in s["best"]["melody"]]))
        rows["Part 42: a rejected draft"] = lis.listen(_rel([n[0] for n in s["shown"][0]["melody"]]))
        ch = json.loads((p42 / "chains.json").read_text())
        rows["Part 42: a chain of order 4"] = lis.listen(ch["orders"]["4"]["notes"])
        rows["Part 42: a chain of order 1"] = lis.listen(ch["orders"]["1"]["notes"])
    except FileNotFoundError:
        pass
    rng = np.random.default_rng(46)
    scale = [0, 2, 4, 5, 7, 9, 11, 12]
    rows["random notes of the scale"] = lis.listen([int(x) for x in rng.choice(scale, 40)])
    return {"names": list(rows), "mean_ic": [rows[k]["mean_ic"] for k in rows], "mean_entropy": [rows[k]["mean_entropy"] for k in rows]}


WORDS = [(60, 66, 64), (69, 62, 71), (65, 61, 68), (63, 70, 67)]


def compute_learn() -> dict:
    s = L.saffran(WORDS, 30, np.random.default_rng(1999))
    ioi = 0.22
    p = [(Clip(sine(m, 0.2), SR), i * ioi, 0.0) for i, m in enumerate(s["sequence"])]
    stream = Clip(mix(p, duration=len(s["sequence"]) * ioi + 0.3).y, SR)
    word = WORDS[1]
    part = (WORDS[0][2], WORDS[1][0], WORDS[1][1])                     # the end of one word and the start of another
    def trip(x):
        return Clip(mix([(Clip(sine(m, 0.2), SR), i * ioi, 0.0) for i, m in enumerate(x)], duration=3 * ioi + 0.3).y, SR)
    test = concat([trip(part), trip(word)], gap=0.8, names=["first", "second"])
    c = concat([stream, test], gap=1.5, names=["stream", "test"])
    tp = s["tp"]
    return {"words": [list(w) for w in WORDS], "sequence": s["sequence"], "tp_inside": s["tp_inside"], "tp_across": s["tp_across"],
            "word": list(word), "part_word": list(part), "answer": "second", "ioi": ioi,
            "starts": {"stream": float(c.events["stream"]), "test": float(c.events["test"]),
                       "first": float(c.events["test"] + test.events["first"]), "second": float(c.events["test"] + test.events["second"])},
            "clips": {"stream": save_synth("learn.stream", c, detail="a stream of 90 sine tones made of four three-tone 'words' in random order, then two test triplets")}}


ENDINGS = {
    "expected": {"notes": LAST_PHRASE + [(0, 2)], "chords": CHORDS_LAST + [(0, 2)]},
    "delayed": {"notes": LAST_PHRASE + [(-3, 2), (5, 1), (4, 1), (2, 2), (0, 3)], "chords": CHORDS_LAST + [(9, 2), (5, 2), (7, 2), (0, 3)]},
    "denied": {"notes": LAST_PHRASE + [(6, 3)], "chords": CHORDS_LAST + [(2, 3)]},
}


def compute_endings() -> dict:
    lis = listener_without(M.THE_TUNE)
    head = THE.pitches[:-7]
    out = {}
    for k, v in ENDINGS.items():
        mel = head + [m for m, _ in v["notes"]]
        r = lis.listen(mel)
        n = len(v["notes"])
        out[k] = {"notes": [[m, b] for m, b in v["notes"]], "chords": [[r_, b] for r_, b in v["chords"]], "ic": r["ic"][-n:], "entropy": r["entropy"][-n:]}
    clips = [play_line(v["notes"], chords=v["chords"], tail=1.4) for v in ENDINGS.values()]
    c = concat(clips, gap=1.0, names=list(ENDINGS))
    out["starts"] = {k: float(c.events[k]) for k in ENDINGS}
    out["beat"] = 0.42
    out["clips"] = {"three": save("endings.three", c, detail="the Tune's last phrase with three endings: expected, delayed by a deceptive turn, denied; Part 7's piano and a plucked bass")}
    return out


def compute_groove() -> dict:
    pats = {"none": [0, 4, 8, 12], "a little": [0, 4, 7, 10, 12], "medium": [0, 3, 6, 10, 12, 14], "a lot": [1, 3, 6, 9, 11, 14]}
    bpm = 110
    step = 60 / bpm / 4
    clips, idx = [], {}
    for name, ons in pats.items():
        parts = []
        for bar in range(4):
            t0 = bar * 16 * step
            for s in range(0, 16, 2):
                parts.append((arr(P40.hat()), t0 + s * step, -12.0))
            for s in (4, 12):
                parts.append((arr(P40.snare(bar + s)), t0 + s * step, -8.0))
            for s in ons:
                parts.append((arr(bass(36 + (7 if s % 8 == 6 else 0), step * 1.6)), t0 + s * step, -2.0))
                parts.append((arr(P40.kick()), t0 + s * step, -4.0))
        clips.append(Clip(mix(parts, duration=4 * 16 * step + 0.5).y, SR))
        idx[name] = L.syncopation(ons)
    c = concat(clips, gap=0.8, names=list(pats))
    return {"patterns": pats, "index": idx, "bpm": bpm, "starts": {k: float(c.events[k]) for k in pats},
            "clips": {"four": save("groove.four", c, detail="one drum groove of ours with its bass and kick on four patterns of rising syncopation; Part 40's drums, a plucked bass")}}


def compute_emotion() -> dict:
    ev = T.events(1.0, [0, 1])
    minor = {0: 0, 2: 2, 4: 3, 5: 5, 7: 7, 9: 8, 11: 10}
    settings = {
        "A": {"emotion": "happy", "beat": 0.26, "base": 72, "mode": "major", "inst": "piano", "vel": 0.9, "held": 0.5},
        "B": {"emotion": "sad", "beat": 0.75, "base": 55, "mode": "minor", "inst": "violin", "vel": 0.4, "held": 1.0},
        "C": {"emotion": "angry", "beat": 0.24, "base": 48, "mode": "minor", "inst": "trumpet f", "vel": 1.0, "held": 0.6},
        "D": {"emotion": "tender", "beat": 0.6, "base": 72, "mode": "major", "inst": "flute", "vel": 0.45, "held": 1.0},
    }
    clips = []
    for k, s in settings.items():
        p = []
        for e in ev:
            m = MAJOR[e["degree"]]
            if s["mode"] == "minor":
                m = minor[m]
            dur = e["dur"] * s["beat"] * s["held"]
            if s["inst"] == "piano":
                y = arr(piano(s["base"] + m, max(dur, 0.12), s["vel"]))
            else:
                y = arr(O.note(s["inst"], s["base"] + m, max(dur, 0.1)))
            p.append((y, e["t"] * s["beat"], 0.0 if s["vel"] > 0.6 else -8.0))
            if s["emotion"] == "angry" and e["i"] % 2 == 0:
                p.append((arr(P40.kick()), e["t"] * s["beat"], -2.0))
        clips.append(Clip(mix(p, duration=ev[-1]["t"] * s["beat"] + 1.5).y, SR))
    c = concat(clips, gap=0.9, names=list(settings))
    return {"settings": settings, "answer": {k: v["emotion"] for k, v in settings.items()}, "starts": {k: float(c.events[k]) for k in settings},
            "clips": {"four": save_synth("emotion.four", c, detail="the Tune's first two phrases set four ways: fast, high, major and detached; slow, low, minor and legato on strings; fast, low, minor and loud on brass with a drum; slow, high, major and soft on a flute; Part 7's piano, the additive orchestra, Part 9's drum")}}


def compute_tune46() -> dict:
    head_notes = [(MAJOR[d], b) for phrase in T.PHRASES[:5] for d, b in phrase]
    clips = []
    for k, v in ENDINGS.items():
        clips.append(play_line(head_notes[-8:] + v["notes"], chords=None, tail=1.6))
    c = concat(clips, gap=1.2, names=list(ENDINGS))
    e = load("endings")
    return {"order": list(ENDINGS), "seconds": c.duration, "final_ic": {k: e[k]["ic"][-1] for k in ENDINGS},
            "turn_ic": {k: e[k]["ic"][len(LAST_PHRASE)] for k in ENDINGS},
            "starts": {k: float(c.events[k]) for k in ENDINGS},
            "clips": {"variation46": save("tune.variation46", c, detail="the Tune's last two phrases three times: ending as expected, with the ending delayed by a deceptive turn, and with the ending denied; Part 7's piano")}}


def compute_variation() -> dict:
    t = load("tune46")
    f, u = t["final_ic"], t["turn_ic"]
    return {"part": 46, "title": "with three endings: expected, delayed, denied", "seconds": round(t["seconds"], 1),
            "measure": f"the turn to the ending costs {u['expected']:.1f}, {u['delayed']:.1f} and {u['denied']:.1f} bits; the last note {f['expected']:.1f}, {f['delayed']:.1f}, {f['denied']:.1f}",
            "clip": "tune.variation46"}


# ---------------------------------------------------------------------------------------------------- more demonstrations
def chord_clip(chords, beat=0.9, base=48, tail=1.2, bass_too=True):
    """chords: lists of pitches relative to C3 (key 48), one per beat-length slot."""
    p = []
    for i, ch in enumerate(chords):
        for m in ch:
            p.append((arr(piano(base + m, beat * 0.95, 0.65)), i * beat, -2.0))
        if bass_too:
            p.append((arr(bass(base - 12 + min(ch) % 12, beat * 0.9)), i * beat, -4.0))
    return Clip(mix(p, duration=len(chords) * beat + tail).y, SR)


def compute_rep() -> dict:
    mot = [(4, 0.5), (2, 0.5), (0, 1), (7, 2)]
    notes = mot * 3 + [(4, 0.5), (2, 0.5), (0, 1), (9, 2)]
    lis = listener_without(None)
    mel = [m for m, _ in notes]
    r = lis.listen(mel)
    c = play_line(notes, beat=0.42, base=60)
    return {"notes": [[m, b] for m, b in notes], "ic": r["ic"], "last_leap_ic": [r["ic"][3], r["ic"][7], r["ic"][11], r["ic"][15]],
            "clips": {"four": save("rep.four", c, detail="a four-note motive of ours three times, then a fourth time with its leap changed; Part 7's piano")}}


def compute_probe() -> dict:
    lis = listener_without(M.THE_TUNE)
    ctx = THE.pitches[:7]
    probes = {"C": 0, "D": 2, "F sharp": 6}
    ic = {k: lis.listen(ctx + [v])["ic"][-1] for k, v in probes.items()}
    ev = T.events(0.42, [0])
    clips = []
    for k in ("D", "C", "F sharp"):
        notes = [(MAJOR[e["degree"]], e["dur"]) for e in ev] + [(probes[k], 2)]
        clips.append(play_line(notes, beat=0.42, base=60, tail=1.0))
    c = concat(clips, gap=0.8, names=["D", "C", "F sharp"])
    return {"ic": ic, "order": ["D", "C", "F sharp"], "starts": {k: float(c.events[k]) for k in ("D", "C", "F sharp")},
            "clips": {"three": save("probe.three", c, detail="the Tune's first phrase followed by a probe note: D, C, F sharp; Part 7's piano")}}


def compute_sing() -> dict:
    lis = listener_without(None)
    rng = np.random.default_rng(46)
    seq = [0]
    for _ in range(23):
        d = lis.ltm.distribution(seq)
        keys = [k for k in d if -5 <= k <= 14]
        p = np.array([d[k] for k in keys])
        seq.append(int(keys[int(rng.choice(len(keys), p=p / p.sum()))]))
    if seq[-1] != 0:
        seq[-1] = 0
    r = lis.listen(seq)
    notes = [(m, 1) for m in seq[:-1]] + [(seq[-1], 2)]
    c = play_line(notes, beat=0.32, base=60)
    return {"notes": seq, "mean_ic": r["mean_ic"], "clips": {"tune": save("sing.tune", c, detail="a melody sampled from the listener model's own predictions, note by note; Part 7's piano")}}


def compute_drafts() -> dict:
    p42 = Path(".cache/music42/search.json")
    s = json.loads(p42.read_text())
    kept = [(n[0] - 60, n[2]) for n in s["best"]["melody"]]
    rej = [(n[0] - 60, n[2]) for n in s["shown"][0]["melody"]]
    c = concat([play_line(rej, beat=0.42, base=60), play_line(kept, beat=0.42, base=60)], gap=0.9, names=["rejected", "kept"])
    lis = listener_without(None)
    return {"ic": {"rejected": lis.listen([m for m, _ in rej])["mean_ic"], "kept": lis.listen([m for m, _ in kept])["mean_ic"]},
            "starts": {k: float(c.events[k]) for k in ("rejected", "kept")},
            "clips": {"two": save("drafts.two", c, detail="Part 42's first rejected draft and the draft its searcher kept, melody only; Part 7's piano")}}


def compute_susp() -> dict:
    plain = [[0, 4, 7], [5, 9, 12], [7, 11, 14], [0, 4, 12]]
    susp = [[0, 4, 7], [5, 9, 12], [7, 12, 14], [7, 11, 14], [0, 4, 12]]       # the C held over G, then falling to B
    c = concat([chord_clip(plain), chord_clip(susp)], gap=0.9, names=["plain", "suspended"])
    return {"plain": plain, "suspended": susp, "starts": {k: float(c.events[k]) for k in ("plain", "suspended")},
            "clips": {"two": save("susp.two", c, detail="a cadence I-IV-V-I, then the same with a 4-3 suspension over the dominant; Part 7's piano and a plucked bass")}}


def compute_neap() -> dict:
    lead = [[0, 4, 7], [5, 9, 12], [0, 7, 16], [7, 11, 14]]
    tonic = lead + [[0, 4, 12]]
    neap = lead + [[5, 8, 13]]                                                 # D flat major in first inversion: the Neapolitan
    c = concat([chord_clip(tonic), chord_clip(neap)], gap=0.9, names=["tonic", "neapolitan"])
    return {"starts": {k: float(c.events[k]) for k in ("tonic", "neapolitan")},
            "clips": {"two": save("neap.two", c, detail="five chords ending on the tonic, then the same ending on a Neapolitan sixth; Part 7's piano and a plucked bass")}}


def compute_corners() -> dict:
    certain = [[0, 4, 7], [5, 9, 12], [7, 11, 14], [7, 11, 14], [8, 12, 15]]   # a strong dominant, then A flat major
    uncertain = [[0, 4, 7], [3, 8, 12], [1, 6, 10], [4, 8, 11], [2, 7, 11], [0, 4, 12]]   # wandering chromatic chords, then home
    c = concat([chord_clip(certain), chord_clip(uncertain)], gap=0.9, names=["certain", "uncertain"])
    return {"starts": {k: float(c.events[k]) for k in ("certain", "uncertain")},
            "clips": {"two": save("corners.two", c, detail="a firm cadential approach that turns to A flat major; then wandering chromatic chords that find their way home to C; Part 7's piano and a plucked bass")}}


def compute_extremes() -> dict:
    rng = np.random.default_rng(46)
    scale = [0, 2, 4, 5, 7, 9, 11, 12]
    rnd = [int(x) for x in rng.choice(scale, 24)]
    ch = json.loads(Path(".cache/music42/chains.json").read_text())["orders"]["4"]["notes"]
    lis = listener_without(None)
    c = concat([play_line([(m, 1) for m in rnd], beat=0.3, base=60), play_line([(m, 1) for m in ch], beat=0.3, base=60)], gap=0.9, names=["random", "chain"])
    return {"random": rnd, "chain": ch, "ic": {"random": lis.listen(rnd)["mean_ic"], "chain": lis.listen(ch)["mean_ic"]},
            "starts": {k: float(c.events[k]) for k in ("random", "chain")},
            "clips": {"two": save("extremes.two", c, detail="random notes of the C major scale, then Part 42's order-4 chain melody; Part 7's piano")}}


def compute_again() -> dict:
    lis = listener_without(M.THE_TUNE)
    head = THE.pitches[:-7]
    end = [m for m, _ in ENDINGS["denied"]["notes"]]
    mel = head + end + end + end
    r = lis.listen(mel)
    n = len(end)
    idx = [len(head) + n - 1, len(head) + 2 * n - 1, len(head) + 3 * n - 1]
    notes = ENDINGS["denied"]["notes"] * 3
    c = play_line(notes, beat=0.42, base=60, chords=ENDINGS["denied"]["chords"] * 3)
    return {"ic": [r["ic"][i] for i in idx], "clips": {"three": save("again.three", c, detail="the Tune's last phrase with its denied ending, three times in a row; Part 7's piano and a plucked bass")}}


def compute_signoff() -> dict:
    """The part's last sound: the opening of its Variation, under the next part's title."""
    load("variation")
    return signoff(CLIPS, "tune.variation46", 46)


ITEMS = {"hook": compute_hook, "tune": compute_tune, "corpus": compute_corpus, "compare": compute_compare, "learn": compute_learn,
         "endings": compute_endings, "groove": compute_groove, "emotion": compute_emotion, "tune46": compute_tune46,
         "variation": compute_variation, "rep": compute_rep, "probe": compute_probe, "sing": compute_sing, "drafts": compute_drafts,
         "susp": compute_susp, "neap": compute_neap, "corners": compute_corners, "again": compute_again, "extremes": compute_extremes,
         "signoff": compute_signoff}


if __name__ == "__main__":
    CACHE.main(ITEMS, __doc__)
