"""Lab 5: make two NAND gates remember, run Pebble's register file against a model, and count the maximal LFSRs."""

import numpy as np

from videos.coursekit import labs
from explainer.cs.pebble import seq

TITLE = "A latch, a register file and every shift register of degree 2 to 8"
GOAL = ("Drive an SR latch of two NAND gates through set, hold, reset and the forbidden input with unit gate "
        "delays; write and read Pebble's 16 x 32 register file at random against an array; then find the period "
        "of every feedback polynomial of degree 2 to 8 and count those that visit all 2^n - 1 states.")
TASKS = [
    "Release the forbidden input one tick apart (S first, then R) instead of together. Does the latch still oscillate?",
    "Build seq.register_file(16, 32, zero_reg=False) and count its flip-flops and gates. What did hard-wiring r0 save?",
    "For degree 8, list the periods that are not 255. Which of them divide 255, and what does that say about the polynomial?",
]


def period(poly, n, start=1):
    """The period of the Galois LFSR of the degree-n polynomial (bit i = the coefficient of x^i): multiply the state
    by x modulo the polynomial until it returns."""
    s, t = start, 0
    while True:
        s <<= 1
        if s >> n & 1:
            s ^= poly
        t += 1
        if s == start:
            return t
        if t > 1 << n:
            return 0  # never returned: the start was not on a cycle through itself


def totient(m):
    r, x, p = m, m, 2
    while p * p <= x:
        if x % p == 0:
            while x % p == 0:
                x //= p
            r -= r // p
        p += 1
    return r - r // x if x > 1 else r


def run(seed=0):
    rng = np.random.default_rng(seed)
    lab = labs.Lab()

    # 1. the SR latch (inputs active low): set, hold, reset, hold, forbidden, released together
    prog = [(1, 1)] * 3 + [(0, 1)] * 4 + [(1, 1)] * 5 + [(1, 0)] * 4 + [(1, 1)] * 5 + [(0, 0)] * 4 + [(1, 1)] * 9
    h = seq.sr_latch().run(lambda t: {"S_": prog[t][0], "R_": prog[t][1]}, len(prog), init={"Q": 0, "Qn": 1})
    q = h["Q"]
    lab.row("SR latch: Q after set, during hold", f"{q[6]}, {q[11]}   (remembers 1)")
    lab.row("SR latch: Q after reset, during hold", f"{q[15]}, {q[20]}   (remembers 0)")
    lab.row("after releasing S = R together", f"Q = {''.join(map(str, q[-8:]))}   (oscillates in the unit-delay model)")
    assert q[9:12] == [1, 1, 1] and h["Qn"][9:12] == [0, 0, 0], "holds the 1 with both inputs released"
    assert q[18:21] == [0, 0, 0] and h["Qn"][18:21] == [1, 1, 1], "holds the 0"
    assert all(q[t] != q[t + 1] and q[t] == h["Qn"][t] for t in range(len(prog) - 8, len(prog) - 1)), "the race never settles"
    ring = seq.ring(5).run(lambda t: {}, 40, init={f"x{i}": i % 2 for i in range(5)})["x0"]
    assert ring[:10] == ring[10:20] and ring[:5] != ring[5:10], "a ring of 5 inverters has period 10"

    # 2. the register file against an array, 64 machines side by side
    rf = seq.register_file(16, 32)
    copies, cycles = 64, 40
    rf.reset(copies)
    model = np.zeros((copies, 16), dtype=np.int64)
    idx = np.arange(copies)
    reads = 0
    for _ in range(cycles):
        we, wa, ra, rb = (rng.integers(0, k, copies) for k in (2, 16, 16, 16))
        wd = rng.integers(0, 1 << 32, copies)
        out = rf.step({"we": we, "wa": wa, "wd": wd, "ra": ra, "rb": rb})
        assert np.array_equal(out["a"], model[idx, ra]) and np.array_equal(out["b"], model[idx, rb])
        reads += 2 * copies
        m = (we == 1) & (wa != 0)  # register 0 is hard-wired to zero
        model[idx[m], wa[m]] = wd[m]
    lab.row("register file", f"{rf.flip_flops} flip-flops, {rf.c.size():,} gates   (the film: 480 and 5,824)")
    lab.row("random reads that matched the model", f"{reads:,} of {reads:,}")
    assert (rf.flip_flops, rf.c.size()) == (480, 5824) and np.all(model[:, 0] == 0)

    # 3. every feedback polynomial x^n + ... + 1 of degree 2 to 8
    degrees = list(range(2, 9))
    maximal, expected, periods8 = [], [], []
    for n in degrees:
        ps = [period((1 << n) | (mid << 1) | 1, n) for mid in range(1 << (n - 1))]
        maximal.append(sum(p == (1 << n) - 1 for p in ps))
        expected.append(totient((1 << n) - 1) // n)
        periods8 = ps
    lab.row("maximal-length polynomials, degree 2 ... 8", f"{maximal}   (phi(2^n - 1) / n: {expected})")
    assert maximal == expected, "the primitive polynomials number phi(2^n - 1) / n"
    start = int(rng.integers(1, 256))
    lab.row(f"x^8 + x^4 + x^3 + x^2 + 1 from state {start}", f"period {period(0b100011101, 8, start)}   (2^8 - 1 = 255)")
    assert period(0b100011101, 8, start) == 255, "a primitive polynomial has full period from every non-zero state"
    l4 = seq.lfsr((3, 2), 4)  # the same machine as gates and flip-flops, 4 bits
    l4.reset(1)
    states = [int(l4.step({})["r"][0]) for _ in range(15)]
    assert sorted(states) == list(range(1, 16)), "the 4-bit LFSR visits all 15 non-zero states"
    lab.note = ("Two gates in a loop hold a bit, 480 flip-flops behind a decoder and two multiplexer trees make a "
                "register file, and a shift register with the right feedback counts through every state but zero.")

    fig, ax = labs.figure(2, size=(11, 4.2))
    t = np.arange(len(prog) + 1)
    for k, (name, color) in enumerate((("Qn", labs.PURPLE), ("Q", labs.GOLD), ("R_", labs.BLUE), ("S_", labs.BLUE))):
        ax[0].step(t, np.array(h[name] + h[name][-1:]) * 0.7 + k, where="post", color=color)
    ax[0].set_yticks([0.35, 1.35, 2.35, 3.35], ["Q̄", "Q", "R̄", "S̄"])
    for x, text in ((3, "set"), (7, "hold"), (12, "reset"), (16, "hold"), (21, "both"), (25, "released")):
        ax[0].axvline(x, color=labs.GRID, lw=1)
        ax[0].text(x + 0.2, 3.95, text, color=labs.MUTED, fontsize=8, va="top")
    ax[0].set(title="An SR latch of two NANDs, tick by tick", xlabel="time (gate delays)", ylim=(-0.2, 4.05))
    ax[0].grid(False)
    ax[1].bar(np.arange(len(periods8)), sorted(periods8), color=[labs.GREEN if p == 255 else labs.BLUE for p in sorted(periods8)], width=1.0)
    ax[1].axhline(255, color=labs.MUTED, ls="--", lw=1)
    ax[1].set(title=f"Degree 8: periods of all 128 polynomials ({maximal[-1]} reach 255)", xlabel="polynomial (sorted by period)",
              ylabel="period from state 1")
    ax[1].set_axisbelow(True)
    lab.fig = fig
    return lab
