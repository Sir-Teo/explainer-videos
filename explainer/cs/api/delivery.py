"""Messages between services (Part 43): a network that loses, duplicates and delays messages; senders that retry;
receivers with and without idempotency keys; the Job as three services (tokenize, count, rank) whose counts stay
exact only with deduplication.  Also offset against cursor pagination under concurrent inserts, and a retry storm."""

from __future__ import annotations

import heapq
import random
from collections import Counter


class Net:
    """Each send is lost with probability loss, duplicated with probability dup, and delayed by a random latency."""

    def __init__(self, rng, loss=0.0, dup=0.0, lat=(1.0, 5.0)):
        self.rng, self.loss, self.dup, self.lat = rng, loss, dup, lat
        self.q = []
        self.t = 0.0
        self.seq = 0
        self.sent = self.lost = self.dups = 0

    def send(self, dst, msg):
        self.sent += 1
        copies = 0 if self.rng.random() < self.loss else 1
        if copies and self.rng.random() < self.dup:
            copies = 2
            self.dups += 1
        if not copies:
            self.lost += 1
        for _ in range(copies):
            self.seq += 1
            heapq.heappush(self.q, (self.t + self.rng.uniform(*self.lat), self.seq, dst, msg))

    def step(self):
        if not self.q:
            return None
        t, _, dst, msg = heapq.heappop(self.q)
        self.t = max(self.t, t)
        return dst, msg


def semantics(n=10_000, loss=0.05, dup=0.02, seed=1):
    """Deliver n increments to a counter under three policies.  At most once: send once, never retry.  At least
    once: retry until acknowledged (acks can be lost too).  Exactly once: at least once plus a receiver that
    remembers the ids it has applied."""
    out = {}
    for policy in ("at most once", "at least once", "exactly once"):
        rng = random.Random(seed)
        net = Net(rng, loss, dup)
        counter, seen, acked = 0, set(), set()
        pending = set(range(n))
        for i in range(n):
            net.send("recv", ("inc", i))
        rounds = 0
        while True:
            while True:
                ev = net.step()
                if ev is None:
                    break
                dst, msg = ev
                if dst == "recv":
                    _, i = msg
                    if policy == "exactly once":
                        if i not in seen:
                            seen.add(i)
                            counter += 1
                    else:
                        counter += 1
                    net.send("sender", ("ack", i))
                else:
                    acked.add(msg[1])
            pending -= acked
            if policy == "at most once" or not pending:
                break
            rounds += 1
            for i in sorted(pending):
                net.send("recv", ("inc", i))
        out[policy] = {"count": counter, "error": counter - n, "messages": net.sent, "retry_rounds": rounds}
    return {"n": n, "loss": loss, "dup": dup, "policies": out}


def _tokens(text):
    return [w.lower().strip(".,;:!?\"'()") for w in text.split() if w.strip(".,;:!?\"'()")]


def job_services(text: str, loss=0.05, dup=0.02, chunk=200, seed=2, dedup=True, top=10):
    """The Job as three services.  The tokenizer sends each chunk's word counts to the counter, retrying until
    acknowledged; the counter adds them, deduplicating by (chunk id) when dedup is on; the ranker asks the counter
    for the top words.  Returns the top words and how far every count is from the truth."""
    rng = random.Random(seed)
    words = _tokens(text)
    truth = Counter(words)
    chunks = [Counter(words[i:i + chunk]) for i in range(0, len(words), chunk)]
    net = Net(rng, loss, dup)
    counts, applied, acked = Counter(), set(), set()
    pending = set(range(len(chunks)))
    rounds = 0
    while pending:
        for k in sorted(pending):
            net.send("counter", (k, chunks[k]))
        while True:
            ev = net.step()
            if ev is None:
                break
            dst, msg = ev
            if dst == "counter":
                k, c = msg
                if not dedup or k not in applied:
                    counts.update(c)
                    applied.add(k)
                net.send("tokenizer", k)
            else:
                acked.add(msg)
        pending -= acked
        rounds += 1
    wrong = sum(1 for w in truth if counts[w] != truth[w])
    over = sum(counts.values()) - sum(truth.values())
    return {"words": len(words), "chunks": len(chunks), "messages": net.sent, "lost": net.lost,
            "duplicated": net.dups, "rounds": rounds, "distinct": len(truth), "wrong_counts": wrong,
            "overcount": over, "top": counts.most_common(top), "true_top": truth.most_common(top)}


# ---------------------------------------------------------------- pagination

