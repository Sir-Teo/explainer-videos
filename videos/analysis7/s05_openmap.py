from __future__ import annotations

import math

import numpy as np

from explainer.analysis import *  # noqa: F403
from videos.analysis7.common import cplot, load, square_axes, zcurve


def G(z):
    return (z * z + 1) / (z - 2.2) + 0.3 * z


class OpenMapping(VoiceoverScene):
    def construct(self):
        self.card()
        self.identity()
        self.local()
        self.maxmod()

    # ------------------------------------------------------------------
    def card(self):
        card = chapter_card(4, r"Zeros, open maps and the maximum modulus", r"Where can $|f|$ be largest?", lit=(), part=7)
        with self.voiceover("Chapter four: what a holomorphic function's zeros and values are allowed to do."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))

    # ------------------------------------------------------------------
    def identity(self):
        S = 5.0
        cx = square_axes([-1.5, 1.5, 0.5], [-1.5, 1.5, 0.5], S / 3).move_to([-3.4, -0.6, 0])
        frame = Square(side_length=S, color=GREY_C, stroke_width=2).move_to(cx.c2p(0, 0))
        th = np.linspace(0.2, 0.75, 60)
        arc = 0.35 * np.exp(1j * th) + 0.2
        c0 = 0.2 + 0.35 * np.exp(0.47j)
        arc_m = zcurve(cx, arc, WHITE, 5)
        radii = [0.12, 0.45, 0.9, 1.6, 2.6]
        imgs = [cplot(cx, G, (-1.5, 1.5), (-1.5, 1.5), px=600, mask=lambda Z, r=r: np.abs(Z - c0) < r) for r in radii]
        g_l = MathTex(r"f(z) = \frac{z^2 + 1}{z - 2.2} + 0.3z", font_size=28).next_to(frame, UP, buff=0.1)
        rows = VGroup(
            label(r"\textbf{RCA 10.18} \ (the identity theorem) \ if $f, g$ are holomorphic on a region $\Omega$", font_size=24),
            label(r"and $f = g$ on a set with a limit point in $\Omega$ \ (a tiny arc is plenty),", font_size=24),
            label(r"then $f = g$ on all of $\Omega$", font_size=26, color=C.EPS),
            label(r"why: \ $f - g$ has non-isolated zeros, \ so it is $0$ \ (chapter 1)", font_size=22, color=GREY_A),
            label(r"on $\R$: \ $e^{-1/x^2}$ and $0$ agree on $(-\infty, 0]$, \ not on $(0, \infty)$", font_size=22,
                  color=C.PATHOLOGY),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.16).move_to([3.3, -0.3, 0])
        for r_ in rows:
            if r_.width > 6.6:
                r_.width = 6.6
        rows.arrange(DOWN, aligned_edge=LEFT, buff=0.16).move_to([3.4, -0.3, 0])
        head = label(r"The third miracle: \ a tiny arc decides everything", font_size=34).to_edge(UP, buff=0.3)
        with self.voiceover(
            "<bookmark mark='a'/> Here's the third miracle. Suppose you know a holomorphic function only on this "
            "short white arc. <bookmark mark='b'/> Then you know it everywhere it can be continued: the power series "
            "at a point of the arc is determined by the values on the arc, and that series decides the next disk, and "
            "the next. <bookmark mark='c'/> The identity theorem: two holomorphic functions that agree on a set with "
            "a limit point agree on the whole region, because their difference has zeros that aren't isolated. "
            "Nothing like it holds on the real line."
        ) as vo:
            vo.wait_until("a")
            self.play(FadeIn(head), Create(frame), FadeIn(g_l), FadeIn(imgs[0]), Create(arc_m))
            vo.wait_until("b")
            cur = imgs[0]
            for k in range(1, len(imgs)):
                self.play(FadeIn(imgs[k]), run_time=1.1)
                self.remove(cur)
                cur = imgs[k]
                self.bring_to_front(arc_m)
            vo.wait_until("c")
            self.play(FadeIn(rows[:3]))
            self.play(FadeIn(rows[3:]))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def local(self):
        ax = square_axes([-1.2, 1.2, 1], [-1.2, 1.2, 1], 1.8).move_to([-4.0, -0.6, 0])
        bx = square_axes([-1.2, 1.2, 1], [-1.2, 1.2, 1], 1.8).move_to([1.2, -0.6, 0])
        for a in (ax, bx):
            a.set_opacity(0.3)
        n = 12
        cols = [ManimColor(tuple(float(c) for c in hue_rgb(np.array(2 * np.pi * (k + 0.5) / n)))) for k in range(n)]
        r0 = 0.95
        sectors, images = VGroup(), VGroup()
        for k in range(n):
            a0, a1 = 2 * np.pi * k / n, 2 * np.pi * (k + 1) / n
            t = np.linspace(a0, a1, 30)
            pts = np.concatenate([[0], r0 * np.exp(1j * t)])
            sectors.add(Polygon(*[ax.c2p(z.real, z.imag) for z in pts], stroke_width=0.5, stroke_color=BACKGROUND,
                                fill_color=cols[k], fill_opacity=0.85))
            w = pts**3
            images.add(Polygon(*[bx.c2p(z.real, z.imag) for z in w], stroke_width=0.5, stroke_color=BACKGROUND,
                               fill_color=cols[k], fill_opacity=0.3))
        # every point of the image disk (except 0) is covered exactly 3 times
        rng = np.random.default_rng(4)
        wq = 0.8 * np.sqrt(rng.uniform(0, 1, 200)) * np.exp(2j * np.pi * rng.uniform(0, 1, 200))
        for w in wq:
            roots = np.roots([1, 0, 0, -w])
            assert int(np.sum(np.abs(roots) < r0)) == 3
        lab = VGroup(MathTex(r"|z| < 0.95", font_size=26).next_to(ax, UP, buff=0.1),
                     MathTex(r"f(z) = z^3: \text{ each sector opens to } 3\times \text{ its angle}", font_size=26).next_to(
                         bx, UP, buff=0.1))
        arrow = Arrow([-1.6, -0.6, 0], [-0.8, -0.6, 0], buff=0, color=GREY_B, stroke_width=4)
        rows = VGroup(
            label(r"\textbf{RCA 10.32} \ near $z_0$:", font_size=24),
            MathTex(r"f(z) - f(z_0) = (z - z_0)^m\, g(z)^m", font_size=26),
            label(r"so $f$ is $m$-to-$1$ near $z_0$, \ and onto a disk", font_size=22),
            label(r"(200 random points: \ 3 preimages each)", font_size=22, color=GREY_A),
            label(r"\textbf{open mapping:} \ nonconstant $f$", font_size=22, color=C.EPS),
            label(r"maps open sets to open sets", font_size=22, color=C.EPS),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.14).move_to([5.25, -0.6, 0])
        for r_ in rows:
            if r_.width > 3.3:
                r_.width = 3.3
        rows.arrange(DOWN, aligned_edge=LEFT, buff=0.14).move_to([5.3, -0.6, 0])
        head = label(r"Near a point, a holomorphic map looks like $z \mapsto z^m$", font_size=34).to_edge(UP, buff=0.3)
        with self.voiceover(
            "<bookmark mark='a'/> Near any point, a nonconstant holomorphic function looks like a power: f of z minus "
            "f of z zero is z minus z zero to the m, times a nonvanishing factor. <bookmark mark='b'/> For z cubed, "
            "color a small disk in twelve sectors. Each sector opens to three times its angle, and the image disk is "
            "covered three times over: every point has three preimages, checked at two hundred random points. "
            "<bookmark mark='c'/> Either way, the image of a small disk contains a disk around f of z zero. That's the "
            "open mapping theorem: nonconstant holomorphic functions send open sets to open sets."
        ) as vo:
            vo.wait_until("a")
            self.play(FadeIn(head), Create(ax), Create(bx), FadeIn(rows[:2]))
            vo.wait_until("b")
            self.play(FadeIn(sectors), FadeIn(lab[0]))
            self.play(GrowArrow(arrow), TransformFromCopy(sectors, images), FadeIn(lab[1]), run_time=2.5)
            self.play(FadeIn(rows[2:4]))
            vo.wait_until("c")
            self.play(FadeIn(rows[4:]))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def maxmod(self):
        d = load("maxmod")
        bmax, th_max, imax = float(d["bmax"]), float(d["th_max"]), float(d["imax"])
        S = 5.0
        ax = square_axes([-1.05, 1.05, 0.5], [-1.05, 1.05, 0.5], S / 2.1).move_to([-3.4, -0.6, 0])
        px = 600
        x = np.linspace(-1.05, 1.05, px)
        X, Y = np.meshgrid(x, x[::-1])
        Z = X + 1j * Y
        M = np.abs(Z**2 + np.exp(Z))
        t = np.clip(M / 3.8, 0, 1)[..., None]
        lo, mid, hi = (np.array(ManimColor(c).to_rgb()) for c in (BACKGROUND, C.MEASURE, "#FFF4D6"))
        rgb = np.where(t < 0.6, lo + (t / 0.6) * (mid - lo), mid + ((t - 0.6) / 0.4) * (hi - mid))
        alpha = (np.abs(Z) <= 1.0).astype(float)[..., None]
        im = ImageMobject((np.concatenate([rgb, alpha], axis=-1) * 255).astype(np.uint8))
        im.set_resampling_algorithm(RESAMPLING_ALGORITHMS["bilinear"])
        im.stretch_to_fit_width(S).stretch_to_fit_height(S).move_to(ax.c2p(0, 0))
        circ = Circle(radius=ax.c2p(1, 0)[0] - ax.c2p(0, 0)[0], color=WHITE, stroke_width=2.5).move_to(ax.c2p(0, 0))
        xs = np.linspace(-1, 1, 241)
        levels = [1.0, 1.5, 2.0, 2.5, 3.0, 3.5]
        Mf = lambda X_, Y_: np.abs((X_ + 1j * Y_) ** 2 + np.exp(X_ + 1j * Y_))  # noqa: E731

        def inside_disk(segs):
            mid = segs.mean(axis=1)
            return segs[np.hypot(mid[:, 0], mid[:, 1]) <= 1.0]

        lines = VGroup(*[contour_mobject(ax, inside_disk(contour_segments(lambda X_, Y_, L=L: Mf(X_, Y_) - L, xs, xs)),
                                         WHITE, 1.2, opacity=0.6) for L in levels])
        mx = Dot(ax.c2p(math.cos(th_max), math.sin(th_max)), radius=0.1, color=C.PATHOLOGY)
        mx_l = MathTex(rf"|f(1)| = 1 + e = {bmax:.4f}", font_size=26, color=C.PATHOLOGY).next_to(mx, UR, buff=0.1)
        rows = VGroup(
            MathTex(r"|f(z)| = |z^2 + e^z| \ \text{on } |z| \le 1", font_size=30),
            MathTex(rf"\max_{{|z| = 1}} |f| = {bmax:.4f}", font_size=28, color=C.PATHOLOGY),
            MathTex(rf"\max_{{|z| \le 0.98}} |f| = {imax:.4f}", font_size=28, color=C.MEASURE),
            label(r"\textbf{RCA 10.24} \ (maximum modulus) \ a nonconstant", font_size=24),
            label(r"holomorphic $f$ has no interior maximum of $|f|$", font_size=24, color=C.EPS),
            label(r"proof: \ near an interior point, \ $f$ covers a disk", font_size=22, color=GREY_A),
            label(r"around $f(z_0)$, \ which contains larger values", font_size=22, color=GREY_A),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.15).move_to([3.4, -0.5, 0])
        assert imax < bmax and abs(bmax - (1 + math.e)) < 1e-9
        head = label(r"The landscape of $|f|$ has no peaks inside", font_size=34).to_edge(UP, buff=0.3)
        with self.voiceover(
            "<bookmark mark='a'/> Here's the size of z squared plus e to the z over the closed unit disk, bright where "
            "it's large, with level curves. <bookmark mark='b'/> The largest value is on the boundary, at z equals "
            "one, where it's one plus e. Inside, even at radius 0.98, it never gets there. "
            "<bookmark mark='c'/> That's the maximum modulus principle, and the open mapping theorem proves it: near "
            "an interior point, f covers a whole disk around f of z zero, and that disk contains values of larger "
            "size. The landscape of a holomorphic function's size has no peaks, only passes."
        ) as vo:
            vo.wait_until("a")
            self.play(FadeIn(head), FadeIn(im), Create(circ), FadeIn(rows[0]))
            self.play(Create(lines), run_time=2.0)
            vo.wait_until("b")
            self.play(FadeIn(mx, scale=2), FadeIn(mx_l), FadeIn(rows[1:3]))
            vo.wait_until("c")
            self.play(FadeIn(rows[3:5]))
            self.play(FadeIn(rows[5:]))
        self.wait(0.4)
        self.clear_scene()
