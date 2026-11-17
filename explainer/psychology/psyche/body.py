"""The body the mind sits in: a clock, a sleep debt, a stress loop and drugs, each as a control loop
(videos/psychology/SYLLABUS.md, Part 10).

**The clock.**  :class:`Clock` is a van der Pol oscillator with a light input, in the style of Kronauer's models
of the human circadian pacemaker: left alone it cycles with a period a little longer than 24 hours
(:func:`free_running_period`); a daily light-dark cycle pulls it to exactly 24 (:func:`entrain`); a pulse of
light moves its phase later or earlier depending on when it falls (:func:`phase_response`); and after a flight
across time zones it re-entrains at about a zone a day, faster going west (:func:`jet_lag`).

**Sleep.**  :func:`two_process` is Borbely's model: a sleep pressure S that rises while awake and falls while
asleep, between two thresholds that a circadian process C moves up and down.  It gives the timing of sleep, the
short recovery sleep after a night without, and an alertness curve (:func:`alertness`) with a dip in the
afternoon.  :func:`lapses` is the dose-response finding of chronic restriction: lapses of attention grow with
cumulative wakefulness beyond about sixteen hours a day.

**Stress.**  :func:`hpa` is the stress axis as a negative-feedback loop of three hormones, with a daily drive, a
response to a stressor that switches itself off, and a version whose feedback is weak.

**Drugs.**  :func:`occupancy` is the Hill equation; :func:`with_antagonist` the rightward shift a competitive
antagonist produces; :func:`first_order` and :func:`zero_order` the two ways a drug leaves the body;
:func:`dosing` a day of repeated doses.  :func:`opponent` is Solomon and Corbit's opponent process: a response
that follows the drug and a slower one that opposes it and grows with use, which gives tolerance and
withdrawal; :func:`conditioned_tolerance` lets the opposing response be triggered by the place.

**Chronotype.**  :func:`midsleep` and :func:`social_jetlag` are the two numbers of the Munich questionnaire.

Nothing here imports manim.
"""

from __future__ import annotations

import math
from dataclasses import dataclass

import numpy as np
from scipy.integrate import solve_ivp

__all__ = [
    "Clock", "light_schedule", "free_running_period", "entrain", "phase_response", "jet_lag",
    "circadian_c", "two_process", "alertness", "lapses", "hpa", "occupancy", "with_antagonist", "first_order",
    "zero_order", "dosing", "opponent", "conditioned_tolerance", "midsleep", "social_jetlag",
]

TAU_RISE, TAU_FALL = 18.18, 4.2  # hours: sleep pressure's time constants awake and asleep (Daan et al. 1984)


# ----------------------------------------------------------------------------------------- the clock
def light_schedule(on: float = 7.0, off: float = 23.0, lux: float = 300.0, dark: float = 0.0, day: float = 24.0,
                   shift_at: float | None = None, shift: float = 0.0):
    """A function of time (hours) giving the light level: ``lux`` between ``on`` and ``off`` o'clock of a day
    ``day`` hours long, ``dark`` otherwise.  From ``shift_at`` on, the whole schedule moves ``shift`` hours later
    (a flight west) or earlier (negative: a flight east)."""
    def light(t: float) -> float:
        tt = t - (shift if shift_at is not None and t >= shift_at else 0.0)
        h = tt % day
        lit = on <= h < off if on < off else (h >= on or h < off)
        return lux if lit else dark
    return light


