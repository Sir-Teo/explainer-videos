"""Lab 55: build Thompson's trojan compiler, catch it by diverse double-compiling, and see when the catch fails."""

from videos.coursekit import labs  # noqa: I001  (must stay first: it lets explainer.cs import without manim)

import numpy as np

from explainer.cs.trust import memory, trojan

TITLE = "A trojan with no source, caught by a second compiler"
GOAL = ("Compile the clean compiler source with the trojaned binary and check that the trojan reproduces itself bit "
        "for bit, run diverse double-compiling with an independent compiler and with one that shares the trojan, "
        "and compare the tries an exploit needs against k bits of ASLR with the two closed forms.")
TASKS = [
    "Rename the parameter in a copy of trojan.CLEAN_LOGIN ('def login(pw):') and compile it with the trojaned binary. Is the backdoor inserted, and what does that say about how a trojan must recognise its target?",
    "Call trojan.build twice with normalize=False and different timestamps, then compare the hashes. Why does the bit-for-bit test of diverse double-compiling need normalize=True?",
    "Raise BITS from 6 to 8 and to 12 in the ASLR simulation. How do the two means move, and what does one more bit cost the attacker?",
]

BITS = memory.ASLR_DEMO_BITS
TRIALS = 20_000


def double_compile(suspect, stage1_of_second):
    """Wheeler's test by hand: Z = X(c), with X the second compiler's build of the clean source c, against A(c)."""
    z = trojan.run_compiler_binary(stage1_of_second, trojan.CLEAN_COMPILER)
    a2 = trojan.run_compiler_binary(trojan.run_compiler_binary(suspect, trojan.CLEAN_COMPILER), trojan.CLEAN_COMPILER)
    return z == a2, len(z), len(a2)


def run(seed=0):
    rng = np.random.default_rng(seed)
    lab = labs.Lab()

    # 1. Thompson's three stages: the trojan is in no source, and reproduces itself from clean source
    clean = trojan.clean_compile(trojan.CLEAN_COMPILER)
    troj = trojan.clean_compile(trojan.trojaned_compiler_source())
    rebuilt = trojan.run_compiler_binary(troj, trojan.CLEAN_COMPILER)          # clean source, trojaned binary
    honest = trojan.run_compiler_binary(clean, trojan.CLEAN_COMPILER)
    assert trojan.MAGIC not in trojan.CLEAN_COMPILER and trojan.MAGIC not in trojan.CLEAN_LOGIN
    assert rebuilt == troj and honest == clean and troj != clean, "both binaries are fixpoints, and they differ"
    lab.row("compiler binary from the clean source", f"{len(honest)} bytes by the clean binary, {len(rebuilt)} bytes "
            f"by the trojaned one (sha {trojan.sha(rebuilt)[:8]} = the trojaned binary's {trojan.sha(troj)[:8]})")
    logins = {name: trojan.run_compiler_binary(b, trojan.CLEAN_LOGIN) for name, b in (("clean", clean), ("trojaned", rebuilt))}
    guesses = ["".join(rng.choice(list("abcdefghijklmnopqrstuvwxyz-"), 12)) for _ in range(200)]
    for name, b in logins.items():
        magic, right = trojan.run_login(b, trojan.MAGIC), trojan.run_login(b, trojan.CORRECT)
        wrong = sum(trojan.run_login(b, g) for g in guesses)
        assert right and wrong == 0 and magic == (name == "trojaned")
        lab.row(f"login built by the {name} compiler", f"correct password {right}, magic password {magic}, "
                f"{wrong} of {len(guesses)} random guesses")

    # 2. diverse double-compiling: an independent second compiler catches it; one with the same trojan does not
    report = trojan.ddc_report()
    assert report["clean"]["match"] and not report["trojaned"]["match"]
    independent = trojan.trusted_compile(trojan.CLEAN_COMPILER)
    shared = trojan.run_compiler_binary(troj, trojan.CLEAN_COMPILER)           # the "second" compiler is trojaned too
    for label, suspect, second, expect in (("honest suspect, independent second compiler", clean, independent, True),
                                           ("trojaned suspect, independent second compiler", troj, independent, False),
                                           ("trojaned suspect, second compiler with the same trojan", troj, shared, True)):
        same, nz, na = double_compile(suspect, second)
        assert same == expect
        lab.row(f"DDC: {label}", f"Z is {nz} bytes, A(c) twice is {na} bytes: {'equal, reported clean' if same else 'differ, TROJAN DETECTED'}")

    # 3. ASLR: every placement tried on Pebble, then the two attack models against their closed forms
    aslr = memory.aslr_experiment(BITS)
    assert aslr["hit_count"] == 1 and aslr["measured_rate"] == 2.0 ** -BITS
    n = 2 ** BITS
    fresh = rng.geometric(1 / n, TRIALS)                                       # the layout is redrawn after every try
    sweep = rng.integers(1, n + 1, TRIALS)                                     # the layout is fixed: try each slot once
    assert abs(fresh.mean() / n - 1) < 0.04 and abs(sweep.mean() / ((n + 1) / 2) - 1) < 0.03
    lab.row(f"ASLR, {BITS} bits on Pebble", f"{aslr['hit_count']} of {aslr['placements']} placements run the shellcode (2^-{BITS})")
    lab.row("tries to the first hit, re-randomized", f"{fresh.mean():.1f}   (theory 2^k = {n})")
    lab.row("tries to the first hit, one sweep", f"{sweep.mean():.1f}   (theory (2^k + 1)/2 = {(n + 1) / 2})")
    lab.note = ("The trojaned binary is a fixpoint of compiling clean source, so no source shows it; a second compiler "
                "exposes it only if it does not carry the same trojan; each bit of ASLR doubles the attacker's work.")

    fig, ax = labs.figure(2, size=(11, 4.3))
    s1t = report["trojaned"]
    names = ["clean binary", "trojaned binary", "clean source by\nthe trojaned binary", "DDC stage 2,\nsuspect's line",
             "DDC stage 2,\nindependent line"]
    sizes = [len(clean), len(troj), len(rebuilt), s1t["stage2_suspect"]["size"], s1t["stage2_trusted"]["size"]]
    colors = [labs.GREEN, labs.RED, labs.RED, labs.RED, labs.GREEN]
    ax[0].bar(range(5), sizes, color=colors, width=0.62)
    for i, v in enumerate(sizes):
        ax[0].text(i, v + 20, f"{v}", ha="center", color=labs.INK, fontsize=9)
    ax[0].set_xticks(range(5), names, fontsize=7.5)
    ax[0].set(title="Compiler binaries: green honest, red carrying the trojan", ylabel="bytes", ylim=(0, max(sizes) * 1.15))
    ax[0].grid(axis="x", visible=False)
    bins = np.arange(0, 5 * n + 1, 8)
    ax[1].hist(fresh, bins=bins, density=True, color=labs.BLUE, alpha=0.65, label=f"re-randomized: mean {fresh.mean():.1f}")
    ax[1].hist(sweep, bins=bins, density=True, color=labs.GOLD, alpha=0.65, label=f"one sweep: mean {sweep.mean():.1f}")
    t = np.linspace(0, 5 * n, 200)
    ax[1].plot(t, np.exp(-t / n) / n, color=labs.INK, lw=1.2, ls="--", label="geometric law, mean 2^k")
    ax[1].set(title=f"Tries to the first hit against {BITS} bits of ASLR", xlabel="tries", ylabel="density", xlim=(0, 5 * n))
    ax[1].legend()
    lab.fig = fig
    return lab
