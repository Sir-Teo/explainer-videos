"""Precompute everything numerical, and every sound, in Part 67 of *Music, Built* ("Doing Research in Music").

    python -m videos.music.music67.compute              # everything missing (some minutes: earlier verdicts are re-run)
    python -m videos.music.music67.compute --force hook

Numbers are cached in ``.cache/music67/<name>.json``, sounds in ``.cache/music67/audio/``.  The tools are Monochord's
research methods (``explainer/music/monochord/research.py``) and *Statistics, Built*'s kit (meta-analysis, Egger's test);
the audits re-run functions of Parts 61, 64, 65 and 66 with new seeds and splits.

Items:
    hook        an ABX trial: a piano phrase, the same through Part 58's coder, and X (an ear question)
    stemma      a manuscript tradition of the Tune: witnesses, a tree recovered from shared errors, the lost original rebuilt
    canon       melodic statistics on Bach's chorale tunes against Part 14's wider collection of tunes, with intervals
    meta        a simulated literature with a small true effect and selective publication: the funnel, Egger, PET
    power       the exact power of ABX tests by trials and by hit rate
    leakage     Part 65's chain scored on a split by chorale (leaky) against a split by hymn tune
    audit       verdicts of Parts 61, 64, 65 and 66 re-run across seeds and splits, with intervals
    stars       every part's research problem, read from the READMEs
    tune67      Variation 67: the Tune's critical edition: the original, a corrupt witness, the reconstruction
    variation   the Variations ledger, row 67
    canonheard  a chorale tune and a tune from Part 14's collection, heard
    phack       the false-positive rate as an analyst's choices multiply (Simmons, Nelson and Simonsohn)
    abx2        a harder ABX trial (an ear question)
    tappers     two simulated beat tappers against each other and the performance: an agreement ceiling
    audit63     Part 63's fingerprinter at 0 dB, re-run with new noise
    repro       a number of Part 65's recomputed, to the last digit
    notation    a sung phrase's pitch against the equal-tempered notes a transcription would write
    mushra      listeners needed for a MUSHRA-style comparison, by the difference sought
    dupes       Variations whose audio recurs elsewhere in this series' library
    pitchstd    the Tune at three pitch standards
    copies      three surviving copies from three generations, heard
    tapsheard   the two simulated tappers' taps as clicks over a performance
    auditheard  one of Part 63's queries in new noise, and what the index said
"""

from __future__ import annotations

import numpy as np

from explainer.ai.cache import Cache
from explainer.music.monochord import EXAMPLE_LEVEL, SR, Clip, ClipStore, concat, mix
from explainer.music.monochord import codec as K
from explainer.music.monochord import machines as MC
from explainer.music.monochord import melody as ML
from explainer.music.monochord import research as R
from explainer.music.monochord.partkit import saver
from explainer.stats.kit import multiple as MT
from explainer.stats.kit import shrink as SH
from explainer.tts import REPO_ROOT
from videos.music.music38 import compute as P38

CACHE = Cache("music67")
CLIPS = ClipStore("music67")
load = CACHE.load
LEVEL = EXAMPLE_LEVEL - 2.5
save = saver(CLIPS, LEVEL, kind="physical model")


def C(y) -> Clip:
    y = np.asarray(y, float)
    k = int(0.005 * SR)
    y[:k] *= np.linspace(0, 1, k)
    r = int(0.08 * SR)
    y[-r:] *= np.linspace(1, 0, r)
    return Clip(y / (np.max(np.abs(y)) + 1e-12) * 0.9, SR)


def piano(keys, beats, beat: float = 0.42) -> np.ndarray:
    t, placed = 0.0, []
    for m, b in zip(keys, beats):
        placed.append((P38.arr(P38.piano(int(m), b * beat * 0.95, 0.8)), t, 0.0))
        t += b * beat
    return mix(placed, duration=t + 1.0).y


def the_tune():
    m = ML.corpus()[0]                                   # Ah! vous dirai-je, maman: the Tune
    return [60 + p for p in m.pitches], list(m.beats)