@dataclass
class Clock:
    """A van der Pol oscillator driven by light.  ``x`` is the rhythm's main variable (its minimum is the body
    temperature minimum); ``xc`` its companion; ``n`` the share of the eye's light-sensitive elements in use.

        dx/dt  = (pi/12) (xc + B)
        dxc/dt = (pi/12) (mu (xc - 4 xc^3 / 3) - x ((24 / (0.99669 tau))^2 + k B))
        dn/dt  = 60 (alpha (1 - n) - beta n),   alpha = alpha0 (I / I0)^p,   B = G alpha (1 - n) (1 - 0.4 x)(1 - 0.4 xc)
    """
    tau: float = 24.2
    mu: float = 0.13
    k: float = 0.55
    alpha0: float = 0.16
    beta: float = 0.013
    G: float = 19.875
    p: float = 0.6
    I0: float = 9500.0

    def rhs(self, t, y, light):
        x, xc, n = y
        I = max(float(light(t)), 0.0)
        alpha = self.alpha0 * (I / self.I0) ** self.p if I > 0 else 0.0
        B = self.G * alpha * (1 - n) * (1 - 0.4 * x) * (1 - 0.4 * xc)
        w = math.pi / 12
        return [w * (xc + B),
                w * (self.mu * (xc - 4 * xc ** 3 / 3) - x * ((24 / (0.99669 * self.tau)) ** 2 + self.k * B)),
                60 * (alpha * (1 - n) - self.beta * n)]

    def run(self, hours: float, light, y0=(-1.0, 0.0, 0.0), dt: float = 0.05):
        """Integrate for ``hours``; returns (t, x, xc)."""
        t = np.arange(0.0, hours + dt / 2, dt)
        sol = solve_ivp(self.rhs, (0.0, float(t[-1])), list(y0), t_eval=t, args=(light,), max_step=0.1, rtol=1e-6,
                        atol=1e-8)
        return sol.t, sol.y[0], sol.y[1]


def _minima(t: np.ndarray, x: np.ndarray) -> np.ndarray:
    """Times of the rhythm's minima (the body temperature minimum): one for each cycle, taken as the lowest point
    between a downward and the next upward crossing of zero, so that ripples from the light do not count."""
    sign = x > 0
    down = np.where(sign[:-1] & ~sign[1:])[0] + 1
    up = np.where(~sign[:-1] & sign[1:])[0] + 1
    out = []
    for d in down:
        later = up[up > d]
        if not len(later):
            break
        k = d + int(np.argmin(x[d:later[0]]))
        if 0 < k < len(x) - 1:
            a, b, c = x[k - 1], x[k], x[k + 1]
            den = a - 2 * b + c
            out.append(t[k] + (0.5 * (a - c) / den if den else 0.0) * (t[1] - t[0]))
    return np.array(out)


def free_running_period(clock: Clock | None = None, days: int = 30, lux: float = 0.0) -> float:
    """The period in constant conditions (darkness by default), from the last ten cycles."""
    clock = clock or Clock()
    t, x, _ = clock.run(24.0 * days, lambda _t: lux)
    m = _minima(t, x)
    return float(np.diff(m[-11:]).mean())


def entrain(clock: Clock | None = None, day: float = 24.0, days: int = 40, lux: float = 300.0, on: float = 7.0,
            off: float = 23.0, dark: float = 0.0) -> dict:
    """Live on a schedule of ``day`` hours with light from ``on`` to ``off``.  Returns the rhythm's period over
    the last ten cycles, whether it has locked to the schedule, and the clock time of its minimum."""
    clock = clock or Clock()
    scale = day / 24.0
    light = light_schedule(on * scale, off * scale, lux, dark, day)
    t, x, _ = clock.run(day * days, light)
    m = _minima(t, x)
    period = float(np.diff(m[-11:]).mean())
    phase = (m[-10:] % day) / scale
    spread = float(np.ptp(np.unwrap(phase * 2 * math.pi / 24) * 24 / (2 * math.pi)))
    return {"period": period, "locked": abs(period - day) < 0.05 and spread < 0.5, "minimum_at": float(phase[-1]),
            "t": t, "x": x, "minima": m}


