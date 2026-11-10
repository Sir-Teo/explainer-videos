"""Streaming Horspool prototype for exercise 5; no Pebble instruction claims.

The input is consumed once. A ring stores at most m bytes; skips avoid comparisons,
not input reads. Positions count bytes, including overlaps.
"""
from collections.abc import Iterable


def search(chunks: Iterable[bytes], pattern: bytes):
    stream = (byte for chunk in chunks for byte in chunk)
    m = len(pattern)
    if not m:
        reads = sum(1 for _ in stream)
        return list(range(reads + 1)), reads, 0
    shift = [m] * 256
    for i, byte in enumerate(pattern[:-1]):
        shift[byte] = m - 1 - i
    ring = bytearray(m)
    reads = comparisons = 0
    for i in range(m):
        byte = next(stream, None)
        if byte is None:
            return [], reads, comparisons
        ring[i] = byte
        reads += 1
    head = start = 0
    positions = []
    while True:
        j = m - 1
        while j >= 0:
            comparisons += 1
            if ring[(head + j) % m] != pattern[j]:
                break
            j -= 1
        if j < 0:
            positions.append(start)
        skip = shift[ring[(head + m - 1) % m]]
        for _ in range(skip):
            byte = next(stream, None)
            if byte is None:
                return positions, reads, comparisons
            ring[head] = byte
            head = (head + 1) % m
            start += 1
            reads += 1
