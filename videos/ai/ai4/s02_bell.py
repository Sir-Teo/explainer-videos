from __future__ import annotations

import math

import numpy as np

from explainer.ai import *  # noqa: F403
from videos.ai.ai4.common import DATA, MODEL, curve, hist_shape, load, normal_pdf

DX, DY = 0.36, 0.27  # peg spacing
TOP = 3.0  # height of the first peg


def peg_xy(r, k, x0):
    """Peg k of row r (k = number of right bounces so far)."""
    return np.array([x0 + (k - r / 2) * DX, TOP - r * DY, 0])


class Bell(VoiceoverScene):
    def construct(self):
        self.card()
        self.galton()
        self.clt()

    # ------------------------------------------------------------------
    def card(self):
        card = chapter_card(1, r"The bell curve", r"Why does the same shape turn up everywhere?", part=4)
        with self.voiceover("Chapter one. The bell curve."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))

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
            "Drop a ball through twelve rows of pegs. At every peg it bounces left or right, fifty-fifty. "
            "<bookmark mark='a'/> Where it lands just counts its right bounces. <bookmark mark='b'/> One ball tells "
            "you nothing. Eighty start to show a shape."
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
            "choose k, the number of paths with k right bounces, out of two to the twelve paths in all. "
            "<bookmark mark='b'/> And the smooth curve hugging them is the bell: the normal distribution, with a "
            "centre mu and a width sigma. Here the centre is six, and the width is the square root of three. Galton "
            "built this board in the 1870s to show it, but de Moivre had found the curve in 1733."
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
        thm_n = label(r"the central limit theorem: \ whatever the pieces look like", font_size=26, color=GREY_A)
        thm_n.next_to(thm, DOWN, buff=0.2).align_to(thm, LEFT)
        width = label(r"the spread of a sum grows like $\sqrt{k}$", font_size=28, color=C.BITS).to_edge(DOWN, buff=0.3)
        with self.voiceover(
            "But why a bell, and why so often? Take one die: six flat bars. <bookmark mark='a'/> Add two dice, and "
            "you get a triangle. Three, and it's already rounding off. <bookmark mark='b'/> Six. Twelve. The bell "
            "again. <bookmark mark='c'/> That's the central limit theorem. Add up many independent random pieces, and "
            "whatever shape the pieces have, the sum takes the shape of the bell, <bookmark mark='d'/> with a spread "
            "that grows like the square root of how many you add. Errors, heights, noise: anything built from many "
            "small independent nudges comes out bell-shaped."
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
