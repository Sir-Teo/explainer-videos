from __future__ import annotations

import numpy as np

from explainer.cs import *  # noqa: F403
from explainer.cs.pebble import isa as I
from videos.cs.cs6.common import (code_text, BG, CODE, COST, CTRL, DATA, FIELD_COLORS, FUNC, HEAD, INF, NO, PART, YES, box,
                                  fmt, load, word_bits)


class Isa(VoiceoverScene):
    def construct(self):
        self.card()
        self.state()
        self.formats()
        self.opcodes()
        self.compare()

    def card(self):
        card = chapter_card(3, r"Designing an instruction set", r"What should a machine's words mean?",
                            lit=(1964, 1980, 2010), part=PART)
        with self.voiceover("Chapter three. Designing an instruction set."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]), FadeIn(card[2]))
        self.play(FadeOut(card))

    # ------------------------------------------------------------------
    def state(self):
        head = label(r"What a program can see", font_size=38).to_edge(UP, buff=0.35)
        regs = VGroup()
        for i, n in enumerate(I.REG_NAMES):
            c = GREY_B if i == 0 else (YES if n in ("ra", "sp") else DATA)
            b = Rectangle(width=2.5, height=0.3, stroke_color=c, stroke_width=1.4, fill_color=c, fill_opacity=0.1)
            t = MathTex(rf"r_{{{i}}}\ \texttt{{{n}}}" + (r" = 0" if i == 0 else ""), font_size=20, color=c).move_to(b)
            regs.add(VGroup(b, t))
        regs.arrange(DOWN, buff=0.03).move_to(LEFT * 4.6 + DOWN * 0.3)
        rl = label(r"16 registers \\ of 32 bits", font_size=22, color=YES).next_to(regs, UP, buff=0.15)
        byte_cells = VGroup(*[Square(0.38, stroke_color=GREY_C, stroke_width=1.2) for _ in range(12)]).arrange(
            RIGHT, buff=0.02).move_to(RIGHT * 1.6 + UP * 1.0)
        addrs = VGroup(*[MathTex(str(k), font_size=16, color=GREY_B).next_to(c, DOWN, buff=0.06)
                         for k, c in enumerate(byte_cells)])
        word = SurroundingRectangle(VGroup(*byte_cells[4:8]), buff=0.04, color=DATA)
        word_l = label(r"a word: \ 4 bytes, \ at an address divisible by 4", font_size=20, color=DATA).next_to(
            word, UP, buff=0.12)
        le = VGroup(*[MathTex(rf"\texttt{{{b:02x}}}", font_size=18, color=DATA).move_to(byte_cells[4 + k])
                      for k, b in enumerate((0x78, 0x56, 0x34, 0x12))])
        lel = MathTex(r"\texttt{0x12345678}\ \text{stored little end first}", font_size=24, color=GREY_A).next_to(
            addrs, DOWN, buff=0.25)
        rules = VGroup(
            label(r"memory: \ bytes, \ numbered from 0 \ (here, up to 1 MiB)", font_size=24, color=GREY_A),
            label(r"registers: \ few and fast, \ so a 4-bit field can name one", font_size=24, color=GREY_A),
            label(r"$r_0$ always reads 0: \ a free constant, \ and a place to throw results away", font_size=24,
                  color=YES),
            label(r"the program counter: \ invisible, \ moved only by the instructions themselves", font_size=24,
                  color=GREY_A),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.28).move_to(RIGHT * 1.7 + DOWN * 1.7)
        with self.voiceover(
            "Designing an instruction set starts with what a program can see. <bookmark mark='a'/> Pebble has sixteen "
            "registers of thirty-two bits. Registers are the processor's working values: a handful of fast storage "
            "cells right next to the ALU, and few enough that four bits can name any of them. Register zero always "
            "reads zero, which turns out to be wonderfully useful: it is a free constant, and writing to it throws a "
            "result away. <bookmark mark='b'/> Memory is a long array of bytes, numbered from zero. A word is four "
            "consecutive bytes at an address divisible by four, stored little end first, the convention used here and "
            "by x86; ARM and RISC-V also support little-endian systems. <bookmark mark='c'/> And there is the program "
            "counter, which no instruction reads or writes directly: it moves on by itself, or jumps."
        ) as vo:
            self.play(FadeIn(head))
            self.play(FadeIn(rl), LaggedStart(*[FadeIn(r) for r in regs], lag_ratio=0.04), run_time=1.6)
            vo.wait_until("a")
            self.play(FadeIn(rules[1]), FadeIn(rules[2]))
            vo.wait_until("b")
            self.play(FadeIn(byte_cells), FadeIn(addrs), FadeIn(rules[0]))
            self.play(Create(word), FadeIn(word_l), FadeIn(le), FadeIn(lel))
            vo.wait_until("c")
            self.play(FadeIn(rules[3]))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def formats(self):
        d = load("isa")
        head = label(r"Four formats, \ every word 32 bits", font_size=38).to_edge(UP, buff=0.3)
        picks = [d["examples"][k] for k in (0, 1, 3, 5)]
        names = ["R", "I", "S", "J"]
        uses = [r"two sources, \ one destination", r"a source and an 18-bit constant",
                r"two sources and a constant: \ stores, \ branches", r"a 22-bit constant: \ \texttt{jal}, \ \texttt{lui}"]
        rows = VGroup()
        for k, ex in enumerate(picks):
            wb = word_bits(ex["word"], ex["fields"], cell=0.25, font_size=15)
            tag = MathTex(names[k], font_size=40, color=HEAD)
            src = Text(ex["src"], font="DejaVu Sans Mono", font_size=18, color=CODE)
            use = label(uses[k], font_size=20, color=GREY_B)
            right = VGroup(src, use).arrange(DOWN, aligned_edge=LEFT, buff=0.08)
            rows.add(VGroup(tag, wb, right).arrange(RIGHT, buff=0.35))
        rows.arrange(DOWN, aligned_edge=LEFT, buff=0.28).move_to(DOWN * 0.15)
        for r in rows:
            r[1].align_to(rows[0][1], LEFT)
            r[2].next_to(r[1], RIGHT, buff=0.35).align_to(r[1], UP)
        rows.move_to(DOWN * 0.15)
        same = VGroup(*[SurroundingRectangle(VGroup(*r[1].cells[:6]), buff=0.03, color=CTRL, stroke_width=2.5)
                        for r in rows])
        foot = label(r"the opcode is always the top 6 bits; \ the first register field always starts at bit 25: \\ "
                     r"the decoder can start before it knows the format", font_size=22, color=GREY_A).to_edge(DOWN,
                                                                                                  buff=0.25)
        with self.voiceover(
            "Every Pebble instruction is one thirty-two-bit word, in one of four formats. <bookmark mark='a'/> R "
            "format, for register operations like add, names two source registers and a destination. "
            "<bookmark mark='b'/> I format replaces the second source with an eighteen-bit constant, the immediate, "
            "so adding minus one is a single instruction. <bookmark mark='c'/> S format, for stores and branches, "
            "names two registers to read and carries a constant: the offset to the address, or how far to branch. "
            "<bookmark mark='d'/> J format gives a twenty-two-bit constant to jumps and to lui, which loads the upper "
            "bits of a register. <bookmark mark='e'/> The layout is regular on purpose. The opcode is always the top "
            "six bits, and register fields sit in the same places, so the hardware can read the registers before it "
            "has even finished working out what the instruction is."
        ) as vo:
            self.play(FadeIn(head))
            for k, mk in enumerate("abcd"):
                vo.wait_until(mk)
                self.play(FadeIn(rows[k][0]), FadeIn(rows[k][1].cells, lag_ratio=0.02), FadeIn(rows[k][2]),
                          run_time=1.0)
                self.play(FadeIn(rows[k][1].braces), FadeIn(rows[k][1].names), run_time=0.6)
            vo.wait_until("e")
            self.play(LaggedStart(*[Create(s) for s in same], lag_ratio=0.15), FadeIn(foot))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def opcodes(self):
        d = load("isa")
        head = label(rf"{d['n_ops']} instructions, \ one opcode each", font_size=38).to_edge(UP, buff=0.3)
        groups = [
            (r"arithmetic and logic", ["add", "sub", "and", "or", "xor", "sll", "srl", "sra", "slt", "sltu"], FUNC),
            (r"with a constant", ["addi", "andi", "ori", "xori", "slti", "sltiu", "slli", "srli", "srai"], FUNC),
            (r"memory", ["lw", "lb", "lbu", "sw", "sb"], DATA),
            (r"branches", ["beq", "bne", "blt", "bge", "bltu", "bgeu"], YES),
            (r"jumps and constants", ["jal", "jalr", "lui", "halt"], HEAD),
        ]
        code = {m: k for k, (m, _) in I.OPS.items()}
        cols = VGroup()
        for title, ops, c in groups:
            items = VGroup(*[VGroup(MathTex(rf"\texttt{{{code[o]:2d}}}", font_size=24, color=GREY_B),
                                    code_text(o, font_size=22, color=c)).arrange(RIGHT, buff=0.22)
                             for o in ops]).arrange(DOWN, aligned_edge=LEFT, buff=0.1)
            t = label(title, font_size=24, color=c)
            cols.add(VGroup(t, items).arrange(DOWN, aligned_edge=LEFT, buff=0.18))
        cols.arrange(RIGHT, buff=0.7, aligned_edge=UP).move_to(UP * 0.5)
        rules = VGroup(
            label(r"regular: \ every instruction one word, \ fields in fixed places", font_size=23, color=GREY_A),
            label(r"simple to decode: \ one opcode per instruction, \ a table anyone can read", font_size=23,
                  color=GREY_A),
            label(r"the common case fast: \ small constants fit in the instruction; \ a big one takes two "
                  r"(\texttt{lui}, \texttt{ori})", font_size=23, color=GREY_A),
            label(r"opcode 0 is illegal: \ a jump into empty memory stops the machine", font_size=23, color=NO),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.18).to_edge(DOWN, buff=0.3)
        with self.voiceover(
            "Pebble has thirty-four instructions. <bookmark mark='a'/> Ten that combine two registers, the ALU "
            "operations of Part 4. Nine that combine a register with a constant. Five that move data between "
            "registers and memory, a word or a byte at a time. Six conditional branches. And jumps, lui, and halt, "
            "which stops the machine until Part 31 gives it an operating system to return to. "
            "<bookmark mark='b'/> The design follows a few rules that every good instruction set shares. Keep it "
            "regular. Keep it simple to decode: Pebble gives every instruction its own opcode, so the decoder is a "
            "table you can read. Make the common case fast: most constants in real programs are small, so they fit "
            "inside the instruction, and a large one costs two instructions. <bookmark mark='c'/> And make mistakes "
            "loud: opcode zero means nothing, so a program that jumps into empty memory stops at once instead of "
            "running garbage."
        ) as vo:
            self.play(FadeIn(head),
                      LaggedStart(*[FadeIn(c, shift=UP * 0.15) for c in cols], lag_ratio=0.3), run_time=2.0)
            vo.wait_until("a")
            vo.wait_until("b")
            self.play(LaggedStart(*[FadeIn(r) for r in rules[:3]], lag_ratio=0.5), run_time=3.0)
            vo.wait_until("c")
            self.play(FadeIn(rules[3]))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def compare(self):
        d = load("isa")
        head = label(r"Pebble-32 \ beside RISC-V \ (RV32I)", font_size=38).to_edge(UP, buff=0.35)
        hdr = VGroup(VectorizedPoint(), label(r"Pebble-32", font_size=24, color=HEAD),
                     label(r"RV32I", font_size=24, color=DATA))
        rows = [hdr]
        for a, p, r in d["rv"]:
            rows.append(VGroup(label(a, font_size=22, color=GREY_B), label(p, font_size=22, color=GREY_A),
                               label(r, font_size=22, color=GREY_A)))
        xs = [-4.6, -0.6, 3.6]
        table = VGroup()
        for i, r in enumerate(rows):
            for j, m in enumerate(r):
                m.move_to([xs[j], 2.2 - 0.52 * i, 0])
                if j == 0 and i > 0:
                    m.align_to(np.array([xs[0] + 1.4, 0.0, 0.0]), RIGHT)
            table.add(r)
        why = label("RISC-V: \\ signed-immediate sign extension from bit 31; \\ branch/jump layouts reduce routing hardware \\\\ Pebble: \\ contiguous fields for teaching", font_size=22,
                    color=GREY_A).to_edge(DOWN, buff=0.35)
        hist = label(r"lineage: \ IBM 801 (1980), \ Berkeley RISC \ and Stanford MIPS (1981), \ RISC-V (2010)",
                     font_size=22, color=GREY_B).next_to(why, UP, buff=0.25)
        with self.voiceover(
            "Pebble is a close cousin of RISC-V, the open instruction set begun at Berkeley in 2010, and the "
            "differences are deliberate. <bookmark mark='a'/> RISC-V has thirty-two registers and five-bit register "
            "fields; Pebble's sixteen leave room for longer constants. RISC-V packs several instructions under one "
            "opcode, told apart by extra function fields; Pebble gives each its own. <bookmark mark='b'/> And RISC-V "
            "scatters the bits of its constants around the word, so sign extension can start from bit thirty-one for "
            "signed immediates; the branch and jump layouts also reduce immediate-routing hardware. That is a good "
            "engineering trade, and a terrible one for drawing, so Pebble keeps each constant in one piece. <bookmark "
            "mark='c'/> Both descend from the reduced instruction set computers of around 1980, IBM's 801, Berkeley's "
            "RISC and Stanford's MIPS, which bet that a few simple instructions, run fast, beat many complicated ones."
        ) as vo:
            self.play(FadeIn(head), FadeIn(table[0]))
            self.play(LaggedStart(*[FadeIn(r) for r in table[1:5]], lag_ratio=0.3), run_time=2.0)
            vo.wait_until("a")
            vo.wait_until("b")
            self.play(LaggedStart(*[FadeIn(r) for r in table[5:]], lag_ratio=0.3), FadeIn(why), run_time=2.0)
            vo.wait_until("c")
            self.play(FadeIn(hist))
        self.wait(0.3)
        self.clear_scene()
