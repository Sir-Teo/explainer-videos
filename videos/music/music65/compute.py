"""Precompute everything numerical, and every sound, in Part 65 of *Music, Built* ("Machines that Compose").

    python -m videos.music.music65.compute              # everything missing (several minutes: two transformers train)
    python -m videos.music.music65.compute --force hook

Numbers are cached in ``.cache/music65/<name>.json``, sounds in ``.cache/music65/audio/``; the two transformers in
``.cache/music65/tf_plain.pt`` and ``tf_aug.pt`` (long runs, for their curves) and ``tf_*_final.pt`` (stopped where
the tunes set aside said).  The tools are Monochord's machines
(``explainer/music/monochord/machines.py``); the corpus is the soprano of Bach's major-mode chorales in 4/4, from
Part 17's table, transposed to C and split by hymn tune.  Every tune, generated or Bach's, is heard on Part 17's organ
tones, harmonized where said by Part 17's chord model and voice-leading search.

Items:
    corpus      the tunes, the split by hymn tune, three representations; a chorale as Bach harmonized it
    markov      bits per note on held-out tunes for orders 0 to 8; samples at orders 1, 2 and 8
    copy        the longest copied run and the share copied, by order, against held-out Bach; an order-8 sample beside
                the chorale it copies
    constrained an order-2 chain sampled under constraints (32 notes, ending on the tonic), against a free draw
    recombine   Cope's recombinancy: four phrases from four chorales, harmonized
    transformer two pocket transformers, on the tunes alone and with transposed copies: curves, bits, memorization
    temperature held-out openings continued at three temperatures: interval divergence, cadences, copying
    harmony     a transformer tune harmonized by Part 17's model
    judge       every generator against held-out Bach by the same judges
    hook        an ear question: three harmonized phrases, one Bach's
    tune65      Variation 65: the Tune's first phrase continued at five temperatures, uncurated
    variation   the Variations ledger, row 65
    surprise    bits note by note along a tune kept back, for the chain and the transformer
    samples     the first three tunes the transformer draws from nothing
    copyquiz    an ear question: a transformer tune and an order-8 tune, harmonized; which is copied?
    bachvs17    a tune kept back, harmonized by Bach and by Part 17's search
"""

from __future__ import annotations

import numpy as np

from explainer.ai.cache import Cache
from explainer.music.monochord import EXAMPLE_LEVEL, Clip, ClipStore, concat
from explainer.music.monochord import fourpart as FP
from explainer.music.monochord import machines as M
from explainer.music.monochord import tune as T
from explainer.music.monochord.partkit import saver, signoff
from videos.music.music17 import compute as P17

CACHE = Cache("music65")
CLIPS = ClipStore("music65")
load = CACHE.load
LEVEL = EXAMPLE_LEVEL - 2.5
save = saver(CLIPS, LEVEL, kind="synthesized")
MAJOR = {1: 0, 2: 2, 3: 4, 4: 5, 5: 7, 6: 9, 7: 11}
TEMPS = (0.5, 1.0, 1.5)
TUNE_TEMPS = (0.25, 0.5, 0.8, 1.0, 1.5)

_D: dict = {}


def data():
    if "d" not in _D:
        ts = M.tunes()
        train, test = M.split(ts, 0.2, seed=0)
        fit, valid = M.split(train, 0.1, seed=1)            # the transformers choose nothing on the test tunes
        _D["d"] = (ts, train, test, fit, valid, M.train_grams(train))
    return _D["d"]


def model_chords():
    if "cm" not in _D:
        _D["cm"] = FP.ChordModel(P17.book(), "major")
    return _D["cm"]


def melody_clip(notes) -> Clip:
    _, _, voice = M.soprano_beats(notes)
    c, _ = P17.sing([voice, [], [], []], which=(0,), organ=True)
    return c


def harmonized(notes) -> Clip:
    sop, ferm, voice = M.soprano_beats(notes)
    r = FP.harmonize(sop, 0, model_chords(), fermatas=ferm)
    voices = P17.from_chords(r["chords"], soprano_voice=voice, ferm=set(ferm))
    c, _ = P17.sing(voices, organ=True)
    return c


def first_phrases(notes, k: int = 2):
    out, seen = [], 0
    for n in notes:
        out.append(n)
        if n[2]:
            seen += 1
            if seen == k:
                break
    return out


