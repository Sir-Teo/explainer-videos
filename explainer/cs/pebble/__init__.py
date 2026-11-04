"""Pebble: the computer *Computer Science, Built* builds, one layer per part (videos/cs/SYLLABUS.md, 2.1).

* :mod:`.hdl`: netlists and a bit-parallel gate simulator (Part 3);
* :mod:`.isa`: the Pebble-32 instruction set, its encodings and disassembly (Part 6);
* :mod:`.emu`: the fast instruction-level emulator (Part 6), the reference every later layer is checked against;
* :mod:`.asm`: the two-pass assembler (Part 6).
"""

from .asm import AsmError, Program, assemble  # noqa: F401
from .emu import Machine, MachineError, run  # noqa: F401
from .isa import Instr, decode, disasm, encode, fields  # noqa: F401
