"""A language-model server, simulated with costs measured on this machine (``compute.phases``): how requests are
batched (static batches, Orca's continuous batching, Sarathi's chunked prefill, DistServe-style disaggregation), how
the key-value memory is handed out (reserved at the maximum length, contiguous, or in vLLM's pages), and how much a
shared prefix saves (SGLang's radix tree).

Everything is deterministic given its seed.  Times are in seconds of this computer's one core, running the series'
novels model; the shapes of the results, not the absolute times, are what carries over to a GPU server.
"""

from __future__ import annotations

import math
from dataclasses import dataclass, field

import numpy as np


# ---------------------------------------------------------------------------
# The cost of one engine step, fitted to the measurements
# ---------------------------------------------------------------------------
@dataclass
class Cost:
    """t(step) = a + b * (sequences decoding) + c * (cached tokens they read) + p * (prompt tokens prefilled)."""
    a: float
    b: float
    c: float
    p: float

    def step(self, n_dec: int, ctx_sum: float, n_pre: int) -> float:
        if n_dec == 0 and n_pre == 0:
            return 0.0
        return self.a + self.b * n_dec + self.c * ctx_sum + self.p * n_pre


def fit_cost(ph: dict) -> tuple[Cost, float]:
    """Least squares over every measured step (decode at several batches and contexts, prefill of several lengths),
    in relative error (each point weighted by 1/t).  Returns the model and its worst relative error."""
    rows, ts = [], []
    for B, t in zip(ph["decode_B"], ph["decode_t"]):
        rows.append([1, B, B * 128, 0])
        ts.append(t)
    for i, B in enumerate(ph["ctx_B"]):
        for j, ctx in enumerate(ph["ctxs"]):
            rows.append([1, B, B * ctx, 0])
            ts.append(ph["ctx_t"][i][j])
    for T, t in zip(ph["prefill_T"], ph["prefill_t"]):
        if T >= 8:
            rows.append([1, 0, 0, T])
            ts.append(t)
    A, y = np.array(rows, float), np.array(ts, float)
    w = 1 / y
    coef, *_ = np.linalg.lstsq(A * w[:, None], y * w, rcond=None)
    coef = np.maximum(coef, 1e-9)
    err = float(np.max(np.abs(A @ coef - y) / y))
    return Cost(*[float(v) for v in coef]), err


# ---------------------------------------------------------------------------
# The workload
# ---------------------------------------------------------------------------
@dataclass
class Req:
    rid: int
    arrive: float
    prompt: int
    out: int
    done_pre: int = 0  # prompt tokens prefilled so far
    made: int = 0  # output tokens written so far
    first: float = -1.0  # time of the first output token
    last: float = -1.0  # time of the latest output token
    finish: float = -1.0
    ready: float = -1.0  # disaggregated: when the cache reaches the decode worker
    slot: int = -1
    gaps: list = field(default_factory=list)  # times between successive output tokens

    @property
    def ctx(self):
        return self.done_pre + self.made


def workload(n=300, rate=4.0, seed=0, p_med=120, o_med=100, p_max=1024, o_max=1000):
    """``n`` requests arriving as a Poisson process at ``rate`` a second; prompt and answer lengths log-normal
    (medians ``p_med`` and ``o_med`` tokens, a long tail, capped)."""
    g = np.random.default_rng(seed)
    t = np.cumsum(g.exponential(1 / rate, n))
    p = np.clip(np.round(g.lognormal(math.log(p_med), 0.8, n)), 8, p_max).astype(int)
    o = np.clip(np.round(g.lognormal(math.log(o_med), 0.9, n)), 4, o_max).astype(int)
    return [Req(i, float(t[i]), int(p[i]), int(o[i])) for i in range(n)]


def fresh(reqs):
    return [Req(r.rid, r.arrive, r.prompt, r.out) for r in reqs]


# ---------------------------------------------------------------------------
# Batching policies
# ---------------------------------------------------------------------------
def _emit(r: Req, t: float):
    """``r`` writes a token at time ``t`` (its first, or the gap since its last)."""
    r.made += 1
    if r.first < 0:
        r.first = t
    else:
        r.gaps.append(t - r.last)
    r.last = t
    if r.made >= r.out and r.finish < 0:
        r.finish = t


