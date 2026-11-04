"""Object files, a linker and a loader for Pebble-32 (Part 11).

    a = assemble_object(MAIN_S, "main.o")      # sections, symbols, relocations
    b = assemble_object(LIB_S, "lib.o")
    exe = link([a, b])                         # resolve symbols, lay out sections, patch relocations
    m = load(exe, argv=["job", "pride.txt"])   # a Machine with the image placed, sp set, argv on the stack

An object file has three sections, ``.text`` (code), ``.data`` (initialised data) and ``.bss`` (zeroed data, which
takes no space in the file), a symbol table, and relocations: the places where the assembler had to leave a hole
because the address was not known yet.  Three kinds, one for each way a Pebble instruction can hold an address:

    hi_lo   ``la rd, sym`` / ``li rd, sym``: ``lui`` takes the top 22 bits of the address, ``ori`` the low 10
    pc22    ``call sym`` / ``j sym`` / ``jal sym`` to a symbol in another section or file: a 22-bit word offset
    abs32   ``.word sym``: a whole 32-bit address in data

Symbols are local unless declared ``.globl`` (a *strong* global) or ``.weak``.  The linker's rules are the ELF ones
(Part 11 shows them on screen): two strong definitions of one name are an error; a strong one beats any number of
weak ones; with only weak ones, the first is chosen; a name used but defined nowhere is an error.  Sections are laid
out text first (all files' text in command-line order), then data, then bss, each aligned to 16 bytes; the entry
point is the global ``_start``.
"""

from __future__ import annotations

import re
from dataclasses import dataclass, field

from .asm import AsmError, _Asm, _li_parts
from .emu import Machine
from .isa import Instr, encode

SECTIONS = (".text", ".data", ".bss")


class LinkError(ValueError):
    pass


@dataclass
class Reloc:
    section: str
    offset: int
    kind: str  # hi_lo, pc22, abs32
    symbol: str
    addend: int = 0


@dataclass
class Symbol:
    name: str
    section: str | None  # None: undefined here
    offset: int = 0
    binding: str = "local"  # local, global, weak


@dataclass
class ObjectFile:
    name: str
    sections: dict[str, bytes]
    bss_size: int
    symbols: dict[str, Symbol]
    relocs: list[Reloc]
    source: str = ""

    def defined(self):
        return {n: s for n, s in self.symbols.items() if s.section is not None}

    def undefined(self):
        return sorted({r.symbol for r in self.relocs if r.symbol not in self.defined()})


class _ObjAsm(_Asm):
    """The Part 6 assembler, one section at a time, leaving holes (relocations) for addresses it cannot know."""

    def __init__(self, text: str, section: str, local: set[str]):
        super().__init__(text)
        self.section = section
        self.local = local  # labels defined in this section (position-independent within it)
        self.relocs: list[Reloc] = []
        self.pc = 0

    def _symbolic(self, s: str) -> bool:
        s = s.strip()
        return bool(re.fullmatch(r"[A-Za-z_.][\w.]*", s)) and s not in self.consts

    def expand(self, op, args, ln, pc):
        if op in ("li", "la") and self._symbolic(args[1]):
            self.relocs.append(Reloc(self.section, pc, "hi_lo", args[1].strip()))
            return super().expand(op, [args[0], "0"], ln, pc)
        if op in ("call", "j") or (op == "jal" and len(args) == 1):
            target = args[0].strip()
            if target not in self.local:
                self.relocs.append(Reloc(self.section, pc, "pc22", target))
                return [Instr("jal", rd=0 if op == "j" else 1, imm=0)]
        return super().expand(op, args, ln, pc)


def _split_sections(text: str):
    """Source lines by section, and the global and weak declarations."""
    cur = ".text"
    parts = {s: [] for s in SECTIONS}
    glob, weak = set(), set()
    for raw in text.splitlines():
        s = raw.split("#")[0].strip()
        low = s.lower()
        if low in SECTIONS or low in (".section .text", ".section .data", ".section .bss"):
            cur = low.split()[-1]
            parts[cur].append("")
            continue
        m = re.match(r"\.(globl|global|weak)\s+(.+)$", s)
        if m:
            names = [x.strip() for x in m.group(2).split(",")]
            (weak if m.group(1) == "weak" else glob).update(names)
            parts[cur].append("")
            continue
        parts[cur].append(raw)
    return parts, glob, weak


