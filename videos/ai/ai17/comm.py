"""Processes on this machine as a tiny cluster: point-to-point messages and all-reduce over pipes.

Workers live in this module so the ``spawn`` start method (macOS's default, and safe with threaded BLAS) can import
them.  Each rank is one process; every pair of ranks shares a duplex pipe.  A send runs on its own thread so that a
rank can send and receive at once, as a ring needs.
"""

from __future__ import annotations

import time

import numpy as np


_POOL = None


def _sendrecv(send_conn, send_buf, recv_conn, recv_buf):
    """Send and receive at once: the send runs on one long-lived helper thread (starting a thread per message
    would cost more than a small message)."""
    global _POOL
    if _POOL is None:
        from concurrent.futures import ThreadPoolExecutor

        _POOL = ThreadPoolExecutor(max_workers=1)
    fut = _POOL.submit(send_conn.send_bytes, send_buf)
    recv_conn.recv_bytes_into(recv_buf)
    fut.result()


def ring_allreduce(x: np.ndarray, rank: int, p: int, conns: dict) -> None:
    """In place: reduce-scatter, then all-gather, p - 1 steps each (Patarasuk & Yuan 2009)."""
    chunks = np.array_split(np.arange(x.size), p)
    bounds = [(c[0], c[-1] + 1) for c in chunks]
    nxt, prv = conns[(rank + 1) % p], conns[(rank - 1) % p]
    tmp = np.empty(max(b - a for a, b in bounds), x.dtype)
    for s in range(p - 1):  # reduce-scatter: after it, this rank holds the full sum of chunk (rank + 1) % p
        a, b = bounds[(rank - s) % p]
        c, d = bounds[(rank - s - 1) % p]
        _sendrecv(nxt, memoryview(x[a:b]).cast("B"), prv, memoryview(tmp[: d - c]).cast("B"))
        x[c:d] += tmp[: d - c]
    for s in range(p - 1):  # all-gather: pass the finished chunks around
        a, b = bounds[(rank + 1 - s) % p]
        c, d = bounds[(rank - s) % p]
        _sendrecv(nxt, memoryview(x[a:b]).cast("B"), prv, memoryview(tmp[: d - c]).cast("B"))
        x[c:d] = tmp[: d - c]


def tree_allreduce(x: np.ndarray, rank: int, p: int, conns: dict) -> None:
    """In place: a binomial-tree reduce to rank 0, then a broadcast back down (2 log2 p steps, whole messages)."""
    tmp = np.empty_like(x)
    k = 1
    while k < p:  # reduce
        if rank % (2 * k) == k:
            conns[rank - k].send_bytes(memoryview(x).cast("B"))
        elif rank % (2 * k) == 0 and rank + k < p:
            conns[rank + k].recv_bytes_into(memoryview(tmp).cast("B"))
            x += tmp
        k *= 2
    k //= 2
    while k >= 1:  # broadcast
        if rank % (2 * k) == 0 and rank + k < p:
            conns[rank + k].send_bytes(memoryview(x).cast("B"))
        elif rank % (2 * k) == k:
            conns[rank - k].recv_bytes_into(memoryview(x).cast("B"))
        k //= 2


def worker(rank, p, conns, barrier, sizes, reps, out):
    """Time ping-pong (ranks 0 and 1) and both all-reduces for every size; rank 0 checks each sum."""
    import os

    os.environ.setdefault("OMP_NUM_THREADS", "1")
    res = {"pingpong": [], "ring": [], "tree": [], "ok": True}
    # ping-pong: half the round trip is one message
    for n in sizes:
        buf = np.zeros(max(n // 4, 1), np.float32)
        best = float("inf")
        for _ in range(reps):
            barrier.wait()
            if rank == 0:
                t = time.perf_counter()
                conns[1].send_bytes(memoryview(buf).cast("B"))
                conns[1].recv_bytes_into(memoryview(buf).cast("B"))
                best = min(best, (time.perf_counter() - t) / 2)
            elif rank == 1:
                conns[0].recv_bytes_into(memoryview(buf).cast("B"))
                conns[0].send_bytes(memoryview(buf).cast("B"))
        if rank == 0:
            res["pingpong"].append(best)
    for algo, fn in (("ring", ring_allreduce), ("tree", tree_allreduce)):
        for n in sizes:
            m = max(n // 4, p)
            times = []
            for r_ in range(reps):
                x = np.full(m, rank + 1, np.float32) + np.arange(m, dtype=np.float32) % 7
                barrier.wait()
                t = time.perf_counter()
                fn(x, rank, p, conns)
                dt = time.perf_counter() - t
                times.append(dt)
                if rank == 0 and r_ == 0:
                    want = p * (p + 1) / 2 + p * (np.arange(m, dtype=np.float32) % 7)
                    res["ok"] &= bool(np.allclose(x, want))
            res[algo].append(times)
    out.put((rank, res))