def run_static(reqs, cost: Cost, bmax: int, trace: list | None = None):
    """Request-level batching (as servers did before 2022): take up to ``bmax`` waiting requests, prefill them
    together (which writes each one's first token), decode until the longest is finished (finished ones keep their
    slot, computed as padding), then take the next batch."""
    reqs = fresh(reqs)
    t, i, waiting = 0.0, 0, []
    while i < len(reqs) or waiting:
        while i < len(reqs) and reqs[i].arrive <= t:
            waiting.append(reqs[i])
            i += 1
        if not waiting:
            t = reqs[i].arrive
            continue
        batch, waiting = waiting[:bmax], waiting[bmax:]
        for k, r in enumerate(batch):
            r.slot = k
        dt = cost.step(0, 0, sum(r.prompt for r in batch))
        if trace is not None:
            trace += [(r.slot, t, t + dt, "prefill", r.rid) for r in batch]
        t0, t = t, t + dt
        for r in batch:
            r.done_pre = r.prompt
            _emit(r, t)
        while any(r.made < r.out for r in batch):
            dt = cost.step(len(batch), sum(r.ctx for r in batch), 0)  # padding: every slot computes
            t += dt
            for r in batch:
                if r.made < r.out:
                    _emit(r, t)
        if trace is not None:
            for r in batch:
                trace.append((r.slot, t0 + (r.first - t0), r.finish, "decode", r.rid))
                if r.finish < t:
                    trace.append((r.slot, r.finish, t, "idle", r.rid))
    return reqs


def run_continuous(reqs, cost: Cost, bmax: int, chunk: int = 0, trace: list | None = None, decode_only=False,
                   copy=True):
    """Iteration-level scheduling (Orca, 2022): after every step, finished requests leave and waiting ones join.
    A joining request's whole prompt is prefilled inside one step (so the decodes in that step wait for it), unless
    ``chunk`` > 0: then each step carries the decodes plus at most ``chunk`` prompt tokens (Sarathi-Serve's chunked
    prefill).  ``decode_only``: requests arrive already prefilled, their first token written (a decode worker)."""
    reqs = fresh(reqs) if copy else reqs
    order = sorted(reqs, key=lambda r: r.arrive)
    t, i = 0.0, 0
    run: list[Req] = []
    waiting: list[Req] = []
    free_slots = list(range(bmax))[::-1]
    seg = {}
    while i < len(order) or run or waiting:
        while i < len(order) and order[i].arrive <= t:
            waiting.append(order[i])
            i += 1
        while waiting and free_slots:
            r = waiting.pop(0)
            r.slot = free_slots.pop()
            run.append(r)
            seg[r.rid] = t
        if not run:
            t = order[i].arrive
            continue
        dec = [r for r in run if r.done_pre >= r.prompt]
        pre = [r for r in run if r.done_pre < r.prompt]
        budget = (chunk - len(dec)) if chunk else 10 ** 9
        take = {}
        for r in pre:  # first come, first served
            k = min(r.prompt - r.done_pre, max(budget, 0))
            if k <= 0:
                break
            take[r.rid] = k
            budget -= k
        dt = cost.step(len(dec), sum(r.ctx for r in dec), sum(take.values()))
        if trace is not None:
            for r in pre:
                if r.rid in take:
                    trace.append((r.slot, t, t + dt, "prefill", r.rid))
        t += dt
        for r in dec:
            _emit(r, t)
        for r in pre:
            if r.rid in take:
                r.done_pre += take[r.rid]
                if r.done_pre >= r.prompt:
                    _emit(r, t)  # the last prompt position's logits give the first token
        for r in list(run):
            if r.made >= r.out:
                run.remove(r)
                free_slots.append(r.slot)
                if trace is not None:
                    trace.append((r.slot, seg[r.rid], t, "decode", r.rid))
    return reqs


def run_disaggregated(reqs, cost: Cost, bmax: int, link_bytes_per_s: float, kv_per_token: float,
                      pre_batch_tokens: int = 512, n_dec: int = 1):
    """Prefill and decode on separate workers (Splitwise, DistServe, 2024): one worker prefills prompts, batched up to
    ``pre_batch_tokens``, writing each first token; each cache is then sent over a link to the decode worker, which
    only decodes, with continuous batching (``n_dec`` decode workers, requests dealt out in turn)."""
    reqs = fresh(reqs)
    order = sorted(reqs, key=lambda r: r.arrive)
    t, i, waiting = 0.0, 0, []
    while i < len(order) or waiting:
        while i < len(order) and order[i].arrive <= t:
            waiting.append(order[i])
            i += 1
        if not waiting:
            t = order[i].arrive
            continue
        batch, tok = [], 0
        while waiting and (not batch or tok + waiting[0].prompt <= pre_batch_tokens):
            r = waiting.pop(0)
            batch.append(r)
            tok += r.prompt
        t += cost.step(0, 0, tok)
        for r in batch:
            r.done_pre = r.prompt
            _emit(r, t)
            r.ready = t + r.prompt * kv_per_token / link_bytes_per_s  # the cache lands on the decode worker
    arrivals = {r.rid: r.arrive for r in reqs}
    for r in reqs:
        r.arrive = r.ready
    for j in range(n_dec):
        run_continuous([r for r in reqs if r.made < r.out and r.rid % n_dec == j], cost, bmax, copy=False)
    for r in reqs:
        r.arrive = arrivals[r.rid]
    return reqs


