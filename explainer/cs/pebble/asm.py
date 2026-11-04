"""The Pebble-32 assembler: text to machine words, in two passes (Part 6 builds it on screen).

    prog = assemble('''
            li   a0, 10          # n
            li   a1, 0           # sum
    loop:   add  a1, a1, a0
            addi a0, a0, -1
            bnez a0, loop
            halt
    ''')
    prog.image, prog.labels, prog.listing

Pass 1 walks the lines, sizing every instruction and directive and recording where each label lands; pass 2 encodes,
now that every label has an address.  Comments start with ``#`` or ``;``.  Directives: ``.org addr``, ``.align n``,
``.word v, ...``, ``.byte v, ...``, ``.ascii "text"``, ``.asciiz "text"``, ``.space n``, ``.equ name, value``.
Pseudo-instructions, expanded here: ``nop mv li la not neg j jr call ret beqz bnez bltz bgez bgt ble bgtu bleu``.
"""

from __future__ import annotations

import ast
import re
from dataclasses import dataclass, field

from .isa import FORMAT, REG_NUM, Instr, encode, sext

PSEUDO = {"nop", "mv", "li", "la", "not", "neg", "j", "jr", "call", "ret", "beqz", "bnez", "bltz", "bgez", "bgt",
          "ble", "bgtu", "bleu"}


class AsmError(ValueError):
    pass


@dataclass
class Program:
    image: bytes
    labels: dict[str, int]
    listing: list[tuple[int, int, str]] = field(default_factory=list)  # (address, word, source line)
    source_lines: dict[int, int] = field(default_factory=dict)  # address -> source line number

    @property
    def addr_labels(self) -> dict[int, str]:
        return {v: k for k, v in self.labels.items()}


def _strip(line: str) -> str:
    out, q = [], False
    for ch in line:
        if ch == '"':
            q = not q
        if not q and ch in "#;":
            break
        out.append(ch)
    return "".join(out).strip()


def _split_args(s: str) -> list[str]:
    out, cur, q = [], "", False
    for ch in s:
        if ch == '"':
            q = not q
        if ch == "," and not q:
            out.append(cur.strip())
            cur = ""
        else:
            cur += ch
    if cur.strip():
        out.append(cur.strip())
    return out


def _li_parts(v: int) -> tuple[int, int]:
    """The (lui, ori) immediates that build the 32-bit constant v."""
    v &= 0xFFFF_FFFF
    return sext(v >> 10, 22), v & 0x3FF


def _size(op: str, args: list[str]) -> int:
    """Bytes an instruction or pseudo-instruction takes (known in pass 1, before labels have values)."""
    if op in ("li", "la"):
        return 8
    return 4


