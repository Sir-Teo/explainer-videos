"""Precompute everything numerical, and every sound, in Part 20 of *Music, Built* ("Canon and Fugue").

    python -m videos.music.music20.compute              # everything missing (a minute or two)
    python -m videos.music.music20.compute --force crab

Numbers are cached in ``.cache/music20/<name>.json``, sounds in ``.cache/music20/audio/``.  The canon tools are
Monochord's (``explainer/music/monochord/canon.py``); the tunes are Part 14's corpus; the voices are played on Part 18's
plucked string over Part 7's soundboard, the endless canon in Part 4's Shepard tones.  No score files were available
offline: the two subjects of Bach's quoted here (the royal theme and the head of *The Art of Fugue*) are written out for
the series with their rhythm simplified, and the README says so.

Items:
    hook        the royal theme of the *Musical Offering*
    rounds      Frère Jacques as a round; every tune of the corpus sung against itself, ranked
    canons      canons counted at every interval from the unison to the ninth; three heard
    forms       the Tune's first phrase forwards, upside down, backwards, and both; the four forms' table
    invertible  a counter-line that survives inversion at the octave, and one that does not; the tables
    augment     the phrase against itself twice as slow
    crab        crab canons counted; one built on the Tune's opening notes, heard
    rising      a canon that rises a tone each time round, in Shepard tones
    answers     the phrase answered really and tonally (an ear question)
    exposition  a three-voice fugue exposition on the Tune's first phrase
    episode     an episode: a fragment sequenced down, against its inversion
    stretto     the phrase's strettos; strettos in the corpus's opening phrases
    bach        B-A-C-H
    tune        Variation 20: the Tune as a canon, a crab canon on its head, and a fugue exposition
    variation   the Variations ledger, row 20
"""

from __future__ import annotations

import numpy as np

from explainer.ai.cache import Cache
from explainer.music.monochord import EXAMPLE_LEVEL, SR, Clip, ClipStore, concat, mix
from explainer.music.monochord import canon as K
from explainer.music.monochord import ear as EAR
from explainer.music.monochord import melody as M
from explainer.music.monochord.instruments.plucked import plucked as pluck
from explainer.music.monochord.instruments import strings as STR
from explainer.music.monochord.partkit import saver, signoff

CACHE = Cache("music20")
CLIPS = ClipStore("music20")
load = CACHE.load
LEVEL = EXAMPLE_LEVEL - 2.5
save = saver(CLIPS, LEVEL, kind="physical model")
BOARD = STR.soundboard()
_NOTES: dict = {}
SEED_CRAB = 0
BEAT = 0.42                                          # seconds to a beat


def hz(m: float) -> float:
    return 440.0 * 2.0 ** ((m - 69) / 12.0)


def harpsichord(m: float, seconds: float) -> Clip:
    """A string plucked near its end, as a quill plucks it (Part 1's monochord, retuned), on Part 7's soundboard."""
    key = (round(m, 3), round(seconds, 3))
    if key not in _NOTES:
        y = BOARD.play(pluck(hz(m), seconds=seconds + 0.4, beta=0.11))
        _NOTES[key] = Clip(np.asarray(y, dtype=float)).fade(0.001, 0.12).at_level(LEVEL)
    return _NOTES[key]


def play_lines(lines, beat: float = BEAT, tail: float = 1.0, gains=None) -> Clip:
    """Lines of (midi, onset, duration) in beats, played together; events ``v{j}.n{k}`` for every note."""
    placed, ev = [], {}
    gains = gains or [0.0] * len(lines)
    for j, ln in enumerate(lines):
        for k, (p, a, d) in enumerate(ln):
            placed.append((harpsichord(p, max(d * beat * 1.15, 0.25)), a * beat, gains[j]))
            ev[f"v{j}.n{k}"] = a * beat
    end = max(K.end(ln) for ln in lines) * beat
    ev["end"] = end
    return Clip(mix(placed, duration=end + tail).y, SR, ev, [])


def rows(ln):
    return [[int(p), float(a), float(d)] for p, a, d in ln]


def tune_phrase(k0: int = 0, k1: int = 7, base: int = 72):
    t = M.corpus([M.THE_TUNE])[0]
    return K.line([base + p for p in t.pitches[k0:k1]], list(t.beats[k0:k1]))