def split_round_robin(reqs, k):
    return [[r for r in reqs if r.rid % k == j] for j in range(k)]


def metrics(reqs, tpot_slo=None, ttft_slo=None) -> dict:
    done = [r for r in reqs if r.finish >= 0]
    ttft = np.array([r.first - r.arrive for r in done])
    gaps = np.concatenate([np.asarray(r.gaps, float) for r in done if r.gaps])
    tpot = np.array([(r.finish - r.first) / max(r.out - 1, 1) for r in done])
    span = max(r.finish for r in done) - min(r.arrive for r in done)
    out = dict(n=len(done), tokens=int(sum(r.out for r in done)), span=span,
               throughput=sum(r.out for r in done) / span,
               ttft=[float(np.percentile(ttft, q)) for q in (50, 90, 99)],
               tpot=[float(np.percentile(tpot, q)) for q in (50, 90, 99)],
               gap=[float(np.percentile(gaps, q)) for q in (50, 90, 99, 100)],
               latency=[float(np.percentile([r.finish - r.arrive for r in done], q)) for q in (50, 90, 99)])
    if tpot_slo and ttft_slo:
        ok = sum(1 for r, a, b in zip(done, ttft, tpot) if a <= ttft_slo and b <= tpot_slo)
        out["slo_share"] = ok / len(done)
        out["goodput"] = ok / span
    return out


