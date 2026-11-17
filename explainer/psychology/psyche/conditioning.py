"""Psyche learns: conditioning (Part 16 of *Psychology, Built*).

Rescorla and Wagner's rule, written for any design given as phases of trial types ("A+", "AX-"), with its asymptote
solved exactly (so the contingency ΔP falls out of it); Mackintosh's and Pearce and Hall's attention rules; a
two-memory model of extinction in which what is learned second is bound to its context (renewal and spontaneous
recovery); a law-of-effect learner in Thorndike's puzzle box; shaping by successive approximation; an operant chamber
running the four basic schedules of reinforcement, with cumulative records; concurrent variable-interval schedules
chosen by melioration, which ends at Herrnstein's matching law, and a choice where melioration is a trap; and scalar
timing with the acquisition rule of rate-estimation theory.

The equations are in the docstrings.  Parameters are chosen to make the classic designs legible, not fitted to an
animal; Part 16's scenes say which numbers are published and which are Psyche's.
"""

from __future__ import annotations

import re
from dataclasses import dataclass

import numpy as np


# ============================================================================================== designs
@dataclass(frozen=True)
class TrialType:
    """One kind of trial: the cues present and the outcome's magnitude (λ; 0 for none)."""

    cues: str
    us: float


def parse(spec: str) -> list[TrialType]:
    """``"A+ AX-"`` → two trial types.  A trailing ``+`` is an outcome of 1, ``-`` none, ``+0.5`` a magnitude."""
    out = []
    for tok in spec.split():
        m = re.fullmatch(r"([A-Za-z]+)([+-])([0-9.]*)", tok)
        if not m:
            raise ValueError(f"cannot read trial type {tok!r}")
        cues, sign, mag = m.groups()
        out.append(TrialType(cues, (float(mag) if mag else 1.0) if sign == "+" else 0.0))
    return out


def sequence(phases, rng=None) -> list[TrialType]:
    """Phases are ``(spec, n)``: n trials cycling through the spec's types in order (or shuffled, given a
    generator), so ``("A+ AX-", 100)`` is fifty of each."""
    seq = []
    for spec, n in phases:
        types = parse(spec)
        block = [types[k % len(types)] for k in range(n)]
        if rng is not None:
            rng.shuffle(block)
        seq += block
    return seq


def cue_names(seq) -> str:
    names = []
    for t in seq:
        for c in t.cues:
            if c not in names:
                names.append(c)
    return "".join(sorted(names))


# ============================================================================================== Rescorla-Wagner
def rescorla_wagner(seq, alpha=0.3, beta=(0.5, 0.5), cues: str | None = None):
    """ΔV_i = α_i β (λ − Σ_{j present} V_j) for every cue i present on the trial; β = beta[0] when the outcome
    occurs and beta[1] when it does not.  This is gradient descent on ½(λ − ΣV)² with step α_i β.

    ``alpha`` is a number or a mapping from cue to salience.  Returns ``(cues, V)`` with V of shape
    (trials + 1, cues): the strengths before the first trial and after each one."""
    cues = cues or cue_names(seq)
    idx = {c: k for k, c in enumerate(cues)}
    a = np.array([alpha.get(c, 0.3) if isinstance(alpha, dict) else alpha for c in cues], float)
    V = np.zeros((len(seq) + 1, len(cues)))
    for n, t in enumerate(seq):
        v = V[n].copy()
        x = np.zeros(len(cues))
        for c in t.cues:
            x[idx[c]] = 1.0
        err = t.us - x @ v
        b = beta[0] if t.us > 0 else beta[1]
        v += a * b * err * x
        V[n + 1] = v
    return cues, V


def rw_gradient(v, x, lam):
    """The gradient of the squared error ½(λ − x·v)² with respect to v: −(λ − x·v) x."""
    return -(lam - x @ v) * x


