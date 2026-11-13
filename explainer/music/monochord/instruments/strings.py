"""Three ways to set a string going, and the boxes that make it heard (Part 7, *Strings, Hammers and Bows*).

    karplus_strong   the algorithm of 1983: a burst of noise going round a delay line
    hammer_strike    a felt hammer thrown at a stiff string (the piano), solved mode by mode during the contact
    struck           the note that follows, as the force on the bridge
    pair             two strings of one note on a shared bridge: Weinreich's double decay
    bowed            a string under a bow: stick and slip (McIntyre, Schumacher and Woodhouse, 1983)
    schelleng        the limits of bow force between which the Helmholtz motion lives
    Body             a box as a set of resonances; a guitar and a violin
    two_mass         the guitar's two lowest resonances: a plate on a spring of air with a hole in it

No manim.  Checked in ``tests/music/test_strings.py`` against closed forms (the stiff string's partials, the
Helmholtz motion's slip time, Schelleng's limits, the two-mass identity) and against published values (Chaigne and
Askenfelt's contact times).
"""

from __future__ import annotations

import math
from dataclasses import dataclass, field

import numpy as np

from ..audio import SR
from ..physics.string import String

try:                                    # the bow's loop is a hundred times faster compiled
    from numba import njit
except Exception:                       # pragma: no cover
    def njit(*a, **k):
        def wrap(f):
            return f
        return wrap if not (a and callable(a[0])) else a[0]


# ---------------------------------------------------------------------------
# Karplus and Strong (1983)
# ---------------------------------------------------------------------------
@njit(cache=True)
def _ks(buf, n_out, stretch):
    n = len(buf)
    out = np.empty(n_out)
    prev = 0.0
    k = 0
    for i in range(n_out):
        x = buf[k]
        y = (1.0 - stretch) * x + stretch * prev         # the averaging that makes high partials die first
        prev = x
        buf[k] = y
        out[i] = x
        k += 1
        if k == n:
            k = 0
    return out


def karplus_strong(hz: float, seconds: float, sr: int = SR, seed: int = 0, stretch: float = 0.5) -> np.ndarray:
    """A plucked string in three lines: fill a delay line one period long with noise, and send it round and round
    through a two-point average.  The delay is a whole number of samples (less the average's half), so the pitch
    is ``sr / (N + 1/2)``, not exactly ``hz``."""
    n = max(int(round(sr / hz - 0.5)), 2)
    rng = np.random.default_rng(seed)
    y = _ks(rng.uniform(-1.0, 1.0, n), int(seconds * sr), stretch)
    return y / np.abs(y).max()


def ks_pitch(hz: float, sr: int = SR) -> float:
    """The pitch the basic algorithm really gives for a requested ``hz``."""
    return sr / (max(int(round(sr / hz - 0.5)), 2) + 0.5)


# ---------------------------------------------------------------------------
# The piano: a hammer and a stiff string
# ---------------------------------------------------------------------------
# Middle C on a grand, after Chaigne and Askenfelt (1994): 62 cm of 1 mm steel at about 650 N, a hammer of 3 grams
# whose felt stiffens as it is squeezed (force = K * compression^p), striking at 12% of the length.
PIANO_C4 = String.tuned(261.6255653005986, L=0.62, mu=6.34e-3, kappa=1.25, sigma0=0.6, sigma1=3.3e-4)


@dataclass
class Hammer:
    mass: float = 2.97e-3       # kg
    K: float = 4.5e9            # N / m^p
    p: float = 2.5
    at: float = 0.12            # striking point, as a fraction of the length


def _modes(string: String, f_max: float):
    n_max = 1
    while string.mode_freq(n_max + 1) < f_max and n_max < 300:
        n_max += 1
    n = np.arange(1, n_max + 1, dtype=np.float64)
    return n, string.mode_omega0(n), string.mode_decay(n)


