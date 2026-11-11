"""Precompute everything numerical in Part 28 of *Computer Science, Built* ("Error-Correcting Codes").

    python -m videos.cs.cs28.compute              # everything missing
    python -m videos.cs.cs28.compute --force qr

Results are cached in ``.cache/cs28/<name>.json``; scenes call ``load(name)``.  The instrument is
``explainer/cs/algo/codes.py`` (tested in tests/test_cs28_codes.py).

Items:
    repetition  bit error of the n-fold repetition code on BSC(0.1), exact and simulated
    hamming     Hamming(7,4): a worked syndrome, and bit/block error curves against repetition and no coding
    bounds      the rate--distance bounds sampled, with the codes of this part as points
    golay       the [23,12,7] Golay code enumerated: weight distribution, perfection
    field       GF(256): the powers of alpha, a multiplication by tables, and the field polynomial
    rs          the evaluation view: a quadratic through nine points, three corrupted, Berlekamp--Welch's answer
    qr          the part's QR code, three scratches, and what errors-only and erasure decoding make of each
    crc         CRC-32 against zlib; CRC-8 on bursts and random errors
    shannon     random linear codes of rate 1/2 under ML decoding, block error by length, below and above capacity
    viterbi     the (7,5) convolutional code: bit error after Viterbi against the raw channel
    ldpc        a (3,6) LDPC code of length 4,800 under belief propagation: the waterfall; BEC density evolution
    polar       polarization of BEC(1/2) by level; successive cancellation at rate 1/2
    storage     RAID-6 rebuilding two lost disks; LT fountain overheads
    local       the Hadamard code's two-query local decoder against the corrupted fraction
    picture     a 1-bit picture sent through BSC(0.05): raw, three-fold repetition, Hamming(7,4)
    gfpoly      the irreducible and primitive polynomials of degree 8 over GF(2)
    qrtrace     the QR decoder's steps on the scratch: syndromes, locator, positions, values
    bptrace     belief propagation on one block: wrong bits and unsatisfied checks per round
"""

from __future__ import annotations

import math
import random
import statistics
import time

from explainer.ai.cache import Cache
from explainer.cs.algo import codes as C

CACHE = Cache("cs28")
DECODER_VERSION = 2


def load(name):
    out = CACHE.load(name)
    # These experiments used an oracle stopping rule before version 2. Refresh
    # existing local caches once so scenes cannot silently reuse those results.
    if name in ("ldpc", "bptrace") and out.get("decoder_version") != DECODER_VERSION:
        out = ITEMS[name]()
        CACHE.save(name, out)
    return out

QR_TEXT = "CS, Built: Part 28"