# ---------------------------------------------------------------------------------------------- items
def compute_hook() -> dict:
    keys, beats = the_tune()
    y = piano(keys[:14], beats[:14])
    coded = K.encode(y, 48)["y"][:len(y)]
    c = concat([C(y), C(coded), C(coded)], gap=0.8, names=["A", "B", "X"])
    return {"answer": "B", "kbps": 48, "starts": {k: float(c.events[k]) for k in ("A", "B", "X")},
            "clips": {"three": save("hook.three", c, detail="an ABX trial: the Tune's first phrase on Part 38's piano (A), the same through Part 58's coder at 48 kbit/s (B), then X, which is one of them")}}


def compute_stemma() -> dict:
    keys, beats = the_tune()
    # the first seed (from 1) whose surviving witnesses all carry errors, so that no copy is simply the original
    for seed in range(1, 200):
        rng = np.random.default_rng(seed)
        t = R.copy_tradition(keys, rng, generations=4, error_rate=0.05)
        W = [t["mss"][i]["notes"] for i in t["survive"]]
        if len(W) >= 10 and min(R.hamming(w, keys) for w in W) >= 2:
            break
    sv = t["survive"]
    D = np.array([[R.hamming(a, b) for b in W] for a in W])
    nj = R.neighbor_joining(D, [str(i) for i in sv])
    true = R.true_adjacency(t["mss"], sv)
    rf = R.rf_distance(true, nj, sv)
    rec = R.reconstruct(W)
    # branches: witnesses grouped by which first-generation copy they descend from
    def root_child(i):
        while t["mss"][i]["parent"] not in (0, None):
            i = t["mss"][i]["parent"]
        return i
    groups = {}
    for k, i in enumerate(sv):
        groups.setdefault(root_child(i), []).append(k)
    rec_b = R.reconstruct_by_branch(W, list(groups.values()))
    errs = [R.hamming(w, keys) for w in W]
    worst = int(np.argmax(errs))
    c = concat([C(piano(keys, beats)), C(piano(W[worst], beats)), C(piano(rec, beats))], gap=0.8, names=["original", "witness", "rebuilt"])
    return {"seed": seed, "n_mss": len(t["mss"]), "n_survive": len(sv), "n_notes": len(keys), "witness_errors": errs, "rf": rf,
            "majority_errors": R.hamming(rec, keys), "branch_errors": R.hamming(rec_b, keys), "branches": len(groups),
            "D": D.tolist(), "survive": sv, "gens": [t["mss"][i]["gen"] for i in sv], "worst": worst,
            "starts": {k: float(c.events[k]) for k in ("original", "witness", "rebuilt")},
            "clips": {"three": save("stemma.three", c, detail="the Tune on Part 38's piano as written, as the most corrupt surviving copy of a simulated manuscript tradition has it, and as rebuilt from all the copies")}}


def _stats(seqs) -> dict:
    iv = [b - a for s in seqs for a, b in zip(s, s[1:])]
    iv = np.array(iv)
    move = iv[iv != 0]
    return {"steps": float(np.mean(np.abs(move) <= 2)), "leaps5": float(np.mean(np.abs(move) >= 5)), "repeats": float(np.mean(iv == 0))}


def compute_canon() -> dict:
    """Is 'melodies move mostly by step' a fact about melody, or about the canon it was learnt from?"""
    chor = [[n[0] for n in t["notes"]] for t in MC.tunes()]
    folk = [list(m.pitches) for m in ML.corpus()]
    rng = np.random.default_rng(67)
    out = {}
    for name, S in (("chorales", chor), ("tunes", folk)):
        point = _stats(S)
        boot = [_stats([S[i] for i in rng.integers(0, len(S), len(S))]) for _ in range(400)]
        out[name] = {k: {"value": point[k], "lo": float(np.percentile([b[k] for b in boot], 2.5)), "hi": float(np.percentile([b[k] for b in boot], 97.5))} for k in point}
        out[name]["n"] = len(S)
    return {"rows": out}


