"""Error-correcting codes for Part 28 of *Computer Science, Built* ("Error-Correcting Codes").

Small teaching implementations, including exact algebra and Monte Carlo experiments:

* channels and information: the binary symmetric channel, entropy, capacity;
* repetition codes, Hamming(7,4) and the general Hamming code, SECDED; linear codes by enumeration; the binary
  Golay code; the asymptotic rate--distance bounds;
* finite fields: GF(p) and GF(2^8) with exp/log tables;
* Reed--Solomon two ways: the evaluation view over GF(p) (Lagrange erasures, Berlekamp--Welch errors) and the
  generator view over GF(256) used by QR codes (Berlekamp--Massey, Chien, Forney, with erasures);
* a QR code (version 2, byte mode) encoder and a decoder that reads a damaged module matrix;
* CRCs as polynomial division, CRC-8 and CRC-32 (checked against zlib in the tests);
* random linear codes with syndrome decoding; the (7,5) convolutional code with Viterbi decoding;
* regular LDPC codes with belief propagation and BEC density evolution; polar codes with successive cancellation;
* LT fountain codes with a peeling decoder; RAID-6 P+Q; the Hadamard code's two-query local decoder.
"""

from __future__ import annotations

import itertools
import math
import random

import numpy as np


# ----------------------------------------------------------------------------------------------- information

def H2(p):
    """Binary entropy in bits."""
    if p <= 0 or p >= 1:
        return 0.0
    return -p * math.log2(p) - (1 - p) * math.log2(1 - p)


def capacity_bsc(p):
    return 1 - H2(p)


def bsc(bits, p, rng):
    return [b ^ (rng.random() < p) for b in bits]


def weight(x):
    return bin(x).count("1")


def binom_tail(n, k, p):
    """P[Binomial(n, p) >= k]."""
    return sum(math.comb(n, j) * p ** j * (1 - p) ** (n - j) for j in range(k, n + 1))


# ----------------------------------------------------------------------------------------------- simple codes