def rw_asymptote(types, alpha=None, beta=(1.0, 1.0)):
    """Where Rescorla-Wagner settles when trial types recur at random.  ``types`` are ``(cues, freq, p)``: how often
    each configuration occurs and the probability of the outcome on it.  The expected change is zero when

        Σ_k f_k x_k [p_k β₁ (1 − x_k·V) − (1 − p_k) β₀ x_k·V] = 0,

    a linear system (α only scales each row, so it drops out).  Returns ``(cues, V)``."""
    cues = "".join(sorted({c for cs, _, _ in types for c in cs}))
    idx = {c: k for k, c in enumerate(cues)}
    A = np.zeros((len(cues), len(cues)))
    b = np.zeros(len(cues))
    for cs, f, p in types:
        x = np.zeros(len(cues))
        for c in cs:
            x[idx[c]] = 1.0
        w = f * (p * beta[0] + (1 - p) * beta[1])
        A += w * np.outer(x, x)
        b += f * p * beta[0] * x
    return cues, np.linalg.lstsq(A, b, rcond=None)[0]


def delta_p(p_cs, p_no):
    """The contingency: P(outcome | cue) − P(outcome | no cue)."""
    return p_cs - p_no


def contingency_learning(p_cs, p_no, n=200, rng=None, alpha=0.15, beta=(1.0, 1.0), share_cs=0.5):
    """A cue X shown on a share of trials, the context C on all of them; outcomes drawn with the two probabilities.
    Returns V_X after each trial (Rescorla-Wagner with the context as a competing cue)."""
    rng = rng or np.random.default_rng(0)
    seq = []
    for _ in range(n):
        cs = rng.random() < share_cs
        us = rng.random() < (p_cs if cs else p_no)
        seq.append(TrialType("CX" if cs else "C", 1.0 if us else 0.0))
    cues, V = rescorla_wagner(seq, alpha=alpha, beta=beta, cues="CX")
    return V[:, 1]


def suppression_ratio(v, k=8.0):
    """A conditioned-suppression read-out: responding during the CS falls as exp(−kV), so the ratio
    A/(A + B) = e^{−kV}/(1 + e^{−kV}); 0.5 is no fear, 0 complete suppression (Psyche's mapping)."""
    e = np.exp(-k * np.maximum(np.asarray(v, float), 0.0))
    return e / (1 + e)


# Rescorla (1968), Experiment 2: shock probability per 2-min interval with the tone, and without it.
RESCORLA_1968_GROUPS = ((0.4, 0.4), (0.2, 0.2), (0.1, 0.1), (0.0, 0.0), (0.4, 0.2), (0.4, 0.1), (0.4, 0.0),
                        (0.2, 0.1), (0.2, 0.0), (0.1, 0.0))


def rescorla_1968(p_cs, p_no, sessions=5, rng=None, alpha=0.12, beta=(1.0, 0.4)):
    """One rat in one group of Rescorla's Experiment 2, as Psyche: each session has 12 two-minute tones and, on
    average, four tone-free two-minute intervals between tones (an 8-min mean gap).  Every interval is a trial;
    the context is present on all of them.  Returns V_tone at the end of conditioning."""
    rng = rng or np.random.default_rng(0)
    seq = []
    for _ in range(sessions):
        for _ in range(12):
            for _ in range(rng.geometric(1 / 4)):
                seq.append(TrialType("C", float(rng.random() < p_no)))
            seq.append(TrialType("CX", float(rng.random() < p_cs)))
    cues, V = rescorla_wagner(seq, alpha=alpha, beta=beta, cues="CX")
    return V[-1, 1]


# ============================================================================================== attention
def mackintosh(seq, alpha0=0.5, theta=0.3, eta=0.2, cues=None, lo=0.05, hi=1.0):
    """Mackintosh (1975), in Le Pelley's (2004) form.  Each cue learns from its own error,
    ΔV_i = α_i θ (λ − V_i), and its associability moves toward cues that predict better than the others present:
    Δα_i = −η (|λ − V_i| − |λ − Σ_{j≠i} V_j|), kept within [lo, hi].  Returns ``(cues, V, alpha)``."""
    cues = cues or cue_names(seq)
    idx = {c: k for k, c in enumerate(cues)}
    V = np.zeros((len(seq) + 1, len(cues)))
    A = np.full((len(seq) + 1, len(cues)), float(alpha0))
    for n, t in enumerate(seq):
        v, a = V[n].copy(), A[n].copy()
        present = [idx[c] for c in t.cues]
        for i in present:
            others = sum(V[n][j] for j in present if j != i)
            a[i] = np.clip(a[i] - eta * (abs(t.us - V[n][i]) - abs(t.us - others)), lo, hi)
            v[i] += A[n][i] * theta * (t.us - V[n][i])
        V[n + 1], A[n + 1] = v, a
    return cues, V, A