# ---------------------------------------------------------------------------
# Key-value memory: reserved, contiguous, paged
# ---------------------------------------------------------------------------
def memory_sim(reqs, cost: Cost, pool: int, mode: str, block: int = 16, max_len: int = 2048, bmax: int = 256,
               snap_t: float | None = None):
    """Continuous batching whose admission is limited by a key-value memory of ``pool`` tokens.
    ``mode``: "reserve" (each request holds ``max_len`` tokens from the start, as servers did before vLLM);
    "contiguous" (each holds exactly its final length in one contiguous range, first fit: it must know its length,
    and free memory splinters); "paged" (blocks of ``block`` tokens anywhere in the pool, taken as the sequence
    grows; when the pool runs out the newest request is preempted and later recomputed, as vLLM does).
    Returns the requests, a time series of (t, running, tokens stored, tokens allocated), the number of preemptions,
    and a snapshot of the memory at time ``snap_t``: [(start, allocated, used, request)]."""
    reqs = fresh(reqs)
    order = sorted(reqs, key=lambda r: r.arrive)
    t, i = 0.0, 0
    run: list[Req] = []
    waiting: list[Req] = []
    held = {}  # rid -> (start, length) for reserve / contiguous; list of block ids for paged
    free_ranges = [(0, pool)]
    free_slots = list(range(pool // max_len))
    total_blocks = pool // block
    free_ids = list(range(total_blocks))
    series, preempted, snap = [], 0, None

    def alloc_contig(n):
        for k, (st, L) in enumerate(free_ranges):
            if L >= n:
                free_ranges[k] = (st + n, L - n)
                if free_ranges[k][1] == 0:
                    free_ranges.pop(k)
                return st
        return None

    def free_contig(st, n):
        free_ranges.append((st, n))
        free_ranges.sort()
        merged = []
        for a_, L in free_ranges:
            if merged and merged[-1][0] + merged[-1][1] == a_:
                merged[-1] = (merged[-1][0], merged[-1][1] + L)
            else:
                merged.append((a_, L))
        free_ranges[:] = merged

    def release(r):
        h = held.pop(r.rid)
        if mode == "contiguous":
            free_contig(*h)
        elif mode == "reserve":
            free_slots.append(h[0] // max_len)
        else:
            free_ids.extend(h)

    while i < len(order) or run or waiting:
        while i < len(order) and order[i].arrive <= t:
            waiting.append(order[i])
            i += 1
        while waiting and len(run) < bmax:  # admit, first come first served
            r = waiting[0]
            if mode == "reserve":
                if not free_slots:
                    break
                held[r.rid] = (free_slots.pop(0) * max_len, max_len)
            elif mode == "contiguous":
                st = alloc_contig(r.prompt + r.out)
                if st is None:
                    break
                held[r.rid] = (st, r.prompt + r.out)
            else:
                need = math.ceil((r.prompt + 1) / block)
                if need > len(free_ids) - len(run):  # keep a block of headroom per running sequence
                    break
                held[r.rid] = [free_ids.pop(0) for _ in range(need)]
            waiting.pop(0)
            run.append(r)
        if not run:
            if i < len(order):
                t = max(t, order[i].arrive)
                continue
            break
        dec = [r for r in run if r.done_pre >= r.prompt]
        pre = [r for r in run if r.done_pre < r.prompt]
        dt = cost.step(len(dec), sum(r.ctx for r in dec), sum(r.prompt - r.done_pre for r in pre))
        t += dt
        for r in dec:
            _emit(r, t)
        for r in pre:
            r.done_pre = r.prompt
            _emit(r, t)
        if mode == "paged":  # grow, preempting the newest when the pool is full
            for r in list(run):
                if r not in run:
                    continue
                need = math.ceil((r.ctx + 1) / block) - len(held[r.rid])
                while need > len(free_ids) and len(run) > 1:
                    victim = run[-1] if run[-1] is not r else run[-2]
                    release(victim)
                    run.remove(victim)
                    victim.done_pre, victim.made, victim.first, victim.gaps, victim.finish = 0, 0, -1.0, [], -1.0
                    waiting.insert(0, victim)
                    preempted += 1
                for _ in range(max(0, min(need, len(free_ids)))):
                    held[r.rid].append(free_ids.pop(0))
        for r in list(run):
            if r.made >= r.out:
                r.finish = t
                run.remove(r)
                release(r)
        stored = sum(r.ctx for r in run)
        alloc = (sum(len(v) for v in held.values()) * block if mode == "paged" else sum(v[1] for v in held.values()))
        series.append((t, len(run), stored, alloc))
        if snap_t is not None and snap is None and t >= snap_t:
            snap = []
            for r in run:
                h = held[r.rid]
                if mode == "paged":
                    left = r.ctx
                    for bid in h:
                        snap.append((bid * block, block, min(block, max(left, 0)), r.rid))
                        left -= block
                else:
                    snap.append((h[0], h[1], r.ctx, r.rid))
    return reqs, np.array(series), preempted, snap


def block_waste(lengths, blocks) -> list[float]:
    """Internal fragmentation of pages: the share of allocated slots left empty, for each page size."""
    L = np.asarray(lengths, float)
    return [float(1 - L.sum() / (np.ceil(L / b) * b).sum()) for b in blocks]


# ---------------------------------------------------------------------------
# Shared prefixes: cached blocks of a prompt, reused
# ---------------------------------------------------------------------------
class PrefixCache:
    """Cached prefixes in blocks of ``block`` tokens, each block keyed by everything before it and itself (a hash
    of the prefix), evicted least-recently-used: vLLM's automatic prefix caching; SGLang's radix tree does the same
    at the granularity of tokens.  ``capacity`` in tokens."""

    def __init__(self, capacity: int, block: int = 16):
        from collections import OrderedDict

        self.cap, self.block = capacity // block, block
        self.lru = OrderedDict()

    def keys(self, seq):
        out, h = [], 0
        for k in range(0, len(seq) - len(seq) % self.block, self.block):
            h = hash((h, tuple(seq[k:k + self.block])))
            out.append(h)
        return out

    def match(self, seq) -> int:
        n = 0
        for h in self.keys(seq):
            if h not in self.lru:
                break
            self.lru.move_to_end(h)
            n += self.block
        return n

    def insert(self, seq):
        for h in self.keys(seq):
            self.lru[h] = True
            self.lru.move_to_end(h)
        while len(self.lru) > self.cap:
            self.lru.popitem(last=False)


def chat_workload(n_conv=40, turns=6, system=300, user=(20, 120), answer=(40, 240), seed=0):
    """Multi-turn conversations sharing one system prompt: each turn's prompt is the system prompt, the whole
    conversation so far and the new message (token ids are unique labels: only sharing matters here)."""
    g = np.random.default_rng(seed)
    nxt = [1_000_000]

    def fresh_tokens(n):
        a = list(range(nxt[0], nxt[0] + n))
        nxt[0] += n
        return a

    sys_t = fresh_tokens(system)
    convs = []
    for c in range(n_conv):
        hist = list(sys_t)
        prompts = []
        for _ in range(turns):
            hist = hist + fresh_tokens(int(g.integers(*user)))
            prompts.append(list(hist))
            hist = hist + fresh_tokens(int(g.integers(*answer)))
        convs.append(prompts)
    # interleave the conversations: turn 1 of each, then turn 2, ... (people answer at their own pace)
    order = []
    for k in range(turns):
        for c in g.permutation(n_conv):
            order.append(convs[c][k] + [0])  # the answer will follow; its tokens are written to the cache too
    return order, sys_t


def prefix_sim(order, capacity) -> dict:
    tree = PrefixCache(capacity)
    total = computed = 0
    for seq in order:
        p = seq[:-1]
        hit = tree.match(p)
        total += len(p)
        computed += len(p) - hit
        tree.insert(p)
    return dict(total=total, computed=computed, saved=1 - computed / total)
