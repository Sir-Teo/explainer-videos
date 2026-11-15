"""Precompute everything numerical, and every sound, in Part 55 of *Music, Built* ("Rooms and Space").

    python -m videos.music.music55.compute              # everything missing (about two minutes)
    python -m videos.music.music55.compute --force hook

Numbers are cached in ``.cache/music55/<name>.json``, sounds in ``.cache/music55/audio/``.  The tools are Monochord's
(``explainer/music/monochord/space.py``, and Part 49's image-source room in ``effects.py``); the voice is Part 8's, the
bass Part 38's.  Every room, diffuser, head and loudspeaker layout is simulated; the headphone examples are rendered
with a spherical-head model, not measured ears.

Items:
    hook        an ear question: a voice in a lecture room as Sabine found it (5.6 s) and after his cushions
    cushions    the same room's reverberation as cushions are added, by Sabine's law; three stages heard
    modes       a small room's modes below 120 Hz, counted against Weyl's formula; the image-source room's bass
                response against them; a bass line heard in a corner and in the middle of the room
    flutter     a clap between two parallel walls, bare and with diffusers
    diffuser    a quadratic-residue diffuser's wells and its scattering against a flat panel
    halls       early lateral energy against a hall's width; a voice in a narrow and a wide hall, rendered binaurally
    cues        the interaural time and level differences round a spherical head; a sound at 60 degrees with only
                the time cue, only the level cue, and both (headphones)
    cone        a sound 30 degrees to the front and 150 degrees behind: identical at the ears (headphones)
    pan         a voice panned from left to right with the linear and the constant-power law
    circle      a shaker circling the head twice (headphones)
    images      how many image sources a room has, order by order
    check       the image-source room against Sabine, Eyring and the exact modes
    ambi        first-order Ambisonics on eight loudspeakers: Gerzon's vectors, basic and max-rE; higher orders
    tune55      Variation 55: the Tune walked through four spaces, then circling the listener (headphones)
    variation   the Variations ledger, row 55
"""

from __future__ import annotations

import math

import numpy as np
from scipy.signal import butter, fftconvolve, sosfilt

from explainer.ai.cache import Cache
from explainer.music.monochord import EXAMPLE_LEVEL, SR, Clip, ClipStore, concat, mix
from explainer.music.monochord import effects as E
from explainer.music.monochord import space as SP
from explainer.music.monochord import tune as T
from explainer.music.monochord.instruments import choir as CH
from explainer.music.monochord.partkit import saver
from videos.music.music38 import compute as P38

CACHE = Cache("music55")
CLIPS = ClipStore("music55")
load = CACHE.load
LEVEL = EXAMPLE_LEVEL - 2.5
save = saver(CLIPS, LEVEL, kind="physical model")
MAJOR = {1: 0, 2: 2, 3: 4, 4: 5, 5: 7, 6: 9, 7: 11}


def C(y) -> Clip:
    return Clip(np.asarray(y, float), SR)


def tune_notes(phrases=(0,), base=60, beat=0.5):
    return [(base + MAJOR[e["degree"]], e["t"], e["dur"]) for e in T.events(beat, list(phrases))]


def norm_rms(y, target=0.1):
    return y * target / (np.sqrt(np.mean(np.asarray(y) ** 2)) + 1e-12)


def fade(y, a=0.005, r=0.08):
    y = np.array(y, float)
    ka, kr = max(int(a * SR), 1), max(int(r * SR), 1)
    y[:ka] *= np.linspace(0, 1, ka)[:, None] if y.ndim == 2 else np.linspace(0, 1, ka)
    y[len(y) - kr:] *= np.linspace(1, 0, kr)[:, None] if y.ndim == 2 else np.linspace(1, 0, kr)
    return y


_V = {}


def voice(phrases=(0,), base=48, beat=0.5, part="tenor"):
    key = (tuple(phrases), base, beat, part)
    if key not in _V:
        y = CH.sing(tune_notes(phrases, base, beat), part, "a")
        _V[key] = 0.5 * y / np.max(np.abs(y))
    return _V[key]


def reverb(x, T, wet_db=0.0, seconds=None, seed=0):
    """A dry signal plus a statistical tail of reverberation time T, the tail's energy ``wet_db`` relative to the
    direct sound."""
    seconds = seconds or min(1.2 * T + 0.2, 7.0)
    h = SP.noise_tail(T, seconds, seed=seed, start=0.01)
    wet = fftconvolve(x, h)
    y = np.r_[x, np.zeros(len(wet) - len(x))] + 10 ** (wet_db / 20) * wet
    return y