def compute_meta() -> dict:
    """A literature like the Mozart effect's, simulated: a small true effect, many small studies, significant ones
    published and others mostly not."""
    rng = np.random.default_rng(1993)
    sim = MT.publication_sim(120, 0.1, rng, tau=0.05, n_range=(12, 120), publish_null=0.15)
    est, se, pub = sim["est"], sim["se"], sim["published"]
    first = int(np.flatnonzero(pub & (sim["p"] < 0.05))[0])
    eg = MT.egger(est[pub], se[pub])
    fe = lambda e, s: float(np.sum(e / s ** 2) / np.sum(1 / s ** 2))
    re_pub = SH.meta(est[pub], se[pub] ** 2)
    big = 0.1 + np.sqrt(2 / 2000) * rng.standard_normal()
    return {"est": est.tolist(), "se": se.tolist(), "published": pub.tolist(), "n_studies": int(len(est)), "n_published": int(pub.sum()),
            "first": {"est": float(est[first]), "se": float(se[first]), "n": int(round(2 / se[first] ** 2))}, "true": 0.1,
            "fe_all": fe(est, se), "fe_published": fe(est[pub], se[pub]), "re_published": {k: (float(v) if np.ndim(v) == 0 else None) for k, v in re_pub.items()},
            "egger": eg, "replication": {"est": float(big), "se": float(np.sqrt(2 / 2000)), "n": 2000}}


def compute_power() -> dict:
    ns = list(range(8, 201, 4))
    rates = [0.55, 0.6, 0.75, 0.9]
    curves = {str(p): [R.abx_power(p, n)["power"] for n in ns] for p in rates}
    need = {str(p): R.abx_trials_needed(p) for p in rates}
    return {"ns": ns, "curves": curves, "needed": need, "twenty": {str(p): R.abx_power(p, 20) for p in rates}}


def compute_leakage() -> dict:
    """Part 65's order-2 chain, scored on held-out chorales chosen at random (so the same hymn tune, harmonized again,
    can be on both sides) against held-out hymn tunes."""
    ts = MC.tunes()
    leaky, honest = [], []
    for seed in range(10):
        rng = np.random.default_rng(seed)
        idx = rng.permutation(len(ts))
        k = int(0.2 * len(ts))
        te = [ts[i] for i in idx[:k]]
        tr = [ts[i] for i in idx[k:]]
        leaky.append(MC.Markov(2).fit(tr).bits(te))
        tr2, te2 = MC.split(ts, 0.2, seed=seed)
        honest.append(MC.Markov(2).fit(tr2).bits(te2))
        if seed == 0:
            shared = sum(1 for t in te if t["group"] in {x["group"] for x in tr})
    return {"leaky": leaky, "honest": honest, "shared_in_first": shared, "test_size": int(0.2 * len(ts))}