def repetition_error(n, p):
    """Bit error rate of the n-fold repetition code (n odd) with majority decoding."""
    return binom_tail(n, n // 2 + 1, p)


def hamming74_encode(d):
    """d = [d1, d2, d3, d4] -> 7 bits at positions 1..7, parity at 1, 2, 4 (Hamming's layout)."""
    d1, d2, d3, d4 = d
    p1 = d1 ^ d2 ^ d4
    p2 = d1 ^ d3 ^ d4
    p4 = d2 ^ d3 ^ d4
    return [p1, p2, d1, p4, d2, d3, d4]


def hamming74_syndrome(c):
    """The XOR of the (1-based) positions holding a 1: zero for a codeword, else the position of a single error."""
    s = 0
    for i, b in enumerate(c, start=1):
        if b:
            s ^= i
    return s


def hamming74_decode(c):
    c = list(c)
    s = hamming74_syndrome(c)
    if s:
        c[s - 1] ^= 1
    return [c[2], c[4], c[5], c[6]], s


def hamming_parity_check(r):
    """Columns are the binary expansions of 1 .. 2^r - 1: the parity-check matrix of Hamming(2^r - 1, 2^r - 1 - r)."""
    n = (1 << r) - 1
    return [[(j >> i) & 1 for j in range(1, n + 1)] for i in range(r)]


def secded_decode(c8):
    """Extended Hamming (8,4): c8 = hamming74 codeword + overall parity bit. Returns (data, status) where status is
    'ok', 'corrected' or 'double' (detected, not correctable)."""
    c7, par = list(c8[:7]), c8[7]
    s = hamming74_syndrome(c7)
    overall = (sum(c7) + par) % 2
    if s == 0 and overall == 0:
        return [c7[2], c7[4], c7[5], c7[6]], "ok"
    if overall == 1:
        if s:
            c7[s - 1] ^= 1
        return [c7[2], c7[4], c7[5], c7[6]], "corrected"
    return None, "double"


def codewords(gen_rows):
    """All codewords spanned by the generator rows (ints)."""
    words = [0]
    for g in gen_rows:
        words += [w ^ g for w in words]
    return words


def weight_distribution(words, n):
    dist = [0] * (n + 1)
    for w in words:
        dist[weight(w)] += 1
    return dist


def min_distance(words):
    return min(weight(w) for w in words if w)


def golay23_generators():
    """Rows x^i g(x), i = 0..11, for g(x) = x^11 + x^10 + x^6 + x^5 + x^4 + x^2 + 1: the [23, 12, 7] Golay code."""
    g = 0b110001110101
    return [g << i for i in range(12)]


def hamming_bound(delta):
    return max(0.0, 1 - H2(delta / 2))


def singleton_bound(delta):
    return max(0.0, 1 - delta)


def gv_bound(delta):
    return max(0.0, 1 - H2(delta)) if delta < 0.5 else 0.0


def mrrw_bound(delta):
    """The first linear-programming bound of McEliece, Rodemich, Rumsey and Welch (1977)."""
    if delta >= 0.5:
        return 0.0
    return H2(0.5 - math.sqrt(delta * (1 - delta)))


def plotkin_bound(delta):
    return max(0.0, 1 - 2 * delta)


# ----------------------------------------------------------------------------------------------- GF(256)

PRIM = 0x11D          # x^8 + x^4 + x^3 + x^2 + 1, the QR code's field
GF_EXP = [0] * 512
GF_LOG = [0] * 256


def _init_tables():
    x = 1
    for i in range(255):
        GF_EXP[i] = x
        GF_LOG[x] = i
        x <<= 1
        if x & 0x100:
            x ^= PRIM
    for i in range(255, 512):
        GF_EXP[i] = GF_EXP[i - 255]


_init_tables()


def gf_mul(a, b):
    if a == 0 or b == 0:
        return 0
    return GF_EXP[GF_LOG[a] + GF_LOG[b]]


def gf_div(a, b):
    if b == 0:
        raise ZeroDivisionError
    if a == 0:
        return 0
    return GF_EXP[(GF_LOG[a] + 255 - GF_LOG[b]) % 255]


def gf_pow(a, k):
    if a == 0:
        if k < 0:
            raise ZeroDivisionError("zero has no multiplicative inverse")
        return 0 if k else 1
    return GF_EXP[(GF_LOG[a] * k) % 255]


def gf_inv(a):
    if a == 0:
        raise ZeroDivisionError("zero has no multiplicative inverse")
    return GF_EXP[255 - GF_LOG[a]]


def gf_mul_slow(a, b, prim=PRIM):
    """Carry-less multiplication reduced by the field polynomial: what the tables encode."""
    r = 0
    while b:
        if b & 1:
            r ^= a
        b >>= 1
        a <<= 1
        if a & 0x100:
            a ^= prim
    return r


# polynomials over GF(256), highest-degree coefficient first

def gp_scale(p, x):
    return [gf_mul(c, x) for c in p]


def gp_add(p, q):
    r = [0] * max(len(p), len(q))
    for i, c in enumerate(p):
        r[i + len(r) - len(p)] = c
    for i, c in enumerate(q):
        r[i + len(r) - len(q)] ^= c
    return r


def gp_mul(p, q):
    r = [0] * (len(p) + len(q) - 1)
    for j, b in enumerate(q):
        for i, a in enumerate(p):
            r[i + j] ^= gf_mul(a, b)
    return r


def gp_eval(p, x):
    y = p[0]
    for c in p[1:]:
        y = gf_mul(y, x) ^ c
    return y


def gp_divmod(dividend, divisor):
    """Synthetic division by a monic divisor."""
    if not divisor or divisor[0] != 1:
        raise ValueError("divisor must be monic and nonzero")
    if len(divisor) == 1:
        return list(dividend), []
    if len(dividend) < len(divisor):
        return [], list(dividend)
    out = list(dividend)
    for i in range(len(dividend) - len(divisor) + 1):
        coef = out[i]
        if coef:
            for j in range(1, len(divisor)):
                if divisor[j]:
                    out[i + j] ^= gf_mul(divisor[j], coef)
    sep = -(len(divisor) - 1)
    return out[:sep], out[sep:]


# ----------------------------------------------------------------------------------------------- Reed--Solomon, GF(256)

def rs_generator(nsym):
    g = [1]
    for i in range(nsym):
        g = gp_mul(g, [1, gf_pow(2, i)])
    return g


def rs_encode(msg, nsym):
    """Systematic encoding: msg followed by nsym check symbols (the remainder of msg * x^nsym by the generator)."""
    msg = list(msg)
    if not isinstance(nsym, int) or not 0 <= nsym <= 255 or len(msg) + nsym > 255:
        raise ValueError("RS length must be at most 255 with nonnegative parity length")
    _, rem = gp_divmod(msg + [0] * nsym, rs_generator(nsym))
    return msg + rem


def rs_syndromes(cw, nsym):
    return [gp_eval(cw, gf_pow(2, i)) for i in range(nsym)]


def _errata_locator(pos_coefs):
    loc = [1]
    for p in pos_coefs:
        loc = gp_mul(loc, gp_add([1], [gf_pow(2, p), 0]))
    return loc


def _error_evaluator(synd, loc, nsym):
    _, rem = gp_divmod(gp_mul(synd, loc), [1] + [0] * (nsym + 1))
    return rem


def _correct_errata(cw, synd, err_pos):
    """Forney's algorithm: values of the errors at the given positions (indices into cw)."""
    cpos = [len(cw) - 1 - p for p in err_pos]
    loc = _errata_locator(cpos)
    ev = _error_evaluator(synd[::-1], loc, len(loc) - 1)[::-1]
    X = [gf_pow(2, p) for p in cpos]
    E = [0] * len(cw)
    for i, Xi in enumerate(X):
        Xi_inv = gf_inv(Xi)
        prime = 1
        for j, Xj in enumerate(X):
            if j != i:
                prime = gf_mul(prime, 1 ^ gf_mul(Xi_inv, Xj))
        y = gf_mul(gp_eval(ev[::-1], Xi_inv), Xi)          # fcr = 0
        if prime == 0:
            raise ValueError("Forney: zero derivative")
        E[err_pos[i]] = gf_div(y, prime)
    return gp_add(cw, E)


def _berlekamp_massey(synd, nsym, erase_count=0):
    """Error locator from (Forney-modified) syndromes, highest degree first."""
    err_loc, old_loc = [1], [1]
    shift = len(synd) - nsym if len(synd) > nsym else 0
    for i in range(nsym - erase_count):
        K = i + shift
        delta = synd[K]
        for j in range(1, len(err_loc)):
            delta ^= gf_mul(err_loc[-(j + 1)], synd[K - j])
        old_loc = old_loc + [0]
        if delta:
            if len(old_loc) > len(err_loc):
                new_loc = gp_scale(old_loc, delta)
                old_loc = gp_scale(err_loc, gf_inv(delta))
                err_loc = new_loc
            err_loc = gp_add(err_loc, gp_scale(old_loc, delta))
    while err_loc and err_loc[0] == 0:
        err_loc.pop(0)
    errs = len(err_loc) - 1
    if (errs - erase_count) * 2 + erase_count > nsym:
        raise ValueError("too many errors")
    return err_loc


def _chien(err_loc_rev, n):
    """Positions (indices into the codeword) where the reversed locator vanishes."""
    errs = len(err_loc_rev) - 1
    pos = [n - 1 - i for i in range(n) if gp_eval(err_loc_rev, gf_pow(2, i)) == 0]
    if len(pos) != errs:
        raise ValueError("could not locate the errors")
    return pos


def _forney_syndromes(synd, pos, n):
    rev = [n - 1 - p for p in pos]
    fsynd = list(synd[1:])
    for p in rev:
        x = gf_pow(2, p)
        for j in range(len(fsynd) - 1):
            fsynd[j] = gf_mul(fsynd[j], x) ^ fsynd[j + 1]
    return fsynd


def rs_decode(cw, nsym, erase_pos=()):
    """Correct e errors and f erasures whenever 2e + f <= nsym (Berlekamp--Massey, Chien search, Forney).
    Returns (corrected codeword, sorted errata positions)."""
    out = list(cw)
    erase_pos = list(erase_pos)
    if not isinstance(nsym, int) or not 0 <= nsym <= len(out) <= 255:
        raise ValueError("RS length must be at most 255 and parity length must fit")
    if len(set(erase_pos)) != len(erase_pos) or any(not isinstance(p, int) or not 0 <= p < len(out)
                                                for p in erase_pos):
        raise ValueError("erasure positions must be distinct codeword indices")
    for p in erase_pos:
        out[p] = 0
    if len(erase_pos) > nsym:
        raise ValueError("too many erasures")
    synd = [0] + rs_syndromes(out, nsym)
    if max(synd) == 0:
        return out, []
    fsynd = _forney_syndromes(synd, erase_pos, len(out))
    err_loc = _berlekamp_massey(fsynd, nsym, erase_count=len(erase_pos))
    err_pos = _chien(err_loc[::-1], len(out))
    allpos = erase_pos + err_pos
    out = _correct_errata(out, synd, allpos)
    if max(rs_syndromes(out, nsym)) > 0:
        raise ValueError("could not correct")
    return out, sorted(allpos)


# ----------------------------------------------------------------------------------------------- Reed--Solomon, GF(p)

def poly_eval_p(coefs, x, p):
    """coefs lowest degree first."""
    y = 0
    for c in reversed(coefs):
        y = (y * x + c) % p
    return y


def rs_eval_encode(msg, xs, p):
    """The evaluation view: the codeword is the message polynomial at n distinct points."""
    return [poly_eval_p(msg, x, p) for x in xs]


def lagrange_coeffs(points, p):
    """The unique polynomial of degree < len(points) through the points, as coefficients (lowest first)."""
    k = len(points)
    out = [0] * k
    for i, (xi, yi) in enumerate(points):
        basis, denom = [1], 1
        for j, (xj, _) in enumerate(points):
            if j == i:
                continue
            basis = [((basis[t - 1] if t else 0) - xj * (basis[t] if t < len(basis) else 0)) % p
                     for t in range(len(basis) + 1)]
            denom = denom * (xi - xj) % p
        f = yi * pow(denom, p - 2, p) % p
        for t in range(k):
            out[t] = (out[t] + f * basis[t]) % p
    return out


def solve_mod_p(A, b, p):
    """Gaussian elimination mod p; returns one solution or None."""
    n, m = len(A), len(A[0])
    M = [list(A[i]) + [b[i]] for i in range(n)]
    piv_cols, r = [], 0
    for c in range(m):
        piv = next((i for i in range(r, n) if M[i][c] % p), None)
        if piv is None:
            continue
        M[r], M[piv] = M[piv], M[r]
        inv = pow(M[r][c], p - 2, p)
        M[r] = [v * inv % p for v in M[r]]
        for i in range(n):
            if i != r and M[i][c]:
                f = M[i][c]
                M[i] = [(a - f * bb) % p for a, bb in zip(M[i], M[r])]
        piv_cols.append(c)
        r += 1
    if any(M[i][m] for i in range(r, n)):
        return None
    x = [0] * m
    for i, c in enumerate(piv_cols):
        x[c] = M[i][m]
    return x


def poly_div_p(num, den, p):
    """Exact division of polynomials (lowest first) mod p: (quotient, remainder)."""
    num = list(num)
    while den and den[-1] % p == 0:
        den = den[:-1]
    q = [0] * max(1, len(num) - len(den) + 1)
    inv = pow(den[-1], p - 2, p)
    for i in range(len(num) - len(den), -1, -1):
        f = num[i + len(den) - 1] * inv % p
        q[i] = f
        for j, d in enumerate(den):
            num[i + j] = (num[i + j] - f * d) % p
    return q, num[:len(den) - 1]


def berlekamp_welch(points, k, e, p):
    """Decode a degree-<k message polynomial from n points with at most e errors (n >= k + 2e).
    Solves y_i E(x_i) = Q(x_i) with E monic of degree e and deg Q < k + e; returns (message coefs, error x's)."""
    points = list(points)
    if k < 1 or e < 0 or len(points) < k + 2 * e:
        raise ValueError("need k >= 1, e >= 0 and at least k + 2e points")
    if len({x % p for x, _ in points}) != len(points):
        raise ValueError("evaluation points must be distinct in the field")
    rows, rhs = [], []
    for x, y in points:
        row = [y * pow(x, j, p) % p for j in range(e)] + [(-pow(x, j, p)) % p for j in range(k + e)]
        rows.append(row)
        rhs.append((-y * pow(x, e, p)) % p)
    sol = solve_mod_p(rows, rhs, p)
    if sol is None:
        return None, None
    E = sol[:e] + [1]
    Q = sol[e:]
    msg, rem = poly_div_p(Q, E, p)
    if any(rem):
        return None, None
    if any(msg[k:]):
        return None, None
    msg = (msg + [0] * k)[:k]
    # E can have extra roots when the actual error count is smaller than e.
    bad = [x for x, y in points if poly_eval_p(msg, x, p) != y % p]
    return (msg, bad) if len(bad) <= e else (None, None)


# ----------------------------------------------------------------------------------------------- QR codes, version 2

QR_SIZE = 25
QR_EC = {"L": (1, 34, 10), "M": (0, 28, 16), "Q": (3, 22, 22), "H": (2, 16, 28)}   # format bits, data, ec


def _qr_function_map():
    size = QR_SIZE
    mods = [[False] * size for _ in range(size)]
    func = [[False] * size for _ in range(size)]

    def setf(x, y, dark):
        mods[y][x] = dark
        func[y][x] = True

    for i in range(size):
        setf(6, i, i % 2 == 0)
        setf(i, 6, i % 2 == 0)
    for cx, cy in ((3, 3), (size - 4, 3), (3, size - 4)):
        for dy in range(-4, 5):
            for dx in range(-4, 5):
                x, y = cx + dx, cy + dy
                if 0 <= x < size and 0 <= y < size:
                    d = max(abs(dx), abs(dy))
                    setf(x, y, d not in (2, 4))
    for dy in range(-2, 3):
        for dx in range(-2, 3):
            setf(18 + dx, 18 + dy, max(abs(dx), abs(dy)) != 1)
    _draw_format(setf, 0, 0)            # reserve; overwritten later
    return mods, func


def qr_format_bits(ecl, mask):
    data = QR_EC[ecl][0] << 3 | mask
    rem = data
    for _ in range(10):
        rem = (rem << 1) ^ ((rem >> 9) * 0x537)
    return (data << 10 | rem) ^ 0x5412


def _draw_format(setf, ecl_bits, mask, bits=None):
    size = QR_SIZE
    if bits is None:
        data = ecl_bits << 3 | mask
        rem = data
        for _ in range(10):
            rem = (rem << 1) ^ ((rem >> 9) * 0x537)
        bits = (data << 10 | rem) ^ 0x5412
    g = lambda i: (bits >> i) & 1 == 1      # noqa: E731
    for i in range(6):
        setf(8, i, g(i))
    setf(8, 7, g(6))
    setf(8, 8, g(7))
    setf(7, 8, g(8))
    for i in range(9, 15):
        setf(14 - i, 8, g(i))
    for i in range(8):
        setf(size - 1 - i, 8, g(i))
    for i in range(8, 15):
        setf(8, size - 15 + i, g(i))
    setf(8, size - 8, True)


def _format_positions():
    size = QR_SIZE
    a = [(8, i) for i in range(6)] + [(8, 7), (8, 8), (7, 8)] + [(14 - i, 8) for i in range(9, 15)]
    b = [(size - 1 - i, 8) for i in range(8)] + [(8, size - 15 + i) for i in range(8, 15)]
    return a, b


def _data_positions(func):
    size = QR_SIZE
    out = []
    right = size - 1
    while right >= 1:
        if right == 6:
            right = 5
        for vert in range(size):
            for j in range(2):
                x = right - j
                upward = ((right + 1) & 2) == 0
                y = size - 1 - vert if upward else vert
                if not func[y][x]:
                    out.append((x, y))
        right -= 2
    return out


def _mask_fn(mask):
    return [lambda x, y: (x + y) % 2 == 0, lambda x, y: y % 2 == 0, lambda x, y: x % 3 == 0,
            lambda x, y: (x + y) % 3 == 0, lambda x, y: (x // 3 + y // 2) % 2 == 0,
            lambda x, y: x * y % 2 + x * y % 3 == 0, lambda x, y: (x * y % 2 + x * y % 3) % 2 == 0,
            lambda x, y: ((x + y) % 2 + x * y % 3) % 2 == 0][mask]


def qr_data_codewords(text, ecl):
    _, ndata, _ = QR_EC[ecl]
    data = text.encode("utf-8")
    bits = [0, 1, 0, 0] + [(len(data) >> i) & 1 for i in range(7, -1, -1)]
    for b in data:
        bits += [(b >> i) & 1 for i in range(7, -1, -1)]
    cap = ndata * 8
    if len(bits) > cap:
        raise ValueError("message too long for version 2-" + ecl)
    bits += [0] * min(4, cap - len(bits))
    bits += [0] * (-len(bits) % 8)
    out = [int("".join(map(str, bits[i:i + 8])), 2) for i in range(0, len(bits), 8)]
    pad = 0xEC
    while len(out) < ndata:
        out.append(pad)
        pad ^= 0xEC ^ 0x11
    return out


def qr_encode(text, ecl="Q", mask=None):
    """A version-2 QR code as a 25 x 25 list of rows of booleans (True = dark). Returns (matrix, info)."""
    _, ndata, nec = QR_EC[ecl]
    data = qr_data_codewords(text, ecl)
    cw = rs_encode(data, nec)
    mods, func = _qr_function_map()
    pos = _data_positions(func)
    bits = [(c >> (7 - i)) & 1 for c in cw for i in range(8)]
    for k, (x, y) in enumerate(pos):
        mods[y][x] = bool(bits[k]) if k < len(bits) else False
    best = None
    for m in ([mask] if mask is not None else range(8)):
        M = [row[:] for row in mods]
        f = _mask_fn(m)
        for x, y in pos:
            if f(x, y):
                M[y][x] = not M[y][x]

        def setf(x, y, dark, M=M):
            M[y][x] = dark
        _draw_format(setf, QR_EC[ecl][0], m)
        pen = qr_penalty(M)
        if best is None or pen < best[0]:
            best = (pen, m, M)
    _, m, M = best
    return M, {"ecl": ecl, "mask": m, "data": data, "codewords": cw, "positions": pos, "func": func}


def qr_penalty(M):
    """The standard's four mask-penalty rules (as in Nayuki's reference implementation)."""
    size = len(M)
    pen = 0

    def runs(line):
        p, run, prev = 0, 0, None
        for v in line:
            if v == prev:
                run += 1
            else:
                if run >= 5:
                    p += 3 + run - 5
                run, prev = 1, v
        if run >= 5:
            p += 3 + run - 5
        return p
    for r in range(size):
        pen += runs(M[r])
        pen += runs([M[y][r] for y in range(size)])
    for y in range(size - 1):
        for x in range(size - 1):
            if M[y][x] == M[y][x + 1] == M[y + 1][x] == M[y + 1][x + 1]:
                pen += 3
    pat = [True, False, True, True, True, False, True]
    for r in range(size):
        rows = [M[r], [M[y][r] for y in range(size)]]
        for line in rows:
            for i in range(size - 6):
                if line[i:i + 7] == pat:
                    before = line[max(0, i - 4):i]
                    after = line[i + 7:i + 11]
                    if (len(before) == 4 and not any(before)) or (len(after) == 4 and not any(after)):
                        pen += 40
    dark = sum(map(sum, M))
    total = size * size
    k = (abs(dark * 20 - total * 10) + total - 1) // total - 1
    pen += max(0, k) * 10
    return pen


def qr_decode(M, erasures=None):
    """Read a (possibly damaged) version-2 matrix. erasures: optional set of (x, y) modules known to be unreadable.
    Returns dict(text, ecl, mask, errors, erased, codewords_read)."""
    fa, fb = _format_positions()
    best = None
    for ecl, (fbits, _, _) in QR_EC.items():
        for mask in range(8):
            ref = qr_format_bits(ecl, mask)
            for posl in (fa, fb):
                read = sum((1 << i) for i, (x, y) in enumerate(posl) if M[y][x])
                d = weight(read ^ ref)
                if best is None or d < best[0]:
                    best = (d, ecl, mask)
    _, ecl, mask = best
    _, ndata, nec = QR_EC[ecl]
    _, func = _qr_function_map()
    pos = _data_positions(func)
    f = _mask_fn(mask)
    ncw = ndata + nec
    bits = []
    for x, y in pos[:ncw * 8]:
        v = M[y][x] ^ f(x, y)
        bits.append(int(v))
    cw = [int("".join(map(str, bits[i:i + 8])), 2) for i in range(0, ncw * 8, 8)]
    erase = []
    if erasures:
        for k, (x, y) in enumerate(pos[:ncw * 8]):
            if (x, y) in erasures and k // 8 not in erase:
                erase.append(k // 8)
    fixed, errpos = rs_decode(cw, nec, erase_pos=erase)
    data = fixed[:ndata]
    bitstr = "".join(f"{b:08b}" for b in data)
    assert bitstr[:4] == "0100", "not byte mode"
    count = int(bitstr[4:12], 2)
    raw = bytes(int(bitstr[12 + 8 * i:20 + 8 * i], 2) for i in range(count))
    wrong = [i for i in range(ncw) if cw[i] != fixed[i] and i not in erase]
    return {"text": raw.decode("utf-8"), "ecl": ecl, "mask": mask, "errors": wrong, "erased": sorted(erase),
            "read": cw, "fixed": fixed, "positions": errpos}


# ----------------------------------------------------------------------------------------------- CRC

def crc_remainder(bits, poly):
    """Remainder of bits(x) * x^r divided by poly(x) over GF(2); poly as a list of bits, highest first (r + 1 long)."""
    r = len(poly) - 1
    reg = list(bits) + [0] * r
    for i in range(len(bits)):
        if reg[i]:
            for j, pb in enumerate(poly):
                reg[i + j] ^= pb
    return reg[-r:]


def crc8(data, poly=0x07):
    c = 0
    for b in data:
        c ^= b
        for _ in range(8):
            c = ((c << 1) ^ poly) & 0xFF if c & 0x80 else (c << 1) & 0xFF
    return c


_CRC32 = []
for _n in range(256):
    _c = _n
    for _ in range(8):
        _c = (_c >> 1) ^ 0xEDB88320 if _c & 1 else _c >> 1
    _CRC32.append(_c)


def crc32(data):
    """The CRC-32 of Ethernet, zip and PNG (reflected, polynomial 0x04C11DB7, init and xor-out 0xFFFFFFFF)."""
    c = 0xFFFFFFFF
    for b in data:
        c = _CRC32[(c ^ b) & 0xFF] ^ (c >> 8)
    return c ^ 0xFFFFFFFF


# ----------------------------------------------------------------------------------------------- random linear codes

def random_systematic(n, k, rng):
    """Generator rows (ints, n bits) [I_k | A] and parity-check rows [A^T | I_{n-k}], bit j = position j."""
    A = [[rng.randrange(2) for _ in range(n - k)] for _ in range(k)]
    G = []
    for i in range(k):
        w = 1 << i
        for j in range(n - k):
            if A[i][j]:
                w |= 1 << (k + j)
        G.append(w)
    Hrows = []
    for j in range(n - k):
        h = 1 << (k + j)
        for i in range(k):
            if A[i][j]:
                h |= 1 << i
        Hrows.append(h)
    return G, Hrows


def syndrome(word, Hrows):
    s = 0
    for j, h in enumerate(Hrows):
        if weight(word & h) & 1:
            s |= 1 << j
    return s


def coset_leaders(n, Hrows):
    """Minimum-weight error pattern for every syndrome: maximum-likelihood decoding on the BSC."""
    r = len(Hrows)
    table = {}
    for w in range(n + 1):
        for pos in itertools.combinations(range(n), w):
            e = sum(1 << i for i in pos)
            s = syndrome(e, Hrows)
            if s not in table:
                table[s] = e
        if len(table) == 1 << r:
            break
    return table


def block_error_rate(n, k, p, trials, rng, code=None):
    """Random [n, k] code (or the given (G, H)), ML-decoded on BSC(p): fraction of blocks decoded wrongly. By
    linearity the all-zero codeword is as good as any."""
    G, Hrows = code or random_systematic(n, k, rng)
    table = coset_leaders(n, Hrows)
    bad = 0
    for _ in range(trials):
        e = sum(1 << i for i in range(n) if rng.random() < p)
        if table[syndrome(e, Hrows)] != e:
            bad += 1
    return bad / trials


# ----------------------------------------------------------------------------------------------- convolutional code

CONV_G = (0b111, 0b101)        # the (7, 5) code, constraint length 3


def conv_encode(bits):
    s = 0
    out = []
    for b in list(bits) + [0, 0]:
        s = ((s << 1) | b) & 0b111
        out += [weight(s & CONV_G[0]) & 1, weight(s & CONV_G[1]) & 1]
    return out


def viterbi(rx):
    """Hard-decision Viterbi decoding of conv_encode's output (terminated), with traceback pointers."""
    INF = 10 ** 9
    T = len(rx) // 2
    metric = [0, INF, INF, INF]
    back = []                      # back[t][state] = (previous state, input bit)
    trans = []
    for st in range(4):
        for b in (0, 1):
            s = ((st << 1) | b) & 0b111
            trans.append((st, b, s & 0b11, weight(s & CONV_G[0]) & 1, weight(s & CONV_G[1]) & 1))
    for t in range(T):
        r0, r1 = rx[2 * t], rx[2 * t + 1]
        new = [INF] * 4
        bp = [None] * 4
        for st, b, ns, o0, o1 in trans:
            if metric[st] >= INF:
                continue
            m = metric[st] + (o0 != r0) + (o1 != r1)
            if m < new[ns]:
                new[ns] = m
                bp[ns] = (st, b)
        metric = new
        back.append(bp)
    st, bits = 0, []
    for t in range(T - 1, -1, -1):
        prev, b = back[t][st]
        bits.append(b)
        st = prev
    return bits[::-1][:-2]


# ----------------------------------------------------------------------------------------------- LDPC

def gallager_ldpc(n, wc, wr, rng, girth6=True):
    """A regular (wc, wr) parity-check matrix by Gallager's construction: wc stacked bands, each a random column
    permutation of a band of disjoint row blocks. With girth6, positions are swapped until no two variables share
    two checks (no 4-cycles), with at most 200 repair passes per band. Check has_4cycle on the result:
    the bounded repair is not a guarantee. Returns the edge list (check, variable) and the number of checks."""
    if not all(isinstance(v, int) and v > 0 for v in (n, wc, wr)) or n % wr:
        raise ValueError("positive degrees and length divisible by row weight required")
    m_band = n // wr
    bands = [list(range(n))]
    for _ in range(1, wc):
        perm = list(range(n))
        rng.shuffle(perm)
        bands.append(perm)

    def checks_of(b):
        return [bands[b][c * wr:(c + 1) * wr] for c in range(m_band)]

    if girth6:
        for b in range(1, wc):
            for _ in range(200):
                seen = {}
                for bb in range(b):
                    for c, vs in enumerate(checks_of(bb)):
                        for v in vs:
                            seen.setdefault(v, set()).update(vs)
                bad = []
                for c, vs in enumerate(checks_of(b)):
                    for i, v in enumerate(vs):
                        if any(u != v and u in seen.get(v, ()) for u in vs):
                            bad.append(c * wr + i)
                if not bad:
                    break
                for pos in bad:
                    j = rng.randrange(n)
                    bands[b][pos], bands[b][j] = bands[b][j], bands[b][pos]
    edges = [(b * m_band + c, v) for b in range(wc) for c, vs in enumerate(checks_of(b)) for v in vs]
    return edges, wc * m_band


def has_4cycle(edges):
    by_var = {}
    for c, v in edges:
        by_var.setdefault(v, set()).add(c)
    pairs = set()
    by_check = {}
    for c, v in edges:
        by_check.setdefault(c, []).append(v)
    for c, vs in by_check.items():
        for i in range(len(vs)):
            for j in range(i + 1, len(vs)):
                key = (min(vs[i], vs[j]), max(vs[i], vs[j]))
                if key in pairs:
                    return True
                pairs.add(key)
    return False


def ldpc_bp_bsc(edges, m, n, p, trials, rng, iters=50):
    """Sum-product decoding on BSC(p) with the all-zero codeword (the decoder is symmetric, so this is general).
    Returns (bit error rate, frame error rate)."""
    ch = np.array([c for c, _ in edges])
    va = np.array([v for _, v in edges])
    L0 = math.log((1 - p) / p)
    nrng = np.random.default_rng(rng.randrange(1 << 30))
    bit_err = frame_err = 0
    order = np.argsort(ch, kind="stable")
    ch_sorted = ch[order]
    starts = np.searchsorted(ch_sorted, np.arange(m))
    for _ in range(trials):
        flips = nrng.random(n) < p
        llr = np.where(flips, -L0, L0)
        v2c = llr[va].copy()
        for _ in range(iters):
            t = np.tanh(np.clip(v2c, -30, 30) / 2)
            t = np.where(np.abs(t) < 1e-12, 1e-12, t)
            logabs = np.log(np.abs(t))
            neg = (t < 0).astype(np.int64)
            sum_log = np.add.reduceat(logabs[order], starts)
            sum_neg = np.add.reduceat(neg[order], starts)
            ext_log = sum_log[ch] - logabs
            ext_neg = (sum_neg[ch] - neg) % 2
            prod = np.exp(ext_log) * np.where(ext_neg == 1, -1.0, 1.0)
            prod = np.clip(prod, -0.999999, 0.999999)
            c2v = 2 * np.arctanh(prod)
            total = llr + np.bincount(va, weights=c2v, minlength=n)
            hard = total < 0
            # The receiver can check parity; it does not know the transmitted word.
            parity = np.bincount(ch, weights=hard[va].astype(float), minlength=m) % 2
            if not parity.any():
                break
            v2c = total[va] - c2v
        errs = int(hard.sum())
        bit_err += errs
        frame_err += errs > 0
    return bit_err / (trials * n), frame_err / trials


def de_bec_threshold(wc, wr, tol=1e-6):
    """Density evolution on the erasure channel: the largest eps with x -> eps (1 - (1 - x)^(wr-1))^(wc-1) -> 0."""
    def converges(eps):
        x = eps
        for _ in range(20000):
            x2 = eps * (1 - (1 - x) ** (wr - 1)) ** (wc - 1)
            if x2 < 1e-10:
                return True
            if abs(x2 - x) < 1e-14:
                return False
            x = x2
        return False
    lo, hi = 0.0, 1.0
    while hi - lo > tol:
        mid = (lo + hi) / 2
        lo, hi = (mid, hi) if converges(mid) else (lo, mid)
    return lo


def de_bec_curve(wc, wr, eps, steps):
    x, out = eps, [eps]
    for _ in range(steps):
        x = eps * (1 - (1 - x) ** (wr - 1)) ** (wc - 1)
        out.append(x)
    return out


# ----------------------------------------------------------------------------------------------- polar codes

def polar_bhattacharyya(n, z):
    """Bhattacharyya parameters of the 2^n synthetic channels of a BEC(z) (exact), in decoding order."""
    return _polar_z(n, z)


def _polar_z(n, z):
    if n == 0:
        return [z]
    return _polar_z(n - 1, 2 * z - z * z) + _polar_z(n - 1, z * z)


def polar_encode(u):
    N = len(u)
    if N == 0 or N & (N - 1):
        raise ValueError("polar block length must be a positive power of two")
    if N == 1:
        return list(u)
    h = N // 2
    a = polar_encode([u[i] ^ u[h + i] for i in range(h)])
    b = polar_encode(u[h:])
    return a + b


def _f(a, b):
    return np.sign(a) * np.sign(b) * np.minimum(np.abs(a), np.abs(b))


def polar_sc(llr, frozen):
    """Successive-cancellation decoding (min-sum). llr: numpy array of channel LLRs; frozen: boolean list."""
    N = len(llr)
    if N == 0 or N & (N - 1) or len(frozen) != N:
        raise ValueError("matching LLR/frozen arrays of power-of-two length required")
    if N == 1:
        u = 0 if frozen[0] else int(llr[0] < 0)
        return [u], [u]
    h = N // 2
    a, b = llr[:h], llr[h:]
    u1, s = polar_sc(_f(a, b), frozen[:h])
    s_arr = np.array(s)
    g = b + (1 - 2 * s_arr) * a
    u2, t = polar_sc(g, frozen[h:])
    return u1 + u2, [si ^ ti for si, ti in zip(s, t)] + t


def polar_frozen(n, K, z):
    zs = _polar_z(n, z)
    order = sorted(range(1 << n), key=lambda i: zs[i])
    info = set(order[:K])
    return [i not in info for i in range(1 << n)]


def polar_block_error(n, K, p, trials, rng, design=None):
    N = 1 << n
    z0 = design if design is not None else 2 * math.sqrt(p * (1 - p))
    frozen = polar_frozen(n, K, z0)
    L0 = math.log((1 - p) / p)
    bad = 0
    for _ in range(trials):
        u = [0 if frozen[i] else rng.randrange(2) for i in range(N)]
        x = polar_encode(u)
        y = [xi ^ (rng.random() < p) for xi in x]
        llr = np.array([L0 if yi == 0 else -L0 for yi in y])
        uh, _ = polar_sc(llr, frozen)
        bad += uh != u
    return bad / trials


# ----------------------------------------------------------------------------------------------- fountain codes

def robust_soliton(k, c=0.1, delta=0.5):
    R = c * math.log(k / delta) * math.sqrt(k)
    rho = [0.0, 1.0 / k] + [1.0 / (d * (d - 1)) for d in range(2, k + 1)]
    tau = [0.0] * (k + 1)
    pivot = int(round(k / R))
    for d in range(1, min(pivot, k + 1)):
        tau[d] = R / (d * k)
    if 1 <= pivot <= k:
        tau[pivot] = R * math.log(R / delta) / k
    z = sum(rho) + sum(tau)
    return [(rho[d] + tau[d]) / z for d in range(k + 1)]


def lt_symbols_needed(k, rng, dist=None):
    """Received encoded symbols until the peeling decoder recovers all k source symbols."""
    dist = dist or robust_soliton(k)
    cum = list(itertools.accumulate(dist))
    known = [False] * k
    n_known = 0
    pending = []                 # sets of unknown neighbours
    by_src = [[] for _ in range(k)]
    received = 0
    while n_known < k:
        received += 1
        r = rng.random() * cum[-1]
        d = next(i for i, c in enumerate(cum) if c >= r)
        nb = set(rng.sample(range(k), max(1, d)))
        nb = {s for s in nb if not known[s]}
        idx = len(pending)
        pending.append(nb)
        for s in nb:
            by_src[s].append(idx)
        ripple = [idx] if len(nb) == 1 else []
        while ripple:
            j = ripple.pop()
            if len(pending[j]) != 1:
                continue
            s = next(iter(pending[j]))
            if known[s]:
                continue
            known[s] = True
            n_known += 1
            for j2 in by_src[s]:
                if s in pending[j2]:
                    pending[j2].discard(s)
                    if len(pending[j2]) == 1:
                        ripple.append(j2)
    return received


# ----------------------------------------------------------------------------------------------- RAID-6, local decoding

def raid6_parity(disks):
    """P = XOR of the data disks, Q = sum g^i D_i over GF(256), byte by byte."""
    P = [0] * len(disks[0])
    Q = [0] * len(disks[0])
    for i, d in enumerate(disks):
        g = gf_pow(2, i)
        for j, byte in enumerate(d):
            P[j] ^= byte
            Q[j] ^= gf_mul(g, byte)
    return P, Q


def raid6_recover_two(disks, x, y, P, Q):
    """Rebuild data disks x < y from the others and P, Q (H. Peter Anvin's equations)."""
    n = len(disks[0])
    Pxy, Qxy = list(P), list(Q)
    for i, d in enumerate(disks):
        if i in (x, y):
            continue
        g = gf_pow(2, i)
        for j in range(n):
            Pxy[j] ^= d[j]
            Qxy[j] ^= gf_mul(g, d[j])
    gx, gy = gf_pow(2, x), gf_pow(2, y)
    denom = gx ^ gy
    Dx, Dy = [0] * n, [0] * n
    for j in range(n):
        # Dx + Dy = Pxy;  gx Dx + gy Dy = Qxy
        Dx[j] = gf_div(Qxy[j] ^ gf_mul(gy, Pxy[j]), denom)
        Dy[j] = Pxy[j] ^ Dx[j]
    return Dx, Dy


def hadamard_encode(x, k):
    """All 2^k inner products <x, a> mod 2."""
    return [weight(x & a) & 1 for a in range(1 << k)]


def hadamard_local_decode(word, k, i, rng, reps=1):
    """Recover bit i of x by majority over reps trials of word[a] xor word[a xor e_i], a random: two queries each."""
    votes = sum(word[a] ^ word[a ^ (1 << i)] for a in (rng.randrange(1 << k) for _ in range(reps)))
    return int(2 * votes > reps)


def rng_bits(n, rng: random.Random):
    return [rng.randrange(2) for _ in range(n)]


# ----------------------------------------------------------------------------------------------- traces for the scenes

def ldpc_bp_trace(edges, m, n, p, rng, iters=30):
    """One block on BSC(p): the number of wrong hard decisions before decoding and after each BP round."""
    ch = np.array([c for c, _ in edges])
    va = np.array([v for _, v in edges])
    L0 = math.log((1 - p) / p)
    nrng = np.random.default_rng(rng.randrange(1 << 30))
    order = np.argsort(ch, kind="stable")
    starts = np.searchsorted(ch[order], np.arange(m))
    flips = nrng.random(n) < p
    llr = np.where(flips, -L0, L0)
    trace = [int(flips.sum())]
    unsat = []
    v2c = llr[va].copy()
    hard = flips.copy()
    for _ in range(iters):
        t = np.tanh(np.clip(v2c, -30, 30) / 2)
        t = np.where(np.abs(t) < 1e-12, 1e-12, t)
        logabs = np.log(np.abs(t))
        neg = (t < 0).astype(np.int64)
        sum_log = np.add.reduceat(logabs[order], starts)
        sum_neg = np.add.reduceat(neg[order], starts)
        prod = np.exp(sum_log[ch] - logabs) * np.where((sum_neg[ch] - neg) % 2 == 1, -1.0, 1.0)
        c2v = 2 * np.arctanh(np.clip(prod, -0.999999, 0.999999))
        total = llr + np.bincount(va, weights=c2v, minlength=n)
        hard = total < 0
        trace.append(int(hard.sum()))
        par = np.bincount(ch, weights=hard[va].astype(float), minlength=m) % 2
        unsat.append(int(par.sum()))
        if not par.any():
            break
        v2c = total[va] - c2v
    return trace, unsat


def irreducible_polys(deg):
    """All irreducible polynomials of the given degree over GF(2) (as ints, leading bit set), and the primitive ones."""
    def mulmod(a, b, mod):
        r = 0
        while b:
            if b & 1:
                r ^= a
            b >>= 1
            a <<= 1
            if a >> deg & 1:
                a ^= mod
        return r

    def divides(f, g):
        while g.bit_length() >= f.bit_length():
            g ^= f << (g.bit_length() - f.bit_length())
        return g == 0
    small = [f for d in range(1, deg // 2 + 1) for f in range(1 << d, 1 << (d + 1))]
    irr = [f for f in range(1 << deg, 1 << (deg + 1)) if f & 1 and not any(divides(s, f) for s in small
                                                                             if _irreducible_small(s))]
    order = (1 << deg) - 1
    prim = []
    for f in irr:
        x, k = 1, 0
        while True:
            x = mulmod(x, 2, f)
            k += 1
            if x == 1:
                break
        if k == order:
            prim.append(f)
    return irr, prim


def _irreducible_small(f):
    d = f.bit_length() - 1
    if d <= 1:
        return d == 1
    for g in range(2, 1 << (d // 2 + 1)):
        h = f
        while h.bit_length() >= g.bit_length() and h:
            h ^= g << (h.bit_length() - g.bit_length())
        if h == 0:
            return False
    return True


def rs_trace(cw, nsym):
    """The steps of rs_decode for display: syndromes, the error locator, the positions and values found."""
    synd = [0] + rs_syndromes(cw, nsym)
    fsynd = _forney_syndromes(synd, [], len(cw))
    loc = _berlekamp_massey(fsynd, nsym)
    pos = _chien(loc[::-1], len(cw))
    fixed = _correct_errata(list(cw), synd, pos)
    return {"syndromes": synd[1:], "locator": loc, "positions": sorted(pos),
            "values": {p: cw[p] ^ fixed[p] for p in pos}, "fixed": fixed}