# ---------------------------------------------------------------------------------------------- Sabine's room
FOGG_V = 2800.0                # m^3: a lecture room of the Fogg's size
FOGG_T0 = 5.6                  # s, empty, as found
CUSHION = 0.22                 # m^2 of absorption per seat cushion (an illustrative value)


def fogg_T(n):
    A0 = 0.161 * FOGG_V / FOGG_T0
    return 0.161 * FOGG_V / (A0 + CUSHION * np.asarray(n, float))


def compute_hook() -> dict:
    v = voice()
    a = reverb(v, FOGG_T0, wet_db=6.0)
    b = reverb(v, float(fogg_T(1500)), wet_db=-1.0, seed=1)
    c = concat([C(norm_rms(fade(a))), C(norm_rms(fade(b)))], gap=1.0, names=["first", "second"])
    return {"answer": "first", "T": [FOGG_T0, float(fogg_T(1500))],
            "starts": {"first": float(c.events["first"]), "second": float(c.events["second"])},
            "clips": {"two": save("hook.two", c, detail="Part 8's voice in a simulated lecture room of the Fogg's size: as found, reverberating for 5.6 s; then with 1,500 cushions' worth of absorption")}}


def compute_cushions() -> dict:
    n = np.arange(0, 2001, 50)
    Ts = fogg_T(n)
    v = voice()
    stages = [0, 300, 1500]
    clips = [C(norm_rms(fade(reverb(v, float(fogg_T(k)), wet_db=6.0 - 7.0 * k / 1500, seed=k)))) for k in stages]
    c = concat(clips, gap=0.8, names=["c0", "c300", "c1500"])
    A0 = 0.161 * FOGG_V / FOGG_T0
    return {"n": n.tolist(), "T": Ts.tolist(), "A0": A0, "cushion": CUSHION, "V": FOGG_V, "stages": stages, "Ts": [float(fogg_T(k)) for k in stages],
            "starts": {k: float(c.events[k]) for k in ("c0", "c300", "c1500")},
            "clips": {"three": save("cushions.three", c, detail="Part 8's voice in the simulated lecture room with no cushions, 300 and 1,500: reverberation " + ", ".join(f"{float(fogg_T(k)):.1f}" for k in stages) + " s")}}


# ---------------------------------------------------------------------------------------------- modes
ROOM = (5.0, 4.0, 2.7)


def bassline(seconds=6.0):
    beat = 0.5
    seq = [36, 36, 43, 43, 45, 45, 43, 41, 41, 40, 40, 38, 38, 36]
    parts = [(Clip(np.asarray(P38.bass(m, beat * 0.9), float), SR), i * beat * 0.5 + 0.0, 0.0) for i, m in enumerate(seq)]
    y = mix(parts, duration=len(seq) * beat * 0.5 + 0.8).y
    return 0.5 * y / np.max(np.abs(y))


def compute_modes() -> dict:
    modes = SP.room_modes(ROOM, 120.0)
    fgrid = np.linspace(20, 120, 101)
    counts = [sum(1 for m in modes if m[0] <= f) for f in fgrid]
    weyl = SP.weyl_count(ROOM, fgrid).tolist()
    pos = {"corner": (0.3, 0.3, 0.3), "middle": (2.5, 2.0, 1.35)}
    src = (4.6, 3.6, 0.3)
    spec = {}
    irs = {}
    for k, mpos in pos.items():
        ir = E.room_ir(ROOM, src, mpos, alpha=0.08, sr=SR, seconds=1.6)
        irs[k] = ir
        H = np.abs(np.fft.rfft(ir, 1 << 18))
        f = np.fft.rfftfreq(1 << 18, 1 / SR)
        sel = (f >= 20) & (f <= 120)
        spec[k] = (20 * np.log10(H[sel] / H[sel].max() + 1e-9))[::3].tolist()
        spec["f"] = f[sel][::3].tolist()
    b = bassline()
    clips = [C(norm_rms(fade(fftconvolve(b, irs[k])[: len(b) + SR]))) for k in ("corner", "middle")]
    c = concat(clips, gap=0.8, names=["corner", "middle"])
    T = E.rt60(irs["middle"], SR)
    V = ROOM[0] * ROOM[1] * ROOM[2]
    return {"modes": [[f, list(n), k] for f, n, k in modes], "fgrid": fgrid.tolist(), "counts": counts, "weyl": weyl, "spec": spec,
            "T": T, "V": V, "fs_room": SP.schroeder_frequency(T, V), "fs_hall": SP.schroeder_frequency(1.9, 18750.0),
            "starts": {"corner": float(c.events["corner"]), "middle": float(c.events["middle"])},
            "clips": {"two": save("modes.two", c, detail="a plucked bass line from Part 38 played from one corner of a simulated 5 x 4 x 2.7 m room, heard in the opposite corner, then in the middle")}}


