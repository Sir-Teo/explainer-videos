"""Stream processing (Part 46), after the Dataflow model (Akidau et al. 2015): events with event times arriving at
processing times, late and out of order; tumbling, sliding and session windows; a heuristic watermark that trades
completeness for latency; and checkpoints by asynchronous barrier snapshots (Carbone et al. 2015) that let a keyed
counter recover from a crash with exactly-once state."""

from __future__ import annotations

import random
from collections import Counter, defaultdict


def make_events(n=3000, rate=10.0, delay_mean=2.0, late_share=0.05, late_extra=(20.0, 60.0), dup=0.01,
                seed=0, keys=None):
    """Events every 1/rate seconds of event time; each arrives after a random network delay (exponential), a few
    much later (a phone offline), and some twice.  Returns (event_time, arrival_time, key, id) sorted by
    arrival."""
    rng = random.Random(seed)
    keys = keys or ["a", "b", "c"]
    ev = []
    for i in range(n):
        et = i / rate
        d = rng.expovariate(1 / delay_mean)
        if rng.random() < late_share:
            d += rng.uniform(*late_extra)
        k = keys[i] if isinstance(keys, list) and len(keys) == n else rng.choice(keys)
        ev.append((et, et + d, k, i))
        if rng.random() < dup:
            ev.append((et, et + d + rng.expovariate(1.0), k, i))
    ev.sort(key=lambda e: e[1])
    return ev