def tune_notes():
    """The series' Tune in C as (key, sixteenths, fermata), a fermata at each phrase's end."""
    ev = T.events(0.5, None)
    out = []
    for i, e in enumerate(ev):
        last = i + 1 == len(ev) or ev[i + 1]["phrase"] != e["phrase"]
        out.append((72 + MAJOR[e["degree"]] - 12 * (MAJOR[e["degree"]] > 9), int(round(e["dur"] / 0.5 * 4)), last))
    return out


def harmonizable(notes) -> bool:
    try:
        sop, ferm, _ = M.soprano_beats(notes)
        FP.harmonize(sop, 0, model_chords(), fermatas=ferm)
        return True
    except ValueError:
        return False


def to_c(x):
    """A draw moved to C (or A minor) from the key the key finder hears in it, by the smaller move."""
    from explainer.music.monochord import key as K
    if not x:
        return x
    (tonic, mode), _ = K.ranking(K.distribution([n[0] for n in x], [n[1] for n in x]))[0]
    home = tonic if mode == "major" else (tonic + 3) % 12
    shift = -home if home <= 6 else 12 - home
    return [(p + shift, d, f) for p, d, f in x]


def chorale_like(draw, seed0: int, phrases: int = 2, tries: int = 200, transpose: bool = True):
    """The first draw (seeds from ``seed0`` up) whose first ``phrases`` phrases, moved to C from the major key the key
    finder hears in them, stay in C major, end on the tonic and can be harmonized; returns (notes, seed).  Draws are not
    otherwise chosen: the first that qualifies is kept."""
    from explainer.music.monochord import key as K
    for s in range(seed0, seed0 + tries):
        x = first_phrases(draw(s), phrases)
        if not x:
            continue
        if transpose:
            (tonic, mode), _ = K.ranking(K.distribution([n[0] for n in x], [n[1] for n in x]))[0]
            if mode != "major":
                continue
            x = to_c(x)
        if sum(1 for n in x if n[2]) < phrases or x[-1][0] % 12 != 0:
            continue
        if any(n[0] % 12 not in MAJOR.values() for n in x):
            continue
        if harmonizable(x):
            return x, s
    raise ValueError("no draw qualified")


_TF: dict = {}


def _long_run(kind: str) -> dict:
    """A long run (1,500 steps), kept for its curve: it shows where held-out loss turns round."""
    import torch
    path = CACHE.dir / f"tf_{kind}.pt"
    if path.exists():
        return torch.load(path, weights_only=False)["info"]
    _, _, _, fit, valid, _ = data()
    tp = (0,) if kind == "plain" else tuple(range(-5, 7))
    r = M.train_transformer(fit, valid, transpose=tp, steps=1500, threads=2, seed=0)
    from dataclasses import asdict
    info = {k: r[k] for k in ("curve", "train_tokens", "params", "seconds")}
    path.parent.mkdir(parents=True, exist_ok=True)
    torch.save({"config": asdict(r["model"].cfg), "state": r["model"].state_dict(), "info": info}, path)
    return info


def long_model(kind: str):
    """The long run's model itself, trained well past its best (for the memorization demonstration)."""
    import torch
    from explainer.lm import pocket
    _long_run(kind)
    ck = torch.load(CACHE.dir / f"tf_{kind}.pt", weights_only=False)
    model = pocket.PocketGPT(pocket.Config(**ck["config"]))
    model.load_state_dict(ck["state"])
    return model


def transformer(kind: str):
    """``plain``: the training tunes alone; ``aug``: each also in eleven other keys (-5 to +6 semitones).  The model
    used is trained for as many steps as the long run needed to reach its lowest loss on the tunes set aside (the
    test tunes play no part in the choice)."""
    if kind in _TF:
        return _TF[kind]
    import torch
    from explainer.lm import pocket
    long = _long_run(kind)
    c = np.array(long["curve"])
    best = int(c[int(np.argmin(c[:, 1])), 0])
    path = CACHE.dir / f"tf_{kind}_final.pt"
    if path.exists():
        ck = torch.load(path, weights_only=False)
        model = pocket.PocketGPT(pocket.Config(**ck["config"]))
        model.load_state_dict(ck["state"])
        _TF[kind] = {"model": model, **ck["info"]}
        return _TF[kind]
    _, _, _, fit, valid, _ = data()
    tp = (0,) if kind == "plain" else tuple(range(-5, 7))
    r = M.train_transformer(fit, valid, transpose=tp, steps=max(best, 60), threads=2, seed=0)
    from dataclasses import asdict
    info = {"curve": long["curve"], "train_tokens": r["train_tokens"], "params": r["params"], "seconds": r["seconds"] + long["seconds"],
            "steps": max(best, 60), "final_curve": r["curve"]}
    torch.save({"config": asdict(r["model"].cfg), "state": r["model"].state_dict(), "info": info}, path)
    _TF[kind] = {"model": r["model"], **info}
    return _TF[kind]


