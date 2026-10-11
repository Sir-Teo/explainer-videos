from __future__ import annotations

import math

import numpy as np

from explainer import *  # noqa: F403
from videos.relativity2.common import (clamp_x, clipped, label, ladder, load, mtex, note, polyline, redraw, under)

LAM, MAT, MET, CURV = C.LAMBDA, C.MATTER, C.METRIC, C.CURVATURE
HOR_P, HOR_E, HUB = C.SPIN, C.CURVATURE, C.PROPER_TIME


class Horizons(VoiceoverScene):
    def construct(self):
        self.co = load("cosmo2")
        self.redshift()
        self.diagram()
        self.cmb()
        self.status()

    # ------------------------------------------------------------------
    def redshift(self):
        rows = [
            mtex(r"0", r"=", r"-dt^2 + a(t)^2d\chi^2\quad\Rightarrow\quad d\chi = \frac{dt}{a}", font_size=40),
            mtex(r"\int_{t_e}^{t_o}\frac{dt}{a}", r"=", r"\int_{t_e + \delta t_e}^{t_o + \delta t_o}\frac{dt}{a}", font_size=40),
            mtex(r"\frac{\delta t_e}{a(t_e)}", r"=", r"\frac{\delta t_o}{a(t_o)}", font_size=42),
            mtex(r"1 + z", r"\equiv", r"\frac{\lambda_o}{\lambda_e} = \frac{a(t_o)}{a(t_e)}", font_size=46),
        ]
        whys = [
            note(r"light moving radially (flat space, $k = 0$; $\chi$: comoving distance)"),
            note(r"two successive crests travel the same comoving distance"),
            note(r"so the time between them grows with the scale factor"),
            note(r"light is stretched exactly as much as the universe expanded while it traveled"),
        ]
        rows[3][0].set_color(C.LIGHT)
        rows[3][2].set_color(MET)
        under(rows, whys, -0.6)
        step = ladder(self, rows, whys, keep=4, top=3.0, x=-0.6, buff=0.6)
        # a wave crossing an expanding grid (illustrative a(t) = 1 + t)
        k = ValueTracker(0.0)
        y0 = -2.85

        def wave():
            s = k.get_value()
            a = 1 + 1.5 * s
            g = VGroup()
            for xc in np.arange(-6, 6.01, 1.0):
                g.add(Line([xc * a / 2.5, y0 - 0.5, 0], [xc * a / 2.5, y0 + 0.5, 0], color=GREY_D, stroke_width=1))
            x_front = -5.5 + 10.5 * s
            xs = np.linspace(x_front - 2.2 * a / 1.6, x_front, 200)
            env = np.exp(-((xs - (x_front - 1.1 * a / 1.6)) / (0.6 * a / 1.6)) ** 2)
            ys = y0 + 0.4 * env * np.sin(2 * np.pi * (xs - x_front) / (0.45 * a))
            g.add(VMobject(stroke_color=C.LIGHT, stroke_width=3).set_points_smoothly(np.stack([xs, ys, 0 * xs], 1)))
            return g

        W = redraw(wave)
        cap = note(r"schematic: the wave and the comoving grid stretch together").to_corner(DR, buff=0.15)
        with self.voiceover(
            "How do we know the universe expands? Through light. <bookmark mark='a'/> A light ray moving through "
            "flat, expanding space covers a comoving distance d t over a in each moment. <bookmark mark='b'/> Two "
            "successive crests of a light wave, sent a moment apart, travel the same comoving distance. "
            "<bookmark mark='c'/> So the interval between them grows in proportion to the scale factor. "
            "<bookmark mark='d'/> The wavelength stretches by exactly the factor the universe expanded while the light "
            "was in flight. That's the cosmological redshift: not a Doppler shift through space, but space itself "
            "stretching the wave."
        ) as vo:
            vo.wait_until("a")
            step(0)
            vo.wait_until("b")
            step(1)
            vo.wait_until("c")
            step(2)
            vo.wait_until("d")
            step(3)
            self.add(W)
            self.play(FadeIn(cap), k.animate.set_value(1.0), run_time=max(vo.remaining(), 4), rate_func=linear)
        W.clear_updaters()
        self.clear_scene()

    # ------------------------------------------------------------------
    def diagram(self):
        co = self.co
        tg, ag, etag = co["tg"], co["ag"], co["etag"]
        part, event, hub, cone = co["particle_com"], co["event_com"], co["hubble_com"], co["cone_com"]
        age, eta0 = float(co["age"]), float(co["eta0"])
        assert abs(age - 13.79) < 0.02 and abs(eta0 - 46.1) < 0.2
        assert abs(float(co["event_now"]) - 16.7) < 0.1 and abs(float(co["hubble_now"]) - 14.5) < 0.05
        X, Tmax, Emax = 60.0, 30.0, 63.0
        s = ValueTracker(0.0)  # 0: proper distance vs t; 1: comoving vs t; 2: comoving vs conformal time
        m = tg <= Tmax

        def scr(chi, idx):
            """Screen points of a curve given by comoving distance chi(t) on the time grid (indices idx)."""
            sv = s.get_value()
            t, a, eta = tg[idx], ag[idx], etag[idx]
            P0 = np.stack([a * chi / X * 5.6, -3.0 + t / Tmax * 5.9, 0 * t], 1)
            P1 = np.stack([chi / X * 5.6, -3.0 + t / Tmax * 5.9, 0 * t], 1)
            P2 = np.stack([chi / X * 5.6, -3.0 + eta / Emax * 5.9, 0 * t], 1)
            if sv <= 1:
                return (1 - sv) * P0 + sv * P1
            return (2 - sv) * P1 + (sv - 1) * P2

        idx_all = np.nonzero(m)[0]
        idx_now = np.nonzero(tg <= age)[0]

        def curves():
            g = VGroup()
            box = (-6.0, 6.0, -3.05, 3.0)
            for chi0 in (10, 20, 30, 40, 50):  # comoving galaxies
                for sg in (1, -1):
                    g.add(clipped(scr(np.full(len(idx_all), sg * chi0), idx_all), color=GREY_D, stroke_width=1.2, box=box))
            for sg in (1, -1):
                g.add(clipped(scr(sg * hub[idx_all], idx_all), color=HUB, stroke_width=3, box=box))
                g.add(clipped(scr(sg * part[idx_all], idx_all), color=HOR_P, stroke_width=3, box=box))
                g.add(clipped(scr(sg * event[idx_all], idx_all), color=HOR_E, stroke_width=3, box=box))
                g.add(clipped(scr(sg * cone[idx_now], idx_now), color=C.LIGHT, stroke_width=4.5, box=box))
            # "now"
            j = int(np.argmin(np.abs(tg - age)))
            P = scr(np.array([-X, X]), np.array([j, j]))
            g.add(DashedLine(P[0], P[1], color=GREY_B, stroke_width=1.5))
            g.add(Dot(scr(np.array([0.0]), np.array([j]))[0], radius=0.07, color=WHITE))
            return g

        G = redraw(curves)
        xlab = always_redraw(lambda: label(r"proper distance (Gly)" if s.get_value() < 0.5 else r"comoving distance (Gly)",
                                           font_size=22).move_to([0, -3.55, 0]))
        ylab = always_redraw(lambda: label(r"time (Gyr)" if s.get_value() < 1.5 else r"conformal time $\eta$ (Gly)",
                                           font_size=22).move_to([-6.25, 3.15, 0]).shift(RIGHT * 0.5))
        leg = VGroup(label(r"our past light cone", font_size=22, color=C.LIGHT),
                     label(r"Hubble sphere, $c/H$", font_size=22, color=HUB),
                     label(r"particle horizon", font_size=22, color=HOR_P),
                     label(r"event horizon", font_size=22, color=HOR_E),
                     label(r"galaxies (fixed comoving distance)", font_size=22, color=GREY_B),
                     label(r"now", font_size=22, color=GREY_B)).arrange(DOWN, aligned_edge=LEFT, buff=0.06).to_corner(UR, buff=0.2)
        leg.add_background_rectangle(color=BACKGROUND, opacity=0.85, buff=0.08)
        cap = note(r"computed: flat $\Lambda$CDM, Planck 2018 (after Davis \& Lineweaver 2004)").to_corner(UL, buff=0.2)
        nums = VGroup(label(rf"today: particle horizon {eta0:.0f} Gly, event horizon {float(co['event_now']):.1f} Gly, "
                            rf"Hubble sphere {float(co['hubble_now']):.1f} Gly", font_size=22)).to_edge(DOWN, buff=0.05)
        nums.shift(UP * 0.0)
        with self.voiceover(
            "Expansion makes distances and horizons subtle, and one picture sorts them out. <bookmark mark='a'/> Time "
            "goes up, distance from us across, computed for our universe. Galaxies drift apart along these grey lines. "
            "Our past light cone, everything we can see now, is this yellow teardrop: light that reaches us from the "
            "most distant sources was emitted when those sources were close to us, and the expansion then carried the "
            "light away before it could make headway toward us. <bookmark mark='b'/> The teal curve is the Hubble "
            "sphere, where galaxies recede at the speed of light. Galaxies beyond it recede faster than light, and we "
            "still see many of them: nothing moves faster than light locally; space between us is expanding."
        ) as vo:
            vo.wait_until("a")
            self.add(G)
            self.play(FadeIn(leg), FadeIn(cap), FadeIn(xlab), FadeIn(ylab))
            vo.wait_until("b")
            self.play(Indicate(leg[2], color=HUB))
        with self.voiceover(
            "<bookmark mark='c'/> Now divide out the expansion, and use comoving distance. <bookmark mark='d'/> And "
            "finally, replace time by conformal time, the distance light could have traveled. "
            "<bookmark mark='e'/> In these coordinates, light moves at forty-five degrees again, like in a Penrose "
            "diagram. The particle horizon, the farthest anything we see could be today, is forty-six billion "
            "light-years away. And the event horizon: events beyond it today, sixteen and a half billion light-years "
            "away, will never be seen by us, because the expansion is accelerating."
        ) as vo:
            vo.wait_until("c")
            self.play(s.animate.set_value(1.0), run_time=4, rate_func=smooth)
            vo.wait_until("d")
            self.play(s.animate.set_value(2.0), run_time=4, rate_func=smooth)
            vo.wait_until("e")
            self.play(FadeIn(nums))
        G.clear_updaters()
        xlab.clear_updaters()
        ylab.clear_updaters()
        self.clear_scene()

    # ------------------------------------------------------------------
    def cmb(self):
        co = self.co
        D, eta_ls, th = float(co["D_ls"]), float(co["eta_ls"]), float(co["theta_h"])
        t_ls = float(co["t_ls"])
        assert abs(D - 45.2) < 0.2 and abs(eta_ls - 0.91) < 0.02 and abs(th - 1.16) < 0.02
        cen = np.array([-2.6, -0.4, 0])
        sc = 3.1 / D
        sky = Circle(radius=D * sc, color=C.LIGHT, stroke_width=4).move_to(cen)
        us = Dot(cen, radius=0.08, color=WHITE)
        usl = label(r"us", font_size=22).next_to(us, DOWN, buff=0.08)
        p1, p2 = cen + D * sc * LEFT, cen + D * sc * RIGHT
        c1 = Circle(radius=eta_ls * sc, color=HOR_P, stroke_width=3, fill_color=HOR_P, fill_opacity=0.6).move_to(p1)
        c2 = Circle(radius=eta_ls * sc, color=HOR_P, stroke_width=3, fill_color=HOR_P, fill_opacity=0.6).move_to(p2)
        lines = VGroup(DashedLine(cen, p1, color=GREY_C, stroke_width=1.5), DashedLine(cen, p2, color=GREY_C, stroke_width=1.5))
        lab = label(r"the last-scattering surface, $z = 1090$", font_size=22, color=C.LIGHT).next_to(sky, UP, buff=0.1)
        facts = VGroup(
            label(rf"emitted $\approx {round(t_ls, -4) / 1e3:.0f}{{,}}000$ years after the Big Bang", font_size=24, color=C.LIGHT),
            label(rf"now {D:.1f} billion light-years away (comoving)", font_size=24),
            label(rf"each region's horizon then: {eta_ls:.2f} Gly (comoving)", font_size=24, color=HOR_P),
            mtex(rf"\theta_H = \frac{{\eta_{{\rm ls}}}}{{D}} \approx {th:.2f}^\circ", font_size=36, color=HOR_P),
            label(r"so the sky holds $\sim 10^4$ regions that never", font_size=24),
            label(r"exchanged a signal before the light left \dots", font_size=24),
            label(r"\dots yet the CMB is the same temperature,", font_size=24, color=C.LIGHT),
            label(r"2.725 K, to one part in $10^5$, in every direction", font_size=24, color=C.LIGHT),
            label(r"the horizon problem; inflation (Guth 1981) is the leading proposal", font_size=22, color=GREY_A),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.12).move_to([3.7, -0.2, 0])
        scl = note(r"to scale, comoving distances").next_to(sky, DOWN, buff=0.15)
        with self.voiceover(
            "The farthest light we can see is the cosmic microwave background, released when the universe became "
            "transparent, a few hundred thousand years after the Big Bang. <bookmark mark='a'/> The places that emitted "
            "it now lie on a sphere forty-five billion light-years away. <bookmark mark='b'/> But at the moment of "
            "emission, each of those places could only have received signals from a tiny region, drawn here to scale: "
            "about a degree across, as seen from Earth. <bookmark mark='c'/> So the sky contains some ten thousand "
            "patches that had never been in causal contact. Yet they all have the same temperature, to one part in a "
            "hundred thousand. How did they know? This is the horizon problem, and the leading proposed answer, "
            "inflation, adds an early epoch of exponential expansion, before the history we've drawn."
        ) as vo:
            self.play(Create(sky), FadeIn(us), FadeIn(usl), FadeIn(lab), FadeIn(scl))
            vo.wait_until("a")
            self.play(Create(lines), FadeIn(facts[:2]))
            vo.wait_until("b")
            self.play(GrowFromCenter(c1), GrowFromCenter(c2), FadeIn(facts[2:4]))
            vo.wait_until("c")
            self.play(FadeIn(facts[4:], lag_ratio=0.2), run_time=3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def status(self):
        rows = VGroup(
            label(r"Open questions, as of 2026", font_size=36),
            label(r"the expansion rate today, $H_0$ (km/s/Mpc):", font_size=28),
            label(r"from the CMB (Planck, ACT, SPT, assuming $\Lambda$CDM): \ $67.2 \pm 0.4$", font_size=26, color=MET),
            label(r"from nearby supernovae and Cepheids (SH0ES and others): \ $73.5 \pm 0.8$", font_size=26, color=C.LIGHT),
            label(r"a 5--7$\sigma$ disagreement, the ``Hubble tension''", font_size=26, color=GREY_A),
            label(r"dark energy: DESI's galaxy maps hint that it changes with time", font_size=28),
            label(r"(about 3--4$\sigma$; not yet the $5\sigma$ physicists require)", font_size=24, color=GREY_A),
        ).arrange(DOWN, buff=0.22)
        rows[1:5].shift(RIGHT * 0.0)
        with self.voiceover(
            "These equations are still being tested at the largest scales. <bookmark mark='a'/> The expansion rate "
            "inferred from the microwave background, assuming this model, is about sixty-seven kilometers per second "
            "per megaparsec. Measured directly from nearby supernovae, it's about seventy-three and a half. The "
            "disagreement, now at five to seven sigma, is called the Hubble tension. <bookmark mark='b'/> And maps of "
            "millions of galaxies from the DESI survey hint that dark energy may change over time, which a "
            "cosmological constant can't. The evidence isn't yet decisive, and DESI's full results are expected in "
            "2027."
        ) as vo:
            self.play(FadeIn(rows[0]))
            vo.wait_until("a")
            self.play(FadeIn(rows[1:5], lag_ratio=0.3), run_time=3)
            vo.wait_until("b")
            self.play(FadeIn(rows[5:], lag_ratio=0.3))
        self.clear_scene()