def pearce_hall(seq, alpha0=0.5, gamma=0.1, s=0.5, cues=None):
    """Pearce and Hall (1980), with the summed error used for strength as in most simulations:
    ΔV_i = s α_i (λ − ΣV), and associability tracks recent surprise, α_i ← γ|λ − ΣV| + (1 − γ) α_i, for the
    cues present.  Attention goes to cues whose consequences are uncertain.  Returns ``(cues, V, alpha)``."""
    cues = cues or cue_names(seq)
    idx = {c: k for k, c in enumerate(cues)}
    V = np.zeros((len(seq) + 1, len(cues)))
    A = np.full((len(seq) + 1, len(cues)), float(alpha0))
    for n, t in enumerate(seq):
        v, a = V[n].copy(), A[n].copy()
        present = [idx[c] for c in t.cues]
        err = t.us - sum(V[n][i] for i in present)
        for i in present:
            v[i] += s * A[n][i] * err
            a[i] = gamma * abs(err) + (1 - gamma) * A[n][i]
        V[n + 1], A[n + 1] = v, a
    return cues, V, A


# ============================================================================================== extinction
def extinction_in_context(phases, alpha=0.25, similarity=0.15, tau=None):
    """Bouton's view as a two-memory model.  Acquisition writes an excitatory memory E that holds in any context;
    extinction writes inhibitory memories I_k bound to the context k it happened in.  On a test in context c,
    after a delay d, the response is

        R = E − Σ_k s(c, k) e^{−d/τ} I_k,       s = 1 for the same context, ``similarity`` otherwise,

    so the time since extinction acts like a change of context (spontaneous recovery).  ``phases`` are
    ``(context, us, n)`` for training and ``("test", context, delay)`` for a probe; returns the probes' R and the
    trial-by-trial R during training.  Learning: δ = λ − R in the current context; δ > 0 grows E, δ < 0 grows the
    current context's I."""
    E, I = 0.0, {}
    probes, curve = [], []

    def respond(ctx, delay=0.0):
        decay = 1.0 if not tau else np.exp(-delay / tau)
        return E - sum((1.0 if k == ctx else similarity) * decay * v for k, v in I.items())

    for ph in phases:
        if ph[0] == "test":
            probes.append(respond(ph[1], ph[2]))
            continue
        ctx, us, n = ph
        for _ in range(n):
            r = respond(ctx)
            curve.append(r)
            d = us - r
            if d > 0:
                E += alpha * d
            else:
                I[ctx] = I.get(ctx, 0.0) - alpha * d
    return np.array(probes), np.array(curve)


def renewal(design="ABA", n_acq=20, n_ext=40, **kw):
    """The response at test for the three renewal designs (and AAA, extinction without a change)."""
    a, e, t = design
    probes, _ = extinction_in_context([(a, 1.0, n_acq), (e, 0.0, n_ext), ("test", t, 0.0)], **kw)
    return float(probes[0])


def generalization(f, f0=1000.0, width=0.35):
    """A generalization gradient over tone frequency: responding falls as a Gaussian in log frequency
    (octaves), the shape Pavlov's laboratory and many since describe (Psyche's width)."""
    return np.exp(-0.5 * (np.log2(np.asarray(f, float) / f0) / width) ** 2)


# ============================================================================================== operant
def puzzle_box(trials=24, actions=12, lr=0.1, rng=None, seconds_per_try=4.0):
    """A cat in Thorndike's box, as a law-of-effect learner: each try picks one of ``actions`` acts with
    probability proportional to e^{w}; the one act that opens the door gets Δw = lr when it does ("stamped in"),
    and the acts tried before it on that trial lose a little (Δw = −lr/10).  Returns the seconds to escape on
    each trial."""
    rng = rng or np.random.default_rng(0)
    w = np.zeros(actions)
    out = []
    for _ in range(trials):
        tries = 0
        tried = []
        while True:
            p = np.exp(w - w.max())
            p /= p.sum()
            k = rng.choice(actions, p=p)
            tries += 1
            if k == 0:
                break
            tried.append(k)
        w[0] += lr
        for k in tried:
            w[k] -= lr / 10
        out.append(tries * seconds_per_try)
    return np.array(out)


