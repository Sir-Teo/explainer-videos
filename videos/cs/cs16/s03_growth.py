from __future__ import annotations

import math

import numpy as np

from explainer.cs import *  # noqa: F403
from videos.cs.cs16.common import (CODE, COST, CTRL, DATA, FUNC, HEAD, LAM, NO, PART, YES, grid_table, load, mono)

FN_COLOR = {"lg n": YES, "n": DATA, "n lg n": FUNC, "n^2": CTRL, "n^3": NO, "2^n": COST}
FN_TEX = {"lg n": r"\lg n", "n": r"n", "n lg n": r"n \lg n", "n^2": r"n^2", "n^3": r"n^3", "2^n": r"2^n"}


def _sci(n):
    if n >= 10 ** 15:
        e = int(math.log10(n))
        return rf"$10^{{{e}}}$"
    return f"{n:,}"


class Growth(VoiceoverScene):
    def construct(self):
        self.card()
        self.notation()
        self.ladder()
        self.stirling()

    def card(self):
        card = chapter_card(2, r"Orders of growth", r"What survives when constants are ignored?", lit=(1894,),
                            extra=((1894, r"Bachmann's $O$"),), part=PART)
        with self.voiceover("Chapter two. Orders of growth."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]), FadeIn(card[2]))
        self.play(FadeOut(card))

    def notation(self):
        head = label(r"Asymptotic notation, \ precisely", font_size=34).to_edge(UP, buff=0.3)
        defs = VGroup(
            MathTex(r"f = O(g) \iff \exists\, c > 0,\ n_0:\ \ f(n) \le c\, g(n) \text{ for all } n \ge n_0",
                    font_size=32),
            MathTex(r"f = \Omega(g) \iff g = O(f)", font_size=32),
            MathTex(r"f = \Theta(g) \iff f = O(g) \text{ and } f = \Omega(g)", font_size=32),
            MathTex(r"f = o(g) \iff f(n)/g(n) \to 0", font_size=32),
        ).arrange(DOWN, buff=0.35, aligned_edge=LEFT).next_to(head, DOWN, buff=0.5)
        ex = VGroup(
            MathTex(r"3n^2 + 100n + 7 = \Theta(n^2)", font_size=30, color=YES),
            label(r"constants and lower-order terms disappear: \ they depend on the machine, \ the growth does not",
                  font_size=21, color=GREY_A),
            label(r"Bachmann \ (1894) \ and Landau; \ Knuth \ (1976) \ fixed $\Omega$ and $\Theta$ as computer "
                  r"scientists use them", font_size=19, color=GREY_B),
        ).arrange(DOWN, buff=0.15).to_edge(DOWN, buff=0.45)
        with self.voiceover(
            "Counting steps exactly is often possible, but rarely necessary. <bookmark mark='a'/> We say f is big O "
            "of g if, beyond some point, f is at most a constant times g. <bookmark mark='b'/> Omega is the same "
            "bound from below, and Theta means both: f and g grow at the same rate. Little o means f becomes "
            "negligible next to g. <bookmark mark='c'/> So three n squared plus a hundred n plus seven is Theta of "
            "n squared. The constants depend on the machine, the compiler, the programmer. The growth rate does "
            "not, which is why it is what we compare. Paul Bachmann introduced the O in 1894; Donald Knuth fixed "
            "the meanings of Omega and Theta that computer scientists use, in 1976."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(Write(defs[0]))
            vo.wait_until("b")
            self.play(FadeIn(defs[1:]))
            vo.wait_until("c")
            self.play(FadeIn(ex))
        self.wait(0.3)
        self.clear_scene()

    def ladder(self):
        d = load("growth")
        head = label(r"The ladder", font_size=34).to_edge(UP, buff=0.3)
        ns = d["ns"]
        ax = Axes(x_range=[0, 30, 5], y_range=[0, 30, 5], x_length=5.4, y_length=4.2,
                  axis_config={"color": GREY_D, "include_numbers": False}).to_edge(LEFT, buff=0.7).shift(DOWN * 0.3)
        curves = VGroup()
        tags = VGroup()
        for name, vals in d["table"].items():
            pts = [ax.c2p(math.log10(n), math.log10(v)) for n, v in zip(ns, vals)
                   if v > 0 and math.log10(v) <= 30 and math.log10(n) <= 30]
            if len(pts) < 2:
                continue
            c = VMobject(color=FN_COLOR[name], stroke_width=3).set_points_as_corners(pts)
            curves.add(c)
            tags.add(MathTex(FN_TEX[name], font_size=24, color=FN_COLOR[name]).next_to(pts[-1], RIGHT, buff=0.08))
        xl = label(r"$\log_{10} n$", font_size=18, color=GREY_B).next_to(ax, DOWN, buff=0.15)
        yl = label(r"$\log_{10}$ steps", font_size=18, color=GREY_B).next_to(ax, UP, buff=0.1).align_to(ax, LEFT)
        b = d["budget"]
        rows = []
        for name in ("n", "n lg n", "n^2", "n^3", "2^n"):
            rows.append([rf"${FN_TEX[name]}$", _sci(b[name]["second"]), _sci(b[name]["day"]),
                         _sci(b[name]["year"])])
        tab = grid_table([r"steps", r"a second", r"a day", r"a year"], rows, widths=[1.5, 1.6, 1.8, 1.8],
                         row_h=0.5, font_size=19, mono_cols=(),
                         colors=[[FN_COLOR[n], WHITE, WHITE, WHITE] for n in ("n", "n lg n", "n^2", "n^3", "2^n")])
        tl = label(r"the largest $n$ solvable at one step per nanosecond", font_size=19, color=GREY_B)
        right = VGroup(tl, tab).arrange(DOWN, buff=0.2).to_edge(RIGHT, buff=0.4)
        note = label(r"a thousand times faster hardware: \ $n^2$ gains a factor of 32; \ $2^n$ gains 10 more",
                     font_size=21, color=HEAD).to_edge(DOWN, buff=0.35)
        with self.voiceover(
            "On a log–log plot every power of n is a straight line, steeper for higher powers, and the exponential "
            "is a curve that leaves them all behind. <bookmark mark='a'/> Make it concrete with one step per "
            "nanosecond. In a second, an n log n algorithm handles forty million items; a quadratic one, thirty "
            "thousand; a cubic one, a thousand; an exponential one, twenty-nine. <bookmark mark='b'/> In a year, "
            "the exponential algorithm reaches fifty-four. <bookmark mark='c'/> That is the lesson of the ledger "
            "in one table. Hardware a thousand times faster lets a quadratic algorithm handle thirty-two times "
            "more, and an exponential one ten more items. A better algorithm changes the line itself."
        ) as vo:
            self.play(FadeIn(head), Create(ax), FadeIn(xl), FadeIn(yl))
            self.play(LaggedStart(*[Create(c) for c in curves], lag_ratio=0.2), FadeIn(tags), run_time=3)
            vo.wait_until("a")
            self.play(FadeIn(tl), FadeIn(tab.rule), *[FadeIn(c) for c in tab.cells[0]],
                      *[FadeIn(VGroup(r[0], r[1])) for r in tab.cells[1:]])
            vo.wait_until("b")
            self.play(*[FadeIn(VGroup(r[2], r[3])) for r in tab.cells[1:]])
            vo.wait_until("c")
            self.play(FadeIn(note))
        self.wait(0.3)
        self.clear_scene()

    def stirling(self):
        d = load("growth")
        head = label(r"Stirling's formula", font_size=34).to_edge(UP, buff=0.3)
        f = MathTex(r"\ln n! \;=\; n \ln n - n + \tfrac12 \ln(2\pi n) + O(1/n)", font_size=40).next_to(head, DOWN,
                                                                                                    buff=0.5)
        rows = [[str(r["n"]), f"{r['ln_fact']:.4f}", f"{r['stirling']:.4f}", f"{100 * r['rel_err']:.4f}\\%"]
                for r in d["stirling"] if r["n"] >= 2]
        tab = grid_table([r"$n$", r"$\ln n!$", r"Stirling", r"error"], rows, widths=[1.4, 2.6, 2.6, 2.2],
                         row_h=0.44, font_size=19).next_to(f, DOWN, buff=0.4)
        pts = VGroup(
            label(r"so $\log_2 n! = n \log_2 n - n \log_2 e + O(\log n)$: \ we need it in chapter 6", font_size=21,
                  color=YES),
            label(r"Stirling \ (1730) \ and de Moivre; \ the sum $\sum \ln k$ is nearly the integral $\int \ln x\,dx$",
                  font_size=20, color=GREY_B),
        ).arrange(DOWN, buff=0.14).to_edge(DOWN, buff=0.4)
        with self.voiceover(
            "One formula appears again and again when we count arrangements. <bookmark mark='a'/> Stirling's "
            "formula says the logarithm of n factorial is n log n minus n, plus a half log of two pi n, plus a "
            "term that vanishes. <bookmark mark='b'/> It is astonishingly accurate. At n equals ten the error is "
            "about one part in two thousand; at a thousand, about one part in a hundred million. <bookmark mark='c'/> In base two it reads: "
            "log of n factorial is n log n minus about one point four four n. Chapter six turns that into the "
            "limit on every comparison sort."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(Write(f))
            vo.wait_until("b")
            self.play(FadeIn(tab))
            vo.wait_until("c")
            self.play(FadeIn(pts))
        self.wait(0.3)
        self.clear_scene()
