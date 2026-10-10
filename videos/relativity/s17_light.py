from __future__ import annotations

import math
from pathlib import Path

import numpy as np

from explainer import *  # noqa: F403
from videos.relativity.common import redraw, BHShader, Raster, boxed, label, ladder, load, mtex, note, stack

EHT = Path(__file__).resolve().parent / "data" / "eht_m87.jpg"
NEWTON = C.GRAV_POTENTIAL
EINSTEIN = C.CURVATURE


class Light(VoiceoverScene):
    def construct(self):
        self.derive()
        self.halves()
        self.eclipse()
        self.fan()
        self.image()

    # ------------------------------------------------------------------
    def derive(self):
        title = label(r"Light rays: null geodesics", font_size=36).to_corner(UL, buff=0.4)
        rows = [
            mtex(r"\frac{d^2u}{d\phi^2} + u", r"=", r"\frac{3GM}{c^2}\,u^2", font_size=40),
            mtex(r"u_0", r"=", r"\frac{\sin\phi}{b}", font_size=40),
            mtex(r"u", r"\approx", r"\frac{\sin\phi}{b} + \frac{GM}{c^2b^2}\big(1 + \cos^2\phi\big)", font_size=40),
            mtex(r"0", r"=", r"-\frac{\delta}{2b} + \frac{2GM}{c^2 b^2}", font_size=40),
            mtex(r"\delta", r"=", r"\frac{4GM}{c^2 b}", font_size=50),
        ]
        whys = [
            note(r"the orbit equation with $\ell\to\infty$ (massless): no Newton term", font_size=22),
            note(r"zeroth order: a straight line at distance $b$", font_size=22),
            note(r"first order: solve with $u_0$ in the small term", font_size=22),
            note(r"far away, $u = 0$ at $\phi = -\delta/2$", font_size=22),
            note(r"total deflection", font_size=22),
        ]
        rows[0][2].set_color(EINSTEIN)
        rows[2][2].set_color(EINSTEIN)
        rows[4][0].set_color(C.LIGHT)
        rows[4][2].set_color(EINSTEIN)
        x0 = -1.2
        for r, w in zip(rows, whys):
            r.shift((x0 - r[1].get_center()[0]) * RIGHT)
            w.next_to(r, DOWN, buff=0.08).align_to(r, RIGHT)
        step = ladder(self, rows, whys, keep=4, top=2.4, x=x0, buff=0.62)
        with self.voiceover(
            "Light follows geodesics too: null geodesics, along which the interval is zero. <bookmark mark='a'/> The same "
            "derivation as for planets gives the orbit equation without the Newtonian term, because light has no rest "
            "mass. <bookmark mark='b'/> Without the right-hand side, the solution is a straight line passing at distance "
            "b, the impact parameter. <bookmark mark='c'/> Put that line into the small term and solve again: the ray "
            "picks up a correction that bends it toward the mass."
        ) as vo:
            self.play(FadeIn(title))
            vo.wait_until("a")
            step(0)
            vo.wait_until("b")
            step(1)
            vo.wait_until("c")
            step(2)
        with self.voiceover(
            "<bookmark mark='d'/> Far from the mass, u goes to zero. Without bending, that happens at phi equals zero; "
            "with it, at a small negative angle, half the deflection. <bookmark mark='e'/> Solving: the total deflection "
            "is four G M over c squared b."
        ) as vo:
            vo.wait_until("d")
            step(3)
            vo.wait_until("e")
            step(4)
            self.play(Circumscribe(rows[4], color=C.LIGHT))
        self.clear_scene()

    # ------------------------------------------------------------------
    def halves(self):
        lt = load("light")
        d = float(lt["sun_exact"])
        assert abs(d - 1.751) < 0.001
        sun = mtex(r"\text{grazing the Sun: } b = R_\odot", r"\ \Rightarrow\ ", r"\delta = 1.75''", font_size=44)
        sun[2].set_color(C.LIGHT)
        sun.to_edge(UP, buff=0.6)
        unit = 3.4
        bar_t = Rectangle(width=unit, height=0.6, stroke_width=0, fill_color=C.PROPER_TIME, fill_opacity=0.85)
        bar_s = Rectangle(width=unit, height=0.6, stroke_width=0, fill_color=C.METRIC, fill_opacity=0.85)
        bars = VGroup(bar_t, bar_s).arrange(RIGHT, buff=0).move_to(UP * 0.6)
        lt_ = label(r"warped time ($g_{tt}$): $0.875''$", font_size=26, color=C.PROPER_TIME).next_to(bar_t, DOWN, buff=0.2)
        ls_ = label(r"warped space ($g_{rr}$): $0.875''$", font_size=26, color=C.METRIC).next_to(bar_s, DOWN, buff=0.2)
        e11 = VGroup(
            label(r"Einstein, 1911, with the equivalence principle alone: $0.83''$", font_size=28, color=NEWTON),
            label(r"(the same as a Newtonian ``corpuscle'' of light, Soldner 1801)", font_size=24, color=GREY_A),
        ).arrange(DOWN, buff=0.12).next_to(VGroup(lt_, ls_), DOWN, buff=0.6)
        why = label(r"Slow planets only feel warped time. Light, moving at $c$, feels both equally.", font_size=28,
                    color=GREY_A).to_edge(DOWN, buff=0.45)
        with self.voiceover(
            "<bookmark mark='s'/> For a ray grazing the Sun, that's one point seven five arcseconds. <bookmark mark='h'/> "
            "And here's a beautiful detail. Half of that comes from the warping of time, the part we found with clocks. "
            "<bookmark mark='p'/> The other half comes from the warping of space. <bookmark mark='e'/> In 1911, using "
            "only the equivalence principle, Einstein predicted the first half alone: about point eight arcseconds, the "
            "same as Newtonian physics would give for a particle moving at the speed of light. <bookmark mark='w'/> Slow "
            "objects feel only the warping of time. Light moves as fast through space as through time, and feels both. So "
            "measuring light bending tests whether space is curved."
        ) as vo:
            vo.wait_until("s")
            self.play(Write(sun))
            vo.wait_until("h")
            self.play(GrowFromEdge(bar_t, LEFT), FadeIn(lt_))
            vo.wait_until("p")
            self.play(GrowFromEdge(bar_s, LEFT), FadeIn(ls_))
            vo.wait_until("e")
            self.play(FadeIn(e11))
            vo.wait_until("w")
            self.play(FadeIn(why))
        self.clear_scene()

    # ------------------------------------------------------------------
    def eclipse(self):
        rng = np.random.default_rng(19)
        center = np.array([-2.6, -0.2, 0])
        R = 0.85
        corona = VGroup(*[Circle(radius=R * (1 + 0.12 * i), stroke_width=0, fill_color=GOLD_A,
                                 fill_opacity=0.10 / (i + 1)).move_to(center) for i in range(6)])
        moon = Circle(radius=R, color=GREY_D, fill_color=BLACK, fill_opacity=1, stroke_width=2).move_to(center)
        stars = []
        while len(stars) < 22:
            p = rng.uniform(-3.2, 3.2, 2)
            if 1.35 * R < np.linalg.norm(p) < 3.3:
                stars.append(p)
        stars = np.array(stars)
        k = ValueTracker(0.0)
        boost = 0.45  # display exaggeration: shift (screen units) at the solar limb

        def field():
            g = VGroup()
            for p in stars:
                rr = np.linalg.norm(p)
                shift = boost * R / rr * p / rr * k.get_value()
                q = center + np.array([*(p + shift), 0])
                g.add(Dot(center + np.array([*p, 0]), radius=0.04, color=GREY_C))
                g.add(Dot(q, radius=0.06, color=WHITE))
                if k.get_value() > 0.02:
                    g.add(Line(center + np.array([*p, 0]), q, color=C.LIGHT, stroke_width=2))
            return g

        fm = redraw(field)
        exag = boost / R * 959.6 / 1.751  # the Sun's angular radius is ~960 arcseconds
        assert 250 < exag < 330
        lab = note(rf"schematic star field; displacements $\propto 1/b$, exaggerated $\sim {round(exag, -1):.0f}\times$").to_corner(DL, buff=0.3)
        res = VGroup(
            label(r"Total eclipse, 29 May 1919", font_size=32),
            label(r"Sobral, Brazil (Crommelin, Davidson):", font_size=26, color=GREY_A),
            mtex(r"1.98'' \pm 0.12''", font_size=34, color=C.LIGHT),
            label(r"Príncipe (Eddington, Cottingham):", font_size=26, color=GREY_A),
            mtex(r"1.61'' \pm 0.30''", font_size=34, color=C.LIGHT),
            label(r"announced 6 November 1919", font_size=26, color=GREY_A),
            label(r"today: radio interferometry confirms GR to $10^{-4}$", font_size=26),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.18).to_edge(RIGHT, buff=0.6)
        with self.voiceover(
            "To see starlight grazing the Sun, you need the Sun's light blocked: a total eclipse. <bookmark mark='a'/> "
            "Photograph the stars around the eclipsed Sun, and compare with photographs of the same stars at night, months "
            "later. <bookmark mark='b'/> Each star should appear pushed away from the Sun, by an amount inversely "
            "proportional to its distance from it. <bookmark mark='c'/> In 1919, two British expeditions, to Sobral in "
            "Brazil and the island of Príncipe off Africa, measured one point nine eight and one point six one "
            "arcseconds, with uncertainties of a few tenths. <bookmark mark='d'/> The announcement in London that "
            "November made Einstein world famous overnight. Today, radio telescopes confirm the prediction to one part in "
            "ten thousand."
        ) as vo:
            vo.wait_until("a")
            self.play(FadeIn(corona), FadeIn(moon))
            self.add(fm)
            self.play(FadeIn(lab))
            vo.wait_until("b")
            self.play(k.animate.set_value(1.0), run_time=2.5)
            vo.wait_until("c")
            self.play(FadeIn(res[:5], lag_ratio=0.2), run_time=2)
            vo.wait_until("d")
            self.play(FadeIn(res[5:], lag_ratio=0.3))
        fm.clear_updaters()
        self.clear_scene()

    # ------------------------------------------------------------------
    def fan(self):
        lt = load("light")
        fan, cap, bs = lt["fan"], lt["fan_captured"], lt["fan_b"]
        bc = float(lt["bc"])
        assert abs(bc - 2.598) < 1e-3 and np.all(cap == (bs < bc))
        sc = 0.42
        center = np.array([0.6, -0.3, 0])
        hole = Circle(radius=sc, color=BLACK, fill_color=BLACK, fill_opacity=1, stroke_color=GREY_C, stroke_width=2).move_to(center)
        ps = DashedVMobject(Circle(radius=1.5 * sc, color=C.CURVATURE, stroke_width=2.5).move_to(center), num_dashes=36)
        rays = VGroup()
        for P, c_ in zip(fan, cap):
            P = P[np.isfinite(P[:, 0])]
            P = P[(np.abs(P[:, 0]) < 16.5) & (np.abs(P[:, 1]) < 9)]
            pts = np.concatenate([center[:2] + sc * P, np.zeros((len(P), 1))], 1)
            pts = pts[(np.abs(pts[:, 0]) < 7.0) & (np.abs(pts[:, 1]) < 3.9)]
            if len(pts) < 2:
                continue
            m = VMobject(stroke_color=C.LIGHT, stroke_width=2.5, stroke_opacity=0.55 if c_ else 0.95)
            m.set_points_as_corners(pts)
            rays.add(m)
        labs = VGroup(
            label(r"photon sphere, $r = \tfrac32 r_s$: light can orbit", font_size=24, color=C.CURVATURE),
            label(r"captured if $b < \tfrac{3\sqrt3}{2}\, r_s \approx 2.6\, r_s$", font_size=24, color=C.LIGHT),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.15).to_corner(UR, buff=0.4)
        hl = label(r"horizon, $r_s$", font_size=22, color=GREY_A).next_to(hole, DOWN, buff=0.75)
        sim = note(r"computed: exact Schwarzschild light paths").to_corner(DL, buff=0.3)
        with self.voiceover(
            "Now go close to a black hole, where the bending is no longer small. <bookmark mark='r'/> Here are exact light "
            "paths, computed from the geodesic equation, all coming in from the left. Far out, they bend a little. "
            "<bookmark mark='p'/> Closer in, they swing around the hole, and at one and a half Schwarzschild radii, light "
            "can travel in a circle: the photon sphere. <bookmark mark='c'/> Any ray aimed within about two point six "
            "Schwarzschild radii of the center falls in. So a black hole casts a shadow more than two and a half times "
            "the size of its horizon."
        ) as vo:
            self.play(FadeIn(hole), FadeIn(hl), FadeIn(sim))
            vo.wait_until("r")
            self.play(LaggedStart(*[Create(r) for r in rays[::-1]], lag_ratio=0.08), run_time=4)
            vo.wait_until("p")
            self.play(Create(ps), FadeIn(labs[0]))
            vo.wait_until("c")
            self.play(FadeIn(labs[1]))
        self.clear_scene()

    # ------------------------------------------------------------------
    def image(self):
        d80, d20 = load("bh80"), load("bh20")
        assert bool(d80["approaching_left"])
        sh80, sh20 = BHShader(d80), BHShader(d20)
        t = ValueTracker(0.0)
        W = 12.4
        H = W * 720 / 1280
        img = Raster(lambda v: sh80(v), t, W, H, center=DOWN * 0.15, alpha=0.0)
        tag = note(r"ray-traced: Schwarzschild light paths, a thin disk (Page--Thorne glow, Doppler $g^4$); "
                   r"colors illustrative").to_edge(DOWN, buff=0.2)
        l1 = label(r"far side of the disk, lensed over the top", font_size=26)
        l1.add_background_rectangle(color=BACKGROUND, opacity=0.7, buff=0.06)
        l1.move_to([0, 2.55, 0])
        l2 = label(r"approaching side: Doppler-brightened", font_size=26)
        l2.add_background_rectangle(color=BACKGROUND, opacity=0.7, buff=0.06)
        l2.move_to([-4.3, -1.6, 0])
        l3 = label(r"thin rings: light that circled the hole", font_size=26)
        l3.add_background_rectangle(color=BACKGROUND, opacity=0.7, buff=0.06)
        l3.move_to([3.6, -1.9, 0])
        with self.voiceover(
            "<bookmark mark='a'/> Put a disk of hot gas around the hole, and trace light from every pixel of a camera back "
            "along those same exact paths. This is what you'd see, from slightly above the disk. <bookmark mark='b'/> The "
            "far side of the disk isn't hidden behind the hole: its light bends up and over the top, and under the bottom. "
            "<bookmark mark='c'/> The gas moves at a sizable fraction of the speed of light, so the side coming toward us "
            "is brightened by the Doppler effect. <bookmark mark='d'/> And the thin rings close to the shadow are light "
            "that went partway around the hole before escaping."
        ) as vo:
            vo.wait_until("a")
            self.add(img)
            self.play(img.fade(1.0), t.animate.set_value(10.0), run_time=1.5, rate_func=linear)
            self.play(FadeIn(tag), t.animate.set_value(25.0), run_time=vo.until("b"), rate_func=linear)
            self.play(FadeIn(l1), t.animate.set_value(40.0), run_time=vo.until("c"), rate_func=linear)
            self.play(FadeIn(l2), t.animate.set_value(55.0), run_time=vo.until("d"), rate_func=linear)
            self.play(FadeIn(l3), t.animate.set_value(75.0), run_time=vo.remaining() + 0.5, rate_func=linear)
        self.play(FadeOut(VGroup(l1, l2, l3)), img.fade(0.0), run_time=1.0)
        self.remove(img)
        img.clear_updaters()
        # face-on, next to the real image of M87*
        t2 = ValueTracker(0.0)
        W2 = 7.2
        img2 = Raster(lambda v: sh20(v), t2, W2, W2 * 720 / 1280, center=[-3.3, 0.2, 0], alpha=0.0)
        eht = ImageMobject(str(EHT))
        eht.set_height(W2 * 720 / 1280).move_to([3.5, 0.2, 0])
        c1 = label(r"ray-traced, seen nearly face-on", font_size=26).next_to(img2, DOWN, buff=0.25)
        c2 = label(r"M87*, Event Horizon Telescope (2019)", font_size=26).next_to(eht, DOWN, buff=0.25)
        cr = note(r"image: EHT Collaboration (ESO), CC BY 4.0").next_to(c2, DOWN, buff=0.12)
        with self.voiceover(
            "<bookmark mark='a'/> Seen more nearly face-on, the disk surrounds a dark shadow, edged by a bright ring. "
            "<bookmark mark='b'/> In 2019, the Event Horizon Telescope, a network of radio dishes the size of the Earth, "
            "photographed exactly this around the black hole at the center of the galaxy M87, six and a half billion "
            "times the mass of the Sun, and three years later the one at the center of our own galaxy."
        ) as vo:
            vo.wait_until("a")
            self.add(img2)
            self.play(img2.fade(1.0), FadeIn(c1), t2.animate.set_value(15.0), run_time=2, rate_func=linear)
            vo.wait_until("b")
            self.play(FadeIn(eht), FadeIn(c2), FadeIn(cr), t2.animate.set_value(40.0), run_time=vo.remaining() + 0.5,
                      rate_func=linear)
        img2.clear_updaters()
        self.clear_scene()
