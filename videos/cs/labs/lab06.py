"""Lab 6: assemble programs for Pebble, run them on the emulator, and predict the Job's cycle count before running it."""

import math

import numpy as np

from videos.coursekit import labs
from explainer.cs import turing
from explainer.cs.pebble import asm, cpu, emu, hdl, programs

TITLE = "Programs on Pebble: Euclid, a Turing machine, and the Job, version 0"
GOAL = ("Assemble Euclid's algorithm and run it on random pairs; run the 3- and 4-state busy beavers on a "
        "Turing-machine interpreter written in Pebble assembly; count words in random passages with the Job, "
        "version 0, and compare its cycle count with the exact formula; and check both control units against the "
        "truth table they implement.")
TASKS = [
    "Replace Euclid's repeated subtraction by the rem instruction and compare the instruction counts on the same pairs.",
    "Double VOCAB and rerun. Which term of the Job's cycle formula grows, and why does a linear search make it quadratic?",
    "Assemble programs.SELFMOD, run it with trace=True, and find the store in m.log that rewrites an instruction.",
]
VOCAB = 300

EUCLID = """
        li   a0, {a}
        li   a1, {b}
loop:   beqz a1, done        # b = 0? stop
mod:    bltu a0, a1, swap    # a < b? swap
        sub  a0, a0, a1      # a = a - b
        j    mod
swap:   mv   t0, a0          # a, b = b, a
        mv   a0, a1
        mv   a1, t0
        j    loop
done:   halt                 # a0 = gcd
"""


def passage(rng, words, n):
    """n words drawn from a made-up vocabulary (frequencies falling like 1 / sqrt(rank)), some capitalized, with
    punctuation."""
    p = 1 / np.sqrt(np.arange(1, len(words) + 1))
    out = []
    for i in rng.choice(len(words), n, p=p / p.sum()):
        w = words[i]
        out.append((w.capitalize() if rng.random() < 0.1 else w) + (", " if rng.random() < 0.1 else " "))
    return "".join(out)


def run(seed=0):
    rng = np.random.default_rng(seed)
    lab = labs.Lab()

    # 1. Euclid in Pebble's machine language
    m = emu.run(asm.assemble(EUCLID.format(a=1071, b=462)), trace=True, mem_size=4096)
    lab.row("Euclid on Pebble: gcd(1071, 462)", f"{m.regs[3]} after {m.steps} instructions   (the rectangle of Part 1: 21)")
    assert m.regs[3] == 21
    regs, a0, a1 = [0] * 16, [], []
    for s in m.log:  # the two registers after every instruction, for the figure
        if s.reg:
            regs[s.reg[0]] = s.reg[1]
        a0.append(regs[3])
        a1.append(regs[4])
    pairs = rng.integers(1, 2000, (40, 2))
    for a, b in pairs:
        assert emu.run(asm.assemble(EUCLID.format(a=a, b=b)), mem_size=4096).regs[3] == math.gcd(int(a), int(b))
    lab.row("40 random pairs below 2000", "all equal to math.gcd")

    # 2. a Turing machine on Pebble: Part 1's loop closed
    for n in (3, 4):
        table, steps, ones, _, _ = turing.CHAMPIONS[n]
        t = emu.run(asm.assemble(programs.tm_program(turing.TM.parse(table))))
        lab.row(f"{n}-state busy beaver, interpreted on Pebble", f"{t.regs[3]} steps, {t.regs[4]} ones, {t.steps:,} Pebble instructions")
        assert (t.regs[3], t.regs[4]) == (steps, ones)

    # 3. the Job, version 0: right answer, and a cycle count known before it runs
    job = asm.assemble(programs.JOB_V0)
    letters = "abcdefghijklmnopqrstuvwxyz"
    words = sorted({"".join(rng.choice(list(letters), rng.integers(2, 9))) for _ in range(VOCAB)})
    sizes, cycles, formula = [], [], []
    for n in (60, 125, 250, 500, 1000):
        tape = programs.job_tape(passage(rng, words, n))
        r = emu.run(job, tape=tape)
        f = programs.job_features(tape)
        assert bytes(r.output) == programs.job_reference(tape), "the twenty most common words, with their counts"
        assert r.steps == programs.job_cycles(f), "the formula is exact"
        sizes.append(len(tape))
        cycles.append(r.steps)
        formula.append(programs.job_cycles(f))
    lab.row(f"the Job on {sizes[-1]:,} bytes", f"{cycles[-1]:,} cycles on the emulator, {formula[-1]:,} by the formula")
    lab.row("cycles per byte", f"{cycles[0] / sizes[0]:.0f} at {sizes[0]} bytes, {cycles[-1] / sizes[-1]:.0f} at {sizes[-1]:,}"
                               "   (thirty novels: 4,279)")
    assert cycles[-1] / sizes[-1] > 1.5 * cycles[0] / sizes[0], "the linear search makes the cost per byte grow"

    # 4. the control unit, two ways, against its truth table
    table = cpu.control_table()
    gates = {}
    for style in ("table", "minimized"):
        c = hdl.Circuit("control")
        out, _ = cpu.build_control(c, c.input("op", 6), style)
        for name, wire in out.items():
            c.output(name, wire)
        got = {k: hdl.unpack(v[0], 64) for k, v in c.evaluate(hdl.exhaustive(c)).items()}
        for code in range(64):
            assert got["ill"][code] == (code not in table)
            assert all(got[s][code] == table[code][s] for s in cpu.SIGNALS if code in table), (style, code)
        gates[style] = c.size()
    whole = cpu.build_cpu("table")
    lab.row("control unit", f"{len(table)} opcodes x {len(cpu.SIGNALS)} signals: {gates['table']} gates as a table, "
                            f"{gates['minimized']} minimized   (the film: 307 and 205)")
    lab.row("the whole CPU", f"{whole.c.size():,} gates and {whole.flip_flops} flip-flops   (the film: 8,224 and 512)")
    assert (len(table), len(cpu.SIGNALS)) == (34, 20) and (gates["table"], gates["minimized"]) == (307, 205)
    assert (whole.c.size(), whole.flip_flops) == (8224, 512)
    lab.note = ("A program is numbers in memory: the same machine runs Euclid, imitates a Turing machine and counts "
                "words, and because every path through the Job costs a fixed number of instructions its running "
                "time can be computed from the text alone.")

    fig, ax = labs.figure(2, size=(11, 4.2))
    t = np.arange(1, len(a0) + 1)
    ax[0].step(t, a0, where="post", color=labs.BLUE, label="a0")
    ax[0].step(t, a1, where="post", color=labs.GOLD, label="a1")
    ax[0].set(title="Euclid on Pebble: gcd(1071, 462), register by register", xlabel="instructions executed", ylabel="register value")
    ax[0].legend()
    ax[1].plot(sizes, np.array(cycles) / np.array(sizes), "o", ms=8, color=labs.BLUE, label="emulator")
    ax[1].plot(sizes, np.array(formula) / np.array(sizes), "-", color=labs.GOLD, label="formula from the text alone")
    ax[1].set(title="The Job, version 0: cycles per byte of text", xlabel="bytes on the tape", ylabel="cycles per byte", ylim=(0, None))
    ax[1].legend()
    lab.fig = fig
    return lab
