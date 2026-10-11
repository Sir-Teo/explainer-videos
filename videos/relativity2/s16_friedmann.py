from __future__ import annotations

import math

import numpy as np

from explainer import *  # noqa: F403
from videos.relativity.common import Globe, great_arc, sphere_points
from videos.relativity2.common import (View3D, clamp_x, label, ladder, load, mtex, note, part_card, polyline, redraw,
                                       under)
from videos.relativity2.geometry import check_flrw

LAM, MAT, MET, CURV = C.LAMBDA, C.MATTER, C.METRIC, C.CURVATURE


def poincare_geodesic(p, q, n=80):
    """Points on the hyperbolic geodesic from p to q in the Poincare disk: the arc of the circle through p, q and the
    inverse point p / |p|^2 (orthogonal to the unit circle)."""
    p, q = np.asarray(p, float), np.asarray(q, float)
    pi = p / (p @ p)
    A = np.array([[2 * (q[0] - p[0]), 2 * (q[1] - p[1])], [2 * (pi[0] - p[0]), 2 * (pi[1] - p[1])]])
    b = np.array([q @ q - p @ p, pi @ pi - p @ p])
    c = np.linalg.solve(A, b)
    R = np.linalg.norm(p - c)
    a0, a1 = math.atan2(*(p - c)[::-1]), math.atan2(*(q - c)[::-1])
    d = (a1 - a0 + math.pi) % (2 * math.pi) - math.pi  # the short way round (inside the disk)
    t = np.linspace(a0, a0 + d, n)
    return np.stack([c[0] + R * np.cos(t), c[1] + R * np.sin(t)], 1)


def corner_angle(P_from, P_a, P_b):
    """Angle at the start of two polylines leaving the same point."""
    u = P_a[1] - P_a[0]
    v = P_b[1] - P_b[0]
    return math.degrees(math.acos(np.clip(u @ v / (np.linalg.norm(u) * np.linalg.norm(v)), -1, 1)))