def compute_flutter() -> dict:
    rng = np.random.default_rng(2)
    n = int(1.6 * SR)
    clap = sosfilt(butter(2, [800, 6000], btype="band", fs=SR, output="sos"), rng.standard_normal(int(0.012 * SR))) * np.hanning(int(0.012 * SR))
    gap = 6.0 / 343.0 * 2                      # a round trip between walls 6 m apart
    bare = np.zeros(n)
    diff = np.zeros(n)
    k = 0
    while k * gap < 1.5:
        i = int(k * gap * SR)
        g = 0.82 ** k
        bare[i:i + len(clap)] += g * clap[: n - i]
        if k == 0:
            diff[i:i + len(clap)] += clap[: n - i]
        else:
            for j in range(12):
                jj = i + int(rng.normal(0, 0.004 * math.sqrt(k)) * SR)
                if 0 <= jj < n - len(clap):
                    diff[jj:jj + len(clap)] += g / math.sqrt(12) * clap * rng.choice([-1, 1])
        k += 1
    claps_b = np.zeros(int(4.0 * SR))
    claps_d = np.zeros(int(4.0 * SR))
    for t0 in (0.0, 1.9):
        i = int(t0 * SR)
        claps_b[i:i + n] += bare[: len(claps_b) - i]
        claps_d[i:i + n] += diff[: len(claps_d) - i]
    c = concat([C(0.4 * claps_b / np.max(np.abs(claps_b))), C(0.4 * claps_d / np.max(np.abs(claps_b)))], gap=0.6, names=["bare", "diffused"])
    return {"gap_ms": 1000 * gap, "rate_hz": 1 / gap, "starts": {"bare": float(c.events["bare"]), "diffused": float(c.events["diffused"])},
            "clips": {"two": save("flutter.two", c, detail="two claps between two parallel hard walls 6 m apart, simulated: bare, then with the walls scattering each reflection")}}


def compute_diffuser() -> dict:
    N, f0, w = 7, 500.0, 0.06
    d = SP.qrd_depths(N, f0)
    ang = np.linspace(-90, 90, 181)
    out = {"depths_cm": (100 * d).tolist(), "N": N, "f0": f0, "width_cm": 100 * w, "angles": ang.tolist(), "pol": {}, "coef": {}}
    for f in (500.0, 1000.0, 2000.0):
        q = 20 * np.log10(SP.scattering(d, w, f, ang) + 1e-9)
        fl = 20 * np.log10(SP.scattering(np.zeros(N), w, f, ang) + 1e-9)
        m = max(q.max(), fl.max())
        out["pol"][str(int(f))] = {"qrd": (q - m).tolist(), "flat": (fl - m).tolist()}
        out["coef"][str(int(f))] = {"qrd": SP.diffusion_coefficient(q[::5]), "flat": SP.diffusion_coefficient(fl[::5])}
    out["residues"] = [n * n % N for n in range(N)]
    return out


# ---------------------------------------------------------------------------------------------- halls
def hall(width, order=3):
    return SP.image_sources((40.0, width, 16.0), (6.0, width / 2 + 1.0, 1.6), (26.0, width / 2 - 1.5, 1.2), order, beta=0.85)


def compute_halls() -> dict:
    widths = [14, 18, 22, 26, 30, 35, 40]
    lf = [SP.lateral_fraction(hall(w, 4)) for w in widths]
    v = voice()
    clips = []
    out_irs = {}
    for name, w in (("narrow", 18.0), ("wide", 40.0)):
        h = SP.binaural_room(hall(w, 3), 1.9, 6.0, 2.6, seed=int(w))
        y = np.stack([fftconvolve(v, h[:, 0]), fftconvolve(v, h[:, 1])], axis=1)
        clips.append(Clip(fade(norm_rms(y)), SR))
        out_irs[name] = SP.lateral_fraction(hall(w, 4))
    c = concat(clips, gap=0.8, names=["narrow", "wide"])
    im = hall(18.0, 2)
    t0 = im[0][0]
    early = [[1000 * (t - t0), g / im[0][1], float(math.degrees(math.atan2(-u[1], -u[0])))] for t, g, u, k in im if (t - t0) < 0.1][:30]
    return {"widths": widths, "lf": lf, "lf_pair": out_irs, "early": early, "starts": {"narrow": float(c.events["narrow"]), "wide": float(c.events["wide"])},
            "clips": {"two": save("halls.two", c, detail="headphones: Part 8's voice from the stage of a simulated 18 m wide shoebox hall, then a 40 m wide one, both reverberating for 1.9 s; the early reflections rendered from their directions by a spherical-head model")}}