def stats(samples, grams) -> dict:
    return {"longest": float(np.mean([M.longest_copy(s, grams)["length"] for s in samples])),
            "share8": float(np.mean([M.copied_share(s, grams, 8) for s in samples])),
            "notes": float(np.mean([len(s) for s in samples]))}


# ---------------------------------------------------------------------------------------------- items
def compute_corpus() -> dict:
    ts, train, test, fit, valid, _ = data()
    reps = M.representations(ts)
    ex = test[0]
    ph = first_phrases(ex["notes"], 1)
    enc = {"note": [f"({p},{d}{',F' if f else ''})" for p, d, f in ph[:6]],
           "split": [M.VOCAB[i] for i in M.encode(ph[:4], bos=False, eos=False)],
           "grid": sum([[str(p)] + ["_"] * (d - 1) for p, d, f in ph[:3]], [])}
    c = P17.chorale(ex["name"])
    t1 = P17.phrase_end(c, 2)
    voices = P17.cut(c.voices, min(o for _, o, _, _ in c.voices[0]), t1)
    cl, _ = P17.sing(voices, organ=True)
    return {"chorales": len(P17.book()), "tunes": len(ts), "hymn_tunes": len({t["group"] for t in ts}), "train": len(train),
            "test": len(test), "fit": len(fit), "valid": len(valid), "train_notes": sum(len(t["notes"]) for t in train),
            "reps": reps, "example": ex["name"], "encodings": enc,
            "clips": {"bach": save("corpus.bach", cl, detail=f"the first two phrases of the chorale {ex['name']} as Bach harmonized it, on organ tones")}}


def compute_markov() -> dict:
    _, train, test, _, _, _ = data()
    bits = {o: M.Markov(o).fit(train).bits(test) for o in range(0, 9)}
    samples = {}
    for o in (1, 2, 8):
        samples[o] = M.Markov(o).fit(train).sample(seed=3)
    segs = [melody_clip(first_phrases(samples[o], 2)) for o in (1, 2, 8)]
    c = concat(segs, gap=1.0, names=["o1", "o2", "o8"])
    return {"bits": {str(k): v for k, v in bits.items()}, "best": int(min(bits, key=bits.get)), "samples": {str(k): v for k, v in samples.items()},
            "starts": {k: float(c.events[k]) for k in ("o1", "o2", "o8")},
            "clips": {"three": save("orders.three", c, detail="the first two phrases of tunes drawn from Markov models of orders 1, 2 and 8 trained on Bach's chorale melodies")}}


def compute_copy() -> dict:
    _, train, test, _, _, grams = data()
    out = {}
    for o in (1, 2, 3, 4, 6, 8):
        m = M.Markov(o).fit(train)
        out[str(o)] = stats([m.sample(seed=s) for s in range(20)], grams)
    bach = stats([t["notes"] for t in test], grams)
    s8 = M.Markov(8).fit(train).sample(seed=3)
    lc = M.longest_copy(s8, grams)
    src = next(t for t in train if t["name"] == lc["source"])
    seg = s8[lc["start"]:lc["start"] + lc["length"]]
    c = concat([melody_clip(seg), melody_clip(first_phrases(src["notes"], 3))], gap=1.0, names=["sample", "source"])
    return {"orders": out, "bach": bach, "sample_copy": lc, "source": src["name"], "bits": load("markov")["bits"],
            "starts": {k: float(c.events[k]) for k in ("sample", "source")},
            "clips": {"two": save("copy.two", c, detail=f"the longest copied stretch of an order-8 sample, then the opening of the chorale it came from ({src['name']})")}}


def compute_constrained() -> dict:
    _, train, _, _, _, grams = data()
    r = M.constrained(train, length=32, seed=2)
    c = concat([melody_clip(r["free"]), melody_clip(r["notes"])], gap=1.0, names=["free", "constrained"])
    return {"p_legal": r["p_legal"], "notes": r["notes"], "free": r["free"], "free_end": r["free"][-1], "end": r["notes"][-1],
            "copy": M.longest_copy(r["notes"], grams), "starts": {k: float(c.events[k]) for k in ("free", "constrained")},
            "clips": {"two": save("constrained.two", c, detail="32 notes from an order-2 chain on Bach's chorale melodies drawn freely, then drawn under constraints (ending on the tonic, long, under a fermata)")}}


