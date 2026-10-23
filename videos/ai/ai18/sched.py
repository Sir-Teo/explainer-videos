"""Pipeline-parallel schedules, simulated exactly: p stages (devices), m micro-batches, integer durations.

An operation is (kind, virtual stage, micro-batch): F (forward), B (backward; with ``split`` only the gradient for
the input) and W (the gradient for the weights, with ``split``).  A virtual stage is chunk c of device s, numbered
c * p + s (interleaving gives each device v chunks; v = 1 is the plain pipeline).  Dependencies: F of a micro-batch
needs F of the previous virtual stage; B needs B of the next one (or F, at the last); W needs B.  A device runs one
operation at a time, in the order its schedule lists them (GPipe, 1F1B, interleaved 1F1B, and the zero-bubble
ZB-H1, whose W passes are deferred into the gaps).
"""

from __future__ import annotations


def _deps(op, V):
    k, g, i = op
    if k == "F":
        return [("F", g - 1, i)] if g > 0 else []
    if k == "B":
        return [("B", g + 1, i)] if g < V - 1 else [("F", g, i)]
    return [("B", g, i)]


def gpipe(p, m):
    return [[("F", s, i) for i in range(m)] + [("B", s, i) for i in range(m)] for s in range(p)]


def one_f_one_b(p, m):
    out = []
    for s in range(p):
        w = min(p - s - 1, m)
        ops = [("F", s, i) for i in range(w)]
        for i in range(m - w):
            ops += [("F", s, w + i), ("B", s, i)]
        ops += [("B", s, i) for i in range(m - w, m)]
        out.append(ops)
    return out


def interleaved(p, m, v):
    """Megatron-LM's interleaved 1F1B (Narayanan et al. 2021); m must be a multiple of p."""
    assert m % p == 0
    out = []
    n = m * v
    for s in range(p):
        def fwd(k):
            c = (k // p) % v
            return ("F", c * p + s, (k // (p * v)) * p + k % p)

        def bwd(k):
            c = v - 1 - (k // p) % v
            return ("B", c * p + s, (k // (p * v)) * p + k % p)

        w = min((p - s - 1) * 2 + (v - 1) * p, n)
        ops = [fwd(k) for k in range(w)]
        for k in range(n - w):
            ops += [fwd(w + k), bwd(k)]
        ops += [bwd(k) for k in range(n - w, n)]
        out.append(ops)
    return out


def simulate_fixed(orders, p, v, dur):
    """Run each device's list in order; an operation starts when its device is free and its inputs are ready."""
    V = p * v
    end, start = {}, {}
    free = [0] * p
    idx = [0] * p
    total = sum(len(o) for o in orders)
    done = 0
    while done < total:
        progress = False
        for s in range(p):
            if idx[s] >= len(orders[s]):
                continue
            op = orders[s][idx[s]]
            deps = _deps(op, V)
            if all(d in end for d in deps):
                t = max([free[s]] + [end[d] for d in deps])
                start[op], end[op] = t, t + dur[op[0]]
                free[s] = end[op]
                idx[s] += 1
                done += 1
                progress = True
        if not progress:
            raise RuntimeError("deadlock: the schedule's order is infeasible")
    return start, end


def zb_h1(p, m):
    """Zero Bubble's ZB-H1 (Qi et al. 2024): 1F1B with the backward pass split in two; stage s runs each weight
    gradient W s micro-batches after its input gradient B, so the W passes fill the cool-down's idle slots.  Bubble
    (p - 1)(F + B - W), a third of 1F1B's when F = B = W, at 1F1B's peak memory."""
    out = []
    for s in range(p):
        w = min(p - s - 1, m)
        ops = [("F", s, i) for i in range(w)]
        pend = []

        def back(i):
            ops.append(("B", s, i))
            pend.append(("W", s, i))
            while len(pend) > s:
                ops.append(pend.pop(0))

        for i in range(m - w):
            ops.append(("F", s, w + i))
            back(i)
        for i in range(m - w, m):
            back(i)
        out.append(ops + pend)
    return out


def stats(start, end, p, v=1):
    """Total time, the bubble (idle share of the devices' time) and the most micro-batches in flight on a device."""
    T = max(end.values())
    busy = [0] * p
    for op, e in end.items():
        busy[op[1] % p] += e - start[op]
    bubble = 1 - sum(busy) / (p * T)
    peak = []
    for s in range(p):
        evs = []
        for op in end:
            if op[1] % p != s:
                continue
            if op[0] == "F":
                evs.append((start[op], 1))
            last = "W" if any(o[0] == "W" for o in end) else "B"
            if op[0] == last:
                evs.append((end[op], -1))
        cur = mx = 0
        for _, dlt in sorted(evs, key=lambda x: (x[0], x[1])):
            cur += dlt
            mx = max(mx, cur)
        peak.append(mx / v)
    return dict(total=T, bubble=bubble, peak=peak)


def ops_list(start, end, p):
    """[(device, kind, chunk, micro-batch, start, end)] for drawing a Gantt chart."""
    return sorted([(op[1] % p, op[0], op[1] // p, op[2], start[op], end[op]) for op in end],
                  key=lambda r: (r[4], r[0]))
