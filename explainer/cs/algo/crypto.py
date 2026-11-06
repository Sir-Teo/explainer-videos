"""Symmetric cryptography for Part 29 of *Computer Science, Built* ("Secrets").

Everything is written from the definitions and checked against published test vectors or Python's ``hashlib``/
``hmac`` in tests/test_cs29_crypto.py:

* classical ciphers and their breaks: Caesar, substitution (hill climbing on quadgram scores), Vigenere (index of
  coincidence, chi-squared per column);
* Enigma I (rotors I-V, reflector B, plugboard, double stepping) and Rejewski's cycle structures;
* the one-time pad and the two-time pad's crib dragging;
* LFSRs and their break by Berlekamp-Massey over GF(2); ChaCha20 (RFC 8439);
* the GGM tree and Feistel networks;
* AES-128 (FIPS-197) with round-by-round states; ECB, CBC with PKCS#7, CTR; Vaudenay's padding-oracle attack;
* CBC-MAC and its forgery; SHA-256 (FIPS 180-4) and the length-extension attack; HMAC; GHASH and AES-GCM;
  Keccak-f[1600] and SHA3-256;
* birthday collisions; Merkle trees;
* a toy 16-bit SPN (Heys) with a differential attack, and meet-in-the-middle on double encryption;
* an early-exit comparison to time, and a PID-seeded key generator to brute-force.
"""

from __future__ import annotations

import math
import random
import struct
import time
from collections import Counter

A2Z = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
ENGLISH_FREQ = {  # relative letter frequencies of English text (Lewand)
    "A": .08167, "B": .01492, "C": .02782, "D": .04253, "E": .12702, "F": .02228, "G": .02015, "H": .06094,
    "I": .06966, "J": .00153, "K": .00772, "L": .04025, "M": .02406, "N": .06749, "O": .07507, "P": .01929,
    "Q": .00095, "R": .05987, "S": .06327, "T": .09056, "U": .02758, "V": .00978, "W": .02360, "X": .00150,
    "Y": .01974, "Z": .00074}


# ----------------------------------------------------------------------------------------------- classical

def letters(text):
    return "".join(c for c in text.upper() if c in A2Z)


def caesar(text, k):
    return "".join(A2Z[(A2Z.index(c) + k) % 26] for c in letters(text))


def subst(text, key):
    """key: a 26-letter string, the image of A..Z."""
    return "".join(key[A2Z.index(c)] for c in letters(text))


def invert_key(key):
    inv = [""] * 26
    for i, c in enumerate(key):
        inv[A2Z.index(c)] = A2Z[i]
    return "".join(inv)


def quadgram_model(text):
    t = letters(text)
    counts = Counter(t[i:i + 4] for i in range(len(t) - 3))
    total = sum(counts.values())
    floor = math.log10(0.01 / total)
    return {q: math.log10(c / total) for q, c in counts.items()}, floor


def quad_score(text, model):
    table, floor = model
    return sum(table.get(text[i:i + 4], floor) for i in range(len(text) - 3))


def break_substitution(ct, model, rng, restarts=8, iters=3000):
    """Hill climbing over decryption keys by random swaps. Returns (decryption key, plaintext, score trace)."""
    best_key, best_score, trace, finals = None, -1e18, [], []
    freq_order = [c for c, _ in Counter(ct).most_common()] + [c for c in A2Z if c not in ct]
    eng_order = sorted(A2Z, key=lambda c: -ENGLISH_FREQ[c])
    start = [""] * 26                                   # start from frequency matching (al-Kindi)
    for c, e in zip(freq_order, eng_order):
        start[A2Z.index(c)] = e
    break_substitution.rank_start = "".join(start[A2Z.index(c)] for c in ct)
    for r in range(restarts):
        key = list(start)
        if r:
            for _ in range(8):
                i, j = rng.sample(range(26), 2)
                key[i], key[j] = key[j], key[i]
        dec = lambda k: "".join(k[A2Z.index(c)] for c in ct)   # noqa: E731
        score = quad_score(dec(key), model)
        cur = [(0, score, dec(key)[:60])]
        stale = 0
        while stale < iters:
            i, j = rng.sample(range(26), 2)
            key[i], key[j] = key[j], key[i]
            s = quad_score(dec(key), model)
            if s > score:
                score, stale = s, 0
                cur.append((len(cur), score, dec(key)[:60]))
            else:
                key[i], key[j] = key[j], key[i]
                stale += 1
        finals.append(score)
        if score > best_score:
            best_key, best_score, trace = "".join(key), score, cur
    break_substitution.finals = finals
    return best_key, "".join(best_key[A2Z.index(c)] for c in ct), trace