def assemble_object(text: str, name: str = "a.o") -> ObjectFile:
    parts, glob, weak = _split_sections(text)
    sections, symbols, relocs = {}, {}, []
    bss = 0
    for sec in SECTIONS:
        src = "\n".join(parts[sec])
        # labels of this section, from a first pass that tolerates unknown symbols
        probe = _ObjAsm(src, sec, set())
        probe.pass1()
        local = set(probe.labels)
        a = _ObjAsm(src, sec, local)
        a.pass1()
        if sec == ".bss":
            size = 0
            for ln, labels, op, args, _ in a.parse():
                if op is None:
                    continue
                if op not in (".space", ".align"):
                    raise AsmError(f"{name}: .bss holds only .space and .align")
                size += a.directive_size(op, args, size, ln)
            bss = size
            sections[sec] = b""
        else:
            prog = _pass2_with_holes(a, name)
            sections[sec] = prog
            relocs += a.relocs
        for lab, off in a.labels.items():
            binding = "weak" if lab in weak else ("global" if lab in glob else "local")
            if lab in symbols:
                raise AsmError(f"{name}: {lab!r} defined in two sections")
            symbols[lab] = Symbol(lab, sec, off, binding)
    for n in glob | weak:
        if n not in symbols:
            symbols[n] = Symbol(n, None, 0, "weak" if n in weak else "global")
    for r in relocs:
        if r.symbol not in symbols:
            symbols[r.symbol] = Symbol(r.symbol, None, 0, "global")
    return ObjectFile(name, sections, bss, symbols, relocs, text)


def _pass2_with_holes(a: _ObjAsm, name: str) -> bytes:
    """pass2, but a ``.word`` of a symbol, or any use of a label from another section, becomes a relocation."""
    out = bytearray()
    for ln, _, op, args, raw in a.parse():
        if op is None or op == ".equ":
            continue
        addr = len(out)
        if op == ".word":
            for k, arg in enumerate(args):
                s = arg.strip()
                if a._symbolic(s):
                    a.relocs.append(Reloc(a.section, addr + 4 * k, "abs32", s))
                    out += bytes(4)
                else:
                    out += (a.value(s, ln) & 0xFFFF_FFFF).to_bytes(4, "little")
            continue
        if op.startswith("."):
            if op == ".byte":
                out += bytes(a.value(x, ln) & 0xFF for x in args)
            elif op in (".ascii", ".asciiz"):
                import ast

                out += ast.literal_eval(args[0]).encode("latin-1") + (b"\0" if op == ".asciiz" else b"")
            else:
                out += bytes(a.directive_size(op, args, addr, ln))
            continue
        try:
            for ins in a.expand(op, args, ln, addr):
                out += encode(ins).to_bytes(4, "little")
        except AsmError as e:
            raise AsmError(f"{name}: {e}") from None
    return bytes(out)


# ---------------------------------------------------------------------------
# linking
# ---------------------------------------------------------------------------
@dataclass
class Executable:
    image: bytes
    entry: int
    symbols: dict[str, int]
    layout: list[tuple[str, str, int, int]]  # (file, section, start, size)
    bss: tuple[int, int]
    patches: list[dict] = field(default_factory=list)  # every relocation applied: for the animation
    resolution: dict[str, str] = field(default_factory=dict)  # global name -> the file whose definition won


def _align(x: int, a: int = 16) -> int:
    return (x + a - 1) // a * a


def resolve(objs: list[ObjectFile]) -> dict[str, tuple[ObjectFile, Symbol]]:
    """The global symbol table, by the strong/weak rules; raises LinkError for duplicates and undefined names."""
    table: dict[str, tuple[ObjectFile, Symbol]] = {}
    for o in objs:
        for s in o.defined().values():
            if s.binding == "local":
                continue
            if s.name in table:
                _, old = table[s.name]
                if old.binding == "global" and s.binding == "global":
                    raise LinkError(f"duplicate symbol {s.name!r}: defined in {table[s.name][0].name} and {o.name}")
                if old.binding == "weak" and s.binding == "global":
                    table[s.name] = (o, s)
            else:
                table[s.name] = (o, s)
    for o in objs:
        for name in o.undefined():
            if name not in table:
                raise LinkError(f"undefined reference to {name!r} in {o.name}")
    return table


