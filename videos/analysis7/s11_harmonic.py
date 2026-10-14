from __future__ import annotations

import math

import numpy as np

from explainer.analysis import *  # noqa: F403
from videos.analysis7.common import load, plain_axes, polyline, square_axes


def tour_tag():
    t = note(r"tour, no proof").to_edge(UP, buff=0.35)
    return t.set_x(6.6 - t.width / 2)  # right edge on the series' 6.6 margin


def temp_colors(v, vmin=-1.4, vmax=1.7):
    """Temperature -> RGB: C.SEQ (cold) through the background (0) to C.MEASURE (warm)."""
    t = np.clip((v - vmin) / (vmax - vmin), 0, 1)[..., None]
    c_lo, c_mid, c_hi = (np.array(ManimColor(c).to_rgb()) for c in (C.SEQ, BACKGROUND, C.MEASURE))
    mid = (0 - vmin) / (vmax - vmin)
    return np.where(t < mid, c_lo + (t / mid) * (c_mid - c_lo), c_mid + ((t - mid) / (1 - mid)) * (c_hi - c_mid))


def g_of(T, th, g):
    """The boundary data, interpolated periodically at the angles T."""
    return np.interp(np.mod(T, 2 * np.pi), np.append(th, 2 * np.pi), np.append(g, g[0]))


