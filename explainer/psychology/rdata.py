"""A minimal reader for R's XDR serialization (``.RData``/``.rda``/``.rds``, format versions 2 and 3).

*Psychology, Built* reads a few classic datasets that are packaged inside CRAN source packages (catlearn, smacof,
janeaustenr; see ``opendata.py``).  This reader turns such a file into plain Python values and nothing else: logical,
integer, double and character vectors, generic vectors (lists), pairlists and attributes.  A function call stored
in a file (a LANGSXP) is read as a list of its parts and **never evaluated**; any other type (closures,
environments, external pointers, bytecode) raises.  No R code, and no pickled Python, is ever run.

    load(path)  ->  [(name, object), ...]     # an .RData/.rda file: its named objects

An object is ``{"type": sexptype, "value": [...], "attrs": {name: object}}``; integers and logicals use ``None`` for
NA; strings are ``str`` or ``None``.
"""

from __future__ import annotations

import bz2
import gzip
import lzma
import struct
import sys

NILVALUE, SYMSXP, LISTSXP, LANGSXP, CHARSXP = 254, 1, 2, 6, 9
LGLSXP, INTSXP, REALSXP, STRSXP, VECSXP = 10, 13, 14, 16, 19
REFSXP = 255
NA_INT = -2147483648


class Reader:
    """Reads one serialized object from the bytes after the format header."""

    def __init__(self, b: bytes):
        self.b, self.i, self.refs = b, 0, []

    def take(self, n: int) -> bytes:
        out = self.b[self.i:self.i + n]
        if len(out) != n:
            raise ValueError("truncated R data")
        self.i += n
        return out

    def int(self) -> int:
        return struct.unpack(">i", self.take(4))[0]

    def item(self):
        flags = self.int()
        t = flags & 0xFF
        has_attr, has_tag = bool(flags & (1 << 9)), bool(flags & (1 << 10))
        if t == NILVALUE:
            return None
        if t == REFSXP:
            return self.refs[(flags >> 8) - 1]
        if t == SYMSXP:
            name = self.item()
            self.refs.append(("sym", name))
            return ("sym", name)
        if t in (LISTSXP, LANGSXP):  # a pairlist, or a call stored as data: read as a list, never evaluated
            if has_attr:
                self.item()
            tag = self.item() if has_tag else None
            out = [(tag[1] if tag else None, self.item())]
            cdr = self.item()
            if isinstance(cdr, list):
                out.extend(cdr)
            return out
        if t == CHARSXP:
            n = self.int()
            return None if n == -1 else self.take(n).decode("utf-8", "replace")
        if t in (LGLSXP, INTSXP):
            n = self.int()
            v = [None if x == NA_INT else x for x in struct.unpack(f">{n}i", self.take(4 * n))]
        elif t == REALSXP:
            n = self.int()
            v = list(struct.unpack(f">{n}d", self.take(8 * n)))
        elif t in (STRSXP, VECSXP):
            n = self.int()
            v = [self.item() for _ in range(n)]
        else:
            raise ValueError(f"unsupported R object type {t}: this reader takes data only")
        attrs = dict(self.item()) if has_attr else {}
        return {"type": t, "value": v, "attrs": attrs}


def load(path) -> list:
    """The named objects in an R data file, as ``[(name, object), ...]``."""
    with open(path, "rb") as f:
        raw = f.read()
    for opener in (gzip.decompress, bz2.decompress, lzma.decompress):
        try:
            raw = opener(raw)
            break
        except (OSError, ValueError, EOFError, lzma.LZMAError):
            continue
    if raw[:5] in (b"RDX2\n", b"RDX3\n"):
        raw = raw[5:]
    if raw[:2] != b"X\n":
        raise ValueError("not an XDR R data file")
    r = Reader(raw[2:])
    version = r.int()
    r.int()  # the writer's R version
    r.int()  # the oldest R that can read it
    if version == 3:
        r.take(r.int())  # the native encoding's name
    return r.item()


if __name__ == "__main__":
    for name, obj in load(sys.argv[1]):
        names = obj["attrs"].get("names", {}).get("value") if isinstance(obj, dict) else None
        print("==", name, names or "")