def pagination(n=1000, page=50, inserts_per_page=3, seed=3):
    """A client pages through a list sorted newest first while new rows keep arriving at the top.  Offset paging
    (skip k, take page) shows rows twice; cursor paging (rows older than the last one seen) never does.  Offset
    paging also costs the database the skipped rows."""
    rng = random.Random(seed)
    rows = list(range(n))          # ids; larger is newer
    nxt = n
    seen_off, cost_off = [], 0
    k = 0
    data = sorted(rows, reverse=True)
    while k < len(data):
        pg = data[k:k + page]
        cost_off += k + len(pg)
        seen_off += pg
        k += page
        for _ in range(inserts_per_page):
            data.insert(0, nxt)
            nxt += 1
        if len(seen_off) >= n + 5 * page:
            break
    rng.random()
    data = sorted(rows, reverse=True)
    nxt = n
    seen_cur, cost_cur, last = [], 0, None
    while True:
        cand = [r for r in data if last is None or r < last]
        pg = cand[:page]
        if not pg:
            break
        cost_cur += len(pg)
        seen_cur += pg
        last = pg[-1]
        for _ in range(inserts_per_page):
            data.insert(0, nxt)
            nxt += 1
    orig = set(range(n))
    c_off = Counter(x for x in seen_off if x in orig)
    return {"n": n, "page": page, "inserts_per_page": inserts_per_page,
            "offset": {"pages": -(-len(seen_off) // page), "duplicates": sum(v - 1 for v in c_off.values() if v > 1),
                       "missed": len(orig - set(seen_off)), "rows_scanned": cost_off},
            "cursor": {"pages": -(-len(seen_cur) // page), "duplicates": len(seen_cur) - len(set(seen_cur)),
                       "missed": len(orig - set(seen_cur)), "rows_scanned": cost_cur}}


# ---------------------------------------------------------------- retry storms

def retry_storm(capacity=100.0, demand=90.0, outage=(20, 30), horizon=120, policy="immediate", seed=5):
    """A service that can answer `capacity` requests per second, offered `demand` new requests per second, is down
    for a few seconds.  Failed requests retry: immediately each second, or with exponential backoff and jitter, or
    with backoff only while a retry budget lasts (gRPC's throttling: each failure costs a token, each success
    earns a tenth of one, and retries stop below half the bucket).  The backlog after the outage is what decides whether it recovers."""
    rng = random.Random(seed)
    waiting = []                    # (due time, attempt)
    max_tokens = tokens = 100.0
    dropped = 0
    series = []
    for t in range(horizon):
        new = [(t, 0)] * int(demand)
        due = [w for w in waiting if w[0] <= t]
        waiting = [w for w in waiting if w[0] > t]
        offered = new + due
        cap = 0 if outage[0] <= t < outage[1] else int(capacity)
        served = offered[:cap]
        failed = offered[cap:]
        tokens = min(max_tokens, tokens + 0.1 * len(served))
        for _, a in failed:
            if policy == "immediate":
                waiting.append((t + 1, a + 1))
            elif policy == "backoff":
                d = min(60, 2 ** a) * rng.uniform(0.5, 1.5)
                waiting.append((t + max(1, int(d)), a + 1))
            elif policy == "budget":
                tokens = max(0.0, tokens - 1)             # gRPC-style retry throttling
                if tokens > max_tokens / 2:
                    d = min(60, 2 ** a) * rng.uniform(0.5, 1.5)
                    waiting.append((t + max(1, int(d)), a + 1))
                else:
                    dropped += 1
        series.append({"t": t, "offered": len(offered), "served": len(served), "backlog": len(waiting)})
    recovered = next((s["t"] for s in series if s["t"] > outage[1] and s["offered"] <= capacity), None)
    return {"policy": policy, "series": series, "recovered_at": recovered,
            "peak_offered": max(s["offered"] for s in series), "gave_up": dropped,
            "served": sum(s["served"] for s in series)}


# ---------------------------------------------------------------- exactly once, model-checked

def model_check(dedup: bool, n_msgs: int = 2, retries: int = 2, max_dups: int = 1):
    """Explore every execution of a sender that retries each of n_msgs increments until acknowledged (up to
    `retries` resends), over a network that may deliver in-flight messages in any order, drop them, or duplicate
    them (at most max_dups times in all); acknowledgements can be dropped too.  Checks, in every final state where
    the sender has seen every acknowledgement, that the counter equals n_msgs (exactly once), and in every state that
    it never exceeds n_msgs (at most once).  Returns the number of states and a counterexample trace if any."""
    from collections import deque
    start = (tuple([retries + 1] * n_msgs), (), 0, frozenset(), frozenset(), 0)
    # (sends left per msg, in-flight multiset as sorted tuple of (kind, i), counter, applied ids, acked ids, dups)
    seen = {start: None}
    q = deque([start])
    bad = None
    finals = 0
    while q:
        st = q.popleft()
        left, fl, cnt, applied, acked, dups = st
        if cnt > n_msgs and bad is None:
            bad = st
        succ = []
        for i in range(n_msgs):
            if i not in acked and left[i] > 0:
                nl = list(left)
                nl[i] -= 1
                succ.append(((tuple(nl), tuple(sorted(fl + (("m", i),))), cnt, applied, acked, dups),
                             f"send {i}"))
        for k, (kind, i) in enumerate(set(fl)):
            rest = list(fl)
            rest.remove((kind, i))
            rest = tuple(rest)
            succ.append(((left, rest, cnt, applied, acked, dups), f"drop {kind}{i}"))
            if dups < max_dups:
                succ.append(((left, tuple(sorted(fl + ((kind, i),))), cnt, applied, acked, dups + 1),
                             f"duplicate {kind}{i}"))
            if kind == "m":
                if dedup and i in applied:
                    nc, na = cnt, applied
                else:
                    nc, na = cnt + 1, applied | {i}
                succ.append(((left, tuple(sorted(rest + (("a", i),))), nc, na, acked, dups), f"deliver m{i}"))
            else:
                succ.append(((left, rest, cnt, applied, acked | {i}, dups), f"deliver a{i}"))
        if not succ:
            finals += 1
            if len(acked) == n_msgs and cnt != n_msgs and bad is None:
                bad = st
        for s2, lab in succ:
            if s2 not in seen:
                seen[s2] = (st, lab)
                q.append(s2)
    trace = []
    if bad is not None:
        x = bad
        while seen[x] is not None:
            x, lab = seen[x]
            trace.append(lab)
        trace.reverse()
    return {"dedup": dedup, "states": len(seen), "final_states": finals, "violation": bad is not None,
            "trace": trace, "counter_at_violation": bad[2] if bad else None}
