from __future__ import annotations

import math

import numpy as np

from explainer.analysis import *  # noqa: F403
from videos.analysis7.common import load, plain_axes, polyline, square_axes


def tour_tag():
    return note(r"tour, no proof").to_corner(UR, buff=0.3)


class Harmonic(VoiceoverScene):
    def construct(self):
        self.card()
        self.poisson()
        self.kernel()

    # ------------------------------------------------------------------
    def card(self):
        card = chapter_card(10, r"A tour: harmonic functions", r"What is the temperature inside a disk?", lit=(), part=7)
        with self.voiceover("Chapter ten begins a short tour of the rest of the complex half of Rudin's book, with "
                            "results stated rather than proved. First, harmonic functions."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))

    # ------------------------------------------------------------------
    def poisson(self):
        d = load("poisson")
        th, g, rs, U, lap_pt, u0, gmean = d["th"], d["g"], d["rs"], d["U"], d["lap_pt"], float(d["u0"]), float(d["gmean"])
        S = 4.8
        ax = square_axes([-1.05, 1.05, 1], [-1.05, 1.05, 1], S / 2.1).move_to([-3.6, -0.6, 0])
        ax.set_opacity(0)
        px = 420
        x = np.linspace(-1.05, 1.05, px)
        X, Y = np.meshgrid(x, x[::-1])
        R, T = np.hypot(X, Y), np.mod(np.arctan2(Y, X), 2 * np.pi)
        ri = np.clip(R / rs[-1] * (len(rs) - 1), 0, len(rs) - 1)
        ti = T / (2 * np.pi) * len(th)
        i0, j0 = np.floor(ri).astype(int), np.floor(ti).astype(int) % len(th)
        i1, j1 = np.minimum(i0 + 1, len(rs) - 1), (j0 + 1) % len(th)
        fr, ft = ri - i0, ti - np.floor(ti)
        Uv = ((1 - fr) * (1 - ft) * U[i0, j0] + fr * (1 - ft) * U[i1, j0] + (1 - fr) * ft * U[i0, j1] +
              fr * ft * U[i1, j1])
        vmin, vmax = -1.4, 1.7
        t = np.clip((Uv - vmin) / (vmax - vmin), 0, 1)[..., None]
        c_lo, c_mid, c_hi = (np.array(ManimColor(c).to_rgb()) for c in (C.SEQ, BACKGROUND, C.MEASURE))
        mid = (0 - vmin) / (vmax - vmin)
        rgb = np.where(t < mid, c_lo + (t / mid) * (c_mid - c_lo), c_mid + ((t - mid) / (1 - mid)) * (c_hi - c_mid))
        alpha = (R <= 1).astype(float)[..., None]
        im = ImageMobject((np.concatenate([rgb, alpha], -1) * 255).astype(np.uint8))
        im.set_resampling_algorithm(RESAMPLING_ALGORITHMS["bilinear"])
        im.stretch_to_fit_width(S).stretch_to_fit_height(S).move_to(ax.c2p(0, 0))
        ring = VGroup()
        for k in range(len(th)):
            a0, a1 = th[k], th[(k + 1) % len(th)] if k + 1 < len(th) else 2 * np.pi
            tv = np.clip((g[k] - vmin) / (vmax - vmin), 0, 1)
            col = c_lo + (tv / mid) * (c_mid - c_lo) if tv < mid else c_mid + ((tv - mid) / (1 - mid)) * (c_hi - c_mid)
            ring.add(AnnularSector(inner_radius=S / 2.1 * 1.0, outer_radius=S / 2.1 * 1.09, angle=a1 - a0, start_angle=a0,
                                   fill_color=ManimColor(tuple(float(v) for v in col)), fill_opacity=1, stroke_width=0)
                     .move_arc_center_to(ax.c2p(0, 0)))
        bx = plain_axes([0, 2 * np.pi, np.pi / 2], [-1.5, 1.8, 1], 4.6, 2.4).move_to([3.3, 1.2, 0])
        gg = polyline(bx, th, g, color=C.MEASURE, stroke_width=3)
        b_l = MathTex(r"g(\theta) = \tanh(4\cos 3\theta) + 0.4\sin\theta + 0.3", font_size=24, color=C.MEASURE).next_to(
            bx, UP, buff=0.1)
        rows = VGroup(
            label(r"\textbf{RCA 11.9} \ the Dirichlet problem: \ given $g$ on the circle,", font_size=22),
            MathTex(r"u(re^{i\theta}) = \frac{1}{2\pi}\int P_r(\theta - t)\, g(t)\,dt", font_size=28, color=C.EPS),
            label(r"is harmonic in the disk and equals $g$ on the edge", font_size=22),
            MathTex(rf"\text{{12 random points: }} |\Delta u| < {sci(float(lap_pt.max()) * 1.5, 0)}", font_size=24,
                    color=GREY_A),
            MathTex(rf"u(0) = {u0:.4f} = \text{{the average of }} g = {gmean:.4f}", font_size=26, color=C.EPS),
            label(r"(the mean value property)", font_size=22, color=GREY_A),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.12).move_to([3.3, -1.75, 0])
        for r_ in rows:
            if r_.width > 6.4:
                r_.width = 6.4
        assert lap_pt.max() < 1e-4 and abs(u0 - gmean) < 1e-12
        with self.voiceover(
            "<bookmark mark='a'/> The real part of a holomorphic function is harmonic: its Laplacian is zero. Think "
            "of it as a steady temperature. <bookmark mark='b'/> Fix the temperature on the boundary circle, here a "
            "pattern with three warm and three cool arcs. <bookmark mark='c'/> Then there's exactly one harmonic "
            "function inside with those boundary values, given by Poisson's integral. Its Laplacian, checked at "
            "random points, is zero to within ten to the minus four, the error of the finite difference. "
            "<bookmark mark='d'/> At the center, the temperature is the average around the edge: 0.3. That's the "
            "mean value property, the harmonic version of Cauchy's formula."
        ) as vo:
            self.add(tour_tag())
            vo.wait_until("a")
            vo.wait_until("b")
            self.play(FadeIn(ring), Create(bx), Create(gg), FadeIn(b_l))
            vo.wait_until("c")
            self.play(FadeIn(im), FadeIn(rows[:3]), run_time=2.0)
            self.play(FadeIn(rows[3]))
            vo.wait_until("d")
            self.play(FadeIn(rows[4:]))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def kernel(self):
        ax = plain_axes([-math.pi, math.pi, math.pi / 2], [0, 40, 10], 6.0, 3.6, numbers=False).move_to([-3.0, -0.6, 0])
        tk = VGroup(*[MathTex(s, font_size=20).next_to(ax.c2p(v, 0), DOWN, buff=0.1)
                      for s, v in ((r"-\pi", -math.pi), ("0", 0), (r"\pi", math.pi))])
        t = np.linspace(-math.pi, math.pi, 2001)
        cols = [C.SEQ, C.APPROX, C.EPS]
        curves = []
        for r, c in zip((0.5, 0.8, 0.95), cols):
            P = (1 - r * r) / (1 - 2 * r * np.cos(t) + r * r)
            mass = float(np.sum((P[1:] + P[:-1]) / 2 * np.diff(t)) / (2 * math.pi))
            assert abs(mass - 1) < 1e-6 and P.min() > 0
            curves.append(VGroup(polyline(ax, t, P, color=c, stroke_width=3),
                                 MathTex(rf"r = {r}", font_size=24, color=c).next_to(ax.c2p(0.4, min(P.max(), 38)), RIGHT,
                                                                                    buff=0.1)))
        rows = VGroup(
            MathTex(r"P_r(t) = \frac{1 - r^2}{1 - 2r\cos t + r^2}", font_size=32),
            label(r"positive, \ average $1$, \ narrowing as $r \to 1$:", font_size=24),
            label(r"the same bump as Landau, \ Fej\'er, \ and Rudin's $(1 + \cos t)^k$", font_size=24, color=C.EPS),
            label(r"Kakutani (1944): \ $u(x)$ is the average of $g$ at the point", font_size=22, color=GREY_A),
            label(r"where a random walk from $x$ first hits the circle", font_size=22, color=GREY_A),
            label(r"(the stochastic video's walkers)", font_size=22, color=GREY_A),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.16).move_to([3.7, -0.5, 0])
        for r_ in rows:
            if r_.width > 5.6:
                r_.width = 5.6
        head = label(r"Poisson's kernel: \ the bump, once more", font_size=34).to_edge(UP, buff=0.3)
        with self.voiceover(
            "<bookmark mark='a'/> Poisson's kernel is an old friend: positive, average one, and narrowing as r "
            "approaches one, the same bump as the Landau and Fejér kernels. That's why the solution takes the right "
            "boundary values. <bookmark mark='b'/> And there's a probabilistic reading, due to Kakutani: the "
            "temperature at a point is the average boundary temperature where a random walk started there first "
            "hits the circle."
        ) as vo:
            self.add(tour_tag())
            self.play(FadeIn(head), Create(ax), FadeIn(tk), FadeIn(rows[0]))
            vo.wait_until("a")
            for c in curves:
                self.play(Create(c[0]), FadeIn(c[1]), run_time=1.0)
            self.play(FadeIn(rows[1:3]))
            vo.wait_until("b")
            self.play(FadeIn(rows[3:]))
        self.wait(0.4)
        self.clear_scene()
