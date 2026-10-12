from __future__ import annotations

import math

import numpy as np

from explainer.analysis import *  # noqa: F403
from videos.analysis1.common import (SQRT2, Window, load, partial_curve, polyline, saw_axes, saw_graph,
                                     saw_partial)


class Hook(VoiceoverScene):
    def construct(self):
        self.fourier()
        self.questions()
        self.history()
        self.holes()
        self.series()
        self.thesis()
        self.plan()

    # ------------------------------------------------------------------
    def fourier(self):
        d = load("sawtooth")
        ax = saw_axes().shift(DOWN * 0.7)
        xl = VGroup(*[MathTex(t, font_size=28, color=GREY_B).next_to(ax.c2p(v, 0), DOWN, buff=0.18)
                      for t, v in ((r"0", 0), (r"\pi", np.pi), (r"2\pi", 2 * np.pi))])
        saw_g = saw_graph(ax)
        who = label(r"Joseph Fourier, 1807", font_size=30, color=GREY_A).to_corner(UL, buff=0.45)
        self.ax = ax

        with self.voiceover(
            "In 1807, Joseph Fourier submitted a memoir on how heat flows through a solid body. Buried in it was a "
            "claim that took mathematics a century to digest. <bookmark mark='s'/> Take a function with a corner, or "
            "even a jump, like this sawtooth. <bookmark mark='w'/> Fourier said that it can be written as a sum of "
            "sine waves."
        ) as vo:
            self.play(FadeIn(who), Create(ax), FadeIn(xl))
            vo.wait_until("s")
            self.play(Create(saw_g[:-1]), run_time=1.6)
            self.play(FadeIn(saw_g.ends))

        # The recipe, one wave at a time
        terms = [r"\sin x", r"\frac{\sin 2x}{2}", r"\frac{\sin 3x}{3}", r"\frac{\sin 4x}{4}", r"\frac{\sin 5x}{5}"]
        parts = [r"\frac{\pi - x}{2}", r"="]
        for i, t in enumerate(terms):
            parts += ([r"+"] if i else []) + [t]
        parts += [r"+\,\cdots"]
        formula = MathTex(*parts, font_size=40).to_edge(UP, buff=0.45)
        formula[0].set_color(C.FUNC)
        formula[2:].set_color(C.APPROX)
        cond = MathTex(r"(0 < x < 2\pi)", font_size=30, color=GREY_B).next_to(formula, DOWN, buff=0.15)
        term_idx = [2, 4, 6, 8, 10]
        n_lab = always_redraw(lambda: VGroup())
        counter = ValueTracker(1)

        def counter_mob():
            return MathTex(rf"n = {int(round(counter.get_value()))}", font_size=32, color=C.APPROX).to_corner(UR, buff=0.5)

        n_lab = always_redraw(counter_mob)
        S = partial_curve(ax, 1)
        with self.voiceover(
            "Here's the recipe. <bookmark mark='a'/> Start with sine of x. <bookmark mark='b'/> Add sine of 2x, over 2. "
            "<bookmark mark='c'/> Then sine of 3x over 3, <bookmark mark='d'/> and keep going, with sine of k x over "
            "k. Each wave is perfectly smooth."
        ) as vo:
            self.play(FadeOut(who))
            vo.wait_until("a")
            wave = polyline(ax, np.linspace(-np.pi, 3 * np.pi, 800), np.sin(np.linspace(-np.pi, 3 * np.pi, 800)),
                            color=C.APPROX, stroke_width=3)
            self.play(Create(wave), Write(formula[term_idx[0]]), FadeIn(n_lab), run_time=1.2)
            self.remove(wave)
            self.add(S)
            for k, mark in ((2, "b"), (3, "c"), (4, "d"), (5, None)):
                if mark:
                    vo.wait_until(mark)
                xs = np.linspace(-np.pi, 3 * np.pi, 800)
                w = polyline(ax, xs, np.sin(k * xs) / k, color=C.APPROX, stroke_width=2, stroke_opacity=0.55)
                self.play(FadeIn(w), Write(formula[term_idx[k - 1] - 1: term_idx[k - 1] + 1]), run_time=0.6)
                self.play(Transform(S, partial_curve(ax, k)), FadeOut(w), counter.animate.set_value(k), run_time=0.8)
        with self.voiceover(
            "And yet, as we add more of them, the sum hugs the sawtooth more and more closely: <bookmark mark='e'/> the "
            "straight edges, and even the sudden jump. <bookmark mark='f'/> Written out, the claim is that pi minus x, "
            "over 2, equals the infinite sum of sine k x over k, for every x strictly between 0 and 2 pi."
        ) as vo:
            for n in (10, 20, 50, 200):
                self.play(Transform(S, partial_curve(ax, n, samples=2400)), counter.animate.set_value(n), run_time=0.9)
            vo.wait_until("f")
            self.play(Write(formula[0:2]), Write(formula[-1]), FadeIn(cond))
        assert np.allclose(d["ns"], [1, 2, 3, 5, 10, 20, 50, 200])
        self.wait(0.3)
        self.S, self.saw_g, self.formula, self.cond, self.n_lab, self.xl = S, saw_g, formula, cond, n_lab, xl

    # ------------------------------------------------------------------
    def questions(self):
        d = load("sawtooth")
        n_lab = self.n_lab
        n_lab.clear_updaters()
        self.clear_scene(extra=[])
        # A magnified view of the jump at x = 2 pi
        ax = Axes(x_range=[2 * np.pi - 0.7, 2 * np.pi + 0.7, 0.7], y_range=[-2.2, 2.2, 1], x_length=8.0, y_length=5.6,
                  tips=False, axis_config={"stroke_color": GREY_C, "include_ticks": False}).shift(LEFT * 2.2 + DOWN * 0.4)
        jx = 2 * np.pi
        tick = MathTex(r"2\pi", font_size=28, color=GREY_B).next_to(ax.c2p(jx, -2.2), DOWN, buff=0.12)
        guide = DashedLine(ax.c2p(jx, -2.2), ax.c2p(jx, 2.2), color=GREY_D, stroke_width=1.5)
        left = Line(ax.c2p(jx - 0.7, (np.pi - (jx - 0.7 - 0)) / 2 - 0 if False else (np.pi - ((jx - 0.7) % (2 * np.pi))) / 2),
                    ax.c2p(jx, -np.pi / 2), color=C.FUNC, stroke_width=4)
        right = Line(ax.c2p(jx, np.pi / 2), ax.c2p(jx + 0.7, (np.pi - 0.7) / 2), color=C.FUNC, stroke_width=4)
        ends = VGroup(Circle(radius=0.07, color=C.FUNC, stroke_width=3).set_fill(BACKGROUND, 1).move_to(ax.c2p(jx, -np.pi / 2)),
                      Circle(radius=0.07, color=C.FUNC, stroke_width=3).set_fill(BACKGROUND, 1).move_to(ax.c2p(jx, np.pi / 2)))
        xs = np.linspace(jx - 0.7, jx + 0.7, 3001)

        def curve(n):
            return polyline(ax, xs, saw_partial(xs, n), color=C.APPROX, stroke_width=3)

        mag = note(r"magnified: $|x - 2\pi| < 0.7$").to_corner(UL, buff=0.4)
        S = curve(20)
        n_t = MathTex(r"n = 20", font_size=32, color=C.APPROX).to_corner(UR, buff=0.5)
        with self.voiceover(
            "Now look closely at the jump, and the questions start. <bookmark mark='a'/> Every one of these partial "
            "sums is smooth: you can differentiate it as often as you like. But the thing they approach is not even "
            "continuous. So a limit of continuous functions can fail to be continuous."
        ) as vo:
            self.play(Create(ax), FadeIn(tick), FadeIn(guide), FadeIn(mag))
            self.play(Create(left), Create(right), FadeIn(ends))
            vo.wait_until("a")
            self.play(Create(S), FadeIn(n_t), run_time=1.5)
        mid = Dot(ax.c2p(jx, 0), radius=0.09, color=WHITE)
        mid_l = label(r"every partial sum is $0$ here", font_size=26).next_to(mid, RIGHT, buff=0.25).shift(DOWN * 0.35)
        si = float(d["peak"])
        over = DashedLine(ax.c2p(jx, si), ax.c2p(jx + 0.7, si), color=C.EPS, stroke_width=2.5)
        top = DashedLine(ax.c2p(jx, np.pi / 2), ax.c2p(jx + 0.7, np.pi / 2), color=GREY_B, stroke_width=1.5)
        br = Brace(VGroup(Dot(ax.c2p(jx + 0.72, np.pi / 2), radius=0.001), Dot(ax.c2p(jx + 0.72, si), radius=0.001)),
                   RIGHT, buff=0.05, color=C.EPS)
        over_l = label(r"overshoot: $8.95\%$ of the jump,\\ whatever $n$ is", font_size=26, color=C.EPS)
        over_l.next_to(br, RIGHT, buff=0.15)
        assert abs((si - np.pi / 2) / np.pi - 0.0895) < 1e-3
        with self.voiceover(
            "At the jump itself, <bookmark mark='m'/> every partial sum equals zero, exactly halfway between the two "
            "sides. And right next to the jump, <bookmark mark='o'/> the partial sums overshoot. <bookmark mark='n'/> "
            "Add more terms, and the overshoot gets narrower, <bookmark mark='p'/> but not lower: it stays at about "
            "nine percent of the size of the jump. We'll prove that in Part 3."
        ) as vo:
            vo.wait_until("m")
            self.play(FadeIn(mid, scale=2), FadeIn(mid_l))
            vo.wait_until("o")
            self.play(Create(top), Create(over))
            vo.wait_until("n")
            for n in (60, 200):
                n_t2 = MathTex(rf"n = {n}", font_size=32, color=C.APPROX).to_corner(UR, buff=0.5)
                self.play(Transform(S, curve(n)), FadeTransform(n_t, n_t2), run_time=1.2)
                n_t = n_t2
            vo.wait_until("p")
            self.play(GrowFromCenter(br), FadeIn(over_l))
        self.wait(0.5)
        self.clear_scene()

    # ------------------------------------------------------------------
    def history(self):
        strip = timeline(lit=(), width=12.5).shift(DOWN * 0.2)
        steps = [
            (1807, r"Fourier: any function is a sum of waves?"),
            (1821, r"Cauchy: what is a limit?"),
            (1829, r"Dirichlet: what is a function?"),
            (1854, r"Riemann: what is an integral?"),
            (1872, r"Dedekind, Cantor, Weierstrass: what is a number?"),
        ]
        q = VGroup(*[label(t, font_size=30) for _, t in steps]).arrange(DOWN, aligned_edge=LEFT, buff=0.28)
        q.to_edge(UP, buff=0.6)
        lag = label(r"Lagrange (on the committee): sums of smooth waves should be smooth", font_size=26, color=GREY_B)
        lag.next_to(strip, DOWN, buff=1.0)
        with self.voiceover(
            "Lagrange, one of the mathematicians who read Fourier's memoir, <bookmark mark='l'/> objected: a sum of smooth "
            "waves ought to be smooth. The arguments that followed took most of the nineteenth century, <bookmark mark='c'/> "
            "and they forced mathematicians to say exactly what a limit is, <bookmark mark='d'/> what a function is, "
            "<bookmark mark='r'/> and what an integral is. Georg Cantor invented set theory while studying these series. "
            "<bookmark mark='n'/> And at the bottom of it all, they had to say what a number is."
        ) as vo:
            self.play(FadeIn(strip), FadeIn(q[0]))
            self.play(Transform(strip, timeline(lit=(1807,), width=12.5).shift(DOWN * 0.2)))
            vo.wait_until("l")
            self.play(FadeIn(lag))
            for mark, i in (("c", 1), ("d", 2), ("r", 3), ("n", 4)):
                vo.wait_until(mark)
                lit = tuple(y for y, _ in steps[: i + 1])
                self.play(FadeIn(q[i], shift=RIGHT * 0.2),
                          Transform(strip, timeline(lit=lit, width=12.5, show_labels=False).shift(DOWN * 0.2)))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def holes(self):
        win = Window(1.5, 1.2, y=-0.6)
        axis, dust, labs = win.axis(), win.dust(height=1.4), win.labels()
        approx = [1.0, 1.4, 1.41, 1.414, 1.4142, 1.41421, 1.414213]
        dots = VGroup(*[win.marker(v, color=C.SEQ, radius=0.075) for v in approx])
        seq = MathTex(*[rf"{v:g}," for v in approx], r"\ldots", font_size=40, color=C.SEQ).to_edge(UP, buff=0.7)
        hole = win.marker(SQRT2, color=C.HOLE, radius=0.12, hollow=True)
        hole_l = always_redraw(lambda: MathTex(r"\sqrt2", font_size=34, color=C.HOLE)
                               .move_to(win.P(SQRT2, 1.95)))
        width_l = always_redraw(lambda: Text(f"window width {sci_text(win.width, 1)}", font_size=20, color=GREY_B)
                                .to_corner(DR, buff=0.3))
        why_l = label(r"Each fraction $p/q$ (in lowest terms) is a tick; smaller $q$, taller tick.", font_size=24,
                      color=GREY_B).to_edge(DOWN, buff=0.35)

        lim = MathTex(r"\sum_{k=1}^{\infty} \frac{\sin kx}{k}", r"\;=\;", r"\lim_{n\to\infty}",
                      r"\sum_{k=1}^{n} \frac{\sin kx}{k}", font_size=46).move_to(UP * 1.2)
        lim[0].set_color(C.APPROX)
        lim[3].set_color(C.APPROX)
        land = label(r"a limit needs a place to land", font_size=32, color=C.EPS).next_to(lim, DOWN, buff=0.5)
        with self.voiceover(
            "Here's why. <bookmark mark='i'/> An infinite sum is a limit: we add terms, and ask what the partial sums "
            "approach. <bookmark mark='l'/> But a limit needs a place to land. <bookmark mark='q'/> These are the "
            "rational numbers, the fractions, drawn as a "
            "ruler: each fraction gets a tick, and fractions with smaller denominators get taller ticks. "
            "<bookmark mark='s'/> Now take the numbers 1, 1.4, 1.41, 1.414, each one the square root of two cut off "
            "one digit later."
        ) as vo:
            self.play(Write(lim))
            vo.wait_until("l")
            self.play(FadeIn(land, shift=UP * 0.2))
            vo.wait_until("q")
            self.play(FadeOut(lim), FadeOut(land))
            self.play(Create(axis), FadeIn(dust), FadeIn(labs), FadeIn(why_l))
            vo.wait_until("s")
            for i in range(4):
                self.play(FadeIn(dots[i], scale=2), FadeIn(seq[i]), run_time=0.5)
        with self.voiceover(
            "Zoom in, and they crowd closer and closer together, <bookmark mark='h'/> closing in on a spot. But no "
            "fraction sits there. The square of a fraction is never exactly two, so if fractions were the only "
            "numbers we had, these numbers would have nothing to approach. <bookmark mark='t'/> The rational numbers "
            "have holes."
        ) as vo:
            self.play(FadeOut(why_l))
            self.add(width_l)
            for w, i in ((0.12, 4), (0.012, 5), (0.0012, 6)):
                self.play(*win.zoom_to(1.414 + w * 0.05, w), FadeIn(seq[min(i, 6)]),
                          FadeIn(dots[min(i, 6)]), run_time=1.6)
            vo.wait_until("h")
            self.play(*win.zoom_to(SQRT2, 2.5e-6), FadeIn(seq[-1]), run_time=2.5)
            self.play(FadeIn(hole, scale=3), FadeIn(hole_l))
            vo.wait_until("t")
            self.play(Indicate(hole_l, color=C.HOLE, scale_factor=1.3))
        self.wait(0.3)
        for m in (axis, dust, labs, hole, hole_l, width_l, *dots):
            m.clear_updaters()
        self.clear_scene()

    # ------------------------------------------------------------------
    def series(self):
        names = [r"the real\\numbers", r"limits", r"integrals,\\$C(X)$", r"$\R^n$", r"measure", r"$L^p$ and\\Hilbert",
                 r"complex\\analysis", r"Banach\\spaces", r"distri-\\butions", r"spectral\\theory"]
        season_col = [C.SEQ] * 4 + [C.MEASURE] * 3 + [C.OPERATOR] * 3
        boxes = VGroup()
        for i, (nm, col) in enumerate(zip(names, season_col)):
            b = RoundedRectangle(width=1.12, height=0.82, corner_radius=0.1, stroke_color=col, stroke_width=2.5,
                                 fill_color=col, fill_opacity=0.12)
            t = label(str(i + 1), font_size=34, color=col).move_to(b)
            n = Tex(r"\begin{tabular}{c}" + nm.replace(r"\\", r"\\") + r"\end{tabular}", font_size=20,
                    color=GREY_A).next_to(b, DOWN, buff=0.15)
            boxes.add(VGroup(b, t, n))
        boxes.arrange(RIGHT, buff=0.18).move_to(DOWN * 0.9)
        for i, gap in ((3, 0.35), (6, 0.35)):
            for b in boxes[i + 1:]:
                b.shift(RIGHT * gap)
        boxes.move_to(DOWN * 0.9)
        groups = [(0, 4, r"\textit{Principles of Mathematical Analysis}"), (4, 7, r"\textit{Real and Complex Analysis}"),
                  (7, 10, r"\textit{Functional Analysis}")]
        heads = VGroup()
        for a, b, t in groups:
            grp = VGroup(*[bx[0] for bx in boxes[a:b]])
            br = Brace(grp, UP, buff=0.12, color=season_col[a])
            tl = label(t, font_size=24 if b - a > 3 else 22, color=season_col[a]).next_to(br, UP, buff=0.12)
            if tl.width > grp.width + 0.6:
                tl.width = grp.width + 0.6
            heads.add(VGroup(br, tl))
        title = label(r"From the real line to functional analysis", font_size=46).to_edge(UP, buff=0.5)
        who = label(r"following the arc of Walter Rudin's three textbooks", font_size=30, color=GREY_A)
        who.next_to(title, DOWN, buff=0.3)
        here = SurroundingRectangle(boxes[0][0], color=C.EPS, buff=0.08, corner_radius=0.12, stroke_width=4)
        here_l = label(r"you are here", font_size=24, color=C.EPS).next_to(boxes[0], DOWN, buff=0.15)
        with self.voiceover(
            "This video is Part 1 of a series that builds analysis from those holes <bookmark mark='a'/> all the way to "
            "functional analysis: the mathematics of infinite-dimensional spaces, which is where Fourier's question "
            "finally gets its full answer. <bookmark mark='b'/> The route follows Walter Rudin's three classic "
            "textbooks: <bookmark mark='p'/> Principles of Mathematical Analysis, <bookmark mark='r'/> Real and "
            "Complex Analysis, <bookmark mark='f'/> and Functional Analysis. <bookmark mark='h'/> Every theorem we use, "
            "we prove on screen."
        ) as vo:
            self.play(FadeIn(title))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(b, shift=UP * 0.2) for b in boxes], lag_ratio=0.12), run_time=2.4)
            vo.wait_until("b")
            self.play(FadeIn(who))
            for mark, h in zip("prf", heads):
                vo.wait_until(mark)
                self.play(GrowFromCenter(h[0]), FadeIn(h[1]))
            vo.wait_until("h")
            self.play(Create(here), FadeIn(here_l))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def thesis(self):
        m_max = 5
        cells = VGroup()
        size = 0.78
        origin = np.array([-3.4, 1.6, 0])
        for m in range(1, m_max + 1):
            for n in range(1, m_max + 1):
                v = m / (m + n)
                sq = Square(side_length=size * 0.94, stroke_width=0, fill_color=interpolate_color(ManimColor("#1B2333"),
                                                                                                  ManimColor(C.EPS), v),
                            fill_opacity=1)
                sq.move_to(origin + np.array([(n - 1) * size, -(m - 1) * size, 0]))
                t = MathTex(rf"\tfrac{{{m}}}{{{m + n}}}", font_size=24, color=BLACK if v > 0.55 else WHITE).move_to(sq)
                cells.add(VGroup(sq, t))
        corner = cells[0][0].get_corner(UL)
        n_lab = MathTex(r"n \to", font_size=30, color=GREY_B).next_to(cells[m_max - 1], RIGHT, buff=0.25).shift(UP * size)
        m_lab = MathTex(r"m \downarrow", font_size=30, color=GREY_B).next_to(cells[0], LEFT, buff=0.3)
        a_mn = MathTex(r"a_{mn} = \frac{m}{m+n}", font_size=40).move_to(corner + np.array([1.9, 1.2, 0]))
        rows_lim = VGroup(*[MathTex(r"\to 0", font_size=28, color=C.LOWER_SUM).next_to(cells[(m - 1) * m_max + m_max - 1],
                                                                                      RIGHT, buff=0.2)
                            for m in range(1, m_max + 1)])
        cols_lim = VGroup(*[MathTex(r"\downarrow 1", font_size=28, color=C.UPPER_SUM).next_to(cells[(m_max - 1) * m_max + n - 1],
                                                                                            DOWN, buff=0.2)
                            for n in range(1, m_max + 1)])
        r1 = MathTex(r"\lim_{m\to\infty}\,\lim_{n\to\infty} a_{mn} = 0", font_size=40, color=C.LOWER_SUM)
        r2 = MathTex(r"\lim_{n\to\infty}\,\lim_{m\to\infty} a_{mn} = 1", font_size=40, color=C.UPPER_SUM)
        res = VGroup(r1, r2).arrange(DOWN, buff=0.5).move_to([3.6, 0.3, 0])
        tag = label(r"Rudin, \textit{Principles}, 7.2", font_size=22, color=GREY_B).next_to(res, DOWN, buff=0.5)
        kinds = VGroup(
            MathTex(r"\text{continuity:}", r"\;\lim_{y\to x} f(y) = f(x)", font_size=36),
            MathTex(r"\text{derivative:}", r"\;\lim_{h\to 0} \frac{f(x+h) - f(x)}{h}", font_size=36),
            MathTex(r"\text{integral:}", r"\;\lim_{n\to\infty} \sum_{i=1}^{n} f(x_i)\,\Delta x", font_size=36),
            MathTex(r"\text{infinite sum:}", r"\;\lim_{n\to\infty} \sum_{k=1}^{n} a_k", font_size=36),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.35).move_to(UP * 0.2)
        for k in kinds:
            k[0].set_color(GREY_A)
            k[1].set_color(C.EPS)
        q_swap = label(r"When may we swap the order of two limits?", font_size=38, color=C.EPS).to_edge(DOWN, buff=0.6)
        with self.voiceover(
            "One idea runs through the whole series. <bookmark mark='k'/> Continuity, derivatives, integrals and "
            "infinite sums are all limits, <bookmark mark='w'/> and almost every theorem we'll prove answers a single "
            "question: when may we swap the order of two limits? <bookmark mark='g'/> Here's the simplest example of "
            "what goes wrong. Take m over m plus n. "
            "<bookmark mark='r'/> Send n to infinity first, and every row goes to zero, so the answer is zero. "
            "<bookmark mark='c'/> Send m to infinity first, and every column goes to one. Same numbers, different "
            "order, different answer."
        ) as vo:
            self.play(LaggedStart(*[FadeIn(k_, shift=RIGHT * 0.2) for k_ in kinds], lag_ratio=0.35), run_time=2.2)
            vo.wait_until("w")
            self.play(FadeIn(q_swap, shift=UP * 0.2))
            vo.wait_until("g")
            self.play(FadeOut(kinds), FadeOut(q_swap))
            self.play(FadeIn(a_mn), LaggedStart(*[FadeIn(c) for c in cells], lag_ratio=0.03), FadeIn(n_lab),
                      FadeIn(m_lab), run_time=1.6)
            vo.wait_until("r")
            self.play(LaggedStart(*[FadeIn(r, shift=RIGHT * 0.2) for r in rows_lim], lag_ratio=0.15), Write(r1))
            vo.wait_until("c")
            self.play(LaggedStart(*[FadeIn(c, shift=DOWN * 0.2) for c in cols_lim], lag_ratio=0.15), Write(r2),
                      FadeIn(tag))
        swap = MathTex(r"\int \sum_k \frac{\sin kx}{k}\,dx", r"\;\overset{?}{=}\;", r"\sum_k \int \frac{\sin kx}{k}\,dx",
                       font_size=42).to_edge(DOWN, buff=0.55)
        swap[0].set_color(C.FUNC)
        swap[2].set_color(C.APPROX)
        with self.voiceover(
            "Fourier's sum is exactly this kind of question. <bookmark mark='s'/> Is the integral of the sum the sum of "
            "the integrals? Each new space in this series is invented to make one more swap like this legal."
        ) as vo:
            vo.wait_until("s")
            self.play(Write(swap))
        self.wait(0.4)
        self.clear_scene()

    # ------------------------------------------------------------------
    def plan(self):
        led = ledger(filled=0, highlight=1).scale(0.92).shift(DOWN * 0.2)
        with self.voiceover(
            "We'll keep a ledger. <bookmark mark='l'/> Each part adds one row: a new space, the reason it has no "
            "holes, what compactness means there, which limits we've earned the right to swap, and how far we've "
            "gotten with Fourier. <bookmark mark='r'/> Today's row is the first: the real numbers."
        ) as vo:
            self.play(FadeIn(led.head), LaggedStart(*[FadeIn(r) for r in led.rows], lag_ratio=0.08), FadeIn(led[-1]),
                      run_time=2)
            vo.wait_until("r")
            self.play(FadeIn(led[0]))
        self.clear_scene()
        chapters = [
            r"Holes in the rational line", r"Filling the holes: Dedekind cuts", r"Archimedes, density and decimals",
            r"Counting infinities", r"What ``close'' means: metric spaces", r"Open and closed sets",
            r"Compactness", r"Heine--Borel, by bisection", r"The Cantor set", r"Connectedness",
            r"A first space of functions",
        ]
        items = VGroup(*[label(rf"{i + 1}.\; {t}", font_size=28) for i, t in enumerate(chapters)])
        col1 = VGroup(*items[:6]).arrange(DOWN, aligned_edge=LEFT, buff=0.3)
        col2 = VGroup(*items[6:]).arrange(DOWN, aligned_edge=LEFT, buff=0.3)
        cols = VGroup(col1, col2).arrange(RIGHT, buff=1.0, aligned_edge=UP).shift(DOWN * 0.3)
        head = label(r"Part 1: The Real Numbers and the Shape of Space", font_size=44).to_edge(UP, buff=0.5)
        with self.voiceover(
            "Here's the plan for today. <bookmark mark='a'/> We'll find the holes in the rational numbers and fill them, "
            "in a way that makes having no holes a theorem. <bookmark mark='b'/> We'll count infinities. "
            "<bookmark mark='c'/> Then we'll step back and ask what close means in general, which gives us the "
            "vocabulary of everything that follows: open sets, compact sets and connected sets. "
            "<bookmark mark='d'/> And we'll end with a warning: the very first space of functions we meet already "
            "breaks one of today's best theorems."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(items[i], shift=RIGHT * 0.2) for i in range(3)], lag_ratio=0.3))
            vo.wait_until("b")
            self.play(FadeIn(items[3], shift=RIGHT * 0.2))
            vo.wait_until("c")
            self.play(LaggedStart(*[FadeIn(items[i], shift=RIGHT * 0.2) for i in range(4, 10)], lag_ratio=0.2))
            vo.wait_until("d")
            self.play(FadeIn(items[10], shift=RIGHT * 0.2))
            self.play(Indicate(items[10], color=C.PATHOLOGY))
        self.wait(0.6)
        self.clear_scene()