def compute_recombine() -> dict:
    _, train, _, _, _, grams = data()
    r = M.recombine(train, seed=4)
    c = harmonized(r["notes"])
    return {**r, "copy": M.longest_copy(r["notes"], grams), "share8": M.copied_share(r["notes"], grams, 8),
            "clips": {"one": save("recombined.one", c, detail="a chorale tune recombined from phrases of four Bach chorales, harmonized by Part 17's model")}}


def compute_transformer() -> dict:
    _, train, test, fit, valid, grams = data()
    out = {}
    plain_samples = []
    for kind in ("plain", "aug"):
        tf = transformer(kind)
        smp = [M.transformer_sample(tf["model"], temperature=1.0, seed=s) for s in range(12)]
        smp = [s for s in smp if len(s) >= 8]
        if kind == "plain":
            plain_samples = smp
        out[kind] = {"bits": M.transformer_bits(tf["model"], test), "curve": tf["curve"], "train_tokens": tf["train_tokens"],
                     "params": tf["params"], "seconds": tf["seconds"], "steps": tf["steps"], **stats(smp, grams)}
    over = long_model("plain")
    over_samples = [s for s in (M.transformer_sample(over, temperature=1.0, seed=s) for s in range(12)) if len(s) >= 8]
    out["overtrained"] = stats(over_samples, grams)
    best = max(over_samples, key=lambda s: M.longest_copy(s, grams)["length"])
    lc = M.longest_copy(best, grams)
    src = next(t for t in train if t["name"] == lc["source"])
    c = concat([melody_clip(first_phrases(best, 2)), melody_clip(first_phrases(src["notes"], 2))], gap=1.0, names=["sample", "source"])
    out["markov2"] = load("markov")["bits"]["2"]
    out["memorized"] = {"copy": lc, "source": src["name"], "notes": len(best)}
    out["starts"] = {k: float(c.events[k]) for k in ("sample", "source")}
    out["clips"] = {"two": save("plain.two", c, detail=f"a tune from the transformer trained on the tunes alone, then the chorale it copies most ({src['name']})")}
    return out


def compute_temperature() -> dict:
    _, train, test, _, _, grams = data()
    tf = transformer("aug")["model"]
    rows = {}
    for temp in TEMPS:
        conts = []
        for k, t in enumerate(test):
            op = first_phrases(t["notes"], 1)
            for rep in range(2):
                conts.append(op + M.transformer_sample(tf, op, temperature=temp, seed=100 * rep + k, min_tokens=6)[:60])
        chrom = float(np.mean([n[0] % 12 not in MAJOR.values() for s in conts for n in s]))
        rows[str(temp)] = {"kl": M.intervals_kl(conts, test), "cadence": M.cadence_share(conts), "chromatic": chrom, **stats(conts, grams)}
    bach = {"kl": 0.0, "cadence": M.cadence_share(test), "chromatic": float(np.mean([n[0] % 12 not in MAJOR.values() for t in test for n in t["notes"]])),
            **stats([t["notes"] for t in test], grams)}
    op = first_phrases(test[1]["notes"], 1)
    segs = [melody_clip(op + first_phrases(M.transformer_sample(tf, op, temperature=temp, seed=11, min_tokens=6), 1)) for temp in TEMPS]
    c = concat(segs, gap=1.0, names=["t05", "t10", "t15"])
    return {"temps": list(TEMPS), "rows": rows, "bach": bach, "opening": test[1]["name"], "starts": {k: float(c.events[k]) for k in ("t05", "t10", "t15")},
            "clips": {"three": save("temperature.three", c, detail=f"the opening phrase of {test[1]['name']}, continued by the transformer at temperatures 0.5, 1.0 and 1.5")}}


def compute_harmony() -> dict:
    tf = transformer("aug")["model"]
    _, _, test, _, _, grams = data()
    x, seed = chorale_like(lambda k: M.transformer_sample(tf, (), temperature=0.9, seed=k), 100, phrases=4)
    sop, ferm, voice = M.soprano_beats(x)
    r = FP.harmonize(sop, 0, model_chords(), fermatas=ferm)
    pars = sum(len(FP.parallels(a, b)) for a, b in zip(r["chords"], r["chords"][1:]))
    voices = P17.from_chords(r["chords"], soprano_voice=voice, ferm=set(ferm))
    c, _ = P17.sing(voices, organ=True)
    return {"notes": x, "seed": seed, "skipped": seed - 100, "chords": r["chords"], "parallels": pars, "copy": M.longest_copy(x, grams),
            "clips": {"one": save("harmony.one", c, detail="a tune drawn from the transformer, harmonized in four parts by Part 17's chord model and voice-leading search")}}