def hammer_strike(string: String = PIANO_C4, hammer: Hammer | None = None, velocity: float = 1.5, sr: float = 384_000.0,
                  window: float = 0.012, f_max: float = 12_000.0) -> dict:
    """Throw the hammer at the string and follow both until the hammer has left.  The string is a sum of its modes
    (each an oscillator, advanced exactly over a time step); the felt's force acts on all of them at the striking
    point.  Returns the contact force against time, the contact time, and each mode's state at the end."""
    h = hammer or Hammer()
    n, w0, sig = _modes(string, f_max)
    phi = np.sin(n * np.pi * h.at)                      # each mode's shape at the striking point
    m_modal = string.mu * string.L / 2.0
    dt = 1.0 / sr
    wd = np.sqrt(np.maximum(w0 ** 2 - sig ** 2, 1e-12))
    e, c, s = np.exp(-sig * dt), np.cos(wd * dt), np.sin(wd * dt)
    q, v = np.zeros(len(n)), np.zeros(len(n))
    yh, vh = 0.0, float(velocity)
    steps = int(window * sr)
    force = np.zeros(steps)
    bridge = np.zeros(steps)
    slope = n * np.pi / string.L * string.T             # bridge force per unit modal amplitude

    def felt(yh_, q_):
        comp = yh_ - float(phi @ q_)
        return h.K * comp ** h.p if comp > 0 else 0.0

    f = felt(yh, q)
    for k in range(steps):
        v = v + 0.5 * dt * f * phi / m_modal            # half a push from the felt
        vh_half = vh - 0.5 * dt * f / h.mass
        a, b = q, (v + sig * q) / wd                    # each mode turns freely for one step
        q_new = e * (a * c + b * s)
        v = e * (-a * wd * s + b * wd * c) - sig * q_new
        q = q_new
        yh = yh + dt * vh_half
        f = felt(yh, q)
        v = v + 0.5 * dt * f * phi / m_modal
        vh = vh_half - 0.5 * dt * f / h.mass
        force[k] = f
        bridge[k] = float(slope @ q)
    on = np.flatnonzero(force > 0)
    contact = (on[-1] - on[0] + 1) / sr if on.size else 0.0
    return {"t": np.arange(steps) / sr, "force": force, "bridge": bridge, "contact": contact, "peak_force": float(force.max()),
            "n": n, "hz": w0 / (2 * np.pi), "omega_d": wd, "decay": sig, "q": q, "v": v, "slope": slope, "sr": sr, "window": window,
            "hammer_out": vh, "energy_in": 0.5 * h.mass * (velocity ** 2 - vh ** 2)}


def struck(string: String = PIANO_C4, hammer: Hammer | None = None, velocity: float = 1.5, seconds: float = 3.0, sr: int = SR,
           strike: dict | None = None) -> np.ndarray:
    """The force on the bridge of a struck string, peak 1: the contact as simulated, then every mode ringing on."""
    d = strike or hammer_strike(string, hammer, velocity)
    step = int(round(d["sr"] / sr))
    head = d["bridge"][::step]
    t = np.arange(int(seconds * sr)) / sr - d["window"]
    tail = np.zeros(len(t))
    later = t >= 0
    tt = t[later]
    for q, v, wd, sig, sl in zip(d["q"], d["v"], d["omega_d"], d["decay"], d["slope"]):
        tail[later] += sl * np.exp(-sig * tt) * (q * np.cos(wd * tt) + (v + sig * q) / wd * np.sin(wd * tt))
    y = tail
    m = min(len(head), int(d["window"] * sr), len(y))
    y[:m] = head[:m]
    return y / max(np.abs(y).max(), 1e-12)


def partial_levels(d: dict) -> np.ndarray:
    """The strength (dB re the strongest) of each partial in the bridge force after a strike."""
    amp = np.abs(d["slope"]) * np.sqrt(d["q"] ** 2 + ((d["v"] + d["decay"] * d["q"]) / d["omega_d"]) ** 2)
    return 20 * np.log10(np.maximum(amp / amp.max(), 1e-9))


