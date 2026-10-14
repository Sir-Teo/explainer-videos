from __future__ import annotations

import math

import numpy as np

from explainer.analysis import *  # noqa: F403
from videos.analysis1.common import (SQRT2, Window, load, partial_curve, polyline, saw, saw_axes, saw_graph,
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
        # the axis numbers sit under the plot box, where no curve passes (the partial sums stay inside |y| < 2)
        xl = VGroup()
        for t, v in ((r"0", 0), (r"\pi", np.pi), (r"2\pi", 2 * np.pi)):
            base = ax.c2p(v, -2.2)
            xl.add(VGroup(Line(base, base + UP * 0.12, color=GREY_C, stroke_width=2),
                          MathTex(t, font_size=28, color=GREY_B).next_to(base, DOWN, buff=0.12)))
        saw_g = saw_graph(ax)
        who = label(r"Joseph Fourier, 1807", font_size=30, color=GREY_A).to_corner(UL, buff=0.45)
        self.ax = ax

        # Fourier's subject: heat in a rod whose ends are kept at 0, starting from the sawtooth profile.
        # u(x, t) = sum_k sin(kx)/k * exp(-k^2 t) solves the heat equation; each wave decays at its own rate.
        rx = np.linspace(0, 2 * np.pi, 161)
        xm = (rx[:-1] + rx[1:]) / 2
        ks = np.arange(1, 401)

        def temp(t):
            return (np.sin(np.outer(xm, ks)) / ks * np.exp(-ks ** 2 * t)).sum(1)

        inner = (xm > 0.4) & (xm < 2 * np.pi - 0.4)
        assert np.abs(temp(1e-4)[inner] - saw(xm[inner])).max() < 0.05  # it starts as the sawtooth
        peaks = [np.abs(temp(t)).max() for t in (1e-4, 0.05, 0.2, 0.6)]
        assert all(a > b for a, b in zip(peaks, peaks[1:]))  # and cools
        cold, mid_c, hot = ManimColor(C.FUNC), ManimColor("#3A4250"), ManimColor(C.TEMPERATURE)

        def tcolor(u):
            s_ = float(np.clip(u / (np.pi / 2), -1, 1))
            return interpolate_color(mid_c, hot, s_) if s_ >= 0 else interpolate_color(mid_c, cold, -s_)

        rod_w, rod_y = 10.0, -0.4
        cells = VGroup(*[Rectangle(width=rod_w / len(xm) + 0.004, height=0.7, stroke_width=0, fill_opacity=1)
                         .move_to([-rod_w / 2 + (i + 0.5) * rod_w / len(xm), rod_y, 0]) for i in range(len(xm))])
        rod_t = ValueTracker(1e-4)

        def paint(g):
            for c_, u in zip(g, temp(rod_t.get_value())):
                c_.set_fill(tcolor(u), 1)

        paint(cells)
        cells.add_updater(paint)
        rod_frame = SurroundingRectangle(cells, buff=0.0, color=GREY_C, stroke_width=1.5)
        rod_l = VGroup(label(r"hot", font_size=24, color=C.TEMPERATURE), label(r"cold", font_size=24, color=C.FUNC))
        rod_l[0].next_to(cells, UP, buff=0.15).set_x(-rod_w / 2 + rod_w * 0.12)
        rod_l[1].next_to(cells, UP, buff=0.15).set_x(rod_w / 2 - rod_w * 0.12)
        rod_cap = label(r"temperature along a rod, its ends kept at $0$: \ the heat flows and evens out",
                        font_size=24, color=GREY_B).next_to(cells, DOWN, buff=0.35)
        rod = VGroup(cells, rod_frame, rod_l, rod_cap)

        with self.voiceover(
            "In 1807, Joseph Fourier submitted a memoir on how heat flows through a solid body. Buried in it was a "
            "claim that took mathematics a century to digest. <bookmark mark='s'/> Take a function with a corner, or "
            "even a jump, like this sawtooth. <bookmark mark='w'/> Fourier said that it can be written as a sum of "
            "sine waves."
        ) as vo:
            self.play(FadeIn(who), FadeIn(rod))
            self.play(rod_t.animate.set_value(0.6), run_time=max(1.0, vo.until("s") - 0.3),
                      rate_func=lambda a: a ** 2)
            vo.wait_until("s")
            cells.clear_updaters()
            self.play(FadeOut(rod), Create(ax), FadeIn(xl), run_time=1.0)
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
            self.bring_to_front(saw_g.ends)  # the target's open ends stay visible over the partial sums
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

        mag = note(r"magnified: $|x - 2\pi| < 0.7$").to_corner(UL, buff=0.45)
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
        over_l = label(r"overshoot $\to 8.95\%$ of the jump\\ as $n$ grows", font_size=26, color=C.EPS)
        over_l.next_to(br, RIGHT, buff=0.15)
        assert abs((si - np.pi / 2) / np.pi - 0.0895) < 1e-3
        with self.voiceover(
            "At the jump itself, <bookmark mark='m'/> every partial sum equals zero, exactly halfway between the two "
            "sides. And right next to the jump, <bookmark mark='o'/> the partial sums overshoot. <bookmark mark='n'/> "
            "Add more terms, and the overshoot gets narrower, <bookmark mark='p'/> but not lower: it settles at about "
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
                          Transform(strip, timeline(lit=lit, width=12.5).shift(DOWN * 0.2)))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def holes(self):
        win = Window(1.5, 1.2, y=-0.6)
        axis, dust, labs = win.axis(), win.dust(height=1.4), win.labels()
        dec = str(load("sqrt2")["dec"])
        approx_s = ["1"] + [dec[: k + 2] for k in range(1, 7)]  # sqrt 2 cut off after k digits
        approx = [float(t) for t in approx_s]
        assert approx_s == ["1", "1.4", "1.41", "1.414", "1.4142", "1.41421", "1.414213"]
        assert all(a < b <= SQRT2 for a, b in zip(approx, approx[1:])) and len(set(approx_s)) == 7
        dots = VGroup(*[win.marker(v, color=C.SEQ, radius=0.075) for v in approx])
        seq = MathTex(*[t + "," for t in approx_s], r"\ldots", font_size=40, color=C.SEQ).to_edge(UP, buff=0.7)
        hole = win.marker(SQRT2, color=C.HOLE, radius=0.12, hollow=True)
        hole_l = always_redraw(lambda: MathTex(r"\sqrt2", font_size=34, color=C.HOLE)
                               .move_to(win.P(SQRT2, 1.45)))
        hole_lead = always_redraw(lambda: Line(win.P(SQRT2, 0.2), win.P(SQRT2, 1.15), color=GREY_B, stroke_width=1.5))
        width_l = always_redraw(lambda: Text(f"window width {sci_text(win.width, 1)}", font_size=22, color=GREY_B)
                                .to_corner(DR, buff=0.45))
        why_l = label(r"Each fraction $p/q$ (in lowest terms) is a tick; smaller $q$, taller tick.", font_size=24,
                      color=GREY_B).to_edge(DOWN, buff=0.35)

        lim = MathTex(r"\sum_{k=1}^{\infty} \frac{\sin kx}{k}", r"\;=\;", r"\lim_{n\to\infty}",
                      r"\sum_{k=1}^{n} \frac{\sin kx}{k}", font_size=46).move_to(UP * 1.2)
        lim[0].set_color(C.APPROX)
        lim[3].set_color(C.APPROX)
        land = label(r"a limit needs a place to land", font_size=32, color=C.EPS).next_to(lim, DOWN, buff=0.5)
        # the partial sums at x = 1, landing on (pi - 1)/2
        Ls = (np.pi - 1) / 2
        sn = np.cumsum(np.sin(np.arange(1, 41)) / np.arange(1, 41))
        assert abs(sn[-1] - Ls) < 0.03 and abs(saw(np.array([1.0]))[0] - Ls) < 1e-12
        Xl = lambda v: (v - 1.05) * 10.0  # noqa: E731
        yl_ = -1.9
        lline = Line([Xl(0.6), yl_, 0], [Xl(1.5), yl_, 0], color=GREY_C, stroke_width=2)
        target = VGroup(Line([Xl(Ls), yl_ - 0.25, 0], [Xl(Ls), yl_ + 0.25, 0], color=C.EPS, stroke_width=3),
                        MathTex(r"\tfrac{\pi - 1}{2}", font_size=28, color=C.EPS).next_to([Xl(Ls), yl_ - 0.25, 0], DOWN,
                                                                                         buff=0.12))
        sdots = VGroup(*[Dot([Xl(v), yl_ + 0.0, 0], radius=0.06, color=C.APPROX).set_opacity(0.35 + 0.65 * (k + 1) / len(sn))
                         for k, v in enumerate(sn)])
        s_cap = MathTex(r"\sum_{k=1}^{n} \frac{\sin k}{k}, \ n = 1, \ldots, 40", font_size=28, color=C.APPROX)
        s_cap.next_to(lline, UP, buff=0.35).set_x(Xl(0.62) + 1.6)
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
            self.play(FadeIn(land, shift=UP * 0.2), Create(lline), FadeIn(s_cap))
            self.play(LaggedStart(*[FadeIn(d_, scale=1.5) for d_ in sdots], lag_ratio=0.15), FadeIn(target), run_time=2.4)
            vo.wait_until("q")
            self.play(FadeOut(lim), FadeOut(land), FadeOut(VGroup(lline, target, sdots, s_cap)))
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
            self.play(FadeIn(hole, scale=3), FadeIn(hole_l), FadeIn(hole_lead))
            vo.wait_until("t")
            self.play(Indicate(hole_l, color=C.HOLE, scale_factor=1.3))
        self.wait(0.3)
        for m in (axis, dust, labs, hole, hole_l, hole_lead, width_l, *dots):
            m.clear_updaters()
        self.clear_scene()

    # ------------------------------------------------------------------
    def series(self):
        names = [r"the real\\numbers", r"limits", r"integrals,\\$C(X)$", r"$\R^n$", r"measure", r"$L^p$ and\\Hilbert",
                 r"complex\\analysis", r"Banach\\spaces", r"distri-\\butions", r"spectral\\theory"]
        season_col = [C.SEQ] * 4 + [C.MEASURE] * 3 + [C.OPERATOR] * 3
        boxes = VGroup()
        for i, (nm, col) in enumerate(zip(names, season_col)):
            b = RoundedRectangle(width=1.05, height=0.82, corner_radius=0.1, stroke_color=col, stroke_width=2.5,
                                 fill_color=col, fill_opacity=0.12)
            t = label(str(i + 1), font_size=34, color=col).move_to(b)
            n = Tex(r"\begin{tabular}{c}" + nm + r"\end{tabular}", font_size=22, color=GREY_A)
            boxes.add(VGroup(b, t, n))
        # line up the boxes themselves (not box + caption), then hang each caption from its box, tops aligned
        frames = VGroup(*[bx[0] for bx in boxes]).arrange(RIGHT, buff=0.15)
        for i, gap in ((3, 0.35), (6, 0.35)):
            for f_ in frames[i + 1:]:
                f_.shift(RIGHT * gap)
        frames.move_to(DOWN * 0.6)
        for bx in boxes:
            bx[1].move_to(bx[0])
            bx[2].next_to(bx[0], DOWN, buff=0.15)
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
                t = MathTex(rf"\frac{{{m}}}{{{m + n}}}", font_size=28, color=BLACK if v > 0.45 else WHITE).move_to(sq)
                cells.add(VGroup(sq, t))
        corner = cells[0][0].get_corner(UL)
        n_lab = MathTex(r"n \to", font_size=30, color=GREY_B).next_to(cells[m_max - 1], RIGHT, buff=0.25).shift(UP * size)
        m_lab = MathTex(r"m \downarrow", font_size=30, color=GREY_B).next_to(cells[0], LEFT, buff=0.3)
        a_mn = MathTex(r"a_{mn} = \frac{m}{m+n}", font_size=40).move_to(corner + np.array([1.9, 1.2, 0]))
        # n first (along each row) in the sequence colour; m first (down each column) in the "response" colour
        rows_lim = VGroup(*[MathTex(r"\to 0", font_size=28, color=C.SEQ).next_to(cells[(m - 1) * m_max + m_max - 1],
                                                                                RIGHT, buff=0.2)
                            for m in range(1, m_max + 1)])
        cols_lim = VGroup(*[MathTex(r"\downarrow 1", font_size=28, color=C.DELTA).next_to(cells[(m_max - 1) * m_max + n - 1],
                                                                                        DOWN, buff=0.2)
                            for n in range(1, m_max + 1)])
        r1 = MathTex(r"\lim_{m\to\infty}\,\lim_{n\to\infty} a_{mn} = 0", font_size=40, color=C.SEQ)
        r2 = MathTex(r"\lim_{n\to\infty}\,\lim_{m\to\infty} a_{mn} = 1", font_size=40, color=C.DELTA)
        res = VGroup(r1, r2).arrange(DOWN, buff=0.5).move_to([3.6, 0.3, 0])
        tag = label(r"Rudin, \textit{Principles}, 7.2", font_size=22, color=GREY_B).next_to(res, DOWN, buff=0.5)
        kinds = VGroup(
            MathTex(r"\text{continuity:}", r"\;\lim_{y\to x} f(y) = f(x)", font_size=36),
            MathTex(r"\text{derivative:}", r"\;\lim_{h\to 0} \frac{f(x+h) - f(x)}{h}", font_size=36),
            MathTex(r"\text{integral:}", r"\;\lim_{n\to\infty} \sum_{i=1}^{n} f(x_i)\,\Delta x", font_size=36),
            MathTex(r"\text{infinite sum:}", r"\;\lim_{n\to\infty} \sum_{k=1}^{n} a_k", font_size=36),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.35).move_to(UP * 0.25)
        kinds.to_edge(LEFT, buff=0.9)
        for k in kinds:
            k[0].set_color(GREY_A)
            k[1].set_color(C.EPS)
        thumbs = VGroup(*[self.thumb(i).move_to([3.9, k.get_y(), 0]) for i, k in enumerate(kinds)])
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
            self.play(LaggedStart(*[AnimationGroup(FadeIn(k_, shift=RIGHT * 0.2), FadeIn(t_, shift=LEFT * 0.2))
                                    for k_, t_ in zip(kinds, thumbs)], lag_ratio=0.35), run_time=2.2)
            vo.wait_until("w")
            self.play(FadeIn(q_swap, shift=UP * 0.2))
            vo.wait_until("g")
            self.play(FadeOut(kinds), FadeOut(thumbs), FadeOut(q_swap))
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
        grid_g = VGroup(cells, rows_lim, cols_lim, n_lab, m_lab, a_mn)
        with self.voiceover(
            "Fourier's sum is exactly this kind of question. <bookmark mark='s'/> Is the integral of the sum the sum of "
            "the integrals? Each new space in this series is invented to make one more swap like this legal."
        ) as vo:
            # make room under the grid for the swap
            self.play(grid_g.animate.scale(0.78, about_edge=UL), run_time=0.8)
            vo.wait_until("s")
            self.play(Write(swap))
        self.wait(0.4)
        self.clear_scene()

    @staticmethod
    def thumb(kind: int) -> VGroup:
        """A 1.8 x 1.0 picture of each kind of limit: continuity, derivative, integral, infinite sum."""
        W, H = 1.8, 1.0

        def P(u, v):  # u, v in [0, 1]
            return np.array([(u - 0.5) * W, (v - 0.5) * H, 0])

        base = Line(P(0, 0), P(1, 0), color=GREY_C, stroke_width=1.5)
        g = VGroup(base)
        if kind == 0:  # f(y) -> f(x) as y -> x
            f = lambda u: 0.25 + 0.5 * u + 0.12 * np.sin(5 * u)  # noqa: E731
            us = np.linspace(0, 1, 100)
            g.add(VMobject(color=C.FUNC, stroke_width=3).set_points_smoothly([P(u, f(u)) for u in us]))
            x0 = 0.35
            for k, du in enumerate((0.55, 0.32, 0.16)):
                g.add(Dot(P(x0 + du, f(x0 + du)), radius=0.045, color=C.EPS).set_opacity(0.45 + 0.25 * k))
            g.add(Dot(P(x0, f(x0)), radius=0.06, color=WHITE))
        elif kind == 1:  # secants turning into the tangent of sin at x0
            sx = lambda u: 0.15 + 0.7 * np.sin(np.pi * u)  # noqa: E731  (sin on [0, pi], scaled)
            us = np.linspace(0, 1, 100)
            g.add(VMobject(color=C.FUNC, stroke_width=3).set_points_smoothly([P(u, sx(u)) for u in us]))
            x0 = 0.22
            slope = 0.7 * np.pi * np.cos(np.pi * x0)
            secs = [(sx(x0 + h) - sx(x0)) / h for h in (0.45, 0.25, 0.1)]
            assert all(abs(a - slope) > abs(b - slope) for a, b in zip(secs, secs[1:]))  # secants -> tangent
            for k, m_ in enumerate(secs):
                g.add(Line(P(x0 - 0.12, sx(x0) - 0.12 * m_), P(x0 + 0.5, sx(x0) + 0.5 * m_), color=GREY_B,
                           stroke_width=1.5, stroke_opacity=0.4 + 0.2 * k))
            g.add(Line(P(x0 - 0.15, sx(x0) - 0.15 * slope), P(x0 + 0.32, sx(x0) + 0.32 * slope), color=C.EPS,
                       stroke_width=3), Dot(P(x0, sx(x0)), radius=0.05, color=WHITE))
        elif kind == 2:  # six midpoint rectangles under sin on [0, pi]
            n = 6
            mids = (np.arange(n) + 0.5) / n
            riemann = (np.sin(np.pi * mids) * np.pi / n).sum()
            assert abs(riemann - 2.0) < 0.05  # the Riemann sum is already close to the integral, 2
            for u in mids:
                h = 0.9 * np.sin(np.pi * u)
                g.add(Rectangle(width=W / n * 0.94, height=h * H, stroke_color=C.MEASURE, stroke_width=1,
                                fill_color=C.MEASURE, fill_opacity=0.35).move_to(P(u, h / 2)))
            us = np.linspace(0, 1, 100)
            g.add(VMobject(color=C.FUNC, stroke_width=3).set_points_smoothly([P(u, 0.9 * np.sin(np.pi * u)) for u in us]))
        else:  # partial sums of 1/2 + 1/4 + ... climbing to 1
            sums = np.cumsum(0.5 ** np.arange(1, 8))
            assert np.allclose(sums, 1 - 0.5 ** np.arange(1, 8))
            g.add(DashedLine(P(0, 0.9), P(1, 0.9), color=GREY_B, stroke_width=1.5, dash_length=0.06))
            pts = []
            for i, v in enumerate(sums):
                u0, u1 = i / len(sums), (i + 1) / len(sums)
                pts += [P(u0, 0.9 * v), P(u1, 0.9 * v)]
            g.add(VMobject(color=C.APPROX, stroke_width=3).set_points_as_corners(pts))
        return g

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
            self.play(FadeIn(led[0]), led.rows[0].animate.set_color(WHITE))  # today's row, readable
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