def whole_tune(base: int = 72):
    t = M.corpus([M.THE_TUNE])[0]
    return K.line([base + p for p in t.pitches], list(t.beats))


def faults(lines, **kw):
    f = K.faults(lines, **kw)
    return {k: v for k, v in f.items() if k != "where"} | {"where": [float(x) for x in f["where"]]}


# ---------------------------------------------------------------------------
def compute_hook() -> dict:
    roy = K.line(K.ROYAL_THEME, K.ROYAL_RHYTHM)
    c = play_lines([roy], beat=0.36)
    s = concat([c.at_level(LEVEL)], gap=0.0, names=["theme"])
    return {"theme": rows(roy), "times": [float(s.events[f"theme.v0.n{k}"]) for k in range(len(roy))],
            "clips": {"royal": save("hook.royal", s, level=None, detail="the royal theme of the Musical Offering (Bach, 1747), its rhythm simplified: a plucked string")}}


def compute_rounds() -> dict:
    fj = [m for m in M.corpus() if m.name == "Frère Jacques"][0]
    ln = K.line([67 + p for p in fj.pitches], list(fj.beats))
    lines = K.canon_lines(ln, 8.0, 0, 3)
    lines = [lines[0], K.transpose(lines[1], -12), K.transpose(lines[2], -24)]
    c = play_lines(lines, beat=0.4)
    s = concat([c.at_level(LEVEL)], gap=0.0, names=["round"])
    census = K.round_census(M.corpus())
    known = ("Frère Jacques", "Row, Row, Row Your Boat", "Three Blind Mice")
    return {"lines": [rows(x) for x in lines], "entries": [float(s.events["round"] + 8.0 * 0.4 * k) for k in range(3)],
            "faults": faults(lines, beat=2.0, start=8.0, stop=K.end(lines[0])),
            "census": census, "known_ranks": {n: next(i for i, r in enumerate(census) if r["name"] == n) + 1 for n in known},
            "n_tunes": len(census),
            "clips": {"frere": save("rounds.frere", s, level=None, detail="Frère Jacques as a round in three voices, two bars apart: a plucked string")}}


def compute_canons() -> dict:
    n, delay = 12, 2
    counts = {K.STEP_NAMES[s]: K.count_canons(n, delay, s) for s in range(0, 9)}
    counts_below = {K.STEP_NAMES[s]: K.count_canons(n, delay, -s) for s in range(1, 9)}
    examples, clips = {}, {}
    for name, steps, seed in (("unison", 0, 3), ("second", 1, 1), ("fifth", -4, 2)):
        rng = np.random.default_rng(seed)
        mel = K.sample_canon(n, delay, steps, rng=rng)
        lead = K.line(mel)
        fol = K.shift(K.line([K.diatonic(p, steps) for p in mel]), delay)
        examples[name] = {"leader": rows(lead), "follower": rows(fol), "steps": steps,
                          "faults": faults([lead, fol], start=delay, stop=n)}
        clips[name] = play_lines([lead, fol])
    s = concat([clips[k].at_level(LEVEL) for k in examples], gap=1.2, names=list(examples))
    for k in examples:
        examples[k]["start"] = float(s.events[k])
    notes = K.scale_notes()
    ways = {p: (1 if p % 12 == 0 else 0) for p in notes}              # melodies of n notes from a C, by the same moves
    for _ in range(n - 1):
        ways = {p: sum(w for q, w in ways.items() if K._ok_move(q, p)) for p in notes}
    total = sum(w for p, w in ways.items() if p % 12 == 0)
    return {"n": n, "delay": delay, "counts": counts, "counts_below": counts_below, "total_melodies": total,
            "examples": examples,
            "clips": {"three": save("canons.three", s, level=None, detail="three canons found by the solver: at the unison, at the second, at the fifth below: a plucked string")}}