def strike_centroid(d: dict) -> float:
    """The brightness of a struck note: the mean frequency of its partials, weighted by their power."""
    amp = np.abs(d["slope"]) * np.sqrt(d["q"] ** 2 + ((d["v"] + d["decay"] * d["q"]) / d["omega_d"]) ** 2)
    return float(np.sum(d["hz"] * amp ** 2) / np.sum(amp ** 2))


# ---------------------------------------------------------------------------
# Two strings, one bridge (Weinreich, 1977)
# ---------------------------------------------------------------------------
def pair(detune_cents: float = 0.0, seconds: float = 6.0, rate: float = 200.0, f0: float = 261.63, own_loss: float = 0.25,
         bridge_loss: float = 1.6, unequal: float = 0.0, single: bool = False) -> dict:
    """Two strings of one note (or one, with ``single``), tuned ``detune_cents`` apart, pushing on the same bridge.
    Each loses energy to its own friction (``own_loss``, 1/s) and to the bridge (``bridge_loss``); but the bridge
    moves with the *sum* of their forces, so strings moving together lose energy to it twice as fast, and strings
    moving oppositely not at all.  Returns the level of the bridge's motion against time (dB), from the exact
    solution of the two coupled equations."""
    t = np.arange(int(seconds * rate)) / rate
    if single:
        env = np.exp(-(own_loss + bridge_loss) * t)
        return {"t": t, "db": 20 * np.log10(np.maximum(env, 1e-9)), "rates": [own_loss + bridge_loss]}
    dw = 2 * np.pi * f0 * (2 ** (detune_cents / 1200.0) - 1.0)
    m = np.array([[-own_loss - bridge_loss + 0.5j * dw, -bridge_loss], [-bridge_loss, -own_loss - bridge_loss - 0.5j * dw]])
    lam, vec = np.linalg.eig(m)
    a0 = np.array([1.0, 1.0 - unequal], dtype=complex)
    coef = np.linalg.solve(vec, a0)
    a = (vec * coef) @ np.exp(np.outer(lam, t))          # the two strings' complex amplitudes
    total = np.abs(a[0] + a[1]) / abs(a0.sum())
    return {"t": t, "db": 20 * np.log10(np.maximum(total, 1e-9)), "rates": sorted((-lam.real).tolist(), reverse=True),
            "beat_hz": abs(lam[0].imag - lam[1].imag) / (2 * np.pi), "amp": total}


def pair_sound(detune_cents: float, seconds: float = 6.0, f0: float = 261.63, partials: int = 12, b: float = 3.9e-4, sr: int = SR,
               single: bool = False, unequal: float = 0.03, own_loss: float = 0.25, bridge_loss: float = 1.6) -> np.ndarray:
    """The same, as sound: each partial of the note is such a pair (higher partials lose more to the bridge)."""
    t = np.arange(int(seconds * sr)) / sr
    y = np.zeros(len(t))
    for n in range(1, partials + 1):
        f = f0 * n * math.sqrt((1 + b * n * n) / (1 + b))
        d = pair(detune_cents, seconds, 400.0, f, own_loss * (1 + 0.15 * n), bridge_loss * (1 + 0.25 * (n - 1)), unequal, single)
        env = np.interp(t, d["t"], 10 ** (d["db"] / 20))
        y += env * np.sin(2 * np.pi * f * t) / n ** 1.2
    return y / np.abs(y).max()


