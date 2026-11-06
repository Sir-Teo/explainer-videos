"""The instrument of Part 30 ("Public Keys"): public-key cryptography from scratch.

Number theory (extended Euclid, square-and-multiply, CRT, Miller-Rabin, generators); Merkle's puzzles; Diffie-Hellman
and its man in the middle; RSA (key generation, CRT, OAEP, hash-and-sign, Bleichenbacher's PKCS #1 v1.5 oracle);
factoring (Pollard's rho, a quadratic sieve with linear algebra over GF(2)); discrete logs (baby-step giant-step, rho,
Pohlig-Hellman, index calculus); elliptic curves (the group law, P-256, ECDH, ECDSA with RFC 6979 nonces, nonce-reuse
key recovery, X25519); certificates; HKDF and a TLS 1.3-style handshake; lattices (Gauss and LLL reduction, a
knapsack broken by LLL, Regev's LWE, ML-KEM's ring arithmetic and a K-PKE built on it); Lamport signatures; Schnorr
and Fiat-Shamir; Shamir secret sharing.

Everything here is for learning, never for real use: no constant-time code, no side-channel care, small parameters.
"""

from __future__ import annotations

import hashlib
import hmac as _hmac
import math
from fractions import Fraction

from explainer.cs.algo import crypto as K


def H(b: bytes) -> bytes:
    return hashlib.sha256(b).digest()


def i2b(x: int, n: int) -> bytes:
    return x.to_bytes(n, "big")


def b2i(b: bytes) -> int:
    return int.from_bytes(b, "big")


# --------------------------------------------------------------------------------------------- number theory

def egcd(a, b):
    """(g, x, y) with a x + b y = g = gcd(a, b)."""
    x0, y0, x1, y1 = 1, 0, 0, 1
    while b:
        q, a, b = a // b, b, a % b
        x0, x1 = x1, x0 - q * x1
        y0, y1 = y1, y0 - q * y1
    return a, x0, y0


def egcd_trace(a, b):
    """The rows of Euclid's algorithm with Bezout coefficients: (a, b, q, r, x, y) where a x_i + b y_i = r_i."""
    rows = []
    r0, r1, x0, x1, y0, y1 = a, b, 1, 0, 0, 1
    while r1:
        q = r0 // r1
        r0, r1 = r1, r0 - q * r1
        x0, x1 = x1, x0 - q * x1
        y0, y1 = y1, y0 - q * y1
        rows.append({"q": q, "r": r0, "x": x0, "y": y0, "next": r1})
    return rows


def inv_mod(a, m):
    g, x, _ = egcd(a % m, m)
    if g != 1:
        raise ValueError("not invertible")
    return x % m


def pow_trace(g, e, m):
    """Left-to-right square-and-multiply: [(bit, value after the step)]."""
    acc, out = 1, []
    for bit in bin(e)[2:]:
        acc = acc * acc % m
        if bit == "1":
            acc = acc * g % m
        out.append((int(bit), acc))
    return out


def crt(rs, ms):
    x, M = 0, 1
    for r, m in zip(rs, ms):
        # x = x + M * t with x + M t = r (mod m)
        t = (r - x) * inv_mod(M, m) % m
        x += M * t
        M *= m
    return x % M


def mr_witness(a, n):
    """True if a proves n composite (Miller-Rabin)."""
    d, s = n - 1, 0
    while d % 2 == 0:
        d //= 2
        s += 1
    x = pow(a, d, n)
    if x in (1, n - 1):
        return False
    for _ in range(s - 1):
        x = x * x % n
        if x == n - 1:
            return False
    return True


SMALL_PRIMES = [p for p in range(2, 1000) if all(p % q for q in range(2, int(p ** 0.5) + 1))]


def is_probable_prime(n, rng=None, rounds=40):
    if n < 2:
        return False
    for p in SMALL_PRIMES:
        if n % p == 0:
            return n == p
    import random as _r
    rng = rng or _r.Random(n)
    return not any(mr_witness(rng.randrange(2, n - 1), n) for _ in range(rounds))


def random_prime(bits, rng):
    while True:
        n = rng.getrandbits(bits) | (1 << (bits - 1)) | 1
        if is_probable_prime(n, rng):
            return n