def phase_response(clock: Clock | None = None, lux: float = 9500.0, hours: float = 3.0, steps: int = 24) -> dict:
    """A phase response curve: after entrainment to an ordinary day, the person stays in dim light, gets one
    pulse of bright light centred at each of ``steps`` times, and the shift of the next minima is read off
    against the same person with no pulse.  Positive is an advance (earlier)."""
    clock = clock or Clock()
    base = entrain(clock, days=30)
    y_end = None
    # restart from the entrained state: rerun to get the full state at the end of day 30
    light0 = light_schedule()
    sol = solve_ivp(clock.rhs, (0.0, 24.0 * 30), [-1.0, 0.0, 0.0], args=(light0,), max_step=0.1, rtol=1e-6, atol=1e-8)
    y_end = sol.y[:, -1]
    dim = 5.0

    def after(pulse_at):
        def light(t):
            return lux if pulse_at is not None and abs(t - pulse_at) <= hours / 2 else dim
        t = np.arange(0.0, 24.0 * 6, 0.05)
        s = solve_ivp(clock.rhs, (0.0, float(t[-1])), list(y_end), t_eval=t, args=(light,), max_step=0.1, rtol=1e-6,
                      atol=1e-8)
        return _minima(s.t, s.y[0])

    ref = after(None)
    centre = np.linspace(0.0, 24.0, steps, endpoint=False) + 24.0   # pulses during the second day in dim light
    shifts = []
    for c in centre:
        m = after(float(c))
        shifts.append(float(ref[-1] - m[-1]))
    # express the pulse time relative to the temperature minimum of that day
    tmin = ref[(ref > 24.0) & (ref < 48.0)]
    rel = (centre - (tmin[0] if len(tmin) else ref[1]) + 12.0) % 24.0 - 12.0
    order = np.argsort(rel)
    return {"hours_from_minimum": rel[order], "shift": np.array(shifts)[order], "entrained_minimum": base["minimum_at"]}


def jet_lag(zones: float, clock: Clock | None = None, days: int = 14, lux: float = 300.0) -> dict:
    """Fly across ``zones`` time zones (positive: east, the day comes earlier) after a month at home.  Returns,
    day by day, how far the rhythm's minimum is from where it will settle, and the days until it is within an
    hour."""
    clock = clock or Clock()
    home = 30
    light = light_schedule(lux=lux, shift_at=24.0 * home, shift=-float(zones))
    t, x, _ = clock.run(24.0 * (home + days), light)
    m = _minima(t, x)
    before = m[m < 24.0 * home]
    target = (before[-1] % 24.0 - zones) % 24.0
    after = m[m >= 24.0 * home]
    off = (after % 24.0 - target + 12.0) % 24.0 - 12.0
    day = np.floor(after / 24.0) - home
    ok = np.where(np.abs(off) < 1.0)[0]
    return {"day": day, "hours_off": off, "days_to_adjust": float(day[ok[0]]) if len(ok) else float("nan")}


# ----------------------------------------------------------------------------------------- sleep
def circadian_c(t) -> np.ndarray:
    """The circadian process of the two-process model: a skewed daily wave (Daan et al. 1984), t in hours, with
    its trough in the small hours and its crest around the middle of the day."""
    w = 2 * math.pi / 24.0
    tt = np.asarray(t, float) - 8.6
    return (0.97 * np.sin(w * tt) + 0.22 * np.sin(2 * w * tt) + 0.07 * np.sin(3 * w * tt) + 0.03 * np.sin(4 * w * tt)
            + 0.001 * np.sin(5 * w * tt))


def two_process(hours: float = 96.0, upper: float = 0.67, lower: float = 0.17, amp: float = 0.12, s0: float = 0.3,
                awake0: bool = True, keep_awake=(), dt: float = 0.01) -> dict:
    """Simulate sleep and waking.  Awake, S rises toward 1 with time constant 18.18 h; asleep it falls toward 0
    with 4.2 h.  Sleep starts when S reaches ``upper + amp C(t)`` and ends when it reaches ``lower + amp C(t)``.
    ``keep_awake`` is a list of (from, to) intervals in hours during which sleep is not allowed.  Returns the time
    grid, S, the two thresholds, a boolean ``asleep`` and the list of sleep episodes (start, end)."""
    t = np.arange(0.0, hours, dt)
    c = circadian_c(t)
    hi, lo = upper + amp * c, lower + amp * c
    S = np.empty_like(t)
    asleep = np.zeros(len(t), bool)
    s, sleeping = s0, not awake0
    episodes, start = [], None
    for i, ti in enumerate(t):
        forced = any(a <= ti < b for a, b in keep_awake)
        if sleeping and (s <= lo[i] or forced):
            sleeping = False
            episodes.append((start, float(ti)))
        elif not sleeping and s >= hi[i] and not forced:
            sleeping, start = True, float(ti)
        s = s * math.exp(-dt / TAU_FALL) if sleeping else 1 - (1 - s) * math.exp(-dt / TAU_RISE)
        S[i], asleep[i] = s, sleeping
    return {"t": t, "S": S, "upper": hi, "lower": lo, "asleep": asleep, "episodes": episodes, "C": c}