# ---------------------------------------------------------------------------------------------- the head
def stereo_render(x, az, itd=True, ild=True):
    n = 512
    f = np.fft.rfftfreq(n, 1 / SR)
    thL = abs(((az + np.pi / 2) + np.pi) % (2 * np.pi) - np.pi)
    thR = abs(((az - np.pi / 2) + np.pi) % (2 * np.pi) - np.pi)
    dt = float(SP.woodworth_itd(az)) if itd else 0.0
    dl = dt / 2 if math.sin(az) > 0 else -dt / 2
    HL = (SP.head_shadow(f, thL) if ild else 1.0) * np.exp(-2j * np.pi * f * (0.002 + dl))
    HR = (SP.head_shadow(f, thR) if ild else 1.0) * np.exp(-2j * np.pi * f * (0.002 - dl))
    hl, hr = np.fft.irfft(HL, n), np.fft.irfft(HR, n)
    return np.stack([fftconvolve(x, hl), fftconvolve(x, hr)], axis=1)


def compute_cues() -> dict:
    az = np.linspace(-np.pi, np.pi, 181)
    itd = (1e6 * SP.woodworth_itd(az) * np.sign(np.sin(az))).tolist()
    ild = {}
    for f in (500.0, 1500.0, 4000.0):
        L = np.array([abs(SP.head_shadow(np.array([f]), abs(((a + np.pi / 2) + np.pi) % (2 * np.pi) - np.pi))[0]) for a in az])
        R = np.array([abs(SP.head_shadow(np.array([f]), abs(((a - np.pi / 2) + np.pi) % (2 * np.pi) - np.pi))[0]) for a in az])
        ild[str(int(f))] = (20 * np.log10(R / L)).tolist()
    rng = np.random.default_rng(3)
    burst = np.zeros(int(2.4 * SR))
    for k in range(6):
        i = int(k * 0.4 * SR)
        nb = sosfilt(butter(2, [200, 9000], btype="band", fs=SR, output="sos"), rng.standard_normal(int(0.15 * SR))) * np.hanning(int(0.15 * SR))
        burst[i:i + len(nb)] += nb
    a60 = math.radians(60)
    clips = [Clip(fade(norm_rms(stereo_render(burst, a60, itd=i_, ild=l_))), SR) for i_, l_ in ((True, False), (False, True), (True, True))]
    c = concat(clips, gap=0.8, names=["time", "level", "both"])
    return {"az": np.degrees(az).tolist(), "itd_us": itd, "ild": ild, "itd_max_us": float(1e6 * SP.woodworth_itd(np.pi / 2)),
            "fc_head": SP.C / (2 * np.pi * SP.HEAD_A), "starts": {k: float(c.events[k]) for k in ("time", "level", "both")},
            "clips": {"three": save("cues.three", c, detail="headphones: noise bursts 60 degrees to the right of a spherical head: the time difference alone, the level difference alone, then both")}}


def compute_cone() -> dict:
    v = voice(phrases=(0,), base=55, part="soprano")
    front = stereo_render(v, math.radians(30))
    back = stereo_render(v, math.radians(150))
    diff = float(np.max(np.abs(front - back)) / np.max(np.abs(front)))
    c = concat([Clip(fade(norm_rms(front)), SR), Clip(fade(norm_rms(back)), SR)], gap=1.0, names=["first", "second"])
    return {"answer": "neither", "max_diff": diff, "itd_30_us": float(1e6 * SP.woodworth_itd(math.radians(30))), "itd_150_us": float(1e6 * SP.woodworth_itd(math.radians(150))),
            "starts": {"first": float(c.events["first"]), "second": float(c.events["second"])},
            "clips": {"two": save("cone.two", c, detail="headphones: Part 8's voice 30 degrees to the right in front of a spherical head, then 150 degrees to the right, behind it")}}


