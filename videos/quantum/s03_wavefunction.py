from __future__ import annotations

import numpy as np

from explainer import *  # noqa: F403
from videos.quantum.common import (Projector, WaveView, boxed, corner_wheel, depth_sorted, frames_at, helix_points,
                                   hue, label, line_3d, load, mtex, note, phase_wheel, phasor, segments_3d, wave_axes,
                                   ylabel)

SIG, K = 1.2, 3.0  # the example packet of this chapter: psi(x) = A exp(-x^2 / 4 sigma^2) exp(i k x)


def packet(x, sigma=SIG, k=K, x0=0.0):
    return (2 * np.pi * sigma**2) ** -0.25 * np.exp(-((x - x0) ** 2) / (4 * sigma**2) + 1j * k * x)


class Wavefunction(VoiceoverScene):
    def construct(self):
        self.arrows_along_x()
        self.helix_views()
        self.to_color()
        self.born_rule()
        self.global_phase()
        self.momentum_in_phase()
        self.plane_wave()

    # ------------------------------------------------------------------
    def arrows_along_x(self):
        xs = np.linspace(-5.6, 5.6, 25)
        psi = packet(xs)
        line = NumberLine(x_range=[-6, 6, 1], length=12, color=GREY_B, include_numbers=False, include_ticks=False)
        line.shift(DOWN * 1.6)
        xl = MathTex("x", font_size=34, color=C.XPOS).next_to(line, RIGHT, buff=0.15)
        R = 0.21
        rings = VGroup(*[Circle(radius=R, color=GREY_D, stroke_width=1.2).move_to([x, 0.2, 0]) for x in xs])
        unit = R / np.abs(psi).max()
        arrows = VGroup(*[phasor(z, origin=[x, 0.2, 0], unit=unit, stroke_width=3, tip=0.08) for x, z in zip(xs, psi)])
        ticks = VGroup(*[DashedLine([x, -1.6, 0], [x, 0.2 - R, 0], color=GREY_D, stroke_width=1, dash_length=0.05)
                         for x in xs])
        one = 12
        zoom_ring = Circle(radius=1.1, color=GREY_C, stroke_width=1.5).move_to(UP * 2.6)
        zarrow = phasor(psi[one], origin=UP * 2.6, unit=1.1 / np.abs(psi).max() * 0.98, stroke_width=5, tip=0.2)
        zlab = MathTex(r"\psi(x)", r"\in\mathbb{C}", font_size=36).next_to(zoom_ring, RIGHT, buff=0.3)
        conn = DashedLine(arrows[one].get_start() + UP * 0.25, zoom_ring.get_bottom(), color=GREY_C, stroke_width=1.5)
        with self.voiceover(
            "In the double slit, each path contributed one arrow, one complex number. Now let an electron be anywhere "
            "on a line. <bookmark mark='a'/> Quantum mechanics assigns it an arrow at every point x: a complex number "
            "whose length and direction can change from place to place. <bookmark mark='z'/> That assignment, x goes to "
            "a complex number, is the wavefunction, psi of x."
        ) as vo:
            self.play(Create(line), FadeIn(xl))
            vo.wait_until("a")
            self.play(LaggedStart(*[AnimationGroup(Create(t), FadeIn(r), GrowArrow(a))
                                    for t, r, a in zip(ticks, rings, arrows)], lag_ratio=0.06), run_time=2.6)
            vo.wait_until("z")
            self.play(Create(conn), FadeIn(zoom_ring), GrowArrow(zarrow), Write(zlab))
        with self.voiceover(
            "If you have seen a quantum state drawn as an arrow with a few components, this is the same idea, "
            "with one component for every point on the line. <bookmark mark='l'/> Two things vary along x: how long "
            "each arrow is, <bookmark mark='d'/> and which way it points."
        ) as vo:
            vo.wait_until("l")
            self.play(LaggedStart(*[Indicate(a, scale_factor=1.25, color=WHITE) for a in arrows[8:17]], lag_ratio=0.1),
                      run_time=1.5)
            vo.wait_until("d")
            self.play(Rotate(zarrow, angle=TAU, about_point=UP * 2.6), run_time=2.2)
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def _helix(self, proj, xs, psi, cols, x_unit, amp, arrow_idx, with_axes=True):
        P = helix_points(xs, psi, x_unit=x_unit, amp_unit=amp)
        parts = [segments_3d(proj, P, cols, stroke_width=3.2, depth_range=amp * 1.2, min_opacity=0.3)]
        x0, x1 = xs[0] * x_unit - 0.4, xs[-1] * x_unit + 0.4
        parts.append(line_3d(proj, [x0, 0, 0], [x1, 0, 0], color=GREY_B, n=48, stroke_width=2, depth_range=amp))
        for i in arrow_idx:
            parts.append(line_3d(proj, [P[i, 0], 0, 0], P[i], color=cols[min(i, len(cols) - 1)], n=4, stroke_width=2.4,
                                 depth_range=amp * 1.2, min_opacity=0.35))
        g = depth_sorted(*parts)
        if with_axes:
            o = np.array([x0, 0, 0])
            ax = VGroup(*[line_3d(proj, o - v * amp * 1.15, o + v * amp * 1.15, color=GREY_C, n=6, stroke_width=1.5,
                                  depth_range=amp) for v in (np.array([0, 1, 0]), np.array([0, 0, 1]))])
            re = MathTex(r"\mathrm{Re}\,\psi", font_size=26, color=GREY_A).move_to(proj.point(o + [0, amp * 1.4, 0]))
            im = MathTex(r"\mathrm{Im}\,\psi", font_size=26, color=GREY_A).move_to(proj.point(o + [0, 0, amp * 1.55]))
            for lab, v in ((re, [0, 1, 0]), (im, [0, 0, 1])):  # fade a label whose axis points at the camera
                seen = np.linalg.norm(proj.point(o + np.array(v) * amp) - proj.point(o))
                lab.set_opacity(float(np.clip((seen / amp - 0.25) / 0.4, 0, 1)))
            xl = MathTex("x", font_size=30, color=C.XPOS).move_to(proj.point([x1 + 0.35, 0, 0]))
            g = VGroup(ax, g, re, im, xl)
        return g

    def helix_views(self):
        xs = np.linspace(-5.6, 5.6, 400)
        psi = packet(xs)
        cols = [hue(np.angle(z)) for z in psi[:-1]]
        amp = 1.55 / np.abs(psi).max()
        proj = Projector(az=-0.62, el=0.32, scale=1.0, center=DOWN * 0.2)
        arrow_idx = list(range(0, 400, 16))
        hel = always_redraw(lambda: self._helix(proj, xs, psi, cols, 1.0, amp, arrow_idx))
        cap = label(r"the wavefunction in 3D: $x$ along the axis, $\psi(x)$ in the plane across it", font_size=28,
                    color=GREY_A).to_edge(UP, buff=0.4)
        with self.voiceover(
            "To see every arrow at once, stand each one up in its own complex plane, perpendicular to the x axis, "
            "<bookmark mark='h'/> and connect their tips. The wavefunction becomes a curve in three dimensions: here, a "
            "helix that swells and fades."
        ) as vo:
            self.play(FadeIn(cap))
            vo.wait_until("h")
            self.add(hel)
            self.play(FadeIn(hel), run_time=1.5)
        with self.voiceover(
            "Now look at it from the front. <bookmark mark='f'/> All you see is the real part: the wiggly curve you "
            "find in most textbooks. But that's only a shadow. <bookmark mark='i'/> Turn it a quarter turn and you see "
            "the imaginary part, the same wiggle shifted by a quarter of a cycle. Neither is more real than the other."
        ) as vo:
            vo.wait_until("f")
            self.play(proj.az.animate.set_value(0.0), proj.el.animate.set_value(0.0), run_time=2.2)
            vo.wait_until("i")
            self.play(proj.el.animate.set_value(-PI / 2), run_time=2.2)
        with self.voiceover(
            "And looking straight down the x axis, <bookmark mark='e'/> every arrow lands in one complex plane: "
            "different lengths, pointing every which way. <bookmark mark='b'/> Both views matter. To keep both in a "
            "flat picture, we need one more idea."
        ) as vo:
            self.play(proj.el.animate.set_value(0.0), run_time=1.5)
            vo.wait_until("e")
            self.play(proj.az.animate.set_value(PI / 2 - 0.02), run_time=2.2)
            vo.wait_until("b")
            self.play(proj.az.animate.set_value(-0.62), proj.el.animate.set_value(0.32), run_time=2.2)
        self.wait(0.3)
        hel.clear_updaters()
        self.clear_scene()

    # ------------------------------------------------------------------
    def to_color(self):
        # One arrow, one color
        wheel = phase_wheel(radius=1.3, labels=True, title=False).move_to(LEFT * 3.2 + UP * 0.6)
        ang = ValueTracker(0.0)
        arr = always_redraw(lambda: phasor(1.0 * np.exp(1j * ang.get_value()), origin=wheel[0].get_center(),
                                           unit=1.0, stroke_width=6, tip=0.22))
        swatch = always_redraw(lambda: Square(1.3, fill_color=hue(ang.get_value()), fill_opacity=1, stroke_width=0)
                               .move_to(RIGHT * 2.4 + UP * 0.6))
        sw_l = label(r"direction of the arrow $\to$ color", font_size=30, color=GREY_A).next_to(swatch, DOWN, buff=0.4)
        with self.voiceover(
            "Here's the idea: replace the direction of each arrow with a color. <bookmark mark='a'/> Pointing right is "
            "red, straight up is yellow-green, left is cyan, down is violet, and everything in between blends smoothly "
            "around the wheel. The angle of a complex number is called its phase, so color will mean phase."
        ) as vo:
            self.play(FadeIn(wheel), FadeIn(arr), FadeIn(swatch), FadeIn(sw_l))
            vo.wait_until("a")
            self.play(ang.animate.set_value(TAU), run_time=vo.remaining() - 0.3, rate_func=linear)
        arr.clear_updaters()
        swatch.clear_updaters()
        self.clear_scene()

        x = np.linspace(-6, 6, 1200)
        psi = packet(x)
        ax = wave_axes((-6, 6), (0, 1.05), x_length=12, y_length=3.4).shift(DOWN * 0.6)
        wv_abs = WaveView(ax, x, psi, mode="abs", scale=1.6)
        wv_den = WaveView(ax, x, psi, mode="density", scale=2.8)
        wheel = corner_wheel()
        ylab = ylabel(ax, r"|\psi(x)|", font_size=32)
        ylab2 = ylabel(ax, r"|\psi(x)|^2", color=C.BORN, font_size=32)
        xl = MathTex("x", font_size=32, color=C.XPOS).next_to(ax.x_axis.get_end(), RIGHT, buff=0.12)
        with self.voiceover(
            "So here is the same wavefunction, flattened. <bookmark mark='a'/> The height is the length of each arrow, "
            "and the color is its direction. The bands of color cycling along x are the helix's turns. "
            "<bookmark mark='s'/> One more change, and we'll keep this convention for the rest of the video: from now "
            "on, the height shows the length squared, <bookmark mark='p'/> for a reason we're about to see."
        ) as vo:
            self.play(Create(ax), FadeIn(xl), FadeIn(wheel))
            vo.wait_until("a")
            self.play(FadeIn(wv_abs), FadeIn(ylab), run_time=1.5)
            vo.wait_until("s")
            self.play(FadeOut(wv_abs), FadeIn(wv_den), ReplacementTransform(ylab, ylab2), run_time=1.5)
        self.wv, self.ax, self.x, self.psi, self.wheel, self.ylab, self.xl = wv_den, ax, x, psi, wheel, ylab2, xl

    # ------------------------------------------------------------------
    def born_rule(self):
        ax, x, psi = self.ax, self.x, self.psi
        a, b = -0.5, 1.5
        xi = np.linspace(a, b, 4001)
        P = float(np.trapezoid(np.abs(packet(xi)) ** 2, xi))
        tot = float(np.trapezoid(np.abs(psi) ** 2, x))
        assert abs(tot - 1) < 1e-6 and abs(P - 0.556) < 0.001, (tot, P)
        area = ax.get_area(ax.plot(lambda t: 2.8 * (2 * np.pi * SIG**2) ** -0.5 * np.exp(-t * t / (2 * SIG**2)),
                                   x_range=[a, b]), x_range=[a, b], color=C.BORN, opacity=0.35)
        la = MathTex("a", font_size=30).next_to(ax.c2p(a, 0), DOWN, buff=0.12)
        lb = MathTex("b", font_size=30).next_to(ax.c2p(b, 0), DOWN, buff=0.12)
        born = MathTex(r"P(a \le x \le b)", r"=", r"\int_a^b |\psi(x)|^2\,dx", font_size=40).to_edge(UP, buff=0.5)
        born[0].set_color(C.BORN)
        val = MathTex(r"=" + f"{P:.3f}", font_size=40, color=C.BORN).next_to(born, RIGHT, buff=0.2)
        norm = MathTex(r"\int_{-\infty}^{\infty} |\psi(x)|^2\,dx = 1", font_size=34).next_to(born, DOWN, buff=0.3)
        norm.align_to(born, RIGHT)
        hist = label(r"Max Born, 1926: ``the probability is proportional to the square''", font_size=24, color=GREY_B)
        hist.to_edge(DOWN, buff=0.3)
        with self.voiceover(
            "What does the wavefunction mean? Max Born's answer, from 1926: <bookmark mark='b'/> the probability of "
            "finding the electron between a and b is the integral of the length squared, the absolute value of psi, "
            "squared. <bookmark mark='v'/> For this wavefunction and this interval, that's 0.556. <bookmark mark='n'/> "
            "And since the electron is somewhere, the total area must be one."
        ) as vo:
            vo.wait_until("b")
            self.play(Write(born), FadeIn(la), FadeIn(lb), FadeIn(area), FadeIn(hist))
            vo.wait_until("v")
            self.play(Write(val))
            vo.wait_until("n")
            self.play(Write(norm))
        # possible detections, resampled independently each frame
        cdf = np.cumsum(np.abs(psi) ** 2)
        cdf /= cdf[-1]
        k = ValueTracker(0)

        def shots():
            n = int(k.get_value())
            rr = np.random.default_rng(1000 + n)
            xs = np.interp(rr.uniform(size=36), cdf, x)
            ys = rr.uniform(-0.12, 0.12, size=36)
            return VGroup(*[Dot(ax.c2p(xx, 0) + DOWN * (0.55 + yy), radius=0.035, color=C.BORN) for xx, yy in zip(xs, ys)])

        dots = always_redraw(shots)
        dl = note(r"each dot: a possible place to find the electron, drawn from $|\psi|^2$ (fresh dots every frame)")
        dl.next_to(ax, DOWN, buff=0.75)
        with self.voiceover(
            "So the wavefunction doesn't say where the electron is. It says where it might be found. "
            "<bookmark mark='d'/> If we prepared this same state over and over and looked, the places we'd find it "
            "would pile up where the height is large, and never where it's zero. These dots aren't a path the electron "
            "follows; each is just one possible outcome."
        ) as vo:
            self.play(FadeOut(VGroup(area, la, lb)))
            vo.wait_until("d")
            self.add(dots)
            self.play(FadeIn(dl), k.animate.set_value(60), run_time=vo.remaining(), rate_func=linear)
        dots.clear_updaters()
        self.play(FadeOut(VGroup(dots, dl, born, val, norm, hist)))

    # ------------------------------------------------------------------
    def global_phase(self):
        alpha = ValueTracker(0.0)
        wv, psi = self.wv, self.psi
        wv.add_updater(lambda m: m.set_psi(psi * np.exp(1j * alpha.get_value())))
        eq = MathTex(r"\psi(x)", r"\;\to\;", r"e^{i\alpha}\,\psi(x)", font_size=42).to_edge(UP, buff=0.5)
        eq[2][:4].set_color(C.HBAR)
        same = MathTex(r"|e^{i\alpha}\psi|^2 = |\psi|^2", font_size=36, color=C.BORN).next_to(eq, DOWN, buff=0.3)
        dial = VGroup(Circle(radius=0.4, color=GREY_C, stroke_width=1.5))
        dial.next_to(eq, RIGHT, buff=0.6)
        hand = always_redraw(lambda: Line(dial[0].get_center(), dial[0].get_center() + 0.4 * np.array(
            [np.cos(alpha.get_value()), np.sin(alpha.get_value()), 0]), color=C.HBAR, stroke_width=4))
        al = MathTex(r"\alpha", font_size=30, color=C.HBAR).next_to(dial, DOWN, buff=0.1)
        with self.voiceover(
            "Notice what this rule throws away. <bookmark mark='m'/> Multiply the whole wavefunction by the same phase "
            "factor, e to the i alpha. Every arrow turns by the same angle, so every color shifts together, "
            "<bookmark mark='r'/> but every length stays the same, so every probability stays the same. No experiment "
            "can ever detect this overall phase. It's pure bookkeeping."
        ) as vo:
            vo.wait_until("m")
            self.play(Write(eq), FadeIn(dial), FadeIn(hand), FadeIn(al))
            self.play(alpha.animate.set_value(TAU), run_time=4, rate_func=linear)
            vo.wait_until("r")
            self.play(Write(same))
        wv.clear_updaters()
        hand.clear_updaters()
        self.clear_scene()

    # ------------------------------------------------------------------
    def momentum_in_phase(self):
        e = load("extras")
        x, ts = e["trio_x"], e["trio_t"]
        names = ("kp", "k0", "km")
        ks = (1.5, 0.0, -1.5)
        t = ValueTracker(0.0)
        axs, wvs = [], []
        for i, n in enumerate(names):
            ax = wave_axes((-20, 20), (0, 0.3), x_length=11, y_length=1.55).move_to(UP * (2.0 - 2.05 * i) + RIGHT * 0.6)
            wv = WaveView(ax, x, e[f"trio_{n}"][0], mode="density", scale=1.0, x_window=(-20, 20))
            wv.follow(t, frames_at(ts, e[f"trio_{n}"]))
            axs.append(ax)
            wvs.append(wv)
        labs = VGroup(*[MathTex(s, font_size=32, color=C.MOMENTUM).next_to(axs[i], LEFT, buff=0.3)
                        for i, s in enumerate([r"k = +1.5", r"k = 0", r"k = -1.5"])])
        wheel = corner_wheel(corner=UR, buff=0.25, radius=0.32)
        sim = note(r"exact free evolution, $\hbar = m = 1$").to_corner(DR, buff=0.25)
        with self.voiceover(
            "But the phase is far from meaningless when it changes from place to place. Here are three wavefunctions "
            "with exactly the same probability density. <bookmark mark='c'/> The only difference is how the colors "
            "cycle: one winds forward, one doesn't wind at all, one winds backward. Let's let them evolve, "
            "<bookmark mark='g'/> by the equation we're about to build."
        ) as vo:
            self.play(*[Create(a) for a in axs], *[FadeIn(w) for w in wvs], FadeIn(wheel), FadeIn(sim))
            vo.wait_until("g")
            self.play(t.animate.set_value(12), run_time=vo.remaining() + 2.5, rate_func=linear)
        with self.voiceover(
            "They fly apart. The first moves right, the second stays put and spreads, the third moves left. "
            "<bookmark mark='k'/> The rate at which the phase winds, radians per unit length, is called the wave "
            "number, k, <bookmark mark='p'/> and de Broglie's rule says the momentum is h-bar times k. Momentum is "
            "written in the phase."
        ) as vo:
            vo.wait_until("k")
            self.play(FadeIn(labs))
            rule = MathTex(r"p", r"=", r"\hbar k", font_size=48).to_edge(DOWN, buff=0.25).shift(LEFT * 3)
            rule[0].set_color(C.MOMENTUM)
            rule[2].set_color(C.MOMENTUM)
            kk = MathTex(r"k = \frac{d(\arg\psi)}{dx}", font_size=40).next_to(rule, RIGHT, buff=1.0)
            vo.wait_until("p")
            self.play(Write(rule), Write(kk))
        self.wait(0.3)
        for w in wvs:
            w.clear_updaters()
        self.clear_scene()

    # ------------------------------------------------------------------
    def plane_wave(self):
        xs = np.linspace(-5.6, 5.6, 360)
        psi = np.exp(2.2j * xs)
        cols = [hue(np.angle(z)) for z in psi[:-1]]
        proj = Projector(az=-0.62, el=0.32, scale=1.0, center=UP * 1.3)
        hel = self._helix(proj, xs, psi, cols, 1.0, 0.9, list(range(0, 360, 18)), with_axes=False)
        ax = wave_axes((-6, 6), (0, 1.2), x_length=11.2, y_length=1.6).shift(DOWN * 2.1)
        x = np.linspace(-6, 6, 1200)
        wv = WaveView(ax, x, np.exp(2.2j * x), mode="density", scale=0.8)
        eq = MathTex(r"\psi(x) = e^{ikx}", font_size=40).to_corner(UL, buff=0.4)
        props = VGroup(MathTex(r"|\psi|^2 = 1 \text{ everywhere}", font_size=30, color=C.BORN),
                       MathTex(r"p = \hbar k \text{ exactly}", font_size=30, color=C.MOMENTUM)).arrange(DOWN, aligned_edge=LEFT)
        props.next_to(eq, DOWN, buff=0.3, aligned_edge=LEFT)
        wheel = corner_wheel()
        with self.voiceover(
            "The purest case is a wave with a single k: <bookmark mark='h'/> a perfect helix, e to the i k x. "
            "<bookmark mark='d'/> Its density is the same everywhere, and its momentum is exactly h-bar k. But that "
            "means the electron could be anywhere at all. <bookmark mark='q'/> Sharp momentum, no position. Keep that "
            "tension in mind; it's coming back as the uncertainty principle. First, though: how do these arrows move?"
        ) as vo:
            self.play(FadeIn(eq), FadeIn(wheel))
            vo.wait_until("h")
            self.play(FadeIn(hel), run_time=1.5)
            vo.wait_until("d")
            self.play(Create(ax), FadeIn(wv), FadeIn(props))
            vo.wait_until("q")
            self.play(Indicate(props))
        self.wait(0.4)
        self.clear_scene()