def compute_judge() -> dict:
    _, train, test, _, _, grams = data()
    gens = {}
    for o in (1, 2, 8):
        m = M.Markov(o).fit(train)
        gens[f"order {o}"] = [m.sample(seed=s) for s in range(20)]
    gens["recombined"] = [M.recombine(train, seed=s)["notes"] for s in range(20)]
    tf = transformer("aug")["model"]
    gens["transformer"] = [to_c(s) for s in (M.transformer_sample(tf, (), temperature=1.0, seed=200 + s) for s in range(20)) if len(s) >= 8]
    gens["Bach (held out)"] = [t["notes"] for t in test]
    rows = {}
    for k, v in gens.items():
        rows[k] = {"kl": M.intervals_kl(v, test) if k != "Bach (held out)" else 0.0, "cadence": M.cadence_share(v), **stats(v, grams)}
    return {"rows": rows, "order": list(gens)}


def compute_hook() -> dict:
    _, train, test, _, _, _ = data()
    c = P17.chorale(test[2]["name"])
    t1 = P17.phrase_end(c, 2)
    bach, _ = P17.sing(P17.cut(c.voices, min(o for _, o, _, _ in c.voices[0]), t1), organ=True)
    m2 = M.Markov(2).fit(train)
    mk, _ = chorale_like(lambda k: m2.sample(seed=k), 7, transpose=False)
    tf, _ = chorale_like(lambda k: M.transformer_sample(transformer("aug")["model"], (), temperature=0.9, seed=k), 7)
    a = harmonized(mk)
    b = harmonized(tf)
    cl = concat([a, bach, b], gap=1.0, names=["first", "second", "third"])
    return {"answer": "second", "bach": test[2]["name"], "starts": {k: float(cl.events[k]) for k in ("first", "second", "third")},
            "clips": {"three": save("hook.three", cl, detail=f"two phrases three times on organ tones: a Markov tune harmonized by Part 17's model, Bach's {test[2]['name']}, a transformer tune harmonized by the same model")}}


def compute_tune65() -> dict:
    tf = transformer("aug")["model"]
    tn = tune_notes()
    op = first_phrases(tn, 1)
    segs, conts = [], []
    for k, temp in enumerate(TUNE_TEMPS):
        cont = first_phrases(M.transformer_sample(tf, op, temperature=temp, seed=65, min_tokens=6), 1)
        conts.append(cont)
        segs.append(melody_clip(op + cont))
    names = [f"t{k}" for k in range(len(TUNE_TEMPS))]
    c = concat(segs, gap=1.0, names=names)
    _, _, _, _, _, grams = data()
    return {"temps": list(TUNE_TEMPS), "opening": op, "continuations": conts, "names": names, "seconds": c.duration,
            "starts": {k: float(c.events[k]) for k in names}, "copies": [M.longest_copy(x, grams)["length"] for x in conts],
            "clips": {"variation65": save("tune.variation65", c, detail="Variation 65: the Tune's first phrase, continued by the transformer at five temperatures, one draw each, uncurated")}}


def compute_variation() -> dict:
    t = load("tune65")
    return {"part": 65, "title": "the Tune's first phrase continued at five temperatures, uncurated", "seconds": round(t["seconds"], 1),
            "measure": f"temperatures {', '.join(f'{x:g}' for x in t['temps'])}; longest copied run {max(t['copies'])} notes",
            "clip": "tune.variation65"}

