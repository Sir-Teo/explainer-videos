"""Circuits that remember: feedback, latches, flip-flops, registers and state machines (built on screen in Part 5,
"Memory and Time").

Two simulators:

``Loop``  a gate network that may contain feedback (an SR latch, a ring oscillator), simulated with unit gate
          delays: at each tick every gate recomputes from the values of the tick before.  This is the level at
          which latches can be seen to hold, race and oscillate.

``Seq``   a synchronous circuit: combinational logic (an ``hdl.Circuit``) plus edge-triggered registers.  At each
          clock edge every register loads its D input at once.  Registers are pseudo-inputs of the circuit (their
          Q) and pseudo-outputs (their D), so all of Part 3 and 4's netlist machinery applies to the logic between
          them; ``run`` is bit-parallel over many independent copies.

    rf = register_file(nregs=8, width=8)          # 2 read ports, 1 write port
    rf.step({"we": 1, "wa": 3, "wd": 77, "ra": 3, "rb": 0})
"""

from __future__ import annotations

from dataclasses import dataclass, field

import numpy as np

from .blocks import mux2, tree
from .hdl import Circuit, simulate

GATES = {
    "NAND": lambda a, b: 1 - (a & b), "NOR": lambda a, b: 1 - (a | b), "AND": lambda a, b: a & b,
    "OR": lambda a, b: a | b, "XOR": lambda a, b: a ^ b, "NOT": lambda a: 1 - a, "BUF": lambda a: a,
}


@dataclass
class Loop:
    """A gate network with feedback.  Gates refer to each other (and to inputs) by name, in any order."""
    gates: dict[str, tuple] = field(default_factory=dict)
    inputs: list[str] = field(default_factory=list)

    def input(self, name: str) -> str:
        self.inputs.append(name)
        return name

    def gate(self, name: str, kind: str, *ins: str) -> str:
        self.gates[name] = (kind, ins)
        return name

    def run(self, drive, steps: int, init: dict | None = None) -> dict[str, list[int]]:
        """``drive(t)`` gives the input values at tick t.  Every gate's output at tick t + 1 is its function of the
        values at tick t (one unit of delay).  Returns the history of every signal."""
        val = {g: 0 for g in self.gates}
        val.update(init or {})
        hist = {n: [] for n in list(self.inputs) + list(self.gates)}
        for t in range(steps):
            val.update(drive(t))
            for n in hist:
                hist[n].append(int(val[n]))
            new = {g: GATES[k](*[val[i] for i in ins]) for g, (k, ins) in self.gates.items()}
            val.update(new)
        return hist


def sr_latch() -> Loop:
    """Two cross-coupled NANDs.  Inputs are active low: S̄ = 0 sets Q, R̄ = 0 resets it, both 1 holds."""
    n = Loop()
    n.input("S_")
    n.input("R_")
    n.gate("Q", "NAND", "S_", "Qn")
    n.gate("Qn", "NAND", "R_", "Q")
    return n


def ring(k: int = 3) -> Loop:
    """k inverters in a ring: for odd k there is no stable state, and it oscillates with period 2k."""
    n = Loop()
    for i in range(k):
        n.gate(f"x{i}", "NOT", f"x{(i - 1) % k}")
    return n


def d_latch() -> Loop:
    """A D latch: transparent while E = 1 (Q follows D), holding while E = 0.  An SR latch whose S̄ and R̄ come from
    D and E through two NANDs, so the forbidden input can never occur."""
    n = Loop()
    n.input("D")
    n.input("E")
    n.gate("Dn", "NOT", "D")
    n.gate("S_", "NAND", "D", "E")
    n.gate("R_", "NAND", "Dn", "E")
    n.gate("Q", "NAND", "S_", "Qn")
    n.gate("Qn", "NAND", "R_", "Q")
    return n


MS_INIT = {"Cn": 1, "Dn": 1, "mS": 1, "mR": 0, "M": 0, "Mn": 1, "sS": 1, "sR": 1, "Q": 0, "Qn": 1}  # D = 0, C = 0


def master_slave() -> Loop:
    """An edge-triggered D flip-flop: a master latch open while the clock is low, a slave open while it is high, so
    Q takes the value D had at the rising edge and holds it for the whole cycle.  Start it from ``MS_INIT`` (a
    consistent state); D must be steady for a few gate delays before the edge (setup) or the master can oscillate:
    the unit-delay picture of metastability."""
    n = Loop()
    n.input("D")
    n.input("C")
    n.gate("Cn", "NOT", "C")
    n.gate("Dn", "NOT", "D")
    n.gate("mS", "NAND", "D", "Cn")
    n.gate("mR", "NAND", "Dn", "Cn")
    n.gate("M", "NAND", "mS", "Mn")
    n.gate("Mn", "NAND", "mR", "M")
    n.gate("sS", "NAND", "M", "C")
    n.gate("sR", "NAND", "Mn", "C")
    n.gate("Q", "NAND", "sS", "Qn")
    n.gate("Qn", "NAND", "sR", "Q")
    return n


