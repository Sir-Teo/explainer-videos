"""Psyche attends: selection, search, time, control and gain (Part 18 of *Psychology, Built*).

Filters: Broadbent's all-or-none filter against Treisman's attenuator, as the probability that a word in the
unattended ear is heard, with low thresholds for one's own name; Lavie's load as spare capacity that spills onto a
flanker.  Space: Posner's cue as a gain that grows after the cue, with an exogenous cue's facilitation turning into
inhibition of return.  Search: displays of coloured, oriented items; a bottom-up saliency (feature contrast) and a
centre-surround saliency map on images with a winner-take-all scan path; Wolfe's guided search, in which items are
checked in order of a noisy priority (top-down match plus saliency) and the search quits when no item above a
threshold is left, which gives flat feature slopes, shallow conjunction slopes and steep, two-to-one slopes for an
unguided search; and the prevalence effect as a criterion that drifts with the base rate.  Change blindness: a
flicker display in which attention samples a few items per alternation, weighted by interest.  Time: the
attentional blink as a two-stage model (a busy consolidation stage, a decaying buffer, sparing at lag 1) and the
psychological refractory period as a central bottleneck between gamma stages.  Control: the Stroop task as a
diffusion whose drift adds a weak, attended colour pathway to a strong word pathway, with conflict monitoring
raising control on the next trial; task switching with a reconfiguration that preparation shortens.  Neurons:
Reynolds and Heeger's normalization model of attention, in which an attention field multiplies the stimulus drive
before divisive normalization, so that the relative sizes of stimulus and attention field decide between contrast
gain and response gain.  Capacity: Bundesen's theory of visual attention as a race of exponential processes into a
short-term store of K slots.  Time on task: the vigilance decrement as a sensitivity that falls over a watch.

Parameters make the classic patterns legible; they are not fitted to a laboratory unless a function says so, and
Part 18's scenes say which numbers are published and which are Psyche's.
"""

from __future__ import annotations

from dataclasses import dataclass

import numpy as np
from scipy.ndimage import gaussian_filter
from scipy.stats import norm


# ============================================================================================== filters and load
def dichotic(attenuation: float = 0.4, noise: float = 0.25, thresholds=None, model: str = "attenuate") -> dict:
    """The probability that a word arriving in the unattended ear reaches awareness.

    A word's signal is 1 in the attended ear and ``attenuation`` in the other (0 under Broadbent's filter), plus
    Gaussian noise of s.d. ``noise``; it is heard if it exceeds the word's threshold.  Treisman's point is that
    thresholds differ: one's own name, or a word the context predicts, has a low one.  Returns
    {word: (P(heard | attended), P(heard | unattended))}."""
    thresholds = thresholds or {"own name": 0.55, "a word the sentence predicts": 0.7, "an ordinary word": 1.1}
    a = 0.0 if model == "filter" else attenuation
    out = {}
    for word, th in thresholds.items():
        att = float(norm.sf((th - 1.0) / noise))
        un = float(norm.sf((th - a) / noise)) if a > 0 else 0.0
        out[word] = (att, un)
    return out


def flanker_interference(load: np.ndarray, capacity: float = 4.0, full: float = 60.0) -> np.ndarray:
    """Lavie's load theory: perception takes in relevant items until capacity is full, then spills what is left onto
    irrelevant ones.  The flanker's interference (ms) is ``full`` times the share of capacity left over by ``load``
    relevant items."""
    load = np.asarray(load, float)
    return full * np.clip(capacity - load, 0.0, capacity) / capacity


# ============================================================================================== space: cueing
def cue_effect(soa: np.ndarray, kind: str = "endogenous", gain: float = 30.0, rise: float = 80.0,
               ior: float = 25.0, ior_onset: float = 250.0, ior_rise: float = 150.0, fade: float = 200.0) -> np.ndarray:
    """Invalid minus valid RT (ms) as a function of cue-target SOA.

    An endogenous, predictive cue (an arrow, 80% valid) moves attention and keeps it there: the effect grows as
    ``2 gain (1 − e^{−soa/rise})`` (a benefit and a cost of ``gain`` each).  An exogenous, non-predictive cue (a flash)
    captures attention at once and lets it go: facilitation ``2 gain e^{−soa/fade}(1 − e^{−soa/rise'})`` with a faster
    rise, minus an inhibition of return that grows after ``ior_onset``; at long SOAs the cued side is slower."""
    t = np.asarray(soa, float)
    if kind == "endogenous":
        return 2 * gain * (1 - np.exp(-t / rise))
    fac = 2 * gain * np.exp(-t / fade) * (1 - np.exp(-t / (rise / 2)))
    inh = np.where(t > ior_onset, ior * (1 - np.exp(-(t - ior_onset) / ior_rise)), 0.0)
    return fac - inh


