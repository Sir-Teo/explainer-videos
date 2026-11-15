"""Precompute everything numerical, and every sound, in Part 43 of *Music, Built* ("Performing").

    python -m videos.music.music43.compute              # everything missing (about two minutes)
    python -m videos.music.music43.compute --force identity

Numbers are cached in ``.cache/music43/<name>.json``, sounds in ``.cache/music43/audio/``.  The tools are Monochord's
(``explainer/music/monochord/perform.py``).  The piano is Part 7's (a struck string on a soundboard, as Part 38 uses
it), with a plucked bass; the vibrato tones are Part 41's bowed-string spectrum.  Every performance is a model's; the
pianists are model pianists; no recording of a real performer is played, and the Hatto case is described, not heard.

Items:
    hook        an ear question: three recordings of the same phrase; which two are really one pianist?
    written     the Tune's first two phrases as written, then as performed by the rules
    rules       the first phrase with each rule alone
    strength    all the rules at strengths 0, 1 and 2
    ritard      three final ritardandi (q = 1, 2, 3), and the curves
    artic       the first phrase legato, as written, staccato
    vibrato     an ear question: a plain tone, then one with wide vibrato: higher, lower or the same?
    rates       vibrato at 3, 6 and 10 Hz
    duo         three duos: both listen, nobody listens, one over-corrects
    duo_curve   the asynchrony's standard deviation against the total correction, simulated and exact
    quartet     a democratic and an autocratic quartet (Wing and colleagues' two quartets, modelled)
    identity    the Hatto test on ten model pianists
    tune        Variation 43: the Tune as written and as performed
    variation   the Variations ledger, row 43
"""

from __future__ import annotations

import numpy as np

from explainer.ai.cache import Cache
from explainer.music.monochord import EXAMPLE_LEVEL, SR, Clip, ClipStore, concat, mix
from explainer.music.monochord import perform as P
from explainer.music.monochord.partkit import saver
from videos.music.music38 import compute as P38

CACHE = Cache("music43")
CLIPS = ClipStore("music43")
load = CACHE.load
LEVEL = EXAMPLE_LEVEL - 2.5
save = saver(CLIPS, LEVEL, kind="physical model")
save_synth = saver(CLIPS, LEVEL, kind="synthesized")
arr = P38.arr
piano, bass = P38.piano, P38.bass

SCORE, PHRASES = P.tune_score()
CHORDS = {0: ["I", "I", "IV", "I"], 1: ["IV", "I", "V", "I"], 2: ["I", "IV", "I", "V"]}
PTYPE = [0, 1, 2, 2, 0, 1]
ROOT = {"I": 48, "IV": 53, "V": 55}


def sub(phrases):
    idx = [i for i, p in enumerate(PHRASES) if p in phrases]
    a0 = SCORE[idx[0]][1]
    return [(m, a - a0, d) for (m, a, d) in (SCORE[i] for i in idx)], [PHRASES[i] for i in idx]


