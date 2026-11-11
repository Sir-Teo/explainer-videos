"""Precompute everything numerical in Part 29 of *Computer Science, Built* ("Secrets").

    python -m videos.cs.cs29.compute              # everything missing
    python -m videos.cs.cs29.compute --force penguin

Results are cached in ``.cache/cs29/<name>.json``; scenes call ``load(name)``.  The instrument is
``explainer/cs/algo/crypto.py`` (tested in tests/test_cs29_crypto.py).

Items:
    subst       a paragraph of Moby-Dick under a random substitution, broken by hill climbing on quadgrams
    vigenere    the same paragraph under Vigenere, its key length by index of coincidence, and the key recovered
    enigma      the Enigma I test vector, a message, the key space, and Rejewski's characteristic under two plugboards
    otp         a two-time pad and crib dragging
    lfsr        a 17-bit LFSR keystream recovered by Berlekamp-Massey from 34 bits
    chacha      RFC 8439 vectors and our keystream speed
    feistel     distinguishing 1-, 2- and 3-round Feistel networks with random round functions from a random function
    ggm         a depth-3 GGM tree with SHA-256 as the length-doubling PRG
    aes         FIPS-197 vectors; the state after every step of AES on the C.1 example
    avalanche   bits of the state changed by one flipped plaintext bit, after each round
    penguin     our logo under ECB, CBC and CTR
    padding     Vaudenay's padding-oracle attack: plaintext recovered and queries used
    mac         CBC-MAC's splicing forgery; HMAC; GCM's NIST vectors
    hashes      birthday collisions on truncated SHA-256; length extension; SHA-256 and SHA3-256 against hashlib
    passwords   PBKDF2 and scrypt costs, and what they mean for guessing
    merkle      a Merkle tree over eight commits and a proof for one of them
    spn         Heys' toy SPN: the difference table, the trail, and the differential attack's key counts; MITM
    timing      an early-exit comparison timed against the number of correct leading bytes
    debian      a PID-seeded key, found by trying all 32,768 seeds
"""

from __future__ import annotations

import hashlib
import math
import random
import statistics
import time

from explainer.ai.cache import Cache
from explainer.cs.algo import crypto as K

CACHE = Cache("cs29")
load = CACHE.load


def _books():
    import videos.ai.ai1.compute as A
    from videos.cs.cs6.compute import novels
    b = novels()
    return {A.BOOKS[k]: b[k] for k in A.BOOKS}


def _paragraph():
    md = _books()["Moby Dick"]
    i = md.find("Call me Ishmael")
    return md[i:i + 1100]


