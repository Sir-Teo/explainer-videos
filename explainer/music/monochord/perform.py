"""Monochord's performer (Part 43 of *Music, Built*): what a player adds to the notes, in milliseconds.

A score is a list of notes ``(key number, onset in beats, length in beats)`` with phrase boundaries; a performance is
the same notes with onsets and lengths in seconds and a velocity each.

    deadpan(score, bpm)              the score played exactly as written
    RULES                            performance rules after the KTH rule system (Friberg, Bresin and Sundberg 2006):
                                     phrase arch, duration contrast, high loud, punctuation, final ritardando
    perform(score, rules, k)         apply rules with strength k; returns the performance and each rule's share
    ritardando(x, w, q)              Friberg and Sundberg's (1999) kinematic final ritardando: tempo against score
                                     position x for a final tempo w and curvature q (q = 2: constant braking force)
    vibrato_tone(f0, rate, cents)    a bowed-string tone with vibrato (Part 41's measured spectrum)
    phase_correction(alpha, ...)     a linear phase-correction ensemble (Vorberg and Wing 1996): asynchronies under
                                     timekeeper and motor noise; the stability bound 0 < sum of alphas < 2
    asynchrony_variance(alpha, s)    the stationary variance of a duo's asynchrony, in closed form
    pianist(seed)                    a model pianist: its own weights for the rules and its own timing noise
    tempo_curve(perf)                beat-level tempo (inter-onset intervals), normalised: what Cook and Sapp compared
    identify(curves, query)          correlate a query's tempo curve with every candidate's (the Hatto test)

No manim here.  Checked in ``tests/music/test_perform.py``.
"""

from __future__ import annotations

import numpy as np

from .audio import SR


# --------------------------------------------------------------------------------------------- scores
def tune_score(phrases: int = 6, base: int = 60):
    """The Tune as a score: (key, onset, length) and the phrase each note belongs to."""
    from . import tune as T
    notes, ph, a = [], [], 0.0
    major = {1: 0, 2: 2, 3: 4, 4: 5, 5: 7, 6: 9, 7: 11}
    for p, phrase in enumerate(T.PHRASES[:phrases]):
        for deg, beats in phrase:
            notes.append((base + major[deg], a, float(beats)))
            ph.append(p)
            a += beats
    return notes, ph


def deadpan(score, bpm: float = 100.0, velocity: float = 0.6):
    beat = 60.0 / bpm
    return [{"key": m, "t": a * beat, "dur": d * beat, "vel": velocity} for m, a, d in score]


# --------------------------------------------------------------------------------------------- rules
def _phrase_pos(phrases):
    """Each note's position within its phrase, 0 at the first note and 1 at the last."""
    out = []
    for i, p in enumerate(phrases):
        idx = [j for j, q in enumerate(phrases) if q == p]
        n = len(idx)
        out.append(idx.index(i) / (n - 1) if n > 1 else 0.0)
    return np.array(out)


def rule_phrase_arch(score, phrases):
    """Tempo and loudness rise towards the middle of each phrase and fall at its ends: the note's length is
    stretched by up to 1 at the boundaries and by 0 in the middle (a parabola), and its velocity follows the
    inverse."""
    x = _phrase_pos(phrases)
    shape = (2 * x - 1) ** 2                        # 1 at the ends, 0 in the middle
    return {"stretch": 0.18 * shape, "vel": -0.18 * shape}


def rule_duration_contrast(score, phrases):
    """Short notes shorter, long notes longer (in relative length), as the KTH rule does."""
    d = np.array([n[2] for n in score])
    rel = np.log2(d / np.median(d))
    return {"stretch": 0.08 * rel, "vel": 0.05 * rel}


def rule_high_loud(score, phrases):
    """Higher notes a little louder."""
    m = np.array([n[0] for n in score], float)
    return {"stretch": np.zeros(len(score)), "vel": 0.025 * (m - m.mean())}


def rule_punctuation(score, phrases):
    """A micro-pause after the last note of each phrase: the note is played shorter (detached), its slot kept."""
    last = np.array([i == len(phrases) - 1 or phrases[i + 1] != phrases[i] for i in range(len(phrases))])
    return {"stretch": np.zeros(len(score)), "vel": np.zeros(len(score)), "detach": 0.35 * last}


def ritardando(x, w: float = 0.6, q: float = 2.0):
    """Friberg and Sundberg (1999): tempo v(x) = [1 + (w^q - 1) x]^(1/q) for score position x from 0 to 1 within the
    ritardando, falling from 1 to the final tempo w.  q = 1 is a linear fall in tempo; q = 2 matches a runner stopping
    with constant braking force (tempo squared falls linearly, as speed squared does with distance); q = 3 is steeper
    at the end."""
    x = np.clip(np.asarray(x, float), 0, 1)
    return (1 + (w ** q - 1) * x) ** (1.0 / q)