def bass_for(score, phrases, perf):
    """A bass root on each two-beat chord slot, at the performed onset of the melody note that starts the slot."""
    out = []
    for i, (m, a, d) in enumerate(score):
        if abs(a % 2) < 1e-9:
            p = phrases[i]
            slot = int((a % 8) // 2)
            sym = CHORDS[PTYPE[p]][slot]
            j = next((k for k in range(i + 1, len(score)) if score[k][1] >= a + 2 - 1e-9), None)
            end = perf[j]["t"] if j is not None else perf[i]["t"] + perf[i]["dur"]
            out.append((ROOT[sym], perf[i]["t"], max(end - perf[i]["t"], 0.3), perf[i]["vel"]))
    return out


def render(perf, score=None, phrases=None, with_bass=True, tail=1.4):
    parts = [(arr(piano(p["key"] + 12, max(p["dur"], 0.12), round(p["vel"] + 0.3, 1))), p["t"], 0.0) for p in perf]
    if with_bass and score is not None:
        parts += [(arr(bass(m, d * 0.95)), t, -6.0 + 6 * (v - 0.6)) for m, t, d, v in bass_for(score, phrases, perf)]
    end = max(p["t"] + p["dur"] for p in perf) + tail
    return Clip(mix(parts, duration=end).y, SR)


def jperf(perf):
    return [{k: (round(v, 4) if isinstance(v, float) else v) for k, v in p.items()} for p in perf]


# ---------------------------------------------------------------------------------------------------------- items
def compute_hook() -> dict:
    sc, ph = sub([0, 1])
    A = P.play(P.pianist(3), sc, ph, take=0)
    B = P.play(P.pianist(7), sc, ph, take=0)
    A2 = P.play(P.pianist(3), sc, ph, take=0, stretch=1.05)
    clips = [render(x, sc, ph) for x in (A, B, A2)]
    c = concat(clips, gap=1.0, names=["one", "two", "three"])
    cur = {k: P.tempo_curve(x) for k, x in zip(("one", "two", "three"), (A, B, A2))}
    r = {f"{a}-{b}": float(np.corrcoef(cur[a], cur[b])[0, 1]) for a, b in (("one", "two"), ("one", "three"), ("two", "three"))}
    return {"perfs": {k: jperf(x) for k, x in zip(("one", "two", "three"), (A, B, A2))}, "r": r, "answer": "first and third",
            "stretch": 1.05, "starts": {k: float(c.events[k]) for k in ("one", "two", "three")},
            "clips": {"three": save("hook.three", c, detail="three recordings of the Tune's first two phrases by model pianists; the third is the first, played 5% slower; Part 7's piano and a plucked bass")}}


def compute_written() -> dict:
    sc, ph = sub([0, 1])
    dp, pf = P.deadpan(sc), P.perform(sc, ph)
    c = concat([render(dp, sc, ph), render(pf, sc, ph)], gap=1.0, names=["written", "performed"])
    dev, vel = P.deviations(pf, sc)
    return {"score": [list(n) for n in sc], "deadpan": jperf(dp), "performed": jperf(pf), "stretch": dev, "vel": vel,
            "starts": {k: float(c.events[k]) for k in ("written", "performed")},
            "clips": {"two": save("written.two", c, detail="the Tune's first two phrases exactly as written, then performed by rules of expression; Part 7's piano and a plucked bass")}}


def compute_rules() -> dict:
    sc, ph = sub([0, 1])
    names = ["as written"] + list(P.RULES)
    perfs, devs = {}, {}
    for nm in names:
        pf = P.deadpan(sc) if nm == "as written" else P.perform(sc, ph, rules=(nm,), k=1.6)
        perfs[nm] = pf
        devs[nm] = P.deviations(pf, sc)
    c = concat([render(perfs[nm], sc, ph, tail=0.8) for nm in names], gap=0.8, names=names)
    held = {}
    for nm, pf in perfs.items():
        ioi = [pf[i + 1]["t"] - pf[i]["t"] for i in range(len(pf) - 1)] + [pf[-1]["dur"]]
        held[nm] = [float(p["dur"] / x) for p, x in zip(pf, ioi)]
    return {"names": names, "stretch": {k: v[0] for k, v in devs.items()}, "vel": {k: v[1] for k, v in devs.items()}, "held": held,
            "score": [list(n) for n in sc], "starts": {k: float(c.events[k]) for k in names}, "k": 1.6,
            "clips": {"each": save("rules.each", c, detail="the Tune's first two phrases as written, then with each rule of expression alone, exaggerated; Part 7's piano and a plucked bass")}}


def compute_strength() -> dict:
    """The rules together at strengths k = 0, 1 and 2 on the first two phrases."""
    sc, ph = sub([0, 1])
    perfs = {str(k): (P.deadpan(sc) if k == 0 else P.perform(sc, ph, k=float(k))) for k in (0, 1, 2)}
    c = concat([render(v, sc, ph, tail=0.8) for v in perfs.values()], gap=0.9, names=list(perfs))
    return {"perfs": {k: jperf(v) for k, v in perfs.items()}, "lengths": {k: float(v[-1]["t"] + v[-1]["dur"]) for k, v in perfs.items()},
            "starts": {k: float(c.events[k]) for k in perfs},
            "clips": {"three": save("strength.three", c, detail="the Tune's first two phrases with all five rules at strength 0 (as written), 1 and 2; Part 7's piano and a plucked bass")}}


def compute_ritard() -> dict:
    sc, ph = sub([5])
    x = np.linspace(0, 1, 101)
    curves = {str(q): P.ritardando(x, 0.5, q).tolist() for q in (1, 2, 3)}
    clips, perfs = [], {}
    for q in (1, 2, 3):
        st = P.rule_final_ritardando(sc, ph, span_beats=8.0, w=0.5, q=q)["stretch"]
        beat = 0.6
        lens = np.array([d for _, _, d in sc]) * beat * (1 + st)
        on = np.concatenate([[0.0], np.cumsum(lens)[:-1]])
        pf = [{"key": sc[i][0], "t": float(on[i]), "dur": float(lens[i]), "vel": 0.55} for i in range(len(sc))]
        perfs[str(q)] = pf
        clips.append(render(pf, sc, [5] * len(sc), tail=1.0))
    c = concat(clips, gap=1.0, names=["q1", "q2", "q3"])
    return {"x": x.tolist(), "curves": curves, "perfs": {k: jperf(v) for k, v in perfs.items()}, "w": 0.5,
            "starts": {k: float(c.events[k]) for k in ("q1", "q2", "q3")},
            "clips": {"three": save("ritard.three", c, detail="the Tune's last phrase slowing to half speed along three curves (q = 1, 2, 3); Part 7's piano and a plucked bass")}}


def compute_artic() -> dict:
    sc, ph = sub([0])
    dp = P.deadpan(sc, bpm=96)
    out = {}
    for name, f in (("legato", 1.12), ("as written", 0.92), ("staccato", 0.4)):
        out[name] = [{**p, "dur": p["dur"] * f} for p in dp]
    c = concat([render(v, sc, ph, tail=0.6) for v in out.values()], gap=0.8, names=list(out))
    return {"versions": {k: jperf(v) for k, v in out.items()}, "ratios": {"legato": 1.12, "as written": 0.92, "staccato": 0.4},
            "starts": {k: float(c.events[k]) for k in out},
            "clips": {"three": save("artic.three", c, detail="the Tune's first phrase legato (each note held past the next), as written, and staccato; Part 7's piano and a plucked bass")}}


def compute_vibrato() -> dict:
    f0 = 440.0
    plain = P.vibrato_tone(f0, 2.2, cents=0.0)
    vib = P.vibrato_tone(f0, 2.2, rate=5.5, cents=60.0)
    c = concat([Clip(plain, SR).fade(0.01, 0.1), Clip(vib, SR).fade(0.01, 0.1)], gap=0.8, names=["plain", "vibrato"])
    # the instantaneous frequency of the vibrato tone over its steady part, and its mean
    t = np.arange(int(2.2 * SR)) / SR
    dev = 60.0 * np.sin(2 * np.pi * 5.5 * t) * np.clip(t / 0.25, 0, 1)
    f = f0 * 2 ** (dev / 1200)
    steady = t > 0.4
    return {"f0": f0, "cents": 60.0, "rate": 5.5, "mean_hz": float(f[steady].mean()), "mean_cents": float(dev[steady].mean()),
            "trace_t": t[::441].tolist(), "trace_cents": dev[::441].tolist(), "answer": "the same",
            "starts": {k: float(c.events[k]) for k in ("plain", "vibrato")},
            "clips": {"quiz": save_synth("vibrato.quiz", c, detail="A4 plain, then with a vibrato of 60 cents either side at 5.5 Hz; additive, from the bowed-string spectrum")}}


def compute_rates() -> dict:
    tones = [Clip(P.vibrato_tone(440.0, 1.8, rate=r, cents=40.0), SR).fade(0.01, 0.1) for r in (3.0, 6.0, 10.0)]
    c = concat(tones, gap=0.6, names=["3", "6", "10"])
    return {"rates": [3.0, 6.0, 10.0], "cents": 40.0, "starts": {k: float(c.events[k]) for k in ("3", "6", "10")},
            "clips": {"three": save_synth("rates.three", c, detail="A4 with vibrato 40 cents either side at 3, 6 and 10 Hz; additive, from the bowed-string spectrum")}}


def duo_clip(on, keys=(72, 64)):
    parts = []
    for k in range(on.shape[0]):
        for i in range(on.shape[1]):
            parts.append((arr(piano(keys[i], 0.3, 0.7)), float(on[k, i] - on[0].min()), -2.0))
    end = float(on.max() - on[0].min()) + 1.0
    return Clip(mix(parts, duration=end).y, SR)


def compute_duo() -> dict:
    cases = {"both listen": [0.25, 0.25], "nobody listens": [0.0, 0.0], "one over-corrects": [0.1, 2.15]}
    out, clips = {}, []
    for k, (name, al) in enumerate(cases.items()):
        r = P.phase_correction(al, n=24, period=[0.5, 0.512], rng=np.random.default_rng(11), timer_sd=0.012)
        a = r["asynchrony"][:, 1]
        out[name] = {"alpha": al, "asynchrony_ms": (1000 * a).tolist(), "sd_ms": float(1000 * a.std()), "final_ms": float(1000 * a[-1])}
        clips.append(duo_clip(r["onsets"]))
    c = concat(clips, gap=1.2, names=list(cases))
    return {"cases": out, "order": list(cases), "answer": "nobody listens", "period": [0.5, 0.512],
            "starts": {k: float(c.events[k]) for k in cases},
            "clips": {"three": save("duo.three", c, detail="three model duos whose players' own tempos differ by 2.4%, one on C5 and one on E4, 24 beats each: both correcting, neither correcting, one over-correcting; Part 7's piano")}}


def compute_duo_curve() -> dict:
    alphas = np.round(np.linspace(0.05, 1.95, 39), 3)
    exact = [float(1000 * np.sqrt(P.asynchrony_variance(a))) for a in alphas]
    sim = []
    for a in alphas:
        r = P.phase_correction([a / 2, a / 2], n=3000, rng=np.random.default_rng(5))
        sim.append(float(1000 * r["asynchrony"][100:, 1].std()))
    best = float(alphas[int(np.argmin(exact))])
    return {"alpha": alphas.tolist(), "exact_ms": exact, "sim_ms": sim, "best_alpha": best, "best_ms": float(min(exact)),
            "timer_ms": 12.0, "motor_ms": 5.0}


def compute_quartet() -> dict:
    demo = np.full((4, 4), 0.12)
    np.fill_diagonal(demo, 0)
    auto = np.array([[0, 0.03, 0.03, 0.03], [0.35, 0, 0.05, 0.05], [0.35, 0.05, 0, 0.05], [0.35, 0.05, 0.05, 0]])
    out = {}
    for name, M in (("democratic", demo), ("autocratic", auto)):
        r = P.phase_correction(M, n=4000, rng=np.random.default_rng(9))
        on = r["onsets"][200:]
        mean = on.mean(axis=1, keepdims=True)
        out[name] = {"M": M.tolist(), "sd_ms": [float(1000 * (on[:, i] - mean[:, 0]).std()) for i in range(4)],
                     "spread_ms": float(1000 * (on.max(axis=1) - on.min(axis=1)).mean()),
                     "contraction": float(sorted(np.abs(np.linalg.eigvals(np.eye(4) - (np.diag(M.sum(1)) - M))), reverse=True)[1])}
    clips = []
    for name, M in (("democratic", demo), ("autocratic", auto)):
        r = P.phase_correction(M, n=16, period=0.45, rng=np.random.default_rng(21), timer_sd=0.012)
        on = r["onsets"]
        parts = []
        chords = [(76, 67, 60, 48), (77, 69, 60, 53), (79, 71, 62, 55), (76, 67, 60, 48)]
        for k in range(16):
            ch = chords[(k // 4) % 4]
            for i in range(4):
                parts.append((arr(piano(ch[i], 0.35, 0.6)), float(on[k, i] - on[0].min()), -4.0))
        clips.append(Clip(mix(parts, duration=float(on.max() - on[0].min()) + 1.0).y, SR))
        out[name]["clip_spread_ms"] = float(1000 * (on.max(axis=1) - on.min(axis=1)).mean())
    c = concat(clips, gap=1.0, names=["democratic", "autocratic"])
    return {**out, "players": ["violin 1", "violin 2", "viola", "cello"], "starts": {k: float(c.events[k]) for k in ("democratic", "autocratic")},
            "clips": {"two": save("quartet.two", c, detail="the two model quartets, each player a piano voice, sixteen chords each; Part 7's piano")}}


def compute_identity() -> dict:
    sc, ph = SCORE, PHRASES
    names = [f"pianist {chr(65 + i)}" for i in range(10)]
    perfs = {nm: P.play(P.pianist(i), sc, ph, take=0) for i, nm in enumerate(names)}
    curves = {nm: P.tempo_curve(p) for nm, p in perfs.items()}
    # the 'new release': pianist D's recording, time-stretched 3% and with 2 ms of editing jitter
    src = perfs["pianist D"]
    rng = np.random.default_rng(2007)
    hoax = [{**p, "t": float(p["t"] * 1.03 + rng.normal(0, 0.002))} for p in src]
    hoax[0]["t"] = 0.0
    other_take = P.play(P.pianist(3), sc, ph, take=1)
    ranking = P.identify(curves, P.tempo_curve(hoax))
    take_rank = P.identify(curves, P.tempo_curve(other_take))
    R = np.corrcoef(np.array([curves[n] for n in names]))
    off = R[np.triu_indices(10, 1)]
    return {"names": names, "ranking": ranking, "take_ranking": take_rank, "R": R.tolist(), "between_mean": float(off.mean()),
            "between_max": float(off.max()), "curves": {k: v.tolist() for k, v in curves.items() if k in ("pianist D", "pianist B")},
            "hoax_curve": P.tempo_curve(hoax).tolist(), "notes": len(sc)}


def compute_tune() -> dict:
    dp, pf = P.deadpan(SCORE), P.perform(SCORE, PHRASES)
    a = render(dp, SCORE, PHRASES, tail=1.0)
    b = render(pf, SCORE, PHRASES, tail=1.6)
    c = concat([a, b], gap=1.2, names=["written", "performed"])
    dev, vel = P.deviations(pf, SCORE)
    last = [i for i in range(len(PHRASES)) if i == len(PHRASES) - 1 or PHRASES[i + 1] != PHRASES[i]]
    return {"deadpan": jperf(dp), "performed": jperf(pf), "stretch": dev, "vel": vel, "phrases": PHRASES,
            "written_s": float(dp[-1]["t"] + dp[-1]["dur"]), "performed_s": float(pf[-1]["t"] + pf[-1]["dur"]),
            "max_stretch_mid": float(max(dev[i] for i in last[:-1])), "last_stretch": float(dev[-1]),
            "vel_range": [float(min(vel)), float(max(vel))], "seconds": c.duration,
            "starts": {k: float(c.events[k]) for k in ("written", "performed")},
            "clips": {"variation43": save("tune.variation43", c, detail="the Tune exactly as written, then performed by rules of expression; Part 7's piano and a plucked bass")}}


def compute_variation() -> dict:
    t = load("tune")
    return {"part": 43, "title": "as written and as performed: the same notes, the differences drawn", "seconds": round(t["seconds"], 1),
            "measure": f"phrase ends up to {100 * (t['max_stretch_mid'] - 1):.0f}% longer, the last note {100 * (t['last_stretch'] - 1):.0f}%; "
                       f"{t['written_s']:.1f} s as written, {t['performed_s']:.1f} s performed",
            "clip": "tune.variation43"}


ITEMS = {"hook": compute_hook, "written": compute_written, "rules": compute_rules, "strength": compute_strength, "ritard": compute_ritard, "artic": compute_artic,
         "vibrato": compute_vibrato, "rates": compute_rates, "duo": compute_duo, "duo_curve": compute_duo_curve,
         "quartet": compute_quartet, "identity": compute_identity, "tune": compute_tune, "variation": compute_variation}


if __name__ == "__main__":
    CACHE.main(ITEMS, __doc__)
