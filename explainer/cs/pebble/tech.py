"""One technology for every timing in the series, so that ledger rows compare like with like.

Part 5 set the gate delay and flip-flop overheads, Part 6 measured the single-cycle netlist, and memories take a
nanosecond per access (an SRAM of tens of kilobytes; Part 9 makes the hierarchy).  Every later machine, pipelined
(Part 7), out of order (Part 8), with caches (Part 9), is timed with these same numbers.
"""

from __future__ import annotations

GATE_PS = 10.0  # one gate delay (Part 5)
T_CQ_PS = 40.0  # clock-to-Q (Part 5)
T_SETUP_PS = 30.0  # setup (Part 5)
FF_PS = T_CQ_PS + T_SETUP_PS
MEM_PS = 1000.0  # one memory access
SINGLE_CYCLE_LOGIC_GATES = 56  # the settled critical path of Part 6's netlist (videos/cs/cs6 compute "cpu")


def single_cycle_period_ps(logic_gates: int = SINGLE_CYCLE_LOGIC_GATES) -> float:
    """Instruction fetch, the logic, and a data access, all inside one cycle (Part 6, problem 3)."""
    return 2 * MEM_PS + logic_gates * GATE_PS + FF_PS


def mhz(period_ps: float) -> float:
    return 1e6 / period_ps
