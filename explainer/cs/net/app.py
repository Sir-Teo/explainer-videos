"""Above transport (Part 37): DNS with caching and its poisoning odds, HTTP head-of-line blocking against QUIC
streams, and CDN caches on Zipf-distributed requests.

    Resolver(zones, rtt): iterative resolution root -> TLD -> authoritative, with a TTL cache; ``resolve(name, now)``
        returns (address, round trips, cache hit)
    kaminsky_odds(id_bits, port_bits, forged, races)   the chance that forged replies guess a query's transaction ID
        (and source port) at least once in ``races`` races of ``forged`` replies each
    page_load(objects, loss, rtt, rate, mode, rng)   objects of given sizes fetched over one lossy path:
        "http1" (six TCP connections, objects queued on them), "http2" (one TCP connection, streams multiplexed: any
        loss stalls every stream until it is repaired) or "quic" (one connection, a loss stalls only its own stream)
    zipf_fit(counts)   the exponent s of rank^-s by least squares on log-log (ranks 10 to 10,000)
    lru_hit_rate(requests, size)   an LRU cache's hit rate on a request stream; ``che(probabilities, size)`` the
        Che approximation
"""
from __future__ import annotations

import heapq
import math
import random
from collections import OrderedDict


class Resolver:
    def __init__(self, zones: dict, rtt: float = 0.03):
        """zones: name -> (address, ttl); every name is "label.tld"."""
        self.zones = zones
        self.rtt = rtt
        self.cache: dict = {}

    def resolve(self, name: str, now: float):
        e = self.cache.get(name)
        if e and e[1] > now:
            return e[0], 0, True
        trips = 0
        tld = name.rsplit(".", 1)[-1]
        if not (self.cache.get("." + tld) and self.cache["." + tld][1] > now):
            trips += 1                                       # ask a root server for the TLD's servers
            self.cache["." + tld] = (tld, now + 172800)
        trips += 1                                           # ask the TLD for the domain's servers
        trips += 1                                           # ask the authoritative server
        addr, ttl = self.zones[name]
        self.cache[name] = (addr, now + ttl)
        return addr, trips, False


def kaminsky_odds(id_bits: int = 16, port_bits: int = 0, forged: int = 100, races: int = 1) -> float:
    """Success probability for independent uniform guesses, with replacement, across all races."""
    if min(id_bits, port_bits, forged, races) < 0:
        raise ValueError("bit counts and attempt counts must be nonnegative")
    space = 2 ** (id_bits + port_bits)
    attempts = forged * races
    if not attempts:
        return 0.0
    return 1.0 if space == 1 else -math.expm1(attempts * math.log1p(-1 / space))


def page_load(objects, loss: float, rtt: float, rate_pps: float, mode: str, rng: random.Random) -> dict:
    """A packet-level model of one page: objects (in packets) requested at time 0.  Every packet takes 1/rate to
    send and arrives one RTT/2 later; a lost packet is resent one RTT after it was sent (fast retransmit).  Data is
    delivered to the application in order within each ordering domain: per connection for HTTP/1.1 and HTTP/2, per
    stream for QUIC."""
    if mode not in ("http1", "http2", "quic") or not 0 <= loss < 1 or rtt < 0 or rate_pps <= 0:
        raise ValueError("invalid transport mode or path parameters")
    if any(not isinstance(n, int) or n < 0 for n in objects):
        raise ValueError("object sizes must be nonnegative packet counts")
    if not objects:
        return {"mode": mode, "page": 0.0, "mean_object": 0.0}
    if mode == "http1":
        conns = [[] for _ in range(6)]
        for i, n in enumerate(objects):
            min(conns, key=lambda c: sum(objects[j] for j in c)).append(i)
        domains = [[(i, n) for i in c for n in [objects[i]]] for c in conns]
        senders = 6
    else:
        # one connection, round-robin across streams, packet by packet
        order = []
        left = list(objects)
        while any(left):
            for i in range(len(left)):
                if left[i]:
                    order.append(i)
                    left[i] -= 1
        domains = [order]
        senders = 1
    finish = {i: 0.0 for i in range(len(objects))}
    for d in domains:
        t = 0.0
        if mode == "http1":
            seq = [i for i, n in d for _ in range(n)]
        else:
            seq = d
        # each connection shares the link equally (rate / senders) for simplicity
        r = rate_pps / senders
        arrivals = []
        for k, obj in enumerate(seq):
            t += 1 / r
            a = t + rtt / 2
            while rng.random() < loss:
                a += rtt                                       # retransmitted a round trip later
            arrivals.append((obj, a))
        if mode == "quic":
            for obj in set(o for o, _ in arrivals):
                finish[obj] = max(a for o, a in arrivals if o == obj)
        else:
            # in-order delivery within the connection: a packet is usable only when all before it have arrived
            latest = 0.0
            for obj, a in arrivals:
                latest = max(latest, a)
                finish[obj] = max(finish.get(obj, 0.0), latest)
    times = [finish[i] for i in range(len(objects))]
    return {"mode": mode, "page": max(times), "mean_object": sum(times) / len(times)}


def zipf_fit(counts, lo: int = 10, hi: int = 10000) -> float:
    c = sorted(counts, reverse=True)[lo - 1:hi]
    xs = [math.log(r) for r in range(lo, lo + len(c))]
    ys = [math.log(v) for v in c]
    mx, my = sum(xs) / len(xs), sum(ys) / len(ys)
    slope = sum((x - mx) * (y - my) for x, y in zip(xs, ys)) / sum((x - mx) ** 2 for x in xs)
    return -slope


def lru_hit_rate(requests, size: int) -> float:
    if size < 0:
        raise ValueError("cache size must be nonnegative")
    cache: OrderedDict = OrderedDict()
    hits = 0
    for r in requests:
        if r in cache:
            hits += 1
            cache.move_to_end(r)
        else:
            cache[r] = True
            if len(cache) > size:
                cache.popitem(last=False)
    return hits / len(requests) if requests else 0.0


def che(probs, size: int) -> float:
    """Che's approximation: find T with sum (1 - e^{-p_i T}) = size; hit rate = sum p_i (1 - e^{-p_i T})."""
    if size < 0 or any(not math.isfinite(p) or p < 0 for p in probs):
        raise ValueError("cache size and probabilities must be nonnegative and finite")
    if size == 0:
        return 0.0
    if size >= sum(p > 0 for p in probs):
        return sum(probs)
    lo, hi = 0.0, 1.0
    while sum(-math.expm1(-p * hi) for p in probs) < size:
        hi *= 2
    for _ in range(200):
        T = (lo + hi) / 2
        occ = sum(-math.expm1(-p * T) for p in probs)
        if occ > size:
            hi = T
        else:
            lo = T
    T = (lo + hi) / 2
    return sum(p * -math.expm1(-p * T) for p in probs)


_ = heapq
