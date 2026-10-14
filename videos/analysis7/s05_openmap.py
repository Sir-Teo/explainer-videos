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
        cx = square_axes([-1.5, 1.5, 0.5], [-1.5, 1.5, 0.5], S / 3).move_to([-3.75, -0.6, 0])
        frame = Square(side_length=S, color=GREY_C, stroke_width=2).move_to(cx.c2p(0, 0))
        th = np.linspace(0.2, 0.75, 60)
        arc = 0.35 * np.exp(1j * th) + 0.2
        c0 = 0.2 + 0.35 * np.exp(0.47j)
        arc_m = zcurve(cx, arc, WHITE, 5)
        # the series at c0 converges out to the pole at 2.2 (radius 1.695); a second center c1 inside that disk has a
        # series reaching 3.0, which covers the rest of the frame: continuation, disk by disk
        c1 = -0.8 + 0j
        assert 1.6 < abs(2.2 - c0) < 1.7 and abs(c1 - c0) < 1.6 and abs(2.2 - c1) > 2.9
        masks = [lambda Z, r=r: np.abs(Z - c0) < r for r in (0.12, 0.45, 0.9, 1.6)]
        masks.append(lambda Z: (np.abs(Z - c0) < 1.6) | (np.abs(Z - c1) < 2.9))
        imgs = [cplot(cx, G, (-1.5, 1.5), (-1.5, 1.5), px=600, mask=mk) for mk in masks]
        c1_d = Dot(cx.c2p(c1.real, c1.imag), radius=0.07, color=WHITE)
        c1_l = label(r"new centre", font_size=22).next_to(c1_d, DOWN, buff=0.1)

        def clipped_circle(c, r):  # the dashed edge of the disk |z - c| < r, kept inside the frame (cut, not clamped)
            t = np.linspace(0, 2 * np.pi, 600)
            zc = c + r * np.exp(1j * t)
            ok = (np.abs(zc.real) <= 1.5) & (np.abs(zc.imag) <= 1.5)
            g = VGroup()
            start = None
            for i in range(len(t) + 1):
                if i < len(t) and ok[i]:
                    start = i if start is None else start
                elif start is not None:
                    if i - start > 2:
                        g.add(DashedVMobject(zcurve(cx, zc[start:i], WHITE, 1.8), num_dashes=max(4, (i - start) // 12)))
                    start = None
            return g

        rings = [clipped_circle(c0, r) for r in (0.12, 0.45, 0.9, 1.6)]
        assert all(len(g) for g in rings)
        pole = Arrow(cx.c2p(1.5, 0) + RIGHT * 0.08, cx.c2p(1.5, 0) + RIGHT * 0.75, buff=0, color=C.PATHOLOGY,
                     stroke_width=4, tip_length=0.18)  # off the frame, on the real axis: the way to the pole
        pole_l = label(r"pole at $2.2$", font_size=22, color=C.PATHOLOGY).next_to(pole, UP, buff=0.08).align_to(pole, LEFT)
        assert abs(G(np.array([2.2 + 1e-9]))[0]) > 1e8  # the pole of the series' function, off the frame
        g_l = MathTex(r"f(z) = \frac{z^2 + 1}{z - 2.2} + 0.3z", font_size=28).next_to(frame, UP, buff=0.1)
        rows = VGroup(
            label(r"\textbf{RCA 10.18} \ (the identity theorem)", font_size=24),
            label(r"if $f, g$ are holomorphic on a region $\Omega$", font_size=24),
            label(r"and $f = g$ on a set with a limit point in $\Omega$", font_size=24),
            label(r"(a tiny arc is plenty), \ then $f = g$ on all of $\Omega$", font_size=24, color=C.EPS),
            label(r"why: \ $f - g$ has non-isolated zeros, \ so it is $0$ \ (chapter 1)", font_size=22, color=GREY_A),
            label(r"on $\R$: \ $e^{-1/x^2}$ and $0$ agree on $(-\infty, 0]$, \ not on $(0, \infty)$", font_size=22,
                  color=C.PATHOLOGY),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.16)
        rows.align_to(np.array([max(pole.get_right()[0], pole_l.get_right()[0]) + 0.3, 0, 0]), LEFT).set_y(-0.3)
        assert rows.get_right()[0] <= 6.6
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
            self.play(Create(rings[0]), run_time=0.5)
            for k in range(1, len(imgs)):
                if k == len(imgs) - 1:  # the first series has reached its pole: recenter inside its disk
                    self.play(FadeIn(c1_d, scale=1.5), FadeIn(c1_l), GrowArrow(pole), FadeIn(pole_l), run_time=0.8)
                    self.play(FadeIn(imgs[k]), run_time=1.1)
                else:
                    self.play(FadeIn(imgs[k]), Create(rings[k]), run_time=1.1)
                self.remove(cur)
                cur = imgs[k]
                self.bring_to_front(*rings[:k + 1], arc_m)
                if k == len(imgs) - 1:
                    self.bring_to_front(c1_d, c1_l, pole, pole_l)
            vo.wait_until("c")
            self.play(FadeIn(rows[:4]))
            self.play(FadeIn(rows[4:]))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def local(self):
        ax = square_axes([-1.2, 1.2, 1], [-1.2, 1.2, 1], 1.5).move_to([-4.8, -0.6, 0])
        bx = square_axes([-1.0, 1.0, 1], [-1.0, 1.0, 1], 1.4).move_to([-0.8, -0.6, 0])
        for a in (ax, bx):
            a.set_opacity(0.3)
        n = 12
        cols = [ManimColor(tuple(float(c) for c in hue_rgb(np.array(2 * np.pi * (k + 0.5) / n)))) for k in range(n)]
        r0 = 0.95
        sectors = VGroup()
        sec_pts = []
        for k in range(n):
            a0, a1 = 2 * np.pi * k / n, 2 * np.pi * (k + 1) / n
            t = np.linspace(a0, a1, 30)
            pts = np.concatenate([[0], r0 * np.exp(1j * t)])
            sec_pts.append(pts)
            sectors.add(Polygon(*[ax.c2p(z.real, z.imag) for z in pts], stroke_width=0.5, stroke_color=BACKGROUND,
                                fill_color=cols[k], fill_opacity=0.85))
        # z^3 opens each 30-degree sector to 90 degrees: sectors 1-4 cover the image disk once (sheet 1), and so do
        # sectors 5-8 and 9-12 (sheets 2 and 3, drawn small beside it). Opaque, never stacked.
        small = 0.62
        cx2 = square_axes([-1.0, 1.0, 1], [-1.0, 1.0, 1], small).move_to([1.7, 0.3, 0])
        cx3 = square_axes([-1.0, 1.0, 1], [-1.0, 1.0, 1], small).move_to([1.7, -1.75, 0])
        sheets = []
        for s_, axk in enumerate((bx, cx2, cx3)):
            g = VGroup(*[Polygon(*[axk.c2p(w.real, w.imag) for w in sec_pts[k] ** 3], stroke_width=0.5,
                                 stroke_color=BACKGROUND, fill_color=cols[k], fill_opacity=0.85)
                         for k in range(4 * s_, 4 * s_ + 4)])
            sheets.append(g)
        for s_ in range(3):  # each sheet's angles add up to one full turn: the image disk, once
            spans = [np.ptp(np.unwrap(np.angle(sec_pts[k][1:] ** 3))) for k in range(4 * s_, 4 * s_ + 4)]
            assert abs(sum(spans) - 2 * np.pi) < 1e-9
        sh_l = VGroup(label(r"sheet 1", font_size=22, color=GREY_A).next_to(bx, DOWN, buff=0.12),
                      label(r"sheet 2", font_size=22, color=GREY_A).next_to(cx2, DOWN, buff=0.08),
                      label(r"sheet 3", font_size=22, color=GREY_A).next_to(cx3, DOWN, buff=0.08))
        # every point of the image disk (except 0) is covered exactly 3 times
        rng = np.random.default_rng(4)
        wq = 0.8 * np.sqrt(rng.uniform(0, 1, 200)) * np.exp(2j * np.pi * rng.uniform(0, 1, 200))
        for w in wq:
            roots = np.roots([1, 0, 0, -w])
            assert int(np.sum(np.abs(roots) < r0)) == 3
        lab = VGroup(MathTex(r"|z| < 0.95", font_size=26).next_to(ax, UP, buff=0.1),
                     VGroup(MathTex(r"f(z) = z^3:", font_size=26),
                            MathTex(r"\text{each sector opens to } 3\times \text{ its angle}", font_size=26)
                            ).arrange(DOWN, buff=0.08).next_to(bx, UP, buff=0.1))
        arrow = Arrow(ax.get_right() + RIGHT * 0.1, bx.get_left() + LEFT * 0.1, buff=0, color=GREY_B, stroke_width=4)
        rows = VGroup(
            label(r"\textbf{RCA 10.32} \ near $z_0$:", font_size=24),
            MathTex(r"f(z) - f(z_0)", font_size=26),
            MathTex(r"= (z - z_0)^m\, g(z)^m", font_size=26),
            label(r"so $f$ is $m$-to-$1$ near $z_0$, \ and onto a disk", font_size=22),
            label(r"(200 random points: \ 3 preimages each)", font_size=22, color=GREY_A),
            label(r"\textbf{open mapping:} \ nonconstant $f$", font_size=22, color=C.EPS),
            label(r"maps open sets to open sets", font_size=22, color=C.EPS),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.14)
        rows[2].shift(RIGHT * 0.3)
        rows.align_to(np.array([6.55 - rows.width, 0, 0]), LEFT).set_y(-0.6)
        assert rows.get_right()[0] <= 6.6 and rows.get_left()[0] > cx2.get_right()[0] + 0.25
        assert ax.get_left()[0] > -6.65 and lab[1].get_left()[0] > lab[0].get_right()[0] + 0.3
        assert lab[1].get_right()[0] < cx2.get_left()[0] or lab[1].get_bottom()[1] > cx2.get_top()[1]
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
            self.play(FadeIn(head), Create(ax), Create(bx), FadeIn(rows[:3]))
            vo.wait_until("b")
            self.play(FadeIn(sectors), FadeIn(lab[0]))
            self.play(GrowArrow(arrow), TransformFromCopy(sectors[0:4], sheets[0]), FadeIn(lab[1]), FadeIn(sh_l[0]),
                      run_time=2.0)
            self.play(TransformFromCopy(sectors[4:8], sheets[1]), FadeIn(sh_l[1]), run_time=1.2)
            self.play(TransformFromCopy(sectors[8:12], sheets[2]), FadeIn(sh_l[2]), run_time=1.2)
            self.play(FadeIn(rows[3:5]))
            vo.wait_until("c")
            self.play(FadeIn(rows[5:]))
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
        mx_l = MathTex(r"z = 1", font_size=26, color=C.PATHOLOGY).next_to(mx, UR, buff=0.08)
        rows = VGroup(
            MathTex(r"|f(z)| = |z^2 + e^z| \ \text{on } |z| \le 1", font_size=30),
            MathTex(rf"\max_{{|z| = 1}} |f| = |f(1)| = 1 + e = {bmax:.4f}", font_size=28, color=C.PATHOLOGY),
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