def compute_repetition() -> dict:
    p, rng = 0.1, random.Random(1)
    rows = []
    for n in (1, 3, 5, 9, 15, 25):
        trials = 20000
        bad = sum(sum(rng.random() < p for _ in range(n)) > n // 2 for _ in range(trials))
        rows.append({"n": n, "rate": 1 / n, "exact": C.repetition_error(n, p), "sim": bad / trials})
    return {"p": p, "rows": rows}


def compute_hamming() -> dict:
    data = [1, 0, 1, 1]
    cw = C.hamming74_encode(data)
    flipped = list(cw)
    flipped[4] ^= 1                                     # position 5
    syn = C.hamming74_syndrome(flipped)
    curves = []
    for k in range(1, 41):
        p = 10 ** (-3 + 2.5 * k / 40)                    # 1e-3 .. ~0.3
        none = p
        rep3 = C.repetition_error(3, p)
        block = 1 - (1 - p) ** 7 - 7 * p * (1 - p) ** 6
        # bit error after decoding, exact: sum over error patterns of weight w of the data-bit errors they cause
        bit = _hamming_bit_error(p)
        curves.append({"p": p, "none": none, "rep3": rep3, "ham_block": block, "ham_bit": bit})
    rng = random.Random(2)
    sim = []
    for p in (0.01, 0.05, 0.1):
        errs = bits = 0
        for _ in range(20000):
            d = [rng.randrange(2) for _ in range(4)]
            r = C.bsc(C.hamming74_encode(d), p, rng)
            dec, _ = C.hamming74_decode(r)
            errs += sum(a != b for a, b in zip(d, dec))
            bits += 4
        sim.append({"p": p, "sim": errs / bits, "exact": _hamming_bit_error(p)})
    return {"data": data, "codeword": cw, "flipped": flipped, "syndrome": syn, "curves": curves, "sim": sim}


def _hamming_bit_error(p):
    tot = 0.0
    for e in range(128):
        w = C.weight(e)
        prob = p ** w * (1 - p) ** (7 - w)
        c = [(e >> i) & 1 for i in range(7)]
        dec, _ = C.hamming74_decode(c)                   # decoding the error pattern alone (linearity)
        tot += prob * sum(dec) / 4
    return tot


def compute_bounds() -> dict:
    ds = [i / 200 for i in range(0, 101)]
    curve = {name: [f(d) for d in ds] for name, f in (("singleton", C.singleton_bound), ("hamming", C.hamming_bound),
                                                      ("plotkin", C.plotkin_bound), ("mrrw", C.mrrw_bound),
                                                      ("gv", C.gv_bound))}
    points = [{"name": "Hamming(7,4)", "R": 4 / 7, "delta": 3 / 7}, {"name": "Golay(23,12)", "R": 12 / 23,
              "delta": 7 / 23}, {"name": "repetition(3)", "R": 1 / 3, "delta": 1.0},
              {"name": "Hamming(15,11)", "R": 11 / 15, "delta": 3 / 15}, {"name": "Hamming(31,26)", "R": 26 / 31,
                                                                            "delta": 3 / 31}]
    return {"delta": ds, "curves": curve, "points": points}


def compute_golay() -> dict:
    t = time.perf_counter()
    w = C.codewords(C.golay23_generators())
    dist = C.weight_distribution(w, 23)
    dt = time.perf_counter() - t
    ball = sum(math.comb(23, i) for i in range(4))
    return {"count": len(w), "dmin": C.min_distance(w), "dist": {i: a for i, a in enumerate(dist) if a},
            "ball": ball, "product": len(w) * ball, "space": 2 ** 23, "seconds": dt}


def compute_field() -> dict:
    powers = [C.gf_pow(2, i) for i in range(255)]
    a, b = 0x57, 0x83
    return {"powers": powers[:24], "order": len(set(powers)), "a": a, "b": b, "log_a": C.GF_LOG[a],
            "log_b": C.GF_LOG[b], "product": C.gf_mul(a, b), "check": C.gf_mul_slow(a, b),
            "alpha8": C.gf_pow(2, 8)}


def compute_rs() -> dict:
    p, msg = 1009, [5, 3, 2]                  # f(x) = 2x^2 + 3x + 5; values stay below p, so mod p = integers
    xs = list(range(1, 10))
    y = C.rs_eval_encode(msg, xs, p)
    bad = {2: 40, 5: -60, 8: 55}               # positions (1-based x) and the corruption
    yb = [(v + bad.get(x, 0)) % p for x, v in zip(xs, y)]
    dec, where = C.berlekamp_welch(list(zip(xs, yb)), 3, 3, p)
    erased = [1, 4, 6, 7, 9, 3]                # any three survivors suffice
    keep = [(x, v) for x, v in zip(xs, y) if x not in erased]
    lag = C.lagrange_coeffs(keep, p)
    return {"p": p, "msg": msg, "xs": xs, "y": y, "y_bad": yb, "bad": sorted(bad), "decoded": dec, "found": where,
            "erased": erased, "lagrange": lag}


def _scratch(M, x0, y0, x1, y1):
    D = [row[:] for row in M]
    hit = set()
    for y in range(y0, y1 + 1):
        for x in range(x0, x1 + 1):
            D[y][x] = False
            hit.add((x, y))
    return D, hit


def compute_qr() -> dict:
    M, info = C.qr_encode(QR_TEXT, "Q")
    pos = info["positions"]
    owner = {xy: k // 8 for k, xy in enumerate(pos[:44 * 8])}
    scratches = [("scratch", (9, 9, 15, 16)), ("blot", (9, 9, 15, 24)), ("hole", (9, 0, 16, 24))]
    rows = []
    for name, (x0, y0, x1, y1) in scratches:
        D, hit = _scratch(M, x0, y0, x1, y1)
        touched = sorted({owner[xy] for xy in hit if xy in owner})
        wrong = [k for k in range(44) if _read_cw(D, info, k) != info["codewords"][k]]
        res = {}
        for mode, er in (("errors", None), ("erasures", hit)):
            try:
                out = C.qr_decode(D, erasures=er)
                res[mode] = {"ok": out["text"] == QR_TEXT, "text": out["text"]}
            except (ValueError, AssertionError, UnicodeDecodeError) as e:
                res[mode] = {"ok": False, "text": None, "why": str(e)[:60]}
        rows.append({"name": name, "rect": [x0, y0, x1, y1], "modules": len(hit), "touched": touched,
                     "wrong": wrong, "result": res})
    return {"text": QR_TEXT, "ecl": "Q", "mask": info["mask"], "matrix": [[int(v) for v in r] for r in M],
            "data": info["data"], "codewords": info["codewords"], "owner": [[owner.get((x, y), -1) for x in range(25)]
                                                                            for y in range(25)],
            "func": [[int(v) for v in r] for r in info["func"]], "scratches": rows}


def _read_cw(D, info, k):
    f = C._mask_fn(info["mask"])
    bits = [int(D[y][x] ^ f(x, y)) for x, y in info["positions"][8 * k:8 * k + 8]]
    return int("".join(map(str, bits)), 2)


def compute_crc() -> dict:
    import zlib
    samples = [b"", b"Hamming", b"CS, Built: Part 28", b"The quick brown fox jumps over the lazy dog"]
    rows = [{"text": s.decode(), "ours": C.crc32(s), "zlib": zlib.crc32(s)} for s in samples]
    rng = random.Random(3)
    msg = bytes(rng.randrange(256) for _ in range(64))
    good = C.crc8(msg)
    bits = 64 * 8

    def flip(data, positions):
        b = bytearray(data)
        for q in positions:
            b[q // 8] ^= 1 << (7 - q % 8)
        return bytes(b)
    trials = 30000
    out = []
    for L in (1, 2, 4, 8, 9, 12, 16):
        miss = 0
        for _ in range(trials):
            start = rng.randrange(bits - L + 1)
            pattern = [start] + [start + i for i in range(1, L - 1) if rng.random() < 0.5] + ([start + L - 1]
                                                                                              if L > 1 else [])
            if C.crc8(flip(msg, pattern)) == good:
                miss += 1
        out.append({"burst": L, "undetected": miss / trials})
    miss = 0
    for _ in range(trials):
        pattern = [q for q in range(bits) if rng.random() < 0.5]
        if pattern and C.crc8(flip(msg, pattern)) == good:
            miss += 1
    return {"crc32": rows, "bursts": out, "random_undetected": miss / trials, "trials": trials, "bound": 1 / 256}


def compute_shannon() -> dict:
    rng = random.Random(4)
    ps = [0.05, 0.11, 0.15]
    rows = []
    for n in (8, 12, 16, 20, 24, 28):
        row = {"n": n}
        codes = [C.random_systematic(n, n // 2, rng) for _ in range(6)]
        for p in ps:
            rates = [C.block_error_rate(n, n // 2, p, 1500, rng, code=c) for c in codes]
            row[str(p)] = statistics.median(rates)
        rows.append(row)
    return {"ps": ps, "capacity": {str(p): C.capacity_bsc(p) for p in ps}, "rows": rows,
            "cap_curve": [[i / 100, C.capacity_bsc(i / 100)] for i in range(0, 51)]}


def compute_viterbi() -> dict:
    rng = random.Random(5)
    rows = []
    for p in (0.005, 0.01, 0.02, 0.03, 0.05, 0.08, 0.1):
        bits = [rng.randrange(2) for _ in range(20000)]
        tx = C.conv_encode(bits)
        rx = C.bsc(tx, p, rng)
        dec = C.viterbi(rx)
        rows.append({"p": p, "coded": sum(a != b for a, b in zip(dec, bits)) / len(bits), "raw": p})
    sample = [1, 0, 1, 1, 0, 0]
    return {"rows": rows, "sample": sample, "sample_out": C.conv_encode(sample)}


def compute_ldpc() -> dict:
    rng = random.Random(6)
    n = 4800
    edges, m = C.gallager_ldpc(n, 3, 6, rng)
    rows = []
    for p in (0.04, 0.05, 0.06, 0.065, 0.07, 0.0725, 0.075, 0.0775, 0.08, 0.085, 0.09, 0.1):
        ber, fer = C.ldpc_bp_bsc(edges, m, n, p, 100, rng)
        rows.append({"p": p, "ber": ber, "fer": fer})
    eps = C.de_bec_threshold(3, 6)
    return {"n": n, "m": m, "rows": rows, "decoder_version": DECODER_VERSION,
            "has_4cycle": C.has_4cycle(edges), "bec_threshold": eps, "bec_shannon": 0.5, "bsc_shannon": 0.11,
            "de_below": C.de_bec_curve(3, 6, 0.42, 60), "de_above": C.de_bec_curve(3, 6, 0.44, 60)}


def compute_polar() -> dict:
    levels = []
    for n in range(0, 11):
        z = C.polar_bhattacharyya(n, 0.5)
        levels.append({"n": n, "good": sum(v < 1e-3 for v in z) / len(z), "bad": sum(v > 1 - 1e-3 for v in z) / len(z),
                       "z": sorted(z) if n <= 6 else None})
    fan = [C.polar_bhattacharyya(n, 0.5) for n in range(0, 7)]
    rng = random.Random(7)
    rows = []
    for p in (0.02, 0.04, 0.06, 0.08, 0.11):
        row = {"p": p}
        for n in (8, 10):
            row[str(1 << n)] = C.polar_block_error(n, 1 << (n - 1), p, 200 if n == 8 else 120, rng)
        rows.append(row)
    return {"levels": levels, "fan": fan, "rows": rows}


def compute_storage() -> dict:
    rng = random.Random(8)
    disks = [[rng.randrange(256) for _ in range(12)] for _ in range(6)]
    P, Q = C.raid6_parity(disks)
    Dx, Dy = C.raid6_recover_two(disks, 1, 4, P, Q)
    lt = {}
    for k in (100, 1000, 10000):
        trials = 40 if k < 10000 else 6
        need = [C.lt_symbols_needed(k, random.Random(1000 * k + s)) for s in range(trials)]
        lt[str(k)] = {"median": statistics.median(need), "max": max(need), "min": min(need),
                      "overhead": statistics.median(need) / k - 1}
    return {"disks": disks, "P": P, "Q": Q, "lost": [1, 4], "recovered": Dx == disks[1] and Dy == disks[4], "lt": lt}


def compute_local() -> dict:
    rng = random.Random(9)
    k = 10
    x = 0b1011001110
    rows = []
    for delta in (0.02, 0.05, 0.1, 0.15, 0.2, 0.25):
        w = C.hadamard_encode(x, k)
        for b in rng.sample(range(1 << k), int(delta * (1 << k))):
            w[b] ^= 1
        one = sum(C.hadamard_local_decode(w, k, i, rng, 1) == (x >> i) & 1 for i in range(k) for _ in range(300))
        maj = sum(C.hadamard_local_decode(w, k, i, rng, 15) == (x >> i) & 1 for i in range(k) for _ in range(300))
        rows.append({"delta": delta, "one": one / (k * 300), "maj15": maj / (k * 300), "bound": 1 - 2 * delta})
    return {"k": k, "n": 1 << k, "rows": rows}


def compute_picture() -> dict:
    from PIL import Image, ImageDraw, ImageFont
    W, Hh = 96, 40
    img = Image.new("1", (W, Hh), 0)
    dr = ImageDraw.Draw(img)
    try:
        font = ImageFont.truetype("DejaVuSans-Bold.ttf", 30)
    except OSError:
        font = ImageFont.load_default()
    dr.text((4, 2), "CODE", fill=1, font=font)
    bits = [int(img.getpixel((x, y)) > 0) for y in range(Hh) for x in range(W)]
    rng = random.Random(10)
    p = 0.05
    raw = C.bsc(bits, p, rng)
    rep = []
    for b in bits:
        r = C.bsc([b] * 3, p, rng)
        rep.append(int(sum(r) >= 2))
    ham = []
    for i in range(0, len(bits), 4):
        d = bits[i:i + 4]
        r = C.bsc(C.hamming74_encode(d), p, rng)
        ham += C.hamming74_decode(r)[0]

    def errs(x):
        return sum(a != b for a, b in zip(x, bits))
    return {"W": W, "H": Hh, "p": p, "orig": bits, "raw": raw, "rep": rep, "ham": ham,
            "errors": {"raw": errs(raw), "rep": errs(rep), "ham": errs(ham)}, "pixels": len(bits),
            "sent": {"raw": len(bits), "rep": 3 * len(bits), "ham": 7 * len(bits) // 4}}


def compute_gfpoly() -> dict:
    irr, prim = C.irreducible_polys(8)
    return {"irreducible": len(irr), "primitive": len(prim), "first": [f"{f:#x}" for f in irr[:8]],
            "qr": "0x11d", "qr_primitive": 0x11D in prim, "aes": "0x11b", "aes_irreducible": 0x11B in irr,
            "aes_primitive": 0x11B in prim, "total_monic": 2 ** 8}


def compute_qrtrace() -> dict:
    q = load("qr")
    M = [[bool(v) for v in row] for row in q["matrix"]]
    info = {"mask": q["mask"], "positions": None}
    _, full = C.qr_encode(QR_TEXT, "Q", mask=q["mask"])
    s = next(x for x in q["scratches"] if x["name"] == "scratch")
    D, _ = _scratch(M, *s["rect"])
    info["positions"] = full["positions"]
    read = [_read_cw(D, info, k) for k in range(44)]
    tr = C.rs_trace(read, 22)
    return {"read": read, "true": q["codewords"], "syndromes": tr["syndromes"], "locator": tr["locator"],
            "found": tr["positions"], "wrong": [k for k in range(44) if read[k] != q["codewords"][k]],
            "values": {str(k): v for k, v in tr["values"].items()}, "ok": tr["fixed"] == q["codewords"]}


def compute_bptrace() -> dict:
    rng = random.Random(6)
    edges, m = C.gallager_ldpc(4800, 3, 6, rng)
    good = C.ldpc_bp_trace(edges, m, 4800, 0.07, random.Random(3))
    bad = C.ldpc_bp_trace(edges, m, 4800, 0.09, random.Random(3))
    return {"n": 4800, "m": m, "decoder_version": DECODER_VERSION,
            "p_good": 0.07, "good": good[0], "good_unsat": good[1], "p_bad": 0.09,
            "bad": bad[0], "bad_unsat": bad[1]}


ITEMS = {k[8:]: v for k, v in globals().items() if k.startswith("compute_")}


if __name__ == "__main__":
    CACHE.main(ITEMS, __doc__)