class _Asm:
    def __init__(self, text: str):
        self.lines = text.splitlines()
        self.labels: dict[str, int] = {}
        self.consts: dict[str, int] = {}

    # -- values -------------------------------------------------------------------
    def reg(self, s: str, ln: int) -> int:
        s = s.strip().lower()
        if s not in REG_NUM:
            raise AsmError(f"line {ln}: no register {s!r}")
        return REG_NUM[s]

    def value(self, s: str, ln: int) -> int:
        s = s.strip()
        if s in self.labels:
            return self.labels[s]
        if s in self.consts:
            return self.consts[s]
        if re.fullmatch(r"'(\\.|.)'", s):
            return ord(ast.literal_eval(s))
        m = re.fullmatch(r"([A-Za-z_.][\w.]*)\s*([+-])\s*(\w+)", s)
        if m and (m.group(1) in self.labels or m.group(1) in self.consts):
            base = self.value(m.group(1), ln)
            off = self.value(m.group(3), ln)
            return base + off if m.group(2) == "+" else base - off
        try:
            return int(s, 0)
        except ValueError:
            raise AsmError(f"line {ln}: unknown value {s!r}") from None

    def mem_arg(self, s: str, ln: int) -> tuple[int, int]:
        m = re.fullmatch(r"\s*(.*?)\s*\(\s*(\w+)\s*\)\s*", s)
        if not m:
            raise AsmError(f"line {ln}: expected offset(register), got {s!r}")
        return self.value(m.group(1) or "0", ln), self.reg(m.group(2), ln)

    # -- passes ---------------------------------------------------------------------
    def parse(self):
        """Yield (line number, label list, op, args, raw) for every line."""
        for ln, raw in enumerate(self.lines, 1):
            s = _strip(raw)
            labels = []
            while True:
                m = re.match(r"([A-Za-z_.][\w.]*)\s*:\s*", s)
                if not m:
                    break
                labels.append(m.group(1))
                s = s[m.end():]
            if not s:
                yield ln, labels, None, [], raw
                continue
            parts = s.split(None, 1)
            op = parts[0].lower()
            args = _split_args(parts[1]) if len(parts) > 1 else []
            yield ln, labels, op, args, raw

    def directive_size(self, op, args, addr, ln) -> int:
        if op == ".word":
            return 4 * len(args)
        if op == ".byte":
            return len(args)
        if op in (".ascii", ".asciiz"):
            return len(ast.literal_eval(args[0]).encode("latin-1")) + (op == ".asciiz")
        if op == ".space":
            return self.value(args[0], ln)
        if op == ".align":
            n = self.value(args[0], ln)
            return (-addr) % n
        if op == ".org":
            return self.value(args[0], ln) - addr
        if op == ".equ":
            return 0
        raise AsmError(f"line {ln}: unknown directive {op}")

    def pass1(self):
        addr = 0
        for ln, labels, op, args, _ in self.parse():
            for lab in labels:
                if lab in self.labels:
                    raise AsmError(f"line {ln}: label {lab!r} defined twice")
                self.labels[lab] = addr
            if op is None:
                continue
            if op == ".equ":
                self.consts[args[0]] = self.value(args[1], ln)
                continue
            if op.startswith("."):
                size = self.directive_size(op, args, addr, ln)
                if size < 0:
                    raise AsmError(f"line {ln}: .org goes backwards")
                addr += size
            else:
                if addr % 4:
                    raise AsmError(f"line {ln}: instruction at unaligned address {addr:#x} (use .align 4)")
                addr += _size(op, args)

    def expand(self, op, args, ln, pc) -> list[Instr]:
        """An instruction or pseudo-instruction as real instructions."""
        r, v = self.reg, self.value

        def off(label):
            d = v(label, ln) - pc
            if d % 4:
                raise AsmError(f"line {ln}: branch target not word-aligned")
            return d // 4

        if op == "nop":
            return [Instr("addi")]
        if op == "mv":
            return [Instr("addi", rd=r(args[0], ln), rs1=r(args[1], ln))]
        if op in ("li", "la"):
            hi, lo = _li_parts(v(args[1], ln))
            rd = r(args[0], ln)
            return [Instr("lui", rd=rd, imm=hi), Instr("ori", rd=rd, rs1=rd, imm=lo)]
        if op == "not":
            return [Instr("xori", rd=r(args[0], ln), rs1=r(args[1], ln), imm=-1)]
        if op == "neg":
            return [Instr("sub", rd=r(args[0], ln), rs2=r(args[1], ln))]
        if op == "j":
            return [Instr("jal", rd=0, imm=off(args[0]))]
        if op == "call":
            return [Instr("jal", rd=1, imm=off(args[0]))]
        if op == "jr":
            return [Instr("jalr", rd=0, rs1=r(args[0], ln))]
        if op == "ret":
            return [Instr("jalr", rd=0, rs1=1)]
        if op in ("beqz", "bnez", "bltz", "bgez"):
            real = {"beqz": "beq", "bnez": "bne", "bltz": "blt", "bgez": "bge"}[op]
            return [Instr(real, rs1=r(args[0], ln), rs2=0, imm=off(args[1]))]
        if op in ("bgt", "ble", "bgtu", "bleu"):
            real = {"bgt": "blt", "ble": "bge", "bgtu": "bltu", "bleu": "bgeu"}[op]
            return [Instr(real, rs1=r(args[1], ln), rs2=r(args[0], ln), imm=off(args[2]))]
        if op not in FORMAT:
            raise AsmError(f"line {ln}: unknown instruction {op!r}")
        f = FORMAT[op]
        if op == "halt":
            return [Instr("halt")]
        if f == "R":
            return [Instr(op, rd=r(args[0], ln), rs1=r(args[1], ln), rs2=r(args[2], ln))]
        if op in ("lw", "lb", "lbu"):
            imm, base = self.mem_arg(args[1], ln)
            return [Instr(op, rd=r(args[0], ln), rs1=base, imm=imm)]
        if op == "jalr":
            if len(args) == 1:
                return [Instr(op, rd=1, rs1=r(args[0], ln))]
            imm, base = self.mem_arg(args[1], ln)
            return [Instr(op, rd=r(args[0], ln), rs1=base, imm=imm)]
        if f == "I":
            return [Instr(op, rd=r(args[0], ln), rs1=r(args[1], ln), imm=v(args[2], ln))]
        if op in ("sw", "sb"):
            imm, base = self.mem_arg(args[1], ln)
            return [Instr(op, rs1=base, rs2=r(args[0], ln), imm=imm)]
        if f == "S":
            return [Instr(op, rs1=r(args[0], ln), rs2=r(args[1], ln), imm=off(args[2]))]
        if op == "jal":
            if len(args) == 1:
                return [Instr(op, rd=1, imm=off(args[0]))]
            return [Instr(op, rd=r(args[0], ln), imm=off(args[1]))]
        if op == "lui":
            return [Instr(op, rd=r(args[0], ln), imm=v(args[1], ln))]
        raise AsmError(f"line {ln}: cannot assemble {op}")

    def pass2(self) -> Program:
        out = bytearray()
        listing, src = [], {}
        for ln, _, op, args, raw in self.parse():
            if op is None or op == ".equ":
                continue
            addr = len(out)
            if op.startswith("."):
                if op == ".word":
                    for a in args:
                        out += (self.value(a, ln) & 0xFFFF_FFFF).to_bytes(4, "little")
                elif op == ".byte":
                    out += bytes(self.value(a, ln) & 0xFF for a in args)
                elif op in (".ascii", ".asciiz"):
                    out += ast.literal_eval(args[0]).encode("latin-1") + (b"\0" if op == ".asciiz" else b"")
                else:
                    out += bytes(self.directive_size(op, args, addr, ln))
                continue
            for k, ins in enumerate(self.expand(op, args, ln, addr)):
                try:
                    w = encode(ins)
                except ValueError as e:
                    raise AsmError(f"line {ln}: {e}") from None
                listing.append((len(out), w, raw.strip() if k == 0 else ""))
                src[len(out)] = ln
                out += w.to_bytes(4, "little")
        return Program(bytes(out), dict(self.labels), listing, src)


def assemble(text: str) -> Program:
    a = _Asm(text)
    a.pass1()
    return a.pass2()