def compute_audit() -> dict:
    out = {}
    # Part 65: which Markov order predicts new hymn tunes best, across ten splits by tune?
    ts = MC.tunes()
    best, bits2 = [], []
    for seed in range(10):
        tr, te = MC.split(ts, 0.2, seed=seed)
        b = {o: MC.Markov(o).fit(tr).bits(te) for o in range(0, 6)}
        best.append(int(min(b, key=b.get)))
        bits2.append(b[2])
    out["p65_best_order"] = {"claim": "order 2 predicts best", "values": best, "share": float(np.mean(np.array(best) == 2)),
                             "bits2_lo": float(np.min(bits2)), "bits2_hi": float(np.max(bits2))}
    # Part 61: YIN's gross errors at 0 dB, across ten noise draws
    from videos.music.music61 import compute as P61
    from explainer.music.monochord.instruments import choir as CH
    from explainer.music.monochord import tune as T
    from explainer.music.monochord.mir import transcribe as TR
    ev = T.events(0.5, [0, 1])
    notes = [(57 + P61.MAJOR[e["degree"]], e["t"], e["dur"]) for e in ev]
    v = CH.sing(notes, "soprano", "a", seed=1)
    v = v / np.max(np.abs(v))
    tt = None
    ge = []
    for seed in range(10):
        nz = np.random.default_rng(100 + seed).standard_normal(len(v)) * np.std(v)
        a = TR.yin(v + nz, SR, fmin=80, fmax=1000)
        truth = np.full(len(a["t"]), np.nan)
        for m, t0, d in notes:
            k = (a["t"] >= t0 + 0.08) & (a["t"] < t0 + d - 0.08)
            truth[k] = TR.midi_hz(m)
        ge.append(TR.gross_error(a["f0"], truth))
    out["p61_yin_0db"] = {"claim": "YIN's gross errors at 0 dB: 9 %", "values": ge, "mean": float(np.mean(ge)), "lo": float(np.min(ge)), "hi": float(np.max(ge))}
    # Part 64: median filtering on three other stretches of the session
    from videos.music.music64 import compute as P64
    from explainer.music.monochord.mir import separate as S
    tonal = []
    for ph in ((0, 1), (2, 3), (4, 5)):
        st = P64.stems(ph)
        r = S.hpss(P64.mix(st))
        tonal.append(S.sdr(st["vocals"] + st["bass"] + st["other"], r["harmonic"]))
    out["p64_hpss_tonal"] = {"claim": "median filtering: tonal stems 7.8 dB", "values": tonal, "lo": float(min(tonal)), "hi": float(max(tonal))}
    # Part 66: how often does the watermark detector fire on unmarked audio?
    from explainer.music.monochord import genaudio as G
    from videos.music.music66 import compute as P66
    _, test = P66.strings_corpus()
    zs = [G.detect(test, 5000 + k, null_keys=20) for k in range(60)]
    out["p66_false_alarms"] = {"claim": "a score above 5 means a mark", "values": zs, "above5": int(np.sum(np.array(zs) > 5)),
                               "max": float(np.max(zs)), "sd": float(np.std(zs))}
    return out


def compute_stars() -> dict:
    ps = R.star_problems(REPO_ROOT)
    q = [(n, t) for n, t in ps if t.endswith("?")]
    acts = [(1, 9), (10, 15), (16, 22), (23, 27), (28, 33), (34, 40), (41, 44), (45, 47), (48, 53), (54, 60), (61, 66), (67, 68)]
    counts = [sum(1 for n, _ in q if a <= n <= b) for a, b in acts]
    return {"problems": q, "count": len(q), "parts": len(ps), "by_act": counts, "acts": acts}


def compute_tune67() -> dict:
    s = load("stemma")
    keys, beats = the_tune()
    c = CLIPS.load("stemma.three")
    return {"names": ["original", "witness", "rebuilt"], "seconds": c.duration, "starts": s["starts"], "witness_errors": s["witness_errors"][s["worst"]],
            "rebuilt_errors": s["majority_errors"],
            "clips": {"variation67": save("tune.variation67", c, detail="Variation 67: the Tune's critical edition: as written, as its most corrupt surviving copy has it, and as rebuilt from all the copies")}}


def compute_variation() -> dict:
    t = load("tune67")
    s = load("stemma")
    return {"part": 67, "title": "a critical edition: the Tune, a corrupt copy, and the original rebuilt", "seconds": round(t["seconds"], 1),
            "measure": f"{s['n_survive']} witnesses; the worst {t['witness_errors']} notes wrong; rebuilt with {t['rebuilt_errors']} wrong",
            "clip": "tune.variation67"}

def compute_canonheard() -> dict:
    """A chorale tune and a tune from Part 14's collection, the first phrase of each, on the piano."""
    t = MC.tunes()[3]
    ch = [n[0] for n in t["notes"]][:12]
    chb = [n[1] / 4 for n in t["notes"]][:12]
    m = ML.corpus()[5]
    fk = [60 + p for p in m.pitches][:12]
    c = concat([C(piano(ch, chb)), C(piano(fk, list(m.beats)[:12]))], gap=0.8, names=["chorale", "tune"])
    st = lambda S: _stats([S])
    return {"chorale": t["name"], "tune": m.name, "chorale_steps": st(ch)["steps"], "tune_steps": st(fk)["steps"],
            "starts": {k: float(c.events[k]) for k in ("chorale", "tune")},
            "clips": {"two": save("canon.two", c, detail=f"the opening of Bach's chorale tune {t['name']}, then of {m.name} from Part 14's collection, on Part 38's piano")}}


