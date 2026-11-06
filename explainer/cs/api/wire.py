"""Serialization (Part 43): Protocol Buffers' wire format from first principles (varints, zigzag, tags and wire
types, length-delimited fields), checked against the examples in the published encoding documentation; JSON's
numbers as IEEE doubles; and a schema-compatibility checker that treats evolution as a subtyping question."""

from __future__ import annotations

import json
import struct

VARINT, I64, LEN, I32 = 0, 1, 2, 5


def varint(n: int) -> bytes:
    """Seven bits per byte, least significant group first; the top bit says another byte follows.  Negative int32
    and int64 values are encoded as their 64-bit two's complement, ten bytes."""
    if n < 0:
        n += 1 << 64
    out = bytearray()
    while True:
        b = n & 0x7F
        n >>= 7
        if n:
            out.append(b | 0x80)
        else:
            out.append(b)
            return bytes(out)


def read_varint(buf: bytes, i: int = 0):
    shift = n = 0
    while True:
        b = buf[i]
        n |= (b & 0x7F) << shift
        i += 1
        if not b & 0x80:
            return n, i
        shift += 7


def zigzag(n: int, bits: int = 64) -> int:
    """Interleave signed values: 0, -1, 1, -2, 2 ... map to 0, 1, 2, 3, 4, so small negatives stay short."""
    return (n << 1) ^ (n >> (bits - 1))


def unzigzag(z: int) -> int:
    return (z >> 1) ^ -(z & 1)


def tag(field: int, wire_type: int) -> bytes:
    return varint(field << 3 | wire_type)


def encode(fields) -> bytes:
    """fields: (number, kind, value) with kind in int, sint, string, bytes, double, message, packed."""
    out = bytearray()
    for num, kind, v in fields:
        if kind == "int":
            out += tag(num, VARINT) + varint(v)
        elif kind == "sint":
            out += tag(num, VARINT) + varint(zigzag(v))
        elif kind == "bool":
            out += tag(num, VARINT) + varint(int(v))
        elif kind == "double":
            out += tag(num, I64) + struct.pack("<d", v)
        elif kind in ("string", "bytes"):
            b = v.encode() if kind == "string" else v
            out += tag(num, LEN) + varint(len(b)) + b
        elif kind == "message":
            b = encode(v)
            out += tag(num, LEN) + varint(len(b)) + b
        elif kind == "packed":
            b = b"".join(varint(x) for x in v)
            out += tag(num, LEN) + varint(len(b)) + b
    return bytes(out)


def decode(buf: bytes):
    """Generic decoding without a schema, as an old reader sees new data: (field, wire type, raw value)."""
    i, out = 0, []
    while i < len(buf):
        key, i = read_varint(buf, i)
        num, wt = key >> 3, key & 7
        if wt == VARINT:
            v, i = read_varint(buf, i)
        elif wt == I64:
            v, i = buf[i:i + 8], i + 8
        elif wt == I32:
            v, i = buf[i:i + 4], i + 4
        elif wt == LEN:
            n, i = read_varint(buf, i)
            v, i = buf[i:i + n], i + n
        else:
            raise ValueError(f"wire type {wt}")
        out.append((num, wt, v))
    return out


# Examples from the Protocol Buffers encoding documentation (protobuf.dev/programming-guides/encoding).
PUBLISHED = {
    "varint 1": (varint(1), "01"),
    "varint 150": (varint(150), "9601"),
    "message {a: 150}": (encode([(1, "int", 150)]), "089601"),
    "message {b: \"testing\"}": (encode([(2, "string", "testing")]), "120774657374696e67"),
    "message {c: {a: 150}}": (encode([(3, "message", [(1, "int", 150)])]), "1a03089601"),
    "packed [3, 270, 86942]": (encode([(4, "packed", [3, 270, 86942])]), "2206038e029ea705"),
    "int32 -2": (varint(-2), "feffffffffffffffff01"),
    "sint32 -2": (varint(zigzag(-2, 32)), "03"),
}
ZIGZAG_TABLE = [(0, 0), (-1, 1), (1, 2), (-2, 3), (2147483647, 4294967294), (-2147483648, 4294967295)]


