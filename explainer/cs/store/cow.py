"""Copy-on-write trees (Part 34): the idea under ZFS and btrfs, with Merkle checksums (Part 29).

A file's blocks hang from a tree of pointer blocks.  Nothing is ever overwritten: to change one data block, write a
new copy of it, then a new copy of its parent pointing at the copy, and so on up to a new root, then switch the
**uberblock** to the new root in one write.  A crash before that last write leaves the old tree whole; after it,
the new one.  Every pointer carries the **checksum** of the block it points to, so the root's checksum vouches for
everything (a Merkle tree): a block that rots on the disk is caught on the way down, and repaired from a mirror.  A
**snapshot** is just an old root kept alive: it shares every block that has not changed since.

    t = CowTree(fanout=4, depth=3)            # 64 data blocks
    t.write(5, b"...")                        # writes 1 data block + 3 pointer blocks, then the uberblock
    snap = t.snapshot()
    t.verify(t.root)                          # [] if every checksum holds
"""
from __future__ import annotations

import hashlib


def h(b: bytes) -> str:
    return hashlib.sha256(b).hexdigest()[:16]


class CowTree:
    def __init__(self, fanout: int = 4, depth: int = 3, block: int = 64):
        self.F, self.D, self.B = fanout, depth, block
        self.store: dict[int, bytes] = {}          # address -> contents (never overwritten)
        self.next = 0
        self.writes = 0
        self.mirror: dict[int, bytes] = {}         # a second copy of every block (ZFS's mirror or "copies=2")
        self.root = self._build(depth)
        self.snapshots: dict[str, tuple[int, str]] = {}

    # -- blocks ------------------------------------------------------------------------------------------
    def _put(self, data: bytes) -> tuple[int, str]:
        a = self.next
        self.next += 1
        self.store[a] = data
        self.mirror[a] = data
        self.writes += 1
        return a, h(data)

    def _node(self, ptrs: list[tuple[int, str]]) -> bytes:
        return "|".join(f"{a}:{c}" for a, c in ptrs).encode()

    def _ptrs(self, a: int) -> list[tuple[int, str]]:
        out = []
        for p in self.store[a].decode().split("|"):
            x, c = p.split(":")
            out.append((int(x), c))
        return out

    def _build(self, depth: int, base: int = 0) -> tuple[int, str]:
        if depth == 0:
            return self._put(bytes(self.B))
        return self._put(self._node([self._build(depth - 1, base * self.F + k) for k in range(self.F)]))

    @property
    def nblocks(self) -> int:
        return self.F ** self.D

    # -- operations ----------------------------------------------------------------------------------------
    def write(self, i: int, data: bytes) -> int:
        """Copy-on-write block i: returns how many blocks were written (one per level, plus the data)."""
        before = self.writes
        path = []
        a, _ = self.root
        for lvl in range(self.D):
            k = i // self.F ** (self.D - 1 - lvl) % self.F
            path.append((a, k))
            a = self._ptrs(a)[k][0]
        new = self._put(data.ljust(self.B, b"\0")[:self.B])
        for a, k in reversed(path):
            ptrs = self._ptrs(a)
            ptrs[k] = new
            new = self._put(self._node(ptrs))
        self.root = new                              # the uberblock: one small write switches trees
        return self.writes - before

    def read(self, i: int, root: tuple[int, str] | None = None) -> bytes:
        a, c = root or self.root
        for lvl in range(self.D):
            k = i // self.F ** (self.D - 1 - lvl) % self.F
            a, c = self._ptrs(a)[k]
        return self.store[a]

    def snapshot(self, name: str = "snap") -> tuple[int, str]:
        self.snapshots[name] = self.root
        return self.root

    def reachable(self, root: tuple[int, str]) -> set[int]:
        out, stack = set(), [(root[0], self.D)]
        while stack:
            a, d = stack.pop()
            out.add(a)
            if d:
                stack += [(x, d - 1) for x, _ in self._ptrs(a)]
        return out

    def live_blocks(self) -> int:
        roots = [self.root] + list(self.snapshots.values())
        s = set()
        for r in roots:
            s |= self.reachable(r)
        return len(s)

    def corrupt(self, a: int) -> None:
        """Flip a bit of block a on the primary copy (bit rot)."""
        b = bytearray(self.store[a])
        b[0] ^= 1
        self.store[a] = bytes(b)

    def verify(self, root: tuple[int, str] | None = None, repair: bool = False) -> list[int]:
        """Walk from the root checking each block against the checksum in its parent; returns the bad blocks
        (with ``repair``, each is rewritten from its mirror copy if that one checks out)."""
        bad = []
        stack = [(root or self.root, self.D)]
        while stack:
            (a, c), d = stack.pop()
            if h(self.store[a]) != c:
                bad.append(a)
                if repair and h(self.mirror[a]) == c:
                    self.store[a] = self.mirror[a]
                else:
                    continue
            if d:
                stack += [(p, d - 1) for p in self._ptrs(a)]
        return bad
