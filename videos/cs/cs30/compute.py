"""Precompute everything numerical in Part 30 of *Computer Science, Built* ("Public Keys").

    python -m videos.cs.cs30.compute              # everything missing
    python -m videos.cs.cs30.compute --force rsa

Results are cached in ``.cache/cs30/<name>.json``; scenes call ``load(name)``.  The instrument is
``explainer/cs/algo/pubkey.py`` (tested in tests/test_cs30_pubkey.py).

Items:
    toydh       Diffie-Hellman with p = 23, g = 5, and the same with a 2048-bit prime
    puzzles     Merkle's puzzles at n = 100, 1,000 and 10,000: Bob's tries against Eve's
    euclid      extended Euclid on (240, 46); 17^-1 mod 3120; square-and-multiply traces
    groups      powers and orders in Z_23^*; g^x mod 1019 as a scatter; Lagrange's divisors
    mitm        Mallory between Alice and Bob
    rsa         2048-bit key generation (candidates tried, seconds), CRT against plain decryption, malleability, OAEP
    oracle      Bleichenbacher's attack on a 256-bit and a 384-bit key: queries and the shrinking interval
    factoring   Pollard's rho and our quadratic sieve on semiprimes of 10 to 34 digits; a QS relation
    rhowalk     one rho walk mod the hidden factor, with its tail and cycle
    dlog        baby-step giant-step timings; Pohlig-Hellman on a smooth p - 1 against a safe prime; index calculus
    curves      the F_97 point cloud, a generator's multiples, P-256 and X25519 vectors and timings
    ecdsa       RFC 6979's vector; two signatures with one nonce, and the key recovered
    pki         a three-certificate chain verified; a tampered leaf rejected
    tls         the TLS 1.3-shaped handshake between two of our machines
    shor        classical period finding for N = 15, 21, 35, and the sizes of RSA and ECC keys
    lattices    Gauss reduction steps; LLL breaking a 20-item knapsack; LWE decryption noise; NTT against schoolbook;
                K-PKE round trips
    beyond      Lamport key and signature sizes; Schnorr; Shamir shares over GF(p)
"""

from __future__ import annotations

import math
import random
import time

from explainer.ai.cache import Cache
from explainer.cs.algo import pubkey as P

CACHE = Cache("cs30")


def load(name):
    out = CACHE.load(name)
    if name == "puzzles" and out.get("version") != 2:
        out = compute_puzzles()
        CACHE.save(name, out)
    return out

# RFC 3526's 2048-bit MODP group (group 14)
MODP2048 = int(
    "FFFFFFFFFFFFFFFFC90FDAA22168C234C4C6628B80DC1CD129024E088A67CC74020BBEA63B139B22514A08798E3404DDEF9519B3CD3A431B302B"
    "0A6DF25F14374FE1356D6D51C245E485B576625E7EC6F44C42E9A637ED6B0BFF5CB6F406B7EDEE386BFB5A899FA5AE9F24117C4B1FE649286651"
    "ECE45B3DC2007CB8A163BF0598DA48361C55D39A69163FA8FD24CF5F83655D23DCA3AD961C62F356208552BB9ED529077096966D670C354E4ABC"
    "9804F1746C08CA18217C32905E462E36CE3BE39E772C180E86039B2783A2EC07A28FB5C55DF06F4C52C9DE2BCBF6955817183995497CEA956AE"
    "515D2261898FA051015728E5A8AACAA68FFFFFFFFFFFFFFFF", 16)


def compute_toydh() -> dict:
    p, g, a, b = 23, 5, 6, 15
    A, B = pow(g, a, p), pow(g, b, p)
    rng = random.Random(1)
    x, X = P.dh_keypair(MODP2048, 2, rng)
    y, Y = P.dh_keypair(MODP2048, 2, rng)
    t = time.perf_counter()
    s1 = pow(Y, x, MODP2048)
    dt = time.perf_counter() - t
    return {"p": p, "g": g, "a": a, "b": b, "A": A, "B": B, "s_alice": pow(B, a, p), "s_bob": pow(A, b, p),
            "big_equal": s1 == pow(X, y, MODP2048), "big_bits": MODP2048.bit_length(), "big_ms": dt * 1000,
            "big_A": hex(X)[:18], "big_B": hex(Y)[:18]}