def compute_subst() -> dict:
    books = _books()
    model = K.quadgram_model("".join(v for k, v in books.items() if k != "Moby Dick")[:6_000_000])
    pt = K.letters(_paragraph())[:600]
    rng = random.Random(1)
    key = list(K.A2Z)
    rng.shuffle(key)
    key = "".join(key)
    ct = K.subst(pt, key)
    t = time.perf_counter()
    dkey, dec, trace = K.break_substitution(ct, model, random.Random(2), restarts=6, iters=2500)
    dt = time.perf_counter() - t
    acc = sum(a == b for a, b in zip(dec, pt)) / len(pt)
    from collections import Counter
    cf = Counter(ct)
    return {"plain": pt, "key": key, "cipher": ct, "decrypted": dec, "accuracy": acc, "seconds": dt,
            "trace": trace[::max(1, len(trace) // 12)] + trace[-1:], "cipher_freq": {c: cf.get(c, 0) / len(ct) for c in K.A2Z},
            "english": K.ENGLISH_FREQ, "keyspace": math.factorial(26),
            "finals": K.break_substitution.finals, "improvements": len(trace) - 1,
            "start": K.break_substitution.rank_start[:60]}


def compute_vigenere() -> dict:
    pt = K.letters(_paragraph())[:600]
    key = "BABBAGE"
    ct = K.vigenere(pt, key)
    rec, dec, scores = K.break_vigenere(ct)
    return {"key": key, "cipher": ct, "recovered": rec, "decrypted_ok": dec == pt, "ioc_plain": K.ioc(pt),
            "ioc_cipher": K.ioc(ct), "ioc_random": 1 / 26, "scores": scores, "plain": pt[:80], "cipher60": ct[:80]}


def compute_enigma() -> dict:
    e = K.Enigma(("II", "IV", "V"), "BLA", "AAA", "AV BS CG DL FU HZ IN KM OW RX")
    msg = "WETTERBERICHTFUERDIENORDSEE"
    ct = e.encrypt(msg)
    e2 = K.Enigma(("II", "IV", "V"), "BLA", "AAA", "AV BS CG DL FU HZ IN KM OW RX")
    back = e2.encrypt(ct)
    a, pa = K.rejewski_characteristic(("II", "IV", "V"), "BLA", "")
    b, pb = K.rejewski_characteristic(("II", "IV", "V"), "BLA", "AV BS CG DL FU HZ IN KM OW RX")
    c, _ = K.rejewski_characteristic(("I", "III", "II"), "QDF", "AV BS CG DL FU HZ IN KM OW RX")
    plug10 = math.factorial(26) // (math.factorial(6) * math.factorial(10) * 2 ** 10)
    total = 60 * 26 ** 3 * plug10
    never_self = all(x != y for x, y in zip(msg, ct))
    return {"vector": K.Enigma().encrypt("AAAAA"), "msg": msg, "cipher": ct, "back": back, "no_self": never_self,
            "char_noplug": a, "char_plug": b, "char_other": c, "cycles_noplug": K.cycles(pa[0]),
            "cycles_plug": K.cycles(pb[0]), "plugboard": plug10, "keyspace": total,
            "rotor_settings": 60 * 26 ** 3}


def compute_otp() -> dict:
    rng = random.Random(4)
    m1 = b"MEET THE AGENT AT THE BRIDGE AT NOON"
    m2 = b"THE CODE BOOK IS UNDER THE STAIRWAY "
    n = min(len(m1), len(m2))
    m1, m2 = m1[:n], m2[:n]
    pad = bytes(rng.randrange(256) for _ in range(n))
    c1, c2 = K.xor(m1, pad), K.xor(m2, pad)
    drag = K.crib_drag(c1, c2, b" THE ")
    hits = [(i, s.decode("latin-1")) for i, s in drag if all(ch == 32 or 65 <= ch <= 90 for ch in s)]
    return {"m1": m1.decode(), "m2": m2.decode(), "c1": c1.hex(), "c2": c2.hex(), "x": K.xor(c1, c2).hex(),
            "hits": hits[:12], "n": n}


def compute_lfsr() -> dict:
    taps = [17, 14]                                      # x^17 + x^14 + 1: primitive, period 2^17 - 1
    rng = random.Random(5)
    seed = [rng.randrange(2) for _ in range(17)]
    s = K.lfsr(taps, seed, 2000)
    L, C = K.berlekamp_massey_gf2(s[:34])
    pred = K.lfsr_from_connection(C, s, 2000)
    return {"taps": taps, "seed": seed, "first": s[:64], "L": L, "C": C, "bits_used": 34,
            "predicted_ok": pred == s, "period": 2 ** 17 - 1}


def compute_chacha() -> dict:
    key = bytes(range(32))
    nonce = bytes.fromhex("000000090000004a00000000")
    blk = K.chacha20_block(key, 1, nonce)
    data = bytes(64 * 200)
    t = time.perf_counter()
    K.chacha20_encrypt(key, 1, nonce, data)
    dt = time.perf_counter() - t
    return {"qr": [hex(v) for v in K.quarter_round(0x11111111, 0x01020304, 0x9B8D6F43, 0x01234567)],
            "block16": blk[:16].hex(), "bytes_per_s": len(data) / dt}


def _rand_fn(rng, bits):
    table = {}

    def f(x):
        if x not in table:
            table[x] = rng.getrandbits(bits)
        return table[x]
    return f


def compute_feistel() -> dict:
    rng = random.Random(6)
    half = 16
    trials = 2000
    rows = []
    for rounds in (1, 2, 3):
        hits_feistel = hits_random = 0
        for _ in range(trials):
            fs = [_rand_fn(rng, half) for _ in range(rounds)]

            def F(L, R, fs=fs):
                for f in fs:
                    L, R = R, L ^ f(R)
                return L, R
            rnd = _rand_fn(rng, 2 * half)

            def test(perm):
                """The 2-round distinguisher: inputs (L1, R) and (L2, R); check the left-half XOR."""
                L1, L2, R = rng.getrandbits(half), rng.getrandbits(half), rng.getrandbits(half)
                a1, b1 = perm(L1, R)
                a2, b2 = perm(L2, R)
                if rounds == 1:
                    return a1 == R and a2 == R
                return (a1 ^ a2) == (L1 ^ L2)
            hits_feistel += test(F)
            hits_random += test(lambda L, R: divmod(rnd((L << half) | R), 1 << half))
        rows.append({"rounds": rounds, "feistel": hits_feistel / trials, "random": hits_random / trials})
    return {"half_bits": half, "trials": trials, "rows": rows}


def compute_ggm() -> dict:
    seed = hashlib.sha256(b"GGM seed").digest()[:8]

    def G(s):
        h = hashlib.sha256(s).digest()
        return h[:8], h[8:16]
    nodes = {"": seed.hex()}
    for depth in range(3):
        for path in [p for p in list(nodes) if len(p) == depth]:
            l, r = G(bytes.fromhex(nodes[path]))
            nodes[path + "0"], nodes[path + "1"] = l.hex(), r.hex()
    return {"nodes": nodes, "input": "101", "output": nodes["101"]}


def compute_aes() -> dict:
    key = bytes.fromhex("000102030405060708090a0b0c0d0e0f")
    pt = bytes.fromhex("00112233445566778899aabbccddeeff")
    rk = K.key_expansion(key)
    ct, steps = K.aes_encrypt_block(pt, rk, trace=True)
    return {"key": key.hex(), "plain": pt.hex(), "cipher": ct.hex(), "expected": "69c4e0d86a7b0430d8cdb78070b4c55a",
            "steps": [(name, bytes(s).hex()) for name, s in steps], "round_keys": [bytes(k).hex() for k in rk],
            "sbox_row": [K.SBOX[x] for x in range(16)], "sbox53": K.SBOX[0x53], "inv53": K._ginv(0x53)}


def compute_avalanche() -> dict:
    rng = random.Random(7)
    data = K.avalanche_by_round(rng, trials=400)
    mean = [statistics.mean(t[r] for t in data) for r in range(11)]
    final = [t[10] for t in data]
    hist = {}
    for v in final:
        hist[v] = hist.get(v, 0) + 1
    # a heatmap: which of the 128 bits differ after rounds 1..4 for one example
    key = bytes(range(16))
    rk = K.key_expansion(key)
    p = bytes(16)
    q = bytearray(p)
    q[0] ^= 1
    _, sa = K.aes_encrypt_block(p, rk, trace=True)
    _, sb = K.aes_encrypt_block(bytes(q), rk, trace=True)
    ka = [s for name, s in sa if name.startswith("AddRoundKey")]
    kb = [s for name, s in sb if name.startswith("AddRoundKey")]
    maps = [[[(x ^ y) >> b & 1 for b in range(8)] for x, y in zip(ka[r], kb[r])] for r in range(5)]
    return {"mean": mean, "final_mean": statistics.mean(final), "final_sd": statistics.pstdev(final), "hist": hist,
            "trials": len(data), "maps": maps}


def _logo(w=128, h=96):
    from PIL import Image, ImageDraw, ImageFont
    img = Image.new("L", (w, h), 230)
    d = ImageDraw.Draw(img)
    d.ellipse((10, 10, 86, 86), fill=40)
    d.ellipse((30, 30, 66, 66), fill=230)
    d.rectangle((70, 52, 118, 86), fill=120)
    try:
        font = ImageFont.truetype("DejaVuSans-Bold.ttf", 26)
    except OSError:
        font = ImageFont.load_default()
    d.text((78, 8), "29", fill=40, font=font)
    return [img.getpixel((x, y)) for y in range(h) for x in range(w)], w, h


def compute_penguin() -> dict:
    px, w, h = _logo()
    data = bytes(px)
    aes = K.AES(bytes.fromhex("2b7e151628aed2a6abf7158809cf4f3c"))
    iv = bytes(range(16))
    ecb = K.ecb_encrypt(aes, data)
    cbc = K.cbc_encrypt(aes, iv, data)
    ctr = K.ctr_encrypt(aes, bytes(8), data)
    blocks = [data[i:i + 16] for i in range(0, len(data), 16)]
    return {"w": w, "h": h, "plain": list(data), "ecb": list(ecb), "cbc": list(cbc), "ctr": list(ctr),
            "blocks": len(blocks), "distinct_plain": len(set(blocks)),
            "distinct_ecb": len(set(ecb[i:i + 16] for i in range(0, len(ecb), 16))),
            "distinct_cbc": len(set(cbc[i:i + 16] for i in range(0, len(cbc), 16)))}


def compute_padding() -> dict:
    aes = K.AES(bytes.fromhex("000102030405060708090a0b0c0d0e0f"))
    iv = bytes.fromhex("f0e1d2c3b4a5968778695a4b3c2d1e0f")
    msg = b"PIN=4921; transfer approved by the bank"
    pt = K.pkcs7_pad(msg)
    ct = K.cbc_encrypt(aes, iv, pt)
    calls = [0]

    def oracle(ivx, blk):
        calls[0] += 1
        try:
            K.pkcs7_unpad(K.cbc_decrypt(aes, ivx, blk))
            return True
        except ValueError:
            return False
    t = time.perf_counter()
    rec, q = K.padding_oracle_attack(iv, ct, oracle)
    dt = time.perf_counter() - t
    return {"message": msg.decode(), "blocks": len(ct) // 16, "recovered": K.pkcs7_unpad(rec).decode(),
            "queries": q, "per_byte": q / len(pt), "seconds": dt, "naive": 256 ** 16}


def compute_mac() -> dict:
    aes = K.AES(bytes(range(16)))
    m1 = b"PAY ALICE $0010."
    m2 = b"PAY EVE $1000000"
    t1 = K.cbc_mac(aes, m1)
    t2 = K.cbc_mac(aes, m2)
    forged = m1 + K.xor(m2[:16], t1)
    ok = K.cbc_mac(aes, forged) == t2
    return {"m1": m1.decode(), "m2": m2.decode(), "t1": t1.hex(), "t2": t2.hex(), "forged_hex": forged.hex(),
            "forgery_valid": ok, "hmac": K.hmac_sha256(b"key", b"message").hex(),
            "gcm_tag": K.aes_gcm_encrypt(bytes(16), bytes(12), bytes(16))[1].hex()}


def compute_hashes() -> dict:
    rng = random.Random(8)
    rows = []
    for bits in (16, 20, 24, 28, 32):
        trials = 30 if bits <= 24 else 10
        counts = [K.birthday_trial(bits, rng) for _ in range(trials)]
        rows.append({"bits": bits, "median": statistics.median(counts), "mean": statistics.mean(counts),
                     "predicted": math.sqrt(math.pi / 2 * 2 ** bits), "trials": trials})
    secret, msg = b"server-secret-16", b"user=alice&role=user"
    mac = hashlib.sha256(secret + msg).digest()
    new, forged = K.length_extension(mac, len(secret), msg, b"&role=admin")
    t = time.perf_counter()
    for _ in range(200):
        K.sha256(b"x" * 64)
    ours = (time.perf_counter() - t) / 200
    t = time.perf_counter()
    for _ in range(200000):
        hashlib.sha256(b"x" * 64).digest()
    lib = (time.perf_counter() - t) / 200000
    return {"birthday": rows, "length_ext": {"msg": msg.decode(), "new": new.hex(), "valid":
                                             forged == hashlib.sha256(secret + new).digest(), "mac": mac.hex(),
                                             "forged": forged.hex(), "glue_len": len(new) - len(msg) - 11},
            "ours_us": ours * 1e6, "hashlib_us": lib * 1e6, "sha3_ok": K.sha3_256(b"abc") == hashlib.sha3_256(b"abc")
            .digest()}


def compute_passwords() -> dict:
    rows = []
    for it in (1, 1000, 100_000, 600_000):
        t = time.perf_counter()
        hashlib.pbkdf2_hmac("sha256", b"correct horse", b"salt", it)
        rows.append({"scheme": f"PBKDF2-SHA256 x {it:,}", "seconds": time.perf_counter() - t})
    t = time.perf_counter()
    hashlib.scrypt(b"correct horse", salt=b"salt", n=2 ** 14, r=8, p=1)
    rows.append({"scheme": "scrypt N=2^14, r=8", "seconds": time.perf_counter() - t, "memory_mb": 128 * 8 * 2 ** 14
                 / 2 ** 20})
    return {"rows": rows, "space_8_lower": 26 ** 8, "space_10_mixed": 62 ** 10}


def compute_merkle() -> dict:
    leaves = [f"commit {i}: {m}".encode() for i, m in enumerate(
        ["init", "add parser", "fix overflow", "tests", "docs", "speed up", "release 1.0", "hotfix"])]
    root, levels = K.merkle_root(leaves)
    proof = K.merkle_proof(levels, 5)
    return {"leaves": [x.decode() for x in leaves], "root": root.hex(), "levels": [[h.hex()[:8] for h in lv]
                                                                                  for lv in levels],
            "proof_len": len(proof), "valid": K.merkle_verify(root, leaves[5], proof),
            "tampered": K.merkle_verify(root, b"commit 5: slow down", proof)}


def compute_spn() -> dict:
    rng = random.Random(9)
    keys = [rng.randrange(1 << 16) for _ in range(5)]
    table = K.spn_difference_table()
    t = time.perf_counter()
    counts = K.spn_differential_attack(keys, 5000, random.Random(10))
    dt = time.perf_counter() - t
    top = sorted(counts.items(), key=lambda kv: -kv[1])[:6]
    p1, p2 = 0x1234, 0xBEEF
    k1, k2 = 0x3A7C, 0xC519
    c1 = K.toy_cipher(K.toy_cipher(p1, k1), k2)
    c2 = K.toy_cipher(K.toy_cipher(p2, k1), k2)
    t = time.perf_counter()
    cands, work = K.meet_in_the_middle(p1, c1, p2, c2)
    mitm_s = time.perf_counter() - t
    return {"table": table, "trail_prob": 27 / 1024, "pairs": 5000, "true_subkey": keys[4] & 0x0F0F,
            "top": [[k, n] for k, n in top], "counts": [counts[k] for k in sorted(counts)],
            "guesses": sorted(counts), "seconds": dt, "expected_right": 5000 * 27 / 1024,
            "mitm": {"keys": [k1, k2], "found": cands, "work": work, "brute": 2 ** 32, "seconds": mitm_s}}


def compute_timing() -> dict:
    secret = bytes.fromhex("8f3a9c4e2b7d1f6a5c8e3b9d4a2f7c1e")
    rows = []
    for k in range(0, 17, 2):
        guess = secret[:k] + bytes(16 - k)
        if k < 16:
            guess = guess[:k] + bytes([secret[k] ^ 0xFF]) + guess[k + 1:]
        samples = [K.time_compare(K.early_exit_equal, secret, guess, 20000) for _ in range(25)]
        ct = [K.time_compare(K.constant_time_equal, secret, guess, 20000) for _ in range(25)]
        rows.append({"correct": k, "early_ns": min(samples) * 1e9, "constant_ns": min(ct) * 1e9})
    return {"rows": rows}


def compute_debian() -> dict:
    pid = 23107
    key = K.pid_seeded_key(pid)
    aes = K.AES(key)
    header = b"-----BEGIN DATA-"
    ct = aes.enc(header)
    t = time.perf_counter()
    found = None
    tried = 0
    for cand in range(1, 32768):
        tried += 1
        if K.AES(K.pid_seeded_key(cand)).enc(header) == ct:
            found = cand
            break
    dt = time.perf_counter() - t
    return {"pid": pid, "found": found, "tried": tried, "seconds": dt, "space": 32767, "key_bits": 128}


ITEMS = {k[8:]: v for k, v in globals().items() if k.startswith("compute_")}

if __name__ == "__main__":
    CACHE.main(ITEMS, __doc__)
