"""Authentication (Part 55, chapter 5): how much a password is worth and how long it stands; one-time codes as an
HMAC over a counter or the clock (RFC 4226 HOTP, RFC 6238 TOTP); and the Needham-Schroeder public-key protocol
(1978) with the man-in-the-middle Gavin Lowe found in 1995 by model checking (Lowe, *Breaking and fixing the
Needham-Schroeder public-key protocol*, TACAS 1996), together with his fix.

Password guessing is arithmetic: entropy = length * log2(alphabet); the time to exhaust a space at a given hash rate
is 2^entropy / rate, and a fast unsalted hash runs ~10^10 guesses/s where a salted slow hash (bcrypt/scrypt/argon2,
Part 29) is deliberately ~10/s per core.  The Zipf model of human-chosen passwords is illustrative (after Bonneau,
*The science of guessing*, 2012; Wang et al., CCS 2016): real distributions are close to Zipf with exponent near 1,
so a small dictionary cracks a large share.

The Needham-Schroeder model is a Dolev-Yao search: the network is the intruder, which intercepts every message, may
replay or forward it, decrypt anything sealed to it, and compose new messages from the pieces it knows.  We explore
every interleaving breadth-first, so the attack comes with a shortest trace.
"""

from __future__ import annotations

import hmac
import math
from collections import deque

# ======================================================================================================================
# 1. Password entropy and guessing
# ======================================================================================================================

ALPHABETS = {"digits": 10, "lowercase": 26, "alnum lower": 36, "alphanumeric": 62, "with symbols": 95}


def password_entropy(alphabet: int, length: int) -> float:
    """Bits of entropy of a *uniformly random* password: length * log2(alphabet)."""
    return length * math.log2(alphabet)


def guessing(entropy_bits: float, rate: float) -> dict:
    """Guesses to search the whole space (2^bits), and the time at ``rate`` guesses/second: the full sweep and the
    expected (half-space) time to the first hit."""
    space = 2.0 ** entropy_bits
    full = space / rate
    return {"space": space, "seconds_full": full, "seconds_expected": full / 2}


def guessing_table(rates=None, lengths=(6, 8, 10, 12, 16)) -> list[dict]:
    """A grid of entropy and crack time: each alphabet x length, at a fast unsalted rate and a slow salted one."""
    rates = rates or {"fast unsalted (1e10/s)": 1e10, "slow salted (10/s/core)": 10.0}
    out = []
    for aname, asize in ALPHABETS.items():
        for n in lengths:
            bits = password_entropy(asize, n)
            times = {rn: guessing(bits, rv)["seconds_expected"] for rn, rv in rates.items()}
            out.append({"alphabet": aname, "size": asize, "length": n, "entropy_bits": bits, "seconds": times})
    return out


def zipf_cracked(vocab: int = 10 ** 7, exponent: float = 1.0, ks=(1, 2, 3, 4, 5, 6)) -> dict:
    """A Zipf-like model of human-chosen passwords (illustrative): the r-th most common password has probability
    proportional to 1/r^exponent over a vocabulary of ``vocab`` entries.  Returns the share of users cracked within
    the first 10^k guesses (a dictionary attack walking the ranks in order).
    """
    # Harmonic-ish normaliser H = sum_{r=1..vocab} r^-exponent, and prefix sums at the 10^k cut-offs.
    cuts = [min(10 ** k, vocab) for k in ks]
    H = 0.0
    prefix = {}
    target = set(cuts)
    acc = 0.0
    for r in range(1, vocab + 1):
        acc += r ** (-exponent)
        if r in target:
            prefix[r] = acc
    H = acc
    out = []
    for k, c in zip(ks, cuts):
        out.append({"guesses": 10 ** k, "share_cracked": prefix[c] / H})
    return {"vocab": vocab, "exponent": exponent, "normaliser": H, "rows": out}


# ======================================================================================================================
# 2. HOTP (RFC 4226) and TOTP (RFC 6238)
# ======================================================================================================================

