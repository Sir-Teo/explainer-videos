from __future__ import annotations

import numpy as np

from explainer.cs import *  # noqa: F403
from videos.cs.cs6.common import (BG, CODE, COST, CTRL, DATA, FUNC, HEAD, HIST, NO, PART, YES, box, fmt, load)

SIG_TEX = {"rw": r"\text{reg write}", "imm": r"\text{imm}", "aop0": r"\text{alu}_0", "aop1": r"\text{alu}_1",
           "aop2": r"\text{alu}_2", "aop3": r"\text{alu}_3", "sf": r"\text{S fmt}", "jf": r"\text{J fmt}",
           "ld": r"\text{load}", "st": r"\text{store}", "byte": r"\text{byte}", "sgn": r"\text{signed}",
           "wb0": r"\text{wb}_0", "wb1": r"\text{wb}_1", "br": r"\text{branch}", "bz": r"\text{zero?}",
           "bn": r"\text{negate}", "jal": r"\text{jal}", "jalr": r"\text{jalr}", "halt": r"\text{halt}"}


def truth_grid(d, cw=0.3, ch=0.152):
    sigs = d["signals"]
    rows = d["rows"]
    cells = VGroup()
    names = VGroup()
    for i, r in enumerate(rows):
        y = -i * ch
        names.add(Text(r["op"], font="DejaVu Sans Mono", font_size=12, color=GREY_B).move_to([-0.45, y, 0],
                                                                                         aligned_edge=RIGHT))
        for j, b in enumerate(r["bits"]):
            sq = Rectangle(width=cw * 0.9, height=ch * 0.8, stroke_width=0, fill_color=HEAD if b else GREY_D,
                           fill_opacity=0.95 if b else 0.25).move_to([j * cw, y, 0])
            cells.add(sq)
    heads = VGroup(*[MathTex(SIG_TEX[s], font_size=17, color=CTRL).rotate(PI / 2).move_to([j * cw, 0.45, 0],
                                                                                         aligned_edge=DOWN)
                     for j, s in enumerate(sigs)])
    g = VGroup(names, cells, heads)
    g.cells, g.names, g.heads = cells, names, heads
    g.ncols = len(sigs)
    return g


