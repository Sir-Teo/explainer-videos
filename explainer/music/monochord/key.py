"""Monochord's keys (Part 15, *Key*).

A key is a home note and a scale, and, in a listener, a ranking of the twelve notes by how well they fit.  This
module holds the published rankings, finds the key of a piece of music from its notes, and maps the twenty-four
keys by how alike they are.

    KK_MAJOR, KK_MINOR                 Krumhansl and Kessler's probe-tone profiles (1982)
    TEMPERLEY_MAJOR, TEMPERLEY_MINOR   Temperley's profiles from the Kostka-Payne corpus (2007)
    distribution(pitches, beats)       how much of the time each of the twelve notes sounds
    find_key(dist, profiles)           Krumhansl and Schmuckler's key finder: the best of 24 correlations
    bayes_key(pitches, profiles)       the key that makes the notes most probable
    learn_profiles(tunes)              profiles counted from a corpus
    key_name, relative, parallel       names and relations of keys
    signature(key)                     sharps or flats in the key signature
    shared_notes(a, b)                 how many notes two keys' scales have in common
    keys_containing(pcs)               the major keys whose scale contains a set of notes
    key_correlations, torus            how alike the 24 keys' profiles are; their places on Krumhansl's torus
    track(pitches, beats, window)      the key, moment by moment

A key is ``(tonic pitch class, "major" | "minor")``.  No manim.  Checked in ``tests/music/test_key.py``.
"""

from __future__ import annotations

import numpy as np

# Krumhansl and Kessler (1982), ratings of how well each of the twelve notes fits a major and a minor key, C = 0
KK_MAJOR = np.array([6.35, 2.23, 3.48, 2.33, 4.38, 4.09, 2.52, 5.19, 2.39, 3.66, 2.29, 2.88])
KK_MINOR = np.array([6.33, 2.68, 3.52, 5.38, 2.60, 3.53, 2.54, 4.75, 3.98, 2.69, 3.34, 3.17])
# Temperley (2007): how often each scale degree is present in a segment of the Kostka-Payne corpus
TEMPERLEY_MAJOR = np.array([0.748, 0.060, 0.488, 0.082, 0.670, 0.460, 0.096, 0.715, 0.104, 0.366, 0.057, 0.400])
TEMPERLEY_MINOR = np.array([0.712, 0.084, 0.474, 0.618, 0.049, 0.460, 0.105, 0.747, 0.404, 0.067, 0.133, 0.330])
PROFILES = {"Krumhansl-Kessler": (KK_MAJOR, KK_MINOR), "Temperley": (TEMPERLEY_MAJOR, TEMPERLEY_MINOR)}

NAMES_SHARP = ("C", "C♯", "D", "D♯", "E", "F", "F♯", "G", "G♯", "A", "A♯", "B")
NAMES_FLAT = ("C", "D♭", "D", "E♭", "E", "F", "G♭", "G", "A♭", "A", "B♭", "B")
MAJOR_SCALE = (0, 2, 4, 5, 7, 9, 11)
MINOR_SCALE = (0, 2, 3, 5, 7, 8, 10)
KEYS = [(t, m) for m in ("major", "minor") for t in range(12)]


def key_name(key, short: bool = False) -> str:
    """``C major``, ``F♯ minor``: the usual spelling (flats for the keys that are written in flats)."""
    t, m = key
    flat_major, flat_minor = {1, 3, 5, 8, 10}, {0, 2, 3, 5, 7, 10}
    name = (NAMES_FLAT if t in (flat_major if m == "major" else flat_minor) else NAMES_SHARP)[t % 12]
    if short:
        return name if m == "major" else name.lower() if len(name) == 1 else name[0].lower() + name[1:]
    return f"{name} {m}"


def relative(key):
    """The key with the same notes and the other mode: C major and A minor."""
    t, m = key
    return ((t + 9) % 12, "minor") if m == "major" else ((t + 3) % 12, "major")


def parallel(key):
    """The key with the same home note and the other mode: C major and C minor."""
    return (key[0], "minor" if key[1] == "major" else "major")


def scale(key) -> tuple[int, ...]:
    t, m = key
    return tuple(sorted((t + s) % 12 for s in (MAJOR_SCALE if m == "major" else MINOR_SCALE)))


def signature(key) -> int:
    """Sharps (+) or flats (-) in the key signature: a key's place on the circle of fifths, from -6 to +6."""
    t, m = key
    t = t if m == "major" else (t + 3) % 12
    n = (7 * t) % 12
    return n if n <= 6 else n - 12


def shared_notes(a, b) -> int:
    return len(set(scale(a)) & set(scale(b)))


def fifths_apart(a, b) -> int:
    """Steps round the circle of fifths between two keys' signatures (0 to 6)."""
    d = abs(signature(a) - signature(b)) % 12
    return min(d, 12 - d)


def keys_containing(pcs) -> list:
    """The major keys whose scale contains every one of a set of notes."""
    s = {int(p) % 12 for p in pcs}
    return [(t, "major") for t in range(12) if s <= set(scale((t, "major")))]


# ---------------------------------------------------------------------------
# Finding the key
# ---------------------------------------------------------------------------
def distribution(pitches, beats=None) -> np.ndarray:
    """How much of the time each of the twelve notes sounds (by duration; by count if no durations are given)."""
    d = np.zeros(12)
    beats = [1.0] * len(pitches) if beats is None else beats
    for p, b in zip(pitches, beats):
        d[int(p) % 12] += float(b)
    return d / max(d.sum(), 1e-12)


def profile_for(key, profiles=(KK_MAJOR, KK_MINOR)) -> np.ndarray:
    t, m = key
    return np.roll(profiles[0] if m == "major" else profiles[1], t)