class Friedmann(VoiceoverScene):
    def construct(self):
        assert check_flrw() == "ok"
        self.card()
        self.geometries()
        self.metric()
        self.derive()
        self.densities()
        self.family()

    def card(self):
        c = part_card("V", r"The universe", r"Einstein's equation, applied to everything")
        self.play(FadeIn(c, shift=UP * 0.2))
        self.wait(1.6)
        self.play(FadeOut(c))

    # ------------------------------------------------------------------
    def geometries(self):
        hdr = VGroup(label(r"Homogeneous and isotropic: the same everywhere, in every direction", font_size=30),
                     label(r"so space has the same curvature everywhere: three possibilities", font_size=26, color=GREY_A)
                     ).arrange(DOWN, buff=0.12).to_edge(UP, buff=0.3)
        # sphere with an equilateral geodesic triangle
        view = View3D(center=[-4.6, -0.4, 0], scale=1.45, azimuth=0.5, elevation=0.45)
        globe = Globe(view, n_lat=4, n_lon=10)
        th0 = math.radians(55)
        V3 = [sphere_points(th0, math.radians(a)) for a in (-30, 90, 210)]
        arcs3 = [great_arc(V3[i], V3[(i + 1) % 3], 80) for i in range(3)]
        tri3 = VGroup(*[globe.curve(A, color=CURV, stroke_width=4) for A in arcs3])

        def sph_angle(i):
            a, b = arcs3[i], arcs3[(i - 1) % 3][::-1]
            return corner_angle(None, a, b)

        s_sph = sum(sph_angle(i) for i in range(3))
        assert s_sph > 180
        # flat
        fc = np.array([0, -0.4, 0])
        Vf = [fc + 1.35 * np.array([math.cos(math.radians(a)), math.sin(math.radians(a)), 0]) for a in (90, 210, 330)]
        tri_f = Polygon(*Vf, color=CURV, stroke_width=4)
        grid_f = VGroup(*[Line(fc + [-1.6, y, 0], fc + [1.6, y, 0], color=GREY_D, stroke_width=1) for y in np.linspace(-1.6, 1.6, 7)],
                        *[Line(fc + [x, -1.6, 0], fc + [x, 1.6, 0], color=GREY_D, stroke_width=1) for x in np.linspace(-1.6, 1.6, 7)])
        # hyperbolic (Poincare disk)
        hc = np.array([4.6, -0.4, 0])
        Rd = 1.6
        disk = Circle(radius=Rd, color=GREY_B, stroke_width=2).move_to(hc)
        Vh = [0.62 * np.array([math.cos(math.radians(a)), math.sin(math.radians(a))]) for a in (90, 210, 330)]
        arcsh = [poincare_geodesic(Vh[i], Vh[(i + 1) % 3]) for i in range(3)]
        tri_h = VGroup(*[VMobject(stroke_color=CURV, stroke_width=4).set_points_as_corners(
            [hc + Rd * np.array([x, y, 0]) for x, y in A]) for A in arcsh])
        s_hyp = sum(corner_angle(None, arcsh[i], arcsh[(i - 1) % 3][::-1]) for i in range(3))
        assert s_hyp < 180
        hgrid = VGroup()
        for ang in np.linspace(0, np.pi, 6, endpoint=False):
            d = np.array([math.cos(ang), math.sin(ang)])
            hgrid.add(Line(hc + Rd * np.array([*(-d), 0]), hc + Rd * np.array([*d, 0]), color=GREY_D, stroke_width=1))
        labs = VGroup(
            VGroup(label(r"$k = +1$: closed", font_size=28), label(rf"angles sum to ${s_sph:.0f}^\circ$", font_size=24, color=CURV),
                   mtex(r"C = 2\pi R\sin\chi", font_size=30)).arrange(DOWN, buff=0.1),
            VGroup(label(r"$k = 0$: flat", font_size=28), label(r"angles sum to $180^\circ$", font_size=24, color=CURV),
                   mtex(r"C = 2\pi R\chi", font_size=30)).arrange(DOWN, buff=0.1),
            VGroup(label(r"$k = -1$: open", font_size=28), label(rf"angles sum to ${s_hyp:.0f}^\circ$", font_size=24, color=CURV),
                   mtex(r"C = 2\pi R\sinh\chi", font_size=30)).arrange(DOWN, buff=0.1),
        )
        for g_, x in zip(labs, (-4.6, 0, 4.6)):
            g_.move_to([x, -2.95, 0])
        cap = note(r"(two-dimensional versions; the open plane is drawn as Poincar\'e's disk, where geodesics are circular arcs)")
        cap.to_edge(DOWN, buff=0.12)
        with self.voiceover(
            "Finally, the biggest solution of all: the universe. <bookmark mark='a'/> On the largest scales, the "
            "universe looks the same everywhere and in every direction. If that's exactly true, space must have the "
            "same curvature at every point, and there are only three possibilities. <bookmark mark='b'/> Positive "
            "curvature, like a sphere: a closed universe, where triangles have more than one hundred eighty degrees. "
            "<bookmark mark='c'/> Zero curvature: flat space. <bookmark mark='d'/> Or negative curvature, a hyperbolic "
            "space, drawn here in Poincaré's disk, where triangles have less than one hundred eighty degrees, and the "
            "circumference of a circle grows exponentially with its radius."
        ) as vo:
            vo.wait_until("a")
            self.play(FadeIn(hdr, lag_ratio=0.2))
            vo.wait_until("b")
            self.add(globe)
            self.play(FadeIn(globe), *[Create(t_) for t_ in tri3], FadeIn(labs[0]))
            vo.wait_until("c")
            self.play(FadeIn(grid_f), Create(tri_f), FadeIn(labs[1]))
            vo.wait_until("d")
            self.play(Create(disk), FadeIn(hgrid), Create(tri_h), FadeIn(labs[2]), FadeIn(cap))
        for m in self.mobjects:
            m.clear_updaters()
        self.clear_scene()

    # ------------------------------------------------------------------
    def metric(self):
        m = mtex(r"ds^2", r"=", r"-dt^2", r"+", r"a(t)^2", r"\Big[\frac{dr^2}{1 - kr^2} + r^2d\Omega^2\Big]", font_size=48)
        m[4].set_color(MET)
        m.to_edge(UP, buff=0.45)
        hist = note(r"Friedmann (1922, 1924), Lema\^itre (1927), Robertson and Walker (1935--37)").next_to(m, DOWN, buff=0.15)
        k = ValueTracker(1.0)
        rng = np.random.default_rng(8)
        gal = rng.uniform(-1, 1, (40, 2)) * np.array([3.0, 1.5])
        cen = np.array([0, -1.0, 0])

        def galaxies():
            s = k.get_value()
            g = VGroup()
            for x in np.arange(-3, 3.01, 0.75):
                g.add(Line(cen + s * np.array([x, -1.6, 0]), cen + s * np.array([x, 1.6, 0]), color=GREY_D, stroke_width=1))
            for y in np.arange(-1.5, 1.51, 0.75):
                g.add(Line(cen + s * np.array([-3.2, y, 0]), cen + s * np.array([3.2, y, 0]), color=GREY_D, stroke_width=1))
            g.add(*[Dot(cen + s * np.array([x, y, 0]), radius=0.05, color=WHITE) for x, y in gal])
            g.add(Dot(cen + s * np.array([*gal[0], 0]), radius=0.09, color=C.LIGHT))
            return g

        G = redraw(galaxies)
        txt = VGroup(
            label(r"galaxies sit at fixed $(r, \theta, \phi)$: comoving coordinates", font_size=26),
            label(r"all distances grow with the scale factor $a(t)$", font_size=26, color=MET),
            label(r"so from any galaxy, the others recede at $v = H d$, \ $H = \dot a/a$: Hubble's law", font_size=26),
        ).arrange(DOWN, buff=0.12).to_edge(DOWN, buff=0.25)
        with self.voiceover(
            "<bookmark mark='a'/> Space with constant curvature, multiplied by a scale factor a that can change with "
            "time: this is the Friedmann–Lemaître–Robertson–Walker metric, where k is plus one, zero, or minus one. "
            "<bookmark mark='b'/> Galaxies sit at fixed coordinates, and all distances between them grow in proportion "
            "to a of t. <bookmark mark='c'/> From any one galaxy, all the others recede, at speeds proportional to "
            "their distance: Hubble's law, with the Hubble rate a dot over a."
        ) as vo:
            vo.wait_until("a")
            self.play(Write(m), FadeIn(hist))
            vo.wait_until("b")
            self.add(G)
            self.play(FadeIn(txt[:2]), k.animate.set_value(1.6), run_time=3, rate_func=smooth)
            vo.wait_until("c")
            self.play(FadeIn(txt[2]), k.animate.set_value(2.2), run_time=2.5, rate_func=smooth)
        G.clear_updaters()
        self.clear_scene()

    # ------------------------------------------------------------------
    def derive(self):
        rows = [
            mtex(r"\Gamma^t{}_{rr}", r"=", r"\frac{a\dot a}{1 - kr^2},\qquad \Gamma^r{}_{tr} = \frac{\dot a}{a},\ \dots", font_size=36),
            mtex(r"R_{tt}", r"=", r"-3\frac{\ddot a}{a},\qquad R_{rr} = \frac{a\ddot a + 2\dot a^2 + 2k}{1 - kr^2}", font_size=36),
            mtex(r"G_{tt}", r"=", r"\frac{3(\dot a^2 + k)}{a^2} = 8\pi\rho + \Lambda", font_size=38),
            mtex(r"H^2 \equiv \Big(\frac{\dot a}{a}\Big)^2", r"=", r"\frac{8\pi}{3}\rho - \frac{k}{a^2} + \frac{\Lambda}{3}", font_size=42),
            mtex(r"\frac{\ddot a}{a}", r"=", r"-\frac{4\pi}{3}(\rho + 3p) + \frac{\Lambda}{3}", font_size=42),
            mtex(r"\dot\rho", r"=", r"-3\,\frac{\dot a}{a}\,(\rho + p)\quad\Rightarrow\quad \rho \propto a^{-3(1+w)}\ \ (p = w\rho)", font_size=38),
        ]
        whys = [
            note(r"the Christoffel symbols of this metric"),
            note(r"its Ricci tensor (all computed and checked symbolically)"),
            note(r"the $tt$ component of Einstein's equation, with a perfect fluid at rest in these coordinates"),
            note(r"the Friedmann equation"),
            note(r"the $rr$ component, combined with the first: part 1's acceleration equation, now derived"),
            note(r"conservation of energy, $\nabla_\mu T^{\mu t} = 0$: matter $w = 0$, radiation $w = \tfrac13$, vacuum $w = -1$"),
        ]
        rows[3][0].set_color(MET)
        rows[3][2].set_color(MAT)
        rows[4][0].set_color(MET)
        under(rows, whys, -0.5)
        step = ladder(self, rows, whys, keep=4, top=3.0, x=-0.5, buff=0.6)
        with self.voiceover(
            "Now run the machine from part one. <bookmark mark='a'/> The Christoffel symbols: <bookmark mark='b'/> "
            "the Ricci tensor, computed and checked symbolically. <bookmark mark='c'/> Fill the universe with a "
            "perfect fluid, at rest relative to the galaxies, and take the time-time component of Einstein's equation. "
            "<bookmark mark='d'/> Divide by three: this is the Friedmann equation. The expansion rate squared is set by "
            "the density, the curvature, and the cosmological constant."
        ) as vo:
            vo.wait_until("a")
            step(0)
            vo.wait_until("b")
            step(1)
            vo.wait_until("c")
            step(2)
            vo.wait_until("d")
            step(3)
        with self.voiceover(
            "<bookmark mark='e'/> The space-space components give the acceleration equation, which we found in part one "
            "from Baez and Bunn's ball of coffee grounds. <bookmark mark='f'/> And energy conservation says how each "
            "ingredient thins out as space expands: matter as one over a cubed, radiation as one over a to the fourth, "
            "because each photon is also stretched, and vacuum energy not at all."
        ) as vo:
            vo.wait_until("e")
            step(4)
            vo.wait_until("f")
            step(5)
        self.clear_scene()

    # ------------------------------------------------------------------
    def densities(self):
        co = load("cosmo2")
        a, rr, rm, rl = co["rho_a"], co["rho_r"], co["rho_m"], co["rho_L"]
        z_eq, z_ml = float(co["z_eq"]), float(co["z_mL"])
        assert abs(z_eq - 3422) < 5 and abs(z_ml - 0.30) < 0.01
        ax = Axes(x_range=[-6, 1, 1], y_range=[-2, 24, 4], x_length=7.0, y_length=4.6, tips=False,
                  axis_config={"stroke_color": GREY_B, "font_size": 20},
                  x_axis_config={"numbers_to_include": [-6, -5, -4, -3, -2, -1, 0, 1]},
                  y_axis_config={"numbers_to_include": [0, 4, 8, 12, 16, 20]}).move_to([-2.2, -0.6, 0])
        xl = label(r"$\log_{10} a$ \ (today $= 0$)", font_size=22).next_to(ax.x_axis, DOWN, buff=0.4)
        yl = label(r"$\log_{10}$ density / today's critical density", font_size=22).next_to(ax, UP, buff=0.1)
        la = np.log10(a)
        c_r = polyline(ax, la, np.log10(rr), color=C.LIGHT, stroke_width=4)
        c_m = polyline(ax, la, np.log10(rm), color=MAT, stroke_width=4)
        c_l = polyline(ax, la, np.log10(rl), color=LAM, stroke_width=4)
        lab = VGroup(label(r"radiation $\propto a^{-4}$", font_size=22, color=C.LIGHT).next_to(ax.c2p(-5.5, 17.5), RIGHT, buff=0.1),
                     label(r"matter $\propto a^{-3}$", font_size=22, color=MAT).next_to(ax.c2p(-5.6, 13.0), RIGHT, buff=0.1),
                     label(r"$\Lambda$: constant", font_size=22, color=LAM).next_to(ax.c2p(-5.0, 0.5), RIGHT, buff=0.1))
        eq1 = Dot(ax.c2p(math.log10(1 / (1 + z_eq)), math.log10(rm[np.argmin(np.abs(a - 1 / (1 + z_eq)))])), radius=0.08)
        eq2 = Dot(ax.c2p(math.log10(1 / (1 + z_ml)), math.log10(0.685)), radius=0.08)
        facts = VGroup(
            label(r"radiation $=$ matter at $z \approx 3400$", font_size=24),
            label(r"matter $= \Lambda$ at $z \approx 0.3$", font_size=24),
            mtex(r"\rho_c = \frac{3H_0^2}{8\pi G} = 8.5\times10^{-27}\ \tfrac{\text{kg}}{\text{m}^3}", font_size=32),
            label(r"about five protons per cubic meter", font_size=24, color=GREY_A),
            mtex(r"\Omega - 1 = \frac{k}{a^2H^2}", font_size=32, color=CURV),
            label(r"measured: flat, to a fraction of a percent", font_size=24, color=CURV),
            note(r"Planck 2018: $H_0 = 67.4$, $\Omega_m = 0.315$, plus radiation"),
        ).arrange(DOWN, buff=0.16).move_to([4.5, -0.3, 0])
        c = load("consts")
        assert abs(float(c["rho_crit"]) / 8.53e-27 - 1) < 0.01
        with self.voiceover(
            "<bookmark mark='a'/> Here are the three ingredients of our universe, with their measured amounts, against "
            "the scale factor. Radiation dominated early on, until the universe was about a three-thousand-four-hundredth "
            "of its present size. Then matter took over, and only recently, at a redshift of about a third, did the "
            "cosmological constant overtake matter. <bookmark mark='b'/> The Friedmann equation also says how much "
            "density makes space flat: the critical density, about five protons per cubic meter today. "
            "<bookmark mark='c'/> The departure from it measures curvature, and our universe turns out to be flat to "
            "within a fraction of a percent."
        ) as vo:
            vo.wait_until("a")
            self.play(Create(ax), FadeIn(xl), FadeIn(yl))
            self.play(Create(c_r), Create(c_m), Create(c_l), FadeIn(lab), run_time=2.5)
            self.play(FadeIn(eq1), FadeIn(eq2), FadeIn(facts[:2], lag_ratio=0.3))
            vo.wait_until("b")
            self.play(FadeIn(facts[2:4], lag_ratio=0.3))
            vo.wait_until("c")
            self.play(FadeIn(facts[4:], lag_ratio=0.3))
        self.clear_scene()

    # ------------------------------------------------------------------
    def family(self):
        co = load("cosmo2")
        ax = Axes(x_range=[-15, 45, 10], y_range=[0, 3.0, 0.5], x_length=8.6, y_length=4.8, tips=False,
                  axis_config={"stroke_color": GREY_B, "font_size": 20},
                  x_axis_config={"numbers_to_include": [-10, 0, 10, 20, 30, 40]},
                  y_axis_config={"numbers_to_include": [0.5, 1, 1.5, 2, 2.5, 3]}).move_to([-1.6, -0.5, 0])
        xl = label(r"billions of years from today", font_size=22).next_to(ax.x_axis, DOWN, buff=0.4)
        yl = label(r"scale factor $a$ (today $= 1$), all with today's $H_0$", font_size=22).next_to(ax, UP, buff=0.1)
        specs = [("desitter", r"only $\Lambda$ (de Sitter): exponential", LAM),
                 ("lcdm", r"ours: matter $+ \Lambda$", WHITE),
                 ("open", r"matter, $\Omega = 0.3$, $k = -1$", GREY_B),
                 ("flat_matter", r"matter, $\Omega = 1$, flat", MAT),
                 ("closed", r"matter, $\Omega = 3$, $k = +1$: recollapse", CURV)]
        curves, labs = VGroup(), VGroup()
        for name, txt, col in specs:
            F = co["fam_" + name]
            ok = (F[:, 0] > -15) & (F[:, 0] < 45) & (F[:, 1] < 3.0)
            curves.add(polyline(ax, F[ok, 0], F[ok, 1], color=col, stroke_width=4 if name == "lcdm" else 3))
            labs.add(label(txt, font_size=22, color=col))
        labs.arrange(DOWN, aligned_edge=LEFT, buff=0.15).to_corner(UR, buff=0.35)
        now = DashedLine(ax.c2p(0, 0), ax.c2p(0, 3.0), color=GREY_C, stroke_width=1.5)
        hist = VGroup(
            label(r"Einstein (1917): a static universe, held up by $\Lambda$, and unstable", font_size=22, color=GREY_A),
            label(r"Friedmann (1922): the universe must expand or contract; Hubble (1929): it expands", font_size=22, color=GREY_A),
        ).arrange(DOWN, buff=0.08).to_edge(DOWN, buff=0.2)
        flat_age = -float(co["fam_flat_matter"][0, 0])
        assert abs(flat_age - 9.7) < 0.1
        with self.voiceover(
            "<bookmark mark='a'/> Solve the Friedmann equation, and each mix of ingredients gives its own history. All "
            "of these universes expand at today's measured rate. A closed universe of matter expands, stops, and "
            "recollapses. A flat one of matter alone keeps slowing forever; an open one coasts. A universe of pure "
            "vacuum energy expands exponentially. <bookmark mark='b'/> Ours, matter plus a cosmological constant, "
            "decelerated for its first seven billion years, and now accelerates, heading toward the exponential. "
            "<bookmark mark='c'/> Einstein himself had wanted a static universe, and added the cosmological constant to "
            "hold it up; but that balance is unstable. Alexander Friedmann saw in 1922 that the equation demands a "
            "universe that changes, and in 1929 Edwin Hubble found that it expands."
        ) as vo:
            vo.wait_until("a")
            self.play(Create(ax), FadeIn(xl), FadeIn(yl), Create(now))
            self.play(LaggedStart(*[Create(c_) for i, c_ in enumerate(curves) if i != 1], lag_ratio=0.3),
                      FadeIn(VGroup(*[l_ for i, l_ in enumerate(labs) if i != 1]), lag_ratio=0.3), run_time=4)
            vo.wait_until("b")
            self.play(Create(curves[1]), FadeIn(labs[1]), run_time=2)
            vo.wait_until("c")
            self.play(FadeIn(hist, lag_ratio=0.3))
        self.clear_scene()
