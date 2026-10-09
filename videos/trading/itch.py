"""Nasdaq TotalView-ITCH 5.0: message layouts, the per-stock records written by ``native/itch_scan.c``,
and a plain (readable, not fast) limit order book used by the analyses in ``compute.py``.

Field layouts follow the Nasdaq TotalView-ITCH 5.0 specification.  Every message starts with an 11-byte
header: type (1 byte), stock locate (2), tracking number (2), timestamp (6, nanoseconds since midnight);
integers are big-endian and prices have four implied decimals.
"""

from __future__ import annotations

from pathlib import Path

import numpy as np

from explainer.tts import REPO_ROOT

CACHE = REPO_ROOT / ".cache" / "trading"
ITCH_DIR = CACHE / "itch"
NS = 1_000_000_000
OPEN_NS = 34_200 * NS  # 9:30:00
CLOSE_NS = 57_600 * NS  # 16:00:00

# (name, offset, length, kind) for the messages the video decodes on screen.
LAYOUT = {
    "A": ("Add Order", [("type", 0, 1, "c"), ("stock locate", 1, 2, "u"), ("tracking number", 3, 2, "u"),
                        ("timestamp", 5, 6, "u"), ("order reference", 11, 8, "u"), ("side", 19, 1, "c"),
                        ("shares", 20, 4, "u"), ("stock", 24, 8, "s"), ("price", 32, 4, "p")]),
    "E": ("Order Executed", [("type", 0, 1, "c"), ("stock locate", 1, 2, "u"), ("tracking number", 3, 2, "u"),
                             ("timestamp", 5, 6, "u"), ("order reference", 11, 8, "u"), ("executed shares", 19, 4, "u"),
                             ("match number", 23, 8, "u")]),
    "D": ("Order Delete", [("type", 0, 1, "c"), ("stock locate", 1, 2, "u"), ("tracking number", 3, 2, "u"),
                           ("timestamp", 5, 6, "u"), ("order reference", 11, 8, "u")]),
    "X": ("Order Cancel", [("type", 0, 1, "c"), ("stock locate", 1, 2, "u"), ("tracking number", 3, 2, "u"),
                           ("timestamp", 5, 6, "u"), ("order reference", 11, 8, "u"), ("canceled shares", 19, 4, "u")]),
    "U": ("Order Replace", [("type", 0, 1, "c"), ("stock locate", 1, 2, "u"), ("tracking number", 3, 2, "u"),
                            ("timestamp", 5, 6, "u"), ("original reference", 11, 8, "u"), ("new reference", 19, 8, "u"),
                            ("shares", 27, 4, "u"), ("price", 31, 4, "p")]),
}

REC = np.dtype([("ts", "<u8"), ("ref", "<u8"), ("ref2", "<u8"), ("shares", "<u4"), ("price", "<u4"),
                ("type", "u1"), ("side", "u1"), ("flag", "u1"), ("pad", "V5")])
assert REC.itemsize == 40


def records(sym: str) -> np.ndarray:
    """Every message of one stock, in feed order, as a read-only memory map."""
    p = ITCH_DIR / f"sym_{sym}.bin"
    if not p.exists():
        raise FileNotFoundError(f"{p} missing: run `python -m videos.trading.compute itch`")
    return np.memmap(p, dtype=REC, mode="r")


def raw_messages(sym: str) -> list[bytes]:
    """The first raw ITCH messages of a stock at or after 9:30:00, exactly as they were on the feed."""
    data = (ITCH_DIR / f"raw_{sym}.bin").read_bytes()
    out, i = [], 0
    while i + 2 <= len(data):
        n = int.from_bytes(data[i:i + 2], "big")
        out.append(data[i + 2:i + 2 + n])
        i += 2 + n
    return out