def vigenere(text, key, decrypt=False):
    t = letters(text)
    k = [A2Z.index(c) for c in key]
    sgn = -1 if decrypt else 1
    return "".join(A2Z[(A2Z.index(c) + sgn * k[i % len(k)]) % 26] for i, c in enumerate(t))


def ioc(text):
    n = len(text)
    c = Counter(text)
    return sum(v * (v - 1) for v in c.values()) / (n * (n - 1)) if n > 1 else 0.0


def vigenere_key_length(ct, max_len=20):
    """Average index of coincidence of the columns, for each candidate length."""
    return {L: sum(ioc(ct[i::L]) for i in range(L)) / L for L in range(1, max_len + 1)}


def chi_squared_shift(col):
    """The Caesar shift whose decryption best fits English letter frequencies."""
    n = len(col)
    best = None
    for s in range(26):
        c = Counter(A2Z[(A2Z.index(x) - s) % 26] for x in col)
        chi = sum((c.get(L, 0) - n * f) ** 2 / (n * f) for L, f in ENGLISH_FREQ.items())
        if best is None or chi < best[0]:
            best = (chi, s)
    return best[1]


def break_vigenere(ct, max_len=20):
    scores = vigenere_key_length(ct, max_len)
    L = min((L for L, s in scores.items() if s > 0.06), default=max(scores, key=scores.get))
    key = "".join(A2Z[chi_squared_shift(ct[i::L])] for i in range(L))
    return key, vigenere(ct, key, decrypt=True), scores


# ----------------------------------------------------------------------------------------------- Enigma

ROTORS = {"I": ("EKMFLGDQVZNTOWYHXUSPAIBRCJ", "Q"), "II": ("AJDKSIRUXBLHWTMCQGZNPYFVOE", "E"),
          "III": ("BDFHJLCPRTXVZNYEIWGAKMUSQO", "V"), "IV": ("ESOVPZJAYQUIRHXLNFTGKDCMWB", "J"),
          "V": ("VZBRGITYUPSDNHLXAWMJQOFECK", "Z")}
REFLECTOR_B = "YRUHQSLDPXNGOKMIEBFZCWVJAT"


class Enigma:
    """Enigma I. rotors: left to right, e.g. ("I", "II", "III"); positions and rings as letters."""

    def __init__(self, rotors=("I", "II", "III"), positions="AAA", rings="AAA", plugs=""):
        self.wiring = [ROTORS[r][0] for r in rotors]
        self.notch = [ROTORS[r][1] for r in rotors]
        self.inv = []
        for w in self.wiring:
            inv = [""] * 26
            for i, c in enumerate(w):
                inv[A2Z.index(c)] = A2Z[i]
            self.inv.append("".join(inv))
        self.pos = [A2Z.index(c) for c in positions]
        self.ring = [A2Z.index(c) for c in rings]
        self.plug = {c: c for c in A2Z}
        for pair in plugs.split():
            a, b = pair[0], pair[1]
            self.plug[a], self.plug[b] = b, a

    def step(self):
        l, m, r = self.pos
        if A2Z[m] == self.notch[1]:                      # double stepping
            self.pos[0] = (l + 1) % 26
            self.pos[1] = (m + 1) % 26
        elif A2Z[r] == self.notch[2]:
            self.pos[1] = (m + 1) % 26
        self.pos[2] = (self.pos[2] + 1) % 26

    def _through(self, c, i, forward):
        shift = self.pos[i] - self.ring[i]
        x = (A2Z.index(c) + shift) % 26
        y = A2Z.index((self.wiring[i] if forward else self.inv[i])[x])
        return A2Z[(y - shift) % 26]

    def press(self, c):
        self.step()
        return self.letter(c)

    def letter(self, c):
        """Encrypt one letter at the current positions, without stepping."""
        c = self.plug[c]
        for i in (2, 1, 0):
            c = self._through(c, i, True)
        c = REFLECTOR_B[A2Z.index(c)]
        for i in (0, 1, 2):
            c = self._through(c, i, False)
        return self.plug[c]

    def encrypt(self, text):
        return "".join(self.press(c) for c in letters(text))

    def permutation(self):
        return "".join(self.letter(c) for c in A2Z)


def cycles(perm):
    """Cycle decomposition of a permutation given as the image string of A..Z."""
    seen, out = set(), []
    for s in A2Z:
        if s in seen:
            continue
        cyc, c = [], s
        while c not in seen:
            seen.add(c)
            cyc.append(c)
            c = perm[A2Z.index(c)]
        out.append("".join(cyc))
    return out


