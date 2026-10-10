from __future__ import annotations

import math

import numpy as np

from explainer import *  # noqa: F403
from videos.relativity.common import redraw, boxed, label, ladder, load, mtex, note, polyline, stack

NEWTON = C.POTENTIAL
EINSTEIN = C.CURVATURE


def orbit_xy(phis, u, scale, center):
    r = 1 / u
    return np.stack([center[0] + scale * r * np.cos(phis), center[1] + scale * r * np.sin(phis), 0 * phis], 1)


class Mercury(VoiceoverScene):
    def construct(self):
        self.problem()
        self.conserved()
        self.potential()
        self.orbit_equation()
        self.precession()
        self.numbers()
        self.rosette()

    # ------------------------------------------------------------------
    def problem(self):
        d = load("mercury")
        phis, u, uN = d["ros_phi"], d["ros_u"], d["ros_uN"]
        center = np.array([0.0, -0.2, 0])
        sc = 1.25
        sun = Dot(center, radius=0.16, color=C.MATTER)
        ell = VMobject(stroke_color=NEWTON, stroke_width=2.5).set_points_as_corners(
            orbit_xy(phis[phis <= 2 * np.pi + 0.01], uN[phis <= 2 * np.pi + 0.01], sc, center))
        k = ValueTracker(0.0)
        n = len(phis)

        def trail():
            j = max(2, int(k.get_value() * (n - 1)))
            return VMobject(stroke_color=EINSTEIN, stroke_width=2.5).set_points_as_corners(orbit_xy(phis[:j], u[:j], sc, center))

        tr = redraw(trail)
        title = label(r"Mercury's orbit turns: 43 arcseconds per century that Newton can't explain", font_size=30)
        title.to_edge(UP, buff=0.35)
        ex = note(r"computed orbit, effect exaggerated 590{,}000$\times$").to_corner(DR, buff=0.3)
        with self.voiceover(
            "Now let's put the Schwarzschild solution to work, starting with the puzzle we began with. "
            "<bookmark mark='a'/> In Newton's theory, a single planet around a star traces a closed ellipse forever. "
            "<bookmark mark='b'/> Mercury's ellipse slowly turns. After accounting for the pull of every other planet, "
            "there remains a turning of forty-three arcseconds per century."
        ) as vo:
            self.play(FadeIn(sun), FadeIn(title))
            vo.wait_until("a")
            self.play(Create(ell), run_time=2)
            vo.wait_until("b")
            self.add(tr)
            self.play(FadeIn(ex), k.animate.set_value(0.45), run_time=vo.remaining() + 0.5, rate_func=linear)
        tr.clear_updaters()
        self.clear_scene()

    # ------------------------------------------------------------------
    def conserved(self):
        L0 = mtex(r"L", r"=", r"\tfrac12\Big[-\Big(1 - \frac{r_s}{r}\Big)c^2\dot t^2 + \frac{\dot r^2}{1 - r_s/r} + r^2\dot\phi^2\Big]",
                  font_size=40)
        L0.to_edge(UP, buff=0.5)
        L0l = note(r"a geodesic in the equatorial plane; $\dot{} = d/d\tau$", font_size=22).next_to(L0, DOWN, buff=0.15)
        cons = VGroup(
            mtex(r"\text{no } t \text{ in } L:", r"\quad E", r"=", r"\Big(1 - \frac{r_s}{r}\Big)c^2\,\dot t", font_size=38),
            mtex(r"\text{no } \phi \text{ in } L:", r"\quad \ell", r"=", r"r^2\,\dot\phi", font_size=38),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.35).next_to(L0l, DOWN, buff=0.5)
        for c_ in cons:
            c_[0].set_color(GREY_A)
        cons[0][1].set_color(C.PROPER_TIME)
        cons[1][1].set_color(C.METRIC)
        consl = VGroup(label(r"energy (per unit mass)", font_size=26, color=GREY_A).next_to(cons[0], RIGHT, buff=0.4),
                       label(r"angular momentum (per unit mass)", font_size=26, color=GREY_A).next_to(cons[1], RIGHT, buff=0.4))
        en = mtex(r"\tfrac12\dot r^2", r"+", r"V_{\text{eff}}(r)", r"=", r"\text{const}", font_size=44)
        en[2].set_color(EINSTEIN)
        en.next_to(cons, DOWN, buff=0.6).set_x(0)
        V = mtex(r"V_{\text{eff}}", r"=", r"-\frac{GM}{r}", r"+", r"\frac{\ell^2}{2r^2}", r"-", r"\frac{GM\ell^2}{c^2r^3}",
                 font_size=44)
        V[0].set_color(EINSTEIN)
        V[6].set_color(EINSTEIN)
        V.next_to(en, DOWN, buff=0.45)
        b = Brace(V[2:5], DOWN, color=NEWTON)
        bl = label(r"Newton", font_size=26, color=NEWTON).next_to(b, DOWN, buff=0.1)
        b2 = Brace(V[6], DOWN, color=EINSTEIN)
        b2l = label(r"new", font_size=26, color=EINSTEIN).next_to(b2, DOWN, buff=0.1)
        with self.voiceover(
            "A planet follows a geodesic of the Schwarzschild metric. <bookmark mark='l'/> Write the geodesic Lagrangian "
            "for an orbit in the equatorial plane. <bookmark mark='e'/> The metric doesn't depend on t, so the quantity "
            "conjugate to t is conserved: that's the energy. <bookmark mark='a'/> It doesn't depend on phi either, so the "
            "angular momentum is conserved. <bookmark mark='v'/> Use these, together with the condition that the "
            "four-velocity has length c, to eliminate t dot and phi dot. What's left looks exactly like a particle "
            "rolling in one dimension, in an effective potential. <bookmark mark='n'/> Its first two terms are Newton's: "
            "gravity and the centrifugal barrier. <bookmark mark='g'/> The third is new: an extra attraction, falling off "
            "like one over r cubed."
        ) as vo:
            vo.wait_until("l")
            self.play(Write(L0), FadeIn(L0l))
            vo.wait_until("e")
            self.play(FadeIn(cons[0]), FadeIn(consl[0]))
            vo.wait_until("a")
            self.play(FadeIn(cons[1]), FadeIn(consl[1]))
            vo.wait_until("v")
            self.play(Write(en))
            self.play(Write(V))
            vo.wait_until("n")
            self.play(GrowFromCenter(b), FadeIn(bl))
            vo.wait_until("g")
            self.play(GrowFromCenter(b2), FadeIn(b2l))
        self.clear_scene()

    # ------------------------------------------------------------------
    def potential(self):
        # units G M = c = 1 (r_s = 2); l^2 = 13.5 (just above the 12 needed for a stable circular orbit)
        l2 = 14.0
        r = np.linspace(2.0, 40, 800)
        VN = -1 / r + l2 / (2 * r * r)
        VG = VN - l2 / r**3
        ax = Axes(x_range=[0, 40, 10], y_range=[-0.08, 0.06, 0.04], x_length=9.0, y_length=4.8, tips=False,
                  axis_config={"stroke_color": GREY_B, "include_ticks": False})
        ax.move_to(DOWN * 0.5)
        xl = MathTex(r"r", font_size=32).next_to(ax.x_axis, RIGHT, buff=0.2)
        yl = mtex(r"V_{\text{eff}}", font_size=32, color=EINSTEIN).next_to(ax.y_axis, UP, buff=0.15)
        okN = VN < 0.06
        okG = (VG > -0.08) & (VG < 0.06)
        cN = polyline(ax, r[okN], VN[okN], color=NEWTON, stroke_width=4)
        cG = polyline(ax, r[okG], VG[okG], color=EINSTEIN, stroke_width=4)
        lN = label(r"Newton", font_size=28, color=NEWTON).next_to(ax.c2p(r[okN][0], VN[okN][0]), RIGHT, buff=0.2)
        lG = label(r"Einstein", font_size=28, color=EINSTEIN).next_to(ax.c2p(4.4, -0.07), RIGHT, buff=0.2)
        rs = DashedLine(ax.c2p(2, -0.08), ax.c2p(2, 0.06), color=GREY_C, stroke_width=2)
        rsl = MathTex(r"r_s", font_size=28, color=GREY_A).next_to(ax.c2p(2, -0.08), DOWN, buff=0.1)
        # a bound orbit: an energy between the GR potential's minimum and the top of its barrier
        E = -0.039
        rr = np.linspace(4.4, 40, 20000)
        vg = -1 / rr + l2 / (2 * rr * rr) - l2 / rr**3
        inside = rr[vg < E]
        r1, r2 = float(inside.min()), float(inside.max())
        assert 6 < r1 < 9 and 11 < r2 < 20
        Eline = DashedLine(ax.c2p(r1, E), ax.c2p(r2, E), color=WHITE, stroke_width=2.5)
        tps = VGroup(Dot(ax.c2p(r1, E), radius=0.06), Dot(ax.c2p(r2, E), radius=0.06))
        Eline = VGroup(Eline, tps)
        El = label(r"a bound orbit rocks between two turning points", font_size=24).next_to(ax.c2p(r2, E), RIGHT, buff=0.2)
        facts = VGroup(
            label(r"no orbit closer than $r = 3r_s$ is stable", font_size=26, color=EINSTEIN),
            label(r"enough energy, and the planet falls in", font_size=26, color=EINSTEIN),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.15).to_corner(UR, buff=0.45)
        with self.voiceover(
            "<bookmark mark='p'/> Here are the two potentials. Newton's has an infinite centrifugal wall: no planet with "
            "angular momentum can reach the center. <bookmark mark='g'/> Einstein's follows Newton's far away, but close "
            "in, the new term wins, the wall turns over, and the potential plunges. <bookmark mark='o'/> A bound orbit still "
            "rocks back and forth between a nearest and farthest point. <bookmark mark='f'/> But close to the hole, "
            "something Newton never allowed: inside three Schwarzschild radii, no circular orbit is stable, and a "
            "particle with enough energy simply falls in."
        ) as vo:
            vo.wait_until("p")
            self.play(Create(ax), FadeIn(xl), FadeIn(yl), Create(rs), FadeIn(rsl))
            self.play(Create(cN), FadeIn(lN))
            vo.wait_until("g")
            self.play(Create(cG), FadeIn(lG))
            vo.wait_until("o")
            self.play(Create(Eline), FadeIn(El))
            vo.wait_until("f")
            self.play(FadeIn(facts, lag_ratio=0.3))
        self.clear_scene()

    # ------------------------------------------------------------------
    def orbit_equation(self):
        title = label(r"The orbit equation", font_size=36).to_corner(UL, buff=0.4)
        rows = [
            mtex(r"\tfrac12\dot r^2", r"=", r"\text{const} + \frac{GM}{r} - \frac{\ell^2}{2r^2} + \frac{GM\ell^2}{c^2r^3}",
                 font_size=38),
            mtex(r"\tfrac12\ell^2\Big(\frac{du}{d\phi}\Big)^2", r"=", r"\text{const} + GM u - \tfrac12\ell^2u^2 + \frac{GM\ell^2}{c^2}u^3",
                 font_size=38),
            mtex(r"\frac{d^2u}{d\phi^2} + u", r"=", r"\frac{GM}{\ell^2}", r"+", r"\frac{3GM}{c^2}\,u^2", font_size=46),
        ]
        whys = [
            note(r"energy equation", font_size=24),
            note(r"$u = 1/r$, $\ \dot r = -\ell\, du/d\phi$", font_size=24),
            note(r"differentiate in $\phi$, divide by $\ell^2 u'$", font_size=24),
        ]
        rows[2][2].set_color(NEWTON)
        rows[2][4].set_color(EINSTEIN)
        x0 = -0.6
        for rr, w in zip(rows, whys):
            rr.shift((x0 - rr[1].get_center()[0]) * RIGHT)
            w.next_to(rr, DOWN, buff=0.1).align_to(rr, RIGHT)
        step = ladder(self, rows, whys, keep=3, top=2.3, x=x0, buff=0.7)
        with self.voiceover(
            "To get the shape of the orbit, change variables. <bookmark mark='a'/> Start from the energy equation. "
            "<bookmark mark='b'/> Use u, one over r, as the variable, and the angle phi instead of time: by conservation "
            "of angular momentum, r dot is minus l times d u d phi. <bookmark mark='c'/> Differentiate once more with "
            "respect to phi, and the constant disappears. This is the relativistic orbit equation."
        ) as vo:
            self.play(FadeIn(title))
            vo.wait_until("a")
            step(0)
            vo.wait_until("b")
            step(1)
            vo.wait_until("c")
            step(2)
        # braces only once step(2) has put the last row in place
        b1 = Brace(rows[2][2], DOWN, color=NEWTON)
        b1l = label(r"Newton: a closed ellipse", font_size=26, color=NEWTON).next_to(b1, DOWN, buff=0.1).align_to(b1, RIGHT)
        b2 = Brace(rows[2][4], DOWN, color=EINSTEIN)
        b2l = label(r"tiny: $3GM/(c^2 r) \sim 10^{-7}$", font_size=26, color=EINSTEIN).next_to(b2, DOWN, buff=0.1).align_to(b2, LEFT)
        # the braces are neighbors: each label hangs away from the other
        if b2l.get_left()[0] < b1l.get_right()[0] + 0.3:
            b2l.shift((b1l.get_right()[0] + 0.3 - b2l.get_left()[0]) * RIGHT)
        with self.voiceover(
            "<bookmark mark='n'/> Without the last term, it's Newton's: its solution is a conic section, an ellipse "
            "for a bound planet. <bookmark mark='e'/> The last term is Einstein's correction, three G M u squared over c "
            "squared. For Mercury it's about ten million times smaller than the others."
        ) as vo:
            vo.wait_until("n")
            self.play(FadeOut(whys[2]), GrowFromCenter(b1), FadeIn(b1l))
            vo.wait_until("e")
            self.play(GrowFromCenter(b2), FadeIn(b2l))
        self.clear_scene()

    # ------------------------------------------------------------------
    def precession(self):
        rows = stack(
            mtex(r"u_0", r"=", r"\frac{GM}{\ell^2}\big(1 + e\cos\phi\big)", font_size=40),
            mtex(r"\frac{3GM}{c^2}u_0^2", r"=", r"\frac{3G^3M^3}{c^2\ell^4}\big(1 +", r"2e\cos\phi", r"+ e^2\cos^2\phi\big)",
                 font_size=40),
            buff=0.5,
        ).to_edge(UP, buff=0.5)
        rows[0][2].set_color(NEWTON)
        rows[1][0].set_color(EINSTEIN)
        res_box = SurroundingRectangle(rows[1][3], color=RED_B, buff=0.08)
        resl = label(r"a push at the orbit's own frequency: resonance", font_size=26, color=RED_B).next_to(rows[1], DOWN, buff=0.3)
        sol = mtex(r"u", r"\approx", r"\frac{GM}{\ell^2}\Big(1 + e\cos\big[(1 - \delta)\phi\big]\Big),\qquad \delta = "
                   r"\frac{3G^2M^2}{c^2\ell^2}", font_size=40)
        sol.next_to(resl, DOWN, buff=0.55)
        dphi = mtex(r"\Delta\phi", r"=", r"2\pi\delta", r"=", r"\frac{6\pi GM}{c^2 a(1 - e^2)}", font_size=48)
        dphi[0].set_color(EINSTEIN)
        dphi[4].set_color(EINSTEIN)
        db = boxed(dphi, color=EINSTEIN, buff=0.25).next_to(sol, DOWN, buff=0.55)
        dl = note(r"per orbit, using $\ell^2 = GMa(1-e^2)$", font_size=24).next_to(db, DOWN, buff=0.15)
        with self.voiceover(
            "Small as it is, it adds up. <bookmark mark='a'/> Start from Newton's ellipse, and feed it into the "
            "correction term. <bookmark mark='b'/> Squaring gives a constant, a cosine of phi, and a cosine squared. "
            "<bookmark mark='r'/> The middle term is the troublemaker: it pushes the orbit at exactly its own natural "
            "frequency, like pushing a swing in time with its motion. Its effect grows with every orbit. "
            "<bookmark mark='s'/> The result is an ellipse whose angle runs slightly slow: the planet returns to its "
            "closest point not after two pi, but a little later. <bookmark mark='d'/> Per orbit, the ellipse turns by six "
            "pi G M over c squared, a, one minus e squared."
        ) as vo:
            vo.wait_until("a")
            self.play(Write(rows[0]))
            vo.wait_until("b")
            self.play(Write(rows[1]))
            vo.wait_until("r")
            self.play(Create(res_box), FadeIn(resl))
            vo.wait_until("s")
            self.play(Write(sol))
            vo.wait_until("d")
            self.play(Write(dphi), Create(db[0]), FadeIn(dl))
        self.clear_scene()

    # ------------------------------------------------------------------
    def numbers(self):
        d = load("mercury")
        cent = float(d["Mercury_century"])
        per = float(d["Mercury_dphi"]) / (math.pi / (180 * 3600))
        orbits = float(d["Mercury_orbits"])
        assert abs(cent - 42.98) < 0.005 and abs(per - 0.1035) < 0.0005 and abs(orbits - 415.2) < 0.05
        assert abs(float(d["Venus_century"]) - 8.62) < 0.01 and abs(float(d["Earth_century"]) - 3.84) < 0.01
        rows = VGroup(
            mtex(r"\text{Mercury: } a = 5.79\times10^{10}\,\text{m},\ e = 0.2056,\ \text{period } 88.0 \text{ days}", font_size=34),
            mtex(r"\Delta\phi = 5.02\times 10^{-7}\ \text{rad} = 0.1035'' \text{ per orbit}", font_size=36),
            mtex(r"\times\ 415.2 \text{ orbits per century}", font_size=36),
            mtex(r"=\ 42.98'' \text{ per century}", font_size=48, color=EINSTEIN),
        ).arrange(DOWN, buff=0.35).to_edge(UP, buff=0.5)
        obs = VGroup(
            label(r"observed, after subtracting the planets: $\approx 43''$ per century", font_size=30),
            label(r"(Le Verrier 1859: $38''$; Newcomb 1882: $43''$)", font_size=26, color=GREY_A),
            label(r"Venus $8.6''$, \ Earth $3.8''$ per century", font_size=26, color=GREY_A),
        ).arrange(DOWN, buff=0.18).next_to(rows, DOWN, buff=0.55)
        quote = label(r"18 November 1915. Einstein wrote that he was beside himself with joy for days.", font_size=28,
                      color=C.CURVATURE).to_edge(DOWN, buff=0.4)
        with self.voiceover(
            "Now the numbers. <bookmark mark='m'/> For Mercury, the semi-major axis, eccentricity, and the mass of the "
            "Sun give a turn of five times ten to the minus seven radians per orbit: a tenth of an arcsecond. "
            "<bookmark mark='o'/> Mercury orbits four hundred and fifteen times a century. <bookmark mark='r'/> Total: forty-"
            "two point nine eight arcseconds per century. <bookmark mark='x'/> Exactly the anomaly astronomers had been "
            "unable to explain for more than half a century. <bookmark mark='q'/> Einstein found this on the eighteenth of "
            "November, 1915, with no adjustable parameters. He later wrote to a friend that for several days he was beside "
            "himself with joy."
        ) as vo:
            vo.wait_until("m")
            self.play(FadeIn(rows[0]))
            self.play(Write(rows[1]))
            vo.wait_until("o")
            self.play(Write(rows[2]))
            vo.wait_until("r")
            self.play(Write(rows[3]))
            vo.wait_until("x")
            self.play(FadeIn(obs, lag_ratio=0.3))
            vo.wait_until("q")
            self.play(FadeIn(quote))
        self.clear_scene()

    # ------------------------------------------------------------------
    def rosette(self):
        d = load("mercury")
        phis, u, uN = d["ros_phi"], d["ros_u"], d["ros_uN"]
        exag = float(d["ros_exaggeration"])
        assert 5.5e5 < exag < 6.2e5
        center = np.array([-2.4, -0.3, 0])
        sc = 1.25
        sun = Dot(center, radius=0.16, color=C.MATTER)
        k = ValueTracker(0.0)
        n = len(phis)
        P = orbit_xy(phis, u, sc, center)
        ell = DashedVMobject(VMobject(stroke_color=NEWTON, stroke_width=2).set_points_as_corners(
            orbit_xy(phis[phis <= 2 * np.pi + 0.01], uN[phis <= 2 * np.pi + 0.01], sc, center)), num_dashes=60)
        # perihelia: local maxima of u
        peri = [i for i in range(1, n - 1) if u[i] >= u[i - 1] and u[i] >= u[i + 1]]

        def trail():
            j = max(2, int(k.get_value() * (n - 1)))
            g = VGroup(VMobject(stroke_color=EINSTEIN, stroke_width=2.5).set_points_as_corners(P[:j]))
            g.add(Dot(P[j - 1], radius=0.08, color=WHITE))
            # a fixed number of submobjects: always_redraw's become() misaligns a family whose size changes
            for i in peri:
                g.add(Line(center, P[i], color=EINSTEIN, stroke_width=1.5, stroke_opacity=0.6 if i < j else 0.0))
            return g

        tr = redraw(trail)
        ex = note(rf"the exact orbit equation, with the effect exaggerated {exag / 1e3:.0f}{{,}}000$\times$", font_size=22)
        ex.to_corner(DL, buff=0.3)
        moon = Circle(radius=1.6, color=GREY_B, fill_color=GREY_D, fill_opacity=0.6).move_to([4.4, 0.4, 0])
        sliver = Rectangle(width=3.2 * 43 / float(d["moon_arcsec"]), height=3.1, stroke_width=0, fill_color=EINSTEIN,
                           fill_opacity=1).move_to(moon)
        ml = VGroup(label(r"$43''$ next to the full Moon ($\approx 1865''$):", font_size=26),
                    label(r"one forty-third of its width, per century", font_size=26, color=EINSTEIN))
        ml.arrange(DOWN, buff=0.12).next_to(moon, DOWN, buff=0.35)
        with self.voiceover(
            "<bookmark mark='a'/> Here's that effect, magnified about six hundred thousand times, by integrating the exact "
            "orbit equation around a far denser star. Each time the planet swings past its closest point, the ellipse has "
            "turned a little further, tracing out a rosette. <bookmark mark='m'/> For the real Mercury, forty-three "
            "arcseconds is tiny: lay it next to the full Moon, and it's a forty-third of the Moon's width, accumulated "
            "over a century. Astronomers measured it anyway, and Newton couldn't account for it."
        ) as vo:
            self.play(FadeIn(sun), Create(ell), FadeIn(ex))
            vo.wait_until("a")
            self.add(tr)
            self.play(k.animate.set_value(0.6), run_time=vo.until("m"), rate_func=linear)
            self.play(FadeIn(moon), FadeIn(sliver), FadeIn(ml), k.animate.set_value(1.0), run_time=vo.remaining() + 0.5,
                      rate_func=linear)
        tr.clear_updaters()
        self.clear_scene()
