from __future__ import annotations

import math

import numpy as np

from explainer import *  # noqa: F403
from videos.relativity2 import spacetime as st
from videos.relativity2.common import (BHShader, KerrShader, Raster, bh_screen_scale, label, ladder, load, load1, mtex,
                                       note, polyline, redraw, shadow_outline, under)
from videos.relativity2.compute import L_SUN

SPIN, HOR = C.SPIN, C.CURVATURE


class Shadow(VoiceoverScene):
    def construct(self):
        self.orbits()
        self.derive()
        self.morph()
        self.images()
        self.eht()

    # ------------------------------------------------------------------
    def orbits(self):
        d = load("kerr_orbits")
        sp, ip, ir, ep, er = d["spins"], d["isco_pro"], d["isco_retro"], d["eff_pro"], d["eff_retro"]
        assert abs(ep[0] - 0.0572) < 1e-4 and abs(float(d["eff_998"]) - 0.321) < 1e-3
        ax1 = Axes(x_range=[0, 1, 0.25], y_range=[0, 10, 2], x_length=5.2, y_length=3.6, tips=False,
                   axis_config={"stroke_color": GREY_B, "font_size": 20},
                   x_axis_config={"numbers_to_include": [0.25, 0.5, 0.75, 1]},
                   y_axis_config={"numbers_to_include": [2, 4, 6, 8, 10]}).move_to([-3.4, -0.9, 0])
        ax2 = Axes(x_range=[0, 1, 0.25], y_range=[0, 0.45, 0.1], x_length=5.2, y_length=3.6, tips=False,
                   axis_config={"stroke_color": GREY_B, "font_size": 20},
                   x_axis_config={"numbers_to_include": [0.25, 0.5, 0.75, 1]},
                   y_axis_config={"numbers_to_include": [0.1, 0.2, 0.3, 0.4]}).move_to([3.4, -0.9, 0])
        t1 = label(r"innermost stable circular orbit, $r/M$", font_size=24).next_to(ax1, UP, buff=0.15)
        t2 = label(r"efficiency $1 - E_{\rm ISCO}$", font_size=24).next_to(ax2, UP, buff=0.15)
        x1 = label(r"spin $a/M$", font_size=22, color=SPIN).next_to(ax1.x_axis, DOWN, buff=0.35)
        x2 = label(r"spin $a/M$", font_size=22, color=SPIN).next_to(ax2.x_axis, DOWN, buff=0.35)
        c_ip = polyline(ax1, sp, ip, color=SPIN, stroke_width=4)
        c_ir = polyline(ax1, sp, ir, color=GREY_B, stroke_width=3)
        c_ep = polyline(ax2, sp, ep, color=SPIN, stroke_width=4)
        c_er = polyline(ax2, sp, er, color=GREY_B, stroke_width=3)
        l1 = VGroup(label(r"prograde", font_size=20, color=SPIN).next_to(ax1.c2p(0.8, 2.6), DOWN, buff=0.05),
                    label(r"retrograde", font_size=20, color=GREY_B).next_to(ax1.c2p(0.8, 8.6), UP, buff=0.05))
        marks = VGroup(label(r"$6M$, \ 5.7\%", font_size=22).next_to(ax2.c2p(0, 0.057), RIGHT, buff=0.15).shift(UP * 0.15),
                       label(r"$a = 0.998$: 32\%", font_size=22, color=SPIN).next_to(ax2.c2p(0.95, 0.32), LEFT, buff=0.2),
                       label(r"$a \to M$: $r \to M$, 42\%", font_size=22, color=SPIN).next_to(ax2.c2p(1.0, 0.423), LEFT, buff=0.15))
        hdr = mtex(r"r_{\rm ISCO}", r"=", r"M\Big(3 + Z_2 \mp \sqrt{(3 - Z_1)(3 + Z_1 + 2Z_2)}\Big)", font_size=34)
        hdr.to_edge(UP, buff=0.3)
        hl = note(r"Bardeen, Press \& Teukolsky (1972); checked against the minimum of $E(r)$ along circular orbits").next_to(hdr, DOWN, buff=0.1)
        with self.voiceover(
            "Spin also changes how close matter can orbit. <bookmark mark='a'/> In part one we found that around a "
            "non-spinning hole, the innermost stable circular orbit is at six M. Around a spinning one, orbits going "
            "the same way as the spin, prograde, can get much closer: down to M itself for a maximally spinning hole, "
            "while backward orbits are pushed out to nine M. <bookmark mark='b'/> That matters, because gas in an "
            "accretion disk spirals in through these orbits, radiating away its binding energy, until it reaches the "
            "innermost one and plunges. The fraction of its rest mass radiated is one minus the energy of that orbit: "
            "five point seven percent for a non-spinning hole, and up to forty-two percent for a maximally spinning "
            "one. Kip Thorne showed that accretion itself spins holes up to about a equals zero point nine nine eight, "
            "where the efficiency is thirty-two percent: the most efficient engines in the universe."
        ) as vo:
            vo.wait_until("a")
            self.play(FadeIn(hdr), FadeIn(hl), Create(ax1), FadeIn(t1), FadeIn(x1))
            self.play(Create(c_ip), Create(c_ir), FadeIn(l1), run_time=2)
            vo.wait_until("b")
            self.play(Create(ax2), FadeIn(t2), FadeIn(x2))
            self.play(Create(c_ep), Create(c_er), run_time=2)
            self.play(FadeIn(marks, lag_ratio=0.3))
        self.clear_scene()

    # ------------------------------------------------------------------
    def derive(self):
        rows = [
            mtex(r"\Sigma\,\frac{dr}{d\lambda}", r"=", r"\pm\sqrt{R(r)},\quad R = \big(r^2 + a^2 - a\xi\big)^2 - \Delta\big(\eta + (\xi - a)^2\big)",
                 font_size=34),
            mtex(r"R", r"=", r"R' = 0", font_size=40),
            mtex(r"\xi", r"=", r"\frac{r^2(3M - r) - a^2(r + M)}{a(r - M)},\qquad \eta = \frac{r^3\big(4a^2M - r(r - 3M)^2\big)}{a^2(r - M)^2}",
                 font_size=34),
            mtex(r"(\alpha, \beta)", r"=", r"\Big(-\frac{\xi}{\sin i},\ \pm\sqrt{\eta + a^2\cos^2 i - \xi^2\cot^2 i}\Big)", font_size=38),
        ]
        whys = [
            note(r"light rays in Kerr separate, thanks to Carter's constant: $\xi = L/E$, \ $\eta = Q/E^2$"),
            note(r"a light ray that circles forever at fixed $r$: a spherical photon orbit"),
            note(r"for every radius between the prograde and retrograde photon orbits"),
            note(r"where those rays appear on the sky of an observer at inclination $i$: the shadow's edge (Bardeen, 1973)"),
        ]
        rows[3][0].set_color(C.LIGHT)
        under(rows, whys, -1.6)
        step = ladder(self, rows, whys, keep=4, top=2.9, x=-1.6, buff=0.62)
        with self.voiceover(
            "What does a spinning black hole look like? The dark shadow is outlined by light rays that barely escape. "
            "<bookmark mark='a'/> In Kerr, light rays obey a separated radial equation, thanks to a hidden conserved "
            "quantity found by Brandon Carter in 1968. <bookmark mark='b'/> The critical rays are the ones that can "
            "circle forever at a fixed radius, where R and its derivative both vanish. <bookmark mark='c'/> Solving "
            "those two equations gives the ray's constants for every radius between the prograde and retrograde photon "
            "orbits. <bookmark mark='d'/> And each pair of constants marks one point on the sky of a distant observer. "
            "Together, they trace the edge of the shadow, as James Bardeen worked out in 1973."
        ) as vo:
            vo.wait_until("a")
            step(0)
            vo.wait_until("b")
            step(1)
            vo.wait_until("c")
            step(2)
            vo.wait_until("d")
            step(3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def morph(self):
        d = load("shadows")
        spins, curves = d["spins"], d["curves_90"]
        cen = np.array([0.0, -0.3, 0])
        sc = 0.42
        k = ValueTracker(0.0)

        def outline():
            x = k.get_value() * (len(spins) - 1)
            i = min(int(x), len(spins) - 2)
            f = x - i
            Cc = (1 - f) * curves[i] + f * curves[i + 1]
            P = np.stack([cen[0] + sc * Cc[:, 0], cen[1] + sc * Cc[:, 1], 0 * Cc[:, 0]], 1)
            g = VGroup(Polygon(*P, stroke_color=C.LIGHT, stroke_width=4, fill_color=BLACK, fill_opacity=1))
            return g

        O = redraw(outline)
        ref = DashedVMobject(Circle(radius=sc * math.sqrt(27), color=GREY_C, stroke_width=2).move_to(cen), num_dashes=60)
        axh = Line(cen + LEFT * 3.4, cen + RIGHT * 3.6, color=GREY_D, stroke_width=1.5)
        axv = Line(cen + DOWN * 2.6, cen + UP * 2.6, color=GREY_D, stroke_width=1.5)
        rd = VGroup(mtex(r"a/M =", font_size=32, color=SPIN), DecimalNumber(0.0, num_decimal_places=3, font_size=32,
                                                                             color=SPIN)).arrange(RIGHT, buff=0.12)
        rd.to_corner(UL, buff=0.4)
        rd[1].add_updater(lambda m: m.set_value(float(np.interp(k.get_value() * (len(spins) - 1), np.arange(len(spins)), spins))))
        notes = VGroup(label(r"seen edge-on ($i = 90^\circ$)", font_size=24),
                       label(r"dashed: $a = 0$, radius $\sqrt{27}\,M$", font_size=22, color=GREY_B),
                       label(r"left: photons orbiting \emph{with} the spin", font_size=22, color=SPIN),
                       label(r"get closer, so the edge flattens", font_size=22, color=SPIN)).arrange(DOWN, aligned_edge=LEFT, buff=0.1)
        notes.to_corner(UR, buff=0.4)
        with self.voiceover(
            "Here's that edge for a black hole seen edge-on. <bookmark mark='a'/> Without spin, it's a circle, of radius "
            "the square root of twenty-seven M, as we found in part one. <bookmark mark='b'/> Spin it up. Photons "
            "orbiting with the rotation can get closer before being captured, so on that side the edge moves in and "
            "flattens, while the other side bulges out. Near maximal spin, the shadow becomes a letter D."
        ) as vo:
            self.add(axh, axv, ref, O)
            self.play(FadeIn(rd), FadeIn(notes[:2]))
            vo.wait_until("b")
            self.play(FadeIn(notes[2:]), k.animate.set_value(1.0), run_time=6, rate_func=smooth)
        O.clear_updaters()
        rd[1].clear_updaters()
        self.clear_scene()

    # ------------------------------------------------------------------
    def images(self):
        kd = load("kerr80")
        assert int(kd["mismatch"]) == 0
        ks = KerrShader(kd)
        ss = KerrShader(load("kerr80_0"))
        t = ValueTracker(0.0)
        W = 6.8
        H = W * 720 / 1280
        cl, cr = np.array([-3.5, 0.4, 0]), np.array([3.5, 0.4, 0])
        left = Raster(lambda v: ss(v), t, W, H, center=cl)
        right = Raster(lambda v: ks(v), t, W, H, center=cr)
        ll = label(r"no spin", font_size=28).next_to(left, DOWN, buff=0.2)
        rl = label(r"$a = 0.99M$", font_size=28, color=SPIN).next_to(right, DOWN, buff=0.2)
        sc = bh_screen_scale(W)
        o_l = shadow_outline(0.0005, 80, cl, sc, color=HOR, stroke_width=2.5)
        o_r = shadow_outline(0.99, 80, cr, sc, color=HOR, stroke_width=2.5)
        same = note(r"both: thin disk out to $26M$ seen from $80^\circ$, 100M away; every ray an integrated null geodesic").to_edge(DOWN, buff=0.6)
        chk = label(r"Bardeen's analytic edge (lilac) matches the ray-traced shadow, pixel for pixel", font_size=24,
                    color=HOR).to_edge(DOWN, buff=0.25)
        with self.voiceover(
            "Now the full picture, ray-traced. <bookmark mark='a'/> On the left, a non-spinning black hole, like part "
            "one's; on the right, the same disk and camera around a hole spinning at ninety-nine percent of the maximum. "
            "<bookmark mark='b'/> The disk reaches much closer in, because the innermost orbit has moved in, and the "
            "approaching side is brighter still, because the gas there moves faster. <bookmark mark='c'/> Overlay "
            "Bardeen's analytic shadow edge: it's exactly the boundary of the rays our tracer sees captured, pixel for "
            "pixel."
        ) as vo:
            self.add(left, right)
            self.play(FadeIn(ll), FadeIn(rl), FadeIn(same), t.animate.set_value(20), run_time=2, rate_func=linear)
            vo.wait_until("b")
            self.play(t.animate.set_value(60), run_time=vo.until("c"), rate_func=linear)
            vo.wait_until("c")
            self.play(Create(o_l), Create(o_r), FadeIn(chk), t.animate.set_value(80), run_time=2, rate_func=linear)
            self.play(t.animate.set_value(110), run_time=vo.remaining() + 0.5, rate_func=linear)
        left.clear_updaters()
        right.clear_updaters()
        self.clear_scene()
        # face-on
        kd2 = load("kerr20")
        assert int(kd2["mismatch"]) == 0
        ks2 = KerrShader(kd2)
        ss2 = KerrShader(load("kerr20_0"))
        t2 = ValueTracker(0.0)
        left = Raster(lambda v: ss2(v), t2, W, H, center=cl)
        right = Raster(lambda v: ks2(v), t2, W, H, center=cr)
        ll = label(r"no spin, $20^\circ$", font_size=28).next_to(left, DOWN, buff=0.2)
        rl = label(r"$a = 0.99M$, $20^\circ$", font_size=28, color=SPIN).next_to(right, DOWN, buff=0.2)
        o_r2 = shadow_outline(0.99, 20, cr, sc, color=HOR, stroke_width=2.5)
        o_l2 = shadow_outline(0.0005, 20, cl, sc, color=HOR, stroke_width=2.5)
        txt = note(r"seen nearly face-on, as we see M87* (about $17^\circ$): the shadow is almost round either way").to_edge(DOWN, buff=0.35)
        with self.voiceover(
            "<bookmark mark='a'/> Seen nearly face-on, which is roughly how we see the black hole in M87, the shadow "
            "is almost round whatever the spin, and its size changes by less than seven percent. That makes the "
            "shadow a good way to weigh a black hole, and a hard way to measure its spin."
        ) as vo:
            self.add(left, right)
            self.play(FadeIn(ll), FadeIn(rl), t2.animate.set_value(20), run_time=2, rate_func=linear)
            self.play(Create(o_l2), Create(o_r2), FadeIn(txt), t2.animate.set_value(50), run_time=2, rate_func=linear)
            self.play(t2.animate.set_value(90), run_time=vo.remaining() + 0.5, rate_func=linear)
        left.clear_updaters()
        right.clear_updaters()
        self.clear_scene()

    # ------------------------------------------------------------------
    def eht(self):
        # shadow angular diameter of M87*: 2 sqrt(27) GM/(c^2 D), M = 6.5e9 Msun, D = 16.8 Mpc
        D = 16.8 * 3.085_677_581e22
        theta = 2 * math.sqrt(27) * 6.5e9 * L_SUN / D * 180 / math.pi * 3600 * 1e6
        assert abs(theta - 39.7) < 0.3
        # spin barely changes the size seen face-on: widths for a = 0 and 0.99 at 17 degrees
        w0 = 2 * math.sqrt(27)
        al, be = st.shadow_curve(0.99, math.radians(17), 800)
        w1 = 0.5 * ((al.max() - al.min()) + (be.max() - be.min()))
        assert 0.06 < abs(w1 / w0 - 1) < 0.08  # 7% smaller at a = 0.99
        rows = VGroup(
            mtex(r"\theta_{\rm shadow}", r"=", r"\frac{2\sqrt{27}\,GM}{c^2 D}", font_size=42),
            label(r"M87*: \ $M = 6.5\times10^9\,M_\odot$, \ $D = 16.8$ Mpc \ $\Rightarrow$ \ $\theta \approx 40\ \mu$as", font_size=30),
            label(r"Event Horizon Telescope (2019): a bright ring of $42 \pm 3\ \mu$as around a dark center", font_size=28,
                  color=C.LIGHT),
            label(rf"(seen face-on, a spin of $0.99M$ shrinks it by only {abs(w1 / w0 - 1) * 100:.0f}\%)",
                  font_size=24, color=GREY_A),
            label(r"Sagittarius A* (2022): $51.8 \pm 2.3\ \mu$as for $4\times10^6\,M_\odot$ at 8 kpc", font_size=28, color=C.LIGHT),
            label(r"both consistent with Kerr; models favor spinning holes, but neither spin is yet measured", font_size=24,
                  color=GREY_A),
        ).arrange(DOWN, buff=0.28)
        rows[0][0].set_color(C.LIGHT)
        with self.voiceover(
            "<bookmark mark='a'/> For the black hole in the galaxy M87, six and a half billion solar masses, fifty-five "
            "million light-years away, the shadow should span about forty micro-arcseconds. <bookmark mark='b'/> In "
            "2019, the Event Horizon Telescope, a planet-sized array of radio dishes, imaged a bright ring forty-two "
            "micro-arcseconds across, around a dark center. <bookmark mark='c'/> In 2022 it imaged Sagittarius A star, "
            "at the center of our own galaxy. Both are consistent with Kerr black holes; models of the glowing gas favor "
            "spinning ones, but neither spin has been pinned down yet."
        ) as vo:
            vo.wait_until("a")
            self.play(Write(rows[0]), FadeIn(rows[1]))
            vo.wait_until("b")
            self.play(FadeIn(rows[2:4], lag_ratio=0.3))
            vo.wait_until("c")
            self.play(FadeIn(rows[4:], lag_ratio=0.3))
        self.clear_scene()
