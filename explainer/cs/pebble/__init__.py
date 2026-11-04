"""Pebble: the computer *Computer Science, Built* builds, one layer per part (videos/cs/SYLLABUS.md, 2.1).

* :mod:`.hdl`: netlists and a bit-parallel gate simulator (Part 3);
* :mod:`.isa`: the Pebble-32 instruction set, its encodings and disassembly (Part 6);
* :mod:`.emu`: the fast instruction-level emulator (Part 6), the reference every later layer is checked against;
* :mod:`.asm`: the two-pass assembler (Part 6);
* :mod:`.seq`: latches, flip-flops, registers and the register file (Part 5);
* :mod:`.blocks`: adders, multipliers and the ALU as netlists (Part 4);
* :mod:`.logic`: Quine–McCluskey minimization (Parts 3, 5, 6);
* :mod:`.cpu`: the single-cycle CPU as one netlist, and ``GateMachine`` to run programs on it (Part 6);
* :mod:`.fast`: any netlist compiled to C, 64 copies per pass (Part 6);
* :mod:`.programs`, :mod:`.randprog`: Part 6's programs (the Job, version 0) and random test programs.
"""

from .asm import AsmError, Program, assemble  # noqa: F401
from .emu import Machine, MachineError, run  # noqa: F401
from .isa import Instr, decode, disasm, encode, fields  # noqa: F401