# ---------------------------------------------------------------------------
# The bowed string
# ---------------------------------------------------------------------------
@njit(cache=True)
def _bow(steps, n1, n2, vb, fb, z, mu_s, mu_d, v0, g_bridge, a_bridge, g_nut):
    to_bridge = np.zeros(n1)            # waves on their way from the bow to the bridge
    from_bridge = np.zeros(n1)
    to_nut = np.zeros(n2)
    from_nut = np.zeros(n2)
    v_out = np.empty(steps)
    f_out = np.empty(steps)
    bridge = np.empty(steps)
    slipping = np.empty(steps)
    i1, i2 = 0, 0
    lp = 0.0
    stick = True
    for s in range(steps):
        k = fb[s] / (2.0 * z)
        vib = from_bridge[i1]           # arriving at the bow from the bridge side
        vin = from_nut[i2]              # and from the nut side
        vh = vib + vin
        a = vb - vh                     # the friction (over 2Z) that would hold the string to the bow
        f2 = 0.0                        # friction force over 2Z
        if a > k * mu_s or a < -k * mu_s:
            sg = 1.0 if a > 0 else -1.0
            aa = a * sg
            b = aa - k * mu_d - v0
            d = 0.5 * (b + math.sqrt(b * b + 4.0 * v0 * (aa - k * mu_s)))
            f2 = sg * (aa - d)
            stick = False
        else:
            sg = 1.0 if a >= 0 else -1.0
            aa = a * sg
            b = aa - k * mu_d - v0
            disc = b * b + 4.0 * v0 * (aa - k * mu_s)
            if (not stick) and disc >= 0.0 and b > 0.0:
                d = 0.5 * (b + math.sqrt(disc))          # keep slipping while a slipping state exists
                f2 = sg * (aa - d)
            else:
                f2 = a
                stick = True
        v = vh + f2
        v_out[s] = v
        f_out[s] = 2.0 * z * f2
        slipping[s] = 0.0 if stick else 1.0
        # send the waves on
        arr_b = to_bridge[i1]           # reaching the bridge now
        arr_n = to_nut[i2]
        lp = (1.0 - a_bridge) * arr_b + a_bridge * lp
        from_bridge[i1] = -g_bridge * lp
        from_nut[i2] = -g_nut * arr_n
        to_bridge[i1] = vin + f2
        to_nut[i2] = vib + f2
        bridge[s] = z * (arr_b + g_bridge * lp)
        i1 += 1
        if i1 == n1:
            i1 = 0
        i2 += 1
        if i2 == n2:
            i2 = 0
    return v_out, f_out, bridge, slipping


@dataclass
class Bow:
    speed: float = 0.2          # m/s
    force: float = 0.4          # N
    at: float = 0.1             # distance from the bridge, as a fraction of the string
    mu_s: float = 0.8           # friction when sticking, at most
    mu_d: float = 0.3           # friction when slipping fast
    v0: float = 0.05            # the speed (m/s) at which friction has fallen halfway


def bowed(hz: float = 196.0, bow: Bow | None = None, seconds: float = 1.0, z: float = 0.25, g_bridge: float = 0.97, a_bridge: float = 0.35,
          g_nut: float = 0.995, oversample: int = 4, sr: int = SR, settle: float = 0.0, attack: float = 0.4, press: float | None = None) -> dict:
    """A string of impedance ``z`` (kg/s) under a bow.  Waves of velocity travel both ways from the bow; at the bow
    the string's speed and the friction must satisfy both the string (a straight line) and the rosin (a falling
    curve), and where they could do so in two ways the string keeps doing what it was doing (Friedlander's rule).
    The bridge reflects a little less than everything, and less still of the high frequencies.

    A player starts a note with a firmer bow and then eases off; so does this one: the force begins at ``press``
    (by default 0.6 of Schelleng's maximum, if that is more than the force asked for) and falls to ``bow.force``
    over ``attack`` seconds.  The Helmholtz motion has to be established: a string started from rest under a light
    bow settles into slipping twice or more in each period, and stays there.

    Returns the string's velocity under the bow, the friction force, the force on the bridge and, for each sample,
    whether the string was slipping; ``sr_sim`` is the rate they are sampled at (chosen so that a period is a whole
    number of steps)."""
    b = bow or Bow()
    half = int(round(sr * oversample / (2.0 * hz)))      # samples for one trip along the string
    sr_sim = 2.0 * hz * half
    n1 = max(int(round(b.at * half)), 1)
    n2 = half - n1
    steps = int((seconds + settle) * sr_sim)
    f_max = schelleng(n1 / half, b.speed, z, g_bridge, b.mu_s, b.mu_d)[1]
    start = press if press is not None else max(b.force, 0.6 * f_max)
    ramp = np.clip(np.arange(steps) / max(attack * sr_sim, 1.0), 0.0, 1.0)
    fb = start * (b.force / start) ** ramp               # eased off evenly on a logarithmic scale
    v, f, br, slip = _bow(steps, n1, n2, b.speed, fb, z, b.mu_s, b.mu_d, b.v0, g_bridge, a_bridge, g_nut)
    skip = int(settle * sr_sim)
    return {"v": v[skip:], "friction": f[skip:], "bridge": br[skip:], "slipping": slip[skip:], "sr_sim": sr_sim, "period": 2 * half,
            "beta": n1 / half, "bow": b, "z": z}


