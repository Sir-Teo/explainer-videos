"""Lab 30: run Diffie-Hellman and RSA, then measure what the attacker pays: square roots, not polynomials."""

from videos.coursekit import labs

import math
import random

import numpy as np

from explainer.cs.algo import pubkey as P

TITLE = "Easy forwards, a square root backwards: Diffie-Hellman, RSA and their generic attacks"
GOAL = ("Redo the film's exchange (p = 23, g = 5) and its RSA example, then break Diffie-Hellman by baby-step "
        "giant-step and factor semiprimes by Pollard's rho as the keys grow, and check that the attacker's work grows "
        "like 2^(bits/2) and 2^(bits/4) while the user's grows like the number of bits. Finally recover a P-256 "
        "signing key from two signatures that share a nonce.")
TASKS = [
    "Extend DLOG_BITS to 36 and 40. How long does baby-step giant-step take, and how much memory does its table need at 2048 bits?",
    "Pick a prime p with p - 1 a product of small primes and solve the logarithm with P.pohlig_hellman. Why are safe primes used?",
    "Sign the two messages with the default RFC 6979 nonces instead of a fixed k. What does P.ecdsa_nonce_reuse return now, and why?",
]
DLOG_BITS = (16, 20, 24, 28, 32)
RSA_BITS = (40, 48, 56, 64)


def run(seed=0):
    rng = random.Random(int(np.random.default_rng(seed).integers(2 ** 31)))
    lab = labs.Lab()

    # 1. the hook: p = 23, g = 5, secrets 6 and 15
    A, B = pow(5, 6, 23), pow(5, 15, 23)
    lab.row("Diffie-Hellman, p = 23, g = 5", f"A = {A}, B = {B}, shared {pow(B, 6, 23)} = {pow(A, 15, 23)}   (the film: 8, 19, 2)")
    assert (A, B, pow(B, 6, 23), pow(A, 15, 23)) == (8, 19, 2, 2)
    for _ in range(20):                                   # and in a 61-bit group: both sides agree, Mallory splits them
        p = 2 ** 61 - 1
        a, ga = P.dh_keypair(p, 3, rng)
        b, gb = P.dh_keypair(p, 3, rng)
        assert pow(gb, a, p) == pow(ga, b, p)
    m = P.dh_mitm(23, 5, rng)
    assert m["alice"] == m["mallory_with_alice"] and m["bob"] == m["mallory_with_bob"], "no authentication, no secret"

    # 2. RSA: the film's toy key, and a 512-bit key from the series' Miller-Rabin
    toy = {"n": 61 * 53, "e": 17, "d": P.inv_mod(17, 60 * 52)}
    c = P.rsa_enc(65, toy)
    lab.row("RSA, p = 61, q = 53, e = 17", f"d = {toy['d']}, 65 -> {c} -> {pow(c, toy['d'], toy['n'])}   (the film: 2753, 2790, 65)")
    assert (toy["d"], c, pow(c, toy["d"], toy["n"])) == (2753, 2790, 65)
    key = P.rsa_keygen(512, rng)
    for _ in range(5):
        msg = rng.randrange(key["n"])
        ct = P.rsa_enc(msg, key)
        assert P.rsa_dec(ct, key) == P.rsa_dec(ct, key, use_crt=False) == msg
    assert key["p"] * key["q"] == key["n"] and key["e"] * key["d"] % math.lcm(key["p"] - 1, key["q"] - 1) == 1

    # 3. the attacker: baby-step giant-step on the discrete log, Pollard's rho on the modulus
    table, logp = [], []
    for bits in DLOG_BITS:
        p = P.random_prime(bits, rng)
        g = P.find_generator(p)
        x = rng.randrange(2, p - 1)
        found, size = P.bsgs(g, pow(g, x, p), p)
        assert found == x and abs(size / math.sqrt(p) - 1) < 0.01
        table.append(size)
        logp.append(math.log2(p))
        lab.row(f"discrete log, {bits}-bit prime", f"table of {size:,} entries   sqrt(p) = {math.sqrt(p):,.0f}   user: about {2 * bits} multiplications")
    steps = []
    for bits in RSA_BITS:
        runs = []
        for _ in range(9):
            p, q = P.random_prime(bits // 2, rng), P.random_prime(bits // 2, rng)
            if p == q:
                continue
            f, st = P.pollard_rho(p * q, rng)
            assert f in (p, q)
            runs.append(st)
        steps.append(float(np.median(runs)))
        lab.row(f"factoring, {bits}-bit modulus", f"rho: median {steps[-1]:,.0f} steps   n^(1/4) = {2 ** (bits / 4):,.0f}")
    slope_dlog = np.polyfit(logp, np.log2(table), 1)[0]
    slope_rho = np.polyfit(RSA_BITS, np.log2(steps), 1)[0]
    lab.row("growth per key bit", f"log2(work): BSGS {slope_dlog:.2f} (theory 1/2)   rho {slope_rho:.2f} (theory 1/4)")
    assert abs(slope_dlog - 0.5) < 0.02 and 0.1 < slope_rho < 0.45, "square-root attacks: exponential in the key length"

    # 4. one repeated nonce gives away an ECDSA key (P-256)
    d, Q = P.ec_keypair(P.P256, rng)
    k = rng.randrange(1, P.P256.n)
    m1, m2 = b"firmware 3.55", b"firmware 3.56"
    s1, s2 = P.ecdsa_sign(d, m1, k=k), P.ecdsa_sign(d, m2, k=k)
    k_found, d_found = P.ecdsa_nonce_reuse(m1, s1, m2, s2)
    forged = P.ecdsa_sign(d_found, b"anything at all")
    lab.row("ECDSA, one nonce used twice", f"nonce recovered: {k_found == k}   private key recovered: {d_found == d}   forgery verifies: {P.ecdsa_verify(Q, b'anything at all', forged)}")
    assert s1[0] == s2[0] and k_found == k and d_found == d and P.ecdsa_verify(Q, b"anything at all", forged)
    lab.note = ("The user's cost grows with the number of key bits and the generic attacker's with a power of two of "
                "it, so adding bits wins; a repeated nonce or a missing signature loses whatever the key length.")

    fig, ax = labs.figure(2, size=(11, 4.2))
    grid = np.linspace(14, 34, 20)
    ax[0].semilogy(DLOG_BITS, table, "o", color=labs.RED, label="baby-step giant-step: table entries")
    ax[0].semilogy(grid, 2 ** (grid / 2), color=labs.RED, lw=1, alpha=0.7, label="2^(bits/2)")
    ax[0].semilogy(grid, 2 * grid, color=labs.GREEN, label="the user: about 2 · bits multiplications")
    ax[0].set(title="Discrete logarithm: user against attacker", xlabel="bits of the prime p", ylabel="operations",
              xticks=DLOG_BITS)
    ax[0].legend()
    grid = np.linspace(38, 66, 20)
    ax[1].semilogy(RSA_BITS, steps, "o", color=labs.GOLD, label="Pollard's rho: median steps")
    ax[1].semilogy(grid, 2 ** (grid / 4), color=labs.GOLD, lw=1, alpha=0.7, label="2^(bits/4) = n^(1/4)")
    ax[1].semilogy(grid, 2 ** (grid / 2), color=labs.MUTED, ls="--", label="trial division: 2^(bits/2)")
    ax[1].set(title="Factoring a semiprime n = pq", xlabel="bits of the modulus n", ylabel="steps", xticks=RSA_BITS)
    ax[1].legend()
    lab.fig = fig
    return lab