def compute_forms() -> dict:
    a = tune_phrase()
    ax = K.degree_of(72)[0]                                   # invert about the tonic, C
    forms = {"P": a, "I": K.diatonic_invert(a, ax), "R": K.retrograde(a), "RI": K.retrograde(K.diatonic_invert(a, ax))}
    c = concat([play_lines([forms[f]]).at_level(LEVEL) for f in ("P", "I", "R", "RI")], gap=0.9, names=["P", "I", "R", "RI"])
    quiz = concat([play_lines([forms["P"]]).at_level(LEVEL), play_lines([forms["R"]]).at_level(LEVEL)], gap=1.0, names=["P", "X"])
    table = {f"{f} {g}": K.compose(f, g) for f in K.FORMS for g in K.FORMS}
    real_inv = K.invert(a)
    return {"forms": {k: rows(v) for k, v in forms.items()}, "real_inversion": rows(real_inv), "table": table, "starts": {k: float(c.events[k]) for k in ("P", "I", "R", "RI")},
            "quiz_starts": {k: float(quiz.events[k]) for k in ("P", "X")}, "checked": K.check_table_on([p for p, _, _ in a]),
            "clips": {"four": save("forms.four", c, level=None, detail="the Tune's first phrase forwards, upside down, backwards, and upside down and backwards: a plucked string"),
                      "quiz": save("forms.quiz", quiz, level=None, detail="the phrase, then one of its forms: a plucked string")}}


def compute_invertible() -> dict:
    a = tune_phrase(base=72)
    grid = [float(t) for t in range(8)]
    notes = K.scale_notes(52, 67)
    plain = K.free_voice([a], grid, notes, below=True, ends=(0, 7))
    # a counter-line built for inversion at the octave: no fifths against the phrase (they would become fourths)
    inv_notes = notes
    safe = K.free_voice([a], grid, inv_notes, below=True, ends=(0, 7), avoid=(7,))
    lines = {}
    for name, cs in (("plain", plain), ("safe", safe)):
        lo = K.line(cs)
        up = K.transpose(lo, 24)                                   # the lower line two octaves up: now above
        lines[name] = {"original": [rows(a), rows(lo)], "inverted": [rows(up), rows(a)],
                       "faults_original": faults([a, lo]), "faults_inverted": faults([up, a], allow_upper_fourths=False)}
    clips = {}
    for name in ("plain", "safe"):
        o = lines[name]["original"]
        i = lines[name]["inverted"]
        clips[name] = play_lines([[tuple(x) for x in i[0]], [tuple(x) for x in i[1]]])
    s = concat([clips["plain"].at_level(LEVEL), clips["safe"].at_level(LEVEL)], gap=1.2, names=["A", "B"])
    return {"lines": lines, "tables": {str(at): K.invertible(at) for at in (7, 9, 11)},
            "starts": {k: float(s.events[k]) for k in "AB"},
            "clips": {"two": save("invertible.two", s, level=None, detail="two counter-lines, each moved above the phrase (inversion at the octave): the first had fifths, the second none: a plucked string")}}


def compute_augment() -> dict:
    a = tune_phrase(base=72)
    slow = K.transpose(K.augment(a, 2.0), -24)
    f = faults([a + K.transpose(K.shift(a, 8.0), 0), slow], beat=2.0)
    lines = [a + K.shift(a, 8.0), slow]
    c = play_lines(lines)
    s = concat([c.at_level(LEVEL)], gap=0.0, names=["aug"])
    return {"lines": [rows(x) for x in lines], "faults": f,
            "clips": {"pair": save("augment.pair", s, level=None, detail="the phrase twice in the upper voice, against itself twice as slow, two octaves down: a plucked string")}}


def compute_crab() -> dict:
    counts = {str(n): K.count_crabs(n) for n in (4, 6, 8, 10, 12)}
    mel = K.sample_crab(12, rng=np.random.default_rng(SEED_CRAB), head=[60, 67, 69])
    ln = K.line(mel)
    back = K.retrograde(ln)
    f = faults([ln, back], allow_upper_fourths=False)
    alone = play_lines([ln])
    both = play_lines([ln, K.transpose(back, -12)])
    s = concat([alone.at_level(LEVEL), both.at_level(LEVEL)], gap=1.2, names=["alone", "both"])
    return {"counts": counts, "melody": mel, "faults": f, "starts": {k: float(s.events[k]) for k in ("alone", "both")},
            "lines": [rows(ln), rows(K.transpose(back, -12))],
            "clips": {"one": save("crab.one", s, level=None, detail="a crab canon found by the solver on the Tune's first three notes: the line alone, then against itself backwards: a plucked string")}}


