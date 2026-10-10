from __future__ import annotations

import math

import numpy as np

from explainer import *  # noqa: F403
from videos.relativity.common import redraw, BHShader, boxed, label, load, mtex, note, polyline, rgba
from videos.relativity.s16_mercury import orbit_xy

NEWTON = C.GRAV_POTENTIAL
EINSTEIN = C.CURVATURE


class Hook(VoiceoverScene):
    def construct(self):
        self.mercury()
        self.equation()
        self.apple()
        self.montage()
        self.roadmap()

    # ------------------------------------------------------------------
    def mercury(self):
        d = load("mercury")
        assert abs(float(d["Mercury_century"]) - 42.98) < 0.005
        phis, u, uN = d["ros_phi"], d["ros_u"], d["ros_uN"]
        center = np.array([-2.2, -0.2, 0])
        sc = 1.3
        sun = VGroup(*[Dot(center, radius=0.16 + 0.06 * i, color=C.MATTER).set_opacity(0.9 if i == 0 else 0.15)
                       for i in range(4)])
        k = ValueTracker(0.0)
        n = len(phis)
        P = orbit_xy(phis, u, sc, center)
        peri = [i for i in range(1, n - 1) if u[i] >= u[i - 1] and u[i] >= u[i + 1]]

        def trail():
            j = max(2, int(k.get_value() * (n - 1)))
            g = VGroup(VMobject(stroke_color=EINSTEIN, stroke_width=2.5).set_points_as_corners(P[:j]))
            g.add(Dot(P[j - 1], radius=0.08, color=WHITE))
            for i in peri:  # fixed size: always_redraw's become() misaligns a family whose size changes
                g.add(Dot(P[i], radius=0.05, color=EINSTEIN).set_opacity(1.0 if i < j else 0.0))
            return g

        tr = redraw(trail)
        ex = note(r"computed orbit; the effect exaggerated about 600{,}000$\times$").to_corner(DL, buff=0.3)
        num = VGroup(label(r"Mercury's orbit turns by", font_size=32),
                     mtex(r"43''\ \text{per century}", font_size=48, color=EINSTEIN),
                     label(r"more than Newton's law allows", font_size=32)).arrange(DOWN, buff=0.2).move_to([4.2, 0.6, 0])
        with self.voiceover(
            "For more than two hundred years, Newton's law of gravity predicted the motion of the planets with astonishing "
            "precision. <bookmark mark='o'/> But not perfectly. Mercury's orbit is an ellipse, and the ellipse slowly "
            "turns. Most of that turning is caused by the pull of the other planets, and Newton's law accounts for it. "
            "<bookmark mark='n'/> But a tiny part, forty-three arcseconds per century, refused to be explained."
        ) as vo:
            self.play(FadeIn(sun))
            self.add(tr)
            self.play(FadeIn(ex), k.animate.set_value(0.6), run_time=vo.until("n"), rate_func=linear)
            self.play(FadeIn(num, lag_ratio=0.3), k.animate.set_value(1.0), run_time=vo.remaining() + 0.5, rate_func=linear)
        tr.clear_updaters()
        self.clear_scene()

    # ------------------------------------------------------------------
    def equation(self):
        eq = mtex(r"G_{\mu\nu}", r"=", r"\frac{8\pi G}{c^4}", r"\,T_{\mu\nu}", font_size=88)
        eq[0].set_color(EINSTEIN)
        eq[3].set_color(C.MATTER)
        eq.move_to(UP * 0.6)
        b1 = Brace(eq[0], DOWN, color=EINSTEIN)
        b1l = label(r"the curvature of spacetime", font_size=30, color=EINSTEIN).next_to(b1, DOWN, buff=0.1)
        b2 = Brace(eq[3], DOWN, color=C.MATTER)
        b2l = label(r"energy and momentum", font_size=30, color=C.MATTER).next_to(b2, DOWN, buff=0.1)
        date = label(r"Albert Einstein, November 1915", font_size=30, color=GREY_A).next_to(eq, UP, buff=0.6)
        quote = VGroup(label(r"``Spacetime tells matter how to move;", font_size=32),
                       label(r"matter tells spacetime how to curve.''", font_size=32),
                       label(r"--- John Wheeler", font_size=26, color=GREY_A)).arrange(DOWN, buff=0.12)
        quote.to_edge(DOWN, buff=0.4)
        with self.voiceover(
            "<bookmark mark='e'/> In November 1915, Albert Einstein explained it, with a new theory of gravity and this "
            "equation. <bookmark mark='l'/> On the left, the curvature of space and time. <bookmark mark='r'/> On the "
            "right, energy and momentum. <bookmark mark='w'/> In John Wheeler's words: spacetime tells matter how to "
            "move, and matter tells spacetime how to curve."
        ) as vo:
            vo.wait_until("e")
            self.play(Write(eq), FadeIn(date), run_time=2)
            vo.wait_until("l")
            self.play(GrowFromCenter(b1), FadeIn(b1l))
            vo.wait_until("r")
            self.play(GrowFromCenter(b2), FadeIn(b2l))
            vo.wait_until("w")
            self.play(FadeIn(quote, lag_ratio=0.2))
        self.clear_scene()

    # ------------------------------------------------------------------
    def apple(self):
        ax = Axes(x_range=[0, 2, 1], y_range=[0, 6, 2], x_length=4.6, y_length=4.0, tips=False,
                  axis_config={"stroke_color": GREY_B, "include_ticks": False}).move_to([-4.2, -0.6, 0])
        xl = label(r"time", font_size=24).next_to(ax.x_axis, DOWN, buff=0.2)
        yl = label(r"height", font_size=24).next_to(ax.y_axis, UP, buff=0.15)
        p0, p1 = ax.c2p(0, 0), ax.c2p(2, 6)
        z = np.linspace(6, 0, 80)[:, None] * np.ones((1, 4))
        col = np.array(ManimColor(C.PROPER_TIME).to_rgb())
        bg = ImageMobject(rgba(np.ones((80, 4, 3)) * col, 0.04 + 0.3 * z / 6)).stretch_to_fit_width(p1[0] - p0[0])
        bg.stretch_to_fit_height(p1[1] - p0[1]).move_to((p0 + p1) / 2)
        ts = np.linspace(0, 2, 100)
        path = polyline(ax, ts, 4 * 4.905 * ts * (2 - ts) / 4, color=WHITE, stroke_width=4)
        txt = VGroup(
            label(r"Drop an apple, or throw it:", font_size=32),
            label(r"it isn't pulled by anything.", font_size=32),
            label(r"It follows the straightest path through spacetime,", font_size=32),
            label(r"and it falls because \emph{time runs slower near the ground}.", font_size=32, color=C.PROPER_TIME),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.22).move_to([2.7, 0.3, 0])
        with self.voiceover(
            "In Einstein's theory, gravity isn't a force at all. Here's the strangest consequence, which we'll derive in "
            "this video. <bookmark mark='a'/> When you throw an apple, nothing pulls it down. It follows the straightest "
            "possible path through spacetime, <bookmark mark='b'/> and the reason that path curves back to the ground is "
            "that time passes more slowly near the Earth than higher up."
        ) as vo:
            self.play(Create(ax), FadeIn(xl), FadeIn(yl), FadeIn(bg))
            vo.wait_until("a")
            self.play(Create(path), FadeIn(txt[:3], lag_ratio=0.3), run_time=2)
            vo.wait_until("b")
            self.play(FadeIn(txt[3]))
        self.clear_scene()

    # ------------------------------------------------------------------
    def montage(self):
        lt = load("light")
        g = load("gw")
        gps = load("gps")
        tiles = Group()
        W, H = 5.6, 3.15
        centers = [np.array([-3.25, 1.75, 0]), np.array([3.25, 1.75, 0]), np.array([-3.25, -1.85, 0]),
                   np.array([3.25, -1.85, 0])]
        frames = VGroup(*[RoundedRectangle(width=W, height=H, corner_radius=0.12, color=GREY_C, stroke_width=1.5).move_to(c)
                          for c in centers])
        # 1: light bending
        c0 = centers[0]
        rays = VGroup()
        for P, cap in zip(lt["fan"], lt["fan_captured"]):
            P = P[np.isfinite(P[:, 0])]
            pts = c0[:2] + 0.17 * P + np.array([0.3, -0.1])
            ok = (np.abs(pts[:, 0] - c0[0]) < W / 2 - 0.1) & (np.abs(pts[:, 1] - c0[1]) < H / 2 - 0.1)
            pts = pts[ok]
            if len(pts) > 1:
                rays.add(VMobject(stroke_color=C.LIGHT, stroke_width=1.8, stroke_opacity=0.5 if cap else 0.9)
                         .set_points_as_corners(np.concatenate([pts, np.zeros((len(pts), 1))], 1)))
        hole = Dot(c0 + np.array([0.3, -0.1, 0]), radius=0.17, color=BLACK).set_stroke(GREY_C, 1.5)
        t1 = label(r"light bends", font_size=26).next_to(frames[0].get_corner(UL), DR, buff=0.12)
        # 2: clocks
        c1 = centers[1]
        clk = VGroup(label(r"GPS clocks gain", font_size=30), mtex(r"38\ \mu\text{s per day}", font_size=40, color=C.PROPER_TIME),
                     label(r"(or your position drifts 11 km a day)", font_size=22, color=GREY_A)).arrange(DOWN, buff=0.15).move_to(c1)
        t2 = label(r"time slows", font_size=26).next_to(frames[1].get_corner(UL), DR, buff=0.12)
        assert abs(float(gps["gps"][2]) - 38.5) < 0.1
        # 3: black hole
        sh = BHShader(load("bh80"))
        bh = ImageMobject(sh(30.0)).set_resampling_algorithm(RESAMPLING_ALGORITHMS["bilinear"])
        bh.set_width(W - 0.1).move_to(centers[2])
        if bh.height > H - 0.1:
            bh.set_height(H - 0.1)
        t3 = label(r"black holes", font_size=26).next_to(frames[2].get_corner(UL), DR, buff=0.12)
        # 4: waves
        c3 = centers[3]
        ax = Axes(x_range=[-0.2, 0.05, 0.05], y_range=[-1.3, 1.3, 1], x_length=W - 0.6, y_length=H - 1.0, tips=False,
                  axis_config={"stroke_color": GREY_D, "include_ticks": False}).move_to(c3 + DOWN * 0.15)
        sel = (g["t"] > -0.2) & (g["t"] < 0.05)
        s = 1 / np.abs(g["H1"][sel]).max()
        wave = polyline(ax, g["t"][sel], g["H1"][sel] * s, color=C.WAVE, stroke_width=2)
        t4 = label(r"gravitational waves (LIGO, 2015)", font_size=26).next_to(frames[3].get_corner(UL), DR, buff=0.12)
        with self.voiceover(
            "From that equation flow some of the most remarkable predictions in science. <bookmark mark='a'/> Light bends "
            "around massive objects. <bookmark mark='b'/> Clocks run at different rates at different heights, which your "
            "phone's GPS has to correct for every day. <bookmark mark='c'/> Black holes, regions from which not even light "
            "can escape. <bookmark mark='d'/> And ripples in spacetime itself, gravitational waves, detected for the first "
            "time in 2015, a century after Einstein predicted them."
        ) as vo:
            self.play(FadeIn(frames))
            vo.wait_until("a")
            self.play(FadeIn(t1), FadeIn(hole), LaggedStart(*[Create(r) for r in rays], lag_ratio=0.05), run_time=2)
            vo.wait_until("b")
            self.play(FadeIn(t2), FadeIn(clk))
            vo.wait_until("c")
            self.play(FadeIn(bh), FadeIn(t3))
            vo.wait_until("d")
            self.play(FadeIn(t4), Create(ax), Create(wave), run_time=2)
        self.wait(1.0)
        self.clear_scene()

    # ------------------------------------------------------------------
    def roadmap(self):
        items = [
            (r"Gravity is geometry", r"\text{falling} = \text{maximal } \tau", C.PROPER_TIME),
            (r"The mathematics of curvature", r"R^\rho{}_{\sigma\mu\nu} = \partial_\mu\Gamma^\rho{}_{\nu\sigma} - \cdots", C.CURVATURE),
            (r"Einstein's equation", r"G_{\mu\nu} = \tfrac{8\pi G}{c^4}T_{\mu\nu}", C.MATTER),
            (r"Solutions and tests", r"ds^2 = -\big(1 - \tfrac{r_s}{r}\big)c^2dt^2 + \cdots", C.LIGHT),
        ]
        title = label(r"This video derives it, from the ground up", font_size=40).to_edge(UP, buff=0.45)
        rows = VGroup()
        for i, (name, f, colr) in enumerate(items, 1):
            n_ = label(rf"Part {i}", font_size=28, color=C.DIM)
            t_ = label(name, font_size=34)
            fm = mtex(f, font_size=32, color=colr)
            rows.add(VGroup(n_, t_, fm))
        for r in rows:
            r[1].next_to(r[0], RIGHT, buff=0.35)
        rows.arrange(DOWN, aligned_edge=LEFT, buff=0.55).next_to(title, DOWN, buff=0.6).to_edge(LEFT, buff=0.8)
        for r in rows:
            r[2].move_to([3.9, r[0].get_y(), 0])
        with self.voiceover(
            "In this video we'll derive Einstein's theory from scratch, and the mathematics will be front and center. "
            "<bookmark mark='a'/> First, why gravity is geometry: the equivalence principle, clocks, and the idea that "
            "falling is maximal aging. <bookmark mark='b'/> Then the mathematics of curved spaces: metrics, tensors, "
            "Christoffel symbols, the covariant derivative, and the Riemann curvature tensor. <bookmark mark='c'/> Then "
            "we'll derive Einstein's equation, two different ways, and see what it means. <bookmark mark='d'/> And "
            "finally, we'll solve it, and test it: black holes, Mercury's orbit, the bending of light, and gravitational "
            "waves."
        ) as vo:
            self.play(FadeIn(title))
            for m, r in zip("abcd", rows):
                vo.wait_until(m)
                self.play(FadeIn(r[0]), FadeIn(r[1], shift=RIGHT * 0.2), Write(r[2]), run_time=1.2)
        self.wait(0.5)
        self.clear_scene()
