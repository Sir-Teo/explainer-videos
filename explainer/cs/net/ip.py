"""IP (Part 36): addresses and prefixes, longest-prefix match three ways, aggregation, fragmentation and NAT.

    Prefix.parse("10.1.0.0/16"); p.contains(addr)
    LinearTable, BinaryTrie, MultibitTrie(stride): insert(prefix, hop), lookup(addr) -> hop, with ``.steps`` (memory
    reads in the last lookup)
    routing_table(n, rng)   a synthetic table with a realistic spread of prefix lengths (most /24, many /16-/23)
    aggregate(prefixes)     merge sibling prefixes with the same next hop, repeatedly (CIDR's point)
    fragment(payload_len, mtu, header=20)   (offset in 8-byte units, length, more-fragments) for each fragment
    Nat: a NAPT box mapping (private ip, port) to ports on one public address
"""
from __future__ import annotations

import random


def ip(s: str) -> int:
    a = [int(x) for x in s.split(".")]
    if len(a) != 4 or any(not 0 <= x <= 255 for x in a):
        raise ValueError("IPv4 addresses need four octets in [0, 255]")
    return (a[0] << 24) | (a[1] << 16) | (a[2] << 8) | a[3]


def dotted(x: int) -> str:
    return ".".join(str((x >> s) & 255) for s in (24, 16, 8, 0))


class Prefix:
    __slots__ = ("net", "len")

    def __init__(self, net: int, length: int):
        if not 0 <= net < 2**32 or not 0 <= length <= 32:
            raise ValueError("invalid IPv4 address or prefix length")
        mask = ((1 << length) - 1) << (32 - length) if length else 0
        self.net = net & mask
        self.len = length

    @staticmethod
    def parse(s: str) -> "Prefix":
        a, n = s.split("/")
        return Prefix(ip(a), int(n))

    def contains(self, addr: int) -> bool:
        return self.len == 0 or (addr >> (32 - self.len)) == (self.net >> (32 - self.len))

    def bit(self, i: int) -> int:
        return (self.net >> (31 - i)) & 1

    def __repr__(self):
        return f"{dotted(self.net)}/{self.len}"

    def __eq__(self, o):
        return (self.net, self.len) == (o.net, o.len)

    def __hash__(self):
        return hash((self.net, self.len))


class LinearTable:
    def __init__(self):
        self.rows = []
        self.steps = 0

    def insert(self, p: Prefix, hop):
        self.rows.append((p, hop))

    def lookup(self, addr: int):
        best, bl, self.steps = None, -1, 0
        for p, h in self.rows:
            self.steps += 1
            if p.len >= bl and p.contains(addr):
                best, bl = h, p.len
        return best


class BinaryTrie:
    """One bit per level; remember the last node with a next hop on the way down."""

    def __init__(self):
        self.root = [None, None, None]          # left, right, hop
        self.nodes = 1
        self.steps = 0

    def insert(self, p: Prefix, hop):
        n = self.root
        for i in range(p.len):
            b = p.bit(i)
            if n[b] is None:
                n[b] = [None, None, None]
                self.nodes += 1
            n = n[b]
        n[2] = hop

    def lookup(self, addr: int):
        n, best, self.steps = self.root, self.root[2], 1
        for i in range(32):
            n = n[(addr >> (31 - i)) & 1]
            if n is None:
                break
            self.steps += 1
            if n[2] is not None:
                best = n[2]
        return best


class MultibitTrie:
    """Stride s bits per level, with controlled prefix expansion: a prefix whose length is not a multiple of s is
    expanded into every longer one at the next multiple (Srinivasan and Varghese)."""

    def __init__(self, stride: int = 8):
        if stride not in (1, 2, 4, 8):
            raise ValueError("supported strides are 1, 2, 4, and 8 bits")
        self.s = stride
        self.root = {"kids": {}, "hop": {}}
        self.nodes = 1
        self.steps = 0

    def insert(self, p: Prefix, hop):
        s = self.s
        n = self.root
        depth = 0
        while p.len - depth > s:
            chunk = (p.net >> (32 - depth - s)) & ((1 << s) - 1)
            if chunk not in n["kids"]:
                n["kids"][chunk] = {"kids": {}, "hop": {}}
                self.nodes += 1
            n = n["kids"][chunk]
            depth += s
        rest = p.len - depth
        base = (p.net >> (32 - depth - s)) & ((1 << s) - 1) if depth + s <= 32 else 0
        for k in range(1 << (s - rest)):
            slot = (base & ~((1 << (s - rest)) - 1)) | k
            old = n["hop"].get(slot)
            if old is None or old[1] <= p.len:
                n["hop"][slot] = (hop, p.len)

    def lookup(self, addr: int):
        s, n, best, depth, self.steps = self.s, self.root, None, 0, 0
        while n is not None and depth < 32:
            chunk = (addr >> (32 - depth - s)) & ((1 << s) - 1)
            self.steps += 1
            h = n["hop"].get(chunk)
            if h is not None:
                best = h[0]
            n = n["kids"].get(chunk)
            depth += s
        return best