def posner_rts(soa: float, kind: str = "endogenous", base: float = 300.0, gain: float = 30.0, sd: float = 40.0,
               n: int = 200, rng=None) -> dict:
    """Simulated RTs for valid, neutral and invalid trials at one SOA: valid = base − b, invalid = base + b, with
    ``b`` half of :func:`cue_effect`; Gaussian trial noise.  Returns {condition: RT array}."""
    rng = rng or np.random.default_rng(0)
    b = float(cue_effect(np.array([soa]), kind, gain)[0]) / 2
    return {c: base + s * b + rng.normal(0, sd, n) for c, s in (("valid", -1), ("neutral", 0), ("invalid", 1))}


# ============================================================================================== search
@dataclass
class Display:
    """A search display: per item a colour (0 green, 1 red), an orientation (0 vertical, 1 horizontal), a shape
    (0 an L, 1 a T) and a position in the unit square; ``target`` is the index of the target or −1."""

    colour: np.ndarray
    orient: np.ndarray
    shape: np.ndarray
    xy: np.ndarray
    target: int


def make_display(n: int, kind: str, present: bool, rng) -> Display:
    """``feature``: a red target among green items; ``conjunction``: a red vertical among red horizontals and green
    verticals; ``spatial``: a T among Ls, all one colour and orientation, so no feature tells them apart."""
    colour, orient, shape = np.zeros(n, int), np.zeros(n, int), np.zeros(n, int)
    if kind == "conjunction":
        half = rng.permutation(n) < n // 2
        colour[half], orient[half] = 1, 1  # red horizontals and green verticals
    t = int(rng.integers(n)) if present else -1
    if present:
        if kind == "feature":
            colour[t] = 1
        elif kind == "conjunction":
            colour[t], orient[t] = 1, 0
        elif kind == "spatial":
            shape[t] = 1
        else:
            raise ValueError(kind)
    side = int(np.ceil(np.sqrt(n * 2)))
    cells = rng.choice(side * side, n, replace=False)
    xy = np.c_[(cells % side + 0.5) / side, (cells // side + 0.5) / side] + rng.uniform(-0.15, 0.15, (n, 2)) / side
    return Display(colour, orient, shape, xy, t)


def item_saliency(d: Display) -> np.ndarray:
    """Bottom-up saliency of each item: summed over feature dimensions, how far its value is from the share of
    items carrying it (a unique colour scores near 1; a colour half the display shares scores 0.5)."""
    s = np.zeros(d.colour.size)
    for f in (d.colour, d.orient):
        share = np.mean(f[:, None] == f[None, :], axis=1)
        s += 1 - share
    return s


def _target_priority(d: Display, kind: str, w_bu: float) -> float:
    """The priority an item with the target's features would earn in this display, noise aside: its top-down match
    plus ``w_bu`` times the saliency it would have among the other items."""
    if kind == "spatial":
        return 0.0
    others = np.arange(d.colour.size) != d.target
    sal = 0.0
    feats = [(d.colour[others], 1)] + ([(d.orient[others], 0)] if kind == "conjunction" else [(d.orient[others], 0)])
    for f, v in feats:
        share = (np.sum(f == v) + 1) / (f.size + 1)
        sal += 1 - share
    return (1.0 if kind == "feature" else 2.0) + w_bu * sal


def guided_search(d: Display, kind: str, rng, per_item: float = 50.0, base: float = 450.0, noise: float = 1.0,
                  w_bu: float = 2.0, z: float = 1.5, item_sd: float = 15.0, quit: float = 70.0) -> tuple[float, bool]:
    """One trial of guided search (after Wolfe 1994, 2021).  Each item's priority is its top-down match to the
    target's features (one point per feature shared; only colour and orientation can guide) plus ``w_bu`` times its
    saliency plus Gaussian noise of s.d. ``noise``.  Items are checked one at a time in order of priority, each check
    taking a gamma time of mean ``per_item``; items whose priority falls below a quitting threshold are never
    checked.  The threshold sits ``z`` noise s.d.s below the priority a target earns, so a target is skipped (missed)
    on about Φ(−z) of trials.  The search ends when the target is checked ('present') or no item above threshold is
    left ('absent'), which takes a further ``quit`` ms to decide.  Returns (RT, correct)."""
    if kind == "spatial":
        top = np.zeros(d.colour.size)
        bu = np.zeros(d.colour.size)
    else:
        top = (d.colour == 1).astype(float) + ((d.orient == 0).astype(float) if kind == "conjunction" else 0.0)
        bu = item_saliency(d)
    pri = top + w_bu * bu + rng.normal(0, noise, d.colour.size)
    cut = _target_priority(d, kind, w_bu) - z * noise
    t = base
    k = 2.0  # gamma shape of each check
    for i in np.argsort(-pri):
        if pri[i] < cut:
            break
        t += rng.gamma(k, per_item / k)
        if i == d.target:
            return t + rng.normal(0, item_sd), True
    return t + quit + rng.normal(0, item_sd), d.target < 0


def search_slopes(kind: str, set_sizes=(4, 8, 16, 32), n: int = 200, rng=None, **kw) -> dict:
    """Mean correct RT and error rate for target-present and target-absent trials at each set size, and the
    least-squares slopes (ms per item).  Returns {"present": (rt, err), "absent": (rt, err), "slopes": (p, a)}."""
    rng = rng or np.random.default_rng(0)
    out = {}
    for present in (True, False):
        rts, errs = [], []
        for ss in set_sizes:
            res = [guided_search(make_display(ss, kind, present, rng), kind, rng, **kw) for _ in range(n)]
            r = np.array([x[0] for x in res])
            c = np.array([x[1] for x in res])
            rts.append(r[c].mean() if c.any() else np.nan)
            errs.append(1 - c.mean())
        out["present" if present else "absent"] = (np.array(rts), np.array(errs))
    ss = np.asarray(set_sizes, float)
    out["slopes"] = tuple(float(np.polyfit(ss, out[k][0], 1)[0]) for k in ("present", "absent"))
    return out


def saliency_map(features: dict, centre: float = 2.0, surround: float = 8.0) -> np.ndarray:
    """A saliency map in the manner of Itti and Koch (1998): for each feature map, the rectified difference between a
    narrow and a wide Gaussian blur (centre minus surround), normalized to a maximum of 1 and weighted up when it has
    one strong peak rather than many (its maximum minus its mean, squared); then summed."""
    total = None
    for f in features.values():
        cs = np.abs(gaussian_filter(f, centre) - gaussian_filter(f, surround))
        m = cs.max()
        if m > 0:
            cs = cs / m
            cs = cs * (1 - cs.mean()) ** 2
        total = cs if total is None else total + cs
    return total / total.max()


def scan_path(sal: np.ndarray, k: int = 5, ior_radius: float = 6.0) -> list[tuple[int, int]]:
    """Winner-take-all with inhibition of return: visit the most salient location, suppress a disc around it,
    repeat ``k`` times."""
    s = sal.copy()
    yy, xx = np.mgrid[: s.shape[0], : s.shape[1]]
    path = []
    for _ in range(k):
        i, j = np.unravel_index(np.argmax(s), s.shape)
        path.append((int(i), int(j)))
        s[(yy - i) ** 2 + (xx - j) ** 2 <= ior_radius ** 2] = 0.0
    return path


def prevalence_misses(prevalence: np.ndarray, d_prime: float = 2.95, shift: float = 0.5) -> np.ndarray:
    """The prevalence effect as signal detection: an observer who moves the criterion ``shift`` of the way to the
    accuracy-maximizing one, c = d'/2 + shift · ln((1 − p)/p)/d', misses Φ(c − d') of targets.  d' = 2.95 gives 7%
    misses at 50% prevalence."""
    p = np.asarray(prevalence, float)
    c = d_prime / 2 + shift * np.log((1 - p) / p) / d_prime
    return norm.cdf(c - d_prime)


def flicker(weights: np.ndarray, changed: int, per_alternation: float = 1.0, transient: bool = False,
            rng=None, max_alt: int = 200) -> int:
    """Change detection in Rensink's flicker paradigm.  With blanks between the images the change's own transient is
    masked, so attention must find it: on each alternation it samples ``per_alternation`` items (on average),
    without replacement, with probability proportional to ``weights`` (interest).  The change is seen when its item
    is sampled.  Without blanks (``transient``) the change captures attention on the first alternation.  Returns the
    number of alternations needed."""
    if transient:
        return 1
    rng = rng or np.random.default_rng(0)
    w = np.asarray(weights, float).copy()
    alt = 0
    while alt < max_alt:
        alt += 1
        k = rng.poisson(per_alternation)
        for _ in range(k):
            if w.sum() <= 0:
                w = np.asarray(weights, float).copy()
            i = rng.choice(w.size, p=w / w.sum())
            if i == changed:
                return alt
            w[i] = 0.0
    return max_alt


# ============================================================================================== time
def attentional_blink(lags, soa: float = 100.0, consolidate: float = 300.0, cv: float = 0.4, decay: float = 100.0,
                      spare: float = 0.85, n: int = 4000, rng=None) -> np.ndarray:
    """P(report T2 | T1 reported) at each lag, in a two-stage model (after Chun and Potter 1995).  T1 occupies a
    consolidation stage for a gamma time (mean ``consolidate``, CV ``cv``).  T2, arriving lag × soa later, waits in a
    fragile buffer that the next item masks; it survives a wait w with probability e^{−w/decay}.  At lag 1, T2 often
    enters consolidation together with T1 (probability ``spare``): lag-1 sparing."""
    rng = rng or np.random.default_rng(0)
    k = 1 / cv ** 2
    busy = rng.gamma(k, consolidate / k, n)
    out = []
    for lag in np.atleast_1d(lags):
        arrive = lag * soa
        wait = np.clip(busy - arrive, 0, None)
        p = np.exp(-wait / decay)
        if lag == 1:
            p = spare + (1 - spare) * p
        out.append(float(np.mean(rng.random(n) < p)))
    return np.array(out)


def prp(soas, a=(100.0, 100.0), b=(150.0, 150.0), c=(80.0, 80.0), cv: float = 0.2, n: int = 4000, rng=None) -> dict:
    """The psychological refractory period under a central bottleneck (Pashler 1994).  Each task has a perceptual
    stage A, a central stage B and a motor stage C (gamma, CV ``cv``).  Task 2's central stage cannot start until
    task 1's has finished: RT2 = max(SOA + A2, A1 + B1) + B2 + C2 − SOA.  Returns mean RT1 and RT2 per SOA; at short
    SOAs RT2 falls with slope −1, at long ones it is flat."""
    rng = rng or np.random.default_rng(0)
    k = 1 / cv ** 2

    def g(m):
        return rng.gamma(k, m / k, n)

    A1, B1, C1, A2, B2, C2 = g(a[0]), g(b[0]), g(c[0]), g(a[1]), g(b[1]), g(c[1])
    rt1 = float(np.mean(A1 + B1 + C1))
    rt2 = [float(np.mean(np.maximum(s + A2, A1 + B1) + B2 + C2 - s)) for s in np.atleast_1d(soas)]
    return {"rt1": rt1, "rt2": np.array(rt2)}


# ============================================================================================== control
def diffusion_rt(drift, bound: float = 1.5, noise: float = 1.0, ter: float = 300.0, dt: float = 1.0, scale: float = 400.0,
                 rng=None, max_t: float = 3000.0) -> tuple[np.ndarray, np.ndarray]:
    """First passage of a Wiener process from 0 to ±``bound`` with the given drifts (one trial each), time in ms
    (``scale`` ms per unit of model time); RT = passage time + ``ter``.  Returns (RT, correct)."""
    rng = rng or np.random.default_rng(0)
    drift = np.asarray(drift, float)
    n = drift.size
    x = np.zeros(n)
    t = np.zeros(n)
    done = np.zeros(n, bool)
    up = np.zeros(n, bool)
    h = dt / scale
    steps = int(max_t / dt)
    for _ in range(steps):
        live = ~done
        if not live.any():
            break
        x[live] += drift[live] * h + noise * np.sqrt(h) * rng.standard_normal(live.sum())
        t[live] += dt
        hit = live & (np.abs(x) >= bound)
        up[hit] = x[hit] > 0
        done |= hit
    up[~done] = x[~done] > 0
    return t + ter, up


def stroop(condition: str, task: str = "colour", n: int = 2000, colour: float = 2.5, word: float = 3.0,
           control: float = 0.6, rng=None) -> tuple[np.ndarray, np.ndarray]:
    """The Stroop task as a diffusion (in the spirit of Cohen, Dunbar and McClelland 1990).  The drift toward the
    correct response is the attended pathway's strength plus or minus the other pathway's.  Naming the ink, the
    colour pathway (``colour``) is attended; the word pathway is stronger (``word``) but damped by control to
    ``(1 − control) word``, and it pushes toward the correct response (congruent), the wrong one (incongruent) or
    neither (neutral, XXXX).  Reading the word, the word pathway is attended and the weak ink pathway, also damped,
    barely matters: the asymmetry.  Returns (RT, correct)."""
    rng = rng or np.random.default_rng(0)
    sign = {"congruent": 1.0, "neutral": 0.0, "incongruent": -1.0}[condition]
    if task == "colour":
        v = colour + sign * (1 - control) * word
    else:
        v = word + sign * (1 - control) * colour * 0.25
    return diffusion_rt(np.full(n, v), rng=rng)


def stroop_sequence(conditions, colour: float = 2.5, word: float = 3.0, control0: float = 0.5, boost: float = 0.25,
                    decay: float = 0.5, rng=None) -> tuple[np.ndarray, np.ndarray, np.ndarray]:
    """Conflict monitoring (Botvinick et al. 2001) on a sequence of Stroop trials.  Conflict on a trial is the
    co-activation of the two responses (1 on incongruent trials, 0 otherwise, here); control on the next trial is
    ``control0 + boost · conflict``, relaxing back by ``decay``.  After an incongruent trial the word is damped more,
    so interference shrinks: the congruency sequence (Gratton) effect.  Returns (RT, correct, control used)."""
    rng = rng or np.random.default_rng(0)
    rts, ok, ctl = [], [], []
    c = control0
    for cond in conditions:
        r, k = stroop(cond, "colour", n=1, colour=colour, word=word, control=min(c, 0.95), rng=rng)
        rts.append(r[0])
        ok.append(k[0])
        ctl.append(c)
        conflict = 1.0 if cond == "incongruent" else 0.0
        c = control0 + (c - control0) * decay + boost * conflict
    return np.array(rts), np.array(ok), np.array(ctl)


def delta_plot(rt_a: np.ndarray, rt_b: np.ndarray, qs=(0.1, 0.3, 0.5, 0.7, 0.9)) -> tuple[np.ndarray, np.ndarray]:
    """The delta plot: at each quantile, the mean of the two conditions' quantiles (x) and their difference (y)."""
    qa, qb = np.quantile(rt_a, qs), np.quantile(rt_b, qs)
    return (qa + qb) / 2, qb - qa


def switch_cost(rsi: np.ndarray, full: float = 200.0, residual: float = 80.0, tau: float = 250.0) -> np.ndarray:
    """Task-switching cost (ms) against the response-stimulus interval: a reconfiguration that preparation completes
    with time constant ``tau``, and a residual it cannot remove (Rogers and Monsell 1995's pattern)."""
    rsi = np.asarray(rsi, float)
    return residual + (full - residual) * np.exp(-rsi / tau)


# ============================================================================================== neurons: normalization
def normalization_crf(contrasts, stim_width: float, af_width: float, attend: bool, af_gain: float = 2.0,
                      sigma: float = 0.1, pool_width: float = 4.0, n: float = 2.0, x_grid=None) -> np.ndarray:
    """Reynolds and Heeger's (2009) normalization model of attention on one spatial dimension, for a neuron centred
    on the stimulus.  The stimulus drive is E(x) = c^n inside a stimulus of width ``stim_width`` (a smooth window);
    the attention field A(x) is 1 + (af_gain − 1) times a Gaussian of s.d. ``af_width`` at the stimulus when
    attending (1 everywhere otherwise); the suppressive drive S is A·E pooled by a Gaussian of s.d. ``pool_width``;
    and the response is R = A E / (S + σ^n), read at the centre.  Returns R for each contrast."""
    x = np.linspace(-20, 20, 801) if x_grid is None else x_grid
    dx = x[1] - x[0]
    win = 1 / (1 + np.exp((np.abs(x) - stim_width / 2) / 0.3))
    A = 1 + (af_gain - 1) * np.exp(-0.5 * (x / af_width) ** 2) if attend else np.ones_like(x)
    kern = np.exp(-0.5 * (x / pool_width) ** 2)
    kern /= kern.sum() * dx
    out = []
    centre = x.size // 2
    for c in np.atleast_1d(contrasts):
        E = c ** n * win
        drive = A * E
        S = np.convolve(drive, kern, mode="same") * dx
        out.append(drive[centre] / (S[centre] + sigma ** n))
    return np.array(out)


def gain_type(contrasts, unattended, attended) -> dict:
    """Fit each curve with R = Rmax c^n/(c^n + c50^n) on log contrast (least squares on a grid) and report the
    ratios of the attended to the unattended Rmax and c50: contrast gain lowers c50, response gain raises Rmax."""
    from scipy.optimize import curve_fit

    c = np.asarray(contrasts, float)

    def f(cc, rmax, c50, nn):
        return rmax * cc ** nn / (cc ** nn + c50 ** nn)

    fits = []
    for r in (unattended, attended):
        p, _ = curve_fit(f, c, r, p0=(r.max() * 1.2, 0.1, 2.0), bounds=([0, 1e-4, 0.5], [np.inf, 10, 6]), maxfev=20000)
        fits.append(p)
    return {"rmax_ratio": float(fits[1][0] / fits[0][0]), "c50_ratio": float(fits[1][1] / fits[0][1]),
            "unattended": fits[0], "attended": fits[1]}


# ============================================================================================== capacity: TVA
def tva_whole_report(exposures, n_items: int = 6, C: float = 30.0, t0: float = 20.0, K: int = 4, n: int = 4000,
                     rng=None) -> np.ndarray:
    """Whole report under Bundesen's (1990) theory of visual attention: each of ``n_items`` equally weighted items is
    encoded at rate v = C/n_items items a second once the effective exposure passes t0 (ms); encoding times are
    exponential; the first K to finish within the exposure enter visual short-term memory.  Returns the mean number
    reported at each exposure (ms)."""
    rng = rng or np.random.default_rng(0)
    v = C / n_items / 1000.0
    times = rng.exponential(1 / v, (n, n_items))
    out = []
    for e in np.atleast_1d(exposures):
        done = (times <= max(e - t0, 0)).sum(axis=1)
        out.append(float(np.minimum(done, K).mean()))
    return np.array(out)


# ============================================================================================== vigilance
def vigilance(minutes: np.ndarray, d0: float = 2.6, drop: float = 0.9, tau: float = 25.0, criterion: float = 1.3,
              c_rise: float = 0.3) -> dict:
    """A watch as signal detection over time on task: sensitivity falls from d0 by ``drop`` with time constant
    ``tau`` minutes, and the criterion rises by ``c_rise`` (observers grow more cautious).  Returns hit and
    false-alarm rates per time point."""
    t = np.asarray(minutes, float)
    d = d0 - drop * (1 - np.exp(-t / tau))
    c = criterion + c_rise * (1 - np.exp(-t / tau))
    return {"d": d, "c": c, "hits": norm.sf(c - d), "fas": norm.sf(c)}


def notice_probability(similarity: np.ndarray, load: float = 0.5, slope: float = 6.0, bias: float = 0.0) -> np.ndarray:
    """Inattentional blindness as an attentional set (Most et al. 2001): the unexpected object is noticed with
    probability logistic(slope · (similarity to the attended items − load) + bias)."""
    s = np.asarray(similarity, float)
    return 1 / (1 + np.exp(-(slope * (s - load) + bias)))
