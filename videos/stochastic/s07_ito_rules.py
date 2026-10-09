from __future__ import annotations

import numpy as np

from explainer import *  # noqa: F403
from videos.stochastic.common import (boxed, density, hist_shape, label, load, mtex, note, num, path_curve, pdf_curve,
                                      polyline, tw_axes)

N_GRID = 6


def ito_pdf(y):
    """Density of (Z^2 - 1)/2, the exact law of int_0^1 W dW."""
    y = np.asarray(y, float)
    x = 2 * y + 1
    out = np.zeros_like(y)
    ok = x > 1e-9
    out[ok] = 2 * np.exp(-x[ok] / 2) / np.sqrt(2 * np.pi * x[ok])
    return out


class ItoRules(VoiceoverScene):
    def construct(self):
        self.mean_zero()
        self.isometry()
        self.monte_carlo()

    # ------------------------------------------------------------------
    def mean_zero(self):
        f = load("fan")["paths"]
        n = f.shape[1] - 1
        G = np.concatenate([np.zeros((len(f), 1)), np.cumsum(f[:, :-1] * np.diff(f, axis=1), axis=1)], axis=1)
        ax = tw_axes(x_length=6.0, y_range=(-0.8, 4.2, 0.5), y_length=5.4).to_edge(LEFT, buff=0.7).shift(DOWN * 0.3)
        yl = MathTex(r"\int_0^t W\,dW", font_size=30, color=C.GAINS).next_to(ax.y_axis.get_end(), UP, buff=0.1)
        zero = DashedLine(ax.c2p(0, 0), ax.c2p(1, 0), color=GREY_D, stroke_width=1.5)
        paths = VGroup(*[path_curve(ax, g, color=C.GAINS, stroke_width=1.2).set_stroke(opacity=0.3) for g in G])
        mean = polyline(ax, np.linspace(0, 1, n + 1), G.mean(axis=0), color=C.MEAN, stroke_width=4)
        mean_l = label(r"average of 200 paths", font_size=26, color=C.MEAN).next_to(ax.c2p(1, 0), UR, buff=0.1).shift(UP * 0.1)

        eq = VGroup(
            MathTex(r"\mathbb E\big[H_{t_i}\,\Delta W_i\big]", r"=", r"\mathbb E\big[H_{t_i}\big]", r"\cdot",
                    r"\mathbb E\big[\Delta W_i\big]", r"=", r"0", font_size=32),
            MathTex(r"\mathbb E\Big[\int_0^T H\,dW\Big]", r"=", r"0", font_size=40),
        ).arrange(DOWN, buff=0.6).to_edge(RIGHT, buff=0.4).shift(UP * 1.3)
        eq[0][2].set_color(C.STAKE)
        eq[0][4].set_color(C.BROWNIAN)
        eq[1][0].set_color(C.GAINS)
        indep = label(r"the stake is set before the move;\\ the move is fresh, independent, mean zero", font_size=24,
                      color=GREY_B).next_to(eq[0], DOWN, buff=0.2)
        mart = label(r"a \emph{martingale}: \ $\mathbb E[M_t \mid \text{past up to } s] = M_s$", font_size=28,
                     color=C.GAINS).next_to(eq[1], DOWN, buff=0.45)

        with self.voiceover(
            "That fairness is the first of two rules that make the Itô integral work. <bookmark mark='a'/> On each step, "
            "the stake is fixed before the move, and the move is a fresh, independent coin flip with mean zero. "
            "<bookmark mark='b'/> So the expected gain on every step factors into the expected stake times zero. "
            "<bookmark mark='c'/> Add them up: every Itô integral has expected value zero."
        ) as vo:
            vo.wait_until("a")
            self.play(Write(eq[0][:2]), FadeIn(indep))
            vo.wait_until("b")
            self.play(Write(eq[0][2:]))
            vo.wait_until("c")
            self.play(Write(eq[1]))
        with self.voiceover(
            "Here are our winnings from the double-down strategy, on two hundred different Brownian paths. "
            "<bookmark mark='m'/> They spread out, and some win big, but their average stays pinned at zero, all the way "
            "along. <bookmark mark='t'/> A process like this, whose best forecast of the future is its present value, is "
            "called a martingale. Itô integrals of adapted strategies are martingales: no strategy beats a fair game."
        ) as vo:
            self.play(Create(ax), FadeIn(yl), Create(zero), FadeIn(ax.x_labels))
            self.play(LaggedStart(*[Create(p) for p in paths], lag_ratio=0.01), run_time=2.5)
            vo.wait_until("m")
            self.play(Create(mean), FadeIn(mean_l))
            vo.wait_until("t")
            self.play(FadeIn(mart))
        self.wait(0.4)
        self.clear_scene()

    # ------------------------------------------------------------------
    def isometry(self):
        n = N_GRID
        top = MathTex(r"\mathbb E\Big[\Big(\sum_i H_{t_i}\,\Delta W_i\Big)^2\Big]", r"=",
                      r"\sum_i \sum_j \mathbb E\big[H_{t_i}\Delta W_i \; H_{t_j}\Delta W_j\big]", font_size=38)
        top.to_edge(UP, buff=0.35)
        cell = 0.85
        grid = VGroup()
        for i in range(n):
            for j in range(n):
                sq = Square(side_length=cell, stroke_color=GREY_C, stroke_width=1.5, fill_color="#1C2430", fill_opacity=1)
                sq.move_to([j * cell, -i * cell, 0])
                grid.add(sq)
        grid.move_to(LEFT * 3.4 + DOWN * 1.0)
        rows = VGroup(*[MathTex(f"{i + 1}", font_size=26, color=GREY_A).next_to(grid[i * n], LEFT, buff=0.15)
                        for i in range(n)])
        cols = VGroup(*[MathTex(f"{j + 1}", font_size=26, color=GREY_A).next_to(grid[j], UP, buff=0.15)
                        for j in range(n)])
        rows.add(MathTex("i", font_size=32, color=GREY_A).next_to(rows, LEFT, buff=0.25))
        cols.add(MathTex("j", font_size=32, color=GREY_A).next_to(cols, RIGHT, buff=0.25))
        zeros = VGroup()
        diags = VGroup()
        for i in range(n):
            for j in range(n):
                c = grid[i * n + j]
                if i == j:
                    diags.add(MathTex(r"\mathbb E[H_{%d}^2]" % (i + 1), r"\Delta t", font_size=20, color=C.QV)
                              .arrange(DOWN, buff=0.04).move_to(c))
                else:
                    zeros.add(MathTex("0", font_size=26, color=GREY_C).move_to(c))
        ex = (1, 4)
        ex_cell = grid[ex[0] * n + ex[1]]
        ex_box = SurroundingRectangle(ex_cell, color=C.BROWNIAN, buff=0.0, stroke_width=4)

        off = VGroup(
            MathTex(r"i < j:", font_size=32),
            MathTex(r"\mathbb E\big[\,\underbrace{H_{t_i}\Delta W_i\,H_{t_j}}_{\text{known by } t_j}\;"
                    r"\underbrace{\Delta W_j}_{\text{fresh}}\big]", font_size=32),
            MathTex(r"= \mathbb E\big[H_{t_i}\Delta W_i\,H_{t_j}\big]\cdot 0 = 0", font_size=32),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.18).to_edge(RIGHT, buff=0.4).shift(UP * 0.8)
        dg = VGroup(
            MathTex(r"i = j:", font_size=32),
            MathTex(r"\mathbb E\big[H_{t_i}^2\,(\Delta W_i)^2\big]", r"=", r"\mathbb E\big[H_{t_i}^2\big]\,", r"\Delta t",
                    font_size=32),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.18).next_to(off, DOWN, buff=0.45).align_to(off, LEFT)
        dg[1][3].set_color(C.CLOCK)
        side = VGroup(off, dg)
        side.shift(LEFT * max(0, side.get_right()[0] - 6.8))
        iso = MathTex(r"\mathbb E\Big[\Big(\int_0^T H\,dW\Big)^2\Big]", r"=", r"\mathbb E\Big[\int_0^T H^2\,dt\Big]",
                      font_size=42)
        iso[0].set_color(C.GAINS)
        iso[2].set_color(C.STAKE)
        isob = boxed(iso, color=C.GAINS, buff=0.2).to_corner(DR, buff=0.35)
        iso_l = label(r"the It\^o isometry", font_size=28, color=C.GAINS).next_to(isob, UP, buff=0.12)

        with self.voiceover(
            "The second rule tells us how big an Itô integral is. <bookmark mark='a'/> Square the sum, and take the "
            "average. Squaring a sum of n terms gives n squared cross terms, one for every pair of steps. "
            "<bookmark mark='g'/> Here they are as a grid."
        ) as vo:
            vo.wait_until("a")
            self.play(Write(top))
            vo.wait_until("g")
            self.play(FadeIn(grid, lag_ratio=0.01), FadeIn(rows), FadeIn(cols), run_time=1.5)
        with self.voiceover(
            "Take any cell off the diagonal, <bookmark mark='x'/> say steps two and five. Step five's move comes last. "
            "Everything else in the product is known by the start of step five, and step five's move is fresh, with mean "
            "zero. <bookmark mark='z'/> So the whole term averages to zero. <bookmark mark='o'/> The same goes for every "
            "off-diagonal cell. The fairness of each step wipes out all the cross terms."
        ) as vo:
            vo.wait_until("x")
            self.play(Create(ex_box), FadeIn(off[:2]))
            vo.wait_until("z")
            self.play(FadeIn(off[2]))
            vo.wait_until("o")
            self.play(LaggedStart(*[FadeIn(z) for z in zeros], lag_ratio=0.02),
                      *[grid[i * n + j].animate.set_fill(opacity=0.25) for i in range(n) for j in range(n) if i != j],
                      FadeOut(ex_box), run_time=1.6)
        with self.voiceover(
            "Only the diagonal survives: <bookmark mark='d'/> the stake squared times the move squared, which averages to "
            "the stake squared times delta t. <bookmark mark='s'/> Add up the diagonal, and you get an ordinary integral. "
            "This is the Itô isometry: the average square of the integral equals the average of the integral of H "
            "squared d t."
        ) as vo:
            vo.wait_until("d")
            self.play(FadeIn(dg), LaggedStart(*[FadeIn(d) for d in diags], lag_ratio=0.15),
                      *[grid[i * n + i].animate.set_fill(C.QV, opacity=0.15) for i in range(n)], run_time=1.5)
            vo.wait_until("s")
            self.play(Write(iso), Create(isob[0]), FadeIn(iso_l))
        with self.voiceover(
            "Notice the d W squared equals d t rule hiding inside it, on the diagonal. And this identity is also what "
            "guarantees that the Riemann sums converge in the first place: it turns questions about random sums into "
            "questions about ordinary integrals."
        ):
            self.play(Indicate(VGroup(*diags), color=C.QV))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def monte_carlo(self):
        d = load("ito_mc")
        ints = d["ints"]
        mean, var, naive_mean, _ = (float(x) for x in d["stats"])
        ax = Axes(x_range=[-0.8, 3.0, 0.5], y_range=[0, 1.6, 0.5], x_length=9.0, y_length=4.6, tips=False,
                  axis_config={"stroke_color": GREY_B, "include_ticks": False}).move_to(DOWN * 0.9 + LEFT * 1.6)
        ticks = VGroup(*[MathTex(f"{v:g}", font_size=24).next_to(ax.c2p(v, 0), DOWN, buff=0.1) for v in (-0.5, 0, 1, 2, 3)])
        edges = np.linspace(-0.8, 3.0, 153)
        hist = hist_shape(ax, edges, np.minimum(density(ints, edges), 1.6), color=C.GAINS, fill_opacity=0.4)
        ys = np.linspace(-0.4995, 3.0, 600)
        exact = pdf_curve(ax, ys, np.minimum(ito_pdf(ys), 1.6), color=WHITE, stroke_width=2.5)
        zero = DashedLine(ax.c2p(0, 0), ax.c2p(0, 1.6), color=C.MEAN, stroke_width=3)
        zl = label(r"mean", font_size=26, color=C.MEAN).next_to(ax.c2p(0, 1.6), UP, buff=0.08)
        edge = DashedLine(ax.c2p(-0.5, 0), ax.c2p(-0.5, 1.6), color=C.QV, stroke_width=2.5)
        el = MathTex(r"-\tfrac12", font_size=30, color=C.QV).next_to(ax.c2p(-0.5, 1.6), UP, buff=0.08)

        pred = VGroup(
            MathTex(r"H = W:", font_size=34),
            MathTex(r"\mathbb E\Big[\Big(\int_0^1 W\,dW\Big)^2\Big]", r"=", r"\int_0^1 \mathbb E[W_t^2]\,dt", r"=",
                    r"\int_0^1 t\,dt", r"=", r"\tfrac12", font_size=34),
        ).arrange(RIGHT, buff=0.3).to_edge(UP, buff=0.35)
        res = VGroup(
            MathTex(r"\text{mean}", r"=", num(mean, 4, sign=True), font_size=34),
            MathTex(r"\text{variance}", r"=", num(var, 3), font_size=34),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.25).to_edge(RIGHT, buff=0.6).shift(UP * 1.2)
        res[0][2].set_color(C.MEAN)
        res[1][2].set_color(C.GAINS)
        sim = note(r"40{,}000 simulated paths,\\1{,}000 steps each;\\white: the exact density", font_size=22)
        sim.next_to(res, DOWN, buff=0.3).align_to(res, LEFT)
        naive = label(rf"the naive $\tfrac12 W_1^2$\\would average {naive_mean:.3f}:\\not fair", font_size=26,
                      color=GREY_A).next_to(sim, DOWN, buff=0.35).align_to(res, LEFT)
        assert round(mean, 4) == -0.0007 and round(var, 3) == 0.505  # quoted in the narration

        with self.voiceover(
            "Let's test both rules on our double-down strategy, H equals W. <bookmark mark='p'/> The isometry predicts "
            "that the average square of the winnings is the integral of t d t from zero to one: one half."
        ) as vo:
            vo.wait_until("p")
            self.play(Write(pred), run_time=2.5)
        with self.voiceover(
            "Now simulate forty thousand paths. <bookmark mark='m'/> The average of the winnings: minus 0.0007, zero up "
            "to sampling noise. <bookmark mark='v'/> The variance: 0.505. Both rules check out. <bookmark mark='s'/> And "
            "look at the shape: you can never lose more than about one half, but you can win big. Lopsided, but fair. "
            "<bookmark mark='n'/> The ordinary-calculus answer, one half W squared, would average one half: it would win "
            "money in a fair game, which is exactly why it can't be right."
        ) as vo:
            self.play(Create(ax), FadeIn(ticks), FadeIn(hist, shift=UP * 0.2), FadeIn(sim))
            vo.wait_until("m")
            self.play(Create(zero), FadeIn(zl), FadeIn(res[0]))
            vo.wait_until("v")
            self.play(FadeIn(res[1]))
            vo.wait_until("s")
            self.play(Create(exact), Create(edge), FadeIn(el))
            vo.wait_until("n")
            self.play(FadeIn(naive))
        self.wait(0.5)
        self.clear_scene()