def compute_puzzles() -> dict:
    rng = random.Random(2)
    rows = []
    for n in (100, 1000, 10000):
        r = P.merkle_puzzles(n, rng)
        rows.append({"n": n, "bob": r["bob_tries"], "eve": r["eve_expected"], "agreed": r["agreed"]})
    return {"rows": rows, "version": 2}


def compute_euclid() -> dict:
    return {"trace": P.egcd_trace(240, 46), "g": P.egcd(240, 46), "inv": P.inv_mod(17, 3120),
            "pow": P.pow_trace(3, 218, 1000), "pow_value": pow(3, 218, 1000),
            "big_mults": 2 * 2048}


def compute_groups() -> dict:
    p, g = 23, 5
    powers = [pow(g, k, p) for k in range(p - 1)]
    orders = {a: P.mult_order(a, p) for a in range(1, p)}
    q = 1019
    gq = P.find_generator(q)
    scatter = [pow(gq, x, q) for x in range(q - 1)]
    return {"p": p, "g": g, "powers": powers, "orders": orders, "q": q, "gq": gq, "scatter": scatter,
            "divisors": [d for d in range(1, p) if (p - 1) % d == 0]}


def compute_mitm() -> dict:
    r = P.dh_mitm(23, 5, random.Random(3))
    return r


def compute_rsa() -> dict:
    rng = random.Random(4)
    times, cands = [], []
    for _ in range(3):
        t = time.perf_counter()
        tried = 0
        while True:
            n = rng.getrandbits(1024) | (1 << 1023) | 1
            tried += 1
            if P.is_probable_prime(n, rng):
                break
        cands.append(tried)
        times.append(time.perf_counter() - t)
    t = time.perf_counter()
    key = P.rsa_keygen(2048, rng)
    keygen = time.perf_counter() - t
    m = P.b2i(b"PAY BOB $100")
    c = P.rsa_enc(m, key)
    t = time.perf_counter()
    for _ in range(20):
        P.rsa_dec(c, key, use_crt=False)
    plain = (time.perf_counter() - t) / 20
    t = time.perf_counter()
    for _ in range(20):
        P.rsa_dec(c, key)
    crt = (time.perf_counter() - t) / 20
    c2 = c * pow(2, key["e"], key["n"]) % key["n"]
    doubled = P.rsa_dec(c2, key)
    oa1 = P.oaep_encrypt(b"PAY BOB $100", key, rng)
    oa2 = P.oaep_encrypt(b"PAY BOB $100", key, rng)
    small = {"p": 61, "q": 53, "n": 3233, "phi": 3120, "e": 17, "d": P.inv_mod(17, 3120), "m": 65,
             "c": pow(65, 17, 3233)}
    return {"cands": cands, "prime_ms": [t_ * 1000 for t_ in times], "expected_cands": 1024 * math.log(2) / 2,
            "keygen_s": keygen, "nbits": key["n"].bit_length(), "n_hex": hex(key["n"])[:34], "e": key["e"],
            "plain_ms": plain * 1000, "crt_ms": crt * 1000, "m": m, "doubled": doubled, "doubled_ok": doubled == 2 * m,
            "oaep_differ": oa1 != oa2, "oaep_back": P.oaep_decrypt(oa1, key).decode(), "small": small}


def compute_oracle() -> dict:
    out = []
    for bits in (256, 384):
        rng = random.Random(5 + bits)
        key = P.rsa_keygen(bits, rng)
        k = P.klen(key)
        em = P.pkcs1_v15_pad(b"PIN 4921", k, rng)
        c = P.rsa_enc(P.b2i(em), key)
        tr = []
        t = time.perf_counter()
        m, q = P.bleichenbacher(c, key, lambda cc: P.pkcs1_v15_conforming(P.i2b(P.rsa_dec(cc, key), k)), trace=tr)
        dt = time.perf_counter() - t
        out.append({"bits": bits, "ok": P.i2b(m, k) == em, "queries": q, "seconds": dt,
                    "trace": [(qq, math.log2(w)) for qq, w in tr], "recovered": P.i2b(m, k)[-8:].decode()})
    return {"runs": out}


