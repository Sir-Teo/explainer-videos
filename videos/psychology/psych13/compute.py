"""Precompute every number in Part 13 of *Psychology, Built* ("The Eye and the Code").

    python -m videos.psychology.psych13.compute            # everything missing, into .cache/psych13/
    python -m videos.psychology.psych13.compute --force quanta

Results are cached in ``.cache/psych13/<name>.json`` (+ ``.npz``); scenes call ``load(name)``.  The models are
Psyche's (``explainer.psychology.psyche.vision``); the colour tables are the CIE's, Stiles and Burch's and Stockman
and Sharpe's (``archive.COLOUR_TABLES``).  Every simulated study the film shows alone is picked by rule (the median
of many), never by its result.

Items:
    quanta      frequency-of-seeing curves for k = 1..9 absorptions; a simulated Hecht-style experiment, fitted, and
                the spread of the fitted k over 101 such experiments; the 1942 losses; the 2016 single-photon test
    optics      the eye's MTF for three pupils; the line spread; the cone mosaic's Nyquist limit and an aliased grating
    adapt       response curves at several backgrounds; increment thresholds with and without gain control
    rate        a stretch receptor's rate against load and its adaptation in time (schematic, after Adrian 1926)
    retina      the DoG profile and its band-pass response; Mach bands; a 1/f image before and after the DoG
    cortex      a Gabor field; orientation tuning; simple and complex cells against phase; a simulated 1959 recording
    csf         the CSF, its fit to simulated thresholds, the acuity it implies, the Campbell-Robson chart
    hybrid      a two-letter hybrid image filtered by the CSF at a near and a far viewing distance
    channels    adaptation to one grating in a bank of channels; normalization and a cross-orientation mask
    cones       cone fundamentals, the rods, a light's spectrum and its three numbers
    matching    colour matching with Stiles and Burch's primaries; derived functions against their 1955 data; a
                metamer pair; the chromaticity diagram and the sRGB gamut
    opponent    opponent channels against wavelength; dichromacy on a palette; the Okabe-Ito palette checked
    dress       a stand-in swatch read under a warm and a cool assumed light; the 2015 survey
    streams     D.F.'s slot task, schematic: matching against posting
    practice    chroma subsampling against luminance subsampling on a synthetic scene
"""

from __future__ import annotations

import math

import numpy as np
from scipy import stats

from explainer.ai.cache import Cache
from explainer.psychology import archive
from explainer.psychology.psyche import neuron as N
from explainer.psychology.psyche import vision as V

CACHE = Cache("psych13")
load = CACHE.load


def rng(seed: int) -> np.random.Generator:
    return np.random.Generator(np.random.PCG64(seed))


def _nested(obj):
    """Arrays inside dicts and lists become lists (the cache stores only top-level arrays as arrays)."""
    if isinstance(obj, np.ndarray):
        return obj.tolist()
    if isinstance(obj, dict):
        return {k: _nested(v) for k, v in obj.items()}
    if isinstance(obj, (list, tuple)):
        return [_nested(v) for v in obj]
    if isinstance(obj, np.generic):
        return obj.item()
    return obj


def _cacheable(out: dict) -> dict:
    return {k: (v if isinstance(v, np.ndarray) else _nested(v)) for k, v in out.items()}