def rule_final_ritardando(score, phrases, span_beats: float = 4.0, w: float = 0.55, q: float = 2.0):
    """The last ``span_beats`` beats slow down along the kinematic curve: each note's length is divided by the tempo
    at its middle."""
    end = max(a + d for _, a, d in score)
    st = []
    for _, a, d in score:
        mid = a + d / 2
        x = (mid - (end - span_beats)) / span_beats
        st.append(1.0 / ritardando(x, w, q) - 1.0 if x > 0 else 0.0)
    return {"stretch": np.array(st), "vel": np.zeros(len(score))}


RULES = {"phrase arch": rule_phrase_arch, "duration contrast": rule_duration_contrast, "high loud": rule_high_loud,
         "punctuation": rule_punctuation, "final ritardando": rule_final_ritardando}


def perform(score, phrases, rules=tuple(RULES), k: float = 1.0, bpm: float = 100.0, velocity: float = 0.6,
            weights=None, noise_ms: float = 0.0, rng=None) -> list[dict]:
    """Apply the rules: lengths stretched by (1 + k * sum of stretches), velocities shifted, phrase-final notes
    detached; onsets follow the stretched lengths.  ``weights`` scales each rule separately (a pianist's taste);
    ``noise_ms`` adds motor timing noise."""
    beat = 60.0 / bpm
    n = len(score)
    st, ve, de = np.zeros(n), np.zeros(n), np.zeros(n)
    for name in rules:
        r = RULES[name](score, phrases)
        w = (weights or {}).get(name, 1.0)
        st += w * r["stretch"]
        ve += w * r["vel"]
        if "detach" in r:
            de += w * r["detach"]
    lens = np.array([d for _, _, d in score]) * beat * np.maximum(1 + k * st, 0.2)
    onsets = np.concatenate([[0.0], np.cumsum(lens)[:-1]])
    # rests in the score are kept in proportion
    gaps = [score[i + 1][1] - (score[i][1] + score[i][2]) for i in range(n - 1)]
    onsets = onsets + np.concatenate([[0.0], np.cumsum(np.array(gaps) * beat)])
    if noise_ms:
        rng = rng or np.random.default_rng(0)
        onsets = onsets + rng.normal(0, noise_ms / 1000.0, n)
        onsets -= onsets[0]
    vel = np.clip(velocity + k * ve, 0.15, 1.0)
    return [{"key": score[i][0], "t": float(onsets[i]), "dur": float(lens[i] * (1 - k * de[i])), "vel": float(vel[i])} for i in range(n)]


def deviations(perf, score, bpm: float = 100.0):
    """Each note's length relative to the deadpan length (1 = as written), and its velocity."""
    beat = 60.0 / bpm
    ioi = [perf[i + 1]["t"] - perf[i]["t"] for i in range(len(perf) - 1)] + [perf[-1]["dur"]]
    return [float(x / (d * beat)) for x, (_, _, d) in zip(ioi, score)], [p["vel"] for p in perf]


# --------------------------------------------------------------------------------------------- vibrato
def vibrato_tone(f0: float, seconds: float = 2.0, rate: float = 5.5, cents: float = 0.0, onset: float = 0.25,
                 sr: int = SR) -> np.ndarray:
    """A bowed-string tone (Part 41's spectrum measured on Part 7's bowed string) whose pitch swings ``cents`` either
    side of f0 at ``rate`` Hz, the vibrato fading in over ``onset`` seconds."""
    from .orchestra import levels
    n = int(seconds * sr)
    t = np.arange(n) / sr
    dev = cents * np.sin(2 * np.pi * rate * t) * np.clip(t / onset, 0, 1)
    f = f0 * 2 ** (dev / 1200.0)
    ph = 2 * np.pi * np.cumsum(f) / sr
    lv = levels("violin")
    y = sum(lv[k] * np.sin((k + 1) * ph) for k in range(12) if (k + 1) * f0 < 0.45 * sr)
    env = np.clip(t / 0.08, 0, 1) * np.clip((seconds - t) / 0.12, 0, 1)
    return y * env / np.abs(y * env).max()


