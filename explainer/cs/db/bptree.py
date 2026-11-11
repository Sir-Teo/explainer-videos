"""A B+ tree (Part 35): every key in the leaves, linked left to right; interior nodes hold only separators.

    t = BPlusTree(order=4)
    for k in keys: t.insert(k, value)
    t.search(k); list(t.range(lo, hi)); t.height()

``order`` is the most children an interior node may have (the most keys a leaf may hold is order - 1).  A full node
splits in two and pushes its middle separator up; the root splitting is the only way the tree grows taller, so all
leaves stay at the same depth.  With a fanout of a few hundred (a 4 KiB page of keys and pointers), three levels
index tens of millions of keys and four index billions.
"""
from __future__ import annotations

import bisect


class Node:
    __slots__ = ("keys", "kids", "vals", "next", "leaf")

    def __init__(self, leaf: bool):
        self.leaf = leaf
        self.keys: list = []
        self.kids: list = []          # interior: children
        self.vals: list = []          # leaf: values
        self.next = None              # leaf: the next leaf


class BPlusTree:
    def __init__(self, order: int = 64):
        if order < 3:
            raise ValueError("B+ tree order must be at least three")
        self.order = order
        self.root = Node(leaf=True)
        self.splits = 0

    def _leaf(self, key):
        n = self.root
        path = []
        while not n.leaf:
            i = bisect.bisect_right(n.keys, key)
            path.append((n, i))
            n = n.kids[i]
        return n, path

    def search(self, key):
        n, _ = self._leaf(key)
        i = bisect.bisect_left(n.keys, key)
        if i < len(n.keys) and n.keys[i] == key:
            return n.vals[i]
        return None

    def insert(self, key, val) -> None:
        n, path = self._leaf(key)
        i = bisect.bisect_left(n.keys, key)
        if i < len(n.keys) and n.keys[i] == key:
            n.vals[i] = val
            return
        n.keys.insert(i, key)
        n.vals.insert(i, val)
        if len(n.keys) < self.order:
            return
        # split the leaf; copy its first key up
        mid = len(n.keys) // 2
        r = Node(leaf=True)
        r.keys, r.vals = n.keys[mid:], n.vals[mid:]
        n.keys, n.vals = n.keys[:mid], n.vals[:mid]
        r.next, n.next = n.next, r
        self.splits += 1
        sep, right = r.keys[0], r
        while path:
            p, i = path.pop()
            p.keys.insert(i, sep)
            p.kids.insert(i + 1, right)
            if len(p.kids) <= self.order:
                return
            mid = len(p.keys) // 2                # split the interior node; move its middle key up
            q = Node(leaf=False)
            sep = p.keys[mid]
            q.keys, q.kids = p.keys[mid + 1:], p.kids[mid + 1:]
            p.keys, p.kids = p.keys[:mid], p.kids[:mid + 1]
            self.splits += 1
            right = q
        new = Node(leaf=False)
        new.keys, new.kids = [sep], [self.root, right]
        self.root = new

    def range(self, lo, hi):
        """(key, value) for lo <= key <= hi, in order, by walking the leaf chain."""
        n, _ = self._leaf(lo)
        while n:
            for k, v in zip(n.keys, n.vals):
                if k > hi:
                    return
                if k >= lo:
                    yield k, v
            n = n.next

    def height(self) -> int:
        h, n = 1, self.root
        while not n.leaf:
            n = n.kids[0]
            h += 1
        return h

    def nodes(self) -> int:
        out, stack = 0, [self.root]
        while stack:
            n = stack.pop()
            out += 1
            if not n.leaf:
                stack += n.kids
        return out

    def check(self) -> None:
        """Every invariant: sorted keys, separators bounding their subtrees, leaves at one depth, sizes."""
        depths = set()

        def walk(n, lo, hi, d):
            assert n.keys == sorted(n.keys)
            assert all((lo is None or k >= lo) and (hi is None or k < hi) for k in n.keys)
            if n.leaf:
                depths.add(d)
                assert len(n.keys) < self.order
                return
            assert len(n.kids) == len(n.keys) + 1 <= self.order
            for i, c in enumerate(n.kids):
                walk(c, n.keys[i - 1] if i else lo, n.keys[i] if i < len(n.keys) else hi, d + 1)
        walk(self.root, None, None, 1)
        assert len(depths) == 1


def levels_for(n: int, fanout: int) -> int:
    """Levels a B+ tree of this fanout needs for n keys (leaves full to the same fanout)."""
    if n < 0 or fanout < 2:
        raise ValueError("key count must be nonnegative and fanout at least two")
    lv, cap = 1, fanout
    while cap < n:
        cap *= fanout
        lv += 1
    return lv