def check_published():
    rows = [(k, b.hex(), want, b.hex() == want) for k, (b, want) in PUBLISHED.items()]
    zz = [(n, zigzag(n, 32), z, zigzag(n, 32) == z and unzigzag(z) == n) for n, z in ZIGZAG_TABLE]
    return {"encodings": rows, "zigzag": zz}


def varint_sizes():
    """Bytes needed for each power-of-two range, for unsigned varints and for negative numbers with and without
    zigzag."""
    rows = []
    for v in (0, 1, 127, 128, 300, 16_383, 16_384, 2 ** 21, 2 ** 28, 2 ** 35, 2 ** 63):
        rows.append({"value": v, "bytes": len(varint(v))})
    neg = [{"value": v, "int": len(varint(v)), "sint": len(varint(zigzag(v)))} for v in (-1, -2, -64, -65, -1000)]
    return {"unsigned": rows, "negative": neg}


def size_comparison(record=None):
    """One record as JSON and as protobuf."""
    record = record or {"id": 150, "word": "whale", "count": 1226, "novel": "Moby-Dick", "score": -2,
                        "tags": [3, 270, 86942]}
    js = json.dumps(record, separators=(",", ":")).encode()
    pb = encode([(1, "int", record["id"]), (2, "string", record["word"]), (3, "int", record["count"]),
                 (4, "string", record["novel"]), (5, "sint", record["score"]), (6, "packed", record["tags"])])
    return {"record": record, "json": js.decode(), "json_bytes": len(js), "proto_hex": pb.hex(),
            "proto_bytes": len(pb)}


def json_doubles():
    """JSON numbers are read as IEEE doubles by JavaScript: integers beyond 2^53 lose their last digits."""
    rows = []
    for n in (2 ** 53 - 1, 2 ** 53, 2 ** 53 + 1, 2 ** 53 + 2, 1_234_567_890_123_456_789):
        d = float(n)
        rows.append({"sent": n, "received": int(d), "exact": int(d) == n})
    tweet = 1_234_567_890_123_456_789
    return {"rows": rows, "max_safe": 2 ** 53 - 1, "example": {"sent": tweet, "received": int(float(tweet))}}


# ---------------------------------------------------------------- schema evolution

def compatible(writer: dict, reader: dict):
    """Schemas as {field number: (name, type, required)}.  A reader can decode a writer's data when every field the
    reader requires is present in the writer with the same type, and fields with the same number agree on type.
    Unknown fields are skipped (protobuf keeps them).  Returns a list of problems; empty means compatible."""
    problems = []
    for num, (name, typ, req) in reader.items():
        if num in writer:
            wname, wtyp, _ = writer[num]
            if wtyp != typ and {wtyp, typ} - {"int32", "int64", "uint32", "uint64", "bool"}:
                problems.append(f"field {num} ({name}): {wtyp} written, read as {typ}")
        elif req:
            problems.append(f"field {num} ({name}) is required but the writer never sends it")
    return problems


def evolution_cases():
    v1 = {1: ("word", "string", True), 2: ("count", "int64", False)}
    cases = {
        "add an optional field": {**v1, 3: ("novel", "string", False)},
        "add a required field": {**v1, 3: ("novel", "string", True)},
        "remove an optional field": {1: ("word", "string", True)},
        "remove a required field": {2: ("count", "int64", False)},
        "change a field's type": {1: ("word", "string", True), 2: ("count", "string", False)},
        "renumber a field": {1: ("word", "string", True), 5: ("count", "int64", False)},
        "widen int32 to int64": {1: ("word", "string", True), 2: ("count", "int64", False)},
    }
    out = []
    for name, v2 in cases.items():
        back = compatible(v1, v2)        # new code reads old data
        fwd = compatible(v2, v1)         # old code reads new data
        out.append({"change": name, "backward": not back, "forward": not fwd, "problems": back + fwd})
    return out