def tumbling(et, size):
    if size <= 0:
        raise ValueError("window size must be positive")
    s = int(et // size) * size
    return [(s, s + size)]


def sliding(et, size, step):
    if size <= 0 or step <= 0:
        raise ValueError("window size and slide step must be positive")
    out = []
    s = int(et // step) * step
    while s > et - size:
        out.append((s, s + size))
        s -= step
    return out


def sessions(times, gap):
    """Merge events closer than gap into sessions."""
    out = []
    for t in sorted(times):
        if out and t - out[-1][1] < gap:
            out[-1][1] = t
        else:
            out.append([t, t])
    return [(a, b + gap) for a, b in out]


def run_windows(events, size=10.0, watermark_lag=5.0, allowed_late=0.0, dedup=True):
    """Count events per (window, key).  The watermark at any moment is (max event time seen) - watermark_lag; a
    window fires when the watermark passes its end, and events arriving after that (beyond allowed lateness) are
    dropped.  Returns fired results with their latency (processing time of firing minus window end), the true
    counts, and how many were dropped."""
    if size <= 0 or watermark_lag < 0 or allowed_late < 0:
        raise ValueError("window size must be positive and lateness parameters nonnegative")
    counts = defaultdict(Counter)
    truth = defaultdict(Counter)
    seen = set()
    fired = {}
    dropped = refinements = 0
    max_et = float("-inf")
    for et, at, k, i in events:
        if (i, k) in seen and dedup:
            continue
        seen.add((i, k))
        w = tumbling(et, size)[0]
        truth[w][k] += 1
        max_et = max(max_et, et)
        wm = max_et - watermark_lag
        if wm >= w[1] + allowed_late:
            dropped += 1
        else:
            counts[w][k] += 1
            if w in fired:                  # a late event within the allowed lateness: fire a refinement
                fired[w] = (fired[w][0], dict(counts[w]))
                refinements += 1
        for w2 in list(counts):
            if w2 not in fired and wm >= w2[1]:
                fired[w2] = (at, dict(counts[w2]))
    last = events[-1][1] if events else 0.0
    for w2 in counts:                       # end of stream: the watermark jumps to infinity
        if w2 not in fired:
            fired[w2] = (last, dict(counts[w2]))
    lat = [at - w[1] for w, (at, _) in fired.items()]
    exact = sum(1 for w, (_, c) in fired.items() if c == dict(truth[w]))
    total = sum(sum(c.values()) for c in truth.values())
    return {"windows": len(fired), "exact": exact, "dropped": dropped, "mean_latency": sum(lat) / max(1, len(lat)),
            "lag": watermark_lag, "complete": 1 - dropped / total if total else 1.0, "refinements": refinements}


def watermark_tradeoff(lags=(0.0, 1.0, 2.0, 5.0, 10.0, 20.0, 60.0), seed=0):
    ev = make_events(seed=seed)
    return [run_windows(ev, watermark_lag=lg) for lg in lags]


def plot_points(n=120, seed=1):
    """A small stream for the event-time / processing-time plot, with the watermark curve."""
    ev = make_events(n=n, rate=2.0, delay_mean=1.5, late_share=0.05, late_extra=(8.0, 15.0), dup=0.0, seed=seed)
    pts = [(et, at) for et, at, _, _ in ev]
    wm, mx = [], float("-inf")
    for et, at in sorted(pts, key=lambda p: p[1]):
        mx = max(mx, et)
        wm.append((at, mx - 3.0))
    return {"points": pts, "watermark": wm, "lag": 3.0}


# ---------------------------------------------------------------- checkpoints

def barrier_snapshot(events, workers=3, checkpoint_every=500, crash_at=1700, seed=0):
    """A keyed counter split across workers (key hash).  A source injects a barrier every checkpoint_every events;
    each worker snapshots its state when the barrier reaches it, and the source records its offset.  At crash_at all
    workers lose their state; recovery restores the last complete snapshot and replays the source from its offset.
    Returns final counts and whether they equal a failure-free run, with and without the checkpoint protocol (the
    naive version restarts from the beginning but keeps an output sink that already received some counts)."""
    def worker_of(k):
        return hash(k) % workers
    clean = Counter(k for _, _, k, _ in events)
    state = [Counter() for _ in range(workers)]
    snap_state, snap_offset = [Counter() for _ in range(workers)], 0
    i = 0
    crashed = False
    restored_from = 0
    while i < len(events):
        if i and i % checkpoint_every == 0 and snap_offset != i:
            snap_state = [Counter(s) for s in state]       # all workers have seen the barrier: snapshot complete
            snap_offset = i
        if i == crash_at and not crashed:
            crashed = True
            state = [Counter(s) for s in snap_state]
            restored_from = snap_offset
            i = snap_offset
            continue
        _, _, k, _ = events[i]
        state[worker_of(k)][k] += 1
        i += 1
    final = Counter()
    for s in state:
        final.update(s)
    # without coordinated snapshots: workers keep state they had at the crash, source replays from the last offset
    naive = Counter()
    for _, _, k, _ in events[:crash_at]:
        naive[k] += 1
    for _, _, k, _ in events[restored_from:]:
        naive[k] += 1
    return {"exact_with_snapshots": final == clean, "replayed": crash_at - restored_from,
            "restored_from": restored_from,
            "naive_overcount": sum(naive.values()) - sum(clean.values()), "events": len(events)}


def job_stream(text: bytes, books=30, per_book_delay=(0.0, 3.0), late_books=3, dup_books=2, seed=3,
               modes=("exactly once", "no dedup", "watermark lag 5 s")):
    """The Job as a stream: each novel's words arrive as events; some novels arrive late, two twice.  A top-20 that
    deduplicates by (book, position) and keeps all-time state converges to the batch answer; without dedup it is
    wrong; with a watermark that closes early it misses the late books."""
    rng = random.Random(seed)
    words = text.decode("latin-1").lower().split()
    n = len(words)
    per = n // books
    ev = []
    late = set(rng.sample(range(books), late_books))
    dups = set(rng.sample([b for b in range(books) if b not in late], dup_books))
    for b in range(books):
        start = b * 1.0 + (20.0 if b in late else rng.uniform(*per_book_delay))
        chunk = words[b * per:(b + 1) * per] if b < books - 1 else words[b * per:]
        ev.append((b, start, b))
        if b in dups:
            ev.append((b, start + 0.5, b))
    ev.sort(key=lambda e: e[1])
    truth = Counter(words).most_common(20)
    res = {}
    for name, dedup, lag in (("exactly once", True, None), ("no dedup", False, None),
                             ("watermark lag 5 s", True, 5.0)):
        if name not in modes:
            continue
        c = Counter()
        seen = set()
        for b, at, _ in ev:
            if dedup and b in seen:
                continue
            if lag is not None and at - b > lag:      # later than the watermark allows: dropped
                continue
            seen.add(b)
            chunk = words[b * per:(b + 1) * per] if b < books - 1 else words[b * per:]
            c.update(chunk)
        top = c.most_common(20)
        res[name] = {"top": top[:5], "matches_batch": top == truth, "total": sum(c.values())}
    return {"books": books, "late": sorted(late), "duplicated": sorted(dups), "words": n, "results": res,
            "truth": truth[:5], "arrivals": [(b, at) for b, at, _ in ev]}