def alertness(t, S, circadian: float = 0.27, crest: float = 18.0, dip: float = 0.05, dip_at: float = 14.5) -> np.ndarray:
    """A waking alertness curve: a circadian drive for wakefulness that crests in the evening, minus sleep
    pressure, which climbs all day.  The two nearly cancel, which is why alertness holds up until bedtime and then
    falls off quickly; a small twelve-hour term flattens the early afternoon (with these defaults it is too small to
    make a dip, and the films claim none).  ``crest`` and ``dip_at`` are
    clock hours."""
    tt = np.asarray(t, float)
    drive = circadian * np.cos(2 * math.pi * (tt - crest) / 24.0)
    return drive - np.asarray(S, float) - dip * np.cos(4 * math.pi * (tt - dip_at) / 24.0)


def lapses(hours_in_bed: float, days: int = 14, need_awake: float = 15.84, per_hour: float = 0.15, base: float = 1.0) -> np.ndarray:
    """Lapses of attention on a ten-minute vigilance test, day by day, when ``hours_in_bed`` are allowed each
    night: proportional to the cumulative wakefulness in excess of ``need_awake`` hours a day (Van Dongen et al.
    2003).  ``per_hour`` and ``base`` set the scale and are illustrative."""
    excess = max(24.0 - hours_in_bed - need_awake, 0.0)
    return base + per_hour * excess * np.arange(1, days + 1)


# ----------------------------------------------------------------------------------------- stress
def hpa(hours: float = 72.0, stress=(), feedback: float = 1.0, drive_amp: float = 0.6, dt: float = 0.01) -> dict:
    """The stress axis: the brain's signal C drives the pituitary's A, which drives cortisol F, and cortisol
    turns both down.

        dC/dt = (d(t) + stress(t)) / (1 + feedback F) - C / 0.3
        dA/dt = C / (1 + feedback F) - A / 0.5
        dF/dt = A - F / 1.2            (hours)

    ``d(t)`` is a daily drive that peaks before waking; ``stress`` is a list of (start, hours, size) pulses.
    ``feedback`` below 1 is a loop whose brake is worn."""
    t = np.arange(0.0, hours, dt)
    C, A, F = np.empty_like(t), np.empty_like(t), np.empty_like(t)
    c = a = f = 0.5
    for i, ti in enumerate(t):
        d = 1.0 + drive_amp * math.cos(2 * math.pi * (ti - 6.0) / 24.0)
        s = sum(size for start, dur, size in stress if start <= ti < start + dur)
        brake = 1 + feedback * f
        c += dt * ((d + s) / brake - c / 0.3)
        a += dt * (c / brake - a / 0.5)
        f += dt * (a - f / 1.2)
        C[i], A[i], F[i] = c, a, f
    return {"t": t, "crh": C, "acth": A, "cortisol": F}


# ----------------------------------------------------------------------------------------- drugs
def occupancy(dose, kd: float = 1.0, n: float = 1.0):
    """The Hill equation: the share of receptors occupied (or of the largest effect) at concentration ``dose``."""
    d = np.asarray(dose, float) ** n
    return d / (kd ** n + d)


def with_antagonist(dose, antagonist: float, kb: float = 1.0, kd: float = 1.0, n: float = 1.0):
    """Occupancy by an agonist while a competitive antagonist at concentration ``antagonist`` (dissociation
    constant ``kb``) is present: the curve keeps its shape and moves right by the factor 1 + antagonist / kb."""
    return occupancy(dose, kd * (1 + antagonist / kb), n)


def first_order(t, dose: float = 1.0, half_life: float = 5.0):
    """The amount left when a constant share leaves per hour."""
    return dose * 0.5 ** (np.asarray(t, float) / half_life)


