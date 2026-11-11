from __future__ import annotations

import numpy as np

from explainer.cs import *  # noqa: F403
from explainer.cs.pebble import isa as I
from videos.cs.cs6.common import (BG, CODE, COST, CTRL, DATA, FUNC, HEAD, NO, PART, YES, box, fmt, load, say)


def mono(s, size=19, color=CODE):
    return Text(s, font="DejaVu Sans Mono", font_size=size, color=color)


class First(VoiceoverScene):
    def construct(self):
        self.card()
        self.sum()
        self.euclid()
        self.verify()

    def card(self):
        card = chapter_card(7, r"First programs, \ gate by gate", r"Does the pile of gates really compute?",
                            part=PART)
        with self.voiceover("Chapter seven. First programs, gate by gate."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]), FadeIn(card[2]))
        self.play(FadeOut(card))

    def listing(self, d, x=-3.6, size=19):
        src = d["source"]
        lines = VGroup(*[mono(s_.rstrip(), size) for s_ in src]).arrange(DOWN, aligned_edge=LEFT, buff=0.14)
        lines.move_to([x, 0.1, 0])
        return lines

    # ------------------------------------------------------------------
    def sum(self):
        d = load("programs")["sum"]
        head = label(r"$1 + 2 + \cdots + 10$, \ on the gate-level machine", font_size=34).to_edge(UP, buff=0.35)
        lines = self.listing(d, x=-3.2, size=20)
        hl = SurroundingRectangle(lines[0], buff=0.06, color=YES, stroke_width=2)
        regs = VGroup()
        vals = {}
        for name in ("a0", "a1"):
            b = Rectangle(width=1.6, height=0.6, stroke_color=GREY_C, stroke_width=1.5)
            v = MathTex("0", font_size=32, color=DATA).move_to(b)
            vals[name] = v
            regs.add(VGroup(MathTex(rf"\texttt{{{name}}}", font_size=30, color=GREY_A), VGroup(b, v)).arrange(
                RIGHT, buff=0.25))
        regs.arrange(DOWN, buff=0.3).move_to(RIGHT * 3.6 + UP * 1.0)
        cyc = ValueTracker(0)
        cl = always_redraw(lambda: label(rf"cycle {int(cyc.get_value())}", font_size=28, color=COST).next_to(
            regs, DOWN, buff=0.5))
        rows = d["rows"]
        src_lines = [s_ for s_ in d["source"]]

        first = rows[0]["line"]
        code_lines = [k for k, s_ in enumerate(src_lines) if s_.strip()]

        def line_of(r):
            # source line numbers count from the program text; the listing shows its non-empty lines
            return code_lines[0] + (r["line"] - first)

        foot = label(rf"{d['steps']} cycles; \ every one evaluates the whole netlist, \ about 8{{,}}000 gates", font_size=24,
                     color=GREY_A).to_edge(DOWN, buff=0.4)
        with self.voiceover(
            "The first program anyone writes for a new machine is a loop. <bookmark mark='a'/> This one adds the "
            "numbers from one to ten: a zero counts down from ten, a one accumulates the sum, and the branch jumps back "
            "until a zero reaches zero. <bookmark mark='b'/> Here it runs on the gate-level Pebble, the netlist itself, "
            "every one of its eight thousand gates evaluated in every clock cycle. The highlighted line is where the "
            "program counter points. <bookmark mark='c'/> Thirty-five cycles later the machine halts with fifty-five "
            "in a one."
        ) as vo:
            self.play(FadeIn(head), FadeIn(lines), FadeIn(regs))
            self.play(Create(hl))
            vo.wait_until("a")
            vo.wait_until("b")
            self.add(cl)
            for k, r in enumerate(rows):
                ln = min(max(line_of(r), 0), len(lines) - 1)
                anims = [hl.animate.move_to(lines[ln]).stretch_to_fit_width(lines[ln].width + 0.12),
                         cyc.animate.set_value(k + 1)]
                for name, v in zip(("a0", "a1"), r["regs"]):
                    nv = MathTex(str(v), font_size=32, color=DATA).move_to(vals[name])
                    anims.append(Transform(vals[name], nv))
                self.play(*anims, run_time=0.22 if k > 6 else 0.45)
            vo.wait_until("c")
            self.play(Indicate(vals["a1"], color=YES, scale_factor=1.4), FadeIn(foot))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def euclid(self):
        d = load("programs")["euclid"]
        head = label(r"Part 1's Euclid, \ $\gcd(1071, 462)$", font_size=36).to_edge(UP, buff=0.35)
        lines = self.listing(d, x=-4.3, size=17).to_edge(LEFT, buff=0.35)
        rows = d["rows"]
        n = len(rows)
        ax = Axes(x_range=[0, n, 10], y_range=[0, 1100, 250], x_length=6.2, y_length=4.0, tips=False,
                  axis_config={"color": GREY_C, "font_size": 18, "include_numbers": True}).move_to(RIGHT * 3.2 +
                                                                                                  DOWN * 0.2)
        xl = note(r"clock cycle", font_size=20).next_to(ax, DOWN, buff=0.3)
        a0 = [r["regs"][0] for r in rows]
        a1 = [r["regs"][1] for r in rows]

        def stairs(v, color):
            pts = []
            for k, y in enumerate(v):
                pts += [ax.c2p(k, y), ax.c2p(k + 1, y)]
            return VMobject(color=color, stroke_width=3).set_points_as_corners(pts)

        s0, s1 = stairs(a0, DATA), stairs(a1, HEAD)
        lab = VGroup(MathTex(r"a_0", font_size=28, color=DATA).next_to(ax.c2p(2, a0[2]), UR, buff=0.1),
                     MathTex(r"a_1", font_size=28, color=HEAD).next_to(ax.c2p(4, a1[4]), UP, buff=0.12))
        res = label(rf"halts after {d['steps']} cycles \ with $a_0 = {d['regs'][3]}$", font_size=26,
                    color=YES).to_edge(DOWN, buff=0.35)
        with self.voiceover(
            "Now Euclid's algorithm from Part 1, the oldest algorithm in this series, on a machine built from NAND "
            "gates. <bookmark mark='a'/> The program subtracts the smaller number from the larger until one of them is "
            "zero, swapping them when necessary. <bookmark mark='b'/> Watch the two registers, cycle by cycle. A "
            "zero starts at one thousand and seventy-one and drops by four hundred and sixty-two, twice; then the "
            "registers swap, and the remainders shrink, a hundred and forty-seven, then twenty-one. "
            "<bookmark mark='c'/> After sixty cycles the machine halts with twenty-one in a zero, the greatest common "
            "divisor, exactly as Euclid's pebbles found it."
        ) as vo:
            self.play(FadeIn(head), FadeIn(lines))
            self.play(Create(ax), FadeIn(xl))
            vo.wait_until("a")
            vo.wait_until("b")
            self.play(Create(s0), Create(s1), FadeIn(lab), run_time=5.0, rate_func=linear)
            vo.wait_until("c")
            self.play(FadeIn(res))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def verify(self):
        c = load("cosim")
        st = c["styles"]
        head = label(r"Is the gate-level machine right?", font_size=38).to_edge(UP, buff=0.35)
        ex = VGroup(*[mono(t, 15, GREY_B) for t in c["example"][12:24]]).arrange(DOWN, aligned_edge=LEFT, buff=0.06)
        ex.move_to(LEFT * 4.9 + DOWN * 0.3)
        el = label(r"a random program \\ (one of 300)", font_size=20, color=GREY_A).next_to(ex, UP, buff=0.2)
        emu = box(2.6, 0.9, r"\text{emulator}", CODE, 26).move_to(LEFT * 0.6 + UP * 1.3)
        gl = box(2.6, 0.9, r"\text{gate level}", YES, 26).move_to(LEFT * 0.6 + DOWN * 1.1)
        arr = VGroup(Arrow(ex.get_right(), emu.get_left(), buff=0.2, color=GREY_B),
                     Arrow(ex.get_right(), gl.get_left(), buff=0.2, color=GREY_B))
        eq = MathTex(r"=", font_size=60, color=YES).move_to(LEFT * 0.6 + UP * 0.1).rotate(PI / 2)
        res = VGroup(
            label(rf"{st['table']['agree']} of {st['table']['programs']} programs: \\ final registers, \ every byte of "
                  r"memory, \\ the step count", font_size=24, color=YES),
            label(rf"{fmt(st['table']['instructions'])} instructions; \ with both control units", font_size=24,
                  color=GREY_A),
            label(r"the emulator: \ a page of \texttt{if}s; \\ the gate-level machine: \ the circuit", font_size=22,
                  color=GREY_B),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.3).move_to(RIGHT * 3.9 + UP * 0.1)
        sp = label(r"the netlist is compiled to C, \ one line per gate: \ thousands of cycles a second", font_size=22,
                   color=GREY_B).to_edge(DOWN, buff=0.3)
        with self.voiceover(
            "Two programs are not a proof. To trust the gate-level machine, the series' library tests it against an "
            "independent model. <bookmark mark='a'/> The emulator is a short Python program that states what each "
            "instruction means, with no circuits at all. <bookmark mark='b'/> A generator writes random programs, the "
            "base instruction set with random registers and constants, branches and jumps, loads and stores of words "
            "and bytes. <bookmark mark='c'/> Both machines run three hundred of them, with both versions of the "
            "control unit. After each completed program, all registers, every memory byte, the program counter and the"
            " step count agree. This is a final-state comparison, not a comparison at every instruction boundary or a "
            "proof for all programs. <bookmark mark='d'/> To make that affordable, the netlist is compiled to C, one "
            "line per gate, so the gate-level Pebble runs a few thousand cycles a second: slow, but fast enough to run"
            " real programs."
        ) as vo:
            self.play(FadeIn(head))
            self.play(FadeIn(emu))
            vo.wait_until("a")
            vo.wait_until("b")
            self.play(FadeIn(el), FadeIn(ex, lag_ratio=0.05), FadeIn(gl), GrowArrow(arr[0]), GrowArrow(arr[1]))
            vo.wait_until("c")
            self.play(FadeIn(eq, scale=1.4), FadeIn(res[0]))
            self.play(FadeIn(res[1]), FadeIn(res[2]))
            vo.wait_until("d")
            self.play(FadeIn(sp))
        self.wait(0.3)
        self.clear_scene()