def temp_image(S, center, th, g, U=None, rs=None, ring=(1.0, 1.09), px=440, ss=2):
    """The ring 1 < |z| <= 1.09 coloured by g(theta) and (if U is given) the disk |z| <= 1 coloured by the Poisson
    integral U(r, theta), in ONE image: one alpha edge, no seams between them. Pixels average ss x ss samples."""
    half = ring[1] + 0.01
    n = px * ss
    x = -half + (np.arange(n) + 0.5) / n * 2 * half
    X, Y = np.meshgrid(x, x[::-1])
    R, T = np.hypot(X, Y), np.mod(np.arctan2(Y, X), 2 * np.pi)
    val = g_of(T, th, g)
    a = ((R > ring[0]) & (R <= ring[1])).astype(float)
    if U is not None:
        ri = np.clip(R / rs[-1] * (len(rs) - 1), 0, len(rs) - 1)
        ti = T / (2 * np.pi) * len(th)
        i0, j0 = np.floor(ri).astype(int), np.floor(ti).astype(int) % len(th)
        i1, j1 = np.minimum(i0 + 1, len(rs) - 1), (j0 + 1) % len(th)
        fr, ft = ri - i0, ti - np.floor(ti)
        Uv = ((1 - fr) * (1 - ft) * U[i0, j0] + fr * (1 - ft) * U[i1, j0] + (1 - fr) * ft * U[i0, j1] +
              fr * ft * U[i1, j1])
        inside = R <= ring[0]
        val = np.where(inside, Uv, val)
        a = np.maximum(a, inside.astype(float))
    rgb = temp_colors(val) * a[..., None]
    A = a.reshape(px, ss, px, ss).mean(axis=(1, 3))
    RGB = rgb.reshape(px, ss, px, ss, 3).sum(axis=(1, 3)) / np.maximum(a.reshape(px, ss, px, ss).sum(axis=(1, 3)),
                                                                        1e-12)[..., None]
    im = ImageMobject((np.clip(np.concatenate([RGB, A[..., None]], -1), 0, 1) * 255).astype(np.uint8))
    im.set_resampling_algorithm(RESAMPLING_ALGORITHMS["bilinear"])
    side = S / 2.1 * 2 * half
    return im.stretch_to_fit_width(side).stretch_to_fit_height(side).move_to(center)


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
        ctr = ax.c2p(0, 0)
        im = temp_image(S, ctr, th, g, U=U, rs=rs)  # the disk and its boundary ring, one image
        ring = temp_image(S, ctr, th, g)  # the ring alone, identical to the full image's ring
        px = 420
        x = np.linspace(-1.05, 1.05, px)
        X, Y = np.meshgrid(x, x[::-1])
        R = np.hypot(X, Y)
        alpha = (R <= 1).astype(float)[..., None]
        # first, the simplest harmonic function: u = Re z^2 = x^2 - y^2 (saddle: warm along x, cool along y)
        Ua = X * X - Y * Y
        imA = ImageMobject((np.concatenate([temp_colors(Ua), alpha], -1) * 255).astype(np.uint8))
        imA.set_resampling_algorithm(RESAMPLING_ALGORITHMS["bilinear"])
        imA.stretch_to_fit_width(S).stretch_to_fit_height(S).move_to(ctr)
        lapA = ((Ua[1:-1, 2:] + Ua[1:-1, :-2] + Ua[2:, 1:-1] + Ua[:-2, 1:-1] - 4 * Ua[1:-1, 1:-1]) / (x[1] - x[0]) ** 2)
        assert np.abs(lapA).max() < 1e-6  # x^2 - y^2 is exactly harmonic (the 5-point stencil is exact)
        assert np.allclose(U[-1], g, atol=1e-8)  # the disk's edge and the ring carry the same values: no seam
        labA = VGroup(MathTex(r"u = \mathrm{Re}\, z^2 = x^2 - y^2", font_size=32, color=C.MEASURE),
                      MathTex(r"\Delta u = u_{xx} + u_{yy} = 2 - 2 = 0", font_size=30, color=C.EPS),
                      label(r"warm along the real axis, \ cool along the imaginary one", font_size=22, color=GREY_A)
                      ).arrange(DOWN, aligned_edge=LEFT, buff=0.15).move_to([3.3, 1.0, 0])
        u_ = S / 2.1
        t0 = VGroup(Line(ctr + RIGHT * 0.97 * u_, ctr + RIGHT * 1.13 * u_, color=WHITE, stroke_width=2.5),
                    MathTex(r"\theta = 0", font_size=22).next_to(ctr + RIGHT * 1.13 * u_, RIGHT, buff=0.08))
        bx = plain_axes([0, 2 * np.pi, np.pi / 2], [-1.5, 1.8, 1], 4.6, 2.4).move_to([3.3, 0.95, 0])
        gg = polyline(bx, th, g, color=C.MEASURE, stroke_width=3)
        assert g.min() > -1.5 and g.max() < 1.8
        b_l = MathTex(r"g(\theta) = \tanh(4\cos 3\theta) + 0.4\sin\theta + 0.3", font_size=24, color=C.MEASURE).next_to(
            bx, UP, buff=0.1)
        bt = VGroup(*[MathTex(s_, font_size=18).next_to(bx.c2p(v, -1.5), DOWN, buff=0.08)  # below the plot, clear of g
                      for s_, v in (("0", 0), (r"\pi", np.pi), (r"2\pi", 2 * np.pi))],
                    MathTex(r"\theta", font_size=20, color=GREY_B).next_to(bx.c2p(2 * np.pi, 0), RIGHT, buff=0.1),
                    *[MathTex(s_, font_size=18).next_to(bx.c2p(0, v), LEFT, buff=0.1) for s_, v in (("1", 1), ("-1", -1))])
        rows = VGroup(
            label(r"\textbf{RCA 11.9} \ the Dirichlet problem: \ given $g$ on the circle,", font_size=22),
            MathTex(r"u(re^{i\theta}) = \frac{1}{2\pi}\int P_r(\theta - t)\, g(t)\,dt", font_size=28, color=C.EPS),
            label(r"is harmonic in the disk and equals $g$ on the edge", font_size=22),
            MathTex(rf"\text{{12 random points: }} |\Delta u| < {sci(float(lap_pt.max()) * 1.5, 0)}", font_size=24,
                    color=GREY_A),
            MathTex(rf"u(0) = {u0:.4f} = \text{{the average of }} g = {gmean:.4f}", font_size=26, color=C.EPS),
            label(r"(the mean value property)", font_size=22, color=GREY_A),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.12)
        rows.align_to(np.array([max(0.3, 6.55 - rows.width), 0, 0]), LEFT).set_y(-2.08)
        assert lap_pt.max() < 1e-4 and abs(u0 - gmean) < 1e-12
        head = label(r"Harmonic functions: \ steady temperatures in the disk", font_size=34).to_edge(UP, buff=0.3)
        tag = tour_tag()
        assert head.get_right()[0] < tag.get_left()[0] - 0.2 or head.get_bottom()[1] > tag.get_top()[1]
        assert rows.get_right()[0] <= 6.6 and rows.get_bottom()[1] > -3.65 and rows.get_top()[1] < bt.get_bottom()[1] - 0.1
        assert t0.get_right()[0] < rows.get_left()[0] - 0.1 and b_l.get_top()[1] < head.get_bottom()[1] - 0.1
        with self.voiceover(
            "<bookmark mark='a'/> The real part of a holomorphic function is harmonic: its Laplacian is zero. Think "
            "of it as a steady temperature. <bookmark mark='b'/> Fix the temperature on the boundary circle, here a "
            "pattern with three warm and three cool arcs. <bookmark mark='c'/> Then there's exactly one harmonic "
            "function inside with those boundary values, given by Poisson's integral. Its Laplacian, checked at "
            "random points, is zero to within ten to the minus four, the error of the finite difference. "
            "<bookmark mark='d'/> At the center, the temperature is the average around the edge: 0.3. That's the "
            "mean value property, the harmonic version of Cauchy's formula."
        ) as vo:
            self.add(tag)
            vo.wait_until("a")
            self.play(FadeIn(head), FadeIn(imA), FadeIn(labA[0]), run_time=1.2)
            self.play(FadeIn(labA[1:]))
            vo.wait_until("b")
            self.play(FadeOut(imA), FadeOut(labA), FadeIn(ring), FadeIn(t0), Create(bx), Create(gg), FadeIn(b_l),
                      FadeIn(bt))
            vo.wait_until("c")
            self.play(FadeIn(im), FadeIn(rows[:3]), run_time=2.0)
            self.remove(ring)
            self.play(FadeIn(rows[3]))
            vo.wait_until("d")
            self.play(FadeIn(rows[4:]))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def kernel(self):
        ax = plain_axes([-math.pi, math.pi, math.pi / 2], [0, 40, 10], 5.6, 3.0, numbers=False).move_to([-3.5, 0.95, 0])
        tk = VGroup(*[MathTex(s, font_size=20).next_to(ax.c2p(v, 0), DOWN, buff=0.1)
                      for s, v in ((r"-\pi", -math.pi), ("0", 0), (r"\pi", math.pi))])
        # heights on the left edge (the y-axis runs up the middle, through the bumps' peaks)
        yk = VGroup(*[VGroup(Line(ax.c2p(-math.pi, v), ax.c2p(-math.pi, v) + RIGHT * 0.1, color=GREY_C, stroke_width=2),
                             MathTex(str(v), font_size=18).next_to(ax.c2p(-math.pi, v), LEFT, buff=0.1))
                      for v in (10, 20, 30, 40)])
        t = np.linspace(-math.pi, math.pi, 2001)
        cols = [C.SEQ, C.APPROX, C.EPS]
        curves, key = [], VGroup()
        for i_, (r, c) in enumerate(zip((0.5, 0.8, 0.95), cols)):
            P = (1 - r * r) / (1 - 2 * r * np.cos(t) + r * r)
            mass = float(np.sum((P[1:] + P[:-1]) / 2 * np.diff(t)) / (2 * math.pi))
            assert abs(mass - 1) < 1e-6 and P.min() > 0 and abs(P.max() - (1 + r) / (1 - r)) < 1e-9 and P.max() < 40
            curves.append(polyline(ax, t, P, color=c, stroke_width=3))
            y = 36 - 6 * i_
            key.add(VGroup(Line(ax.c2p(1.35, y), ax.c2p(1.85, y), color=c, stroke_width=3),
                           MathTex(rf"r = {r}", font_size=22, color=c).next_to(ax.c2p(1.85, y), RIGHT, buff=0.1)))
            assert P[t > 1.2].max() < y - 4  # the key sits where the curves have already fallen to the floor
        rows = VGroup(
            MathTex(r"P_r(t) = \frac{1 - r^2}{1 - 2r\cos t + r^2}", font_size=32),
            label(r"positive, \ average $1$, \ narrowing as $r \to 1$:", font_size=24),
            label(r"the same bump as Landau, \ Fej\'er,", font_size=24, color=C.EPS),
            label(r"and Rudin's $(1 + \cos t)^k$", font_size=24, color=C.EPS),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.16)
        rows.align_to(np.array([ax.get_right()[0] + 0.6, 0, 0]), LEFT).set_y(1.2)
        # Kakutani, computed: random walks (step 0.03) from x0 until they leave the disk; the average of g at the
        # exit points against Poisson's integral u(x0)
        d = load("poisson")
        th, g = d["th"], d["g"]
        x0 = 0.3 + 0.2j
        tq = np.linspace(0, 2 * np.pi, 4097)[:-1]
        u_x0 = float(np.mean((1 - abs(x0) ** 2) / np.abs(np.exp(1j * tq) - x0) ** 2 * g_of(tq, th, g)))
        rng = np.random.default_rng(11)
        N, h = 2000, 0.03
        zw, alive, path = np.full(N, x0), np.ones(N, bool), [x0]
        while alive.any():
            zw = np.where(alive, zw + h * np.exp(1j * rng.uniform(0, 2 * np.pi, N)), zw)
            if alive[0]:
                path.append(zw[0])
            alive &= np.abs(zw) < 1
        ge = g_of(np.angle(zw), th, g)
        mc, se = float(ge.mean()), float(ge.std() / math.sqrt(N))
        assert abs(mc - u_x0) < 3 * se and abs(path[-1]) >= 1 and np.all(np.abs(path[:-1]) < 1)
        Sd = 2.0
        wctr = np.array([-5.05, -2.3, 0])
        disk = VGroup(Circle(radius=Sd / 2.1, color=GREY_C, stroke_width=1.5).move_to(wctr))
        ringw = temp_image(Sd, wctr, th, g, px=300)
        uw = Sd / 2.1
        walk = VMobject(stroke_color=GREY_A, stroke_width=1.2).set_points_as_corners(
            [wctr + uw * np.array([z.real, z.imag, 0]) for z in path])
        start = VGroup(Dot(wctr + uw * np.array([x0.real, x0.imag, 0]), radius=0.06, color=WHITE),
                       MathTex(r"x", font_size=24).next_to(wctr + uw * np.array([x0.real, x0.imag, 0]), UL, buff=0.06))
        ze = path[-1] / abs(path[-1])
        col_e = ManimColor(tuple(float(v) for v in temp_colors(np.array(g_of(np.angle(ze), th, g)))))
        end = Dot(wctr + uw * np.array([ze.real, ze.imag, 0]), radius=0.09, color=col_e, stroke_color=WHITE,
                  stroke_width=2)
        kak = VGroup(
            label(r"Kakutani (1944): \ $u(x)$ is the average of $g$ at the point", font_size=22, color=GREY_A),
            label(r"where a random walk from $x$ first hits the circle", font_size=22, color=GREY_A),
            label(r"(the stochastic video's walkers)", font_size=22, color=GREY_A),
            MathTex(rf"\text{{{N} walks: average of }} g = {mc:.3f}, \quad u(x) = {u_x0:.3f}", font_size=24, color=C.EPS),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.14)
        kak.next_to(wctr + RIGHT * 1.3, RIGHT, buff=0).set_y(wctr[1])
        head = label(r"Poisson's kernel: \ the bump, once more", font_size=34).to_edge(UP, buff=0.3)
        assert rows.get_right()[0] <= 6.6 and kak.get_right()[0] <= 6.6 and ringw.get_bottom()[1] > -3.65
        assert ringw.get_top()[1] < tk.get_bottom()[1] - 0.05 and yk.get_left()[0] > -6.7
        with self.voiceover(
            "<bookmark mark='a'/> Poisson's kernel is an old friend: positive, average one, and narrowing as r "
            "approaches one, the same bump as the Landau and Fejér kernels. That's why the solution takes the right "
            "boundary values. <bookmark mark='b'/> And there's a probabilistic reading, due to Kakutani: the "
            "temperature at a point is the average boundary temperature where a random walk started there first "
            "hits the circle."
        ) as vo:
            self.add(tour_tag())
            self.play(FadeIn(head), Create(ax), FadeIn(tk), FadeIn(yk), FadeIn(rows[0]), Create(curves[0]), FadeIn(key[0]))
            vo.wait_until("a")
            for c, k_ in zip(curves[1:], key[1:]):
                self.play(Create(c), FadeIn(k_), run_time=1.0)
            self.play(FadeIn(rows[1:]))
            vo.wait_until("b")
            self.play(FadeIn(ringw), Create(disk), FadeIn(start), FadeIn(kak[:2]))
            self.play(Create(walk), run_time=2.5, rate_func=linear)
            self.play(FadeIn(end, scale=1.6), FadeIn(kak[2:]))
        self.wait(0.4)
        self.clear_scene()