def factorize(n):
    """Trial division then rho; small and medium n only."""
    out, d = {}, 2
    while d * d <= n and d < 100000:
        while n % d == 0:
            out[d] = out.get(d, 0) + 1
            n //= d
        d += 1 if d == 2 else 2
    if n > 1:
        stack = [n]
        import random as _r
        rng = _r.Random(1)
        while stack:
            m = stack.pop()
            if is_probable_prime(m):
                out[m] = out.get(m, 0) + 1
                continue
            f = pollard_rho(m, rng)[0]
            stack += [f, m // f]
    return out


def mult_order(g, p, factors=None):
    n = p - 1
    factors = factors or factorize(n)
    o = n
    for q in factors:
        while o % q == 0 and pow(g, o // q, p) == 1:
            o //= q
    return o


def find_generator(p):
    f = factorize(p - 1)
    for g in range(2, p):
        if all(pow(g, (p - 1) // q, p) != 1 for q in f):
            return g
    raise ValueError


# --------------------------------------------------------------------------------------------- key agreement

def merkle_puzzles(n, rng, bits=None):
    """Merkle's puzzles (1974): Alice publishes n puzzles, each a (key id, key) pair locked under a key from a space of
    n; Bob solves one at random (about n/2 tries), announces its id; Eve must solve about n/2 puzzles of n/2 tries."""
    space = n
    puzzles, secrets = [], {}
    for i in range(n):
        pk = rng.randrange(space)
        pid, key = rng.getrandbits(32), rng.getrandbits(64)
        tag = H(i2b(pk, 8) + b"check")[:4]
        payload = K.xor(i2b(pid, 4) + i2b(key, 8), H(i2b(pk, 8) + b"pad")[:12])
        puzzles.append((tag, payload))
        secrets[pid] = key
    j = rng.randrange(n)
    tries = 0
    for pk in range(space):
        tries += 1
        if H(i2b(pk, 8) + b"check")[:4] == puzzles[j][0]:
            plain = K.xor(puzzles[j][1], H(i2b(pk, 8) + b"pad")[:12])
            pid, key = b2i(plain[:4]), b2i(plain[4:])
            break
    return {"n": n, "bob_tries": tries, "agreed": secrets[pid] == key, "eve_expected": n * n // 4,
            "alice_work": n}


def dh_keypair(p, g, rng):
    x = rng.randrange(2, p - 1)
    return x, pow(g, x, p)


def dh_mitm(p, g, rng):
    """Mallory sits between Alice and Bob and runs one exchange with each."""
    a, A = dh_keypair(p, g, rng)
    b, B = dh_keypair(p, g, rng)
    m, M = dh_keypair(p, g, rng)
    alice_key = pow(M, a, p)          # Alice thinks M is Bob's
    bob_key = pow(M, b, p)            # Bob thinks M is Alice's
    return {"alice": alice_key, "bob": bob_key, "mallory_with_alice": pow(A, m, p),
            "mallory_with_bob": pow(B, m, p)}


# --------------------------------------------------------------------------------------------- RSA

def rsa_keygen(bits, rng, e=65537):
    while True:
        p = random_prime(bits // 2, rng)
        q = random_prime(bits - bits // 2, rng)
        if p == q:
            continue
        phi = (p - 1) * (q - 1)
        if math.gcd(e, phi) == 1 and (p * q).bit_length() == bits:
            break
    d = inv_mod(e, phi)
    return {"n": p * q, "e": e, "d": d, "p": p, "q": q, "dp": d % (p - 1), "dq": d % (q - 1),
            "qinv": inv_mod(q, p)}


def rsa_enc(m, key):
    return pow(m, key["e"], key["n"])


def rsa_dec(c, key, use_crt=True):
    if not use_crt:
        return pow(c, key["d"], key["n"])
    mp = pow(c, key["dp"], key["p"])
    mq = pow(c, key["dq"], key["q"])
    h = key["qinv"] * (mp - mq) % key["p"]
    return mq + h * key["q"]


def klen(key):
    return (key["n"].bit_length() + 7) // 8


def mgf1(seed, length):
    out, c = b"", 0
    while len(out) < length:
        out += H(seed + i2b(c, 4))
        c += 1
    return out[:length]


def oaep_encode(msg, k, rng, label=b""):
    hl = 32
    if len(msg) > k - 2 * hl - 2:
        raise ValueError("message too long")
    db = H(label) + bytes(k - len(msg) - 2 * hl - 2) + b"\x01" + msg
    seed = bytes(rng.randrange(256) for _ in range(hl))
    mdb = K.xor(db, mgf1(seed, k - hl - 1))
    mseed = K.xor(seed, mgf1(mdb, hl))
    return b"\x00" + mseed + mdb


def oaep_decode(em, k, label=b""):
    hl = 32
    mseed, mdb = em[1:1 + hl], em[1 + hl:]
    seed = K.xor(mseed, mgf1(mdb, hl))
    db = K.xor(mdb, mgf1(seed, k - hl - 1))
    if em[0] != 0 or db[:hl] != H(label):
        raise ValueError("decryption error")
    rest = db[hl:]
    i = rest.index(b"\x01")
    if any(rest[:i]):
        raise ValueError("decryption error")
    return rest[i + 1:]


def oaep_encrypt(msg, key, rng):
    k = klen(key)
    return i2b(rsa_enc(b2i(oaep_encode(msg, k, rng)), key), k)


def oaep_decrypt(ct, key):
    k = klen(key)
    return oaep_decode(i2b(rsa_dec(b2i(ct), key), k), k)


def rsa_sign(msg, key):
    """Hash-and-sign with a full-domain-style hash (MGF1 of SHA-256 to the modulus size, top byte cleared)."""
    k = klen(key)
    h = b"\x00" + mgf1(H(msg), k - 1)
    return pow(b2i(h), key["d"], key["n"])


def rsa_verify(msg, sig, key):
    k = klen(key)
    return pow(sig, key["e"], key["n"]) == b2i(b"\x00" + mgf1(H(msg), k - 1))


def pkcs1_v15_pad(msg, k, rng):
    ps = bytes(rng.randrange(1, 256) for _ in range(k - 3 - len(msg)))
    return b"\x00\x02" + ps + b"\x00" + msg


def pkcs1_v15_conforming(em):
    return em[0] == 0 and em[1] == 2


def bleichenbacher(c, key, oracle, trace=None):
    """Bleichenbacher (1998): recover m from c = m^e mod n, given an oracle saying whether c' decrypts to something
    that starts 00 02. Returns (m, queries)."""
    n, e = key["n"], key["e"]
    k = klen(key)
    B = 1 << (8 * (k - 2))
    q = 0

    def ask(s):
        nonlocal q
        q += 1
        return oracle(c * pow(s, e, n) % n)
    M = [(2 * B, 3 * B - 1)]
    s = -(-n // (3 * B))
    while not ask(s):
        s += 1
    i = 1
    while True:
        if i > 1 and len(M) > 1:
            s += 1
            while not ask(s):
                s += 1
        elif i > 1:
            a, b = M[0]
            r = -(-2 * (b * s - 2 * B) // n)
            found = False
            while not found:
                lo = -(-(2 * B + r * n) // b)
                hi = (3 * B + r * n) // a
                for s2 in range(lo, hi + 1):
                    if ask(s2):
                        s, found = s2, True
                        break
                r += 1
        newM = []
        for a, b in M:
            rlo = -(-(a * s - 3 * B + 1) // n)
            rhi = (b * s - 2 * B) // n
            for r in range(rlo, rhi + 1):
                lo = max(a, -(-(2 * B + r * n) // s))
                hi = min(b, (3 * B - 1 + r * n) // s)
                if lo <= hi:
                    newM.append((lo, hi))
        M = sorted(set(newM))
        if trace is not None:
            trace.append((q, sum(b - a + 1 for a, b in M)))
        if len(M) == 1 and M[0][0] == M[0][1]:
            return M[0][0], q
        i += 1


# --------------------------------------------------------------------------------------------- factoring

def pollard_rho(n, rng, trace=False):
    """Brent's variant of Pollard's rho. Returns (factor, steps[, the walk x_i mod the factor])."""
    if n % 2 == 0:
        return 2, 1
    while True:
        c = rng.randrange(1, n)
        f = lambda x: (x * x + c) % n          # noqa: E731
        y, r, qq, g, steps = rng.randrange(n), 1, 1, 1, 0
        x = ys = y
        while g == 1:
            x = y
            for _ in range(r):
                y = f(y)
                steps += 1
            k = 0
            while k < r and g == 1:
                ys = y
                for _ in range(min(128, r - k)):
                    y = f(y)
                    qq = qq * abs(x - y) % n
                    steps += 1
                g = math.gcd(qq, n)
                k += 128
            r *= 2
        if g == n:
            g = 1
            while g == 1:
                ys = f(ys)
                g = math.gcd(abs(x - ys), n)
        if g != n:
            return g, steps


def rho_walk(n, p, c=1, x0=2, steps=60):
    """The sequence x_{i+1} = x_i^2 + c mod n, reduced mod the hidden factor p: it enters a cycle (the rho)."""
    xs, x = [], x0
    for _ in range(steps):
        xs.append(x % p)
        x = (x * x + c) % n
    return xs


def _tonelli(n, p):
    if p == 2:
        return n % 2
    q, s = p - 1, 0
    while q % 2 == 0:
        q //= 2
        s += 1
    z = 2
    while pow(z, (p - 1) // 2, p) != p - 1:
        z += 1
    m, c, t, r = s, pow(z, q, p), pow(n, q, p), pow(n, (q + 1) // 2, p)
    while t != 1:
        i, t2 = 0, t
        while t2 != 1:
            t2 = t2 * t2 % p
            i += 1
        b = pow(c, 1 << (m - i - 1), p)
        m, c, t, r = i, b * b % p, t * b * b % p, r * b % p
    return r


def gf2_dependencies(rows, ncols):
    """Rows are int bitmasks (exponent vectors mod 2); returns sets of row indices whose XOR is zero."""
    pivots = {}
    combos = []
    for i, v in enumerate(rows):
        comb = 1 << i
        for col in range(ncols):
            if not (v >> col) & 1:
                continue
            if col in pivots:
                pv, pc = pivots[col]
                v ^= pv
                comb ^= pc
            else:
                pivots[col] = (v, comb)
                break
        if v == 0:
            combos.append([j for j in range(len(rows)) if (comb >> j) & 1])
    return combos


def quadratic_sieve(n, B=None, M=None, tries=4):
    """Retry wrapper: grow the factor base and the interval until a factor appears."""
    for _ in range(tries):
        f, st = _qs(n, B, M)
        if f:
            return f, st
        B = int((st["B"]) * 1.6)
        M = st["M"] * 2
    return None, st


def _qs(n, B=None, M=None):
    """A basic quadratic sieve: sieve x^2 - n near sqrt(n) over a factor base of primes with (n/p) = 1, keep
    B-smooth values, find a GF(2) dependency, and take gcd(x - y, n). Returns (factor, stats)."""
    L = math.exp(math.sqrt(math.log(n) * math.log(math.log(n))))
    B = B or max(50, int(L ** 0.5 * 1.2))
    base = [p for p in range(2, B + 1) if is_probable_prime(p) and (p == 2 or pow(n % p, (p - 1) // 2, p) == 1)]
    root = math.isqrt(n) + 1
    M = M or max(5000, 60 * len(base) ** 2)
    xs = list(range(root, root + M))
    vals = [x * x - n for x in xs]
    logs = [0.0] * M
    for p in base:
        if p == 2:
            for i in range(M):
                if vals[i] % 2 == 0:
                    logs[i] += math.log(2)
            continue
        r = _tonelli(n % p, p)
        for rr in {r, p - r}:
            start = (rr - root) % p
            for i in range(start, M, p):
                logs[i] += math.log(p)
    rels, rows = [], []
    for i in range(M):
        if logs[i] > math.log(vals[i]) - 2 * math.log(base[-1]):
            v, vec, exps = vals[i], 0, {}
            for j, p in enumerate(base):
                while v % p == 0:
                    v //= p
                    exps[p] = exps.get(p, 0) + 1
                    vec ^= 1 << j
            if v == 1:
                rels.append((xs[i], exps))
                rows.append(vec)
                if len(rels) > len(base) + 10:
                    break
    for dep in gf2_dependencies(rows, len(base)):
        x, ex = 1, {}
        for j in dep:
            x = x * rels[j][0] % n
            for p, e in rels[j][1].items():
                ex[p] = ex.get(p, 0) + e
        y = 1
        for p, e in ex.items():
            y = y * pow(p, e // 2, n) % n
        g = math.gcd(x - y, n)
        if 1 < g < n:
            return g, {"base": len(base), "B": B, "M": M, "relations": len(rels), "dependency": len(dep),
                       "example": rels[0]}
    return None, {"base": len(base), "relations": len(rels), "B": B, "M": M}


# --------------------------------------------------------------------------------------------- discrete logs

def bsgs(g, h, p, n=None):
    """Baby-step giant-step: x with g^x = h (mod p), in about 2 sqrt(n) multiplications."""
    n = n or p - 1
    m = math.isqrt(n) + 1
    table, e = {}, 1
    for j in range(m):
        table.setdefault(e, j)
        e = e * g % p
    step = pow(g, -m, p)
    y = h
    for i in range(m + 1):
        if y in table:
            return i * m + table[y], m
        y = y * step % p
    return None, m


def rho_log(g, h, p, n, rng):
    """Pollard's rho for logarithms in the subgroup of prime order n generated by g."""
    def step(x, a, b):
        s = x % 3
        if s == 0:
            return x * x % p, 2 * a % n, 2 * b % n
        if s == 1:
            return x * g % p, (a + 1) % n, b
        return x * h % p, a, (b + 1) % n
    while True:
        a0, b0 = rng.randrange(n), rng.randrange(n)
        x = pow(g, a0, p) * pow(h, b0, p) % p
        X, A, Bb = x, a0, b0
        x, a, b = x, a0, b0
        steps = 0
        while True:
            x, a, b = step(x, a, b)
            X, A, Bb = step(*step(X, A, Bb))
            steps += 1
            if x == X:
                break
        db = (Bb - b) % n
        if db:
            return (a - A) * inv_mod(db, n) % n, steps


def pohlig_hellman(g, h, p):
    """Discrete log in Z_p^* by reducing to each prime-power factor of p - 1 (with BSGS there), then CRT."""
    n = p - 1
    f = factorize(n)
    rs, ms = [], []
    for q, e in f.items():
        qe = q ** e
        gq = pow(g, n // qe, p)
        hq = pow(h, n // qe, p)
        gamma = pow(gq, qe // q, p)
        x = 0
        for k in range(e):
            hk = pow(pow(gq, -x, p) * hq % p, q ** (e - 1 - k), p)
            dk, _ = bsgs(gamma, hk, p, q)
            x += dk * q ** k
        rs.append(x)
        ms.append(qe)
    return crt(rs, ms), f


def index_calculus(g, h, p, B, rng):
    """Toy index calculus: logs of the factor base from smooth powers of g (linear algebra mod p - 1, done prime by
    prime), then one smooth h g^s. Returns (x, stats)."""
    base = [q for q in range(2, B + 1) if is_probable_prime(q)]
    n = p - 1
    rels = []
    tries = 0
    while len(rels) < len(base) + 15:
        k = rng.randrange(1, n)
        v = pow(g, k, p)
        tries += 1
        ex = []
        for q in base:
            c = 0
            while v % q == 0:
                v //= q
                c += 1
            ex.append(c)
        if v == 1:
            rels.append((ex, k))
    f = factorize(n)
    logs_by_mod = []
    for q, e in f.items():
        m = q ** e
        sol = _solve_mod_prime_power([r[0] for r in rels], [r[1] for r in rels], q, e)
        if sol is None:
            return None, {"relations": len(rels), "tries": tries}
        logs_by_mod.append((sol, m))
    logs = [crt([s[0][i] for s in logs_by_mod], [s[1] for s in logs_by_mod]) for i in range(len(base))]
    while True:
        s = rng.randrange(n)
        v = h * pow(g, s, p) % p
        tot = 0
        for q, lq in zip(base, logs):
            while v % q == 0:
                v //= q
                tot += lq
        if v == 1:
            x = (tot - s) % n
            return x, {"relations": len(rels), "tries": tries, "base": len(base), "logs": dict(zip(base, logs))}


def _solve_mod_prime_power(A, b, q, e):
    """Solve A x = b mod q^e for a consistent overdetermined system (Hensel lifting from mod q)."""
    m = q ** e
    rows = [list(r) + [bb % m] for r, bb in zip(A, b)]
    ncol = len(A[0])
    x = [0] * ncol
    # Gaussian elimination mod q to find a solution mod q, then lift (we simply retry elimination mod q^e with unit
    # pivots, which works for these random systems with high probability)
    R = [r[:] for r in rows]
    piv_rows = []
    r = 0
    for c in range(ncol):
        pr = next((i for i in range(r, len(R)) if R[i][c] % q), None)
        if pr is None:
            return None
        R[r], R[pr] = R[pr], R[r]
        inv = inv_mod(R[r][c], m)
        R[r] = [v * inv % m for v in R[r]]
        for i in range(len(R)):
            if i != r and R[i][c]:
                f_ = R[i][c]
                R[i] = [(vi - f_ * vr) % m for vi, vr in zip(R[i], R[r])]
        piv_rows.append(r)
        r += 1
    for c in range(ncol):
        x[c] = R[c][-1]
    return x


# --------------------------------------------------------------------------------------------- elliptic curves

INF = None


class Curve:
    """y^2 = x^3 + a x + b over F_p, in affine coordinates; the point at infinity is None."""

    def __init__(self, p, a, b, G=None, n=None, h=1, name=""):
        self.p, self.a, self.b, self.G, self.n, self.h, self.name = p, a, b, G, n, h, name

    def on(self, P):
        if P is INF:
            return True
        x, y = P
        return (y * y - x * x * x - self.a * x - self.b) % self.p == 0

    def neg(self, P):
        return INF if P is INF else (P[0], -P[1] % self.p)

    def add(self, P, Q):
        p = self.p
        if P is INF:
            return Q
        if Q is INF:
            return P
        if P[0] == Q[0] and (P[1] + Q[1]) % p == 0:
            return INF
        if P == Q:
            lam = (3 * P[0] * P[0] + self.a) * inv_mod(2 * P[1], p) % p
        else:
            lam = (Q[1] - P[1]) * inv_mod(Q[0] - P[0], p) % p
        x = (lam * lam - P[0] - Q[0]) % p
        return x, (lam * (P[0] - x) - P[1]) % p

    def mul(self, k, P, trace=None):
        """Double-and-add from the top bit; ``trace`` (a list) collects ('D'|'A', point) steps."""
        R = INF
        for bit in bin(k)[2:]:
            R = self.add(R, R)
            if trace is not None:
                trace.append(("D", R))
            if bit == "1":
                R = self.add(R, P)
                if trace is not None:
                    trace.append(("A", R))
        return R

    def points(self):
        """Every affine point (small p only)."""
        p = self.p
        sq = {}
        for y in range(p):
            sq.setdefault(y * y % p, []).append(y)
        return [(x, y) for x in range(p) for y in sq.get((x ** 3 + self.a * x + self.b) % p, [])]


P256 = Curve(
    p=0xffffffff00000001000000000000000000000000ffffffffffffffffffffffff,
    a=-3 % 0xffffffff00000001000000000000000000000000ffffffffffffffffffffffff,
    b=0x5ac635d8aa3a93e7b3ebbd55769886bc651d06b0cc53b0f63bce3c3e27d2604b,
    G=(0x6b17d1f2e12c4247f8bce6e563a440f277037d812deb33a0f4a13945d898c296,
       0x4fe342e2fe1a7f9b8ee7eb4a7c0f9e162bce33576b315ececbb6406837bf51f5),
    n=0xffffffff00000000ffffffffffffffffbce6faada7179e84f3b9cac2fc632551, name="P-256")

TOY = Curve(p=97, a=2, b=3, name="y^2 = x^3 + 2x + 3 over F_97")


def toy_curve_group(curve):
    """Order of the group and a generator of the largest cyclic subgroup we find (small curves)."""
    pts = curve.points()
    N = len(pts) + 1
    best = None
    for P in pts:
        k, Q = 1, P
        while Q is not INF:
            Q = curve.add(Q, P)
            k += 1
        if best is None or k > best[1]:
            best = (P, k)
    return N, best


def ec_keypair(curve, rng):
    d = rng.randrange(1, curve.n)
    return d, curve.mul(d, curve.G)


def rfc6979_k(d, h1, curve):
    """Deterministic ECDSA nonce (RFC 6979, HMAC-SHA-256)."""
    q = curve.n
    qlen = q.bit_length()
    rlen = (qlen + 7) // 8

    def bits2int(b):
        v = b2i(b)
        blen = len(b) * 8
        return v >> (blen - qlen) if blen > qlen else v

    def int2octets(x):
        return i2b(x, rlen)

    def bits2octets(b):
        return int2octets(bits2int(b) % q)
    V, Kk = b"\x01" * 32, b"\x00" * 32
    Kk = _hmac.new(Kk, V + b"\x00" + int2octets(d) + bits2octets(h1), hashlib.sha256).digest()
    V = _hmac.new(Kk, V, hashlib.sha256).digest()
    Kk = _hmac.new(Kk, V + b"\x01" + int2octets(d) + bits2octets(h1), hashlib.sha256).digest()
    V = _hmac.new(Kk, V, hashlib.sha256).digest()
    while True:
        T = b""
        while len(T) < rlen:
            V = _hmac.new(Kk, V, hashlib.sha256).digest()
            T += V
        k = bits2int(T)
        if 1 <= k < q:
            return k
        Kk = _hmac.new(Kk, V + b"\x00", hashlib.sha256).digest()
        V = _hmac.new(Kk, V, hashlib.sha256).digest()


def ecdsa_sign(d, msg, curve=P256, k=None):
    n = curve.n
    z = b2i(H(msg)) >> max(0, 256 - n.bit_length())
    k = k or rfc6979_k(d, H(msg), curve)
    r = curve.mul(k, curve.G)[0] % n
    s = inv_mod(k, n) * (z + r * d) % n
    return r, s


def ecdsa_verify(Q, msg, sig, curve=P256):
    r, s = sig
    n = curve.n
    if not (1 <= r < n and 1 <= s < n):
        return False
    z = b2i(H(msg)) >> max(0, 256 - n.bit_length())
    w = inv_mod(s, n)
    X = curve.add(curve.mul(z * w % n, curve.G), curve.mul(r * w % n, Q))
    return X is not INF and X[0] % n == r


def ecdsa_nonce_reuse(msg1, sig1, msg2, sig2, curve=P256):
    """Two signatures with the same k (same r) give k = (z1 - z2)/(s1 - s2) and then d = (s k - z)/r."""
    n = curve.n
    (r, s1), (_, s2) = sig1, sig2
    z1, z2 = b2i(H(msg1)), b2i(H(msg2))
    k = (z1 - z2) * inv_mod(s1 - s2, n) % n
    d = (s1 * k - z1) * inv_mod(r, n) % n
    return k, d


X25519_P = 2 ** 255 - 19


def x25519(k: bytes, u: bytes) -> bytes:
    """RFC 7748's Montgomery ladder on Curve25519."""
    p, a24 = X25519_P, 121665
    kk = bytearray(k)
    kk[0] &= 248
    kk[31] &= 127
    kk[31] |= 64
    sc = int.from_bytes(kk, "little")
    x1 = int.from_bytes(u, "little") & ((1 << 255) - 1)
    x2, z2, x3, z3, swap = 1, 0, x1, 1, 0
    for t in range(254, -1, -1):
        kt = (sc >> t) & 1
        swap ^= kt
        if swap:
            x2, x3, z2, z3 = x3, x2, z3, z2
        swap = kt
        A, B = (x2 + z2) % p, (x2 - z2) % p
        AA, BB = A * A % p, B * B % p
        E = (AA - BB) % p
        C, D = (x3 + z3) % p, (x3 - z3) % p
        DA, CB = D * A % p, C * B % p
        x3, z3 = (DA + CB) ** 2 % p, x1 * (DA - CB) ** 2 % p
        x2, z2 = AA * BB % p, E * (AA + a24 * E) % p
    if swap:
        x2, z2 = x3, z3
    return (x2 * pow(z2, p - 2, p) % p).to_bytes(32, "little")


X25519_BASE = (9).to_bytes(32, "little")


# --------------------------------------------------------------------------------------------- certificates

def ec_pub_bytes(Q):
    return b"\x04" + i2b(Q[0], 32) + i2b(Q[1], 32)


def make_cert(subject, pub, issuer, issuer_key):
    body = f"subject={subject};issuer={issuer};".encode() + ec_pub_bytes(pub)
    return {"subject": subject, "issuer": issuer, "pub": pub, "body": body, "sig": ecdsa_sign(issuer_key, body)}


def verify_chain(chain, roots):
    """chain: leaf first; roots: {name: public key}. Each certificate must be signed by the next one's key."""
    for cert, parent in zip(chain, chain[1:] + [None]):
        key = parent["pub"] if parent else roots.get(cert["issuer"])
        if key is None or not ecdsa_verify(key, cert["body"], cert["sig"]):
            return False
    return True


# --------------------------------------------------------------------------------------------- HKDF and TLS

def hkdf_extract(salt, ikm):
    return _hmac.new(salt or bytes(32), ikm, hashlib.sha256).digest()


def hkdf_expand(prk, info, length):
    out, t, c = b"", b"", 1
    while len(out) < length:
        t = _hmac.new(prk, t + info + bytes([c]), hashlib.sha256).digest()
        out += t
        c += 1
    return out[:length]


def hkdf_expand_label(secret, lbl, context, length):
    full = b"tls13 " + lbl.encode()
    info = i2b(length, 2) + bytes([len(full)]) + full + bytes([len(context)]) + context
    return hkdf_expand(secret, info, length)


def derive_secret(secret, lbl, transcript):
    return hkdf_expand_label(secret, lbl, H(transcript), 32)


def tls_handshake(rng, server_name="pebble.example"):
    """A TLS 1.3-shaped handshake between two of our machines: X25519 key shares, a certificate chain signed with
    ECDSA P-256, the key schedule (HKDF), Finished MACs and AES-128-GCM records. Returns the transcript and checks."""
    rb = lambda n: bytes(rng.randrange(256) for _ in range(n))    # noqa: E731
    ca_key, ca_pub = ec_keypair(P256, rng)
    srv_key, srv_pub = ec_keypair(P256, rng)
    cert = make_cert(server_name, srv_pub, "Pebble Root CA", ca_key)
    roots = {"Pebble Root CA": ca_pub}
    msgs = []
    c_priv = rb(32)
    c_share = x25519(c_priv, X25519_BASE)
    ch = b"ClientHello" + rb(32) + c_share + server_name.encode()
    msgs.append(("client", "ClientHello", "random, X25519 key share, supported suites", ch))
    s_priv = rb(32)
    s_share = x25519(s_priv, X25519_BASE)
    sh = b"ServerHello" + rb(32) + s_share
    msgs.append(("server", "ServerHello", "random, X25519 key share, chosen suite", sh))
    shared_c = x25519(c_priv, s_share)
    shared_s = x25519(s_priv, c_share)
    early = hkdf_extract(None, bytes(32))
    derived = derive_secret(early, "derived", b"")
    hs = hkdf_extract(derived, shared_s)
    tr = ch + sh
    s_hs = derive_secret(hs, "s hs traffic", tr)
    c_hs = derive_secret(hs, "c hs traffic", tr)

    def keys(secret):
        return hkdf_expand_label(secret, "key", b"", 16), hkdf_expand_label(secret, "iv", b"", 12)
    skey, siv = keys(s_hs)
    enc_ext = b"EncryptedExtensions"
    certmsg = b"Certificate" + cert["body"] + i2b(cert["sig"][0], 32) + i2b(cert["sig"][1], 32)
    tr2 = tr + enc_ext + certmsg
    cv_sig = ecdsa_sign(srv_key, b" " * 64 + b"TLS 1.3, server CertificateVerify\x00" + H(tr2))
    cv = b"CertificateVerify" + i2b(cv_sig[0], 32) + i2b(cv_sig[1], 32)
    tr3 = tr2 + cv
    fin_key = hkdf_expand_label(s_hs, "finished", b"", 32)
    s_fin = _hmac.new(fin_key, H(tr3), hashlib.sha256).digest()
    flight = enc_ext + certmsg + cv + b"Finished" + s_fin
    ct_flight, tag = K.aes_gcm_encrypt(skey, siv, flight)
    msgs.append(("server", "{EncryptedExtensions, Certificate, CertificateVerify, Finished}",
                 "encrypted under handshake keys", ct_flight + tag))
    # the client side: decrypt and check everything
    hs_c = hkdf_extract(derived, shared_c)
    s_hs_c = derive_secret(hs_c, "s hs traffic", tr)
    ck, civ = keys(s_hs_c)
    pt, tag2 = K.aes_gcm_encrypt(ck, civ, ct_flight)       # CTR decryption is encryption
    got_tag = K.aes_gcm_encrypt(ck, civ, pt)[1]
    cert_ok = verify_chain([cert], roots)
    cv_ok = ecdsa_verify(cert["pub"], b" " * 64 + b"TLS 1.3, server CertificateVerify\x00" + H(tr2), cv_sig)
    fin_ok = _hmac.compare_digest(_hmac.new(hkdf_expand_label(s_hs_c, "finished", b"", 32), H(tr3),
                                            hashlib.sha256).digest(), s_fin)
    tr4 = tr3 + b"Finished" + s_fin
    c_fin = _hmac.new(hkdf_expand_label(c_hs, "finished", b"", 32), H(tr4), hashlib.sha256).digest()
    msgs.append(("client", "{Finished}", "the client's MAC over the transcript", c_fin))
    master = hkdf_extract(derive_secret(hs, "derived", b""), bytes(32))
    c_app = derive_secret(master, "c ap traffic", tr4)
    ak, aiv = keys(c_app)
    req = b"GET /part30 HTTP/1.1"
    app_ct, app_tag = K.aes_gcm_encrypt(ak, aiv, req)
    msgs.append(("client", "application data", "AES-128-GCM under traffic keys", app_ct + app_tag))
    return {"messages": [(a, b, c, len(d)) for a, b, c, d in msgs], "shared_equal": shared_c == shared_s,
            "tags_equal": got_tag == tag, "cert_ok": cert_ok, "cv_ok": cv_ok, "finished_ok": fin_ok,
            "plaintext_ok": pt == flight, "shared": shared_s.hex(), "request": req.decode(),
            "app": (app_ct + app_tag).hex()}


# --------------------------------------------------------------------------------------------- lattices

def gauss_reduce(b1, b2):
    """Lagrange-Gauss reduction of a 2-D basis; returns the reduced basis and every intermediate basis."""
    b1, b2 = list(b1), list(b2)
    steps = [(tuple(b1), tuple(b2))]
    dot = lambda u, v: u[0] * v[0] + u[1] * v[1]   # noqa: E731
    if dot(b1, b1) > dot(b2, b2):
        b1, b2 = b2, b1
    while True:
        m = round(Fraction(dot(b1, b2), dot(b1, b1)))
        b2 = [b2[0] - m * b1[0], b2[1] - m * b1[1]]
        steps.append((tuple(b1), tuple(b2)))
        if dot(b2, b2) >= dot(b1, b1):
            break
        b1, b2 = b2, b1
        steps.append((tuple(b1), tuple(b2)))
    return (tuple(b1), tuple(b2)), steps


def lll(B, delta=Fraction(3, 4)):
    """The LLL algorithm (exact rational Gram-Schmidt, recomputed after each change; small dimensions only)."""
    B = [list(map(int, b)) for b in B]
    n = len(B)

    def dot(u, v):
        return sum(Fraction(a) * b for a, b in zip(u, v))

    def gs(B):
        Bs, mu = [], [[Fraction(0)] * n for _ in range(n)]
        for i in range(n):
            v = [Fraction(x) for x in B[i]]
            for j in range(i):
                mu[i][j] = dot(B[i], Bs[j]) / dot(Bs[j], Bs[j])
                v = [a - mu[i][j] * b for a, b in zip(v, Bs[j])]
            Bs.append(v)
        return Bs, mu
    Bs, mu = gs(B)
    k = 1
    while k < n:
        for j in range(k - 1, -1, -1):
            q = round(mu[k][j])
            if q:
                B[k] = [a - q * b for a, b in zip(B[k], B[j])]
                Bs, mu = gs(B)
        if dot(Bs[k], Bs[k]) >= (delta - mu[k][k - 1] ** 2) * dot(Bs[k - 1], Bs[k - 1]):
            k += 1
        else:
            B[k], B[k - 1] = B[k - 1], B[k]
            Bs, mu = gs(B)
            k = max(k - 1, 1)
    return B


def knapsack_keygen(n, rng):
    """Merkle-Hellman (1978): a superincreasing sequence disguised by modular multiplication."""
    w, s = [], 0
    for _ in range(n):
        x = s + rng.randrange(1, 2 ** 8)
        w.append(x)
        s += x
    q = s + rng.randrange(1, 2 ** 8)
    r = rng.randrange(2, q)
    while math.gcd(r, q) != 1:
        r = rng.randrange(2, q)
    return {"w": w, "q": q, "r": r, "pub": [r * x % q for x in w]}


def knapsack_attack(pub, c):
    """Lagarias-Odlyzko style: the lattice [I | N a ; 0 | N c]; a short vector reveals the 0/1 message."""
    n = len(pub)
    N = math.isqrt(n) + 1
    B = [[2 if i == j else 0 for j in range(n)] + [N * pub[i]] for i in range(n)]
    B.append([1] * n + [N * c])
    for v in lll(B):
        if v[-1] == 0 and all(abs(x) == 1 for x in v[:-1]):
            bits = [(1 - x) // 2 for x in v[:-1]]
            if sum(b * a for b, a in zip(bits, pub)) == c:
                return bits
            bits = [1 - b for b in bits]
            if sum(b * a for b, a in zip(bits, pub)) == c:
                return bits
    return None


def lwe_keygen(n, m, q, rng, noise=2):
    s = [rng.randrange(q) for _ in range(n)]
    A = [[rng.randrange(q) for _ in range(n)] for _ in range(m)]
    e = [rng.randint(-noise, noise) for _ in range(m)]
    b = [(sum(a * x for a, x in zip(row, s)) + ei) % q for row, ei in zip(A, e)]
    return s, (A, b)


def lwe_encrypt(pub, bit, q, rng):
    """Regev (2005): sum a random subset of the public samples, add bit * q/2."""
    A, b = pub
    S = [i for i in range(len(A)) if rng.random() < 0.5]
    u = [sum(A[i][j] for i in S) % q for j in range(len(A[0]))]
    v = (sum(b[i] for i in S) + bit * (q // 2)) % q
    return u, v


def lwe_decrypt(s, ct, q):
    u, v = ct
    d = (v - sum(a * x for a, x in zip(u, s))) % q
    return int(q // 4 < d < 3 * q // 4), d


# ML-KEM's ring: Z_q[x]/(x^256 + 1), q = 3329, with FIPS 203's number-theoretic transform (zeta = 17).
MLQ, MLN = 3329, 256


def _bitrev7(i):
    return int(f"{i:07b}"[::-1], 2)


ZETAS = [pow(17, _bitrev7(i), MLQ) for i in range(128)]
GAMMAS = [pow(17, 2 * _bitrev7(i) + 1, MLQ) for i in range(128)]


def ntt(f):
    """FIPS 203 Algorithm 9."""
    f = list(f)
    i, length = 1, 128
    while length >= 2:
        for start in range(0, 256, 2 * length):
            z = ZETAS[i]
            i += 1
            for j in range(start, start + length):
                t = z * f[j + length] % MLQ
                f[j + length] = (f[j] - t) % MLQ
                f[j] = (f[j] + t) % MLQ
        length //= 2
    return f


def intt(f):
    """FIPS 203 Algorithm 10."""
    f = list(f)
    i, length = 127, 2
    while length <= 128:
        for start in range(0, 256, 2 * length):
            z = ZETAS[i]
            i -= 1
            for j in range(start, start + length):
                t = f[j]
                f[j] = (t + f[j + length]) % MLQ
                f[j + length] = z * (f[j + length] - t) % MLQ
        length *= 2
    return [x * 3303 % MLQ for x in f]


def ntt_mul(f, g):
    """Multiplication in the NTT domain: 128 products of degree-1 polynomials mod x^2 - gamma (FIPS 203 Alg. 11)."""
    h = [0] * 256
    for i in range(128):
        a0, a1, b0, b1, gm = f[2 * i], f[2 * i + 1], g[2 * i], g[2 * i + 1], GAMMAS[i]
        h[2 * i] = (a0 * b0 + a1 * b1 * gm) % MLQ
        h[2 * i + 1] = (a0 * b1 + a1 * b0) % MLQ
    return h


def poly_mul_schoolbook(f, g):
    h = [0] * 256
    for i, a in enumerate(f):
        if a:
            for j, b in enumerate(g):
                k = i + j
                if k < 256:
                    h[k] = (h[k] + a * b) % MLQ
                else:
                    h[k - 256] = (h[k - 256] - a * b) % MLQ
    return h


def cbd(eta, rng):
    return [sum(rng.getrandbits(1) for _ in range(eta)) - sum(rng.getrandbits(1) for _ in range(eta))
            for _ in range(256)]


def _compress(x, d):
    return ((x << d) + MLQ // 2) // MLQ % (1 << d)


def _decompress(y, d):
    return (y * MLQ + (1 << (d - 1))) >> d


def kpke_keygen(rng, k=2, eta=3):
    """ML-KEM-512's K-PKE arithmetic (k = 2, eta1 = 3, eta2 = 2, du = 10, dv = 4), with our own random sampling
    instead of SHAKE and no byte encodings."""
    A = [[[rng.randrange(MLQ) for _ in range(256)] for _ in range(k)] for _ in range(k)]   # already NTT domain
    s = [ntt([x % MLQ for x in cbd(eta, rng)]) for _ in range(k)]
    e = [ntt([x % MLQ for x in cbd(eta, rng)]) for _ in range(k)]
    t = [[(sum(ntt_mul(A[i][j], s[j])[c] for j in range(k)) + e[i][c]) % MLQ for c in range(256)] for i in range(k)]
    return {"A": A, "t": t, "s": s, "k": k}


def kpke_encrypt(pub, m_bits, rng, eta1=3, eta2=2, du=10, dv=4):
    k, A, t = pub["k"], pub["A"], pub["t"]
    r = [ntt([x % MLQ for x in cbd(eta1, rng)]) for _ in range(k)]
    e1 = [[x % MLQ for x in cbd(eta2, rng)] for _ in range(k)]
    e2 = [x % MLQ for x in cbd(eta2, rng)]
    u = []
    for i in range(k):
        acc = [sum(ntt_mul(A[j][i], r[j])[c] for j in range(k)) % MLQ for c in range(256)]
        u.append([(a + b) % MLQ for a, b in zip(intt(acc), e1[i])])
    mu = [_decompress(b, 1) for b in m_bits]
    vt = [sum(ntt_mul(t[j], r[j])[c] for j in range(k)) % MLQ for c in range(256)]
    v = [(a + b + c) % MLQ for a, b, c in zip(intt(vt), e2, mu)]
    return [[_compress(x, du) for x in ui] for ui in u], [_compress(x, dv) for x in v]


def kpke_decrypt(sk, ct, du=10, dv=4):
    k, s = sk["k"], sk["s"]
    c1, c2 = ct
    u = [ntt([_decompress(x, du) for x in ci]) for ci in c1]
    v = [_decompress(x, dv) for x in c2]
    su = intt([sum(ntt_mul(s[j], u[j])[c] for j in range(k)) % MLQ for c in range(256)])
    w = [(a - b) % MLQ for a, b in zip(v, su)]
    return [_compress(x, 1) for x in w], w


# --------------------------------------------------------------------------------------------- signatures and sharing

def lamport_keygen(rng, bits=256):
    sk = [[bytes(rng.randrange(256) for _ in range(32)) for _ in range(2)] for _ in range(bits)]
    return sk, [[H(x) for x in pair] for pair in sk]


def lamport_sign(sk, msg):
    h = b2i(H(msg))
    return [sk[i][(h >> (255 - i)) & 1] for i in range(256)]


def lamport_verify(pk, msg, sig):
    h = b2i(H(msg))
    return all(H(sig[i]) == pk[i][(h >> (255 - i)) & 1] for i in range(256))


def schnorr_group(rng, qbits=160, pbits=512):
    """A prime-order-q subgroup of Z_p^*: p = k q + 1."""
    q = random_prime(qbits, rng)
    while True:
        kk = rng.getrandbits(pbits - qbits) | 1 << (pbits - qbits - 1)
        p = kk * q + 1
        if is_probable_prime(p, rng):
            break
    while True:
        g = pow(rng.randrange(2, p - 1), (p - 1) // q, p)
        if g != 1:
            return p, q, g


def schnorr_sign(x, msg, grp, rng):
    p, q, g = grp
    k = rng.randrange(1, q)
    R = pow(g, k, p)
    e = b2i(H(i2b(R, (p.bit_length() + 7) // 8) + msg)) % q
    return e, (k + e * x) % q


def schnorr_verify(y, msg, sig, grp):
    p, q, g = grp
    e, s = sig
    R = pow(g, s, p) * pow(y, -e, p) % p
    return b2i(H(i2b(R, (p.bit_length() + 7) // 8) + msg)) % q == e


def shamir_split(secret, k, n, p, rng):
    coeffs = [secret] + [rng.randrange(p) for _ in range(k - 1)]
    return [(x, sum(c * pow(x, i, p) for i, c in enumerate(coeffs)) % p) for x in range(1, n + 1)], coeffs


def shamir_combine(shares, p):
    s = 0
    for i, (xi, yi) in enumerate(shares):
        num = den = 1
        for j, (xj, _) in enumerate(shares):
            if i != j:
                num = num * -xj % p
                den = den * (xi - xj) % p
        s = (s + yi * num * inv_mod(den, p)) % p
    return s