def bow_regime(d: dict, cycles: int = 40) -> dict:
    """What the string settled into: slips per period, the fraction of the time spent slipping, and the pitch
    (by autocorrelation of the bridge force) relative to the string's own."""
    p = d["period"]
    s = d["slipping"][-cycles * p:]
    w = max(p // 60, 3)                                  # ignore chatter shorter than a sixtieth of a period
    sm = np.convolve(s, np.ones(w) / w, mode="same") > 0.5
    starts = np.flatnonzero(sm[1:] & ~sm[:-1])
    per_cycle = len(starts) / cycles
    x = d["bridge"][-cycles * p:]
    x = x - x.mean()
    spec = np.abs(np.fft.rfft(x * np.hanning(len(x)), 8 * len(x)))
    freqs = np.fft.rfftfreq(8 * len(x), 1 / d["sr_sim"])
    f_string = d["sr_sim"] / p
    band = (freqs > 0.6 * f_string) & (freqs < 1.25 * f_string)
    pitch = float(freqs[band][int(np.argmax(spec[band]))]) if spec[band].max() > 1e-12 else 0.0
    frac = float(s.mean())
    if frac < 1e-6:
        kind = "stuck"
    elif abs(pitch / f_string - 1) > 0.01 or frac < 0.75 * d["beta"]:
        kind = "raucous"                                 # the bow holds on too long: the pitch sags, or breaks up
    elif frac > 1.3 * d["beta"]:
        kind = "multiple slips"                          # the bow lets go more than once in each period
    else:
        kind = "Helmholtz"
    return {"slips_per_period": per_cycle, "slip_fraction": frac, "pitch_ratio": pitch / f_string, "kind": kind}


def bow_limits(beta: float, hz: float = 196.0, speed: float = 0.2, z: float = 0.25, g_bridge: float = 0.97, seconds: float = 5.0, **kw) -> dict:
    """The least and the greatest bow force at which this model keeps a Helmholtz motion, at a bow position
    ``beta``.  The least: start in the Helmholtz motion and ease the force down slowly until the string starts to
    slip more than once a period.  The greatest: by bisection on steady notes, until the pitch sags."""
    lo, hi = schelleng(beta, speed, z, g_bridge)
    start = 0.6 * hi
    d = bowed(hz, Bow(speed=speed, force=lo / 6, at=beta), seconds=seconds, attack=seconds, press=start, z=z, g_bridge=g_bridge, **kw)
    p = d["period"]
    ncyc = len(d["slipping"]) // p
    frac = d["slipping"][: ncyc * p].reshape(ncyc, p).mean(axis=1)
    force = start * ((lo / 6) / start) ** np.clip(np.arange(ncyc) * p / (seconds * d["sr_sim"]), 0, 1)
    ok = np.abs(frac / d["beta"] - 1) < 0.3
    run = np.convolve(ok.astype(float), np.ones(15), mode="valid") >= 15            # fifteen good periods in a row
    k = np.flatnonzero(run)
    f_min = float(force[k[-1] + 14]) if k.size else float("nan")                   # the last force at which it still held
    a, b = 0.6 * hi, 6.0 * hi
    for _ in range(7):
        mid = math.sqrt(a * b)
        r = bow_regime(bowed(hz, Bow(speed=speed, force=mid, at=beta), seconds=1.2, z=z, g_bridge=g_bridge, press=0.6 * hi, attack=0.3, **kw))
        if r["kind"] == "Helmholtz":
            a = mid
        else:
            b = mid
    return {"beta": d["beta"], "min": f_min, "max": math.sqrt(a * b), "schelleng_min": lo, "schelleng_max": hi}


def schelleng(beta: float, speed: float, z: float, g_bridge: float, mu_s: float = 0.8, mu_d: float = 0.3) -> tuple[float, float]:
    """Schelleng's limits (1973) on the bow force for a Helmholtz motion: ``(minimum, maximum)``.  The maximum falls
    as 1/beta and the minimum as 1/beta^2; the bridge's resistance R follows from how much it reflects."""
    r = z * (1 + g_bridge) / (1 - g_bridge)
    f_max = 2 * z * speed / (beta * (mu_s - mu_d))
    f_min = z * z * speed / (2 * r * beta * beta * (mu_s - mu_d))
    return f_min, f_max


def bowed_note(hz: float, seconds: float, bow: Bow | None = None, attack: float = 0.06, release: float = 0.08, sr: int = SR, **kw) -> np.ndarray:
    """The force on the bridge of a bowed note at the film's sample rate (a slow start of the bow is imitated by a
    fade: the string itself is started in its steady motion)."""
    from scipy.signal import resample_poly

    d = bowed(hz, bow, seconds + 0.45, settle=0.0, sr=sr, **kw)
    y = d["bridge"]
    ratio = d["sr_sim"] / sr
    up, down = 1, int(round(ratio)) if abs(ratio - round(ratio)) < 1e-9 else 0
    if down:
        y = resample_poly(y, up, down)
    else:
        n = int(len(y) / ratio)
        y = np.interp(np.arange(n) * ratio, np.arange(len(y)), y)
    y = y[int(0.4 * sr): int(0.4 * sr) + int(seconds * sr)]
    y = y - y.mean()
    a, r = int(attack * sr), int(release * sr)
    y[:a] *= np.linspace(0, 1, a) ** 2
    y[-r:] *= np.linspace(1, 0, r)
    return y / max(np.abs(y).max(), 1e-12)


# ---------------------------------------------------------------------------
# Bodies
# ---------------------------------------------------------------------------
RHO, C_AIR = 1.2, 343.0


def two_mass(volume: float = 0.014, hole_radius: float = 0.043, plate_mass: float = 0.06, plate_area: float = 0.05, plate_hz: float = 185.0,
             neck: float | None = None) -> dict:
    """The guitar below 250 Hz (Christensen and Vistisen, 1980): the top plate is a mass on a spring; the air in the
    soundhole is a second mass; the air in the box is the spring between them.  ``plate_hz`` is the plate's own
    resonance with the hole taped shut.  Returns the Helmholtz resonance of the box if its walls were rigid, and
    the two resonances of the coupled pair, which obey ``f_-^2 + f_+^2 = f_h^2 + f_p^2``."""
    s = math.pi * hole_radius ** 2
    length = 1.7 * hole_radius if neck is None else neck      # the hole's effective length: two end corrections
    m_h = RHO * s * length
    k_air = RHO * C_AIR ** 2 / volume
    w_h2 = k_air * s * s / m_h
    w_p2 = (2 * math.pi * plate_hz) ** 2
    w_c4 = k_air ** 2 * s * s * plate_area ** 2 / (m_h * plate_mass)        # the coupling
    mean, half = 0.5 * (w_h2 + w_p2), 0.5 * math.sqrt((w_p2 - w_h2) ** 2 + 4 * w_c4)
    return {"helmholtz": math.sqrt(w_h2) / (2 * math.pi), "plate": plate_hz, "lower": math.sqrt(mean - half) / (2 * math.pi),
            "upper": math.sqrt(mean + half) / (2 * math.pi), "hole_mass": m_h, "air_spring": k_air}


@dataclass
class Body:
    """A box as a list of resonances ``(hz, Q, strength)``; ``strength`` may be negative (a mode that moves the
    other way).  ``tilt`` (dB per octave above ``knee``) is how the response falls away at high frequencies."""
    modes: list = field(default_factory=list)
    knee: float = 4000.0
    tilt: float = -12.0
    name: str = ""

    def response(self, f) -> np.ndarray:
        f = np.asarray(f, dtype=float)
        h = np.zeros(len(f), dtype=complex)
        for hz, q, a in self.modes:
            h += a * (f / hz) ** 2 / (1 - (f / hz) ** 2 + 1j * (f / hz) / q)    # the sound a mode radiates follows its acceleration
        roll = np.where(f > self.knee, (np.maximum(f, 1e-9) / self.knee) ** (self.tilt / 6.02), 1.0)
        return h * roll

    def response_db(self, f) -> np.ndarray:
        h = np.abs(self.response(f))
        return 20 * np.log10(np.maximum(h, 1e-12))

    def play(self, force: np.ndarray, sr: int = SR, mix_direct: float = 0.0) -> np.ndarray:
        """The sound of a force on the bridge, through this body (peak 1)."""
        n = len(force) + int(0.5 * sr)                   # room for the box to ring on
        spec = np.fft.rfft(force, n)
        f = np.fft.rfftfreq(n, 1 / sr)
        y = np.fft.irfft(spec * self.response(np.maximum(f, 1e-6)), n)[: len(force) + int(0.3 * sr)]
        if mix_direct:
            y[: len(force)] += mix_direct * force * np.abs(y).max() / max(np.abs(force).max(), 1e-12)
        return y / max(np.abs(y).max(), 1e-12)

    def tap(self, seconds: float = 0.6, sr: int = SR) -> np.ndarray:
        """A knuckle on the bridge: the body's own sound."""
        x = np.zeros(int(seconds * sr))
        x[: int(0.003 * sr)] = np.hanning(int(0.003 * sr))            # a knuckle is soft: three milliseconds
        return self.play(x, sr)[: len(x)]


def guitar_body() -> Body:
    """A classical guitar: the two lowest resonances from :func:`two_mass`, then top-plate modes placed as on
    measured instruments (Fletcher and Rossing, table 9.2), their strengths falling with frequency."""
    t = two_mass()
    modes = [(t["lower"], 18.0, 1.0), (t["upper"], 22.0, -1.3), (290.0, 30.0, 0.35), (375.0, 30.0, -0.5), (436.0, 35.0, 0.45), (553.0, 35.0, -0.4),
             (628.0, 40.0, 0.3), (760.0, 40.0, -0.3), (980.0, 45.0, 0.25), (1200.0, 45.0, -0.2), (1500.0, 40.0, 0.18), (1900.0, 40.0, -0.15),
             (2500.0, 30.0, 0.12), (3200.0, 30.0, -0.1)]
    return Body(modes, knee=3500.0, tilt=-18.0, name="guitar")


def violin_body() -> Body:
    """A violin: the air resonance A0, the two main body resonances B1- and B1+, a crowd of plate modes, and the
    broad 'bridge hill' between 2 and 3 kHz (frequencies typical of measured violins: Jansson; Bissinger)."""
    modes = [(275.0, 22.0, 0.8), (460.0, 35.0, -1.0), (540.0, 35.0, 1.1), (700.0, 30.0, -0.5), (860.0, 30.0, 0.55), (1050.0, 28.0, -0.5),
             (1300.0, 25.0, 0.4), (1650.0, 22.0, -0.4), (2050.0, 18.0, 0.5), (2500.0, 3.0, 3.5), (3100.0, 15.0, -0.4), (3900.0, 14.0, 0.3)]
    return Body(modes, knee=4500.0, tilt=-18.0, name="violin")


def soundboard() -> Body:
    """A piano's soundboard: so many overlapping resonances that above a hundred hertz it is nearly even; a few
    broad modes at the bottom stand for the rest."""
    modes = [(62.0, 6.0, 0.6), (110.0, 5.0, -0.8), (180.0, 4.0, 0.9), (300.0, 3.0, -1.0), (520.0, 2.5, 1.0), (900.0, 2.0, -1.0), (1600.0, 1.8, 1.0),
             (2800.0, 1.6, -0.9), (4800.0, 1.5, 0.7)]
    return Body(modes, knee=5000.0, tilt=-12.0, name="soundboard")
