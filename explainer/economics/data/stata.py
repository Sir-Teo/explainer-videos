"""A reader for old Stata data files (formats 113, 114 and 115), the binary format of the replication archives the
Data Room draws on.  It parses bytes and nothing else: no code in a file is ever evaluated.  Value labels are read
when present; missing values become NaN (numbers) or the empty string (text).

    from explainer.economics.data.stata import read_dta
    cols, labels = read_dta(path)      # {name: list of values}, {name: variable label}
"""

from __future__ import annotations

import math
import struct

_NUM = {251: ("b", 1), 252: ("h", 2), 253: ("l", 4), 254: ("f", 4), 255: ("d", 8)}
_MISSING = {251: 100, 252: 32740, 253: 2147483620, 254: 1.701e38, 255: 8.988e307}


def _cstr(b: bytes) -> str:
    return b.split(b"\x00", 1)[0].decode("latin-1")


def read_dta(path, value_labels: bool = False):
    """Columns and variable labels of a Stata file in format 113, 114 or 115.  With ``value_labels`` the result
    has a third item, ``{label name: {code: text}}``."""
    raw = open(path, "rb").read()
    fmt, order = raw[0], raw[1]
    if fmt not in (113, 114, 115):
        raise ValueError(f"Stata format {fmt} is not supported (113-115 only)")
    e = "<" if order == 2 else ">"
    nvar, nobs = struct.unpack(e + "Hi", raw[4:10])
    pos = 4 + 2 + 4 + 81 + 18
    types = list(raw[pos:pos + nvar])
    pos += nvar
    names = [_cstr(raw[pos + 33 * k:pos + 33 * (k + 1)]) for k in range(nvar)]
    pos += 33 * nvar
    pos += 2 * (nvar + 1)                                 # sort order
    pos += (12 if fmt == 113 else 49) * nvar              # display formats
    lblnames = [_cstr(raw[pos + 33 * k:pos + 33 * (k + 1)]) for k in range(nvar)]
    pos += 33 * nvar
    labels = [_cstr(raw[pos + 81 * k:pos + 81 * (k + 1)]) for k in range(nvar)]
    pos += 81 * nvar
    while True:                                           # expansion fields
        kind, length = struct.unpack(e + "bi", raw[pos:pos + 5])
        pos += 5
        if kind == 0 and length == 0:
            break
        pos += length
    widths = [(_NUM[t][1] if t in _NUM else t) for t in types]
    rec = sum(widths)
    cols = {n: [] for n in names}
    for i in range(nobs):
        p = pos + i * rec
        for n, t, w in zip(names, types, widths):
            chunk = raw[p:p + w]
            p += w
            if t in _NUM:
                v = struct.unpack(e + _NUM[t][0], chunk)[0]
                if v > _MISSING[t] or (isinstance(v, float) and math.isnan(v)):
                    v = float("nan")
                cols[n].append(v)
            else:
                cols[n].append(_cstr(chunk))
    out = (cols, dict(zip(names, labels)))
    if not value_labels:
        return out
    pos += nobs * rec
    vl: dict = {}
    while pos + 4 <= len(raw):
        (length,) = struct.unpack(e + "i", raw[pos:pos + 4])
        name = _cstr(raw[pos + 4:pos + 37])
        body = raw[pos + 40:pos + 40 + length]
        pos += 40 + length
        n, txtlen = struct.unpack(e + "ii", body[:8])
        offs = struct.unpack(e + f"{n}i", body[8:8 + 4 * n])
        vals = struct.unpack(e + f"{n}i", body[8 + 4 * n:8 + 8 * n])
        txt = body[8 + 8 * n:8 + 8 * n + txtlen]
        vl[name] = {v: _cstr(txt[o:]) for v, o in zip(vals, offs)}
    return out + ({lblnames[k] and names[k]: vl.get(lblnames[k], {}) for k in range(nvar) if lblnames[k]},)