def correlations(dist, profiles=(KK_MAJOR, KK_MINOR)) -> dict:
    """Pearson's correlation of a distribution of notes with the profile of each of the 24 keys."""
    d = np.asarray(dist, dtype=float)
    out = {}
    for key in KEYS:
        p = profile_for(key, profiles)
        out[key] = float(np.corrcoef(d, p)[0, 1]) if d.std() > 0 else 0.0
    return out


def find_key(dist, profiles=(KK_MAJOR, KK_MINOR)) -> tuple:
    """Krumhansl and Schmuckler's algorithm: the key whose profile correlates best with the notes."""
    c = correlations(dist, profiles)
    return max(c, key=c.get)


def ranking(dist, profiles=(KK_MAJOR, KK_MINOR)) -> list:
    c = correlations(dist, profiles)
    return sorted(c.items(), key=lambda kv: -kv[1])


def bayes_scores(pitches, beats=None, profiles=(TEMPERLEY_MAJOR, TEMPERLEY_MINOR)) -> dict:
    """The log-probability of the notes under each key, taking a key's profile as the chance of each note (a
    multinomial model: the simplest of Temperley's Bayesian key finders)."""
    d = np.zeros(12)
    beats = [1.0] * len(pitches) if beats is None else beats
    for p, b in zip(pitches, beats):
        d[int(p) % 12] += float(b)
    out = {}
    for key in KEYS:
        q = profile_for(key, profiles)
        q = q / q.sum()
        out[key] = float((d * np.log(q)).sum())
    return out


def bayes_key(pitches, beats=None, profiles=(TEMPERLEY_MAJOR, TEMPERLEY_MINOR)) -> tuple:
    s = bayes_scores(pitches, beats, profiles)
    return max(s, key=s.get)


def posterior(pitches, beats=None, profiles=(TEMPERLEY_MAJOR, TEMPERLEY_MINOR)) -> dict:
    """The probability of each key given the notes, all 24 keys equally likely beforehand."""
    s = bayes_scores(pitches, beats, profiles)
    m = max(s.values())
    w = {k: np.exp(v - m) for k, v in s.items()}
    z = sum(w.values())
    return {k: float(v / z) for k, v in w.items()}


def learn_profiles(tunes, floor: float = 0.005) -> tuple[np.ndarray, np.ndarray]:
    """Profiles counted from tunes (objects with ``pitches`` above their tonic, ``beats`` and ``mode``): the share
    of time on each note, for the major tunes and for the minor ones."""
    out = []
    for mode in ("major", "minor"):
        d = np.zeros(12)
        for m in tunes:
            if m.mode == mode:
                for p, b in zip(m.pitches, m.beats):
                    d[p % 12] += b
        out.append(d / d.sum() + floor if d.sum() else np.full(12, 1 / 12))
    return out[0], out[1]


def track(pitches, beats, window: float = 8.0, hop: float = 2.0, profiles=(KK_MAJOR, KK_MINOR)) -> list[dict]:
    """The key of each stretch of ``window`` beats, every ``hop`` beats: a piece's path from key to key."""
    on = np.concatenate([[0.0], np.cumsum(beats)])
    out, t = [], 0.0
    while t < on[-1] - 1e-9:
        d = np.zeros(12)
        for p, a, b in zip(pitches, on[:-1], on[1:]):
            overlap = min(b, t + window) - max(a, t)
            if overlap > 0:
                d[int(p) % 12] += overlap
        if d.sum() > 0:
            r = ranking(d / d.sum(), profiles)
            out.append({"t": float(t), "key": r[0][0], "r": r[0][1], "second": r[1][0]})
        t += hop
    return out


# ---------------------------------------------------------------------------
# The map of keys (Krumhansl and Kessler 1982)
# ---------------------------------------------------------------------------
def key_correlations(profiles=(KK_MAJOR, KK_MINOR)) -> np.ndarray:
    """The 24 by 24 table of correlations between the keys' profiles, in the order of ``KEYS``."""
    P = np.array([profile_for(k, profiles) for k in KEYS])
    return np.corrcoef(P)


def torus(profiles=(KK_MAJOR, KK_MINOR)) -> dict:
    """Each key's place on a torus: classical multidimensional scaling of the keys' distances into four
    dimensions gives two circles, and a key is an angle on each.  One circle is the circle of fifths; on the other,
    keys a major third apart are a third of the way round.  Returns ``{key: (theta, phi)}`` in turns (0 to 1) and
    the share of the distances' variance that the four dimensions hold."""
    C = key_correlations(profiles)
    D2 = 2.0 * (1.0 - C)                                    # squared distances between standardized profiles
    n = len(C)
    J = np.eye(n) - np.ones((n, n)) / n
    B = -0.5 * J @ D2 @ J
    w, v = np.linalg.eigh(B)
    order = np.argsort(-w)
    w, v = w[order], v[:, order]
    X = v[:, :4] * np.sqrt(np.maximum(w[:4], 0))
    out = {}
    for k, x in zip(KEYS, X):
        out[k] = (float(np.arctan2(x[1], x[0]) / (2 * np.pi)) % 1.0, float(np.arctan2(x[3], x[2]) / (2 * np.pi)) % 1.0)
    return {"angles": out, "explained": float(w[:4].sum() / w[w > 0].sum()), "eigenvalues": w[:6].tolist()}


def nearest_keys(key, profiles=(KK_MAJOR, KK_MINOR), top: int = 5) -> list:
    C = key_correlations(profiles)
    i = KEYS.index(key)
    order = np.argsort(-C[i])
    return [(KEYS[j], float(C[i, j])) for j in order if j != i][:top]
