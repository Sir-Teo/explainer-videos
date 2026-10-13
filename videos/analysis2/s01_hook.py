from __future__ import annotations

import math

import numpy as np

from explainer.analysis import *  # noqa: F403
from videos.analysis2.common import hop, load, plain_axes, polyline


class Hook(VoiceoverScene):
    def construct(self):
        self.recap()
        self.natural()
        self.to_pi()
        self.anything()
        self.plan()

    # ------------------------------------------------------------------
    def recap(self):
        led = ledger(filled=1, highlight=1).scale(0.9)
        with self.voiceover(
            "In Part 1 we built the real numbers: a line with no holes, where every bounded set has a least upper bound. "
            "<bookmark mark='l'/> That's the first row of our ledger. Now we put it to work on limits: sequences, "
            "infinite sums, continuity and derivatives. And we start with a warning about infinite sums."
        ) as vo:
            self.play(FadeIn(led))
            vo.wait_until("l")
            self.play(Indicate(led.rows[0], color=C.EPS, scale_factor=1.04))
        self.play(FadeOut(led))

    # ------------------------------------------------------------------
    def natural(self):
        d = load("rearrange")
        s_nat = d["s_nat"]
        X = lambda v: -5.5 + (v - 0.0) * 9.0  # noqa: E731  screen x of the value v (0 .. 1.2)
        y0 = -0.6
        line = Line([X(-0.05), y0, 0], [X(1.25), y0, 0], color=GREY_C, stroke_width=2)
        ticks = VGroup(*[VGroup(Line([X(v), y0 - 0.07, 0], [X(v), y0 + 0.07, 0], color=GREY_C),
                                Text(f"{v:g}", font_size=22, color=GREY_B).move_to([X(v), y0 - 0.35, 0]))
                         for v in (0, 0.5, 1.0)])
        ln2 = VGroup(DashedLine([X(math.log(2)), y0 - 0.5, 0], [X(math.log(2)), y0 + 1.9, 0], color=WHITE, stroke_width=2),
                     MathTex(r"\ln 2", font_size=32).move_to([X(math.log(2)), y0 + 2.15, 0]))
        series = MathTex(r"1", r"-\tfrac12", r"+\tfrac13", r"-\tfrac14", r"+\tfrac15", r"-\tfrac16", r"+\cdots",
                         r"= \ln 2 = 0.6931\ldots", font_size=44).to_edge(UP, buff=0.6)
        for i in (0, 2, 4):
            series[i].set_color(C.SEQ)
        for i in (1, 3, 5):
            series[i].set_color(C.CUT_HIGH)
        dot = Dot([X(0), y0, 0], radius=0.09, color=WHITE)
        arrows = VGroup()
        with self.voiceover(
            "Here's the alternating harmonic series: one, minus a half, plus a third, minus a quarter, and so on. "
            "<bookmark mark='a'/> Add it up one term at a time and the running total swings back and forth, each swing "
            "smaller than the last, <bookmark mark='l'/> closing in on the natural log of two, about 0.693."
        ) as vo:
            self.play(Write(series[:-1]), Create(line), FadeIn(ticks))
            vo.wait_until("a")
            self.play(FadeIn(dot))
            prev = 0.0
            for k in range(10):
                v = float(s_nat[k])
                col = C.SEQ if k % 2 == 0 else C.CUT_HIGH
                ar = hop([X(prev), y0, 0], [X(v), y0, 0], col, up=(k % 2 == 0))
                arrows.add(ar)
                self.play(Create(ar), dot.animate.move_to([X(v), y0, 0]), run_time=0.45 if k > 2 else 0.7)
                prev = v
            vo.wait_until("l")
            self.play(FadeIn(ln2), Write(series[-1]), dot.animate.move_to([X(float(s_nat[-1])), y0, 0]))
        assert abs(s_nat[-1] - math.log(2)) < 2e-4
        self.wait(0.3)
        self.play(FadeOut(VGroup(arrows, dot, ln2, line, ticks)), series.animate.scale(0.75).to_edge(UP, buff=0.3))
        self.series = series

    # ------------------------------------------------------------------
    def to_pi(self):
        d = load("rearrange")
        t, s = d["t_pi"], d["s_pi"]
        ratio = float(d["ratio_pi"])
        X = lambda v: -6.0 + (v + 0.2) * 3.0  # noqa: E731  values -0.2 .. 3.8
        y0 = 1.0
        line = Line([X(-0.2), y0, 0], [X(3.85), y0, 0], color=GREY_C, stroke_width=2)
        ticks = VGroup(*[VGroup(Line([X(v), y0 - 0.07, 0], [X(v), y0 + 0.07, 0], color=GREY_C),
                                Text(f"{v:g}", font_size=22, color=GREY_B).move_to([X(v), y0 - 0.35, 0]))
                         for v in (0, 1, 2, 3)])
        pi_l = VGroup(DashedLine([X(math.pi), y0 - 0.45, 0], [X(math.pi), y0 + 0.9, 0], color=C.EPS, stroke_width=2.5),
                      MathTex(r"\pi", font_size=36, color=C.EPS).move_to([X(math.pi), y0 + 1.15, 0]))
        rule = VGroup(label(r"Same terms, new order:", font_size=28, color=GREY_A),
                      label(r"take positive terms ($1, \tfrac13, \tfrac15, \ldots$) until the total passes $\pi$,", font_size=26),
                      label(r"then negative ones ($-\tfrac12, -\tfrac14, \ldots$) until it drops below; repeat.", font_size=26)
                      ).arrange(DOWN, aligned_edge=LEFT, buff=0.12).to_edge(DOWN, buff=0.35)
        dot = Dot([X(0), y0, 0], radius=0.08, color=WHITE)
        with self.voiceover(
            "Now take exactly the same terms, and add them in a different order. <bookmark mark='r'/> Use positive terms, "
            "one, a third, a fifth, and so on, until the total passes pi. Then use negative terms until it drops back "
            "below pi. Then positive terms again. <bookmark mark='g'/> Watch where the total goes."
        ) as vo:
            self.play(Create(line), FadeIn(ticks), FadeIn(pi_l))
            vo.wait_until("r")
            self.play(FadeIn(rule))
            vo.wait_until("g")
            self.play(FadeIn(dot))
            for k in range(0, 60):
                self.play(dot.animate.move_to([X(float(s[k])), y0, 0]), run_time=0.07 if k > 8 else 0.25,
                          rate_func=linear)
        # the long run, as a graph of the partial sums against the number of terms used
        K = len(s)
        ax = plain_axes([0, K, 1000], [2.6, 3.7, 0.5], 9.8, 2.8, numbers=False).move_to(DOWN * 1.35 + LEFT * 0.6)
        tgt = DashedLine(ax.c2p(0, math.pi), ax.c2p(K, math.pi), color=C.EPS, stroke_width=2)
        curve = polyline(ax, np.arange(1, K + 1), np.clip(s, 2.6, 3.7), color=C.SEQ, stroke_width=2)
        kl = label(r"terms used $\to$", font_size=22, color=GREY_B).next_to(ax.x_axis.get_end(), DOWN, buff=0.15).shift(LEFT * 0.7)
        pl = MathTex(r"\pi", font_size=30, color=C.EPS).next_to(ax.c2p(K, math.pi), RIGHT, buff=0.1)
        fin = VGroup(MathTex(rf"\text{{after }} 10^6 \text{{ terms: }} {float(d['final_pi']):.6f}", font_size=34),
                     MathTex(rf"\pi = {math.pi:.6f}", font_size=34, color=C.EPS)).arrange(DOWN, buff=0.15)
        fin.move_to([-2.6, 2.25, 0])
        assert abs(float(d["final_pi"]) - math.pi) < 1e-5 and abs(ratio - 134) < 1.5
        with self.voiceover(
            "<bookmark mark='p'/> Plot the running total against the number of terms used. It overshoots pi, falls back, "
            "overshoots again, and the swings shrink, because each swing is at most the size of the last term used. "
            "<bookmark mark='m'/> After a million terms, the total is within a hundred-thousandth of pi. Reaching pi "
            "takes about a hundred and thirty-four positive terms for every negative one, but every term of the original "
            "series gets used, exactly once."
        ) as vo:
            self.play(FadeOut(rule), FadeOut(dot))
            vo.wait_until("p")
            self.play(Create(ax), Create(tgt), FadeIn(pl), FadeIn(kl))
            self.play(Create(curve), run_time=3, rate_func=linear)
            vo.wait_until("m")
            self.play(FadeIn(fin))
        self.wait(0.3)
        self.play(FadeOut(VGroup(ax, tgt, curve, pl, kl, fin, line, ticks, pi_l)))

    # ------------------------------------------------------------------
    def anything(self):
        d = load("rearrange")
        K = 4000
        ax = plain_axes([0, K, 1000], [-1.6, 3.8, 1], 10.5, 4.6, numbers=True, font_size=20,
                        axis_config={"decimal_number_config": {"num_decimal_places": 0}}).move_to(DOWN * 0.7)
        c_pi = polyline(ax, np.arange(1, K + 1), d["s_pi"][:K], color=C.SEQ, stroke_width=2)
        c_m1 = polyline(ax, np.arange(1, K + 1), d["s_m1"][:K], color=C.CUT_HIGH, stroke_width=2)
        c_inf = polyline(ax, np.arange(1, K + 1), np.clip(d["s_inf"][:K], -1.6, 3.8), color=C.APPROX, stroke_width=2)
        c_nat = polyline(ax, np.arange(1, K + 1), d["s_nat"][:K], color=WHITE, stroke_width=2)
        labs = VGroup(MathTex(r"\to \pi", font_size=30, color=C.SEQ).next_to(ax.c2p(K, math.pi), RIGHT, buff=0.1),
                      MathTex(r"\to -1", font_size=30, color=C.CUT_HIGH).next_to(ax.c2p(K, -1), RIGHT, buff=0.1),
                      MathTex(r"\to \infty", font_size=30, color=C.APPROX).next_to(ax.c2p(K, float(np.clip(d["s_inf"][K - 1], -1.6, 3.8))), RIGHT, buff=0.1),
                      MathTex(r"\ln 2", font_size=30).next_to(ax.c2p(K, math.log(2)), RIGHT, buff=0.1))
        assert abs(float(d["final_m1"]) + 1) < 1e-5 and float(d["s_inf"][K - 1]) > 3.5
        head = label(r"Four orders of the same terms", font_size=36).to_edge(UP, buff=0.45)
        with self.voiceover(
            "And pi isn't special. <bookmark mark='a'/> Aim at minus one instead, and the same recipe lands on minus one. "
            "<bookmark mark='b'/> Keep raising the target and the total runs off to infinity. Same terms, every time; "
            "only the order changes, <bookmark mark='c'/> and in the natural order they add up to log two."
        ) as vo:
            self.play(FadeOut(self.series), FadeIn(head), Create(ax))
            self.play(Create(c_pi), FadeIn(labs[0]), run_time=1.2)
            vo.wait_until("a")
            self.play(Create(c_m1), FadeIn(labs[1]), run_time=1.5)
            vo.wait_until("b")
            self.play(Create(c_inf), FadeIn(labs[2]), run_time=1.5)
            vo.wait_until("c")
            self.play(Create(c_nat), FadeIn(labs[3]), run_time=1.2)
        moral = VGroup(label(r"An infinite sum is not a sum. It is a limit,", font_size=34, color=C.EPS),
                       label(r"and limits can depend on the order in which you take them.", font_size=34, color=C.EPS))
        moral.arrange(DOWN, buff=0.15)
        box = BackgroundRectangle(moral, color=BACKGROUND, fill_opacity=0.9, buff=0.25)
        with self.voiceover(
            "This is Riemann's rearrangement theorem, which we'll prove in chapter eight. The lesson: <bookmark mark='m'/> "
            "an infinite sum is not a sum. It's a limit, and limits can depend on the order in which you take them, "
            "which is exactly the thesis of this series. So before we can trust any manipulation with infinitely many "
            "terms, we need to say precisely what convergence means."
        ) as vo:
            vo.wait_until("m")
            self.play(FadeIn(box), FadeIn(moral))
        self.wait(0.4)
        self.clear_scene()

    # ------------------------------------------------------------------
    def plan(self):
        chapters = [
            r"Sequences and their limits", r"Cauchy sequences and completeness", r"Upper and lower limits",
            r"Series, and the comparison tests", r"The number $e$", r"Root, ratio and power series",
            r"Summation by parts, and multiplying series", r"Rearrangements", r"Continuity",
            r"Continuity and compactness", r"Continuity and connectedness", r"The derivative",
            r"Mean value theorems", r"Taylor's theorem",
        ]
        items = VGroup(*[label(rf"{i + 1}.\; {t}", font_size=27) for i, t in enumerate(chapters)])
        col1 = VGroup(*items[:7]).arrange(DOWN, aligned_edge=LEFT, buff=0.28)
        col2 = VGroup(*items[7:]).arrange(DOWN, aligned_edge=LEFT, buff=0.28)
        cols = VGroup(col1, col2).arrange(RIGHT, buff=0.9, aligned_edge=UP).shift(DOWN * 0.3)
        head = label(r"Part 2: Limits", font_size=46).to_edge(UP, buff=0.5)
        sub = label(r"Rudin, \textit{Principles}, chapters 3--5", font_size=26, color=GREY_B).next_to(head, DOWN, buff=0.15)
        with self.voiceover(
            "Here's the plan, following chapters three to five of Rudin's Principles. <bookmark mark='a'/> First, "
            "sequences and series: convergence, Cauchy sequences, upper and lower limits, the convergence tests, the "
            "number e, and what you may and may not do with an infinite sum. <bookmark mark='b'/> Then continuity, "
            "and what it gains from compactness and connectedness. <bookmark mark='c'/> And then the derivative: the "
            "mean value theorem, and Taylor's theorem."
        ) as vo:
            self.play(FadeIn(head), FadeIn(sub))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(items[i], shift=RIGHT * 0.2) for i in range(8)], lag_ratio=0.2))
            vo.wait_until("b")
            self.play(LaggedStart(*[FadeIn(items[i], shift=RIGHT * 0.2) for i in range(8, 11)], lag_ratio=0.25))
            vo.wait_until("c")
            self.play(LaggedStart(*[FadeIn(items[i], shift=RIGHT * 0.2) for i in range(11, 14)], lag_ratio=0.25))
        self.wait(0.6)
        self.clear_scene()