def shaping(trials=300, target=3.0, sd=1.0, lr=0.15, rng=None, successive=True, window=20, quantile=0.6):
    """A response with a continuous form (how high a rat rears, say) drawn from N(μ, sd²).  A reinforced response
    pulls μ toward itself, Δμ = lr (h − μ).  With ``successive`` the criterion is the ``quantile`` of the last
    ``window`` responses, never above ``target``: successive approximation.  Without it, only responses beyond the
    target are reinforced.  Returns μ after each trial and the share of trials reinforced."""
    rng = rng or np.random.default_rng(0)
    mu, hist, mus, hits = 0.0, [], [], 0
    for _ in range(trials):
        h = rng.normal(mu, sd)
        crit = min(target, np.quantile(hist[-window:], quantile)) if successive and len(hist) >= 5 else target
        if h > crit:
            mu += lr * (h - mu)
            hits += 1
        hist.append(h)
        mus.append(mu)
    return np.array(mus), hits / trials


def schedule(kind: str, value: float, duration=1800.0, rng=None, dt=0.25, run_rate=2.0):
    """An operant chamber running one of the four basic schedules, with a model animal whose behaviour has the
    textbook signatures (Ferster and Skinner 1957):

    * FR n: a pause after each reinforcer that grows with n (mean 0.4 s per required response), then a run at
      ``run_rate``: break and run.
    * VR n: the same requirement on average; a brief pause, then a steady high rate.
    * FI t: responding starts at a break point drawn from N(0.6 t, (0.15 t)²), the scalar property, and runs
      until the reinforcer; averaged over intervals, the scallop.
    * VI t: a steady moderate rate set by the obtained rate of reinforcement, B = k R/(R + R_e) (Herrnstein's
      hyperbola, k = 1.6/s, R_e = 1/min); reinforcers arm at random with mean t and wait to be collected.

    Returns ``(response_times, reinforcer_times)``."""
    rng = rng or np.random.default_rng(0)
    t, last = 0.0, 0.0
    resp, rf = [], []
    count = 0
    need = value if kind == "FR" else max(1, rng.geometric(1 / value)) if kind == "VR" else 0
    pause = rng.gamma(4, 0.1 * value) if kind == "FR" else rng.exponential(1.0) if kind == "VR" else 0.0
    brk = max(0.0, rng.normal(0.6 * value, 0.15 * value)) if kind == "FI" else 0.0
    armed_at = rng.exponential(value) if kind == "VI" else None
    vi_rate = 1.6 * (1 / value) / (1 / value + 1 / 60) if kind == "VI" else None
    while t < duration:
        since = t - last
        if kind in ("FR", "VR"):
            p = run_rate * dt if since > pause else 0.0
        elif kind == "FI":
            p = run_rate * dt if since > brk else 0.02 * dt
        else:
            p = vi_rate * dt
        if rng.random() < p:
            resp.append(t)
            count += 1
            hit = False
            if kind in ("FR", "VR"):
                hit = count >= need
            elif kind == "FI":
                hit = since >= value
            else:
                hit = t >= armed_at
            if hit:
                rf.append(t)
                last, count = t, 0
                if kind == "FR":
                    pause = rng.gamma(4, 0.1 * value)
                elif kind == "VR":
                    need, pause = max(1, rng.geometric(1 / value)), rng.exponential(1.0)
                elif kind == "FI":
                    brk = max(0.0, rng.normal(0.6 * value, 0.15 * value))
                else:
                    armed_at = t + rng.exponential(value)
        t += dt
    return np.array(resp), np.array(rf)


def cumulative(resp, duration, step=1.0):
    """The cumulative record: responses so far, sampled every ``step`` seconds."""
    grid = np.arange(0, duration + step, step)
    return grid, np.searchsorted(np.sort(resp), grid, side="right")