def compute_phack() -> dict:
    """Simmons, Nelson and Simonsohn's simulation (2011), from Statistics, Built's kit: no true effect, and the
    false-positive rate as an analyst's choices multiply."""
    rng = np.random.default_rng(11)
    return {"rates": MT.phack(1500, rng)}


def compute_abx2() -> dict:
    """A harder ABX trial: the same phrase through the coder at 128 kbit/s."""
    keys, beats = the_tune()
    y = piano(keys[14:28], beats[14:28])
    coded = K.encode(y, 128)["y"][:len(y)]
    c = concat([C(y), C(coded), C(y)], gap=0.8, names=["A", "B", "X"])
    nmr = K.encode(y, 128).get("nmr", None)
    return {"answer": "A", "kbps": 128, "starts": {k: float(c.events[k]) for k in ("A", "B", "X")},
            "clips": {"three": save("abx2.three", c, detail="a second ABX trial: the Tune's second phrase on Part 38's piano (A), through Part 58's coder at 128 kbit/s (B), then X")}}


def compute_tappers() -> dict:
    """Two simulated people tapping the beat of the same performance (each a little early, each with its own jitter,
    and one who sometimes taps on the off-beat), scored against each other and against the beats as played."""
    from explainer.music.monochord.mir import rhythm as RH
    rng = np.random.default_rng(62)
    beat = 0.5
    t, played = 0.0, []
    for k in range(64):
        played.append(t)
        t += beat * (1 + 0.06 * np.sin(2 * np.pi * k / 16))
    played = np.array(played)
    a = played - 0.03 + rng.normal(0, 0.025, len(played))
    b = played - 0.05 + rng.normal(0, 0.035, len(played))
    off = rng.random(len(b)) < 0.1
    b[off] += beat / 2
    fa = RH.beat_scores(played, a)["f"]
    fb = RH.beat_scores(played, b)["f"]
    fab = RH.beat_scores(a, b)["f"]
    return {"a_vs_played": float(fa), "b_vs_played": float(fb), "a_vs_b": float(fab), "offbeat_share": float(off.mean())}


def compute_audit63() -> dict:
    """Part 63's fingerprinter at 0 dB in bar noise, re-run with three new noise draws."""
    from videos.music.music63 import compute as P63
    idx = P63.index()
    lib = P63.library()
    qs = P63._queries(5.0, seed=7)
    al = P63._aliases(idx, qs)
    rates = []
    for seed in (101, 202, 303):
        rng = np.random.default_rng(seed)
        noise = P63.bar_noise(6.0, seed=seed)
        ok = 0
        for k, seg in qs:
            nz = np.roll(noise, int(rng.integers(len(noise))))[: len(seg)]
            r = idx.query(P63.at_snr(seg, nz, 0.0), SR)
            ok += bool(r and r[0]["track"] in al[k])
        rates.append(ok / len(qs))
    return {"claim": "61 per cent named at 0 dB in bar noise", "values": rates, "n": len(qs)}


def compute_repro() -> dict:
    """The same computation twice: Part 65's order-2 bits, recomputed here and compared with the number Part 65
    stored."""
    from videos.music.music65 import compute as P65
    stored = P65.load("markov")["bits"]["2"]
    ts = MC.tunes()
    tr, te = MC.split(ts, 0.2, seed=0)
    again = MC.Markov(2).fit(tr).bits(te)
    return {"stored": float(stored), "again": float(again), "equal": bool(abs(stored - again) < 1e-12)}