class Control(VoiceoverScene):
    def construct(self):
        self.card()
        self.table()
        self.logic()
        self.microcode()

    def card(self):
        card = chapter_card(5, r"The control unit", r"How does a word of bits steer the datapath?", lit=(1951,),
                            part=PART)
        with self.voiceover("Chapter five. The control unit."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]), FadeIn(card[2]))
        self.play(FadeOut(card))

    # ------------------------------------------------------------------
    def table(self):
        d = load("control")
        head = label(r"The control unit is a truth table", font_size=36).to_edge(UP, buff=0.3)
        g = truth_grid(d)
        g.move_to(LEFT * 2.5 + DOWN * 0.55)
        k = next(i for i, r in enumerate(d["rows"]) if r["op"] == "lw")
        n = g.ncols
        row = VGroup(*g.cells[k * n:(k + 1) * n])
        hl = SurroundingRectangle(VGroup(row, g.names[k]), buff=0.03, color=YES, stroke_width=2)
        on = [d["signals"][j] for j, b in enumerate(d["rows"][k]["bits"]) if b]
        expl = VGroup(
            label(r"input: \ the 6-bit opcode", font_size=24, color=GREY_A),
            label(rf"output: \ {len(d['signals'])} control signals", font_size=24, color=CTRL),
            label(rf"{len(d['rows'])} rows, \ one per instruction; \\ the other {64 - len(d['rows'])} opcodes "
                  r"are illegal", font_size=22, color=GREY_B),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.18).move_to(RIGHT * 4.0 + UP * 1.2)
        lw = VGroup(
            label(r"\texttt{lw} \ asks for:", font_size=24, color=YES),
            label(r"write a register; \ the immediate into the ALU; \\ the ALU adds; \ read memory; \\ write back the "
                  r"loaded word", font_size=22, color=GREY_A),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.12).move_to(RIGHT * 4.0 + DOWN * 0.9)
        with self.voiceover(
            "The datapath has about twenty control wires: whether to write a register, which input the ALU takes, "
            "which operation it does, whether to touch memory, what to write back, whether this is a branch. "
            "<bookmark mark='a'/> For each instruction, those wires take fixed values, so the control unit is a truth "
            "table with the six-bit opcode as its input and twenty outputs. <bookmark mark='b'/> Here it is, one row "
            "per instruction, a bright cell for every one. <bookmark mark='c'/> The load-word row, for example, asks "
            "for a register write, the immediate as the ALU's second operand, an addition, a memory read, and the "
            "loaded word on the write-back path. Every other opcode, thirty of the sixty-four, is illegal."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(FadeIn(expl[0]), FadeIn(expl[1]), FadeIn(g.heads, lag_ratio=0.05), FadeIn(g.names))
            vo.wait_until("b")
            self.play(LaggedStart(*[FadeIn(c) for c in g.cells], lag_ratio=0.0015), run_time=2.5)
            vo.wait_until("c")
            self.play(Create(hl), FadeIn(lw), FadeIn(expl[2]))
            self.play(LaggedStart(*[Indicate(g.heads[d["signals"].index(s)], color=YES, scale_factor=1.4)
                                    for s in on], lag_ratio=0.25), run_time=2.0)
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def logic(self):
        d = load("control")
        st = d["styles"]
        head = label(r"Two ways to build it", font_size=38).to_edge(UP, buff=0.35)
        # a PLA picture: decoder lines (AND plane) and OR columns
        n_and, n_or = 10, 7
        rng = np.random.default_rng(3)
        lines = VGroup(*[Line([-6.2, 1.4 - 0.3 * i, 0], [-1.8, 1.4 - 0.3 * i, 0], color=GREY_C, stroke_width=1.5)
                         for i in range(n_and)])
        ins = VGroup(*[Line([-6.0 + 0.3 * j, 1.75, 0], [-6.0 + 0.3 * j, -1.4, 0], color=DATA, stroke_width=1.5)
                       for j in range(6)])
        outs = VGroup(*[Line([-3.7 + 0.3 * j, 1.75, 0], [-3.7 + 0.3 * j, -1.4, 0], color=CTRL, stroke_width=1.5)
                        for j in range(n_or)])
        dots = VGroup()
        for i in range(n_and):
            for j in range(6):
                dots.add(Dot([-6.0 + 0.3 * j, 1.4 - 0.3 * i, 0], radius=0.05, color=DATA if rng.random() < 0.5
                             else GREY_A))
            for j in range(n_or):
                if rng.random() < 0.35:
                    dots.add(Dot([-3.7 + 0.3 * j, 1.4 - 0.3 * i, 0], radius=0.05, color=HEAD))
        pl = VGroup(label(r"AND plane: \\ one line per opcode", font_size=20, color=DATA).next_to(ins, DOWN, buff=0.15),
                    label(r"OR plane: \\ one column per signal", font_size=20, color=CTRL).next_to(outs, DOWN,
                                                                                                   buff=0.15))
        opts = VGroup(
            VGroup(label(r"as a table \ (a ROM, \ or a PLA)", font_size=26, color=YES),
                   label(rf"one product term per opcode: \ {st['table']['terms']} terms, \ {st['table']['gates']} gates",
                         font_size=22, color=GREY_A),
                   label(r"easy to read, \ easy to change", font_size=22, color=GREY_B)).arrange(DOWN, aligned_edge=LEFT,
                                                                                               buff=0.1),
            VGroup(label(r"as minimized logic", font_size=26, color=HEAD),
                   label(rf"Quine--McCluskey (Part 3), \ the illegal opcodes as don't-cares: \ {st['minimized']['gates']} "
                         r"gates", font_size=22, color=GREY_A),
                   label(r"smaller and faster, \ but every change means minimizing again", font_size=22,
                         color=GREY_B)).arrange(DOWN, aligned_edge=LEFT, buff=0.1),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.5).move_to(RIGHT * 3.0 + UP * 0.4)
        same = label(r"both built, \ and both run the same 300 random programs \ with identical results", font_size=24,
                     color=YES).to_edge(DOWN, buff=0.4)
        with self.voiceover(
            "A truth table can be built in two ways, and Pebble's library builds both. <bookmark mark='a'/> The direct "
            "way gives every opcode its own detector, an AND of six literals, and makes each control signal the OR of "
            "the detectors where it is one. This is a programmable logic array, or a read-only memory: an AND plane "
            "and an OR plane, and changing the instruction set means changing which dots are connected. It costs "
            "about three hundred gates. <bookmark mark='b'/> The clever way minimizes each signal with Part 3's "
            "Quine–McCluskey method, using the thirty illegal opcodes as don't-cares, and shares the product terms "
            "between signals. Two hundred and five gates, a third fewer. <bookmark mark='c'/> Both versions of the "
            "processor run the same three hundred random programs, and end in exactly the same state."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(Create(ins), Create(lines), Create(outs), run_time=1.5)
            self.play(LaggedStart(*[FadeIn(dd, scale=2) for dd in dots], lag_ratio=0.01), FadeIn(pl), run_time=1.8)
            self.play(FadeIn(opts[0]))
            vo.wait_until("b")
            self.play(FadeIn(opts[1]))
            vo.wait_until("c")
            self.play(FadeIn(same))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def microcode(self):
        d = load("control")
        head = label(r"Microcode \ (Wilkes, 1951)", font_size=38).to_edge(UP, buff=0.35)
        rows, cols = 8, 10
        rng = np.random.default_rng(9)
        grid = VGroup()
        for i in range(rows):
            for j in range(cols):
                on = rng.random() < 0.35
                grid.add(Circle(radius=0.09, stroke_color=HEAD if on else GREY_D, stroke_width=1.5,
                                fill_color=HEAD, fill_opacity=0.9 if on else 0).move_to([-5.6 + 0.36 * j,
                                                                                         1.4 - 0.4 * i, 0]))
        nxt = VGroup(*[MathTex(rf"\to {int(rng.integers(0, rows))}", font_size=20, color=CTRL)
                       .move_to([-5.6 + 0.36 * cols + 0.25, 1.4 - 0.4 * i, 0]) for i in range(rows)])
        gl = label(r"a control store: \\ one row per step, \ a dot per signal, \\ and the next row to use", font_size=20,
                   color=GREY_A).next_to(grid, DOWN, buff=0.3)
        ptr = Arrow(LEFT * 0.5, ORIGIN, buff=0, color=YES, stroke_width=4).next_to(grid[0], LEFT, buff=0.1)
        pts = VGroup(
            label(r"Maurice Wilkes: \ control as a \textit{program} of microinstructions, \\ stored in a diode "
                  r"matrix", font_size=22, color=HIST),
            label(r"a multi-step instruction \ (a multiply, \ a string copy) \\ walks through several rows", font_size=22,
                  color=GREY_A),
            label(r"IBM's System/360 (1964): \ one instruction set \\ on a family of machines, \ most microcoded",
                  font_size=22, color=GREY_A),
            label(r"today's x86 cores: \ simple instructions hard-wired, \\ complex ones microcoded, \ and the microcode "
                  r"patchable \\ (the 2018 Spectre fixes shipped this way)", font_size=22, color=YES),
            label(rf"Pebble's whole table: \ {d['store_words']} words of {d['word_bits']} bits", font_size=22,
                  color=CTRL),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.25).move_to(RIGHT * 2.3 + DOWN * 0.1)
        with self.voiceover(
            "There is a third way, and for decades it was the usual one. <bookmark mark='a'/> In 1951 Maurice Wilkes, "
            "of EDSAC, proposed that control should itself be a program: a store of microinstructions, each a row of "
            "control signals plus the address of the next row, kept in a matrix of diodes. <bookmark mark='b'/> A "
            "simple instruction uses one row. A complicated one, a multiplication or a string copy, walks through "
            "several, one per clock cycle, just as a program walks through instructions. <bookmark mark='c'/> "
            "Microcode let IBM's System/360 of 1964 offer one instruction set on a whole family of machines, small to "
            "huge, most of them microcoded. Modern x86 processors still hard-wire the common instructions and microcode "
            "the rare complex ones, and the microcode can be patched after the chip is sold: some of the fixes for "
            "the Spectre attacks in 2018 shipped exactly this way. Pebble's instructions are all simple, so its whole "
            "control store would be one row each: thirty-four words of twenty bits."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(c) for c in grid], lag_ratio=0.01), FadeIn(nxt), FadeIn(gl), run_time=2.0)
            self.play(FadeIn(pts[0]))
            vo.wait_until("b")
            self.play(GrowArrow(ptr))
            for r in (1, 2, 5, 6):
                self.play(ptr.animate.next_to(grid[r * cols], LEFT, buff=0.1), run_time=0.45)
            self.play(FadeIn(pts[1]))
            vo.wait_until("c")
            self.play(FadeIn(pts[2]))
            self.play(FadeIn(pts[3]))
            self.play(FadeIn(pts[4]))
        self.wait(0.3)
        self.clear_scene()