# ============================================================================================== choice
def concurrent(kind=("VI", "VI"), means=(30.0, 90.0), minutes=600, rng=None, eta=0.5, tau=200.0, explore=0.03,
               rate=1.0):
    """Two keys, each on its own schedule (VI with a mean interval in seconds, or VR with a mean ratio), and a
    meliorating chooser: every second it responds (with probability ``rate``) on the left with probability p,
    keeps exponentially weighted local rates (reinforcers per response, time constant ``tau`` responses) for each
    key, and moves p toward the richer one, Δp = η (r_L − r_R) p (1 − p), with a floor of ``explore``.  Returns
    responses and reinforcers on each key over the second half of the session."""
    rng = rng or np.random.default_rng(0)
    p = 0.5
    loc = np.array([0.02, 0.02])
    armed = [False, False]
    arm_t = [rng.exponential(m) if k == "VI" else 0 for k, m in zip(kind, means)]
    B = np.zeros(2)
    R = np.zeros(2)
    T = int(minutes * 60)
    for t in range(T):
        for s in (0, 1):
            if kind[s] == "VI" and not armed[s] and t >= arm_t[s]:
                armed[s] = True
        if rng.random() >= rate:
            continue
        side = 0 if rng.random() < p else 1
        if kind[side] == "VI":
            got = armed[side]
            if got:
                armed[side] = False
                arm_t[side] = t + rng.exponential(means[side])
        else:
            got = rng.random() < 1 / means[side]
        loc[side] += (float(got) - loc[side]) / tau
        if t >= T // 2:
            B[side] += 1
            R[side] += got
        p = float(np.clip(p + eta * (loc[0] - loc[1]) * p * (1 - p) * 10, explore, 1 - explore))
    return B, R


def generalized_matching(B, R):
    """Fit log(B_L/B_R) = a log(R_L/R_R) + log b by least squares over sessions; returns (a, log b).  Strict
    matching is a = 1, b = 1; undermatching a < 1."""
    x = np.log(np.asarray(R)[:, 0] / np.asarray(R)[:, 1])
    y = np.log(np.asarray(B)[:, 0] / np.asarray(B)[:, 1])
    a, c = np.polyfit(x, y, 1)
    return float(a), float(c)


def melioration_trap(trials=400, window=10, rng=None, temp=0.3, policy="meliorate"):
    """A choice where the locally better option is globally worse (after Herrnstein and Prelec).  With f the share
    of the last ``window`` choices that were B, A pays 1 + 3f and B pays 3f: A always pays one more right now, but
    every A lowers what both will pay.  A meliorator picks the option whose recent payoffs were higher (softmax with
    temperature ``temp``); a maximizer always picks B.  Returns the payoffs."""
    rng = rng or np.random.default_rng(0)
    hist = []
    pay = []
    seen = {"A": [], "B": []}
    for _ in range(trials):
        f = np.mean([h == "B" for h in hist[-window:]]) if hist else 0.5
        if policy == "maximize":
            c = "B"
        else:
            ma = np.mean(seen["A"][-5:]) if seen["A"] else 2.0
            mb = np.mean(seen["B"][-5:]) if seen["B"] else 2.0
            pa = 1 / (1 + np.exp(-(ma - mb) / temp))
            c = "A" if rng.random() < pa else "B"
        v = 1 + 3 * f if c == "A" else 3 * f
        seen[c].append(v)
        hist.append(c)
        pay.append(v)
    return np.array(pay)


# ============================================================================================== timing
def peak_curve(t, T, cv=0.2, base=0.05):
    """Responding in the peak procedure: a timed rate that peaks at the trained interval T with a spread
    proportional to T (Weber's law for time, the scalar property), on a small baseline."""
    t = np.asarray(t, float)
    return base + (1 - base) * np.exp(-0.5 * ((t - T) / (cv * T)) ** 2)


def reinforcements_to_acquisition(i_over_t, k=300.0):
    """Gallistel and Gibbon's (2000) summary of autoshaping data: reinforcements to an acquisition criterion fall
    in inverse proportion to the ratio of the intertrial interval to the CS duration, n ≈ k (I/T)⁻¹, whatever I
    and T are separately."""
    return k / np.asarray(i_over_t, float)


def rw_trials_to_criterion(i_over_t, alpha=0.1, beta=(0.5, 0.5), criterion=0.5, max_trials=5000):
    """Rescorla-Wagner with the context as a cue, where each CS-US trial is followed by I/T context-alone
    "trials" of the CS's length: the number of CS trials before V_CS reaches ``criterion``."""
    out = []
    for r in np.atleast_1d(i_over_t):
        v = np.zeros(2)  # context, CS
        carry = 0.0
        n = 0
        while v[1] < criterion and n < max_trials:
            n += 1
            err = 1.0 - v.sum()
            v += alpha * beta[0] * err * np.array([1.0, 1.0])
            carry += r
            while carry >= 1.0:
                carry -= 1.0
                v[0] += alpha * beta[1] * (0.0 - v[0])
        out.append(n)
    return np.array(out)
