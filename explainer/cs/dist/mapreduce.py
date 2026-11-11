"""MapReduce (Dean and Ghemawat, 2004) on simulated Pebbles (Part 39): the Job as map, shuffle and reduce, with a
master that reassigns the tasks of a crashed worker and launches backup copies of stragglers.

    r = run_job(text, workers=16, maps=64, reduces=16, crash=(worker, time), slow={worker: factor}, backup=True)
    r["top"]       the twenty most common words, ties by first appearance: identical to the one-machine Job
    r["time"]      simulated seconds; r["timeline"] every task attempt (worker, kind, start, end, outcome)

The computation is real: every map task counts the words of its split (remembering where each word first
appears), partitions its counts by a hash of the word, and every reduce task merges the partitions it is sent.  The
clock is simulated from measured rates: a Pebble counts ``cpu_rate`` bytes a second (calibrated on Part 34's run of
the Job under PebbleOS), reads its split from disk at ``disk_rate``, and sends intermediate data over ``net_mbps``.
Map output lives on the mapper's local disk, so when a worker crashes, the master re-executes not only its
in-progress tasks but also its completed map tasks whose output reducers have not yet fetched.
"""
from __future__ import annotations

import heapq
import re
import zlib

WORD = re.compile(rb"[a-z]+")


def _split(text: bytes, k: int):
    """k pieces cut at whitespace, with their offsets."""
    n = len(text)
    cuts = [0]
    for i in range(1, k):
        c = i * n // k
        while c < n and text[c:c + 1].isalpha():
            c += 1
        cuts.append(c)
    cuts.append(n)
    return [(cuts[i], text[cuts[i]:cuts[i + 1]]) for i in range(k)]


def map_task(offset: int, piece: bytes, reduces: int):
    counts, first = {}, {}
    low = piece.lower()
    for m in WORD.finditer(low):
        w = m.group()
        if w in counts:
            counts[w] += 1
        else:
            counts[w] = 1
            first[w] = offset + m.start()
    parts = [dict() for _ in range(reduces)]
    for w, c in counts.items():
        parts[zlib.crc32(w) % reduces][w] = (c, first[w])
    return parts, len(piece), sum(len(w) + 8 for w in counts)


def reduce_task(partitions):
    out = {}
    for part in partitions:
        for w, (c, f) in part.items():
            if w in out:
                oc, of = out[w]
                out[w] = (oc + c, min(of, f))
            else:
                out[w] = (c, f)
    return out


def run_job(text: bytes, workers: int = 16, maps: int = 64, reduces: int = 16, crash=None, slow=None,
            backup: bool = True, cpu_rate: float = 11.6e6, disk_rate: float = 50e6, net_mbps: float = 1000.0,
            startup: float = 0.05, top: int = 20):
    slow = slow or {}
    pieces = _split(text, maps)
    # real work, done once; the simulation only decides when and where it happens
    results = [map_task(o, p, reduces) for o, p in pieces]
    map_cost = [n / disk_rate + n / cpu_rate for _, n, _ in results]
    out_bytes = [[sum(len(w) + 8 for w in part) for part in r[0]] for r in results]
    events, k = [], 0

    def push(t, kind, data):
        nonlocal k
        k += 1
        heapq.heappush(events, (t, k, kind, data))

    alive = set(range(workers))
    idle = sorted(range(workers))
    running = {}                      # worker -> (kind, task, start, attempt id)
    map_done = {}                     # task -> worker holding its output
    map_pending = list(range(maps))
    attempts = {}
    reduce_pending = list(range(reduces))
    reduce_done = {}
    fetched = set()                   # (map task, reduce task) pairs already copied to a reducer
    timeline = []
    attempt = 0
    t = 0.0
    backups = 0
    reexec = 0
    crash_t, crash_w = (crash[1], crash[0]) if crash else (None, None)
    if crash:
        push(crash_t, "crash", crash_w)

    def speed(w):
        return slow.get(w, 1.0)

    def assign(now):
        nonlocal attempt, backups
        while idle:
            w = idle[0]
            if map_pending:
                task = map_pending.pop(0)
                kind = "map"
            elif len(map_done) == maps and reduce_pending:
                task = reduce_pending.pop(0)
                kind = "reduce"
            elif backup and (len(map_done) < maps or len(reduce_done) < reduces):
                # backup task: duplicate the oldest still-running attempt not already duplicated
                cand = [(st, kd, tk) for ww, (kd, tk, st, aid) in running.items()
                        if (kd, tk) not in attempts or attempts[(kd, tk)] < 2]
                cand = [c for c in cand if not (c[1] == "map" and c[2] in map_done)
                        and not (c[1] == "reduce" and c[2] in reduce_done)]
                if not cand:
                    break
                st, kind, task = min(cand)
                backups += 1
            else:
                break
            idle.pop(0)
            attempt += 1
            attempts[(kind, task)] = attempts.get((kind, task), 0) + 1
            if kind == "map":
                dur = startup + map_cost[task] * speed(w)
            else:
                nbytes = sum(out_bytes[m][task] for m in range(maps))
                dur = startup + nbytes * 8 / (net_mbps * 1e6) + nbytes / cpu_rate * speed(w)
            running[w] = (kind, task, now, attempt)
            push(now + dur, "done", (w, kind, task, attempt))

    assign(0.0)
    while events:
        t, _, kind, data = heapq.heappop(events)
        if kind == "crash":
            w = data
            alive.discard(w)
            if w in idle:
                idle.remove(w)
            if w in running:
                kd, tk, st, aid = running.pop(w)
                timeline.append({"worker": w, "kind": kd, "task": tk, "start": st, "end": t, "outcome": "lost"})
                if kd == "map" and tk not in map_done and tk not in map_pending:
                    map_pending.insert(0, tk)
                if kd == "reduce" and tk not in reduce_done and tk not in reduce_pending:
                    reduce_pending.insert(0, tk)
            # completed maps on the dead worker whose output some reducer still needs must run again
            for m, holder in list(map_done.items()):
                if holder == w and any((m, r) not in fetched for r in range(reduces)):
                    del map_done[m]
                    map_pending.insert(0, m)
                    reexec += 1
            assign(t)
            continue
        w, kd, tk, aid = data
        if w not in alive or running.get(w, (None, None, None, None))[3] != aid:
            continue
        st = running.pop(w)[2]
        first = (kd == "map" and tk not in map_done) or (kd == "reduce" and tk not in reduce_done)
        timeline.append({"worker": w, "kind": kd, "task": tk, "start": st, "end": t,
                         "outcome": "done" if first else "duplicate"})
        if kd == "map" and first:
            map_done[tk] = w
        elif kd == "reduce" and first:
            reduce_done[tk] = w
            for m in range(maps):
                fetched.add((m, tk))
        idle.append(w)
        idle.sort()
        assign(t)
        if len(reduce_done) == reduces:
            break
    # the real answer
    merged = {}
    for r in range(reduces):
        merged.update(reduce_task([results[m][0][r] for m in range(maps)]))
    best = sorted(merged, key=lambda w: (-merged[w][0], merged[w][1]))[:top]
    shuffle = sum(sum(b) for b in out_bytes)
    return {"top": [(w.decode(), merged[w][0]) for w in best], "time": t, "timeline": timeline,
            "maps": maps, "reduces": reduces, "workers": workers, "backups": backups, "reexecuted": reexec,
            "shuffle_bytes": shuffle, "input_bytes": len(text), "distinct": len(merged),
            "map_seconds": sum(map_cost), "crash": crash, "slow": slow}