def compose(p, q):
    """x -> q(p(x)): first p, then q."""
    return "".join(q[A2Z.index(p[A2Z.index(c)])] for c in A2Z)


def rejewski_characteristic(rotors, positions, plugs):
    """The permutations A1..A6 of six successive key presses; the products A1A4, A2A5, A3A6 and their cycle
    lengths (Rejewski's 'characteristic'), which the plugboard cannot change."""
    e = Enigma(rotors, positions, "AAA", plugs)
    A = []
    for _ in range(6):
        e.step()
        A.append(e.permutation())
    prods = [compose(A[i], A[i + 3]) for i in range(3)]
    return [sorted((len(c) for c in cycles(p)), reverse=True) for p in prods], prods


# ----------------------------------------------------------------------------------------------- one-time pad

def xor(a, b):
    return bytes(x ^ y for x, y in zip(a, b))


def crib_drag(c1, c2, crib):
    """Slide a guessed word along c1 xor c2; at each offset, what the other message would read."""
    x = xor(c1, c2)
    out = []
    for i in range(len(x) - len(crib) + 1):
        out.append((i, xor(x[i:i + len(crib)], crib)))
    return out


# ----------------------------------------------------------------------------------------------- LFSR, BM over GF(2)

def lfsr(taps, state, n):
    """Fibonacci LFSR: s_{t+L} = XOR of s_{t+L-i} for i in taps (1..L). state: first L bits."""
    s = list(state)
    while len(s) < n:
        s.append(sum(s[len(s) - i] for i in taps) & 1)
    return s[:n]


def berlekamp_massey_gf2(s):
    """Shortest LFSR generating s: (L, connection polynomial C as a list, C[0] = 1)."""
    n = len(s)
    C, B = [1] + [0] * n, [1] + [0] * n
    L, m = 0, 1
    for i in range(n):
        d = s[i]
        for j in range(1, L + 1):
            d ^= C[j] & s[i - j]
        if d == 0:
            m += 1
        elif 2 * L <= i:
            T = C[:]
            for j in range(n + 1 - m):
                C[j + m] ^= B[j]
            L, B, m = i + 1 - L, T, 1
        else:
            for j in range(n + 1 - m):
                C[j + m] ^= B[j]
            m += 1
    return L, C[:L + 1]


def lfsr_from_connection(C, seed, n):
    L = len(C) - 1
    s = list(seed[:L])
    while len(s) < n:
        s.append(sum(C[j] & s[len(s) - j] for j in range(1, L + 1)) & 1)
    return s


# ----------------------------------------------------------------------------------------------- ChaCha20

def _rotl32(v, c):
    return ((v << c) & 0xFFFFFFFF) | (v >> (32 - c))


def quarter_round(a, b, c, d):
    a = (a + b) & 0xFFFFFFFF
    d = _rotl32(d ^ a, 16)
    c = (c + d) & 0xFFFFFFFF
    b = _rotl32(b ^ c, 12)
    a = (a + b) & 0xFFFFFFFF
    d = _rotl32(d ^ a, 8)
    c = (c + d) & 0xFFFFFFFF
    b = _rotl32(b ^ c, 7)
    return a, b, c, d


def chacha20_block(key, counter, nonce):
    const = [0x61707865, 0x3320646E, 0x79622D32, 0x6B206574]
    st = const + list(struct.unpack("<8I", key)) + [counter] + list(struct.unpack("<3I", nonce))
    x = list(st)
    for _ in range(10):
        for a, b, c, d in ((0, 4, 8, 12), (1, 5, 9, 13), (2, 6, 10, 14), (3, 7, 11, 15),
                           (0, 5, 10, 15), (1, 6, 11, 12), (2, 7, 8, 13), (3, 4, 9, 14)):
            x[a], x[b], x[c], x[d] = quarter_round(x[a], x[b], x[c], x[d])
    return struct.pack("<16I", *[(x[i] + st[i]) & 0xFFFFFFFF for i in range(16)])