def compute_rising() -> dict:
    mel = K.sample_canon(8, 2, -4, rng=np.random.default_rng(11))
    lead = K.line(mel)
    fol = K.shift(K.line([K.diatonic(p, -4) for p in mel]), 2)
    lap = 10.0                                        # beats a lap (the follower finishes two beats after the leader)
    tones, ev = [], {}
    beat = 0.36
    for L in range(7):
        ev[f"lap{L}"] = L * lap * beat
        for ln in (lead, fol):
            for p, a, d in ln:
                y = EAR.shepard((p - 21) + 2 * L, seconds=d * beat * 1.1)
                tones.append((Clip(y).fade(0.005, 0.05), (L * lap + a) * beat, 0.0))
    dur = 7 * lap * beat + 0.8
    c = Clip(mix(tones, duration=dur).y, SR, ev, []).at_level(LEVEL)
    return {"leader": rows(lead), "follower": rows(fol), "laps": 7, "lap_beats": lap, "beat": beat,
            "faults": faults([lead, fol], start=2, stop=8),
            "clips": {"shepard": save("rising.shepard", c, level=None, kind="synthesized", detail="a two-voice canon found by the solver, played seven times, each a tone higher, in Shepard tones (Part 4): the seventh lap sounds like the first")}}


def compute_answers() -> dict:
    a = tune_phrase(base=72)
    real = K.shift(K.real_answer(a), 8.0)
    tonal = K.shift(K.tonal_answer(a), 8.0)
    sA = play_lines([a, real])
    sB = play_lines([a, tonal])
    s = concat([sA.at_level(LEVEL), sB.at_level(LEVEL)], gap=1.2, names=["A", "B"])
    return {"subject": rows(a), "real": rows(real), "tonal": rows(tonal), "starts": {k: float(s.events[k]) for k in "AB"},
            "answer_start": 8.0 * BEAT,
            "clips": {"two": save("answers.two", s, level=None, detail="the Tune's first phrase as a fugue subject, answered at the fifth twice, really and tonally: a plucked string")}}


def exposition_lines():
    """Three voices: the subject (soprano), the tonal answer (alto) against the countersubject, the subject in the
    bass against the countersubject (alto) and a free voice (soprano); one note a beat in the counter-lines."""
    s1 = tune_phrase(base=72)                                # soprano, bars 1-2
    ans = K.shift(K.transpose(K.tonal_answer(s1), -12), 8.0)  # alto, bars 3-4 (G4 ...)
    grid2 = [8.0 + k for k in range(8)]
    cs = K.free_voice([ans], grid2, K.scale_notes(67, 84), below=False, ends=None, avoid=(7,))
    cs_line = K.line(cs, start=8.0)
    s3 = K.shift(K.transpose(s1, -24), 16.0)                  # bass, bars 5-6
    grid3 = [16.0 + k for k in range(8)]
    # the countersubject against the subject: the same line, a fifth lower (a fourth up in the answer's terms)
    best = None
    for steps in (-4, 3, -11, -7, -14):
        cand = [K.diatonic(p, steps) for p in cs]
        while max(cand) > 74:
            cand = [p - 12 for p in cand]
        while min(cand) < 55:
            cand = [p + 12 for p in cand]
        ln2 = K.line(cand, start=16.0)
        f = K.faults([s3, ln2])
        score = (f["dissonant"], f["parallels"], abs(steps))
        if best is None or score < best[0]:
            best = (score, ln2)
    cs2_line = best[1]
    # where the returning countersubject clashes with the subject, move that note to the nearest consonant scale note
    # (composers adjust a countersubject this way: an altered note, not a new line)
    fixed = []
    for p, a_, d in cs2_line:
        q = K.sounding(s3, a_)
        if q is not None and abs(p - q) % 12 not in K.CONSONANT:
            alts = sorted((x for x in K.scale_notes(p - 4, p + 4) if abs(x - q) % 12 in K.CONSONANT and x > q), key=lambda x: abs(x - p))
            p = alts[0] if alts else p
        fixed.append((p, a_, d))
    cs2_line = fixed
    free = K.free_voice([s3, cs2_line], grid3, K.scale_notes(67, 84), below=False)
    sop = s1 + cs_line + K.line(free, start=16.0)
    alto = ans + cs2_line
    bass = s3
    return sop, alto, bass, {"cs": cs, "free": free}