def compute_surprise() -> dict:
    """Bits note by note along one tune kept back, for the order-2 chain and the transformer: where Bach surprises."""
    import math
    import torch
    import torch.nn.functional as F
    _, train, test, _, _, _ = data()
    t = test[3]
    s2 = M.Markov(2).fit(train).ng.surprise(t["notes"]).tolist()
    tf = transformer("aug")["model"]
    ids = M.encode(t["notes"])
    tf.eval()
    with torch.no_grad():
        lp = F.log_softmax(tf(torch.tensor([ids[:-1]]))[0], -1)
    tok = (-lp[torch.arange(len(ids) - 1), torch.tensor(ids[1:])] / math.log(2)).tolist()
    per, k = [], 0
    for p, d, f in t["notes"]:
        n = 2 + int(f)
        per.append(float(sum(tok[k:k + n])))
        k += n
    ends = [i for i, n in enumerate(t["notes"]) if n[2]]
    after = [i + 1 for i in ends if i + 1 < len(t["notes"])]
    return {"name": t["name"], "notes": t["notes"], "markov": s2, "transformer": per, "ends": ends,
            "mean_at_ends": float(np.mean([per[i] for i in ends])), "mean_after_ends": float(np.mean([per[i] for i in after])),
            "markov_at_ends": float(np.mean([s2[i] for i in ends])), "markov_after_ends": float(np.mean([s2[i] for i in after])),
            "markov_mean": float(np.mean(s2)),
            "mean": float(np.mean(per))}


def compute_samples() -> dict:
    """Three tunes from the transformer trained in twelve keys, from nothing, at temperature 1: the first three drawn."""
    tf = transformer("aug")["model"]
    _, _, _, _, _, grams = data()
    out = [first_phrases(M.transformer_sample(tf, (), temperature=1.0, seed=300 + s), 2) for s in range(3)]
    c = concat([melody_clip(x) for x in out], gap=1.0, names=["one", "two", "three"])
    keys = []
    from explainer.music.monochord import key as K
    for x in out:
        dist = K.distribution([n[0] for n in x], [n[1] for n in x])
        keys.append(K.key_name(K.ranking(dist)[0][0]))
    return {"tunes": out, "keys": keys, "copies": [M.longest_copy(x, grams)["length"] for x in out],
            "starts": {k: float(c.events[k]) for k in ("one", "two", "three")},
            "clips": {"three": save("samples.three", c, detail="the first two phrases of the first three tunes the transformer drew from nothing, at temperature 1")}}


def compute_copyquiz() -> dict:
    """An ear question: two tunes of two phrases, one from the order-8 chain (mostly copied), one from the transformer."""
    _, train, _, _, _, grams = data()
    m8 = M.Markov(8).fit(train)
    a, _ = chorale_like(lambda k: m8.sample(seed=k), 21, transpose=False)
    b, _ = chorale_like(lambda k: M.transformer_sample(transformer("aug")["model"], (), temperature=0.9, seed=k), 21)
    c = concat([harmonized(b), harmonized(a)], gap=1.0, names=["first", "second"])
    return {"answer": "second", "copied": M.copied_share(a, grams, 8), "copied_new": M.copied_share(b, grams, 8),
            "longest": M.longest_copy(a, grams), "longest_new": M.longest_copy(b, grams),
            "starts": {k: float(c.events[k]) for k in ("first", "second")},
            "clips": {"two": save("copyquiz.two", c, detail="two machine tunes harmonized by Part 17: the transformer's, then an order-8 chain's")}}


def compute_bachvs17() -> dict:
    """One tune kept back, harmonized by Bach and by Part 17's search."""
    _, _, test, _, _, _ = data()
    t = test[5]
    ch = P17.chorale(t["name"])
    t1 = P17.phrase_end(ch, 2)
    bach, _ = P17.sing(P17.cut(ch.voices, min(o for _, o, _, _ in ch.voices[0]), t1), organ=True)
    ours = harmonized(first_phrases(t["notes"], 2))
    c = concat([bach, ours], gap=1.0, names=["bach", "ours"])
    return {"name": t["name"], "starts": {k: float(c.events[k]) for k in ("bach", "ours")},
            "clips": {"two": save("bachvs17.two", c, detail=f"the first two phrases of {t['name']} as Bach harmonized it, then as Part 17's search harmonizes the same tune (in C)")}}



def compute_signoff() -> dict:
    """The part's last sound: the opening of its Variation, under the next part's title."""
    load("variation")
    return signoff(CLIPS, "tune.variation65", 65)


ITEMS = {"corpus": compute_corpus, "markov": compute_markov, "copy": compute_copy, "constrained": compute_constrained,
         "recombine": compute_recombine, "transformer": compute_transformer, "temperature": compute_temperature,
         "harmony": compute_harmony, "judge": compute_judge, "hook": compute_hook, "tune65": compute_tune65,
         "variation": compute_variation, "surprise": compute_surprise, "samples": compute_samples, "copyquiz": compute_copyquiz,
         "bachvs17": compute_bachvs17,
         "signoff": compute_signoff}

if __name__ == "__main__":
    CACHE.main(ITEMS, __doc__)