def _median_pick(values) -> int:
    v = np.asarray(values, float)
    return int(np.argsort(v)[len(v) // 2])


# ------------------------------------------------------------------------------------------------- quanta
K_TRUE, EFF_TRUE = 6, 0.09  # Psyche's observer: 6 absorptions needed; 9% of corneal quanta absorbed


def compute_quanta() -> dict:
    h = archive.HECHT_1942.data
    lam = np.geomspace(0.3, 40, 300)  # mean absorptions
    curves = {k: V.frequency_of_seeing(lam, k) for k in range(1, 10)}
    slopes = {k: V.fos_slope(k) for k in range(1, 10)}
    # a simulated experiment: 7 intensities (quanta at the cornea), 50 flashes each; 101 repeats, the median by k
    q = np.geomspace(25, 250, 7)
    fits = []
    for s in range(101):
        y = V.simulate_fos(K_TRUE, EFF_TRUE, q, 50, rng=rng(1300 + s))
        f = V.fit_fos(q, y, 50)
        fits.append((f["k"], f["efficiency"], y))
    ks = np.array([f[0] for f in fits])
    order = np.lexsort((np.array([f[1] for f in fits]), ks))
    pick = fits[int(order[len(order) // 2])]
    qq = np.geomspace(15, 400, 200)
    best = V.fit_fos(q, pick[2], 50)
    loss = [("at the cornea", 1.0), ("after reflection", 1 - h["reflection"]),
            ("after the eye's media", (1 - h["reflection"]) * (1 - h["media"])),
            ("absorbed by rods", (1 - h["reflection"]) * (1 - h["media"]) * h["retina_absorbed"])]
    t = archive.TINSLEY_2016.data
    return {"lam": lam, "curves": {str(k): v for k, v in curves.items()}, "slopes": {str(k): v for k, v in slopes.items()},
            "q": q, "seen": pick[2], "n": 50, "k_fit": best["k"], "eff_fit": best["efficiency"], "qq": qq,
            "fit_curve": V.frequency_of_seeing(qq, best["k"], best["efficiency"]),
            "profile_k": list(best["profile"].keys()), "profile_ll": list(best["profile"].values()),
            "k_counts": np.bincount(ks, minlength=13)[:13], "k_true": K_TRUE, "eff_true": EFF_TRUE,
            "k_within1": float(np.mean(np.abs(ks - K_TRUE) <= 1)),
            "loss": loss, "cornea": h["cornea"], "absorbed": h["absorbed"],
            "tinsley": (t["p_correct"], t["se"], t["p_value"], t["trials"], t["single_photon_events"]),
            "baylor": archive.BAYLOR_1979.data}


# ------------------------------------------------------------------------------------------------- optics
def compute_optics() -> dict:
    f = np.linspace(0, 100, 401)
    mtf = {p: V.diffraction_mtf(f, p) for p in (2.0, 3.0, 6.0)}
    eye = V.eye_mtf(f, 3.0, blur_arcmin=0.5)
    x = np.linspace(-3, 3, 241)
    lsf = V.line_spread(x, 3.0, blur_arcmin=0.5)
    # the mosaic: cones 0.5 arcmin apart sample at 120 per degree; an 80 c/deg grating aliases to 40
    xs = np.linspace(0, 0.05, 1000)  # degrees
    fine = np.cos(2 * np.pi * 80 * xs)
    samples = np.arange(0, 0.05 + 1e-9, 1 / 120)
    alias = np.cos(2 * np.pi * 40 * xs)
    return {"f": f, "mtf": {str(k): v for k, v in mtf.items()}, "eye": eye, "cutoff": V.cutoff_cpd(3.0),
            "cutoff2": V.cutoff_cpd(2.0), "cutoff6": V.cutoff_cpd(6.0), "x": x, "lsf": lsf,
            "lsf_fwhm": float(2 * x[lsf >= 0.5].max()), "nyquist": V.nyquist_cpd(0.5),
            "eye_at_60": float(V.eye_mtf(60.0, 3.0, blur_arcmin=0.5)), "xs": xs, "fine": fine, "samples": samples,
            "sampled": np.cos(2 * np.pi * 80 * samples), "alias": alias}


# ------------------------------------------------------------------------------------------------- adaptation
def compute_adapt() -> dict:
    li = np.linspace(-4, 8, 400)
    i = 10 ** li
    bgs = (-2, 1, 4, 7)
    curves = {str(b): V.naka_rushton(i, 10.0 ** b) for b in bgs}
    fixed = V.naka_rushton(i, 10.0)
    lb = np.linspace(-4, 8, 200)
    b = 10 ** lb
    tvi = V.increment_threshold(b, sigma0=1.0, adapt=True)
    tvi_fixed = V.increment_threshold(b, sigma0=1.0, adapt=False)
    return {"li": li, "curves": curves, "fixed": fixed, "bgs": bgs, "lb": lb, "tvi": np.log10(tvi),
            "tvi_fixed": np.log10(np.where(np.isfinite(tvi_fixed), tvi_fixed, np.nan)),
            "weber": float(tvi[-1] / b[-1]), "fixed_dies": float(lb[np.isfinite(tvi_fixed)].max())}


# ------------------------------------------------------------------------------------------------- the rate code
def compute_rate() -> dict:
    """Schematic, after Adrian and Zotterman (1926): impulses of one size, a rate that grows with the load and
    falls while the load stays on.  Trains drawn as Poisson spikes from that rate; illustrative numbers."""
    loads = np.array([0.0, 0.5, 1.0, 2.0, 4.0, 8.0])
    rate = N.adrian(loads + 1e-9, gain=30.0, threshold=0.25)
    t = np.linspace(0, 10, 500)
    tau = 3.0
    adapt = {}
    for L in (1.0, 4.0):
        r0 = float(N.adrian(np.array([L]), gain=30.0, threshold=0.25)[0])
        adapt[str(L)] = r0 * (0.35 + 0.65 * np.exp(-t / tau))
    g = rng(1313)
    trains = {}
    for L in (0.5, 2.0, 8.0):
        r = float(N.adrian(np.array([L]), gain=30.0, threshold=0.25)[0])
        trains[str(L)] = N.poisson_train(r, 1.0, g, refractory=0.004)
    return {"loads": loads, "rate": rate, "t": t, "adapt": adapt, "trains": trains}


# ------------------------------------------------------------------------------------------------- the retina
def _one_over_f(n: int, seed: int) -> np.ndarray:
    g = rng(seed)
    fy = np.fft.fftfreq(n)[:, None]
    fx = np.fft.fftfreq(n)[None, :]
    f = np.sqrt(fx ** 2 + fy ** 2)
    f[0, 0] = 1.0
    spec = (g.normal(size=(n, n)) + 1j * g.normal(size=(n, n))) / f
    spec[0, 0] = 0
    img = np.real(np.fft.ifft2(spec))
    return (img - img.mean()) / img.std()


def _radial(img) -> tuple:
    n = img.shape[0]
    p = np.abs(np.fft.fft2(img)) ** 2
    fy = np.fft.fftfreq(n)[:, None]
    fx = np.fft.fftfreq(n)[None, :]
    f = np.sqrt(fx ** 2 + fy ** 2)
    edges = np.geomspace(2 / n, 0.5, 14)
    mids, power = [], []
    for a, b in zip(edges[:-1], edges[1:]):
        m = (f >= a) & (f < b)
        mids.append(math.sqrt(a * b))
        power.append(float(p[m].mean()))
    return np.array(mids), np.array(power)


def compute_retina() -> dict:
    x = np.linspace(-12, 12, 241)
    prof = V.dog_profile(x, 1.5, 4.5, 1.0)
    f = np.geomspace(0.005, 0.5, 200)
    resp = V.dog_response(f, 1.5, 4.5, 1.0)
    centre_only = V.dog_response(f, 1.5, 4.5, 0.0)
    m_in = V.mach_profile()
    m_out = V.mach_response(m_in, 3.0, 9.0, 0.9)
    img = _one_over_f(128, 1301)
    out = V.dog_image(img, 0.5, 2.0, 1.0)
    out = (out - out.mean()) / out.std()
    fi, pi = _radial(img)
    fo, po = _radial(out)
    slope_in = float(np.polyfit(np.log10(fi), np.log10(pi), 1)[0])
    slope_out = float(np.polyfit(np.log10(fo[:8]), np.log10(po[:8]), 1)[0])  # where the signal is strong
    # correlation between pixels two apart, before and after
    cin = float(np.corrcoef(img[:, :-2].ravel(), img[:, 2:].ravel())[0, 1])
    cout = float(np.corrcoef(out[:, :-2].ravel(), out[:, 2:].ravel())[0, 1])
    return {"x": x, "prof": prof, "f": f, "resp": resp, "centre_only": centre_only, "m_in": m_in, "m_out": m_out,
            "img": img, "out": out, "fi": fi, "pi": pi, "fo": fo, "po": po, "slope_in": slope_in,
            "slope_out": slope_out, "corr_in": cin, "corr_out": cout}


# ------------------------------------------------------------------------------------------------- cortex
def compute_cortex() -> dict:
    size, wl = 64, 12.0
    rf_even = V.gabor(size, wl, 0.0, 0.0)
    rf_odd = V.gabor(size, wl, 0.0, np.pi / 2)
    th = np.deg2rad(np.arange(-90, 91, 3))
    tune = V.orientation_tuning(th, size, wl)
    tune = tune / tune.max()
    ph = np.linspace(0, 2 * np.pi, 73)
    simple = np.array([V.simple_cell(V.grating(size, wl, 0, p), rf_even) for p in ph])
    cplx = np.array([V.complex_cell(V.grating(size, wl, 0, p), size, wl) for p in ph])
    # a simulated 1959-style recording: a bar swept at 12 orientations, 10 sweeps each, Poisson spikes
    g = rng(1359)
    bar_th = np.deg2rad(np.arange(0, 180, 15))
    peak_rate = 40.0
    mean = peak_rate * np.interp(np.abs(((bar_th + np.pi / 2) % np.pi) - np.pi / 2), np.abs(th[th >= 0]), tune[th >= 0]) + 2
    counts = g.poisson(np.repeat(mean[:, None], 10, axis=1))
    return {"rf_even": rf_even, "rf_odd": rf_odd, "th": np.rad2deg(th), "tune": tune,
            "hw": float(np.rad2deg(V.half_width(th, tune))), "phase": np.rad2deg(ph), "simple": simple / cplx.max(),
            "complex": cplx / cplx.max(), "bar_th": np.rad2deg(bar_th), "bar_mean": counts.mean(axis=1),
            "bar_counts": counts}


# ------------------------------------------------------------------------------------------------- the CSF
CSF_TRUE = {"gain": 200.0, "peak": 4.0, "bandwidth": 2.75, "truncation": 0.5}


def compute_csf() -> dict:
    f = np.geomspace(0.25, 64, 300)
    s = V.csf(f, **CSF_TRUE)
    # a simulated observer's thresholds at 8 frequencies, with 0.08 log-unit noise; 101 observers, the median by rms
    fq = np.array([0.5, 1, 2, 4, 8, 16, 24, 32])
    fits = []
    for k in range(101):
        y = V.csf(fq, **CSF_TRUE) * 10 ** rng(1400 + k).normal(0, 0.08, len(fq))
        fits.append((V.fit_csf(fq, y), y))
    i = _median_pick([ft[0]["rms"] for ft in fits])
    fit, y = fits[i]
    chart = V.campbell_robson(640, 320, 0.25, 32.0, 0.003, 1.0, pixels_per_degree=128.0)
    return {"f": f, "s": s, "fq": fq, "y": y, "fit": fit,
            "fit_curve": V.csf(f, fit["gain"], fit["peak"], fit["bandwidth"], fit["truncation"]),
            "acuity": V.acuity_cpd(CSF_TRUE["gain"], CSF_TRUE["peak"], CSF_TRUE["bandwidth"]), "chart": chart,
            "peak_contrast": 1.0 / CSF_TRUE["gain"]}


def _letter(ch: str, n: int) -> np.ndarray:
    from matplotlib import font_manager
    from PIL import Image, ImageDraw, ImageFont

    path = font_manager.findfont(font_manager.FontProperties(family="DejaVu Sans", weight="bold"))
    im = Image.new("L", (n, n), 0)
    d = ImageDraw.Draw(im)
    font = ImageFont.truetype(path, int(n * 0.8))
    box = d.textbbox((0, 0), ch, font=font)
    d.text(((n - (box[2] - box[0])) / 2 - box[0], (n - (box[3] - box[1])) / 2 - box[1]), ch, fill=255, font=font)
    return np.asarray(im, float) / 255.0


def _lowpass(img, cutoff: float) -> np.ndarray:
    fy = np.fft.fftfreq(img.shape[0])[:, None]
    fx = np.fft.fftfreq(img.shape[1])[None, :]
    h = np.exp(-(fx ** 2 + fy ** 2) / (2 * cutoff ** 2))
    return np.real(np.fft.ifft2(np.fft.fft2(img) * h))


def compute_hybrid() -> dict:
    """An 'A' kept only at low spatial frequencies plus an 'E' kept only at high ones.  Up close the CSF passes the
    fine 'E'; far away the image shrinks on the retina, its fine detail passes the acuity limit, and the 'A' is all
    that is left."""
    n = 192
    a, e = _letter("A", n), _letter("E", n)
    low = _lowpass(a, 0.012)
    high = e - _lowpass(e, 0.05)
    hyb = 0.5 + 0.55 * (low - low.mean()) + 0.9 * high
    hyb = np.clip(hyb, 0, 1)
    # the image spans 2 degrees up close and 0.25 degrees far away
    near = V.csf_filter(hyb, n / 2.0, **CSF_TRUE)
    far = V.csf_filter(hyb, n / 0.25, **CSF_TRUE)
    return {"hybrid": hyb, "low": 0.5 + 0.55 * (low - low.mean()), "high": 0.5 + 0.9 * high, "near": near, "far": far}


# ------------------------------------------------------------------------------------------------- channels
def compute_channels() -> dict:
    """A bank of log-Gaussian channels one octave wide at half height; the CSF is their envelope.  Adapting to an
    8 c/deg grating divides the gain of each channel by 1 + 4 x its response to the adapter: threshold rises up to
    fivefold at 8 c/deg and little an octave and a half away."""
    f = np.geomspace(0.5, 40, 300)
    centres = 2.0 ** np.arange(-1, 5.6, 1 / 3)  # a third of an octave apart
    width = 1.0 / (2 * math.sqrt(2 * math.log(2)))  # octaves: one octave full width at half height

    def tuning(c):
        return np.exp(-0.5 * (np.log2(f / c) / width) ** 2)

    env = V.csf(f, **CSF_TRUE)
    gains = V.csf(centres, **CSF_TRUE)
    bank = np.array([g * tuning(c) for g, c in zip(gains, centres)])
    before = bank.max(axis=0)
    adapter = 8.0
    resp = np.exp(-0.5 * (np.log2(adapter / centres) / width) ** 2)
    after_g = gains / (1 + 4 * resp)
    bank_after = np.array([g * tuning(c) for g, c in zip(after_g, centres)])
    after = bank_after.max(axis=0)
    c = np.geomspace(0.01, 1, 200)
    return {"f": f, "env": env, "bank": bank, "before": before, "after": after, "centres": centres,
            "adapter": adapter, "elevation": before / after, "max_elevation": float((before / after).max()),
            "c": c, "crf": V.contrast_response(c, 0.15, 2.0), "crf_mask": V.contrast_response(c, 0.15, 2.0, mask=0.3),
            "norm_a": V.normalize([1.0, 0.5, 0.25, 0.1], 0.05), "norm_b": V.normalize([4.0, 2.0, 1.0, 0.4], 0.05)}


# ------------------------------------------------------------------------------------------------- colour
_LMS_TO_XYZ = np.linalg.lstsq(V.LMS, V.XYZ, rcond=None)[0]  # 3 x 3, least squares over the grid


def lms_to_srgb(lms, scale: float) -> np.ndarray:
    return V.srgb(np.asarray(lms, float) @ _LMS_TO_XYZ, scale)


def compute_cones() -> dict:
    daylight = V.planck(6500)
    leaf = V.surface(550, 45, 0.05, 0.5)
    light = daylight * leaf
    return {"wl": V.WAVELENGTHS, "lms": V.LMS, "rod": V.SCOTOPIC, "daylight": daylight, "leaf": leaf, "light": light,
            "light_lms": V.cone_excitations(light), "peaks": V.WAVELENGTHS[np.argmax(V.LMS, axis=0)],
            "rod_peak": float(V.WAVELENGTHS[np.argmax(V.SCOTOPIC)]), "n_samples": len(V.WAVELENGTHS)}


def compute_matching() -> dict:
    prim = V.SB_PRIMARIES
    cm = V.matching_functions(prim)
    idx = [int(np.where(V.WAVELENGTHS == w)[0][0]) for w in V.SB_WAVELENGTHS]
    mine = cm[idx]
    # put the derived functions on the 1955 data's scale: one least-squares factor per primary
    scale = np.array([float(np.dot(mine[:, j], V.SB_RGB[:, j]) / np.dot(mine[:, j], mine[:, j])) for j in range(3)])
    derived = mine * scale
    r = [float(np.corrcoef(derived[:, j], V.SB_RGB[:, j])[0, 1]) for j in range(3)]
    w500 = V.match(V.monochromatic(500), prim) * scale
    w580 = V.match(V.monochromatic(580), prim) * scale
    # a metamer pair: a broad 'surface under daylight' spectrum and a null-space twin
    base = V.surface(560, 70, 0.25, 0.55)
    twin = V.null_space_metamer(base, 0.9, seed=7)
    scale = 1.2 * float(np.max(V.to_xyz(base) @ V._XYZ_TO_SRGB.T))
    rgb_base, rgb_twin = V.srgb(V.to_xyz(base), scale), V.srgb(V.to_xyz(twin), scale)
    # the same pair under a warm light: the match breaks
    A = V.planck(2856)
    la, lb = V.cone_excitations(base * A), V.cone_excitations(twin * A)
    locus = V.spectral_locus(400, 700)
    srgb_xy = np.array([[0.64, 0.33], [0.30, 0.60], [0.15, 0.06]])
    return {"sb_wl": V.SB_WAVELENGTHS, "sb": V.SB_RGB, "derived": derived, "r": r, "prim": prim, "w500": w500,
            "w580": w580, "wl": V.WAVELENGTHS, "base": base, "twin": twin, "rgb_base": rgb_base, "rgb_twin": rgb_twin,
            "lms_base": V.cone_excitations(base), "lms_twin": V.cone_excitations(twin),
            "under_a": (la / lb), "locus": locus, "locus_nm": V.WAVELENGTHS[(V.WAVELENGTHS >= 400) & (V.WAVELENGTHS <= 700)],
            "srgb_xy": srgb_xy, "white": V.chromaticity(V.to_xyz(np.ones(len(V.WAVELENGTHS)))),
            "max_diff": float(np.max(np.abs(derived - V.SB_RGB)) / np.max(np.abs(V.SB_RGB)))}


def _hex_rgb(h: str) -> np.ndarray:
    h = h.lstrip("#")
    return np.array([int(h[i:i + 2], 16) for i in (0, 2, 4)]) / 255.0


def _srgb_to_lms(rgb) -> np.ndarray:
    c = np.asarray(rgb, float)
    lin = np.where(c <= 0.04045, c / 12.92, ((c + 0.055) / 1.055) ** 2.4)
    m = np.linalg.inv(np.array([[3.2406, -1.5372, -0.4986], [-0.9689, 1.8758, 0.0415], [0.0557, -0.2040, 1.0570]]))
    xyz = lin @ m.T
    return xyz @ np.linalg.inv(_LMS_TO_XYZ)


def _lms_to_srgb_abs(lms) -> np.ndarray:
    xyz = np.asarray(lms, float) @ _LMS_TO_XYZ
    lin = np.clip(xyz @ np.array([[3.2406, -1.5372, -0.4986], [-0.9689, 1.8758, 0.0415], [0.0557, -0.2040, 1.0570]]).T, 0, 1)
    return np.where(lin <= 0.0031308, 12.92 * lin, 1.055 * lin ** (1 / 2.4) - 0.055)


def _lab(rgb) -> np.ndarray:
    """sRGB to CIELAB (D65), for colour differences."""
    c = np.asarray(rgb, float)
    lin = np.where(c <= 0.04045, c / 12.92, ((c + 0.055) / 1.055) ** 2.4)
    m = np.linalg.inv(np.array([[3.2406, -1.5372, -0.4986], [-0.9689, 1.8758, 0.0415], [0.0557, -0.2040, 1.0570]]))
    xyz = (lin @ m.T) / np.array([0.95047, 1.0, 1.08883])
    f = np.where(xyz > (6 / 29) ** 3, np.cbrt(xyz), xyz / (3 * (6 / 29) ** 2) + 4 / 29)
    return np.array([116 * f[1] - 16, 500 * (f[0] - f[1]), 200 * (f[1] - f[2])])


def _closest(rgbs) -> tuple:
    """The smallest colour difference (CIE 1976 Delta E) between two members of a palette, and which pair."""
    lab = [_lab(c) for c in rgbs]
    best = (np.inf, 0, 0)
    for i in range(len(lab)):
        for j in range(i + 1, len(lab)):
            d = float(np.linalg.norm(lab[i] - lab[j]))
            if d < best[0]:
                best = (d, i, j)
    return best


def compute_opponent() -> dict:
    lms = V.LMS / V.LMS.max(axis=0)
    wl = V.WAVELENGTHS
    # red-green weighted L - 1.5 M, silent near 580 nm; blue-yellow S - (L + M)/2; luminance L + M
    opp = np.column_stack([lms[:, 0] + lms[:, 1], lms[:, 0] - 1.5 * lms[:, 1], lms[:, 2] - (lms[:, 0] + lms[:, 1]) / 2])
    lm = opp[:, 1]
    band = (wl > 540) & (wl < 640)
    zero_lm = float(np.interp(0, lm[band], wl[band]))
    rainbow = ["#E41A1C", "#FF7F00", "#4DAF4A", "#377EB8", "#984EA3", "#A65628"]
    okabe = list(archive.OKABE_ITO.data["hex"][:6])
    sims = {}
    for name, pal in (("rainbow", rainbow), ("okabe", okabe)):
        rgb = [_hex_rgb(h) for h in pal]
        for kind in ("none", "L", "M"):
            if kind == "none":
                sims[f"{name}_{kind}"] = rgb
            else:
                sims[f"{name}_{kind}"] = [np.clip(_lms_to_srgb_abs(V.dichromat(_srgb_to_lms(c), kind)), 0, 1) for c in rgb]
    dist = {k: _closest(v) for k, v in sims.items()}
    return {"wl": wl, "opp": opp, "zero_lm": zero_lm, "sims": {k: np.array(v) for k, v in sims.items()},
            "dist": dist, "rainbow": rainbow, "okabe": okabe}


def compute_dress() -> dict:
    """A stand-in swatch with colours like the photograph's (a pale blue and a dark gold-brown), read under two
    assumed lights by von Kries scaling.  Not the photograph."""
    stripes = {"pale": np.array([0.53, 0.57, 0.78]), "dark": np.array([0.45, 0.37, 0.22])}
    warm = V.cone_excitations(V.planck(3000))
    cool = V.cone_excitations(V.planck(12000))
    ref = V.cone_excitations(V.planck(6500))
    out = {}
    for name, c in stripes.items():
        lms = _srgb_to_lms(c)
        out[name] = c
        out[f"{name}_warm"] = np.clip(_lms_to_srgb_abs(V.von_kries(lms, warm / warm.sum(), ref / ref.sum())), 0, 1)
        out[f"{name}_cool"] = np.clip(_lms_to_srgb_abs(V.von_kries(lms, cool / cool.sum(), ref / ref.sum())), 0, 1)
    s = archive.LAFER_SOUSA_2015.data
    out["survey"] = (s["blue_black"], s["white_gold"], s["blue_brown"], s["other"])
    out["n"] = s["n"]
    return out


def compute_streams() -> dict:
    """Schematic of the slot task (after Milner et al. 1991): a disc's slot at random orientations; D.F. matches the
    orientation with a card held still (errors nearly uniform) or posts the card into it (errors small).  Simulated
    trials, not her data."""
    g = rng(1391)
    slot = g.uniform(0, 180, 40)
    match_err = g.uniform(-90, 90, 40)
    post_err = g.normal(0, 9, 40)
    return {"slot": slot, "matched": (slot + match_err) % 180, "posted": (slot + post_err) % 180,
            "sd_match": float(np.std(match_err)), "sd_post": float(np.std(post_err))}


def compute_practice() -> dict:
    """A synthetic scene (coloured discs on a gradient); its luminance or its colour kept at a quarter of the
    resolution.  The colour loss is hard to see; the luminance loss is not."""
    n = 160
    y, x = np.mgrid[:n, :n] / n
    img = np.stack([0.3 + 0.5 * x, 0.35 + 0.3 * y, 0.6 - 0.3 * x], axis=-1)
    g = rng(1366)
    for _ in range(9):
        cx, cy, r = g.uniform(0.15, 0.85, 2).tolist() + [float(g.uniform(0.06, 0.13))]
        m = (x - cx) ** 2 + (y - cy) ** 2 < r * r
        img[m] = g.uniform(0.05, 0.95, 3)
    for k in range(6):  # thin dark lines: fine luminance detail
        img[:, 20 + 25 * k:21 + 25 * k] *= 0.25
    M = np.array([[0.299, 0.587, 0.114], [-0.168736, -0.331264, 0.5], [0.5, -0.418688, -0.081312]])
    ycc = img @ M.T

    def coarse(ch, f=4):
        small = ch.reshape(n // f, f, n // f, f).mean(axis=(1, 3))
        return np.repeat(np.repeat(small, f, axis=0), f, axis=1)

    chroma = ycc.copy()
    chroma[..., 1] = coarse(ycc[..., 1])
    chroma[..., 2] = coarse(ycc[..., 2])
    luma = ycc.copy()
    luma[..., 0] = coarse(ycc[..., 0])
    Mi = np.linalg.inv(M)
    return {"original": img, "chroma_cut": np.clip(chroma @ Mi.T, 0, 1), "luma_cut": np.clip(luma @ Mi.T, 0, 1),
            "bits_full": 3 * n * n, "bits_420": n * n + 2 * (n // 2) ** 2}


_RAW = {
    "quanta": compute_quanta,
    "optics": compute_optics,
    "adapt": compute_adapt,
    "rate": compute_rate,
    "retina": compute_retina,
    "cortex": compute_cortex,
    "csf": compute_csf,
    "hybrid": compute_hybrid,
    "channels": compute_channels,
    "cones": compute_cones,
    "matching": compute_matching,
    "opponent": compute_opponent,
    "dress": compute_dress,
    "streams": compute_streams,
    "practice": compute_practice,
}
ITEMS = {name: (lambda f=f: _cacheable(f())) for name, f in _RAW.items()}

if __name__ == "__main__":
    CACHE.main(ITEMS, __doc__)
