from __future__ import annotations

import math

import numpy as np

from explainer.cs import *  # noqa: F403
from videos.cs.cs28.common import (BG, CTRL, DATA, HEAD, LAM, NO, PART, YES, bit_row, fit_right, grid_table, load,
                                   mono)

# positions 1..7 by region of the Venn diagram: circle A = p1 {1,3,5,7}, B = p2 {2,3,6,7}, C = p4 {4,5,6,7}
REGION = {1: (-1.25, 0.85), 2: (1.25, 0.85), 4: (0.0, -1.5), 3: (0.0, 1.3), 5: (-0.95, -0.45), 6: (0.95, -0.45),
          7: (0.0, 0.1)}
NAMES = {1: "p_1", 2: "p_2", 3: "d_1", 4: "p_4", 5: "d_2", 6: "d_3", 7: "d_4"}


class Hamming(VoiceoverScene):
    def construct(self):
        self.card()
        self.venn()
        self.matrix()
        self.family()
        self.curves()

    def card(self):
        card = chapter_card(3, r"Hamming(7,4)", r"How can three check bits find the bad one?", lit=(1947, 1950),
                            extra=((1950, r"Hamming, \ \textit{Bell System Technical Journal}"),), part=PART)
        with self.voiceover("Chapter three. Hamming's code."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]), FadeIn(card[2]))
        self.play(FadeOut(card))

    def venn(self):
        h = load("hamming")
        head = label(r"Three overlapping parity checks", font_size=34).to_edge(UP, buff=0.3)
        o = np.array([-3.6, -0.6, 0])
        circ = VGroup(Circle(radius=1.75, color=DATA, stroke_width=3).move_to(o + np.array([-0.75, 0.55, 0])),
                      Circle(radius=1.75, color=HEAD, stroke_width=3).move_to(o + np.array([0.75, 0.55, 0])),
                      Circle(radius=1.75, color=LAM, stroke_width=3).move_to(o + np.array([0.0, -0.75, 0])))
        cn = VGroup(label(r"check A", font_size=19, color=DATA).next_to(circ[0], UL, buff=-0.2),
                    label(r"check B", font_size=19, color=HEAD).next_to(circ[1], UR, buff=-0.2),
                    label(r"check C", font_size=19, color=LAM).next_to(circ[2], DOWN, buff=0.1))
        cw, fl = h["codeword"], h["flipped"]
        vals = VGroup(*[mono(str(cw[i - 1]), 30, WHITE).move_to(o + np.array([*REGION[i], 0])) for i in range(1, 8)])
        names = VGroup(*[MathTex(NAMES[i], font_size=20, color=GREY_B).next_to(vals[i - 1], DOWN, buff=0.04)
                         for i in range(1, 8)])
        bad = 5
        newv = mono(str(fl[bad - 1]), 30, NO).move_to(vals[bad - 1])
        lines = VGroup(
            label(rf"four data bits \ ({''.join(map(str, h['data']))}) \ sit in the overlaps; \\ three check bits "
                  r"make each circle's count of 1s \textbf{even}", font_size=22, color=WHITE),
            label(r"seven bits sent: \ rate $\tfrac47$", font_size=22, color=GREY_A),
            label(r"the channel flips $d_2$", font_size=22, color=NO),
            label(r"circles A and C are now odd, \ B is even: \\ the bad bit is in A and C but not B: \ $d_2$",
                  font_size=22, color=YES),
            label(r"each of the 7 positions has a different pattern of circles, \\ so every single flip is "
                  r"located, \ and flipped back", font_size=22, color=HEAD),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.32).next_to(circ, RIGHT, buff=0.9).align_to(circ, UP)
        fit_right(lines)
        with self.voiceover(
            "Hamming's construction fits in a picture. <bookmark mark='a'/> Draw three overlapping circles. Put the "
            "four data bits, here one zero one one, in the four overlapping regions, and choose a check bit for each "
            "circle's private region so that every circle contains an even number of ones. <bookmark mark='b'/> "
            "Seven bits are sent for four of data. <bookmark mark='c'/> Now the channel flips one of them. "
            "<bookmark mark='d'/> The receiver recounts: circles A and C are odd, B is still even. The flipped bit "
            "must lie inside A and C and outside B, and only one region does: it is d two. <bookmark mark='e'/> "
            "Every one of the seven positions sits in a different combination of circles, so any single flip is "
            "located and corrected, and with no flips, every circle is even."
        ) as vo:
            self.play(FadeIn(head), Create(circ), FadeIn(cn))
            vo.wait_until("a")
            self.play(FadeIn(VGroup(*[vals[i - 1] for i in (3, 5, 6, 7)])),
                      FadeIn(VGroup(*[names[i - 1] for i in (3, 5, 6, 7)])), FadeIn(lines[0]))
            self.play(FadeIn(VGroup(*[vals[i - 1] for i in (1, 2, 4)])),
                      FadeIn(VGroup(*[names[i - 1] for i in (1, 2, 4)])))
            vo.wait_until("b")
            self.play(FadeIn(lines[1]))
            vo.wait_until("c")
            self.play(Transform(vals[bad - 1], newv), FadeIn(lines[2]))
            vo.wait_until("d")
            self.play(circ[0].animate.set_stroke(NO, width=6), circ[2].animate.set_stroke(NO, width=6),
                      circ[1].animate.set_stroke(YES, width=5), FadeIn(lines[3]))
            self.play(Indicate(vals[bad - 1], color=NO, scale_factor=1.5))
            vo.wait_until("e")
            self.play(FadeIn(lines[4]))
        self.wait(0.3)
        self.clear_scene()

    def matrix(self):
        h = load("hamming")
        head = label(r"The syndrome names the position", font_size=34).to_edge(UP, buff=0.3)
        cols = [[(j >> i) & 1 for j in range(1, 8)] for i in (2, 1, 0)]
        H = Matrix(cols, element_to_mobject=lambda v: MathTex(str(v), font_size=30), h_buff=0.6,
                   v_buff=0.6).scale(0.85)
        Hl = MathTex(r"H =", font_size=34).next_to(H, LEFT)
        pos = VGroup(*[label(str(j), font_size=18, color=GREY_A).next_to(H.get_columns()[j - 1], UP, buff=0.25)
                       for j in range(1, 8)])
        grp = VGroup(Hl, H, pos).next_to(head, DOWN, buff=0.6).to_edge(LEFT, buff=1.2)
        col5 = SurroundingRectangle(H.get_columns()[4], color=NO, buff=0.08)
        r = bit_row(h["flipped"], size=0.45, font=22, labels=[str(i) for i in range(1, 8)])
        rl = label(r"received:", font_size=20, color=GREY_A)
        rgrp = VGroup(rl, r).arrange(RIGHT, buff=0.3).next_to(grp, DOWN, buff=0.6).align_to(grp, LEFT)
        r.boxes[4].set_stroke(NO, width=4)
        syn = MathTex(r"H r^{\mathsf T} = \begin{pmatrix} 1 \\ 0 \\ 1 \end{pmatrix} = 5", font_size=36,
                      color=NO).next_to(rgrp, DOWN, buff=0.45).align_to(grp, LEFT)
        lines = VGroup(
            label(r"column $j$ of $H$ is $j$ written in binary", font_size=22, color=WHITE),
            label(r"a codeword satisfies $H c^{\mathsf T} = 0$: \\ each row is one of the three circles", font_size=22,
                  color=GREY_A),
            label(r"one flip at position $j$ adds column $j$: \\ the \textbf{syndrome} $H r^{\mathsf T}$ \textbf{is} "
                  r"$j$ in binary", font_size=22, color=NO),
            label(r"$2^r - 1$ positions, \ $r$ checks: \\ Hamming(15,11), \ (31,26), \ $\ldots$", font_size=22,
                  color=DATA),
            label(r"\textbf{perfect}: \ the balls of radius 1 around \\ the 16 codewords cover all $2^7 = 128$ words "
                  r"exactly \ ($16 \times 8$)", font_size=22, color=YES),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.3).next_to(grp, RIGHT, buff=1.0).align_to(grp, UP)
        fit_right(lines)
        with self.voiceover(
            "The same code as a matrix. <bookmark mark='a'/> Write the numbers one to seven in binary as the columns "
            "of a three-row matrix H. <bookmark mark='b'/> Codewords are the words that H sends to zero; each row of "
            "H is one of the three circles. <bookmark mark='c'/> If the channel flips position j, multiplying by H "
            "gives column j: the syndrome spells out the position of the error in binary. Our flipped word gives one "
            "zero one: five. <bookmark mark='d'/> The construction works for any number of checks r: two to the r "
            "minus one positions, all but r of them data. <bookmark mark='e'/> And the code is perfect: the balls "
            "of radius one around the sixteen codewords each hold eight words, and together they cover all a hundred "
            "and twenty-eight words of length seven exactly once. No space is wasted."
        ) as vo:
            self.play(FadeIn(head), FadeIn(grp))
            vo.wait_until("a")
            self.play(FadeIn(lines[0]))
            vo.wait_until("b")
            self.play(FadeIn(lines[1]))
            vo.wait_until("c")
            self.play(FadeIn(rgrp), FadeIn(lines[2]))
            self.play(Create(col5), Write(syn))
            for mk, ln in zip("de", lines[3:]):
                vo.wait_until(mk)
                self.play(FadeIn(ln, shift=UP * 0.1))
        self.wait(0.3)
        self.clear_scene()

    def family(self):
        head = label(r"The Hamming family", font_size=34).to_edge(UP, buff=0.35)
        rows = []
        for r in range(2, 8):
            n = 2 ** r - 1
            k = n - r
            rows.append([str(r), f"({n}, {k})", f"{k / n:.3f}", r"1"])
        rows.append([r"8 + 1", r"(72, 64)", f"{64 / 72:.3f}", r"1, \ and detects 2"])
        tab = grid_table([r"checks $r$", r"$(n, k)$", r"rate", r"errors corrected"], rows,
                         widths=[2.2, 2.6, 2.0, 3.6], row_h=0.42, font_size=21, mono_cols=(),
                         colors=[[WHITE, DATA, YES, HEAD]] * 6 + [[WHITE, DATA, YES, LAM]])
        tab.next_to(head, DOWN, buff=0.4).set_x(0)
        lines = VGroup(
            label(r"the rate climbs towards 1 as the blocks grow, \ but each block still corrects only \textbf{one} "
                  r"error", font_size=22, color=WHITE),
            label(r"so long Hamming codes only suit channels where errors are rare: \ like memory", font_size=22,
                  color=HEAD),
            label(r"the last row: \ 64 data bits, \ 7 Hamming checks, \ 1 overall parity: \ the ECC word of a "
                  r"server's DIMM", font_size=22, color=LAM),
        ).arrange(DOWN, buff=0.25).next_to(tab, DOWN, buff=0.4)
        with self.voiceover(
            "Hamming's construction gives a whole family. <bookmark mark='a'/> With r checks the block has two to "
            "the r minus one bits, and the rate climbs towards one: a hundred and twenty bits of data for seven "
            "checks at r equals seven. But every block, however long, still corrects only a single error. "
            "<bookmark mark='b'/> So long Hamming codes suit channels where errors are rare and isolated, such as "
            "memory. <bookmark mark='c'/> The last row is the one in your server: sixty-four data bits, seven "
            "Hamming checks and one overall parity bit, seventy-two bits per memory word."
        ) as vo:
            self.play(FadeIn(head), FadeIn(VGroup(*tab.cells[0])), FadeIn(tab.rule))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(VGroup(*row)) for row in tab.cells[1:7]], lag_ratio=0.3),
                      FadeIn(lines[0]), run_time=3.0)
            vo.wait_until("b")
            self.play(FadeIn(lines[1]))
            vo.wait_until("c")
            self.play(FadeIn(VGroup(*tab.cells[7])), FadeIn(lines[2]))
        self.wait(0.3)
        self.clear_scene()

    def curves(self):
        h = load("hamming")
        head = label(r"What a code buys, \ measured", font_size=34).to_edge(UP, buff=0.3)
        ax = Axes(x_range=[0, 2.5, 0.5], y_range=[0, 6, 1], x_length=6.0, y_length=4.2,
                  axis_config={"color": GREY_D, "include_numbers": False}).next_to(head, DOWN, buff=0.55).to_edge(
            LEFT, buff=1.0)
        lg = math.log10
        xt = VGroup(*[label(t, font_size=15, color=GREY_A).next_to(ax.c2p(x + 3, 0), DOWN, buff=0.08)
                      for x, t in ((-3, r"0.001"), (-2, r"0.01"), (-1, r"0.1"))])
        yt = VGroup(*[label(rf"$10^{{{y}}}$", font_size=15, color=GREY_A).next_to(ax.c2p(0, y + 6), LEFT, buff=0.08)
                      for y in (-6, -4, -2, 0)])
        xl = label(r"channel flip probability $p$", font_size=17, color=GREY_A).next_to(ax, DOWN, buff=0.35)
        yl = label(r"bit error after decoding", font_size=17, color=GREY_A).rotate(PI / 2).next_to(ax, LEFT,
                                                                                                     buff=0.5)

        def curve(key, color):
            pts = [ax.c2p(lg(c["p"]) + 3, max(0, lg(c[key]) + 6)) for c in h["curves"] if lg(c["p"]) <= -0.5]
            return VMobject(color=color, stroke_width=3).set_points_smoothly(pts)
        cn, cr, ch = curve("none", GREY_B), curve("rep3", DATA), curve("ham_bit", YES)
        keys = VGroup(label(r"no code \ (rate 1)", font_size=18, color=GREY_B),
                      label(r"repetition $\times 3$ \ (rate $\tfrac13$)", font_size=18, color=DATA),
                      label(r"Hamming(7,4) \ (rate $\tfrac47$)", font_size=18, color=YES)).arrange(
            DOWN, aligned_edge=LEFT, buff=0.12).move_to(ax.c2p(0.65, 5.1))
        s1 = next(s for s in h["sim"] if s["p"] == 0.01)
        notes = VGroup(
            label(rf"at $p = 0.01$: \ Hamming leaves {s1['exact'] * 1e4:.1f} errors in 10{{,}}000 \\ instead of "
                  r"100, \ spending only 3 bits per 4", font_size=21, color=YES),
            label(r"simulated: \ 20{,}000 blocks per point \\ agree with the exact curve", font_size=21, color=GREY_A),
            label(r"\textbf{ECC memory}: \ Hamming plus one parity bit \\ (SECDED) \ guards every 64-bit word \\ "
                  r"with 8 check bits", font_size=21, color=HEAD),
            label(r"it corrects one flip, \ detects two: \\ part of the defence against cosmic rays \\ and Rowhammer \ (Part 5)",
                  font_size=21, color=DATA),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.3).next_to(ax, RIGHT, buff=0.7).align_to(ax, UP)
        fit_right(notes)
        with self.voiceover(
            "How much does it help? <bookmark mark='a'/> On a log scale: with no code, the error rate is just p. "
            "Three-fold repetition squares it, roughly, at a third of the rate. Hamming's code does almost as well at "
            "four sevenths of the rate. At one flip in a hundred, Hamming leaves under nine errors in ten thousand "
            "instead of a hundred. <bookmark mark='b'/> The simulated points agree with the exact curves. <bookmark "
            "mark='c'/> Hamming codes are still everywhere. Error-correcting memory stores each 64-bit word with "
            "eight check bits: a Hamming code plus one overall parity bit. <bookmark mark='d'/> It corrects any "
            "single flip and detects any two: part of the defence against cosmic rays, and against the Rowhammer "
            "attack of Part 5, though attackers have since found ways to flip several bits at once."
        ) as vo:
            self.play(FadeIn(head), Create(ax), FadeIn(xt), FadeIn(yt), FadeIn(xl), FadeIn(yl))
            vo.wait_until("a")
            self.play(Create(cn), FadeIn(keys[0]))
            self.play(Create(cr), FadeIn(keys[1]))
            self.play(Create(ch), FadeIn(keys[2]), FadeIn(notes[0]))
            for mk, n_ in zip("bcd", notes[1:]):
                vo.wait_until(mk)
                self.play(FadeIn(n_))
        self.wait(0.3)
        self.clear_scene()