def compute_pan() -> dict:
    p = np.linspace(-1, 1, 101)
    lin = SP.pan_gains(p, "linear")
    pw = SP.pan_gains(p, "power")
    v = voice(phrases=(0, 1), beat=0.4)
    n = len(v)
    pp = np.linspace(-1, 1, n)
    clips = []
    for law in ("linear", "power"):
        gL, gR = SP.pan_gains(pp, law)
        y = np.stack([v * gL, v * gR], axis=1)
        # heard on loudspeakers at +-30 degrees, rendered for headphones
        L = stereo_render(y[:, 0], math.radians(-30))
        R = stereo_render(y[:, 1], math.radians(30))
        clips.append(Clip(fade(0.4 * (L + R) / np.max(np.abs(L + R))), SR))
    c = concat(clips, gap=0.8, names=["linear", "power"])
    phantom = SP.tangent_law(*SP.pan_gains(np.array([-1, -0.5, 0, 0.5, 1.0])))
    return {"p": p.tolist(), "lin_power_db": (10 * np.log10(lin[0] ** 2 + lin[1] ** 2)).tolist(), "pw_power_db": (10 * np.log10(pw[0] ** 2 + pw[1] ** 2)).tolist(),
            "lin": [lin[0].tolist(), lin[1].tolist()], "pw": [pw[0].tolist(), pw[1].tolist()], "phantom": phantom.tolist(),
            "starts": {"linear": float(c.events["linear"]), "power": float(c.events["power"])},
            "clips": {"two": save("pan.two", c, detail="headphones: Part 8's voice panned from the left loudspeaker to the right (both at 30 degrees, rendered round a spherical head), first by the linear law, then by the constant-power law")}}


def compute_ambi() -> dict:
    spk = np.radians(np.arange(0, 360, 45))
    th = np.radians(np.linspace(0, 360, 145))
    res = {}
    for kind in ("basic", "maxre"):
        rv, re, dr = [], [], []
        for t in th:
            v = SP.gerzon_vectors(SP.ambisonic_decode(t, spk, kind), spk)
            rv.append(v["|rV|"])
            re.append(v["|rE|"])
            dr.append(((v["dir_rE"] - math.degrees(t) + 180) % 360) - 180)
        res[kind] = {"rV": rv, "rE": re, "err": dr}
    orders = {str(N): math.cos(math.pi / (2 * N + 2)) for N in (1, 2, 3, 5, 7)}
    spread = {k: math.degrees(math.acos(v)) for k, v in orders.items()}
    g20 = SP.ambisonic_decode(math.radians(20), spk, "basic").tolist()
    return {"theta": np.degrees(th).tolist(), "res": res, "orders_rE": orders, "spread_deg": spread, "gains20": g20, "speakers_deg": np.degrees(spk).tolist()}


def compute_circle() -> dict:
    """A shaker's rhythm circling the head twice in eight seconds, rendered for headphones."""
    rng = np.random.default_rng(6)
    secs = 8.0
    n = int(secs * SR)
    x = np.zeros(n)
    for k in range(int(secs / 0.125)):
        i = int(k * 0.125 * SR)
        L = int(0.06 * SR)
        hit = sosfilt(butter(2, [2500, 9000], btype="band", fs=SR, output="sos"), rng.standard_normal(L)) * np.exp(-np.arange(L) / SR / 0.015)
        x[i:i + L] += (1.0 if k % 2 == 0 else 0.6) * hit[: n - i]
    y = SP.binaural(x, lambda t: 2 * math.pi * 2 * t / secs)
    c = concat([Clip(fade(norm_rms(y)), SR)], names=["circle"])
    return {"seconds": secs, "turns": 2, "clips": {"one": save("circle.one", c, detail="headphones: a shaker's rhythm circling a spherical head twice in eight seconds, starting in front and moving to the right")}}


