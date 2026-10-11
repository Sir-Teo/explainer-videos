from __future__ import annotations

import math

import numpy as np
from scipy.linalg import expm

from explainer import *  # noqa: F403
from videos.relativity2.common import (boxed, label, ladder, load, mtex, note, polyline, redraw, under, zigzag)

TH, SH, RO, RIC = C.EXPANSION, C.WAVE, C.SPIN, C.MATTER


class Focusing(VoiceoverScene):
    def construct(self):
        self.question()
        self.congruence()
        self.derive()
        self.meaning()
        self.focusing()
        self.trapped()
        self.theorem()

    # ------------------------------------------------------------------
    def question(self):
        q = VGroup(
            label(r"Is the singularity an artifact of perfect symmetry?", font_size=38),
            label(r"Lifshitz \& Khalatnikov (1963): in a generic collapse, no singularity forms", font_size=26,
                  color=GREY_A),
            label(r"Penrose (1965): yes it does, whenever a \emph{trapped surface} forms", font_size=26,
                  color=C.CURVATURE),
        ).arrange(DOWN, buff=0.35)
        tool = label(r"the tool: Raychaudhuri's equation (1955), for bundles of free particles or light rays",
                     font_size=28).next_to(q, DOWN, buff=0.7)
        with self.voiceover(
            "In 1963, two Soviet physicists, Lifshitz and Khalatnikov, argued that the singularity was an artifact of "
            "symmetry: in a realistic, irregular collapse, they concluded, no singularity would form. "
            "<bookmark mark='p'/> Two years later, Roger Penrose proved the opposite. Once a certain kind of surface "
            "forms, a trapped surface, a singularity is unavoidable, whatever the symmetry. <bookmark mark='t'/> The "
            "key tool is an equation found in 1955 by Amal Kumar Raychaudhuri, about how a bundle of free particles, "
            "or light rays, spreads out or converges."
        ) as vo:
            self.play(FadeIn(q[0]))
            self.play(FadeIn(q[1]))
            vo.wait_until("p")
            self.play(FadeIn(q[2]))
            vo.wait_until("t")
            self.play(FadeIn(tool))
        self.clear_scene()

    # ------------------------------------------------------------------
    def congruence(self):
        top = VGroup(
            mtex(r"B_{\mu\nu}", r"=", r"\nabla_\nu u_\mu", font_size=44),
            label(r"how the velocity $u$ of a bundle of free worldlines changes across it:", font_size=26,
                  color=GREY_A),
            mtex(r"\frac{D\xi^\mu}{d\tau} = B^\mu{}_\nu\,\xi^\nu", font_size=36),
        ).arrange(DOWN, buff=0.18).to_edge(UP, buff=0.35)
        dec = mtex(r"B_{\mu\nu}", r"=", r"\tfrac13\theta\, h_{\mu\nu}", r"+", r"\sigma_{\mu\nu}", r"+", r"\omega_{\mu\nu}",
                   font_size=44).next_to(top, DOWN, buff=0.35)
        dec[2].set_color(TH)
        dec[4].set_color(SH)
        dec[6].set_color(RO)
        centers = [np.array([-4.3, -1.7, 0]), np.array([0, -1.7, 0]), np.array([4.3, -1.7, 0])]
        mats = [np.array([[-0.5, 0], [0, -0.5]]), np.array([[0.45, 0], [0, -0.45]]), np.array([[0, -0.9], [0.9, 0]])]
        cols = [TH, SH, RO]
        names = [r"expansion $\theta$: volume", r"shear $\sigma$: shape", r"rotation $\omega$: twist"]
        n = 16
        ang = np.linspace(0, 2 * np.pi, n, endpoint=False)
        base = np.stack([np.cos(ang), np.sin(ang)], 1) * 1.0
        k = ValueTracker(0.0)

        def ring(i):
            def make():
                A = expm(mats[i] * k.get_value())
                P = base @ A.T
                pts = [centers[i] + np.array([x, y, 0]) for x, y in P]
                g = VGroup(Circle(radius=1.0, color=GREY_D, stroke_width=1.5).move_to(centers[i]))
                g.add(VMobject(stroke_color=cols[i], stroke_width=2, stroke_opacity=0.6).set_points_as_corners([*pts, pts[0]]))
                g.add(*[Dot(p, radius=0.06, color=cols[i]) for p in pts])
                g.add(Dot(pts[0], radius=0.09, color=WHITE))
                return g
            return redraw(make)

        rings = [ring(i) for i in range(3)]
        labs = VGroup(*[label(nm, font_size=24, color=c).move_to(cc + DOWN * 1.65) for nm, c, cc in zip(names, cols, centers)])
        with self.voiceover(
            "<bookmark mark='a'/> Picture a whole family of freely falling worldlines, side by side, like the ball of "
            "test particles from part one. Let u be their four-velocity, and B the tensor that says how u changes "
            "across the bundle: it tells you how the separation between neighbors grows. "
            "<bookmark mark='b'/> B splits into three parts, each with its own meaning. <bookmark mark='c'/> Its trace, "
            "theta, the expansion, says how fast the bundle's volume grows. Its symmetric, traceless part, the shear "
            "sigma, changes the shape without changing the volume. And its antisymmetric part, the rotation omega, "
            "twists it."
        ) as vo:
            vo.wait_until("a")
            self.play(FadeIn(top, lag_ratio=0.2))
            vo.wait_until("b")
            self.play(Write(dec))
            vo.wait_until("c")
            self.add(*rings)
            self.play(FadeIn(labs, lag_ratio=0.3))
            self.play(k.animate.set_value(1.0), run_time=3, rate_func=there_and_back_with_pause)
        for r in rings:
            r.clear_updaters()
        self.clear_scene()

    # ------------------------------------------------------------------
    def derive(self):
        rows = [
            mtex(r"\frac{dB_{\mu\nu}}{d\tau}", r"=", r"u^\sigma\nabla_\sigma\nabla_\nu u_\mu", font_size=38),
            mtex(r"\frac{dB_{\mu\nu}}{d\tau}", r"=", r"u^\sigma\nabla_\nu\nabla_\sigma u_\mu - R_{\lambda\mu\sigma\nu}\,u^\lambda u^\sigma", font_size=38),
            mtex(r"\frac{dB_{\mu\nu}}{d\tau}", r"=", r"\nabla_\nu\big(u^\sigma\nabla_\sigma u_\mu\big) - (\nabla_\nu u^\sigma)(\nabla_\sigma u_\mu) - R_{\lambda\mu\sigma\nu}\,u^\lambda u^\sigma", font_size=38),
            mtex(r"\frac{dB_{\mu\nu}}{d\tau}", r"=", r"-B_{\mu\sigma}B^\sigma{}_\nu - R_{\lambda\mu\sigma\nu}\,u^\lambda u^\sigma", font_size=38),
            mtex(r"\frac{d\theta}{d\tau}", r"=", r"-B_{\mu\sigma}B^{\sigma\mu} - R_{\mu\nu}\,u^\mu u^\nu", font_size=38),
            mtex(r"\frac{d\theta}{d\tau}", r"=", r"-\tfrac13\theta^2", r"-", r"\sigma_{\mu\nu}\sigma^{\mu\nu}", r"+",
                 r"\omega_{\mu\nu}\omega^{\mu\nu}", r"-", r"R_{\mu\nu}u^\mu u^\nu", font_size=42),
        ]
        whys = [
            note(r"rate of change along the flow"),
            note(r"swap the derivatives: their commutator is the Riemann tensor (part 1)"),
            note(r"product rule"),
            note(r"the worldlines are geodesics: $u^\sigma\nabla_\sigma u_\mu = 0$"),
            note(r"take the trace: $\theta = B^\mu{}_\mu$; \ $g^{\mu\nu}R_{\lambda\mu\sigma\nu} = R_{\lambda\sigma}$"),
            note(r"square of $\tfrac13\theta h + \sigma + \omega$: the cross terms vanish"),
        ]
        for r in rows[4:]:
            r[0].set_color(TH)
        last = rows[5]
        last[2].set_color(TH)
        last[4].set_color(SH)
        last[6].set_color(RO)
        last[8].set_color(RIC)
        under(rows, whys, -2.6)
        step = ladder(self, rows, whys, keep=4, top=3.1, x=-2.6, buff=0.62)
        with self.voiceover(
            "<bookmark mark='a'/> Now let's derive how theta changes along the bundle. The rate of change of B is u "
            "dotted into a second covariant derivative of u. <bookmark mark='b'/> Swap the order of the two "
            "derivatives. Their commutator, as we found in part one, is the Riemann tensor. <bookmark mark='c'/> Use "
            "the product rule on the first term. <bookmark mark='d'/> The worldlines are free, so they're geodesics: u "
            "dot grad u is zero, and what's left is B times B, and curvature."
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
            "<bookmark mark='e'/> Take the trace, and Riemann contracts to the Ricci tensor. <bookmark mark='f'/> "
            "Finally, write B as its three parts: the trace gives a third of theta squared, the shear and rotation give "
            "their squares, and the cross terms vanish. This is Raychaudhuri's equation."
        ) as vo:
            vo.wait_until("e")
            step(4)
            vo.wait_until("f")
            step(5)
            self.play(Circumscribe(last, color=TH))
        self.clear_scene()

    # ------------------------------------------------------------------
    def meaning(self):
        eq = mtex(r"\frac{d\theta}{d\tau}", r"=", r"-\tfrac13\theta^2", r"-", r"\sigma_{\mu\nu}\sigma^{\mu\nu}", r"+",
                  r"\omega_{\mu\nu}\omega^{\mu\nu}", r"-", r"R_{\mu\nu}u^\mu u^\nu", font_size=46).to_edge(UP, buff=0.4)
        eq[0].set_color(TH)
        eq[2].set_color(TH)
        eq[4].set_color(SH)
        eq[6].set_color(RO)
        eq[8].set_color(RIC)
        bs = [Brace(eq[i], DOWN, buff=0.1, color=c) for i, c in ((2, TH), (4, SH), (6, RO), (8, RIC))]
        bl = [label(t, font_size=22, color=c).next_to(b, DOWN, buff=0.08) for t, c, b in (
            (r"converging feeds itself", TH, bs[0]), (r"shear focuses", SH, bs[1]),
            (r"rotation defocuses", RO, bs[2]), (r"matter focuses", RIC, bs[3]))]
        ein = mtex(r"R_{\mu\nu}u^\mu u^\nu", r"=", r"8\pi\Big(T_{\mu\nu} - \tfrac12 T g_{\mu\nu}\Big)u^\mu u^\nu", r"=",
                   r"4\pi(\rho + 3p)", font_size=38).move_to(DOWN * 0.55)
        ein[0].set_color(RIC)
        ein[4].set_color(RIC)
        einl = note(r"Einstein's equation (trace-reversed), for a perfect fluid").next_to(ein, DOWN, buff=0.1)
        bb = VGroup(
            label(r"Part 1's ball of coffee grounds was this equation: start at rest ($\theta = \sigma = \omega = 0$),", font_size=26),
            mtex(r"\frac{d\theta}{d\tau} = \frac{\ddot V}{V} = -4\pi(\rho + 3p)", font_size=38),
        ).arrange(DOWN, buff=0.15).next_to(einl, DOWN, buff=0.35)
        bb[1].set_color(C.CURVATURE)
        ec = VGroup(
            label(r"energy conditions: \ $\rho + 3p \geq 0$ (strong), \ $\rho + p \geq 0$ (null, for light rays)",
                  font_size=26, color=GREY_A),
            label(r"dark energy breaks the strong one (so it can accelerate the universe); all ordinary matter obeys both",
                  font_size=22, color=GREY_B),
        ).arrange(DOWN, buff=0.1).to_edge(DOWN, buff=0.3)
        with self.voiceover(
            "Read it term by term. <bookmark mark='a'/> Theta squared: once a bundle starts converging, convergence "
            "feeds on itself. <bookmark mark='b'/> Shear always adds to the focusing. <bookmark mark='c'/> Rotation is "
            "the only term that pushes the other way, like a centrifugal force. <bookmark mark='d'/> And the last term "
            "is where gravity enters. <bookmark mark='e'/> By Einstein's equation, for a fluid it's four pi times rho "
            "plus three p. <bookmark mark='f'/> We've seen this before: it's exactly Baez and Bunn's statement about a "
            "ball of particles starting at rest. That was Raychaudhuri's equation all along. "
            "<bookmark mark='g'/> As long as rho plus three p is positive, which is true of all ordinary matter, gravity "
            "focuses. For light rays, the condition needed is even weaker: rho plus p non-negative."
        ) as vo:
            self.play(Write(eq))
            for k, (b, l_) in zip("abcd", zip(bs, bl)):
                vo.wait_until(k)
                self.play(GrowFromCenter(b), FadeIn(l_), run_time=0.7)
            vo.wait_until("e")
            self.play(Write(ein), FadeIn(einl))
            vo.wait_until("f")
            self.play(FadeIn(bb, lag_ratio=0.2))
            vo.wait_until("g")
            self.play(FadeIn(ec, lag_ratio=0.2))
        self.clear_scene()

    # ------------------------------------------------------------------
    def focusing(self):
        # left: theta(lambda) for light, theta0 = -1: pure focusing and with extra shear/matter
        ax = Axes(x_range=[0, 2.4, 0.5], y_range=[-12, 0, 4], x_length=5.4, y_length=3.6, tips=False,
                  axis_config={"stroke_color": GREY_B, "font_size": 20},
                  x_axis_config={"numbers_to_include": [0.5, 1, 1.5, 2]},
                  y_axis_config={"numbers_to_include": [-12, -8, -4]}).move_to([-3.3, -1.0, 0])
        xl = label(r"$\lambda \,/\, |\theta_0|^{-1}$", font_size=22).next_to(ax.x_axis, DOWN, buff=0.35)
        yl = label(r"$\theta / |\theta_0|$", font_size=22, color=TH).next_to(ax.y_axis, UP, buff=0.1)
        lam = np.linspace(0, 1.99, 400)
        pure = -1 / (1 - lam / 2)
        ok = pure > -12
        c0 = polyline(ax, lam[ok], pure[ok], color=TH, stroke_width=4)
        # with matter: d theta/d lambda = -theta^2/2 - R, R = 0.5 (Euler, fine step)
        th, ys = -1.0, []
        dl = lam[1] - lam[0]
        for _ in lam:
            ys.append(th)
            th += dl * (-th * th / 2 - 0.5)
        ys = np.array(ys)
        ok2 = ys > -12
        c1 = polyline(ax, lam[ok2], ys[ok2], color=RIC, stroke_width=3)
        wall = DashedLine(ax.c2p(2, 0), ax.c2p(2, -12), color=C.SINGULARITY, stroke_width=2)
        eqs = VGroup(
            mtex(r"\frac{d\theta}{d\lambda} \le -\tfrac12\theta^2", font_size=34, color=TH),
            mtex(r"\Rightarrow\ \frac{1}{\theta(\lambda)} \ge \frac{1}{\theta_0} + \frac{\lambda}{2}", font_size=34),
            label(r"if $\theta_0 < 0$: \ $\theta \to -\infty$ before $\lambda = 2/|\theta_0|$", font_size=26, color=TH),
            label(r"a caustic: neighboring rays cross", font_size=24, color=GREY_A),
        ).arrange(DOWN, buff=0.18).move_to([-3.3, 2.3, 0])
        lab = VGroup(label(r"no shear, no matter", font_size=20, color=TH).next_to(ax.c2p(1.0, -2.0), DOWN, buff=0.1),
                     label(r"with matter", font_size=20, color=RIC).next_to(ax.c2p(1.25, -7.5), LEFT, buff=0.1))
        # right: a beam of light focused by a mass (part 1's exact rays, units r_s = 1)
        rz = load("raych")
        beam = rz["beam"]
        cen = np.array([3.0, -0.5, 0])
        sc = 0.2
        rays = VGroup()
        for P in beam:
            P = P[np.isfinite(P[:, 0])]
            pts = np.concatenate([cen[:2] + sc * P, np.zeros((len(P), 1))], 1)
            for sgn in (1, -1):
                q = pts.copy()
                q[:, 1] = cen[1] + sgn * (q[:, 1] - cen[1])
                q = q[(q[:, 0] < 6.9) & (q[:, 0] > -0.4)]
                if len(q) > 2:
                    rays.add(VMobject(stroke_color=C.LIGHT, stroke_width=1.6, stroke_opacity=0.85).set_points_as_corners(q))
        mass = Dot(cen, radius=0.12, color=C.MATTER)
        bl = note(r"light past a mass (exact rays); the beam's cross-section shrinks").move_to([3.2, -3.4, 0])
        with self.voiceover(
            "Now the key consequence, for light rays. <bookmark mark='a'/> Suppose there's no rotation, which is true "
            "for the light rays leaving any surface, and the energy condition holds. Then every term on the right is "
            "negative or zero, so d theta d lambda is at most minus one half theta squared. <bookmark mark='b'/> "
            "Divide by theta squared and integrate. If the bundle starts out converging, with theta naught negative, "
            "then theta must reach minus infinity within an affine distance two over the magnitude of theta naught. "
            "<bookmark mark='c'/> Here's that bound, and an example with matter, which gets there even sooner. Minus "
            "infinity means the rays cross: a caustic, a focal point. <bookmark mark='d'/> Gravity is a lens that only "
            "ever converges."
        ) as vo:
            vo.wait_until("a")
            self.play(FadeIn(eqs[0]))
            vo.wait_until("b")
            self.play(FadeIn(eqs[1]), FadeIn(eqs[2]))
            vo.wait_until("c")
            self.play(Create(ax), FadeIn(xl), FadeIn(yl), Create(wall))
            self.play(Create(c0), Create(c1), FadeIn(lab), FadeIn(eqs[3]), run_time=2)
            vo.wait_until("d")
            self.play(FadeIn(mass), Create(rays, lag_ratio=0.05), FadeIn(bl), run_time=2.5)
        self.clear_scene()

    # ------------------------------------------------------------------
    def trapped(self):
        rz = load("raych")
        tt = rz["tt"]
        sets = [("out3", np.array([-3.4, -0.4, 0]), r"a sphere at $r = 3M$ (outside)"),
                ("in15", np.array([3.4, -0.4, 0]), r"a sphere at $r = 1.5M$ (inside)")]
        k = ValueTracker(0.0)
        sc = 0.55

        def panel(name, cen):
            ro, ri = rz[name + "_out"], rz[name + "_in"]

            def make():
                i = int(k.get_value() * (len(tt) - 1))
                g = VGroup(Circle(radius=2 * sc, color=C.CURVATURE, stroke_width=2, fill_color=BLACK, fill_opacity=0.6).move_to(cen))
                r0 = ro[0]
                g.add(Circle(radius=r0 * sc, color=GREY_B, stroke_width=1.5).move_to(cen))
                if ro[i] > 0.02:
                    g.add(Circle(radius=ro[i] * sc, color=C.LIGHT, stroke_width=4).move_to(cen))
                if ri[i] > 0.02:
                    g.add(DashedVMobject(Circle(radius=ri[i] * sc, color=C.LIGHT, stroke_width=3).move_to(cen), num_dashes=30))
                return g
            return redraw(make)

        P1, P2 = panel("out3", sets[0][1]), panel("in15", sets[1][1])
        heads = VGroup(*[label(t, font_size=26).move_to(c + UP * 3.1) for _, c, t in sets])
        leg = VGroup(label(r"outgoing flash", font_size=22, color=C.LIGHT),
                     label(r"ingoing flash (dashed)", font_size=22, color=C.LIGHT),
                     label(r"horizon", font_size=22, color=C.CURVATURE)).arrange(RIGHT, buff=0.5).to_edge(DOWN, buff=0.7)
        verdict = VGroup(label(r"outgoing area grows: $\theta_{\rm out} > 0$", font_size=24).move_to(sets[0][1] + DOWN * 2.05),
                         label(r"\emph{both} areas shrink: a trapped surface", font_size=24, color=C.CURVATURE).move_to(sets[1][1] + DOWN * 2.05))
        cmp = note(r"radii of the light fronts computed from outgoing and ingoing radial null rays (Eddington--Finkelstein)").to_edge(DOWN, buff=0.3)
        with self.voiceover(
            "So where would light rays start out converging? <bookmark mark='a'/> Take a sphere outside a black hole and "
            "set off a flash of light on it. The flash splits into two fronts, one moving out and one moving in. The "
            "inner front shrinks, but the outer one grows, as you'd expect. <bookmark mark='b'/> Now do the same inside "
            "the horizon. Both fronts shrink. Even the light aimed outward converges, because inside, r is a time and "
            "it only decreases. <bookmark mark='c'/> A closed surface whose outgoing and ingoing light both converge is "
            "called a trapped surface."
        ) as vo:
            vo.wait_until("a")
            self.add(P1)
            self.play(FadeIn(heads[0]), FadeIn(leg), FadeIn(cmp))
            self.play(k.animate.set_value(0.5), run_time=2.5, rate_func=linear)
            self.play(FadeIn(verdict[0]))
            vo.wait_until("b")
            self.add(P2)
            self.play(FadeIn(heads[1]), k.animate.set_value(0.0), run_time=0.5)
            self.play(k.animate.set_value(1.0), run_time=4, rate_func=linear)
            vo.wait_until("c")
            self.play(FadeIn(verdict[1]))
        P1.clear_updaters()
        P2.clear_updaters()
        self.clear_scene()

    # ------------------------------------------------------------------
    def theorem(self):
        thm = VGroup(
            label(r"\textbf{Penrose (1965).} \ If", font_size=30),
            label(r"1. \ $R_{\mu\nu}k^\mu k^\nu \ge 0$ for all light-like $k$ \ (gravity focuses light),", font_size=28),
            label(r"2. \ space at one moment is infinite (a non-compact Cauchy surface), and", font_size=28),
            label(r"3. \ a closed trapped surface forms,", font_size=28, color=C.CURVATURE),
            label(r"then some light ray ends after a finite affine distance: spacetime is singular.", font_size=28,
                  color=C.SINGULARITY),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.15)
        box = SurroundingRectangle(thm, color=GREY_B, buff=0.25, corner_radius=0.1)
        g = VGroup(box, thm).to_edge(UP, buff=0.35)
        # schematic of the proof idea: the boundary of the trapped surface's future closes up
        o1, o2 = np.array([-3.4, -2.3, 0]), np.array([3.4, -2.3, 0])

        def sheet(o, converge):
            g_ = VGroup()
            w = 0.9
            L, R = o + LEFT * w, o + RIGHT * w
            g_.add(Line(L, R, color=WHITE, stroke_width=4))
            if converge:
                apex = o + UP * 0.9
                g_.add(Line(L, apex, color=C.LIGHT, stroke_width=3), Line(R, apex, color=C.LIGHT, stroke_width=3))
                g_.add(Polygon(L, R, apex, stroke_width=0, fill_color=C.LIGHT, fill_opacity=0.15))
            else:
                g_.add(Line(L, L + np.array([-1.3, 1.3, 0]), color=C.LIGHT, stroke_width=3),
                       Line(R, R + np.array([1.3, 1.3, 0]), color=C.LIGHT, stroke_width=3))
                g_.add(Line(L, L + np.array([0.9, 0.9, 0]), color=C.LIGHT, stroke_width=2, stroke_opacity=0.6),
                       Line(R, R + np.array([-0.9, 0.9, 0]), color=C.LIGHT, stroke_width=2, stroke_opacity=0.6))
            return g_

        s1, s2 = sheet(o1, False), sheet(o2, True)
        c1 = label(r"ordinary sphere: the edge of its future runs off to infinity", font_size=22).next_to(s1, DOWN, buff=0.2)
        c2 = label(r"trapped: the light rays meet; the edge of its future is finite", font_size=22,
                   color=C.CURVATURE).next_to(s2, DOWN, buff=0.2)
        sch = note(r"schematic (one space dimension shown)").to_corner(DR, buff=0.2)
        nob = VGroup(
            label(r"Nobel Prize 2020: ``for the discovery that black hole formation is a robust", font_size=24,
                  color=GREY_A),
            label(r"prediction of the general theory of relativity''", font_size=24, color=GREY_A),
        ).arrange(DOWN, buff=0.08).move_to(DOWN * 0.15)
        with self.voiceover(
            "Here is Penrose's theorem. <bookmark mark='a'/> If gravity focuses light, if space at one moment is "
            "infinite, and if a trapped surface forms, then some light ray must come to an end after a finite affine "
            "distance: spacetime has an edge, a singularity. <bookmark mark='b'/> The idea of the proof: the light rays "
            "leaving a trapped surface are all converging, so by Raychaudhuri, they all reach caustics within a finite "
            "distance. So the boundary of everything the surface can influence is finite, closed off. "
            "<bookmark mark='c'/> But that finite boundary would have to map onto the whole of an infinite space, which "
            "is impossible, unless some of those light rays simply end."
        ) as vo:
            vo.wait_until("a")
            self.play(Create(box), FadeIn(thm, lag_ratio=0.15), run_time=3)
            vo.wait_until("b")
            self.play(FadeIn(s2), FadeIn(c2), FadeIn(sch))
            vo.wait_until("c")
            self.play(FadeIn(s1), FadeIn(c1))
        with self.voiceover(
            "Nothing in this argument needs symmetry, and a slightly deformed trapped surface is still trapped, so the "
            "conclusion is robust. <bookmark mark='n'/> In 2020, Penrose received the Nobel Prize for exactly this: "
            "showing that black hole formation is a robust prediction of general relativity. <bookmark mark='h'/> "
            "Stephen Hawking turned the same argument around in time: an expanding universe filled with ordinary "
            "matter must have a singularity in its past, a precise version of the Big Bang. <bookmark mark='q'/> What the theorems don't say is what the singularity is like. "
            "They predict where general relativity itself breaks down, and a quantum theory of gravity must take over."
        ) as vo:
            vo.wait_until("n")
            self.play(FadeOut(VGroup(s1, s2, c1, c2, sch)), FadeIn(nob, lag_ratio=0.2))
        self.clear_scene()
