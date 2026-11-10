from __future__ import annotations

import math

import numpy as np

from explainer.cs import *  # noqa: F403
from videos.cs.cs16.common import (CODE, COST, CTRL, DATA, FUNC, HEAD, LAM, NO, PART, YES, grid_table, load, mono)

FN_COLOR = {"lg n": YES, "n": DATA, "n lg n": FUNC, "n^2": CTRL, "n^3": NO, "2^n": COST}
FN_TEX = {"lg n": r"\lg n", "n": r"n", "n lg n": r"n \lg n", "n^2": r"n^2", "n^3": r"n^3", "2^n": r"2^n"}


def _sci(n):
    if n<10**6:return f"{n:,}"
    exponent=len(str(n))-1
    quantum=10**max(0,exponent-2)
    rounded=((n+quantum//2)//quantum)*quantum
    prefix=r"\approx " if rounded!=n else ""
    return rf"${prefix}{rounded/10**exponent:.2f}\times10^{{{exponent}}}$"


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
            label(r"constants and lower-order terms are suppressed for the chosen algorithm and cost model",
                  font_size=21, color=GREY_A),
            label(r"Bachmann \ (1894) \ and Landau; \ Knuth \ (1976) \ fixed $\Omega$ and $\Theta$ as computer "
                  r"scientists use them", font_size=19, color=GREY_B),
        ).arrange(DOWN, buff=0.15).to_edge(DOWN, buff=0.45)
        with self.voiceover(
            (
            "Asymptotic notation compares eventually nonnegative cost functions. <bookmark mark='a'/> Big O means "
            "an eventual constant-factor upper bound, with one fixed constant and one threshold. <bookmark "
            "mark='b'/> Omega gives a lower bound; Theta gives both. Little o says the ratio tends to zero when "
            "the denominator is positive. <bookmark mark='c'/> Thus three n squared plus a hundred n plus seven "
            "is Theta of n squared. This suppresses constants and lower-order terms for the chosen algorithm and "
            "model. Changing the algorithm, representation or model can change the growth itself."
        )
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
        d=load("growth")
        head=label(r"Growth rates, and an explicit step budget",font_size=34).to_edge(UP,buff=0.3)
        ax=Axes(x_range=[0,10,2],y_range=[0,30,10],x_length=5.1,y_length=3.8,
                axis_config={"color":GREY_D,"include_numbers":False}).move_to(LEFT*3.5+UP*0.2)
        xt=VGroup(*[MathTex(rf"10^{{{v}}}",font_size=17,color=GREY_B).next_to(ax.c2p(v,0),DOWN,buff=0.1) for v in (0,3,6,9)])
        yt=VGroup(*[MathTex(rf"10^{{{v}}}",font_size=17,color=GREY_B).next_to(ax.c2p(0,v),LEFT,buff=0.1) for v in (0,10,20,30)])
        xl=label(r"input size $n$ (log scale)",font_size=18,color=GREY_B).next_to(xt,DOWN,buff=0.12)
        yl=label(r"abstract steps (log scale)",font_size=18,color=GREY_B).next_to(ax,UP,buff=0.15).align_to(ax,LEFT)
        functions={"lg n":lambda n:math.log10(math.log2(n)),"n":lambda n:math.log10(n),
                   "n lg n":lambda n:math.log10(n*math.log2(n)),"n^2":lambda n:2*math.log10(n),
                   "n^3":lambda n:3*math.log10(n),"2^n":lambda n:n*math.log10(2)}
        curves=VGroup();tags=VGroup()
        for name,f in functions.items():
            points=[]
            for n in np.geomspace(2,2**30,180):
                x,y=math.log10(n),f(n)
                if y>30:
                    if name=="2^n":points.append(ax.c2p(math.log10(30/math.log10(2)),30))
                    break
                points.append(ax.c2p(x,y))
            curves.add(VMobject(color=FN_COLOR[name],stroke_width=3).set_points_as_corners(points))
            tags.add(MathTex(FN_TEX[name],font_size=24,color=FN_COLOR[name]))
        tags.arrange_in_grid(rows=2,cols=3,buff=(0.55,0.2)).next_to(xl,DOWN,buff=0.25)
        names=("n","n lg n","n^2","n^3","2^n")
        rows=[[rf"${FN_TEX[name]}$",*[_sci(d["budget"][name][unit]) for unit in ("second","day","year")]] for name in names]
        tab=grid_table([r"steps",r"1 second",r"1 day",r"1 year"],rows,widths=[1.3,1.7,1.8,1.8],row_h=0.54,font_size=18,mono_cols=(),colors=[[FN_COLOR[n],WHITE,WHITE,WHITE] for n in names])
        title=label(r"maximum integer $n$, assuming 1 ns per step",font_size=20,color=GREY_A)
        cap=label(r"$\approx$ marks display rounding; no machine overhead modeled",font_size=17,color=GREY_B)
        right=VGroup(title,tab,cap).arrange(DOWN,buff=0.22).to_edge(RIGHT,buff=0.32).shift(UP*0.2)
        note=label(r"$1000\times$ speed: $n^2$ permits about $32\times$ more items; $2^n$ about 10 more",font_size=21,color=HEAD).to_edge(DOWN,buff=0.35)
        with self.voiceover("The axes now show base-ten logarithms of input size and step count. Powers become straight lines; the exponential bends upward. <bookmark mark='a'/> For the table, assume exactly one nanosecond per abstract step, with no extra overhead. Solve each displayed cost function against one second's budget. The entries are integer maxima, except where explicitly rounded for display. <bookmark mark='b'/> Even a year only permits fifty-four items when the cost is two to the n. These are consequences of the assumed functions, not timing predictions for real sorts. <bookmark mark='c'/> A thousandfold speedup expands a quadratic input limit by about thirty-two, and an exponential limit by about ten items. Changing growth can matter much more than changing a constant.") as vo:
            self.play(FadeIn(head),Create(ax),FadeIn(xt),FadeIn(yt),FadeIn(xl),FadeIn(yl))
            self.play(LaggedStart(*[Create(c) for c in curves],lag_ratio=0.08),FadeIn(tags),run_time=1.4)
            vo.wait_until("a")
            self.play(FadeIn(right))
            vo.wait_until("b")
            self.play(Indicate(VGroup(*tab.cells[-1]),color=COST))
            vo.wait_until("c")
            self.play(FadeIn(note))
        self.wait(0.3);self.clear_scene()

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