def compute_factoring() -> dict:
    rng = random.Random(6)
    rows = []
    for digits in (10, 14, 18, 22, 26, 30, 34):
        bits = int(digits * 3.3219 / 2)
        a, b = P.random_prime(bits, rng), P.random_prime(bits, rng)
        n = a * b
        t = time.perf_counter()
        f, steps = P.pollard_rho(n, rng)
        rho = time.perf_counter() - t
        t = time.perf_counter()
        g, st = P.quadratic_sieve(n)
        qs = time.perf_counter() - t
        rows.append({"digits": len(str(n)), "rho_s": rho, "rho_steps": steps, "qs_s": qs, "qs_ok": g in (a, b),
                     "rho_ok": f in (a, b), "base": st.get("base")})
    pp, qq = 1009, 1000003
    walk = P.rho_walk(pp * qq, pp, c=1, x0=2, steps=80)
    seen, tail, cyc = {}, None, None
    for i, v in enumerate(walk):
        if v in seen:
            tail, cyc = seen[v], i - seen[v]
            break
        seen[v] = i
    n20 = P.random_prime(33, rng) * P.random_prime(33, rng)
    g, st = P.quadratic_sieve(n20)
    x, ex = st["example"]
    return {"rows": rows, "walk": walk[:tail + cyc + 1], "tail": tail, "cycle": cyc, "p": pp, "n_walk": pp * qq,
            "qs_n": n20, "qs_factor": g, "qs_stats": {k: v for k, v in st.items() if k != "example"},
            "qs_example": {"x": x, "value": x * x - n20, "factors": ex}}


def compute_rhowalk() -> dict:
    """x -> x^2 + 1 mod n = 1009 * 1000003, from 4, watched mod the hidden factor 1009: a tail of 7 and a cycle of 14."""
    p, q = 1009, 1000003
    n = p * q
    walk = P.rho_walk(n, p, c=1, x0=4, steps=40)
    seen = {}
    for i, v in enumerate(walk):
        if v in seen:
            tail, cyc = seen[v], i - seen[v]
            break
        seen[v] = i
    full, x = [], 4
    for _ in range(tail + cyc + 1):
        full.append(x)
        x = (x * x + 1) % n
    import math as _m
    g = _m.gcd(abs(full[tail + cyc] - full[tail]), n)
    return {"p": p, "q": q, "n": n, "walk": walk[:tail + cyc + 1], "tail": tail, "cycle": cyc,
            "x_full": [str(v) for v in full], "gcd": g}


def compute_dlog() -> dict:
    rng = random.Random(7)
    rows = []
    for bits in (24, 28, 32, 36, 40):
        p = P.random_prime(bits, rng)
        g = P.find_generator(p)
        x = rng.randrange(p - 1)
        t = time.perf_counter()
        r, m = P.bsgs(g, pow(g, x, p), p)
        rows.append({"bits": bits, "seconds": time.perf_counter() - t, "table": m, "ok": r == x})
    # a prime with smooth p - 1 against a safe prime of similar size
    while True:
        k = 1
        for q in P.SMALL_PRIMES[:30]:
            if rng.random() < 0.5:
                k *= q
        p = 2 * k + 1
        if p.bit_length() > 60 and P.is_probable_prime(p):
            break
    g = P.find_generator(p)
    x = rng.randrange(p - 1)
    t = time.perf_counter()
    xr, f = P.pohlig_hellman(g, pow(g, x, p), p)
    ph = time.perf_counter() - t
    while True:
        q = P.random_prime(p.bit_length() - 1, rng)
        if P.is_probable_prime(2 * q + 1):
            safe = 2 * q + 1
            break
    p2 = P.random_prime(30, rng)
    g2 = P.find_generator(p2)
    x2 = rng.randrange(p2 - 1)
    t = time.perf_counter()
    xi, st = P.index_calculus(g2, pow(g2, x2, p2), p2, 80, rng)
    ic = time.perf_counter() - t
    return {"rows": rows, "smooth_p": p, "smooth_bits": p.bit_length(), "smooth_factors": {str(k): v for k, v in
                                                                                             f.items()},
            "ph_ok": xr == x, "ph_seconds": ph, "safe_p": safe, "safe_bits": safe.bit_length(),
            "ic_p": p2, "ic_ok": xi == x2, "ic_seconds": ic, "ic_relations": st["relations"], "ic_tries": st["tries"],
            "ic_base": st["base"]}


