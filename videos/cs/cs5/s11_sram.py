from __future__ import annotations

import numpy as np

from explainer.cs import *  # noqa: F403
from videos.cs.cs5.common import BG, CLOCK, CODE, COST, CTRL, DATA, FUNC, HEAD, INF, NO, PART, WIRE, YES, gate, load


class Sram(VoiceoverScene):
    def construct(self):
        self.card()
        self.cell()
        self.sense()
        self.array()

    def card(self):
        card = chapter_card(10, r"Static memory", r"How do you build a million bits?", part=PART)
        with self.voiceover("Chapter ten. Static memory."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]), FadeIn(card[2]))
        self.play(FadeOut(card))

    # ------------------------------------------------------------------
    def cell(self):
        head = label(r"The 6-transistor SRAM cell", font_size=38).to_edge(UP, buff=0.35)
        g1 = gate("NOT", size=0.8).move_to(UP * 0.9)
        g2 = gate("NOT", size=0.8).rotate(PI).move_to(DOWN * 0.3)
        loop = VGroup(
            VMobject(color=WIRE, stroke_width=3).set_points_as_corners([g1.out(), g1.out() + RIGHT * 0.5,
                                                                       g2.inp[0]() + RIGHT * 0.5, g2.inp[0]()]),
            VMobject(color=WIRE, stroke_width=3).set_points_as_corners([g2.out(), g2.out() + LEFT * 0.5,
                                                                       g1.inp[0]() + LEFT * 0.5, g1.inp[0]()]))
        L, R = g1.inp[0]()[0] - 0.5, g1.out()[0] + 0.5
        bl = Line([L - 1.6, 2.4, 0], [L - 1.6, -1.2, 0], color=DATA, stroke_width=3)
        blb = Line([R + 1.6, 2.4, 0], [R + 1.6, -1.2, 0], color=DATA, stroke_width=3)
        wl = Line([L - 2.4, 1.9, 0], [R + 2.4, 1.9, 0], color=HEAD, stroke_width=3)
        acc1 = VGroup(Square(0.35, color=HEAD, stroke_width=2).move_to([L - 0.8, 0.3, 0]))
        acc2 = VGroup(Square(0.35, color=HEAD, stroke_width=2).move_to([R + 0.8, 0.3, 0]))
        links = VGroup(Line([L, 0.3, 0], acc1.get_right(), color=WIRE, stroke_width=2),
                       Line(acc1.get_left(), [L - 1.6, 0.3, 0], color=WIRE, stroke_width=2),
                       Line([R, 0.3, 0], acc2.get_left(), color=WIRE, stroke_width=2),
                       Line(acc2.get_right(), [R + 1.6, 0.3, 0], color=WIRE, stroke_width=2),
                       Line(acc1.get_top(), [L - 0.8, 1.9, 0], color=HEAD, stroke_width=2),
                       Line(acc2.get_top(), [R + 0.8, 1.9, 0], color=HEAD, stroke_width=2))
        labs = VGroup(MathTex(r"\text{bit line}", font_size=22, color=DATA).next_to(bl, DOWN, buff=0.1),
                      MathTex(r"\overline{\text{bit line}}", font_size=22, color=DATA).next_to(blb, DOWN, buff=0.1),
                      MathTex(r"\text{word line}", font_size=22, color=HEAD).next_to(wl, UP, buff=0.1))
        notes = VGroup(
            label(r"two cross-coupled inverters \ (4 transistors): \ the latch of chapter 2", font_size=24, color=YES),
            label(r"two access transistors connect it to the bit lines \ when the word line is high", font_size=24,
                  color=HEAD),
            label(r"read: \ the cell tilts the two precharged bit lines apart; \\ a \textit{sense amplifier}, \ itself a "
                  r"latch, \ amplifies the difference", font_size=24, color=GREY_A),
            label(r"write: \ strong drivers on the bit lines overpower the little inverters", font_size=24,
                  color=GREY_A),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.2).to_edge(DOWN, buff=0.3)
        vbl = MathTex(r"V", font_size=24, color=DATA).next_to(bl, RIGHT, buff=0.12).shift(DOWN * 1.2)
        vblb = MathTex(r"V - \delta", font_size=24, color=NO).next_to(blb, LEFT, buff=0.12).shift(DOWN * 1.2)
        with self.voiceover(
            "A register file of flip-flops is fast but large. For memories of millions of bits, a common compact "
            "choice is the six-transistor cell shown here. <bookmark mark='a'/> At its heart is chapter two's "
            "latch again: two cross-coupled inverters, four transistors, with two stable states. <bookmark "
            "mark='b'/> Two more transistors, switched by a word line, connect the two sides of the latch to a "
            "pair of bit lines. Six transistors in all: the static RAM cell, which retains its bit while powered "
            "within its operating margins. <bookmark mark='c'/> To read, both bit lines are charged up, and the "
            "word line opens the cell; the cell pulls one of them down slightly. That tiny difference is too weak "
            "to use directly, so a sense amplifier, which is yet another cross-coupled latch, balanced right on "
            "its saddle, falls one way or the other and turns it into a full zero or one. To write, strong "
            "drivers force the bit lines, and the cell's small inverters give in."
        ) as vo:
            self.play(FadeIn(head), FadeIn(g1), FadeIn(g2), Create(loop), FadeIn(notes[0]))
            vo.wait_until("a")
            self.play(Indicate(VGroup(g1, g2, loop), scale_factor=1.03))
            vo.wait_until("b")
            self.play(Create(bl), Create(blb), Create(wl), FadeIn(acc1), FadeIn(acc2), Create(links), FadeIn(labs),
                      FadeIn(notes[1]))
            vo.wait_until("c")
            self.play(bl.animate.set_stroke(width=6), blb.animate.set_stroke(width=6), FadeIn(notes[2]))
            self.play(wl.animate.set_stroke(width=6), FadeIn(vbl))
            self.play(blb.animate.set_stroke(opacity=0.45), FadeIn(vblb))
            self.play(FadeIn(notes[3]))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def sense(self):
        d = load("phase")
        head = label(r"The sense amplifier: \ a latch balanced on purpose", font_size=36).to_edge(UP, buff=0.35)
        ax = Axes(x_range=[0, 1, 0.5], y_range=[0, 1, 0.5], x_length=4.6, y_length=4.6, tips=False,
                  axis_config={"color": GREY_C, "font_size": 18, "include_numbers": True}).move_to(LEFT * 3.6 + DOWN * 0.4)
        axl = VGroup(MathTex("v_1", font_size=26, color=GREY_A).next_to(ax.x_axis, DOWN, buff=0.35),
                     MathTex("v_2", font_size=26, color=GREY_A).next_to(ax.y_axis, LEFT, buff=0.35))
        diag = DashedLine(ax.c2p(0, 0), ax.c2p(1, 1), color=NO, stroke_width=2)
        GAIN = 6.0

        def f(v):
            return 0.5 * (1 - np.tanh(GAIN * (v - 0.5)))

        def path(d0, T=6.0, dt=0.01):
            v1, v2 = 0.5 + d0 / 2, 0.5 - d0 / 2
            pts = [(v1, v2)]
            for _ in range(int(T / dt)):
                v1, v2 = v1 + dt * (f(v2) - v1), v2 + dt * (f(v1) - v2)
                pts.append((v1, v2))
            return VMobject(color=HEAD, stroke_width=3).set_points_as_corners([ax.c2p(x, y) for x, y in pts[::4]])

        tr = VGroup(path(0.02), path(-0.02), path(0.002))
        st = VGroup(*[Dot(ax.c2p(*p), radius=0.1, color=YES) for p in d["stable"]])
        steps = VGroup(
            label(r"1. \ precharge: \ normalized model: balanced \\ near the unstable operating point", font_size=24,
                  color=GREY_A),
            label(r"2. \ the cell nudges the bit lines \\ a few percent apart", font_size=24, color=GREY_A),
            label(r"3. \ release: \ the latch falls toward the side \\ it was nudged to, \ amplifying the "
                  r"difference \\ exponentially: \ $\delta(t) = \delta_0\, e^{\lambda t}$", font_size=24, color=HEAD),
            label(r"chapter 2's danger, \ used as an amplifier: \\ a smaller nudge just takes longer, \\ "
                  r"$t = \tfrac{1}{\lambda}\ln(1/\delta_0)$", font_size=24, color=YES),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.32).move_to(RIGHT * 2.9 + DOWN * 0.3)
        with self.voiceover(
            "An idealized regenerative sense amplifier reuses chapter two's instability. <bookmark mark='a'/> It "
            "is a latch too, but one that is deliberately parked on its saddle: the two internal nodes are first "
            "balanced near an unstable operating point. Real circuits choose suitable bias and common-mode "
            "voltages; this normalized phase portrait illustrates the regeneration. <bookmark mark='b'/> Then the "
            "bit lines, nudged a few percent apart by the cell, are connected to it. <bookmark mark='c'/> When it "
            "is released, the instability that makes metastability dangerous does useful work: the imbalance "
            "grows exponentially, and the latch falls quickly to the side it was nudged towards, turning a "
            "whisper into a full zero or one. A smaller nudge simply takes longer to resolve, which is chapter "
            "five's tail again, and why memory designers specify the smallest signal their amplifiers can read in "
            "time."
        ) as vo:
            self.play(FadeIn(head), Create(ax), FadeIn(axl), Create(diag), FadeIn(st))
            vo.wait_until("a")
            self.play(FadeIn(steps[0]), FadeIn(Dot(ax.c2p(0.5, 0.5), radius=0.1, color=NO)))
            vo.wait_until("b")
            self.play(FadeIn(steps[1]))
            vo.wait_until("c")
            self.play(LaggedStart(*[Create(t) for t in tr], lag_ratio=0.4), FadeIn(steps[2]), run_time=3.0)
            self.play(FadeIn(steps[3]))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def array(self):
        head = label(r"Cells in a grid", font_size=38).to_edge(UP, buff=0.35)
        n = 8
        grid = VGroup(*[Square(0.42, stroke_color=GREY_D, stroke_width=1, fill_color=YES, fill_opacity=0.18)
                        for _ in range(n * n)]).arrange_in_grid(n, n, buff=0.08).move_to(LEFT * 2.9 + UP * 0.15)
        row = 5
        rowhl = SurroundingRectangle(VGroup(*grid[row * n:(row + 1) * n]), buff=0.04, color=HEAD)
        dec = RoundedRectangle(width=1.0, height=grid.height, corner_radius=0.08, stroke_color=CTRL,
                               stroke_width=2).next_to(grid, LEFT, buff=0.3)
        dl = MathTex(r"\text{row}\\ \text{decoder}", font_size=22, color=CTRL).move_to(dec)
        sa = RoundedRectangle(width=grid.width, height=0.5, corner_radius=0.08, stroke_color=HEAD,
                              stroke_width=2).next_to(grid, DOWN, buff=0.25)
        sl = MathTex(r"\text{sense amplifiers}", font_size=22, color=HEAD).move_to(sa)
        cm = RoundedRectangle(width=grid.width * 0.6, height=0.45, corner_radius=0.08, stroke_color=CTRL,
                              stroke_width=2).next_to(sa, DOWN, buff=0.2)
        cml = MathTex(r"\text{column mux}", font_size=22, color=CTRL).move_to(cm)
        cols = (2, 3)
        colhl = VGroup(*[SurroundingRectangle(grid[row * n + c], buff=0.02, color=YES, stroke_width=3) for c in cols])
        outa = Arrow(cm.get_bottom(), cm.get_bottom() + DOWN * 0.45, buff=0, color=YES, stroke_width=3)
        addr = MathTex(r"\text{address} = \underbrace{\texttt{101}}_{\text{row}}\,"
                       r"\underbrace{\texttt{01}}_{\text{column}}", font_size=26, color=DATA).next_to(dec, UP, buff=0.3)
        addr.align_to(dec, LEFT)
        side = VGroup(
            label(r"the address picks one row: \ every cell in it \\ drives its bit lines at once", font_size=24,
                  color=GREY_A),
            label(r"a column multiplexer \ picks the bits wanted", font_size=24, color=GREY_A),
            label(r"a cache of a megabyte \ is millions of these cells \ (Part 9)", font_size=24, color=YES),
            label(r"about 120 to 150 $F^2$ of silicon per bit \\ ($F$: the smallest feature size)", font_size=22,
                  color=GREY_B),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.3).next_to(grid, RIGHT, buff=0.7).shift(DOWN * 0.2)
        with self.voiceover(
            "Memories put their cells in a grid. <bookmark mark='a'/> The address splits in two. The high part "
            "goes to a row decoder, which raises one word line, and every cell in that row connects to its bit "
            "lines at once. <bookmark mark='b'/> A row of sense amplifiers reads them all, and a multiplexer "
            "picks out the bits that were asked for. <bookmark mark='c'/> Many processor caches use SRAM arrays "
            "like this, though some use other memory technologies, millions of cells, and Part 9 is about how "
            "they are organized. A large server processor carries hundreds of megabytes of it, billions of these "
            "cells, and still finds them too few. Fast as it is, static RAM is big: six transistors and their "
            "wiring for every bit, so on many chips the caches take more area than the processor cores "
            "themselves. Main memory needs something much denser."
        ) as vo:
            self.play(FadeIn(head), FadeIn(grid, lag_ratio=0.005))
            vo.wait_until("a")
            self.play(FadeIn(addr), FadeIn(dec), FadeIn(dl))
            self.play(Create(rowhl), *[grid[row * n + c].animate.set_fill(YES, 0.6) for c in range(n)], FadeIn(side[0]))
            vo.wait_until("b")
            self.play(FadeIn(sa), FadeIn(sl), FadeIn(side[1]))
            self.play(FadeIn(cm), FadeIn(cml), Create(colhl), GrowArrow(outa))
            vo.wait_until("c")
            self.play(FadeIn(side[2]), FadeIn(side[3]))
        self.wait(0.3)
        self.clear_scene()
