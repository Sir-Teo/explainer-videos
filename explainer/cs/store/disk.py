"""Disks (Part 34): the time a hard disk takes to serve a request, and the schedulers that order its queue.

A request costs a **seek** (move the arm across d cylinders), a **rotational delay** (wait for the sector to come
round) and a **transfer**.  The seek model is the square-root curve of an arm that accelerates and then decelerates
(Ruemmler & Wilkes 1994): seek(d) = t_min + (t_max - t_min) * sqrt(d / C) for d > 0.  The defaults describe a
7200 rpm desktop drive, as modelled here (not any one product): 0.5 ms track to track, 16 ms full stroke, so a random
seek averages t_min + (t_max - t_min) * 8/15 = 8.8 ms; half a turn, 4.17 ms; 150 MB/s off the platter.

Flash has no arm; :data:`SSD` is a rough NVMe drive for comparison: 80 us to read a random 4 KiB page, 3 GB/s in
sequence.
"""
from __future__ import annotations

import math
import random
from dataclasses import dataclass


@dataclass
class HDD:
    rpm: float = 7200
    cylinders: int = 100_000
    t_min: float = 0.5           # ms, track to track
    t_max: float = 16.0          # ms, full stroke
    mb_s: float = 150.0          # sustained transfer, MB/s
    blocks: int = 4_000_000_000  # 1 KiB blocks: a 4 TB disk

    @property
    def rev_ms(self) -> float:
        return 60_000 / self.rpm

    def seek(self, d: int) -> float:
        d = abs(d)
        return 0.0 if d == 0 else self.t_min + (self.t_max - self.t_min) * math.sqrt(d / self.cylinders)

    def avg_seek(self) -> float:
        return self.t_min + (self.t_max - self.t_min) * 8 / 15      # E sqrt|U - V| = 8/15 for U, V uniform

    def transfer(self, nbytes: int) -> float:
        return nbytes / (self.mb_s * 1e6) * 1e3

    def random_io(self, nbytes: int) -> float:
        """ms for one request at a random place: average seek, half a turn, and the transfer."""
        return self.avg_seek() + self.rev_ms / 2 + self.transfer(nbytes)

    def cyl(self, block: int) -> int:
        return min(self.cylinders - 1, block * self.cylinders // self.blocks)

    def trace_time(self, blocks: list[int], bs: int = 1024, start: int | None = None) -> dict:
        """Time to read ``blocks`` in this order: a block right after the last one costs only its transfer;
        anything else a seek, half a turn on average, and the transfer.  Returns ms, and how many jumps."""
        t = seeks = 0
        prev = start
        for b in blocks:
            if prev is not None and b == prev + 1:
                t += self.transfer(bs)
            else:
                d = 0 if prev is None else self.cyl(b) - self.cyl(prev)
                t += (self.seek(d) if prev is not None else self.avg_seek()) + self.rev_ms / 2 + self.transfer(bs)
                seeks += 1
            prev = b
        return {"ms": t, "jumps": seeks, "blocks": len(blocks)}


@dataclass
class Flash:
    read_us: float = 80.0        # a random 4 KiB read
    gb_s: float = 3.0            # sequential

    def trace_time(self, blocks: list[int], bs: int = 1024) -> dict:
        t = jumps = 0
        prev = None
        for b in blocks:
            if prev is not None and b == prev + 1:
                t += bs / (self.gb_s * 1e9) * 1e3
            else:
                t += self.read_us / 1e3
                jumps += 1
            prev = b
        return {"ms": t, "jumps": jumps, "blocks": len(blocks)}


SSD = Flash()


# ---- scheduling ------------------------------------------------------------------------------------------------
def order(policy: str, head: int, queue: list[int], direction: int = 1, cylinders: int = 200) -> list[int]:
    """The order a static queue of cylinder numbers is served in."""
    q = list(queue)
    if policy == "fcfs":
        return q
    if policy == "sstf":
        out, h = [], head
        while q:
            nxt = min(q, key=lambda c: (abs(c - h), c))
            q.remove(nxt)
            out.append(nxt)
            h = nxt
        return out
    up = sorted(c for c in q if c >= head)
    down = sorted((c for c in q if c < head), reverse=True)
    if policy == "scan":                 # the elevator: sweep one way, then back
        return up + down if direction > 0 else down + up
    if policy == "cscan":                # sweep one way only, then return to the start
        return up + sorted(c for c in q if c < head)
    raise ValueError(policy)


def distance(head: int, seq: list[int], policy: str = "", cylinders: int = 200) -> int:
    d, h = 0, head
    for c in seq:
        d += abs(c - h)
        h = c
    return d


def simulate(policy: str, rate: float, n: int = 20_000, disk: HDD | None = None, seed: int = 0,
             hot: tuple[float, float] | None = None) -> dict:
    """A disk under load: requests arrive at ``rate`` per second (Poisson) for random cylinders (or, with ``hot`` =
    (fraction of requests, fraction of the disk), mostly in one band); the scheduler picks the next one each time
    the arm is free.  Returns the mean and the worst response time (ms), and the throughput."""
    disk = disk or HDD()
    rng = random.Random(seed)
    C = disk.cylinders
    t = 0.0
    arrivals = []
    for i in range(n):
        t += rng.expovariate(rate) * 1e3
        if hot and rng.random() < hot[0]:
            c = int(rng.random() * hot[1] * C)
        else:
            c = rng.randrange(C)
        arrivals.append((t, c))
    pending: list[tuple[float, int]] = []
    now, head, i, direction = 0.0, C // 2, 0, 1
    resp = []
    while i < n or pending:
        while i < n and arrivals[i][0] <= now:
            pending.append(arrivals[i])
            i += 1
        if not pending:
            now = arrivals[i][0]
            continue
        if policy == "fcfs":
            k = 0
        elif policy == "sstf":
            k = min(range(len(pending)), key=lambda j: abs(pending[j][1] - head))
        elif policy in ("scan", "cscan"):
            ahead = [j for j in range(len(pending)) if (pending[j][1] - head) * direction >= 0]
            if not ahead:
                if policy == "scan":
                    direction = -direction
                    ahead = [j for j in range(len(pending)) if (pending[j][1] - head) * direction >= 0]
                else:
                    now += disk.seek(head)          # C-SCAN: back to cylinder 0, then sweep up again
                    head = 0
                    ahead = list(range(len(pending)))
            k = min(ahead, key=lambda j: abs(pending[j][1] - head))
        else:
            raise ValueError(policy)
        ta, c = pending.pop(k)
        now += disk.seek(c - head) + rng.random() * disk.rev_ms + disk.transfer(4096)
        head = c
        resp.append(now - ta)
    resp.sort()
    return {"mean": sum(resp) / n, "p99": resp[int(0.99 * n)], "max": resp[-1], "iops": n / (now / 1e3)}