def compute_exposition() -> dict:
    sop, alto, bass, parts = exposition_lines()
    f = faults([sop, alto, bass])
    c = play_lines([sop, alto, bass], gains=[0.0, -1.0, 0.0])
    s = concat([c.at_level(LEVEL)], gap=0.0, names=["expo"])
    return {"lines": [rows(sop), rows(alto), rows(bass)], "faults": f, "countersubject": parts["cs"], "free": parts["free"],
            "entries": [0.0, 8.0 * BEAT, 16.0 * BEAT], "beat": BEAT,
            "clips": {"three": save("fugue.exposition", s, level=None, detail="a three-voice fugue exposition on the Tune's first phrase: subject, tonal answer with countersubject, subject in the bass: a plucked string")}}


def compute_episode() -> dict:
    """An episode: a fragment of the exposition's free voice, sequenced down a step a bar in the upper voice, against
    the same fragment inverted in the lower voice, sequenced with it."""
    _, _, _, parts = exposition_lines()
    frag = parts["free"][:4]
    up, low = [], []
    for k in range(4):
        for j, p in enumerate(frag):
            up.append((K.diatonic(p, -k), 4.0 * k + j, 1.0))
    inv = [p for p, _, _ in K.diatonic_invert(K.line(frag), K.degree_of(frag[0])[0])]
    best = None
    for shift_ in (-5, -7, -9, -11):
        lo_line = [(K.diatonic(inv[j], shift_ - k), 4.0 * k + j, 1.0) for k in range(4) for j in range(4)]
        f = K.faults([up, lo_line])
        sc = (f["dissonant"], f["parallels"], abs(shift_))
        if best is None or sc < best[0]:
            best = (sc, lo_line, f)
    low = best[1]
    c = play_lines([up, low])
    s = concat([c.at_level(LEVEL)], gap=0.0, names=["episode"])
    return {"fragment": frag, "lines": [rows(up), rows(low)], "faults": best[2] | {"where": [float(x) for x in best[2]["where"]]},
            "clips": {"sequence": save("episode.sequence", s, level=None, detail="an episode: a four-note fragment sequenced down a step a bar, against its inversion: a plucked string")}}


def compute_stretto() -> dict:
    a = tune_phrase(base=72)
    st = K.strettos(a)
    close = [x for x in st if x["delay"] <= 4]
    best = min(close, key=lambda x: (x["delay"], abs(x["interval"])))
    lines = K.canon_lines(a, best["delay"], best["interval"], 2)
    tries = [(faults(lines + [K.transpose(K.shift(a, d3), iv)])["dissonant"], d3, iv) for d3 in (3.0, 4.0, 5.0, 6.0)
             for iv in (-24, -19, -17, -12, -7, -5)]
    _, d3, iv3 = min(tries)
    third = K.transpose(K.shift(a, d3), iv3)
    f3 = faults(lines + [third])
    c = play_lines(lines)
    c3 = play_lines(lines + [third])
    s = concat([c.at_level(LEVEL), c3.at_level(LEVEL)], gap=1.2, names=["two", "three"])
    # the corpus: does each tune's first phrase admit a stretto with the follower entering by its middle?
    census = []
    for m in M.corpus():
        k1 = min(len(m.pitches), m.phrase_ends[0] if m.phrase_ends else 8)
        ph = K.line([72 + p for p in m.pitches[:k1]], list(m.beats[:k1]))
        T = K.end(ph)
        found = K.strettos(ph, delays=[float(d) for d in np.arange(1.0, T / 2 + 1e-9, 1.0)])
        census.append({"name": m.name, "length": T, "strettos": len(found)})
    inv = K.diatonic_invert(a, K.degree_of(72)[0])
    by_inversion = []
    for dl in [float(x) for x in range(1, 7)]:
        for iv in (-24, -19, -17, -12, -7, -5, 0, 5, 7, 12):
            f = K.faults([a, K.transpose(K.shift(inv, dl), iv)], start=dl, stop=K.end(a))
            if f["beats"] >= 2 and f["dissonant"] == 0 and f["parallels"] == 0:
                by_inversion.append({"delay": dl, "interval": iv, "overlap": f["beats"]})
    roy = K.line(K.ROYAL_THEME, K.ROYAL_RHYTHM)
    roy_st = K.strettos(roy)
    return {"royal": {"strettos": roy_st, "length": K.end(roy), "earliest": min(x["delay"] for x in roy_st) if roy_st else None},
            "by_inversion": by_inversion, "all": st, "best": best, "lines": [rows(x) for x in lines], "third": rows(third), "faults_three": f3, "third_entry": {"delay": d3, "interval": iv3},
            "starts": {k: float(s.events[k]) for k in ("two", "three")},
            "census": census, "with_stretto": sum(1 for r in census if r["strettos"]), "n": len(census),
            "clips": {"tune": save("stretto.tune", s, level=None, detail="the phrase in stretto: a second voice two beats behind and a fourth below; then a third entry in the bass: a plucked string")}}


