from __future__ import annotations

import numpy as np

from explainer.cs import *  # noqa: F403
from videos.cs.cs3.s05_cmos import cmos_gate
from videos.cs.cs6.common import (BG, CODE, COST, CTRL, DATA, FUNC, HEAD, HIST, NO, PART, YES, Datapath, box, fmt,
                                  gate, load, say)


class Counted(VoiceoverScene):
    def construct(self):
        self.card()
        self.blocks()
        self.compare()
        self.missing()
        self.tower()

    def card(self):
        card = chapter_card(14, r"The whole machine, \ counted", r"How big is a computer?", lit=(1975,), part=PART)
        with self.voiceover("Chapter fourteen. The whole machine, counted."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]), FadeIn(card[2]))
        self.play(FadeOut(card))

    # ------------------------------------------------------------------
    def blocks(self):
        cp = load("cpu")
        head = label(r"Where Pebble's gates go", font_size=38).to_edge(UP, buff=0.35)
        order = [("register read", r"register read ports", YES), ("write-back", r"write-back and register writes", YES),
                 ("ALU", r"ALU", FUNC), ("next pc", r"next pc: \ two adders, \ muxes", COST),
                 ("control", r"control", CTRL), ("immediate", r"immediates", HEAD)]
        tot = cp["gates"]
        scale = 7.4 / max(cp["blocks"].values())
        bars = VGroup()
        for k, (key, name, c) in enumerate(order):
            n = cp["blocks"][key]
            w = max(n * scale, 0.05)
            y = 1.9 - 0.62 * k
            r = Rectangle(width=w, height=0.42, stroke_width=0, fill_color=c, fill_opacity=0.75).move_to(
                [-3.2 + w / 2, y, 0])
            nl = label(name, font_size=20, color=c).move_to([-3.4, y, 0], aligned_edge=RIGHT)
            vl = label(rf"{fmt(n)} \ ({100 * n / tot:.0f}\%)", font_size=20, color=GREY_A).next_to(r, RIGHT, buff=0.12)
            bars.add(VGroup(nl, r, vl))
        tl = label(rf"{fmt(tot)} gates \ (AND, OR, NOT, XOR) \ and {cp['flip_flops']} flip-flops", font_size=26,
                   color=HEAD).to_edge(DOWN, buff=0.95)
        notes = label(r"most of the machine is moving data between registers, \ not computing on it", font_size=22,
                      color=GREY_A).to_edge(DOWN, buff=0.4)
        with self.voiceover(
            "Now count the whole machine. <bookmark mark='a'/> The biggest block is not the ALU. It is the register "
            "file's two read ports: thirty-two-bit multiplexer trees choosing among sixteen registers, about three "
            "thousand logic gates. The four hundred and eighty register-state inputs belong to storage and are "
            "excluded from that logic count. Next are the multiplexers that write a register or keep its value, then "
            "the ALU itself, the two adders and multiplexers that choose the next program counter, and finally the "
            "control unit, a few hundred gates, and the immediates, almost nothing. <bookmark mark='b'/> Eight "
            "thousand two hundred and twenty-four gates and five hundred and twelve flip-flops. Most of a processor, "
            "it turns out, is choosing and moving data, not computing on it."
        ) as vo:
            self.play(FadeIn(head), FadeIn(bars[0][0]), GrowFromEdge(bars[0][1], LEFT), FadeIn(bars[0][2]))
            vo.wait_until("a")
            self.play(LaggedStart(*[AnimationGroup(FadeIn(b[0]), GrowFromEdge(b[1], LEFT), FadeIn(b[2]))
                                  for b in bars[1:]], lag_ratio=0.35), run_time=2.4)
            vo.wait_until("b")
            self.play(FadeIn(tl))
            self.play(FadeIn(notes))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def compare(self):
        cp = load("cpu")
        head = label(r"Pebble among real processors", font_size=38).to_edge(UP, buff=0.35)
        peb = cp["transistors_logic"] + cp["transistors_ff"]
        items = [(r"MOS 6502 (1975)", 3510, GREY_B), (r"Intel 8086 (1978)", 29000, GREY_B),
                 ("Pebble: \\ synthetic logic estimate", peb, HEAD), (r"Intel 80386 (1985)", 275000, GREY_B),
                 (r"Apple M1 (2020), \ the whole chip", 16_000_000_000, GREY_B)]
        lo, hi = 3, 10.5
        x0, width = -2.0, 6.2
        rows = VGroup()
        for k, (name, n, c) in enumerate(items):
            e = np.log10(n)
            w = (e - lo) / (hi - lo) * width
            y = 1.7 - 0.7 * k
            r = Rectangle(width=w, height=0.45, stroke_width=0, fill_color=c, fill_opacity=0.7).move_to(
                [x0 + w / 2, y, 0])
            nl = label(name, font_size=21, color=c).move_to([x0 - 0.2, y, 0], aligned_edge=RIGHT)
            vl = label(fmt(n) + r" transistors", font_size=19, color=GREY_A).next_to(r, RIGHT, buff=0.12)
            rows.add(VGroup(nl, r, vl))
        axis = VGroup(*[VGroup(DashedLine([x0 + (e - lo) / (hi - lo) * width, 2.1, 0],
                                          [x0 + (e - lo) / (hi - lo) * width, -1.4, 0], color=GREY_D, stroke_width=1),
                               MathTex(rf"10^{{{e}}}", font_size=18, color=GREY_B).move_to(
                                   [x0 + (e - lo) / (hi - lo) * width, -1.6, 0])) for e in (3, 5, 7, 9)])
        how = label(rf"{fmt(cp['nand'])} two-input NAND equivalents $\times$ 4 transistors, \ plus "
                    rf"{cp['flip_flops']} flip-flops $\times$ 24", font_size=21, color=GREY_B).to_edge(DOWN, buff=0.9)
        cav = label("Pebble excludes memory, I/O, clocks, buffers and layout; \\\\ different counting scopes, \\ not an area comparison", font_size=21, color=GREY_B).to_edge(DOWN, buff=0.4)
        with self.voiceover(
            "How does that compare with real chips? <bookmark mark='a'/> Our teaching count maps each two-input NAND "
            "equivalent to four transistors and each flip-flop to twenty-four, giving about ninety thousand. This is a"
            " synthetic logic estimate, excluding memory, I/O, clock distribution, buffers and physical layout; it is "
            "not a fabricated chip count. <bookmark mark='b'/> The 6502, the processor of the Apple II and, in a "
            "variant, the Commodore 64, had three and a half thousand, because it was eight bits wide and squeezed by "
            "brilliant hand design. Intel's 8086 had twenty-nine thousand, and the 386, the first thirty-two-bit x86, "
            "two hundred and seventy-five thousand. <bookmark mark='c'/> Apple's M1 was reported at sixteen billion "
            "transistors for the whole system on a chip, including caches, graphics and accelerators. These bars show "
            "orders of magnitude with different counting scopes, not how many working Pebbles fit on an M1 or a "
            "physical area comparison."
        ) as vo:
            self.play(FadeIn(head), FadeIn(axis))
            self.play(FadeIn(rows[2][0]), GrowFromEdge(rows[2][1], LEFT), FadeIn(rows[2][2]), FadeIn(how))
            vo.wait_until("a")
            vo.wait_until("b")
            for k in (0, 1, 3):
                self.play(FadeIn(rows[k][0]), GrowFromEdge(rows[k][1], LEFT), FadeIn(rows[k][2]), run_time=0.8)
            vo.wait_until("c")
            self.play(FadeIn(rows[4][0]), GrowFromEdge(rows[4][1], LEFT), FadeIn(rows[4][2]), run_time=1.2)
            self.play(FadeIn(cav))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def missing(self):
        head = label(r"What a real processor adds", font_size=38).to_edge(UP, buff=0.35)
        rows = VGroup(*[VGroup(label(a, font_size=24, color=c), label(b, font_size=22, color=GREY_A)).arrange(
            RIGHT, buff=0.4) for a, b, c in (
            (r"a pipeline, \ then out-of-order execution", r"several instructions at once \ (Parts 7, 8)", DATA),
            (r"multiply, divide, floating point", r"Part 4's circuits, wired in \ (Part 7)", FUNC),
            (r"caches", r"most memory accesses never leave the chip \ (Part 9)", YES),
            (r"several cores", r"and the problem of sharing memory \ (Part 10)", HEAD),
            (r"privilege, \ virtual memory", r"so an operating system can protect programs \ (Parts 31, 32)", NO),
        )]).arrange(DOWN, aligned_edge=LEFT, buff=0.32).move_to(DOWN * 0.1)
        for r in rows:
            r[1].align_to(rows[0][1], LEFT).set_x(0.4, direction=LEFT)
        foot = label("base-ISA programs remain compatible; \\ extensions add new instructions", font_size=24,
                     color=HEAD).to_edge(DOWN, buff=0.35)
        with self.voiceover(
            "Pebble is a complete computer, but a modest one, and the next acts add what real processors have. "
            "<bookmark mark='a'/> Pipelines and then out-of-order execution, to work on many instructions at once. "
            "Multiplication, division and floating point, from Part 4's circuits. <bookmark mark='b'/> Caches, so that "
            "most memory accesses never leave the chip. Several cores, and the surprisingly deep problem of letting them "
            "share memory. And privilege levels and virtual memory, so that an operating system can keep programs from "
            "trampling each other. <bookmark mark='c'/> Each of these keeps the contract of the instruction set. The "
            "Job's program will not change for the next three parts; only the machine under it will."
        ) as vo:
            self.play(FadeIn(head))
            self.play(FadeIn(rows[0]))
            vo.wait_until("a")
            self.play(FadeIn(rows[1]))
            vo.wait_until("b")
            self.play(FadeIn(rows[2]))
            self.play(FadeIn(rows[3]))
            self.play(FadeIn(rows[4]))
            vo.wait_until("c")
            self.play(FadeIn(foot))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def tower(self):
        head = label(r"Down the tower, \ and back", font_size=38).to_edge(UP, buff=0.35)
        dp = Datapath().scale(0.8).shift(DOWN * 0.3)
        alu = dp.blocks["alu"]
        # level 2: the ALU's adder, bit by bit
        bits = VGroup(*[box(0.8, 0.8, rf"\Sigma_{{{k}}}", FUNC, 22) for k in range(8)]).arrange(LEFT, buff=0.15)
        bits.move_to(DOWN * 0.2)
        carry = VGroup(*[Arrow(bits[k].get_left(), bits[k + 1].get_right(), buff=0.02, color=COST, stroke_width=2,
                               max_tip_length_to_length_ratio=0.4) for k in range(7)])
        bl = label(r"the ALU's adder: \ one full adder per bit \ (Part 4)", font_size=24, color=FUNC).next_to(
            bits, DOWN, buff=0.5)
        # level 3: a full adder in gates
        g1, g2 = gate("XOR", size=0.8).move_to(LEFT * 1.6 + UP * 0.6), gate("XOR", size=0.8).move_to(RIGHT * 0.8 +
                                                                                                    UP * 0.4)
        g3, g4 = gate("AND", size=0.8).move_to(LEFT * 1.6 + DOWN * 0.9), gate("AND", size=0.8).move_to(RIGHT * 0.2 +
                                                                                                    DOWN * 0.8)
        g5 = gate("OR", size=0.8).move_to(RIGHT * 2.2 + DOWN * 0.9)
        fa = VGroup(g1, g2, g3, g4, g5)
        fl = label(r"one full adder: \ five gates \ (Part 4)", font_size=24, color=GREY_A).next_to(fa, DOWN, buff=0.5)
        # level 4: a NAND gate in transistors
        cm = cmos_gate("NAND", center=ORIGIN + DOWN * 0.2, s=0.85).scale(0.85)
        cl = label(r"each gate: \ a few NANDs; \ each NAND: \ four transistors \ (Part 3)", font_size=24,
                   color=GREY_A).to_edge(DOWN, buff=0.3)
        up = label(r"and back up: \ transistors, \ gates, \ adders, \ an ALU, \ a computer", font_size=26,
                   color=HEAD).to_edge(DOWN, buff=0.3)
        with self.voiceover(
            "Before we leave Act One, take the trip down the tower once, all the way. <bookmark mark='a'/> Here is "
            "Pebble's datapath. Pick the ALU, and look inside. <bookmark mark='b'/> Its adder is a row of full adders,"
            " one per bit, with carries rippling between them, or racing through a prefix tree, as in Part 4. "
            "<bookmark mark='c'/> Pick one full adder: five gates. <bookmark mark='d'/> Pick one gate, built as NANDs,"
            " and one NAND is four transistors, two pulling the output up and two pulling it down, as in Part 3. "
            "<bookmark mark='e'/> And back up again: transistors make gates, gates make adders, adders make an ALU, "
            "and an ALU, registers and a little control make a computer that runs programs within its instruction set "
            "and available memory. Every layer of that tower, in this series, is code you can read and run."
        ) as vo:
            self.play(FadeIn(head))
            self.play(FadeIn(dp))
            vo.wait_until("a")
            self.play(Indicate(alu, color=HEAD, scale_factor=1.15))
            vo.wait_until("b")
            self.play(FadeOut(dp, scale=2.0), FadeIn(bits, scale=0.4), run_time=1.2)
            self.play(LaggedStart(*[GrowArrow(c) for c in carry], lag_ratio=0.15), FadeIn(bl))
            vo.wait_until("c")
            self.play(Indicate(bits[3], color=HEAD, scale_factor=1.3), run_time=0.5)
            self.play(FadeOut(VGroup(bits, carry, bl), scale=2.0), FadeIn(fa, scale=0.4), run_time=1.0)
            self.play(FadeIn(fl), run_time=0.5)
            vo.wait_until("d")
            self.play(Indicate(g1, color=HEAD, scale_factor=1.3))
            self.play(FadeOut(VGroup(fa, fl), scale=2.0), FadeIn(cm, scale=0.4), run_time=1.2)
            self.play(FadeIn(cl))
            vo.wait_until("e")
            self.play(FadeOut(VGroup(cm, cl), scale=0.3), run_time=0.8)
            dp2 = Datapath().scale(0.8).shift(DOWN * 0.3)
            self.play(FadeIn(dp2, scale=0.3), FadeIn(up), run_time=1.4)
        self.wait(0.3)
        self.clear_scene()
