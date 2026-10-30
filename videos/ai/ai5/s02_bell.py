from __future__ import annotations

import math

import numpy as np

from explainer.ai import *  # noqa: F403
from videos.ai.ai5.common import DATA, HIST, MODEL, PART, curve, hist_shape, load, normal_pdf

DX, DY = 0.36, 0.27  # peg spacing
TOP = 3.0  # height of the first peg


def peg_xy(r, k, x0):
    """Peg k of row r (k = number of right bounces so far)."""
    return np.array([x0 + (k - r / 2) * DX, TOP - r * DY, 0])


class Bell(VoiceoverScene):
    def construct(self):
        self.card()
        self.lln()
        self.galton()
        self.clt()
        self.convolution()
        self.rate()

    # ------------------------------------------------------------------
    def card(self):
        card = chapter_card(1, r"The bell curve", r"Why does the same shape turn up everywhere?", part=PART)
        with self.voiceover("Chapter one. The bell curve."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))

    # ------------------------------------------------------------------
    def lln(self):
        d = load("lln")
        idx, run, n = np.asarray(d["idx"], float), np.asarray(d["run"]), int(d["n"])
        ax = Axes(x_range=[0, math.log10(n), 1], y_range=[0, 1, 0.25], x_length=8.6, y_length=4.4, tips=False,
                  axis_config={"stroke_color": GREY_C, "include_ticks": True, "tick_size": 0.04}).move_to([-1.6, -0.5, 0])
        xt = VGroup(*[MathTex(t, font_size=22, color=GREY_B).next_to(ax.c2p(v, 0), DOWN, buff=0.12)
                      for t, v in (("1", 0), ("10", 1), ("100", 2), ("1{,}000", 3))])
        yt = VGroup(*[MathTex(t, font_size=22, color=GREY_B).next_to(ax.c2p(0, v), LEFT, buff=0.12)
                      for t, v in (("0", 0), (r"\tfrac12", 0.5), ("1", 1))])
        xl = label(r"flips", font_size=24, color=GREY_A).next_to(xt, DOWN, buff=0.15)
        yl = label(r"share of heads so far", font_size=24, color=GREY_A).next_to(ax, UP, buff=0.15).align_to(ax, LEFT)
        lx = np.log10(idx)
        cols = [interpolate_color(ManimColor(DATA), ManimColor(C.BITS), k / 5) for k in range(6)]
        runs = VGroup(*[VMobject(color=cols[k], stroke_width=2.5).set_points_as_corners(
            [ax.c2p(x, y) for x, y in zip(lx, run[k])]) for k in range(6)])
        ns = np.logspace(0, math.log10(n), 120)
        bnd = band(ax, np.log10(ns), np.maximum(0.5 - 1 / np.sqrt(ns), 0), np.minimum(0.5 + 1 / np.sqrt(ns), 1), C.BITS, 0.12)
        bl = label(r"$\tfrac12 \pm 1/\sqrt{n}$: \ two standard deviations", font_size=22, color=C.BITS)
        bl.next_to(ax.c2p(math.log10(n), 0.5 + 1 / math.sqrt(n)), UP, buff=0.5).shift(LEFT * 1.0)
        hc = history_card(1713, r"Jacob Bernoulli, \textit{Ars Conjectandi}", r"averages settle: \ the law of large "
                          r"numbers, \ his ``golden theorem''", width=4.6).to_corner(UR, buff=0.35)
        lo, hi = float(d["final"].min()), float(d["final"].max())
        with self.voiceover(
            "Flip a fair coin and track the share of heads. <bookmark mark='a'/> Six runs of five thousand flips all "
            f"settle toward a half, here between {lo:.3f} and {hi:.3f}: Jacob Bernoulli's law of large numbers, "
            "published in 1713. <bookmark mark='b'/> How far off is a run after n flips? About one over the square "
            "root of n, and the shape of that scatter is this chapter's subject."
        ) as vo:
            self.play(Create(ax), FadeIn(xt), FadeIn(yt), FadeIn(xl), FadeIn(yl))
            self.play(Create(runs[0]), run_time=2.0, rate_func=linear)
            vo.wait_until("a")
            self.play(LaggedStart(*[Create(r) for r in runs[1:]], lag_ratio=0.2), FadeIn(hc), run_time=2.5)
            vo.wait_until("b")
            self.play(FadeIn(bnd), FadeIn(bl))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def galton(self):
        d = load("galton")
        rows, n = int(d["rows"]), int(d["n"])
        steps, counts, binom = np.asarray(d["steps"]), np.asarray(d["counts"], float), np.asarray(d["binom"])
        assert counts.sum() == n and d["chi2"] < 30
        x0 = -3.3
        pegs = VGroup(*[Dot(peg_xy(r, k, x0), radius=0.035, color=GREY_B) for r in range(rows) for k in range(r + 1)])
        floor_y = TOP - rows * DY - 0.15
        bin_x = [x0 + (k - rows / 2) * DX for k in range(rows + 1)]
        walls = VGroup(*[Line([x - DX / 2, floor_y, 0], [x - DX / 2, floor_y - 3.0, 0], color=GREY_D, stroke_width=1.5)
                         for x in bin_x + [bin_x[-1] + DX]])
        base = Line([bin_x[0] - DX / 2, floor_y - 3.0, 0], [bin_x[-1] + DX / 2, floor_y - 3.0, 0], color=GREY_C)
        bottom = floor_y - 3.0
        ball_r = 0.055
        # the first 80 balls fall one by one and stack
        stack = [0] * (rows + 1)
        balls, paths = VGroup(), []
        for b in range(len(steps)):
            k = 0
            pts = [np.array([x0, TOP + 0.45, 0])]
            for r in range(rows):
                p = peg_xy(r, k, x0) + UP * 0.09
                pts.append(p)
                k += int(steps[b, r])
            land = np.array([bin_x[k], bottom + ball_r + 2 * ball_r * stack[k], 0])
            stack[k] += 1
            pts.append(np.array([bin_x[k], floor_y, 0]))
            pts.append(land)
            path = VMobject().set_points_smoothly(pts)
            paths.append(path)
            balls.add(Dot(pts[0], radius=ball_r, color=interpolate_color(ManimColor(DATA), ManimColor(C.BITS), k / rows)))
        head = label(r"Twelve rows of pegs: \ left or right, \ fifty-fifty, \ at each", font_size=30)
        head.to_edge(UP, buff=0.4).to_edge(RIGHT, buff=0.5)
        # a thousand balls: the counts as bars
        hscale = 2.8 / counts.max()
        bars = VGroup(*[Rectangle(width=DX * 0.86, height=max(c * hscale, 0.001), stroke_width=0, fill_color=DATA,
                                  fill_opacity=0.75).move_to([bin_x[k], bottom + c * hscale / 2, 0])
                        for k, c in enumerate(counts)])
        nl = label(rf"${n:,}$ balls".replace(",", "{,}"), font_size=30, color=DATA).move_to([x0, bottom - 0.35, 0])
        bdots = VGroup(*[Dot([bin_x[k], bottom + p * n * hscale, 0], radius=0.06, color=C.BITS) for k, p in enumerate(binom)])
        colors = {r"\binom{12}{k}": C.BITS, r"2^{12}": WHITE}
        f1 = cmath(r"P(k)", "=", r"\binom{12}{k}", r"\big/", r"2^{12}", colors=colors, font_size=44).move_to([3.4, 1.6, 0])
        f1n = label(r"$\binom{12}{k}$: \ the number of paths with $k$ right bounces", font_size=24, color=C.BITS)
        f1n.next_to(f1, DOWN, buff=0.25)
        xs = np.linspace(-0.5, rows + 0.5, 160)
        bell = VMobject(color=MODEL, stroke_width=4).set_points_smoothly(
            [np.array([x0 + (x - rows / 2) * DX, bottom + n * hscale * normal_pdf(x, rows / 2, math.sqrt(rows / 4)), 0])
             for x in xs])
        colors2 = {r"\mu": DATA, r"\sigma": MODEL}
        f2 = cmath(r"\varphi(x)", "=", r"\frac{1}{\sigma\sqrt{2\pi}}", r"\,e^{-(x-\mu)^2 / 2\sigma^2}", colors=colors2,
                   font_size=46).move_to([3.4, -0.4, 0])
        f2n = label(r"centre $\mu = 6$, \ width $\sigma = \sqrt{3}$", font_size=28, color=GREY_A).next_to(f2, DOWN, buff=0.3)
        cite_ = cite(r"F.~Galton, \textit{Natural Inheritance} (1889); \ A.~de Moivre (1733)", corner=DR)
        with self.voiceover(
            "Here is the scatter made visible: balls dropped through twelve rows of pegs, bouncing left or right, "
            "fifty-fifty. <bookmark mark='a'/> Where one lands counts its right bounces. <bookmark mark='b'/> Eighty "
            "start to show a shape."
        ) as vo:
            self.play(FadeIn(pegs), Create(walls), Create(base), FadeIn(head))
            vo.wait_until("a")
            for k in range(3):
                self.play(MoveAlongPath(balls[k], paths[k]), run_time=1.6, rate_func=rate_functions.ease_in_quad)
            vo.wait_until("b")
            self.play(LaggedStart(*[MoveAlongPath(balls[k], paths[k], rate_func=rate_functions.ease_in_quad)
                                    for k in range(3, len(balls))], lag_ratio=0.06), run_time=7.0)
        with self.voiceover(
            "A thousand make it unmistakable. <bookmark mark='a'/> Counting paths gives the exact chances: twelve "
            "choose k, out of two to the twelve. <bookmark mark='b'/> The smooth curve hugging them is the bell, the "
            "normal distribution, with a centre mu and a width sigma, here six and the square root of three. De "
            "Moivre found it in 1733, as the limit of exactly these counts."
        ) as vo:
            self.play(FadeOut(balls), LaggedStart(*[GrowFromEdge(b, DOWN) for b in bars], lag_ratio=0.05), FadeIn(nl),
                      run_time=1.6)
            vo.wait_until("a")
            self.play(FadeOut(head), Write(f1), LaggedStart(*[FadeIn(x, scale=0.5) for x in bdots], lag_ratio=0.05))
            self.play(FadeIn(f1n))
            vo.wait_until("b")
            self.play(Create(bell), run_time=1.5)
            self.play(Write(f2), FadeIn(f2n), FadeIn(cite_))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def clt(self):
        d = load("clt")
        ks = [int(k) for k in d["ks"]]
        ax = Axes(x_range=[-4, 4, 1], y_range=[0, 0.62, 0.2], x_length=9.0, y_length=4.2, tips=False,
                  axis_config={"stroke_color": GREY_C, "include_ticks": True, "tick_size": 0.05}).move_to([-0.6, -0.5, 0])
        shapes = []
        for k in ks:
            pmf = np.asarray(d[f"k{k}"])
            sd = math.sqrt(35 * k / 12)
            s = np.arange(k, 6 * k + 1)
            z = (s - 3.5 * k) / sd
            w = 1 / sd
            edges = np.concatenate([z - w / 2, [z[-1] + w / 2]])
            shapes.append(hist_shape(ax, np.clip(edges, -4, 4), pmf * sd, color=DATA, opacity=0.6))
        xs = np.linspace(-4, 4, 200)
        bell = curve(ax, xs, normal_pdf(xs), color=MODEL, stroke_width=4)
        bell_l = label(r"the bell", font_size=28, color=MODEL).next_to(ax.c2p(1.2, normal_pdf(1.2)), UR, buff=0.1)
        kv = Integer(1, font_size=46, color=DATA)
        kl = VGroup(label(r"number of dice:", font_size=34), kv).arrange(RIGHT, buff=0.2).to_corner(UR, buff=0.5)
        xl = label(r"the sum, centred and rescaled", font_size=24, color=GREY_A).next_to(ax, DOWN, buff=0.25)
        colors = {r"S_k": DATA, r"\mathcal{N}(0, 1)": MODEL}
        thm = cmath(r"\frac{S_k - k\mu}{\sigma\sqrt{k}}", r"\;\longrightarrow\;", r"\mathcal{N}(0, 1)", colors=colors,
                    font_size=40).to_corner(UL, buff=0.5)
        thm_n = label(r"the central limit theorem \ (Laplace, 1810): \ whatever the pieces look like", font_size=26,
                      color=GREY_A)
        thm_n.next_to(thm, DOWN, buff=0.2).align_to(thm, LEFT)
        width = label(r"the spread of a sum grows like $\sqrt{k}$", font_size=28, color=C.BITS).to_edge(DOWN, buff=0.3)
        with self.voiceover(
            "Why a bell, and why so often? One die: six flat bars. <bookmark mark='a'/> Two dice: a triangle. Three: "
            "already rounding off. <bookmark mark='b'/> Six, twelve: the bell. <bookmark mark='c'/> That's the "
            "central limit theorem: add many independent pieces, whatever their shape, and the sum is bell-shaped, "
            "<bookmark mark='d'/> with a spread that grows like the square root of their number. Laplace proved it in "
            "1810."
        ) as vo:
            self.play(Create(ax), FadeIn(xl), FadeIn(kl), FadeIn(shapes[0]))
            vo.wait_until("a")
            cur = shapes[0]
            for i, k in enumerate(ks[1:3], start=1):
                self.play(Transform(cur, shapes[i]), ChangeDecimalToValue(kv, k), run_time=1.2)
            self.play(Create(bell), FadeIn(bell_l))
            vo.wait_until("b")
            for i, k in enumerate(ks[3:], start=3):
                self.play(Transform(cur, shapes[i]), ChangeDecimalToValue(kv, k), run_time=1.2)
            vo.wait_until("c")
            self.play(Write(thm), FadeIn(thm_n))
            vo.wait_until("d")
            self.play(FadeIn(width))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def convolution(self):
        """Why: the density of a sum is a convolution, and convolving again and again makes the bell."""
        colors = {r"f": DATA, r"g": MODEL, r"(f * g)(s)": C.BITS}
        rows = [
            cmath(r"P(X + Y = s)", "=", r"\textstyle\sum_x P(X = x)\, P(Y = s - x)", font_size=34),
            cmath(r"(f * g)(s)", "=", r"\int f(x)\, g(s - x)\, dx", colors=colors, font_size=34),
            cmath(r"f_{X_1 + \dots + X_n}", "=", r"f * f * \dots * f", font_size=34),
        ]
        whys = [why(r"every way to split $s$ \\ into $x$ and $s - x$", font_size=22),
                why(r"densities: \ the sum becomes an integral", font_size=22),
                why(r"independent pieces: \ convolve $n$ times", font_size=22)]
        step = ladder(self, rows, whys, keep=3, top=3.2, x=-2.6, buff=0.35, edge=6.8)
        # the picture: f(x) = e^{-x} and its flipped copy g(s - x) sliding, the overlap's area traced as (f * f)(s)
        ax = Axes(x_range=[-0.5, 6.5, 1], y_range=[0, 1.1, 0.5], x_length=6.0, y_length=2.4, tips=False,
                  axis_config={"stroke_color": GREY_C, "include_ticks": False}).move_to([-3.4, -2.0, 0])
        xs = np.linspace(0, 6.5, 200)
        f_c = curve(ax, xs, np.exp(-xs), color=DATA, stroke_width=3)
        s = ValueTracker(0.6)

        def flipped():
            sv = s.get_value()
            xx = np.linspace(-0.5, sv, 120)
            return curve(ax, xx, np.exp(-(sv - xx)), color=MODEL, stroke_width=3)

        def overlap():
            sv = s.get_value()
            xx = np.linspace(0, max(sv, 1e-3), 60)
            pts = [ax.c2p(x, math.exp(-x) * math.exp(-(sv - x))) for x in xx]
            return Polygon(ax.c2p(0, 0), *pts, ax.c2p(max(sv, 1e-3), 0), stroke_width=0, fill_color=C.BITS,
                           fill_opacity=0.55)

        g_c, ov = always_redraw(flipped), always_redraw(overlap)
        bx = Axes(x_range=[0, 6.5, 1], y_range=[0, 0.45, 0.2], x_length=4.8, y_length=2.4, tips=False,
                  axis_config={"stroke_color": GREY_C, "include_ticks": False}).move_to([3.6, -2.0, 0])
        trace = always_redraw(lambda: curve(bx, np.linspace(0, s.get_value(), 80),
                                            np.linspace(0, s.get_value(), 80) * np.exp(-np.linspace(0, s.get_value(), 80)),
                                            color=C.BITS, stroke_width=4))
        lab = VGroup(label(r"$f(x) = e^{-x}$", font_size=22, color=DATA),
                     label(r"$f(s - x)$, \ flipped and slid to $s$", font_size=22, color=MODEL),
                     label(r"overlap $f(x)\,f(s-x)$", font_size=22, color=C.BITS)).arrange(DOWN, aligned_edge=LEFT, buff=0.08)
        lab.next_to(ax, UP, buff=0.12).align_to(ax, LEFT)
        bl = label(r"its area, \ for each $s$: \ $(f * f)(s) = s\,e^{-s}$", font_size=22, color=C.BITS)
        bl.next_to(bx, UP, buff=0.12)
        with self.voiceover(
            "Why? Two dice add up to s in every way of splitting s: x on one die, s minus x on the other. <bookmark "
            "mark='a'/> For densities the sum becomes an integral, a convolution. <bookmark mark='b'/> Picture it "
            "with a lopsided piece, the exponential. Flip a copy, slide it to s, multiply: the area of the overlap is "
            "the density of the sum at s. <bookmark mark='c'/> Slide s along, and the area traces out the density of "
            "two pieces. <bookmark mark='d'/> n pieces take n minus one convolutions."
        ) as vo:
            step(0)
            vo.wait_until("a")
            step(1)
            vo.wait_until("b")
            self.play(Create(ax), Create(f_c), FadeIn(lab[0]))
            self.play(Create(g_c), FadeIn(ov), FadeIn(lab[1:]))
            vo.wait_until("c")
            self.play(Create(bx), FadeIn(bl))
            self.add(trace)
            self.play(s.animate.set_value(6.4), run_time=4.0, rate_func=linear)
            vo.wait_until("d")
            step(2)
        for m in (g_c, ov, trace):
            m.clear_updaters()
        self.wait(0.3)
        self.clear_scene()
        # repeated convolution of the exponential, standardized: the bell appears
        d = load("conv")
        zg, dens, show = np.asarray(d["zg"]), np.asarray(d["exp_dens"]), [int(v) for v in d["show"]]
        ax2 = Axes(x_range=[-4, 4, 1], y_range=[0, 1.0, 0.25], x_length=9.0, y_length=4.4, tips=False,
                   axis_config={"stroke_color": GREY_C, "include_ticks": True, "tick_size": 0.05}).move_to([-0.8, -0.5, 0])
        shapes = [curve(ax2, zg, np.minimum(dd, 1.0), color=DATA, stroke_width=4) for dd in dens]
        bell = curve(ax2, zg, normal_pdf(zg), color=MODEL, stroke_width=3).set_stroke(opacity=0.8)
        bl2 = label(r"the bell", font_size=26, color=MODEL).next_to(ax2.c2p(1.3, normal_pdf(1.3)), UR, buff=0.1)
        nv = Integer(1, font_size=44, color=DATA)
        nl = VGroup(label(r"exponentials added:", font_size=30), nv).arrange(RIGHT, buff=0.2).to_corner(UR, buff=0.45)
        xl = label(r"the sum, \ centred and rescaled", font_size=24, color=GREY_A).next_to(ax2, DOWN, buff=0.25)
        tag = note(r"computed by repeated convolution on a grid; \ checked against the exact answer").to_corner(DL, buff=0.25)
        with self.voiceover(
            "So convolve again and again. One exponential, all on one side. <bookmark mark='a'/> Two, three, five: "
            "each convolution smooths and spreads it. <bookmark mark='b'/> Ten, thirty: the lopsidedness fades, "
            "and what is left is the bell. Convolution is an averaging, and the only shape that averaging leaves "
            "unchanged, up to scale, is the bell."
        ) as vo:
            self.play(Create(ax2), FadeIn(xl), FadeIn(nl), Create(shapes[0]), FadeIn(tag), Create(bell), FadeIn(bl2))
            cur = shapes[0]
            vo.wait_until("a")
            for i in (1, 2, 3):
                self.play(Transform(cur, shapes[i]), ChangeDecimalToValue(nv, show[i]), run_time=1.2)
            vo.wait_until("b")
            for i in (4, 5):
                self.play(Transform(cur, shapes[i]), ChangeDecimalToValue(nv, show[i]), run_time=1.4)
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def rate(self):
        d = load("conv")
        ns = np.asarray(d["ns"], float)
        ed, ud, eb = np.asarray(d["exp_dist"]), np.asarray(d["uni_dist"]), np.asarray(d["exp_bound"])
        es, us = float(d["exp_slope"]), float(d["uni_slope"])
        ax = Axes(x_range=[0, 2, 1], y_range=[-4, 0.5, 1], x_length=6.6, y_length=4.6, tips=False,
                  axis_config={"stroke_color": GREY_C, "include_ticks": True, "tick_size": 0.05}).move_to([-3.2, -0.5, 0])
        xt = VGroup(*[MathTex(t, font_size=22, color=GREY_B).next_to(ax.c2p(v, -4), DOWN, buff=0.12)
                      for t, v in (("1", 0), ("10", 1), ("100", 2))])
        yt = VGroup(*[MathTex(t, font_size=22, color=GREY_B).next_to(ax.c2p(0, v), LEFT, buff=0.12)
                      for t, v in (("1", 0), ("10^{-2}", -2), ("10^{-4}", -4))])
        xl = label(r"pieces added, $n$", font_size=24, color=GREY_A).next_to(xt, DOWN, buff=0.12)
        yl = label(r"largest gap from the bell's CDF", font_size=24, color=GREY_A).next_to(ax, UP, buff=0.15).align_to(ax, LEFT)
        lx = np.log10(ns)

        def series(v, col):
            return VGroup(curve(ax, lx, np.log10(v), color=col, stroke_width=3.5),
                          *[Dot(ax.c2p(a, b), radius=0.05, color=col) for a, b in zip(lx, np.log10(v))])

        s_e, s_u = series(ed, DATA), series(ud, C.INTERVAL)
        s_b = DashedVMobject(curve(ax, lx, np.log10(eb), color=WHITE, stroke_width=2.5), num_dashes=30)
        l_e = label(rf"exponential: \ slope ${es:.2f}$", font_size=22, color=DATA).next_to(ax.c2p(2, math.log10(ed[-1])), RIGHT, buff=0.1)
        l_u = label(rf"uniform: \ slope ${us:.2f}$", font_size=22, color=C.INTERVAL).next_to(ax.c2p(2, math.log10(ud[-1])), RIGHT, buff=0.1)
        l_b = label(r"Berry--Esseen bound", font_size=22, color=WHITE).next_to(ax.c2p(2, math.log10(eb[-1])), RIGHT, buff=0.1)
        thm = theorem_card(r"Berry--Esseen", MathTex(r"\sup_x \big|F_n(x) - \Phi(x)\big| \;\le\; "
                                                     r"\frac{C\,\rho}{\sigma^3 \sqrt{n}}, \qquad C \le 0.4748",
                                                     font_size=30),
                           who=r"Berry (1941), \ Esseen (1942); \ constant: \ Shevtsova (2011)", width=6.2)
        thm.to_corner(UR, buff=0.3)
        rn = label(r"$\rho = \mathbb{E}|X - \mu|^3$: \ how lopsided and heavy-tailed a piece is", font_size=22,
                   color=GREY_A).next_to(thm, DOWN, buff=0.2).align_to(thm, LEFT)
        k64 = int(np.argmin(np.abs(ns - 64)))
        sym = (f"The uniform pieces, symmetric, close the gap much faster: slope {us:.1f}, like one over n, because "
               "with no skew the first correction to the bell cancels.") if us < es - 0.25 else (
            f"The uniform pieces close the gap at about the same rate, slope {us:.1f}.")
        with self.voiceover(
            "How fast does the bell arrive? Measure the largest gap between the sum's cumulative distribution and "
            f"the bell's. <bookmark mark='a'/> For the exponential it falls on a line of slope {es:.2f}: the gap "
            f"shrinks like one over the square root of n, {ed[k64]:.3f} after sixty-four pieces. "
            "<bookmark mark='b'/> That is the Berry-Esseen theorem: the gap is at most a constant times the third "
            "absolute moment over the cube of the spread, over the square root of n, and the measured gap sits "
            f"under it. <bookmark mark='c'/> {sym}"
        ) as vo:
            self.play(Create(ax), FadeIn(xt), FadeIn(yt), FadeIn(xl), FadeIn(yl))
            vo.wait_until("a")
            self.play(Create(s_e), FadeIn(l_e), run_time=1.5)
            vo.wait_until("b")
            self.play(FadeIn(thm), FadeIn(rn))
            self.play(Create(s_b), FadeIn(l_b))
            vo.wait_until("c")
            self.play(Create(s_u), FadeIn(l_u), run_time=1.5)
        self.wait(0.3)
        self.clear_scene()
