from __future__ import annotations

import numpy as np

from explainer.cs import *  # noqa: F403
from videos.cs.cs16.common import (CODE, COST, CTRL, DATA, FUNC, HEAD, LAM, NO, PART, YES, code, load, mono, words)


class Models(VoiceoverScene):
    def construct(self):
        self.card()
        self.ram()
        self.pitfall()
        self.others()

    def card(self):
        card = chapter_card(1, r"What counts as a step", r"How do we measure an algorithm, not a machine?",
                            lit=(1963,), extra=((1963, r"Shepherdson and Sturgis: \ register machines"),), part=PART)
        with self.voiceover("Chapter one. What counts as a step."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]), FadeIn(card[2]))
        self.play(FadeOut(card))

    def ram(self):
        head = label(r"The RAM: \ a machine for counting", font_size=34).to_edge(UP, buff=0.3)
        cells = VGroup(*[VGroup(Rectangle(width=0.9, height=0.5, color=GREY_B, stroke_width=1.5),
                                mono(str(v), 16, WHITE)) for v in (7, 3, 0, 12, 5, 9, 1, 4)])
        for c in cells:
            c[1].move_to(c[0])
        cells.arrange(RIGHT, buff=0).move_to(UP * 1.4)
        addr = VGroup(*[mono(str(k), 13, GREY_B).next_to(c, UP, buff=0.08) for k, c in enumerate(cells)])
        cpu = VGroup(RoundedRectangle(width=2.6, height=1.0, corner_radius=0.12, color=DATA, stroke_width=2),
                     label(r"one instruction, \ one step", font_size=20, color=DATA))
        cpu[1].move_to(cpu[0])
        cpu.next_to(cells, DOWN, buff=0.8)
        ar = DoubleArrow(cpu.get_top(), cells[3].get_bottom(), buff=0.08, color=GREY_B, stroke_width=2,
                         tip_length=0.14)
        pts = VGroup(
            label(r"the \textbf{RAM}: \ memory cells with addresses; \ read, \ write, \ add, \ compare, \ jump: "
                  r"\ each one step", font_size=21, color=GREY_A),
            label(r"the \textbf{word-RAM}: \ a cell holds $w$ bits, \ with $w \ge \log_2 n$ \ (enough to hold an "
                  r"address)", font_size=21, color=GREY_A),
            label(r"Pebble is one: \ 32-bit words, \ and instructions that cost a cycle or a few", font_size=21,
                  color=YES),
            label(r"state the word width and allowed operations; \ count within that model",
                  font_size=21, color=HEAD),
        ).arrange(DOWN, buff=0.15).to_edge(DOWN, buff=0.4)
        with self.voiceover(
            (
            "An algorithm needs a declared cost model. <bookmark mark='a'/> A RAM gives memory cells addresses "
            "and charges for a specified set of instructions: reads, writes, arithmetic, comparisons and jumps. "
            "<bookmark mark='b'/> A word-RAM holds w bits per cell. Its word must address the input, so w is at "
            "least logarithmic in n; its allowed operations and their word widths are part of the definition. "
            "<bookmark mark='c'/> Pebble is a concrete thirty-two-bit example within its address and arithmetic "
            "limits. <bookmark mark='d'/> Counting those steps lets us compare algorithms in that model. Seconds "
            "still depend on the implementation, memory hierarchy and machine."
        )
        ) as vo:
            self.play(FadeIn(head), FadeIn(cells), FadeIn(addr), FadeIn(cpu), GrowArrow(ar))
            vo.wait_until("a")
            self.play(FadeIn(pts[0]))
            vo.wait_until("b")
            self.play(FadeIn(pts[1]))
            vo.wait_until("c")
            self.play(FadeIn(pts[2]))
            vo.wait_until("d")
            self.play(FadeIn(pts[3]))
        self.wait(0.3)
        self.clear_scene()

    def pitfall(self):
        d = load("ram")
        head = label(r"The pitfall of unit cost", font_size=34).to_edge(UP, buff=0.3)
        src = code(["x = 3", "repeat n times:", "    x = x * x        # one step?"], size=20,
                   color=CODE).to_edge(LEFT, buff=0.7).shift(UP * 1.6)
        rows = [r for r in d["rows"] if r["step"] >= 8]
        ax = Axes(x_range=[8, rows[-1]["step"] + 1, 2], y_range=[-7, 1, 2], x_length=6.0, y_length=3.6,
                  axis_config={"color": GREY_D, "include_numbers": False}).to_edge(RIGHT, buff=0.6).shift(DOWN * 0.4)
        pts = [ax.c2p(r["step"], np.log10(max(r["seconds"], 1e-7))) for r in rows]
        line = VMobject(color=NO, stroke_width=3).set_points_as_corners(pts)
        dots = VGroup(*[Dot(p, radius=0.05, color=NO) for p in pts])
        yt = VGroup(*[label(t, font_size=15, color=GREY_B).next_to(ax.c2p(8, v), LEFT, buff=0.1)
                      for v, t in ((-6, r"1 $\mu$s"), (-3, r"1 ms"), (0, r"1 s"))])
        xt = VGroup(*[mono(str(k), 14, GREY_B).next_to(ax.c2p(k, -7), DOWN, buff=0.08) for k in (8,12,16,20)])
        xl = label(r"squaring number", font_size=17, color=GREY_B).next_to(ax, DOWN, buff=0.2)
        yl = label(r"time for that one multiplication, \ CPython, \ this machine", font_size=17,
                   color=GREY_B).next_to(ax, UP, buff=0.1)
        last = d["rows"][-1]
        pts2 = VGroup(
            label(r"after $n$ squarings, \ $x = 3^{2^n}$ \ has about $1.6 \cdot 2^n$ bits", font_size=21, color=GREY_A),
            label(rf"step {last['step']}: \ a {words(last['bits'])}-bit number, \ "
                  rf"{human_time(last['seconds'])} for one ``step''", font_size=21, color=NO),
            VGroup(label(r"a unit-cost RAM with unbounded words", font_size=20, color=HEAD),
                   label(r"hides operand growth; \ multiword arithmetic needs its own cost", font_size=20,
                         color=HEAD)).arrange(DOWN, aligned_edge=LEFT, buff=0.08),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.16).to_edge(LEFT, buff=0.7).shift(DOWN * 0.6)
        if pts2.width > 5.4:
            pts2.scale_to_fit_width(5.4)
        with self.voiceover(
            (
            "Why bound the word size? <bookmark mark='a'/> Starting from three, square the result n times. The "
            "answer is three raised to two to the n, with about one point six times two to the n bits. Calling "
            "every multiplication one step hides an exponentially growing operand. <bookmark mark='b'/> Here are "
            "host Python measurements: the minimum of three same-operand squarings at each step, with the result "
            "checked outside the timer. Small values are dominated by timing and interpreter overhead; large "
            "values require real multiword arithmetic. No fixed threefold timing ratio is promised. <bookmark "
            "mark='c'/> A word-RAM operation handles a bounded number of words. An arbitrary-precision "
            "multiplication needs its own cost analysis."
        )
        ) as vo:
            self.play(FadeIn(head), FadeIn(src))
            vo.wait_until("a")
            self.play(FadeIn(pts2[0]))
            vo.wait_until("b")
            self.play(Create(ax), FadeIn(yt), FadeIn(xt), FadeIn(xl), FadeIn(yl))
            self.play(Create(line), FadeIn(dots), FadeIn(pts2[1]), run_time=2)
            vo.wait_until("c")
            self.play(FadeIn(pts2[2]))
        self.wait(0.3)
        self.clear_scene()

    def others(self):
        head = label(r"Other ways to count", font_size=34).to_edge(UP, buff=0.3)
        rows = VGroup(
            VGroup(label(r"Turing machine \ (Part 2)", font_size=22, color=LAM),
                   label(r"polynomial simulation overhead for standard logarithmic-word RAMs; \ bounded operands required", font_size=20, color=GREY_A)).arrange(DOWN, aligned_edge=LEFT, buff=0.08),
            VGroup(label(r"comparison model", font_size=22, color=YES),
                   label(r"count only comparisons between keys: \ the model of chapter 6's lower bound", font_size=20,
                         color=GREY_A)).arrange(DOWN, aligned_edge=LEFT, buff=0.08),
            VGroup(label(r"cell-probe model \ (Yao, \ 1981)", font_size=22, color=DATA),
                   label(r"count only memory accesses, \ computation free: \ the strongest lower bounds for data "
                         r"structures", font_size=20, color=GREY_A)).arrange(DOWN, aligned_edge=LEFT, buff=0.08),
            VGroup(label(r"external memory \ (Aggarwal and Vitter, \ 1988)", font_size=22, color=CTRL),
                   label(r"count block transfers: \ Part 9's caches, \ and chapter 14's disks", font_size=20,
                         color=GREY_A)).arrange(DOWN, aligned_edge=LEFT, buff=0.08),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.35).next_to(head, DOWN, buff=0.55)
        note = label(r"choose the model that matches the cost you care about", font_size=23,
                     color=HEAD).to_edge(DOWN, buff=0.5)
        with self.voiceover(
            (
            "Different questions charge for different resources. <bookmark mark='a'/> A standard logarithmic-word "
            "RAM with an effectively simulable instruction set can be simulated by a Turing machine with "
            "polynomial overhead. That statement needs bounded operands; it does not grant free arithmetic on "
            "arbitrary integers. <bookmark mark='b'/> The comparison model counts comparisons between keys. Its "
            "lower bound will assume distinct keys. <bookmark mark='c'/> The cell-probe model charges for memory "
            "accesses while allowing free computation between probes, which makes some lower bounds especially "
            "strong. <bookmark mark='d'/> The external-memory model counts block transfers between memory levels. "
            "<bookmark mark='e'/> Declare the resource before quoting the bound."
        )
        ) as vo:
            self.play(FadeIn(head))
            for mk, r in zip("abcd", rows):
                vo.wait_until(mk)
                self.play(FadeIn(r, shift=RIGHT * 0.1))
            vo.wait_until("e")
            self.play(FadeIn(note))
        self.wait(0.3)
        self.clear_scene()
