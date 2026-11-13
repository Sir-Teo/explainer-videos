"""Lab 3: build a random truth table from gates, rewrite it in NAND alone, and count what parity costs in two levels."""

import numpy as np

from videos.coursekit import labs
from explainer.cs.pebble import hdl, logic
from explainer.cs.pebble.blocks import tree

TITLE = "One gate is enough, and what two levels cost"
GOAL = ("Minimize a random five-input truth table with Quine-McCluskey, build it as a netlist, rewrite the netlist "
        "in NAND gates alone and check both on all 32 inputs. Then search for the fewest NANDs for each two-input "
        "function, and compare parity as a sum of products with parity as a tree of XORs.")
TASKS = [
    "Replace the random table by majority of five inputs. How many prime implicants does it have, and how many gates?",
    "Change the search to NOR gates (out = ~(a | b)). Which function now needs five gates instead of four?",
    "Rewrite the XOR tree with to_nand() and compare its gate count and depth with the sum of products for n = 8.",
]
NAMES = {0b0110: "XOR", 0b1001: "XNOR", 0b1000: "AND", 0b1110: "OR", 0b0111: "NAND", 0b0001: "NOR", 0b0011: "NOT x",
         0b0101: "NOT y", 0b1100: "x", 0b1010: "y", 0b0000: "0", 0b1111: "1", 0b0100: "x AND NOT y",
         0b0010: "y AND NOT x", 0b1101: "x OR NOT y", 0b1011: "y OR NOT x"}


def table_of(c, n):
    """The circuit's output on all 2^n inputs, as an array of 0/1 (input pattern p sets variable j to bit j of p)."""
    return hdl.unpack(c.evaluate(hdl.exhaustive(c))["f"][0], 1 << n)


def sum_of_products(on, n):
    """The minimized sum of products of the function that is 1 on the minterms ``on``: (circuit, product terms)."""
    c = hdl.Circuit("sum of products")
    xs = c.input("x", n)
    terms = logic.min_cover(set(on), set(), n)
    c.output("f", logic.sop(c, terms, logic.Literals(c, xs)))
    return c, terms


def fewest_nands(max_gates=5):
    """Breadth-first search over sets of wire functions: the fewest NAND gates for each two-input function."""
    x, y = 0b1100, 0b1010  # bit 2x + y of a 4-bit table is the value at (x, y)
    best = {x: 0, y: 0}
    frontier = {(y, x)}
    for g in range(1, max_gates + 1):
        nxt = set()
        for wires in frontier:
            for i, a in enumerate(wires):
                for b in wires[i:]:
                    out = ~(a & b) & 0b1111
                    if out not in wires:
                        nxt.add(tuple(sorted(wires + (out,))))
                        best.setdefault(out, g)
        frontier = nxt
    return best


def run(seed=0):
    rng = np.random.default_rng(seed)
    lab = labs.Lab()

    # 1. a random function of five inputs: truth table -> minimized sum of products -> NAND only
    n = 5
    truth = rng.integers(0, 2, 1 << n)
    c, terms = sum_of_products(np.flatnonzero(truth), n)
    nand = c.to_nand()
    lab.row("random 5-input function", f"{int(truth.sum())} ones in its table, {len(terms)} product terms after minimizing")
    lab.row("as AND, OR, NOT", f"{c.size()} gates, depth {c.depth()}")
    lab.row("rewritten in NAND alone", f"{nand.size()} gates, depth {nand.depth()}")
    assert np.array_equal(table_of(c, n), truth), "the sum of products is the function"
    assert set(nand.counts()) == {"NAND"} and np.array_equal(table_of(nand, n), truth), "and so is the NAND rewrite"

    # 2. the fewest NANDs for each of the sixteen two-input functions
    best = fewest_nands()
    lab.row("two-input functions reached with at most 5 NANDs", f"{len(best)} of 16")
    lab.row("fewest NANDs", f"NOT {best[0b0011]}, AND {best[0b1000]}, OR {best[0b1110]}, XOR {best[0b0110]}, XNOR {best[0b1001]}"
                            "   (the film: XOR 4, XNOR 5)")
    assert len(best) == 16 and (best[0b0011], best[0b1000], best[0b1110], best[0b0110], best[0b1001]) == (1, 2, 3, 4, 5)

    # 3. parity: 2^(n-1) product terms in two levels, n - 1 XOR gates in a tree
    ns = list(range(2, 9))
    sop_gates, xor_gates = [], []
    for k in ns:
        odd = [m for m in range(1 << k) if m.bit_count() % 2]
        terms = sorted(logic.prime_implicants(set(odd), set(), k))  # Quine-McCluskey's merging rounds
        assert len(terms) == 2 ** (k - 1) and all(mask == 0 for _, mask in terms), "no two minterms of parity merge"
        flat = hdl.Circuit("parity, sum of products")
        flat.output("f", logic.sop(flat, terms, logic.Literals(flat, flat.input("x", k))))
        t = hdl.Circuit("parity, xor tree")
        t.output("f", tree(t, t.xor, t.input("x", k)))
        assert t.size() == k - 1 and np.array_equal(table_of(flat, k), table_of(t, k))
        sop_gates.append(flat.size())
        xor_gates.append(t.size())
    lab.row("parity of 8 inputs, sum of products", f"{2 ** 7} terms (2^(n-1)), {sop_gates[-1]} gates, depth {flat.depth()}")
    lab.row("parity of 8 inputs, XOR tree", f"{xor_gates[-1]} gates (n - 1), depth {t.depth()}")
    lab.note = ("Any truth table can be built from NAND alone, but the recipe that proves it, the sum of products, "
                "is exponentially wasteful for parity; nobody knows a function in NP that provably needs more than "
                "a small multiple of n gates.")

    fig, ax = labs.figure(2, size=(11, 4.2))
    ax[0].semilogy(ns, sop_gates, "o-", color=labs.RED, label="sum of products (2 levels)")
    ax[0].semilogy(ns, xor_gates, "o-", color=labs.GREEN, label="tree of XOR gates")
    ax[0].semilogy(ns, [2 ** (k - 1) for k in ns], "--", color=labs.MUTED, label="2^(n-1) product terms")
    ax[0].set(title="Parity of n inputs: gates needed", xlabel="n", ylabel="gates")
    ax[0].legend()
    order = sorted(best, key=lambda f: (best[f], NAMES[f]))
    ax[1].barh([NAMES[f] for f in order], [best[f] for f in order], color=[labs.GOLD if NAMES[f] in ("XOR", "XNOR") else labs.BLUE for f in order])
    ax[1].invert_yaxis()
    ax[1].set(title="Fewest NAND gates for each two-input function", xlabel="NAND gates")
    ax[1].tick_params(axis="y", labelsize=8)
    ax[1].set_axisbelow(True)
    lab.fig = fig
    return lab