def compute_curves() -> dict:
    C = P.TOY
    pts = C.points()
    N, (G, order) = P.toy_curve_group(C)
    mult = []
    Q = None
    for k in range(1, order + 1):
        Q = C.add(Q, G)
        mult.append(Q)
    rng = random.Random(8)
    d, Q = P.ec_keypair(P.P256, rng)
    t = time.perf_counter()
    for _ in range(5):
        P.P256.mul(d, P.P256.G)
    ms = (time.perf_counter() - t) / 5 * 1000
    tr = []
    P.P256.mul(0b10110101, P.P256.G, trace=tr)
    a, b = bytes(rng.randrange(256) for _ in range(32)), bytes(rng.randrange(256) for _ in range(32))
    A, B = P.x25519(a, P.X25519_BASE), P.x25519(b, P.X25519_BASE)
    k = bytes.fromhex("a546e36bf0527c9d3b16154b82465edd62144c0ac1fc5a18506a2244ba449ac4")
    u = bytes.fromhex("e6db6867583030db3594c1a424b15f7c726624ec26b3353b10a903a6d0ab1c4c")
    return {"p": C.p, "a": C.a, "b": C.b, "points": pts, "N": N, "G": G, "order": order,
            "multiples": [list(m) if m else None for m in mult], "p256_ms": ms,
            "ladder": [s for s, _ in tr], "x25519_equal": P.x25519(a, B) == P.x25519(b, A),
            "x25519_vector": P.x25519(k, u).hex(),
            "x25519_expected": "c3da55379de9c6908e94ea4df28d084f32eccf03491c71f754b4075577a28552"}


def compute_ecdsa() -> dict:
    x = 0xC9AFA9D845BA75166B5C215767B1D6934E50C3DB36E89B127B8A622B120F6721
    r, s = P.ecdsa_sign(x, b"sample")
    rng = random.Random(9)
    d, Qk = P.ec_keypair(P.P256, rng)
    k = rng.randrange(1, P.P256.n)
    m1, m2 = b"game update 3.55", b"game update 3.56"
    s1, s2 = P.ecdsa_sign(d, m1, k=k), P.ecdsa_sign(d, m2, k=k)
    kk, dd = P.ecdsa_nonce_reuse(m1, s1, m2, s2)
    forged = P.ecdsa_sign(dd, b"homebrew loader")
    return {"r": hex(r), "s": hex(s), "r_expected": "0xefd48b2aacb6a8fd1140dd9cd45e81d69d2c877b56aaf991c34d0ea84eaf3716",
            "same_r": s1[0] == s2[0], "k_ok": kk == k, "d_ok": dd == d,
            "forged_ok": P.ecdsa_verify(Qk, b"homebrew loader", forged), "r1": hex(s1[0])[:18],
            "s1": hex(s1[1])[:18], "s2": hex(s2[1])[:18], "d": hex(d)[:18]}


def compute_pki() -> dict:
    rng = random.Random(10)
    root_k, root_p = P.ec_keypair(P.P256, rng)
    int_k, int_p = P.ec_keypair(P.P256, rng)
    leaf_k, leaf_p = P.ec_keypair(P.P256, rng)
    inter = P.make_cert("Pebble Intermediate CA", int_p, "Pebble Root CA", root_k)
    leaf = P.make_cert("pebble.example", leaf_p, "Pebble Intermediate CA", int_k)
    roots = {"Pebble Root CA": root_p}
    ok = P.verify_chain([leaf, inter], roots)
    bad = dict(leaf)
    bad["body"] = leaf["body"].replace(b"pebble.example", b"evil.example!!")
    tampered = P.verify_chain([bad, inter], roots)
    mk, mp = P.ec_keypair(P.P256, rng)
    self_signed = P.make_cert("pebble.example", mp, "Pebble Root CA", mk)
    return {"ok": ok, "tampered": tampered, "self_signed": P.verify_chain([self_signed], roots),
            "chain": [leaf["subject"], inter["subject"], "Pebble Root CA"], "body_len": len(leaf["body"])}