# share of IPv4 BGP prefixes by length, roughly as in 2024 tables (the /24s are about 60 percent)
LENGTHS = {8: 0.00002, 12: 0.0003, 14: 0.001, 16: 0.012, 17: 0.008, 18: 0.014, 19: 0.025, 20: 0.04, 21: 0.05,
           22: 0.12, 23: 0.11, 24: 0.6195}


def routing_table(n: int, rng: random.Random, hops: int = 16) -> list[tuple[Prefix, int]]:
    lens, w = zip(*LENGTHS.items())
    out = set()
    rows = []
    while len(rows) < n:
        L = rng.choices(lens, w)[0]
        p = Prefix(rng.getrandbits(32), L)
        if (p.net, p.len) in out:
            continue
        out.add((p.net, p.len))
        rows.append((p, rng.randrange(hops)))
    return rows


def aggregate(rows: list[tuple[Prefix, int]]) -> list[tuple[Prefix, int]]:
    """Repeatedly replace two sibling prefixes (same length, same parent) with the same next hop by their parent."""
    cur = {(p.net, p.len): h for p, h in rows}
    changed = True
    while changed:
        changed = False
        for (net, L), h in list(cur.items()):
            if L == 0 or (net, L) not in cur:
                continue
            sib = net ^ (1 << (32 - L))
            if cur.get((sib, L)) == h:
                parent = (net & ~(1 << (32 - L)), L - 1)
                if parent in cur and cur[parent] != h:
                    continue
                del cur[(net, L)]
                del cur[(sib, L)]
                cur[parent] = h
                changed = True
    return [(Prefix(n, L), h) for (n, L), h in cur.items()]


def fragment(payload_len: int, mtu: int, header: int = 20) -> list[tuple[int, int, bool]]:
    """IPv4 payload fragments; only non-final fragments need eight-byte alignment."""
    if header not in range(20, 61, 4) or not 0 <= payload_len <= 65535 - header or mtu < header:
        raise ValueError("invalid IPv4 payload, header size, or MTU")
    capacity = mtu - header
    per = (mtu - header) // 8 * 8
    if payload_len > capacity and per == 0:
        raise ValueError("MTU cannot hold an eight-byte non-final fragment")
    out, off = [], 0
    while off < payload_len:
        remaining = payload_len - off
        n = remaining if remaining <= capacity else per
        out.append((off // 8, n, off + n < payload_len))
        off += n
    return out


class Nat:
    def __init__(self, public: str, first_port: int = 40000):
        self.public = public
        self.next = first_port
        self.out: dict = {}
        self.back: dict = {}

    def outbound(self, src: str, sport: int) -> tuple[str, int]:
        k = (src, sport)
        if k not in self.out:
            self.out[k] = self.next
            self.back[self.next] = k
            self.next += 1
        return self.public, self.out[k]

    def inbound(self, dport: int):
        return self.back.get(dport)


def checksum(data: bytes) -> int:
    """The Internet checksum: the ones'-complement of the ones'-complement sum of 16-bit words (RFC 1071)."""
    if len(data) % 2:
        data += b"\0"
    s = sum(int.from_bytes(data[i:i + 2], "big") for i in range(0, len(data), 2))
    while s >> 16:
        s = (s & 0xFFFF) + (s >> 16)
    return ~s & 0xFFFF


def ipv4_header(src: str, dst: str, proto: int, payload_len: int, ttl: int = 64, ident: int = 1) -> bytes:
    h = bytearray(20)
    h[0] = 0x45                                     # version 4, header length 5 words
    h[2:4] = (20 + payload_len).to_bytes(2, "big")
    h[4:6] = ident.to_bytes(2, "big")
    h[6:8] = (0x4000).to_bytes(2, "big")            # don't fragment
    h[8] = ttl
    h[9] = proto
    h[12:16] = ip(src).to_bytes(4, "big")
    h[16:20] = ip(dst).to_bytes(4, "big")
    h[10:12] = checksum(bytes(h)).to_bytes(2, "big")
    return bytes(h)


def udp_header(sport: int, dport: int, payload: bytes, src: str, dst: str) -> bytes:
    length = 8 + len(payload)
    pseudo = ip(src).to_bytes(4, "big") + ip(dst).to_bytes(4, "big") + bytes([0, 17]) + length.to_bytes(2, "big")
    h = sport.to_bytes(2, "big") + dport.to_bytes(2, "big") + length.to_bytes(2, "big") + b"\0\0"
    c = checksum(pseudo + h + payload) or 0xFFFF
    return h[:6] + c.to_bytes(2, "big")