def chacha20_encrypt(key, counter, nonce, data):
    out = bytearray()
    for i in range(0, len(data), 64):
        ks = chacha20_block(key, counter + i // 64, nonce)
        out += bytes(a ^ b for a, b in zip(data[i:i + 64], ks))
    return bytes(out)


# ----------------------------------------------------------------------------------------------- GF(2^8), AES

def _gmul(a, b, poly=0x11B):
    r = 0
    while b:
        if b & 1:
            r ^= a
        b >>= 1
        a <<= 1
        if a & 0x100:
            a ^= poly
    return r


def _ginv(a):
    if a == 0:
        return 0
    r = 1
    for _ in range(254):          # a^254 = a^-1 in GF(2^8)
        r = _gmul(r, a)
    return r


def _affine(b):
    c = 0x63
    out = 0
    for i in range(8):
        bit = ((b >> i) ^ (b >> ((i + 4) % 8)) ^ (b >> ((i + 5) % 8)) ^ (b >> ((i + 6) % 8))
               ^ (b >> ((i + 7) % 8)) ^ (c >> i)) & 1
        out |= bit << i
    return out


SBOX = [_affine(_ginv(x)) for x in range(256)]
INV_SBOX = [0] * 256
for _i, _v in enumerate(SBOX):
    INV_SBOX[_v] = _i
RCON = [0x01, 0x02, 0x04, 0x08, 0x10, 0x20, 0x40, 0x80, 0x1B, 0x36]
MUL2 = [_gmul(x, 2) for x in range(256)]
MUL3 = [_gmul(x, 3) for x in range(256)]


def key_expansion(key):
    w = [list(key[4 * i:4 * i + 4]) for i in range(4)]
    for i in range(4, 44):
        t = list(w[i - 1])
        if i % 4 == 0:
            t = t[1:] + t[:1]
            t = [SBOX[b] for b in t]
            t[0] ^= RCON[i // 4 - 1]
        w.append([a ^ b for a, b in zip(w[i - 4], t)])
    return [sum(w[4 * r:4 * r + 4], []) for r in range(11)]


def _sub_bytes(s):
    return [SBOX[b] for b in s]


def _shift_rows(s):
    # state is column-major: s[r + 4c]
    return [s[(r + 4 * ((c + r) % 4))] for c in range(4) for r in range(4)]


def _mix_columns(s):
    out = []
    for c in range(4):
        a = s[4 * c:4 * c + 4]
        out += [MUL2[a[0]] ^ MUL3[a[1]] ^ a[2] ^ a[3], a[0] ^ MUL2[a[1]] ^ MUL3[a[2]] ^ a[3],
                a[0] ^ a[1] ^ MUL2[a[2]] ^ MUL3[a[3]], MUL3[a[0]] ^ a[1] ^ a[2] ^ MUL2[a[3]]]
    return out


def _add(s, k):
    return [a ^ b for a, b in zip(s, k)]


def aes_encrypt_block(block, round_keys, rounds=10, trace=False):
    s = _add(list(block), round_keys[0])
    steps = [("AddRoundKey 0", s)] if trace else None
    for r in range(1, rounds + 1):
        s = _sub_bytes(s)
        if trace:
            steps.append((f"SubBytes {r}", s))
        s = _shift_rows(s)
        if trace:
            steps.append((f"ShiftRows {r}", s))
        if r != 10:
            s = _mix_columns(s)
            if trace:
                steps.append((f"MixColumns {r}", s))
        s = _add(s, round_keys[r])
        if trace:
            steps.append((f"AddRoundKey {r}", s))
    return (bytes(s), steps) if trace else bytes(s)


def _inv_shift_rows(s):
    return [s[(r + 4 * ((c - r) % 4))] for c in range(4) for r in range(4)]


def _inv_mix_columns(s):
    out = []
    for c in range(4):
        a = s[4 * c:4 * c + 4]
        out += [_gmul(a[0], 14) ^ _gmul(a[1], 11) ^ _gmul(a[2], 13) ^ _gmul(a[3], 9),
                _gmul(a[0], 9) ^ _gmul(a[1], 14) ^ _gmul(a[2], 11) ^ _gmul(a[3], 13),
                _gmul(a[0], 13) ^ _gmul(a[1], 9) ^ _gmul(a[2], 14) ^ _gmul(a[3], 11),
                _gmul(a[0], 11) ^ _gmul(a[1], 13) ^ _gmul(a[2], 9) ^ _gmul(a[3], 14)]
    return out


def aes_decrypt_block(block, round_keys):
    s = _add(list(block), round_keys[10])
    for r in range(9, -1, -1):
        s = _inv_shift_rows(s)
        s = [INV_SBOX[b] for b in s]
        s = _add(s, round_keys[r])
        if r:
            s = _inv_mix_columns(s)
    return bytes(s)


class AES:
    def __init__(self, key):
        self.rk = key_expansion(key)

    def enc(self, b):
        return aes_encrypt_block(b, self.rk)

    def dec(self, b):
        return aes_decrypt_block(b, self.rk)


def bit_diff(a, b):
    return sum(bin(x ^ y).count("1") for x, y in zip(a, b))


def avalanche_by_round(rng, trials=200):
    """Flip one random plaintext bit; how many of the 128 state bits differ after each round?"""
    out = [[0] * 11 for _ in range(trials)]
    for t in range(trials):
        key = bytes(rng.randrange(256) for _ in range(16))
        rk = key_expansion(key)
        p = bytes(rng.randrange(256) for _ in range(16))
        bit = rng.randrange(128)
        q = bytearray(p)
        q[bit // 8] ^= 1 << (bit % 8)
        _, sa = aes_encrypt_block(p, rk, trace=True)
        _, sb = aes_encrypt_block(bytes(q), rk, trace=True)
        ka = [s for name, s in sa if name.startswith("AddRoundKey")]
        kb = [s for name, s in sb if name.startswith("AddRoundKey")]
        for r in range(11):
            out[t][r] = bit_diff(ka[r], kb[r])
    return out


# ----------------------------------------------------------------------------------------------- modes

def pkcs7_pad(data, n=16):
    k = n - len(data) % n
    return data + bytes([k]) * k


def pkcs7_unpad(data):
    k = data[-1]
    if k < 1 or k > 16 or data[-k:] != bytes([k]) * k:
        raise ValueError("bad padding")
    return data[:-k]


def ecb_encrypt(aes, data):
    return b"".join(aes.enc(data[i:i + 16]) for i in range(0, len(data), 16))


def cbc_encrypt(aes, iv, data):
    out, prev = [], iv
    for i in range(0, len(data), 16):
        prev = aes.enc(xor(data[i:i + 16], prev))
        out.append(prev)
    return b"".join(out)


def cbc_decrypt(aes, iv, data):
    out, prev = [], iv
    for i in range(0, len(data), 16):
        blk = data[i:i + 16]
        out.append(xor(aes.dec(blk), prev))
        prev = blk
    return b"".join(out)


def ctr_encrypt(aes, nonce8, data):
    out = bytearray()
    for i in range(0, len(data), 16):
        ks = aes.enc(nonce8 + struct.pack(">Q", i // 16))
        out += xor(data[i:i + 16], ks)
    return bytes(out)


def padding_oracle_attack(iv, ct, oracle):
    """Vaudenay (2002): recover the plaintext of a CBC ciphertext using only a valid-padding oracle.
    Returns (plaintext with padding, number of oracle queries)."""
    blocks = [iv] + [ct[i:i + 16] for i in range(0, len(ct), 16)]
    plain = b""
    queries = 0
    for b in range(1, len(blocks)):
        prev, cur = blocks[b - 1], blocks[b]
        inter = [0] * 16                     # D_K(cur)
        for pos in range(15, -1, -1):
            pad = 16 - pos
            found = None
            for g in range(256):
                fake = bytearray(16)
                for j in range(pos + 1, 16):
                    fake[j] = inter[j] ^ pad
                fake[pos] = g
                queries += 1
                if oracle(bytes(fake), cur):
                    if pos == 15:                # rule out a longer accidental padding
                        fake2 = bytearray(fake)
                        fake2[14] ^= 1
                        queries += 1
                        if not oracle(bytes(fake2), cur):
                            continue
                    found = g
                    break
            inter[pos] = found ^ pad
        plain += xor(bytes(inter), prev)
    return plain, queries


# ----------------------------------------------------------------------------------------------- MACs, hashes

_K256 = [0x428a2f98, 0x71374491, 0xb5c0fbcf, 0xe9b5dba5, 0x3956c25b, 0x59f111f1, 0x923f82a4, 0xab1c5ed5,
         0xd807aa98, 0x12835b01, 0x243185be, 0x550c7dc3, 0x72be5d74, 0x80deb1fe, 0x9bdc06a7, 0xc19bf174,
         0xe49b69c1, 0xefbe4786, 0x0fc19dc6, 0x240ca1cc, 0x2de92c6f, 0x4a7484aa, 0x5cb0a9dc, 0x76f988da,
         0x983e5152, 0xa831c66d, 0xb00327c8, 0xbf597fc7, 0xc6e00bf3, 0xd5a79147, 0x06ca6351, 0x14292967,
         0x27b70a85, 0x2e1b2138, 0x4d2c6dfc, 0x53380d13, 0x650a7354, 0x766a0abb, 0x81c2c92e, 0x92722c85,
         0xa2bfe8a1, 0xa81a664b, 0xc24b8b70, 0xc76c51a3, 0xd192e819, 0xd6990624, 0xf40e3585, 0x106aa070,
         0x19a4c116, 0x1e376c08, 0x2748774c, 0x34b0bcb5, 0x391c0cb3, 0x4ed8aa4a, 0x5b9cca4f, 0x682e6ff3,
         0x748f82ee, 0x78a5636f, 0x84c87814, 0x8cc70208, 0x90befffa, 0xa4506ceb, 0xbef9a3f7, 0xc67178f2]
_H256 = [0x6a09e667, 0xbb67ae85, 0x3c6ef372, 0xa54ff53a, 0x510e527f, 0x9b05688c, 0x1f83d9ab, 0x5be0cd19]


def _rotr(x, n):
    return (x >> n) | ((x << (32 - n)) & 0xFFFFFFFF)


def _sha256_compress(h, block):
    w = list(struct.unpack(">16I", block))
    for i in range(16, 64):
        s0 = _rotr(w[i - 15], 7) ^ _rotr(w[i - 15], 18) ^ (w[i - 15] >> 3)
        s1 = _rotr(w[i - 2], 17) ^ _rotr(w[i - 2], 19) ^ (w[i - 2] >> 10)
        w.append((w[i - 16] + s0 + w[i - 7] + s1) & 0xFFFFFFFF)
    a, b, c, d, e, f, g, hh = h
    for i in range(64):
        S1 = _rotr(e, 6) ^ _rotr(e, 11) ^ _rotr(e, 25)
        ch = (e & f) ^ (~e & g)
        t1 = (hh + S1 + ch + _K256[i] + w[i]) & 0xFFFFFFFF
        S0 = _rotr(a, 2) ^ _rotr(a, 13) ^ _rotr(a, 22)
        maj = (a & b) ^ (a & c) ^ (b & c)
        t2 = (S0 + maj) & 0xFFFFFFFF
        hh, g, f, e, d, c, b, a = g, f, e, (d + t1) & 0xFFFFFFFF, c, b, a, (t1 + t2) & 0xFFFFFFFF
    return [(x + y) & 0xFFFFFFFF for x, y in zip(h, (a, b, c, d, e, f, g, hh))]


def md_padding(length):
    """Merkle-Damgard padding for a message of `length` bytes."""
    return b"\x80" + b"\x00" * ((55 - length) % 64) + struct.pack(">Q", 8 * length)


def sha256(data, state=None, length_so_far=0):
    """SHA-256; with `state` and `length_so_far`, continues from a previous digest (length extension)."""
    h = list(state) if state else list(_H256)
    msg = data + md_padding(length_so_far + len(data))
    for i in range(0, len(msg), 64):
        h = _sha256_compress(h, msg[i:i + 64])
    return struct.pack(">8I", *h)


def length_extension(mac, secret_len, msg, extra):
    """Forge SHA-256(secret || msg || pad || extra) from mac = SHA-256(secret || msg), without the secret."""
    state = list(struct.unpack(">8I", mac))
    glue = md_padding(secret_len + len(msg))
    total = secret_len + len(msg) + len(glue)
    forged = sha256(extra, state, total)
    return msg + glue + extra, forged


def hmac_sha256(key, msg):
    if len(key) > 64:
        key = sha256(key)
    key = key.ljust(64, b"\x00")
    return sha256(xor(key, b"\x5c" * 64) + sha256(xor(key, b"\x36" * 64) + msg))


def cbc_mac(aes, msg):
    return cbc_encrypt(aes, bytes(16), msg)[-16:]


def _gf128_mul(x, y):
    R = 0xE1 << 120
    z, v = 0, y
    for i in range(127, -1, -1):
        if (x >> i) & 1:
            z ^= v
        v = (v >> 1) ^ R if v & 1 else v >> 1
    return z


def ghash(h, data):
    hi = int.from_bytes(h, "big")
    y = 0
    for i in range(0, len(data), 16):
        blk = data[i:i + 16].ljust(16, b"\x00")
        y = _gf128_mul(y ^ int.from_bytes(blk, "big"), hi)
    return y.to_bytes(16, "big")


def aes_gcm_encrypt(key, iv12, plaintext, aad=b""):
    aes = AES(key)
    h = aes.enc(bytes(16))
    j0 = iv12 + b"\x00\x00\x00\x01"
    ctr = int.from_bytes(j0, "big")
    ct = bytearray()
    for i in range(0, len(plaintext), 16):
        ctr = (ctr & ~0xFFFFFFFF) | ((ctr + 1) & 0xFFFFFFFF)
        ks = aes.enc(ctr.to_bytes(16, "big"))
        ct += xor(plaintext[i:i + 16], ks)
    ct = bytes(ct)

    def pad(b):
        return b + b"\x00" * (-len(b) % 16)
    s = ghash(h, pad(aad) + pad(ct) + struct.pack(">QQ", 8 * len(aad), 8 * len(ct)))
    tag = xor(aes.enc(j0), s)
    return ct, tag


# Keccak-f[1600] and SHA3-256

_RC = [0x0000000000000001, 0x0000000000008082, 0x800000000000808A, 0x8000000080008000, 0x000000000000808B,
       0x0000000080000001, 0x8000000080008081, 0x8000000000008009, 0x000000000000008A, 0x0000000000000088,
       0x0000000080008009, 0x000000008000000A, 0x000000008000808B, 0x800000000000008B, 0x8000000000008089,
       0x8000000000008003, 0x8000000000008002, 0x8000000000000080, 0x000000000000800A, 0x800000008000000A,
       0x8000000080008081, 0x8000000000008080, 0x0000000080000001, 0x8000000080008008]
_ROT = [[0, 36, 3, 41, 18], [1, 44, 10, 45, 2], [62, 6, 43, 15, 61], [28, 55, 25, 21, 56], [27, 20, 39, 8, 14]]
M64 = (1 << 64) - 1


def _rol64(v, n):
    return ((v << n) | (v >> (64 - n))) & M64 if n else v


def keccak_f(A):
    """A[x][y] lanes of 64 bits."""
    for rnd in range(24):
        C = [A[x][0] ^ A[x][1] ^ A[x][2] ^ A[x][3] ^ A[x][4] for x in range(5)]
        D = [C[(x - 1) % 5] ^ _rol64(C[(x + 1) % 5], 1) for x in range(5)]
        A = [[A[x][y] ^ D[x] for y in range(5)] for x in range(5)]
        B = [[0] * 5 for _ in range(5)]
        for x in range(5):
            for y in range(5):
                B[y][(2 * x + 3 * y) % 5] = _rol64(A[x][y], _ROT[x][y])
        A = [[B[x][y] ^ ((~B[(x + 1) % 5][y]) & B[(x + 2) % 5][y]) for y in range(5)] for x in range(5)]
        A[0][0] ^= _RC[rnd]
    return A


def sha3_256(data, trace=None):
    rate = 136
    msg = bytearray(data) + b"\x06"
    msg += b"\x00" * (-len(msg) % rate)
    msg[-1] |= 0x80
    A = [[0] * 5 for _ in range(5)]
    for off in range(0, len(msg), rate):
        blk = msg[off:off + rate]
        for i in range(rate // 8):
            x, y = i % 5, i // 5
            A[x][y] ^= int.from_bytes(blk[8 * i:8 * i + 8], "little")
        A = keccak_f(A)
        if trace is not None:
            trace.append(off // rate)
    out = b"".join(A[i % 5][i // 5].to_bytes(8, "little") for i in range(rate // 8))
    return out[:32]


def birthday_trial(bits, rng):
    """Hash random messages with SHA-256 truncated to `bits` bits until two collide; return the count."""
    import hashlib
    seen = set()
    n = 0
    while True:
        n += 1
        h = int.from_bytes(hashlib.sha256(rng.getrandbits(64).to_bytes(8, "big")).digest(), "big") >> (256 - bits)
        if h in seen:
            return n
        seen.add(h)


def merkle_root(leaves):
    import hashlib
    level = [hashlib.sha256(b"\x00" + x).digest() for x in leaves]
    levels = [level]
    while len(level) > 1:
        if len(level) % 2:
            level = level + [level[-1]]
        level = [hashlib.sha256(b"\x01" + level[i] + level[i + 1]).digest() for i in range(0, len(level), 2)]
        levels.append(level)
    return level[0], levels


def merkle_proof(levels, index):
    proof = []
    for lv in levels[:-1]:
        if len(lv) % 2:
            lv = lv + [lv[-1]]
        sib = index ^ 1
        proof.append((lv[sib], sib < index))
        index //= 2
    return proof


def merkle_verify(root, leaf, proof):
    import hashlib
    h = hashlib.sha256(b"\x00" + leaf).digest()
    for sib, left in proof:
        h = hashlib.sha256(b"\x01" + (sib + h if left else h + sib)).digest()
    return h == root


# ----------------------------------------------------------------------------------------------- toy SPN (Heys)

SPN_SBOX = [0xE, 0x4, 0xD, 0x1, 0x2, 0xF, 0xB, 0x8, 0x3, 0xA, 0x6, 0xC, 0x5, 0x9, 0x0, 0x7]
SPN_INV = [SPN_SBOX.index(i) for i in range(16)]


def _spn_sub(x, box):
    return sum(box[(x >> (4 * i)) & 0xF] << (4 * i) for i in range(4))


def _spn_perm(x):
    """Bit (4i + j) moves to (4j + i), counting from the most significant bit."""
    y = 0
    for p in range(16):
        bit = (x >> (15 - p)) & 1
        q = (p % 4) * 4 + p // 4
        y |= bit << (15 - q)
    return y


def spn_encrypt(x, keys):
    """Heys' 4-round SPN on 16 bits with five round keys."""
    for r in range(3):
        x = _spn_perm(_spn_sub(x ^ keys[r], SPN_SBOX))
    x = _spn_sub(x ^ keys[3], SPN_SBOX)
    return x ^ keys[4]


def spn_difference_table():
    t = [[0] * 16 for _ in range(16)]
    for x in range(16):
        for dx in range(16):
            t[dx][SPN_SBOX[x] ^ SPN_SBOX[x ^ dx]] += 1
    return t


def spn_differential_attack(keys, pairs, rng, dP=0x0B00, dU=0x0606):
    """Chosen-plaintext pairs with difference dP; for each guess of the 8 last-round key bits under S-boxes 2 and 4,
    count pairs whose partial decryption shows the expected difference dU. Returns counts by guess."""
    data = []
    for _ in range(pairs):
        p = rng.randrange(1 << 16)
        data.append((spn_encrypt(p, keys), spn_encrypt(p ^ dP, keys)))
    counts = {}
    for g2 in range(16):
        for g4 in range(16):
            k = (g2 << 8) | g4
            n = 0
            for c1, c2 in data:
                if (c1 ^ c2) & 0xF0F0:            # S-boxes 1 and 3 must be inactive in the output difference
                    continue
                v1 = c1 ^ k
                v2 = c2 ^ k
                u1 = _spn_sub(v1, SPN_INV)
                u2 = _spn_sub(v2, SPN_INV)
                if ((u1 ^ u2) & 0x0F0F) == (dU & 0x0F0F):
                    n += 1
            counts[k] = n
    return counts


def toy_cipher(x, k):
    """A 16-bit block cipher with a 16-bit key: the SPN with every round key derived from k."""
    ks = [k, ((k << 3) | (k >> 13)) & 0xFFFF, k ^ 0xA5A5, ((k << 7) | (k >> 9)) & 0xFFFF, k ^ 0x3C3C]
    return spn_encrypt(x, ks)


def meet_in_the_middle(p1, c1, p2, c2):
    """Double encryption c = E_k2(E_k1(p)) with two 16-bit keys: a table of E_k1(p1) for every k1, then D_k2(c1) for
    every k2 looked up in it; a second pair weeds out false matches. About 2 * 2^16 cipher calls instead of 2^32."""
    fwd = {}
    for k1 in range(1 << 16):
        fwd.setdefault(toy_cipher(p1, k1), []).append(k1)
    cands = []
    work = 1 << 16
    for k2 in range(1 << 16):
        mid = toy_decrypt(c1, k2)
        work += 1
        for k1 in fwd.get(mid, ()):
            if toy_cipher(toy_cipher(p2, k1), k2) == c2:
                cands.append((k1, k2))
    return cands, work


def toy_decrypt(c, k):
    ks = [k, ((k << 3) | (k >> 13)) & 0xFFFF, k ^ 0xA5A5, ((k << 7) | (k >> 9)) & 0xFFFF, k ^ 0x3C3C]
    x = _spn_sub(c ^ ks[4], SPN_INV) ^ ks[3]
    for r in (2, 1, 0):
        x = _spn_sub(_spn_perm(x), SPN_INV) ^ ks[r]   # the bit permutation is its own inverse
    return x


# ----------------------------------------------------------------------------------------------- side channels

def early_exit_equal(a, b):
    if len(a) != len(b):
        return False
    for x, y in zip(a, b):
        if x != y:
            return False
    return True


def constant_time_equal(a, b):
    if len(a) != len(b):
        return False
    d = 0
    for x, y in zip(a, b):
        d |= x ^ y
    return d == 0


def time_compare(fn, secret, guess, reps):
    t = time.perf_counter()
    for _ in range(reps):
        fn(secret, guess)
    return (time.perf_counter() - t) / reps


def pid_seeded_key(pid):
    """A key generator with the 2008 Debian OpenSSL bug's flaw: the only entropy left is the process id."""
    return random.Random(pid).getrandbits(128).to_bytes(16, "big")