def decode(msg: bytes) -> dict:
    """Field values of a raw message whose type is in LAYOUT."""
    name, fields = LAYOUT[chr(msg[0])]
    out = {"_name": name}
    for fname, off, n, kind in fields:
        b = msg[off:off + n]
        if kind == "c":
            out[fname] = chr(b[0])
        elif kind == "s":
            out[fname] = b.decode("ascii").rstrip()
        elif kind == "p":
            out[fname] = int.from_bytes(b, "big") / 10_000
        else:
            out[fname] = int.from_bytes(b, "big")
    return out


def clock(ns: int, digits: int = 9) -> str:
    """Nanoseconds since midnight -> 'HH:MM:SS.fffffffff'."""
    s, frac = divmod(int(ns), NS)
    h, s = divmod(s, 3600)
    m, s = divmod(s, 60)
    return f"{h:02d}:{m:02d}:{s:02d}." + f"{frac:09d}"[:digits]


class Book:
    """A readable price-time-priority book: levels[side][price] is an insertion-ordered dict ref -> shares,
    so iterating a level walks its queue front to back.  Prices are integer cents."""

    def __init__(self):
        self.orders: dict[int, list] = {}  # ref -> [side, price, shares]
        self.levels = {66: {}, 83: {}}  # ord('B'), ord('S')
        self.best = {66: None, 83: None}

    # -- updates -------------------------------------------------------------------------------
    def add(self, ref, side, price, shares):
        self.orders[ref] = [side, price, shares]
        lv = self.levels[side].setdefault(price, {})
        lv[ref] = shares
        b = self.best[side]
        if b is None or (price > b if side == 66 else price < b):
            self.best[side] = price

    def reduce(self, ref, n):
        o = self.orders.get(ref)
        if o is None:
            return
        side, price, shares = o
        if n >= shares:
            self.remove(ref)
        else:
            o[2] = shares - n
            self.levels[side][price][ref] = shares - n

    def remove(self, ref):
        o = self.orders.pop(ref, None)
        if o is None:
            return None
        side, price, _ = o
        lv = self.levels[side][price]
        del lv[ref]
        if not lv:
            del self.levels[side][price]
            if self.best[side] == price:
                keys = self.levels[side].keys()
                self.best[side] = (max(keys) if side == 66 else min(keys)) if keys else None
        return o

    def apply(self, r):
        t = r["type"]
        if t == 65 or t == 70:  # A, F
            self.add(int(r["ref"]), int(r["side"]), int(r["price"]) // 100, int(r["shares"]))
        elif t == 69 or t == 67 or t == 88:  # E, C, X
            self.reduce(int(r["ref"]), int(r["shares"]))
        elif t == 68:  # D
            self.remove(int(r["ref"]))
        elif t == 85:  # U
            o = self.remove(int(r["ref"]))
            if o is not None:
                self.add(int(r["ref2"]), o[0], int(r["price"]) // 100, int(r["shares"]))

    # -- queries ---------------------------------------------------------------------------------
    @property
    def bid(self):
        return self.best[66]

    @property
    def ask(self):
        return self.best[83]

    def depth(self, side, price) -> int:
        lv = self.levels[side].get(price)
        return sum(lv.values()) if lv else 0

    def ladder(self, n=8):
        """[(price, [order sizes front to back])] for the n best levels of each side."""
        bids = sorted(self.levels[66], reverse=True)[:n]
        asks = sorted(self.levels[83])[:n]
        return ([(p, list(self.levels[66][p].values())) for p in bids],
                [(p, list(self.levels[83][p].values())) for p in asks])


def iter_rows(recs: np.ndarray, start: int = 0, stop: int | None = None, chunk: int = 1 << 20):
    """Yield (index, ts, type, ref, ref2, shares, price, side) as Python ints, chunked for speed."""
    stop = len(recs) if stop is None else stop
    for a in range(start, stop, chunk):
        b = min(stop, a + chunk)
        part = np.asarray(recs[a:b])
        cols = [part[k].tolist() for k in ("ts", "type", "ref", "ref2", "shares", "price", "side")]
        for j, row in enumerate(zip(*cols)):
            yield (a + j, *row)


def path(name: str) -> Path:
    return CACHE / name