# ---------------------------------------------------------------------------
# synchronous circuits
# ---------------------------------------------------------------------------
class Seq:
    """Combinational logic between edge-triggered registers.  Build the logic on ``self.c`` (an ``hdl.Circuit``):
    ``q = reg(name, width, init)`` returns the register's outputs as wires; ``set_next(name, wires)`` connects its
    D inputs; ``c.input`` and ``c.output`` are the circuit's own ports."""

    def __init__(self, name: str = "seq"):
        self.c = Circuit(name)
        self.regs: dict[str, tuple[int, int]] = {}   # name -> (width, init)
        self.state: dict[str, np.ndarray] = {}

    def reg(self, name: str, width: int = 1, init: int = 0):
        q = self.c.input("q:" + name, width)
        self.regs[name] = (width, init)
        return [q] if isinstance(q, int) else q

    def set_next(self, name: str, wires) -> None:
        self.c.output("d:" + name, wires)

    @property
    def flip_flops(self) -> int:
        return sum(w for w, _ in self.regs.values())

    def reset(self, copies: int = 1) -> None:
        self.state = {n: np.full(copies, init, dtype=np.int64) for n, (_, init) in self.regs.items()}

    def step(self, inputs: dict) -> dict[str, np.ndarray]:
        """One clock cycle for every copy at once: outputs computed from the current state and these inputs, then
        every register loads its next value."""
        if not self.state:
            self.reset(len(np.atleast_1d(next(iter(inputs.values())))) if inputs else 1)
        n = len(next(iter(self.state.values())))
        vals = {k: np.broadcast_to(np.asarray(v, dtype=np.int64), (n,)) for k, v in inputs.items()}
        vals.update({"q:" + k: v for k, v in self.state.items()})
        out = simulate(self.c, vals)
        for k in self.regs:
            self.state[k] = out.pop("d:" + k).astype(np.int64)
        return {k: v.astype(np.int64) for k, v in out.items()}

    def run(self, seq_inputs: list[dict]) -> list[dict]:
        return [self.step(x) for x in seq_inputs]


def counter(width: int = 4) -> Seq:
    """A binary counter: the register plus one, every cycle (a half-adder chain)."""
    s = Seq(f"{width}-bit counter")
    c = s.c
    q = s.reg("count", width)
    carry = c.const(1)
    nxt = []
    for b in q:
        nxt.append(c.xor(b, carry))
        carry = c.and_(b, carry)
    s.set_next("count", nxt)
    c.output("count", q)
    return s


def lfsr(taps: tuple[int, ...], width: int, init: int = 1) -> Seq:
    """A Fibonacci LFSR: shift left, feeding in the XOR of the tapped bits (bit positions, 0 = lowest)."""
    s = Seq(f"{width}-bit LFSR")
    c = s.c
    q = s.reg("r", width, init)
    fb = tree(c, c.xor, [q[t] for t in taps])
    s.set_next("r", [fb] + q[:-1])
    c.output("r", q)
    return s


def register_file(nregs: int = 16, width: int = 32, zero_reg: bool = True) -> Seq:
    """Pebble's register file: ``nregs`` registers of ``width`` bits, two read ports (``ra`` → ``a``, ``rb`` → ``b``)
    and one write port (``we``, ``wa``, ``wd``), written at the clock edge.  Register 0 always reads 0, as in
    Pebble's ISA.  Built from a decoder (which register to write), a multiplexer per register bit (load or keep), and
    two multiplexer trees (which register to read)."""
    k = (nregs - 1).bit_length()
    s = Seq(f"{nregs} x {width} register file")
    c = s.c
    we = c.input("we")
    wa = c.input("wa", k)
    wd = c.input("wd", width)
    ra = c.input("ra", k)
    rb = c.input("rb", k)
    wa, ra, rb = ([w] if isinstance(w, int) else w for w in (wa, ra, rb))
    wd = [wd] if isinstance(wd, int) else wd
    nwa = [c.not_(x) for x in wa]
    regs = []
    for r in range(nregs):
        if zero_reg and r == 0:
            regs.append(None)  # hard-wired zero: no flip-flops at all
            continue
        q = s.reg(f"r{r}", width)
        regs.append(q)
        sel = tree(c, c.and_, [wa[i] if (r >> i) & 1 else nwa[i] for i in range(k)] + [we])
        s.set_next(f"r{r}", [mux2(c, sel, q[i], wd[i]) for i in range(width)])

    def read(addr):
        zero = c.const(0)
        layer = [regs[r] if regs[r] is not None else [zero] * width for r in range(nregs)]
        for st in range(k):
            layer = [[mux2(c, addr[st], layer[2 * j][i], layer[2 * j + 1][i]) for i in range(width)]
                     for j in range(len(layer) // 2)]
        return layer[0]

    c.output("a", read(ra))
    c.output("b", read(rb))
    return s