def compute_check() -> dict:
    """The image-source room against Sabine, Eyring and the exact modes."""
    from scipy.signal import find_peaks
    V = ROOM[0] * ROOM[1] * ROOM[2]
    S = 2 * (ROOM[0] * ROOM[1] + ROOM[1] * ROOM[2] + ROOM[0] * ROOM[2])
    rows = []
    for a in (0.04, 0.08, 0.15, 0.3):
        ir = E.room_ir(ROOM, (4.6, 3.6, 0.3), (2.5, 2.0, 1.35), alpha=a, sr=SR, seconds=min(2.5, 3 * 0.161 * V / (a * S)), air=False)
        rows.append({"alpha": a, "image": E.rt60(ir, SR), "sabine": 0.161 * V / (a * S), "eyring": 0.161 * V / (-S * math.log(1 - a))})
    ir = E.room_ir(ROOM, (4.6, 3.6, 0.3), (0.3, 0.3, 0.3), alpha=0.08, sr=SR, seconds=1.6)
    H = np.abs(np.fft.rfft(ir, 1 << 19))
    f = np.fft.rfftfreq(1 << 19, 1 / SR)
    sel = (f >= 25) & (f <= 90)
    db = 20 * np.log10(H[sel] / H[sel].max() + 1e-12)
    pk, _ = find_peaks(db, prominence=3)
    peaks = f[sel][pk].tolist()
    modes = [m[0] for m in SP.room_modes(ROOM, 90.0)]
    match = [[p_, min(modes, key=lambda m: abs(m - p_))] for p_ in peaks]
    return {"rt": rows, "V": V, "S": S, "peaks": match, "worst_hz": max(abs(a - b) for a, b in match)}


def compute_images() -> dict:
    counts = {str(k): len(SP.image_sources((20.0, 15.0, 10.0), (5.0, 5.0, 2.0), (12.0, 9.0, 1.5), k)) for k in range(1, 9)}
    return {"counts": counts, "reflections_per_s": 4 * math.pi * 343.0 ** 3 / (20.0 * 15.0 * 10.0)}


# ---------------------------------------------------------------------------------------------- Variation 55
def compute_tune55() -> dict:
    v = voice(phrases=(0,), base=48, beat=0.45)
    segs = []
    names = ["anechoic", "room", "hall", "cathedral"]
    # anechoic: the voice straight ahead, rendered for headphones
    segs.append(stereo_render(v, 0.0))
    small = SP.image_sources((5.0, 4.0, 2.7), (4.0, 2.4, 1.6), (1.5, 1.8, 1.2), 3, beta=0.8)
    h = SP.binaural_room(small, 0.45, 0.6, 1.0, seed=1)
    segs.append(np.stack([fftconvolve(v, h[:, 0]), fftconvolve(v, h[:, 1])], axis=1))
    h = SP.binaural_room(hall(20.0, 3), 1.9, 6.0, 2.6, seed=2)
    segs.append(np.stack([fftconvolve(v, h[:, 0]), fftconvolve(v, h[:, 1])], axis=1))
    h = SP.binaural_room(SP.image_sources((80.0, 30.0, 30.0), (10.0, 15.0, 1.6), (50.0, 13.0, 1.6), 2, beta=0.9), 5.0, 14.0, 6.0, seed=3)
    segs.append(np.stack([fftconvolve(v, h[:, 0]), fftconvolve(v, h[:, 1])], axis=1))
    w = voice(phrases=(0, 1), base=48, beat=0.45)
    secs = len(w) / SR
    circ = SP.binaural(w, lambda t: 2 * math.pi * t / secs)
    segs.append(circ)
    names.append("circling")
    c = concat([Clip(fade(norm_rms(s_)), SR) for s_ in segs], gap=0.6, names=names)
    return {"names": names, "T": [0.0, 0.45, 1.9, 5.0], "circle_s": secs, "seconds": c.duration, "starts": {k: float(c.events[k]) for k in names},
            "clips": {"variation55": save("tune.variation55", c, detail="headphones: the Tune's first phrase sung by Part 8's voice with no room, in a small room, in a shoebox hall and in a cathedral (all simulated, rendered round a spherical head); then the first two phrases circling the listener once")}}


def compute_variation() -> dict:
    t = load("tune55")
    return {"part": 55, "title": "walked through four spaces, then circling the listener", "seconds": round(t["seconds"], 1),
            "measure": f"reverberation 0, 0.45, 1.9 and 5.0 s; one circle of the head in {t['circle_s']:.1f} s",
            "clip": "tune.variation55"}


ITEMS = {"hook": compute_hook, "cushions": compute_cushions, "modes": compute_modes, "flutter": compute_flutter, "diffuser": compute_diffuser,
         "halls": compute_halls, "cues": compute_cues, "cone": compute_cone, "pan": compute_pan, "ambi": compute_ambi, "circle": compute_circle, "images": compute_images, "check": compute_check, "tune55": compute_tune55,
         "variation": compute_variation}


if __name__ == "__main__":
    CACHE.main(ITEMS, __doc__)