def hotp(key: bytes, counter: int, digits: int = 6, algorithm: str = "sha1") -> str:
    """RFC 4226 HOTP: HMAC of the 8-byte big-endian counter, dynamically truncated to ``digits`` decimal digits."""
    mac = hmac.new(key, counter.to_bytes(8, "big"), algorithm).digest()
    offset = mac[-1] & 0x0F
    code = ((mac[offset] & 0x7F) << 24) | (mac[offset + 1] << 16) | (mac[offset + 2] << 8) | mac[offset + 3]
    return str(code % (10 ** digits)).zfill(digits)


def totp(key: bytes, when: int, t0: int = 0, step: int = 30, digits: int = 8, algorithm: str = "sha1") -> str:
    """RFC 6238 TOTP: HOTP over the time step counter floor((when - t0) / step)."""
    return hotp(key, (when - t0) // step, digits=digits, algorithm=algorithm)


# RFC 6238 Appendix B seeds: the ASCII string repeated/truncated to the hash's block-key length.
RFC6238_SEEDS = {
    "sha1": b"12345678901234567890",
    "sha256": b"12345678901234567890123456789012",
    "sha512": b"1234567890123456789012345678901234567890123456789012345678901234",
}


def hotp_vectors() -> list[dict]:
    """RFC 4226 Appendix D test values for counters 0..9 (seed "12345678901234567890", 6 digits, SHA-1)."""
    key = b"12345678901234567890"
    return [{"counter": c, "hotp": hotp(key, c, digits=6)} for c in range(10)]


def totp_vectors() -> list[dict]:
    """RFC 6238 Appendix B test values (8 digits), across SHA-1/256/512 at the specified times."""
    times = [59, 1111111109, 1111111111, 1234567890, 2000000000, 20000000000]
    out = []
    for algo, seed in RFC6238_SEEDS.items():
        for t in times:
            out.append({"algorithm": algo, "time": t, "totp": totp(seed, t, digits=8, algorithm=algo)})
    return out


# ======================================================================================================================
# 3. Needham-Schroeder public-key protocol and Lowe's attack
# ======================================================================================================================
#
#   M1  A -> B : {Na, A}_pub(B)
#   M2  B -> A : {Na, Nb}_pub(A)              (flawed: nothing says the reply is from B)
#   M3  A -> B : {Nb}_pub(B)
#
# Lowe's fix puts B's identity in M2:  {Na, Nb, B}_pub(A).
#
# Terms are tuples: ('id', X), ('nonce', n), ('pub', X), ('priv', X), ('enc', key, body), ('pair', x, y).

PRINCIPALS = ("A", "B", "I")


def _k0() -> frozenset:
    """What the Dolev-Yao intruder starts out knowing: every identity and public key, and its own private key."""
    base = {("id", x) for x in PRINCIPALS} | {("pub", x) for x in PRINCIPALS} | {("priv", "I")}
    return frozenset(base)


def _closure(known: frozenset) -> frozenset:
    """Everything the intruder can take apart: split pairs, and decrypt anything sealed to a key it holds."""
    know = set(known)
    changed = True
    while changed:
        changed = False
        for t in list(know):
            if t[0] == "pair":
                for part in (t[1], t[2]):
                    if part not in know:
                        know.add(part)
                        changed = True
            elif t[0] == "enc":
                key = t[1]
                if key[0] == "pub" and ("priv", key[1]) in know and t[2] not in know:
                    know.add(t[2])
                    changed = True
    return frozenset(know)


def _derivable(closure: frozenset, t) -> bool:
    """Can the intruder produce term ``t``?  Either it already holds it (a replay/forward), or it can build it from
    pieces it can produce (pairing, or encrypting with a public key it knows)."""
    if t in closure:
        return True
    if t[0] == "pair":
        return _derivable(closure, t[1]) and _derivable(closure, t[2])
    if t[0] == "enc":
        return _derivable(closure, t[1]) and _derivable(closure, t[2])
    return False


def _nonces_known(closure: frozenset):
    return {t for t in closure if t[0] == "nonce"}


# State: (a_step, a_partner, a_nb, b_step, b_partner, b_na, net)
#   a_step 0 not started / 1 sent M1, waiting M2 / 2 done;  a_partner in {None,'B','I'};  a_nb learned nonce or None
#   b_step 0 waiting M1 / 1 sent M2, waiting M3 / 2 done;   b_partner believed id or None;  b_na received nonce or None
#   net    frozenset of messages the intruder has intercepted

NA = ("nonce", "na")
NB = ("nonce", "nb")


def _successors(state, fixed: bool):
    a_step, a_partner, a_nb, b_step, b_partner, b_na, net = state
    closure = _closure(_k0() | set(net))
    nonces = _nonces_known(closure) | {NA, NB}

    # --- A ---
    if a_step == 0:
        for resp in ("B", "I"):
            m1 = ("enc", ("pub", resp), ("pair", NA, ("id", "A")))
            yield (f"A initiates with {resp}: send M1 {{Na,A}}_{resp}",
                   (1, resp, a_nb, b_step, b_partner, b_na, frozenset(net | {m1})))
    elif a_step == 1:
        # A waits for {Na, Nb'}_A  (flawed) or {Na, Nb', B'}_A (fixed, must name A's partner)
        for y in nonces:
            if not fixed:
                msg = ("enc", ("pub", "A"), ("pair", NA, y))
                if _derivable(closure, msg):
                    m3 = ("enc", ("pub", a_partner), y)
                    yield (f"A receives M2 {{Na,{y[1]}}}_A, replies M3 {{{y[1]}}}_{a_partner}",
                           (2, a_partner, y, b_step, b_partner, b_na, frozenset(net | {m3})))
            else:
                for p in PRINCIPALS:
                    msg = ("enc", ("pub", "A"), ("pair", NA, ("pair", y, ("id", p))))
                    if _derivable(closure, msg) and p == a_partner:
                        m3 = ("enc", ("pub", a_partner), y)
                        yield (f"A receives M2 {{Na,{y[1]},{p}}}_A (partner ok), replies M3 {{{y[1]}}}_{a_partner}",
                               (2, a_partner, y, b_step, b_partner, b_na, frozenset(net | {m3})))

    # --- B ---
    if b_step == 0:
        for n in nonces:
            for p in PRINCIPALS:
                msg = ("enc", ("pub", "B"), ("pair", n, ("id", p)))
                if _derivable(closure, msg):
                    if not fixed:
                        m2 = ("enc", ("pub", p), ("pair", n, NB))
                    else:
                        m2 = ("enc", ("pub", p), ("pair", n, ("pair", NB, ("id", "B"))))
                    yield (f"B receives M1 {{{n[1]},{p}}}_B (believes {p}), sends M2",
                           (a_step, a_partner, a_nb, 1, p, n, frozenset(net | {m2})))
    elif b_step == 1:
        msg = ("enc", ("pub", "B"), NB)
        if _derivable(closure, msg):
            yield ("B receives M3 {Nb}_B: completes",
                   (a_step, a_partner, a_nb, 2, b_partner, b_na, net))


def _is_attack(state) -> bool:
    """B completed a run it believes is with A, but A never ran a session with B."""
    a_step, a_partner, a_nb, b_step, b_partner, b_na, net = state
    return b_step == 2 and b_partner == "A" and a_partner != "B"


def needham_schroeder(fixed: bool = False, limit: int = 2_000_000) -> dict:
    """Explore the protocol with one initiator run, one responder run, and the Dolev-Yao intruder.  Reports whether
    the man-in-the-middle attack is reachable, a shortest trace to it, how many states were explored, and whether the
    intruder learned B's secret nonce Nb.
    """
    start = (0, None, None, 0, None, None, frozenset())
    parent = {start: None}
    q = deque([start])
    attack = None
    while q:
        s = q.popleft()
        if attack is None and _is_attack(s):
            attack = s
        for label, t in _successors(s, fixed):
            if t not in parent:
                parent[t] = (s, label)
                q.append(t)
                if len(parent) > limit:
                    raise RuntimeError("state space too large")
    trace = None
    knows_nb = False
    if attack is not None:
        steps = []
        cur = attack
        while parent[cur] is not None:
            p, label = parent[cur]
            steps.append(label)
            cur = p
        trace = steps[::-1]
        knows_nb = NB in _closure(_k0() | set(attack[6]))
    return {"fixed": fixed, "attack_found": attack is not None, "trace": trace,
            "states_explored": len(parent), "intruder_knows_Nb": knows_nb}
