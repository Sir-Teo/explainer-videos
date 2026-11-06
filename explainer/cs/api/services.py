"""Data and time across services (Part 43): the dual-write problem against a transactional outbox; sagas with
compensations under injected failures; latency budgets composed over a call graph with fan-out; bounded queues and
load shedding; and a JWT verifier that falls for ``alg: none`` and one that does not."""

from __future__ import annotations

import base64
import hashlib
import hmac
import json
import random


# ---------------------------------------------------------------- dual writes and the outbox

def dual_write(n=10_000, crash=0.01, seed=0):
    """An order service commits a row and publishes an event.  Written as two steps, a crash between them loses the
    event, and publishing first can announce an order that never committed.  With an outbox, the event row is
    committed in the same transaction as the order; a relay publishes unsent outbox rows and then marks them sent,
    and after a crash it republishes whatever is unmarked.  Counts how many events each committed order produced."""
    out = {}
    for mode in ("commit then publish", "publish then commit", "outbox"):
        rng = random.Random(seed)
        committed, events = 0, {}
        for i in range(n):
            if mode == "commit then publish":
                committed += 1
                if rng.random() >= crash:
                    events[i] = events.get(i, 0) + 1
            elif mode == "publish then commit":
                events[i] = events.get(i, 0) + 1
                if rng.random() >= crash:
                    committed += 1
                else:
                    events[i] = -events[i]            # announced, never committed: a phantom
            else:
                committed += 1                        # order row and outbox row, one transaction
                while True:
                    events[i] = events.get(i, 0) + 1  # relay publishes
                    if rng.random() >= crash:         # and marks the row sent, unless it crashes first
                        break
        lost = sum(1 for i in range(n) if events.get(i, 0) == 0)
        phantom = sum(1 for v in events.values() if v < 0)
        dup = sum(1 for v in events.values() if v > 1)
        out[mode] = {"committed": committed, "lost_events": lost, "phantom_events": phantom,
                     "duplicate_events": dup}
    return {"orders": n, "crash": crash, "modes": out}


# ---------------------------------------------------------------- sagas

SAGA = [("reserve stock", "release stock"), ("charge card", "refund card"), ("book courier", "cancel courier"),
        ("send confirmation", None)]


def saga_run(fail_at=None, comp_fail=0.0, rng=None):
    """Run the order saga; if step fail_at fails, compensate the completed steps in reverse order.  A compensation
    can itself fail and is retried until it succeeds (compensations must be idempotent).  Returns the log."""
    log, done = [], []
    for k, (step, comp) in enumerate(SAGA):
        if k == fail_at:
            log.append(("fail", step))
            for j in reversed(done):
                c = SAGA[j][1]
                tries = 1
                while rng is not None and rng.random() < comp_fail:
                    tries += 1
                log.append(("compensate", c, tries))
            return log, "compensated"
        log.append(("do", step))
        done.append(k)
    return log, "completed"


def saga_experiment(n=10_000, p_fail=(0.01, 0.03, 0.02, 0.0), comp_fail=0.05, seed=1):
    """Many orders, each step failing with its own probability; count outcomes and check the invariant that every
    order ends either fully done or fully compensated (no money taken without stock, no courier without payment)."""
    rng = random.Random(seed)
    outcome = {"completed": 0, "compensated": 0}
    by_step = [0] * len(SAGA)
    retries = 0
    inconsistent = 0
    for _ in range(n):
        fail_at = None
        for k, p in enumerate(p_fail):
            if rng.random() < p:
                fail_at = k
                break
        log, res = saga_run(fail_at, comp_fail, rng)
        outcome[res] += 1
        if fail_at is not None:
            by_step[fail_at] += 1
        retries += sum(e[2] - 1 for e in log if e[0] == "compensate")
        state = set()
        for e in log:
            if e[0] == "do":
                state.add(e[1])
            elif e[0] == "compensate":
                state.discard([s for s, c in SAGA if c == e[1]][0])
        if res == "compensated" and state:
            inconsistent += 1
    return {"orders": n, **outcome, "failed_at": dict(zip([s for s, _ in SAGA], by_step)),
            "compensation_retries": retries, "inconsistent": inconsistent,
            "example": saga_run(2)[0]}


# ---------------------------------------------------------------- latency budgets

