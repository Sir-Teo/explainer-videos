from __future__ import annotations

import math

import numpy as np

from explainer.analysis import *  # noqa: F403
from videos.analysis8.common import p_ball, pnorm, square_axes


class Dual(VoiceoverScene):
    def construct(self):
        self.card()
        self.polars()
        self.table()

    # ------------------------------------------------------------------
    def card(self):
        card = chapter_card(7, r"Dual spaces", r"What does a functional on $\ell^p$ look like?", lit=(), part=8)
        with self.voiceover("Chapter seven: dual spaces, the spaces of functionals."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))

    # ------------------------------------------------------------------
    def polars(self):
        pairs = [(1.0, np.inf, r"\ell^1", r"\ell^\infty"), (2.0, 2.0, r"\ell^2", r"\ell^2"), (3.0, 1.5, r"\ell^3", r"\ell^{3/2}")]
        groups = VGroup()
        for k, (p, q, n1, n2) in enumerate(pairs):
            ax = square_axes([-1.3, 1.3, 1], [-1.3, 1.3, 1], 0.85).move_to([-4.6 + 4.6 * k, 1.05, 0])
            bx = square_axes([-1.3, 1.3, 1], [-1.3, 1.3, 1], 0.85).move_to([-4.6 + 4.6 * k, -1.6, 0])
            for a in (ax, bx):
                a.set_opacity(0.3)
            b1 = p_ball(ax, p, C.DIST)
            b2 = p_ball(bx, q, C.FUNCTIONAL)
            t1 = MathTex(rf"\text{{ball of }} {n1}", font_size=24, color=C.DIST).next_to(ax, UP, buff=0.05)
            t2 = MathTex(rf"\text{{dual ball: }} {n2}", font_size=24, color=C.FUNCTIONAL).next_to(bx, UP, buff=0.05)
            groups.add(VGroup(ax, b1, t1, bx, b2, t2))
        # the polar of the p-ball is the q-ball: sup over the p-sphere of g . x equals the q-norm of g
        rng = np.random.default_rng(3)
        th = np.linspace(0, 2 * np.pi, 20001)
        circ = np.stack([np.cos(th), np.sin(th)], 1)
        worst = 0.0
        for p, q, _, _ in pairs:
            sphere = circ / np.array([pnorm(v, p) for v in circ])[:, None]
            for _ in range(20):
                g = rng.normal(size=2)
                worst = max(worst, abs((sphere @ g).max() - pnorm(g, q)) / pnorm(g, q))
        assert worst < 1e-6
        # in R^8: p = 1 and p = infinity exactly
        g8 = rng.normal(size=8)
        verts = np.vstack([np.eye(8), -np.eye(8)])
        assert abs((verts @ g8).max() - np.abs(g8).max()) < 1e-12  # sup over the l^1 ball: at a vertex
        assert abs(g8 @ np.sign(g8) - np.abs(g8).sum()) < 1e-12  # sup over the cube: at sign(g)
        note_ = VGroup(
            MathTex(r"\|g\|_{X^*} = \sup_{\|x\|_p \le 1} g \cdot x = \|g\|_q, \quad \tfrac1p + \tfrac1q = 1", font_size=28,
                    color=C.EPS),
            MathTex(r"\text{checked: 60 random } g \text{ in } \R^2: \ \text{rel. error} < 10^{-6}", font_size=22,
                    color=GREY_A),
        ).arrange(DOWN, buff=0.08).to_edge(DOWN, buff=0.12)
        head = label(r"Each unit ball has a dual ball: \ the functionals of norm at most $1$", font_size=32).to_edge(UP,
                                                                                                          buff=0.25)
        with self.voiceover(
            "<bookmark mark='a'/> A functional on a normed space has its own norm: its largest value on the unit "
            "ball. So the functionals form a normed space too, the dual, with a unit ball of its own. "
            "<bookmark mark='b'/> For the one-norm, whose ball is the diamond, the dual ball is the square: the "
            "largest value of g dot x on the diamond is the largest coordinate of g. <bookmark mark='c'/> The circle "
            "is its own dual. And in general the dual of the p-norm is the q-norm, with conjugate exponents, checked "
            "here for sixty random functionals."
        ) as vo:
            vo.wait_until("a")
            self.play(FadeIn(head))
            vo.wait_until("b")
            self.play(FadeIn(groups[0]))
            vo.wait_until("c")
            self.play(FadeIn(groups[1]))
            self.play(FadeIn(groups[2]), FadeIn(note_))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def table(self):
        card = dictionary_card(r"the space $X$", r"its dual $X^*$", [
            (r"$\ell^p$, \ $1 < p < \infty$", r"$\ell^q$, \ $\frac1p + \frac1q = 1$ \ \ (reflexive: $X^{**} = X$)"),
            (r"$c_0$ \ (sequences $\to 0$)", r"$\ell^1$"),
            (r"$\ell^1$", r"$\ell^\infty$ \ \ (so $\ell^1$ is not reflexive)"),
            (r"$C(K)$", r"$M(K)$, \ the measures \ (Riesz, Part 6)"),
            (r"$\ell^\infty$", r"much more than $\ell^1$: \ Banach limits"),
            (r"a row vector", r"a functional \ (the dictionary)"),
        ], font_size=24)
        card.scale(0.8)
        card.move_to([-6.85 + card.width / 2, -0.35, 0])
        head = label(r"\textbf{FA 4.1--4.7, RCA 6.16, 6.19} \ the duals, computed", font_size=32).to_edge(UP, buff=0.3)
        # why c_0* = l^1: against y in l^1, the best x in the unit ball of c_0 is sign(y) cut off at N, and the
        # pairing climbs to sum |y_n| = ||y||_1 (here y_n = (-0.75)^n, ||y||_1 = 4, partial sums 4(1 - 0.75^N))
        nn = np.arange(20)
        yv = (-0.75) ** nn
        cxp, W_, H_ = 4.0, 5.4, 1.6
        x0p = cxp - W_ / 2

        def bars(vals, yc, color, scale):
            g = VGroup(Line([x0p, yc, 0], [x0p + W_, yc, 0], color=GREY_D, stroke_width=1.5))
            for i, v in enumerate(vals):
                if abs(v) > 1e-12:
                    g.add(Rectangle(width=0.18, height=abs(v) * scale, stroke_width=0, fill_color=color,
                                    fill_opacity=0.85).move_to([x0p + (i + 0.5) * W_ / len(vals), yc + v * scale / 2, 0]))
            return g

        yb = bars(yv, 1.35, C.FUNCTIONAL, H_ / 2)
        yl = MathTex(r"y = \big((-0.75)^n\big) \in \ell^1, \ \ \|y\|_1 = 4", font_size=26, color=C.FUNCTIONAL
                     ).next_to([cxp, 1.35 + H_ / 2, 0], UP, buff=0.15)
        Ns = [1, 2, 3, 4, 6, 8, 11, 14]
        xbs = [bars(np.where(nn < N, np.sign(yv), 0.0), -1.0, C.SEQ, 0.55) for N in Ns]
        xl = MathTex(r"x^{(N)} = \operatorname{sign}(y_n) \text{ for } n < N: \ \ \|x^{(N)}\|_\infty = 1", font_size=24,
                     color=C.SEQ).next_to([cxp, -1.0 + 0.55, 0], UP, buff=0.15)
        pair = [float(np.sum(np.where(nn < N, np.sign(yv), 0.0) * yv)) for N in Ns]
        assert all(abs(v - 4 * (1 - 0.75**N)) < 1e-12 for v, N in zip(pair, Ns))
        prd = [MathTex(rf"N = {N}: \ \langle x^{{(N)}}, y\rangle = \sum_{{n < N}} |y_n| = {v:.4f}", font_size=26,
                       color=C.EPS).move_to([cxp, -2.35, 0]) for N, v in zip(Ns, pair)]
        pnote = label(r"$\to \|y\|_1$: \ the norm of $y$ as a functional on $c_0$", font_size=22, color=GREY_A
                      ).move_to([cxp, -2.95, 0])
        assert card.get_right()[0] < x0p - 0.2 and x0p + W_ < 6.95 and max(m.width for m in prd) < 6.0
        with self.voiceover(
            "<bookmark mark='a'/> The duals we know. For p between one and infinity, the dual of l p is l q, and the "
            "dual of that is l p again: these spaces are reflexive. <bookmark mark='b'/> The sequences tending to "
            "zero have dual l one, and l one has dual l infinity, which is strictly bigger, so l one isn't reflexive. "
            "The continuous functions have the measures as their dual, as Part 6 proved. <bookmark mark='c'/> And "
            "l infinity has functionals that no sequence describes, like a limit for every bounded sequence, which "
            "only Hahn-Banach can produce. That's the promise from Part 6 kept."
        ) as vo:
            vo.wait_until("a")
            self.play(FadeIn(head), FadeIn(card.titles), FadeIn(card.rows[0]), FadeIn(card.arrows[0]))
            vo.wait_until("b")
            self.play(FadeIn(card.rows[1]), FadeIn(card.arrows[1]), FadeIn(yb), FadeIn(yl))
            self.play(FadeIn(xbs[0]), FadeIn(xl), FadeIn(prd[0]))
            for k in range(1, len(Ns)):
                self.play(ReplacementTransform(xbs[k - 1], xbs[k]), FadeTransform(prd[k - 1], prd[k]), run_time=0.55)
            self.play(FadeIn(pnote))
            for i in (2, 3):
                self.play(FadeIn(card.rows[i]), FadeIn(card.arrows[i]), run_time=0.7)
            vo.wait_until("c")
            for i in (4, 5):
                self.play(FadeIn(card.rows[i]), FadeIn(card.arrows[i]), run_time=0.7)
        self.wait(0.4)
        self.clear_scene()