def compute_tls() -> dict:
    t = time.perf_counter()
    r = P.tls_handshake(random.Random(11))
    r["seconds"] = time.perf_counter() - t
    return r


def compute_shor() -> dict:
    rows = []
    for N, a in ((15, 7), (21, 2), (35, 2)):
        r = 1
        while pow(a, r, N) != 1:
            r += 1
        y = pow(a, r // 2, N)
        rows.append({"N": N, "a": a, "r": r, "powers": [pow(a, k, N) for k in range(2 * r + 1)],
                     "f1": math.gcd(y - 1, N), "f2": math.gcd(y + 1, N)})
    return {"rows": rows}


def compute_lattices() -> dict:
    rng = random.Random(12)
    (b1, b2), steps = P.gauss_reduce((90, 123), (56, 76))
    kp = P.knapsack_keygen(20, rng)
    bits = [rng.getrandbits(1) for _ in range(20)]
    c = sum(b * x for b, x in zip(bits, kp["pub"]))
    t = time.perf_counter()
    rec = P.knapsack_attack(kp["pub"], c)
    lll_s = time.perf_counter() - t
    q = 3329
    s, pub = P.lwe_keygen(32, 128, q, rng)
    ds = {0: [], 1: []}
    for i in range(400):
        b = i % 2
        ds[b].append(P.lwe_decrypt(s, P.lwe_encrypt(pub, b, q, rng), q)[1])
    f = [rng.randrange(q) for _ in range(256)]
    g = [rng.randrange(q) for _ in range(256)]
    t = time.perf_counter()
    for _ in range(5):
        P.poly_mul_schoolbook(f, g)
    school = (time.perf_counter() - t) / 5
    t = time.perf_counter()
    for _ in range(5):
        P.intt(P.ntt_mul(P.ntt(f), P.ntt(g)))
    nttt = (time.perf_counter() - t) / 5
    sk = P.kpke_keygen(rng)
    wrong, trials, ws = 0, 100, []
    for _ in range(trials):
        m = [rng.getrandbits(1) for _ in range(256)]
        out, w = P.kpke_decrypt(sk, P.kpke_encrypt(sk, m, rng))
        wrong += sum(x != y for x, y in zip(out, m))
        ws.append([(wi if wi < q // 2 else wi - q) for wi, mi in zip(w, m) if mi == 0][:20])
    return {"gauss": steps, "reduced": [b1, b2], "knap_ok": rec == bits, "knap_n": 20, "lll_s": lll_s,
            "knap_pub": kp["pub"][:5], "lwe_d0": ds[0], "lwe_d1": ds[1], "q": q, "school_ms": school * 1000,
            "ntt_ms": nttt * 1000, "kpke_wrong": wrong, "kpke_trials": trials, "kpke_noise": sum(ws, [])[:400]}


def compute_beyond() -> dict:
    rng = random.Random(13)
    sk, pk = P.lamport_keygen(rng)
    sig = P.lamport_sign(sk, b"hello")
    grp = P.schnorr_group(rng, qbits=160, pbits=1024)
    x = rng.randrange(grp[1])
    y = pow(grp[2], x, grp[0])
    ss = P.schnorr_sign(x, b"hello", grp, rng)
    p = 2 ** 61 - 1
    shares, coeffs = P.shamir_split(31337, 3, 5, p, rng)
    return {"lamport_pk_bytes": 2 * 256 * 32, "lamport_sig_bytes": 256 * 32,
            "lamport_ok": P.lamport_verify(pk, b"hello", sig), "schnorr_ok": P.schnorr_verify(y, b"hello", ss, grp),
            "shamir_p": p, "shares": shares, "coeffs": coeffs,
            "from_3": P.shamir_combine(shares[:3], p), "from_other_3": P.shamir_combine([shares[1], shares[3],
                                                                                       shares[4]], p),
            "from_2": P.shamir_combine(shares[:2], p)}


ITEMS = {k[8:]: v for k, v in globals().items() if k.startswith("compute_")}

if __name__ == "__main__":
    CACHE.main(ITEMS, __doc__)