def call_latency(rng, p50=10.0, tail=0.01, tail_ms=200.0):
    """One call: lognormal around p50, with a small chance of a slow outlier (a GC pause, a retransmit)."""
    x = p50 * rng.lognormvariate(0, 0.35)
    if rng.random() < tail:
        x += tail_ms * rng.random()
    return x


def call_graph(fanout=(1, 5, 20, 100), n=20_000, seed=2):
    """A front end calls a service that fans out to k back ends in parallel and waits for all of them (Part 39's
    tail at scale): the request's latency is the maximum of k draws plus the serial hops."""
    rng = random.Random(seed)
    rows = []
    for k in fanout:
        lat = []
        for _ in range(n):
            serial = call_latency(rng, 5.0) + call_latency(rng, 5.0)
            par = max(call_latency(rng) for _ in range(k))
            lat.append(serial + par)
        lat.sort()
        rows.append({"fanout": k, "p50": lat[n // 2], "p99": lat[int(n * 0.99)], "p999": lat[int(n * 0.999)],
                     "share_slow": sum(1 for x in lat if x > 100) / n})
    one = sorted(call_latency(rng) for _ in range(n))
    return {"rows": rows, "single": {"p50": one[n // 2], "p99": one[int(n * 0.99)]},
            "analytic_slow": [{"fanout": k, "p_any_tail": 1 - 0.99 ** k} for k in fanout]}


def budget(chain=(("gateway", 5), ("auth", 8), ("orders", 25), ("inventory", 30), ("payments", 60)), slo=150,
           timeout_rule="half the remaining"):
    """A deadline propagated down a call chain: each hop gets what its caller has left minus its own work."""
    left = slo
    rows = []
    for name, own in chain:
        rows.append({"service": name, "deadline_ms": left, "own_ms": own})
        left -= own
    return {"slo": slo, "rows": rows, "slack": left, "rule": timeout_rule}


# ---------------------------------------------------------------- backpressure

def queueing(load=(0.5, 0.8, 0.9, 0.95, 0.99, 1.05, 1.2), bound=None, n=50_000, seed=3, service=1.0):
    """An M/M/1 queue (Part 31) in front of a service: mean wait, and with a bound, the share of requests shed."""
    rows = []
    for rho in load:
        rng = random.Random(seed)
        t = 0.0
        free_at = 0.0
        in_sys = []                 # departure times of requests still in the system
        waits, shed = [], 0
        for _ in range(n):
            t += rng.expovariate(rho / service)
            in_sys = [d for d in in_sys if d > t]
            if bound is not None and len(in_sys) >= bound:
                shed += 1
                continue
            start = max(t, free_at)
            free_at = start + rng.expovariate(1 / service)
            in_sys.append(free_at)
            waits.append(free_at - t)
        waits.sort()
        rows.append({"load": rho, "mean": sum(waits) / len(waits), "p99": waits[int(len(waits) * 0.99)],
                     "shed": shed / n, "theory_mean": service / (1 - rho) if rho < 1 else None})
    return {"bound": bound, "rows": rows}


# ---------------------------------------------------------------- tokens

def _b64(b: bytes) -> str:
    return base64.urlsafe_b64encode(b).rstrip(b"=").decode()


def _unb64(s: str) -> bytes:
    return base64.urlsafe_b64decode(s + "=" * (-len(s) % 4))


def jwt_sign(payload: dict, key: bytes, alg="HS256") -> str:
    h = _b64(json.dumps({"alg": alg, "typ": "JWT"}, separators=(",", ":")).encode())
    p = _b64(json.dumps(payload, separators=(",", ":")).encode())
    sig = "" if alg == "none" else _b64(hmac.new(key, f"{h}.{p}".encode(), hashlib.sha256).digest())
    return f"{h}.{p}.{sig}"


def jwt_verify_naive(token: str, key: bytes):
    """Trusts the header's choice of algorithm: the classic bug."""
    h, p, s = token.split(".")
    alg = json.loads(_unb64(h))["alg"]
    if alg == "none":
        return json.loads(_unb64(p))
    good = _b64(hmac.new(key, f"{h}.{p}".encode(), hashlib.sha256).digest())
    return json.loads(_unb64(p)) if hmac.compare_digest(good, s) else None


def jwt_verify(token: str, key: bytes, alg="HS256"):
    """Pins the algorithm on the server, as RFC 8725 (JWT best current practice) requires."""
    h, p, s = token.split(".")
    if json.loads(_unb64(h)).get("alg") != alg:
        return None
    good = _b64(hmac.new(key, f"{h}.{p}".encode(), hashlib.sha256).digest())
    return json.loads(_unb64(p)) if hmac.compare_digest(good, s) else None


def jwt_demo():
    key = b"server-secret"
    honest = jwt_sign({"sub": "ada", "role": "reader", "exp": 1_900_000_000}, key)
    forged = jwt_sign({"sub": "ada", "role": "admin", "exp": 1_900_000_000}, b"", alg="none")
    tampered = honest.split(".")
    tampered[1] = _b64(json.dumps({"sub": "ada", "role": "admin", "exp": 1_900_000_000},
                                  separators=(",", ":")).encode())
    tampered = ".".join(tampered)
    rows = []
    for name, tok in (("honest", honest), ("payload edited", tampered), ("alg: none", forged)):
        rows.append({"token": name, "naive": jwt_verify_naive(tok, key), "pinned": jwt_verify(tok, key)})
    return {"honest": honest, "forged": forged, "rows": rows}


# ---------------------------------------------------------------- GraphQL's N + 1 and batching

def n_plus_one(authors=50, books_per=4):
    """A query for authors and their books: resolving each author's books separately costs one query per author;
    a DataLoader-style batcher collects the keys requested in one tick and issues one query for all of them."""
    queries_naive = 1 + authors
    queries_batched = 1 + 1
    nested = 1 + authors + authors * books_per        # and each book's reviews, naively
    nested_batched = 3
    return {"authors": authors, "naive": queries_naive, "batched": queries_batched,
            "nested_naive": nested, "nested_batched": nested_batched}


# ---------------------------------------------------------------- queues: visibility timeouts and dead letters

def visibility(n=2000, timeout=30.0, work=(5.0, 20.0), slow=0.05, slow_work=(40.0, 90.0), poison=0.002,
               max_receives=5, seed=4):
    """Workers take messages from a queue; a taken message is hidden for `timeout` seconds and reappears unless
    deleted.  Slow work outlives the timeout and is processed twice; a poison message fails every time and, after
    max_receives, goes to a dead-letter queue instead of blocking the queue forever."""
    rng = random.Random(seed)
    processed, twice, dlq, receives = 0, 0, 0, 0
    for _ in range(n):
        if rng.random() < poison:
            receives += max_receives
            dlq += 1
            continue
        t = rng.uniform(*(slow_work if rng.random() < slow else work))
        copies = 1 + int(t // timeout)          # it reappears every timeout until the first copy finishes
        receives += copies
        processed += 1
        if copies > 1:
            twice += 1
    return {"messages": n, "processed": processed, "processed_more_than_once": twice, "dead_lettered": dlq,
            "receives": receives, "timeout": timeout}


# ---------------------------------------------------------------- time in APIs

def time_pitfalls():
    """Facts about clocks an API must survive, computed with the standard library."""
    from datetime import datetime, timedelta
    from zoneinfo import ZoneInfo
    ny = ZoneInfo("America/New_York")
    a = datetime(2026, 3, 8, 1, 30, tzinfo=ny)
    b = a + timedelta(hours=1)                      # wall-clock arithmetic in a zone
    real = (b.astimezone(ZoneInfo("UTC")) - a.astimezone(ZoneInfo("UTC"))).total_seconds() / 3600
    lh = ZoneInfo("Australia/Lord_Howe")
    c = datetime(2026, 4, 5, 12, 0, tzinfo=lh)
    norm = b.astimezone(ZoneInfo("UTC")).astimezone(ny)
    return {"dst_gap": {"start": a.isoformat(), "plus_1h_wall": b.isoformat(), "elapsed_hours": real,
                        "normalized": norm.isoformat(), "exists": norm.replace(tzinfo=None) == b.replace(tzinfo=None)},
            "lord_howe_offset": str(c.utcoffset()),
            "leap_seconds_since_1972": 27,
            "unix_2038": datetime.fromtimestamp(2 ** 31 - 1, ZoneInfo("UTC")).isoformat()}