def link(objs: list[ObjectFile], base: int = 0, entry: str = "_start") -> Executable:
    table = resolve(objs)
    place: dict[tuple[str, str], int] = {}
    layout = []
    addr = base
    for sec in (".text", ".data"):
        for o in objs:
            addr = _align(addr)
            place[(o.name, sec)] = addr
            layout.append((o.name, sec, addr, len(o.sections[sec])))
            addr += len(o.sections[sec])
    image_end = addr
    bss_start = addr = _align(addr)
    for o in objs:
        addr = _align(addr)
        place[(o.name, ".bss")] = addr
        layout.append((o.name, ".bss", addr, o.bss_size))
        addr += o.bss_size
    bss_end = addr
    img = bytearray(image_end - base)
    for o in objs:
        for sec in (".text", ".data"):
            st = place[(o.name, sec)] - base
            img[st:st + len(o.sections[sec])] = o.sections[sec]

    def address(o: ObjectFile, name: str) -> int:
        s = o.symbols.get(name)
        if s is not None and s.section is not None and s.binding == "local":
            return place[(o.name, s.section)] + s.offset
        if name in table:
            fo, fs = table[name]
            return place[(fo.name, fs.section)] + fs.offset
        if s is not None and s.section is not None:
            return place[(o.name, s.section)] + s.offset
        raise LinkError(f"undefined reference to {name!r} in {o.name}")

    patches = []
    for o in objs:
        for r in o.relocs:
            at = place[(o.name, r.section)] + r.offset
            target = address(o, r.symbol) + r.addend
            i = at - base
            if r.kind == "abs32":
                img[i:i + 4] = (target & 0xFFFF_FFFF).to_bytes(4, "little")
            elif r.kind == "hi_lo":
                hi, lo = _li_parts(target)
                lui = int.from_bytes(img[i:i + 4], "little")
                ori = int.from_bytes(img[i + 4:i + 8], "little")
                lui = (lui & ~0x3FFFFF) | (hi & 0x3FFFFF)
                ori = (ori & ~0x3FFFF) | (lo & 0x3FFFF)
                img[i:i + 4] = lui.to_bytes(4, "little")
                img[i + 4:i + 8] = ori.to_bytes(4, "little")
            elif r.kind == "pc22":
                d = target - at
                if d % 4 or not -(1 << 21) <= d // 4 < (1 << 21):
                    raise LinkError(f"{o.name}: call to {r.symbol!r} out of range")
                w = int.from_bytes(img[i:i + 4], "little")
                w = (w & ~0x3FFFFF) | ((d // 4) & 0x3FFFFF)
                img[i:i + 4] = w.to_bytes(4, "little")
            patches.append({"file": o.name, "section": r.section, "at": at, "kind": r.kind, "symbol": r.symbol,
                            "target": target})
    syms = {n: address(fo, n) for n, (fo, _) in table.items()}
    if entry not in syms:
        raise LinkError(f"no entry point {entry!r}")
    return Executable(bytes(img), syms[entry], syms, layout, (bss_start, bss_end), patches,
                      {n: fo.name for n, (fo, _) in table.items()})


def load(exe: Executable, argv: list[str] = (), tape: bytes = b"", mem_size: int = 1 << 20) -> Machine:
    """A Machine ready to run ``exe``: the image placed, bss zeroed, pc at the entry point, and argv on the stack in
    the System V way (strings at the top, then the pointer array, then argc), with a0 = argc and a1 = argv."""
    m = Machine(image=exe.image, tape=tape, mem_size=mem_size)
    m.pc = exe.entry
    sp = mem_size
    ptrs = []
    for a in reversed(list(argv)):
        b = a.encode() + b"\0"
        sp -= len(b)
        m.mem[sp:sp + len(b)] = b
        ptrs.append(sp)
    ptrs.reverse()
    sp &= ~3
    sp -= 4 * (len(ptrs) + 1)  # argv[], NULL-terminated
    for k, p in enumerate(ptrs + [0]):
        m.mem[sp + 4 * k:sp + 4 * k + 4] = p.to_bytes(4, "little")
    argv_at = sp
    sp -= 4
    m.mem[sp:sp + 4] = len(ptrs).to_bytes(4, "little")
    sp &= ~15
    m.regs[2] = sp
    m.regs[3] = len(ptrs)
    m.regs[4] = argv_at
    return m