def compute_notation() -> dict:
    """What a staff-notation transcription discards from a sung performance: the Tune sung with Part 8's vibrato and
    glides, tracked by Part 61's YIN, its pitch against the nearest equal-tempered note, in cents."""
    from explainer.music.monochord.instruments import choir as CH
    from explainer.music.monochord import tune as T
    from explainer.music.monochord.mir import transcribe as TR
    MAJ = {1: 0, 2: 2, 3: 4, 4: 5, 5: 7, 6: 9, 7: 11}
    ev = T.events(0.55, [0])
    notes = [(60 + MAJ[e["degree"]], e["t"], e["dur"]) for e in ev]
    y = CH.sing(notes, "alto", "a", seed=9, glide=0.09, vibrato=5.6, depth=0.012)
    y = y / np.max(np.abs(y)) * 0.8
    p = TR.yin(y, SR, fmin=120, fmax=800)
    ok = np.isfinite(p["f0"]) & (np.asarray(p["aperiodicity"]) < 0.2) & (np.asarray(p["f0"]) > 0)
    cents = 1200 * np.log2(np.asarray(p["f0"])[ok] / 440.0) + 6900
    dev = cents - 100 * np.round(cents / 100)
    hist, edges = np.histogram(dev, bins=np.linspace(-50, 50, 41))
    track = (cents / 100).tolist()
    c = concat([C(y)], gap=0.5, names=["sung"])
    return {"track": track[::3], "t": np.asarray(p["t"])[ok][::3].tolist(), "notes": [[m, a, d] for m, a, d in notes],
            "within10": float(np.mean(np.abs(dev) < 10)), "within25": float(np.mean(np.abs(dev) < 25)), "hist": hist.tolist(),
            "edges": edges.tolist(), "sd": float(np.std(dev)),
            "clips": {"one": save("notation.one", C(y), kind="synthesized", detail="the Tune's first phrase sung by Part 8's alto with a wide vibrato and slow glides between notes")}}


def compute_mushra() -> dict:
    """How many listeners a MUSHRA-style comparison needs: paired differences of d points on a 100-point scale, with a
    listener-to-listener spread of 15 points, for 80 per cent power at the 5 per cent level (two-sided paired t)."""
    from scipy import stats as ST
    out = {}
    for d in (3, 5, 10, 20):
        for n in range(3, 2000):
            df = n - 1
            nc = d / (15 / np.sqrt(n))
            crit = ST.t.ppf(0.975, df)
            power = ST.nct.sf(crit, df, nc) + ST.nct.cdf(-crit, df, nc)
            if power >= 0.8:
                out[str(d)] = n
                break
    return {"listeners": out, "sd": 15}


def compute_dupes() -> dict:
    """This series' own library, audited for duplicates: clips of Parts 1 to 60 that hold the same audio as a Variation
    (found by Part 63's fingerprints)."""
    from videos.music.music63 import compute as P63
    r = P63.load("robust")
    return {"variations_with_copies": int(r["n_alias"]), "variations": int(r["n"])}


def compute_pitchstd() -> dict:
    """The Tune's first phrase on organ tones at A = 440 Hz, then at A = 415, a pitch often used for Baroque music
    today, and at A = 466 (a high organ pitch of the time)."""
    from explainer.music.monochord.partkit import organ_tone
    keys, beats = the_tune()
    segs = []
    for a in (440.0, 415.0, 466.0):
        t, y = 0.0, np.zeros(int(8 * SR))
        for m, b in zip(keys[:14], beats[:14]):
            z = organ_tone(a * 2 ** ((m - 69) / 12), b * 0.42 * 0.95, partials=6, rolloff=0.7)
            i = int(t * SR)
            y[i:i + len(z)] += z[: len(y) - i]
            t += b * 0.42
        segs.append(C(y[: int((t + 0.5) * SR)]))
    c = concat(segs, gap=0.8, names=["a440", "a415", "a466"])
    return {"cents_415": float(1200 * np.log2(415 / 440)), "cents_466": float(1200 * np.log2(466 / 440)),
            "starts": {k: float(c.events[k]) for k in ("a440", "a415", "a466")},
            "clips": {"three": save("pitchstd.three", c, kind="synthesized", detail="the Tune's first phrase on organ tones at A = 440 Hz, at A = 415 and at A = 466")}}