def zero_order(t, dose: float = 1.0, rate: float = 0.15):
    """The amount left when a constant amount leaves per hour (alcohol, roughly)."""
    return np.clip(dose - rate * np.asarray(t, float), 0.0, None)


def dosing(times, hours: float = 24.0, dose: float = 1.0, half_life: float = 5.0, absorb: float = 0.75, dt: float = 0.01) -> dict:
    """Doses taken at ``times`` (hours), absorbed with time constant ``absorb`` hours and cleared with
    ``half_life``.  Returns the time grid and the level in the body."""
    t = np.arange(0.0, hours, dt)
    ke, ka = math.log(2) / half_life, 1.0 / absorb
    level = np.zeros_like(t)
    for t0 in times:
        s = np.clip(t - t0, 0.0, None)
        level += np.where(t >= t0, dose * ka / (ka - ke) * (np.exp(-ke * s) - np.exp(-ka * s)), 0.0)
    return {"t": t, "level": level}


def opponent(doses: int = 1, every: float = 24.0, on: float = 4.0, hours: float | None = None, gain: float = 0.25,
             tau_b: float = 1.5, growth: float = 0.3, b_max: float = 1.2, dt: float = 0.01) -> dict:
    """Solomon and Corbit's opponent process.  The a-process is 1 while the drug is on board and 0 otherwise; the
    b-process follows it slowly (time constant ``tau_b`` hours) with a strength that starts at ``gain`` and grows
    with each dose toward ``b_max``.  What is felt is a - b.  Returns the time grid, a, b, their difference, and
    for each dose the peak of the felt effect and the depth of the after-effect."""
    hours = hours if hours is not None else every * doses + 24.0
    t = np.arange(0.0, hours, dt)
    a = np.zeros_like(t)
    b = np.zeros_like(t)
    strength, bv = gain, 0.0
    peaks, troughs = [], []
    for k in range(doses):
        a[(t >= k * every) & (t < k * every + on)] = 1.0
    k_now = -1
    for i, ti in enumerate(t):
        k = int(ti // every)
        if k != k_now and k < doses:
            if k_now >= 0:
                strength = strength + growth * (b_max - strength)
            k_now = k
        bv += dt * (strength * a[i] - bv) / tau_b
        b[i] = bv
    net = a - b
    felt = []
    for k in range(doses):
        sel = (t >= k * every) & (t < (k + 1) * every)
        peaks.append(float(net[sel].max()))
        troughs.append(float(net[sel].min()))
        felt.append(float(net[(t >= k * every) & (t < k * every + on)].mean()))
    return {"t": t, "a": a, "b": b, "net": net, "peaks": np.array(peaks), "troughs": np.array(troughs),
            "felt": np.array(felt)}


def conditioned_tolerance(dose: float, tolerance_usual: float, tolerance_new: float, lethal: float = 1.0, spread: float = 0.35,
                          n: int = 100_000, rng=None) -> dict:
    """The compensating response has been learned to the usual place.  An animal's effective dose is
    ``dose`` minus the tolerance the setting brings out, and it dies if that exceeds its own lethal dose (which
    varies between animals, log-normally, with median ``lethal``).  Returns the share dying in the usual place, in
    a new place, and with no tolerance at all."""
    rng = rng or np.random.default_rng(0)
    ld = lethal * np.exp(spread * rng.standard_normal(n))
    die = lambda tol: float((dose - tol > ld).mean())  # noqa: E731
    return {"usual": die(tolerance_usual), "new": die(tolerance_new), "none": die(0.0)}


# ----------------------------------------------------------------------------------------- chronotype
def midsleep(bed: float, wake: float) -> float:
    """The midpoint of sleep on the 24-hour clock, from the time of falling asleep and the time of waking."""
    dur = (wake - bed) % 24.0
    return (bed + dur / 2.0) % 24.0


def social_jetlag(bed_work: float, wake_work: float, bed_free: float, wake_free: float) -> float:
    """The difference, in hours, between the midpoint of sleep on free days and on work days."""
    d = midsleep(bed_free, wake_free) - midsleep(bed_work, wake_work)
    return (d + 12.0) % 24.0 - 12.0