def compute_bach() -> dict:
    motif = K.line([70, 69, 72, 71], [2, 2, 2, 2])
    c = play_lines([motif], beat=0.5)
    s = concat([c.at_level(LEVEL)], gap=0.0, names=["bach"])
    return {"motif": rows(motif), "names": ["B", "A", "C", "H"], "spelled": ["B♭", "A", "C", "B♮"],
            "clips": {"motif": save("bach.motif", s, level=None, detail="B-A-C-H: B flat, A, C, B natural: a plucked string")}}


def compute_tune() -> dict:
    full = whole_tune(base=72)
    st = K.strettos(full, delays=[2.0], intervals=(-5,), tolerance=2)
    canon = [full, K.transpose(K.shift(full, 2.0), -5)]
    fc = faults(canon, start=2.0, stop=K.end(full))
    crab = load("crab")
    ln = [tuple(x) for x in crab["lines"][0]]
    back = [tuple(x) for x in crab["lines"][1]]
    sop, alto, bass, _ = exposition_lines()
    cl = {"canon": play_lines(canon, beat=0.36), "crab": play_lines([ln, back]), "exposition": play_lines([sop, alto, bass], gains=[0.0, -1.0, 0.0])}
    s = concat([cl[k].at_level(LEVEL) for k in ("canon", "crab", "exposition")], gap=1.4, names=["canon", "crab", "exposition"])
    return {"order": ["canon", "crab", "exposition"], "starts": {k: float(s.events[k]) for k in ("canon", "crab", "exposition")},
            "canon": [rows(x) for x in canon], "canon_faults": fc, "crab": [rows(ln), rows(back)],
            "exposition": [rows(sop), rows(alto), rows(bass)], "beats": {"canon": 0.36, "crab": BEAT, "exposition": BEAT},
            "seconds": s.duration, "clip": {"name": "tune.variation20", "seconds": s.duration},
            "clips": {"variation": save("tune.variation20", s, level=None, detail="the Tune as a canon at the fourth below; a crab canon on its first notes; a three-voice fugue exposition on its first phrase: a plucked string")}}


def compute_variation() -> dict:
    t = load("tune")
    return {"part": 20, "title": r"as a canon at the fourth below, a crab canon, and a three-voice fugue exposition", "seconds": round(t["seconds"], 2),
            "measure": rf"the whole Tune against itself two beats later: {t['canon_faults']['dissonant']} dissonant beats in {t['canon_faults']['beats']}", "clip": "tune.variation20"}


def compute_signoff() -> dict:
    """The part's last sound: the opening of its Variation, under the next part's title."""
    load("variation")
    return signoff(CLIPS, "tune.variation20", 20)


ITEMS = {"hook": compute_hook, "rounds": compute_rounds, "canons": compute_canons, "forms": compute_forms, "invertible": compute_invertible,
         "augment": compute_augment, "crab": compute_crab, "rising": compute_rising, "answers": compute_answers,
         "exposition": compute_exposition, "episode": compute_episode, "stretto": compute_stretto, "bach": compute_bach, "tune": compute_tune,
         "variation": compute_variation,
         "signoff": compute_signoff}


if __name__ == "__main__":
    CACHE.main(ITEMS, __doc__)