def compute_copies() -> dict:
    """Three surviving copies of the simulated tradition, from the first, second and last generations, heard."""
    s = load("stemma")
    keys, beats = the_tune()
    rng = np.random.default_rng(s["seed"])
    t = R.copy_tradition(keys, rng, generations=4, error_rate=0.05)
    sv = t["survive"]
    by_gen = {}
    for i in sv:
        by_gen.setdefault(t["mss"][i]["gen"], []).append(i)
    picks = [by_gen[g][0] for g in sorted(by_gen) if g in (1, 2, 4)]
    segs = [C(piano(t["mss"][i]["notes"][:14], beats[:14])) for i in picks]
    names = [f"g{t['mss'][i]['gen']}" for i in picks]
    c = concat(segs, gap=0.8, names=names)
    return {"gens": [t["mss"][i]["gen"] for i in picks], "errors": [R.hamming(t["mss"][i]["notes"][:14], keys[:14]) for i in picks],
            "names": names, "starts": {k: float(c.events[k]) for k in names},
            "clips": {"three": save("copies.three", c, detail="the Tune's first phrase as three surviving copies of a simulated manuscript tradition have it, from the first, second and fourth generations of copying")}}


def compute_tapsheard() -> dict:
    """The two simulated tappers, heard: a piano performance with each one's taps as clicks."""
    from explainer.music.monochord.mir import rhythm as RH
    rng = np.random.default_rng(62)
    beat = 0.5
    t, played = 0.0, []
    for k in range(64):
        played.append(t)
        t += beat * (1 + 0.06 * np.sin(2 * np.pi * k / 16))
    played = np.array(played)
    a = played - 0.03 + rng.normal(0, 0.025, len(played))
    b = played - 0.05 + rng.normal(0, 0.035, len(played))
    off = rng.random(len(b)) < 0.1
    b[off] += beat / 2
    keys, beats = the_tune()
    n = 16
    placed, tt = [], 0.0
    for i in range(n):
        placed.append((P38.arr(P38.piano(int(keys[i % len(keys)]), 0.45, 0.7)), float(played[i]), -6.0))
    perf = mix(placed, duration=float(played[n - 1]) + 1.0).y
    click = np.sin(2 * np.pi * 2000 * np.arange(int(0.015 * SR)) / SR) * np.exp(-np.arange(int(0.015 * SR)) / (0.003 * SR))
    def with_clicks(times):
        y = perf.copy()
        for x in times[:n]:
            i = int(max(x, 0) * SR)
            y[i:i + len(click)] += 0.5 * click[: len(y) - i]
        return y
    c = concat([C(with_clicks(a)), C(with_clicks(b))], gap=1.0, names=["first", "second"])
    return {"starts": {k: float(c.events[k]) for k in ("first", "second")},
            "clips": {"two": save("taps.two", c, detail="sixteen piano notes played with a gently varying beat, first with one simulated person's taps as clicks, then with another's")}}


def compute_auditheard() -> dict:
    """One of Part 63's queries in a new draw of the bar's noise, level with the music, and what the index said."""
    from videos.music.music63 import compute as P63
    idx = P63.index()
    qs = P63._queries(5.0, seed=7)
    al = P63._aliases(idx, qs)
    k, seg = qs[9]
    noise = P63.bar_noise(6.0, seed=404)[: len(seg)]
    q = P63.at_snr(seg, noise, 0.0)
    r = idx.query(q, SR)
    c = concat([C(q)], gap=0.5, names=["query"])
    return {"truth": f"{k[0]}/{k[1]}", "found": r[0]["track"] if r else None, "ok": bool(r and r[0]["track"] in al[k]),
            "votes": r[0]["votes"] if r else 0,
            "clips": {"one": save("audit.one", C(q), detail=f"five seconds of {k[1]} in a new draw of Part 63's simulated bar noise, music and noise equally loud")}}



ITEMS = {"hook": compute_hook, "stemma": compute_stemma, "canon": compute_canon, "meta": compute_meta, "power": compute_power,
         "leakage": compute_leakage, "audit": compute_audit, "stars": compute_stars, "tune67": compute_tune67,
         "variation": compute_variation, "canonheard": compute_canonheard, "phack": compute_phack, "abx2": compute_abx2,
         "tappers": compute_tappers, "audit63": compute_audit63, "repro": compute_repro, "notation": compute_notation,
         "mushra": compute_mushra, "dupes": compute_dupes, "pitchstd": compute_pitchstd, "copies": compute_copies,
         "tapsheard": compute_tapsheard, "auditheard": compute_auditheard}

if __name__ == "__main__":
    CACHE.main(ITEMS, __doc__)