# --------------------------------------------------------------------------------------------- ensembles
def phase_correction(alpha, n: int = 64, period: float = 0.5, timer_sd: float = 0.012, motor_sd: float = 0.005,
                     rng=None, start_offset=None) -> dict:
    """Players i = 0..P-1 each keep time with their own timekeeper (period plus noise) and correct each onset by
    alpha[i][j] times the last asynchrony with player j (Vorberg and Wing 1996; Wing, Endo, Bradbury and Vorberg
    2014).  ``alpha`` may be a number (a duo with equal correction), a list (each player's total correction, shared
    equally among the others) or a full matrix.  ``period`` may differ from player to player (their own tempos).
    Returns onsets (n x P) and asynchronies to player 0."""
    rng = rng or np.random.default_rng(0)
    A = np.atleast_1d(np.asarray(alpha, float))
    if A.ndim == 1:
        P = 2 if A.size == 1 else A.size
        tot = np.repeat(A, 2) if A.size == 1 else A
        M = np.zeros((P, P))
        for i in range(P):
            for j in range(P):
                if i != j:
                    M[i, j] = tot[i] / (P - 1)
    else:
        M, P = A, A.shape[0]
    on = np.zeros((n, P))
    on[0] = 0.0 if start_offset is None else np.asarray(start_offset, float)
    motor_prev = rng.normal(0, motor_sd, P)
    for k in range(1, n):
        motor = rng.normal(0, motor_sd, P)
        T = np.asarray(period, float) + rng.normal(0, timer_sd, P)
        for i in range(P):
            corr = sum(M[i, j] * (on[k - 1, i] - on[k - 1, j]) for j in range(P) if j != i)
            on[k, i] = on[k - 1, i] + T[i] - corr + motor[i] - motor_prev[i]
        motor_prev = motor
    asy = on - on[:, [0]]
    return {"onsets": on, "asynchrony": asy, "M": M}


def asynchrony_variance(alpha_total: float, timer_sd: float = 0.012, motor_sd: float = 0.005) -> float:
    """For a duo whose total correction is a = alpha1 + alpha2, the asynchrony follows
    A[k+1] = (1 - a) A[k] + (T1 - T2) + (M1[k+1] - M1[k]) - (M2[k+1] - M2[k]);  its stationary variance is
    2 s_T^2 / (1 - b^2) + 4 s_M^2 / (1 + b) with b = 1 - a, finite only for 0 < a < 2."""
    a = alpha_total
    if not 0 < a < 2:
        return float("inf")
    b = 1 - a
    # A = b A_prev + e, e = (T1 - T2) + (dM1 - dM2): an ARMA(1,1) in the motor part.
    # Var of white part: 2 sT^2 / (1 - b^2).  Motor part: x = b x_prev + u - u_prev with u = M1 - M2, var(u) = 2 sM^2:
    # var(x) = var(u) * (1 + 1 - 2 b) / (1 - b^2) = 2 sM^2 * 2 (1 - b) / (1 - b^2) = 4 sM^2 / (1 + b).
    return float(2 * timer_sd ** 2 / (1 - b * b) + 4 * motor_sd ** 2 / (1 + b))


# --------------------------------------------------------------------------------------------- identity
def pianist(seed: int) -> dict:
    """A model pianist: weights for each rule drawn around 1, a tempo, a ritardando depth and personal timing noise
    that repeats from one performance to the next (a habit) plus noise that does not."""
    rng = np.random.default_rng(seed)
    return {"weights": {k: float(rng.uniform(0.3, 1.8)) for k in RULES}, "bpm": float(rng.uniform(84, 112)),
            "habit": rng.normal(0, 0.12, 400), "noise": float(rng.uniform(0.03, 0.05)), "seed": seed}


def play(p: dict, score, phrases, take: int = 0, stretch: float = 1.0) -> list[dict]:
    """One recording by pianist p: the rules with p's weights, p's habits, fresh noise for this take; ``stretch``
    time-scales the recording (what an engineer's time-stretch does)."""
    rng = np.random.default_rng(1000 * p["seed"] + take)
    perf = perform(score, phrases, weights=p["weights"], bpm=p["bpm"])
    n = len(perf)
    lens = np.array([perf[i + 1]["t"] - perf[i]["t"] for i in range(n - 1)] + [perf[-1]["dur"]])
    lens = lens * np.exp(p["habit"][:n] + rng.normal(0, p["noise"], n))
    on = np.concatenate([[0.0], np.cumsum(lens)[:-1]]) * stretch
    return [{**perf[i], "t": float(on[i]), "dur": float(perf[i]["dur"] * stretch)} for i in range(n)]


def tempo_curve(perf) -> np.ndarray:
    """Log inter-onset intervals, centred and scaled: the shape of a performance's timing, whatever its tempo."""
    t = np.array([p["t"] for p in perf])
    ioi = np.log(np.diff(t))
    return (ioi - ioi.mean()) / (ioi.std() + 1e-12)


def identify(curves: dict, query) -> list[tuple[str, float]]:
    """Correlation of the query's tempo curve with each candidate's, best first."""
    q = np.asarray(query)
    out = [(k, float(np.corrcoef(q, np.asarray(c))[0, 1])) for k, c in curves.items()]
    return sorted(out, key=lambda kv: -kv[1])
