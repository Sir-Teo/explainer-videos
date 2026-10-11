from __future__ import annotations

import math

import numpy as np

from explainer import *  # noqa: F403
from videos.relativity2 import spacetime as st
from videos.relativity2.common import (clamp_x, label, ladder, load, mtex, note, polyline, redraw, under)
from videos.relativity2.geometry import check_kerr_thermo

SPIN, HOR, NEG = C.SPIN, C.CURVATURE, C.NEG_ENERGY


class Extraction(VoiceoverScene):
    def construct(self):
        assert check_kerr_thermo() == "ok"
        self.d = load("kerr_orbits")
        self.negative()
        self.process()
        self.limit()
        self.irreducible()

    # ------------------------------------------------------------------
    def negative(self):
        rows = [
            mtex(r"E", r"=", r"-p_t = -\,p\cdot\partial_t", font_size=42),
            mtex(r"E", r"=", r"\alpha\,\varepsilon + \omega\,L", font_size=42),
            mtex(r"E < 0", r"\iff", r"L < 0 \ \text{ and }\ \omega\sqrt{g_{\phi\phi}} > \alpha\ \ (\text{the ergosphere})", font_size=38),
        ]
        whys = [
            note(r"the conserved energy, as measured from far away (the metric doesn't depend on $t$)"),
            note(r"$\varepsilon$: energy measured by a local observer orbiting with the dragging ($\varepsilon > 0$ always); \ $\alpha$: the redshift factor"),
            note(r"a fast enough backward-moving particle, deep enough in"),
        ]
        rows[0][0].set_color(C.MATTER)
        rows[2][0].set_color(NEG)
        under(rows, whys, -1.0)
        step = ladder(self, rows, whys, keep=3, top=2.8, x=-1.0, buff=0.7)
        pt = label(r"$\partial_t$ is spacelike inside the ergosphere, so $-p\cdot\partial_t$ can be negative", font_size=28,
                   color=SPIN).to_edge(DOWN, buff=0.6)
        hdr = label(r"Negative energy", font_size=44, color=NEG)
        with self.voiceover(
            "The ergosphere allows something impossible anywhere else: negative energy. <bookmark mark='a'/> A "
            "particle's conserved energy, the one measured from far away, is minus its momentum dotted into the time "
            "direction. <bookmark mark='b'/> Split it into what a local observer, carried around by the dragging, "
            "measures, which is always positive, plus a term from frame dragging times the angular momentum. "
            "<bookmark mark='c'/> If the particle moves backward against the rotation, L is negative, and inside the "
            "ergosphere, the dragging is strong enough that the total can be negative. <bookmark mark='d'/> Geometrically, "
            "the time direction of the distant observers is spacelike there, so this dot product can have either sign. "
            "A particle on such an orbit can never escape. But it can fall in."
        ) as vo:
            self.play(FadeIn(hdr))
            vo.wait_until("a")
            self.play(FadeOut(hdr), run_time=0.5)
            step(0)
            vo.wait_until("b")
            step(1)
            vo.wait_until("c")
            step(2)
            vo.wait_until("d")
            self.play(FadeIn(pt))
        self.clear_scene()

    # ------------------------------------------------------------------
    def process(self):
        d = self.d
        a = float(d["pp_a"])
        E0, E1, E2 = d["pp_E"]
        assert abs(E1 + 0.095) < 1e-3 and abs(E2 - 1.095) < 1e-3
        cen = np.array([-2.6, -0.3, 0])
        sc = 0.85
        rp = st.r_plus(a)
        hor = Circle(radius=math.sqrt(rp * rp + a * a) * sc, color=HOR, stroke_width=3, fill_color=BLACK,
                     fill_opacity=1).move_to(cen)
        ergo = DashedVMobject(Circle(radius=math.sqrt(4 + a * a) * sc, color=SPIN, stroke_width=2.5).move_to(cen),
                              num_dashes=48)
        rot = Arc(radius=0.35, start_angle=0, angle=1.6 * PI, color=SPIN, stroke_width=3).move_arc_center_to(cen)
        rot.add_tip(tip_length=0.15)
        P0, P1, P2 = d["pp_in"], d["pp_neg"], d["pp_out"]
        t0, t1, t2 = d["pp_tau0"], d["pp_tau1"], d["pp_tau2"]

        def scr(P):
            return np.concatenate([cen[:2] + sc * P, np.zeros((len(P), 1))], 1)

        S0, S1, S2 = scr(P0)[::-1], scr(P1), scr(P2)
        tt0 = -t0[::-1]  # (particle 0 was integrated backward from the split, tau <= 0)
        T0 = float(-tt0[0])
        k = ValueTracker(-T0)

        def trails():
            t = k.get_value()
            g = VGroup()
            j = int(np.searchsorted(tt0, min(t, 0.0)))
            if j >= 2:
                g.add(VMobject(stroke_color=C.MATTER, stroke_width=4).set_points_as_corners(S0[:j]))
            if t < 0:
                g.add(Dot(S0[max(j - 1, 0)], radius=0.1, color=C.MATTER))
                return g
            j1 = int(np.searchsorted(t1, t))
            j2 = int(np.searchsorted(t2, t))
            if j1 >= 2:
                g.add(VMobject(stroke_color=NEG, stroke_width=4).set_points_as_corners(S1[:j1]))
            if j2 >= 2:
                g.add(VMobject(stroke_color=C.MATTER, stroke_width=4).set_points_as_corners(S2[:j2]))
            g.add(Dot(S1[max(min(j1, len(S1)) - 1, 0)], radius=0.07, color=NEG))
            g.add(Dot(S2[max(min(j2, len(S2)) - 1, 0)], radius=0.08, color=C.MATTER))
            return g

        TR = redraw(trails)
        tab = VGroup(
            label(r"in: \ $E_0 = 1.000$", font_size=30, color=C.MATTER),
            label(rf"falls in: \ $E_1 = {E1:.3f}$", font_size=30, color=NEG),
            label(rf"escapes: \ $E_2 = {E2:.3f}$", font_size=30, color=C.MATTER),
            label(rf"gain: \ {100 * (E2 - E0):.0f}\%", font_size=34, color=SPIN),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.25).move_to([4.2, 0.6, 0])
        info = VGroup(
            note(r"computed: Kerr geodesics, $a = 0.99M$, split at $r = 1.4M$; each fragment"),
            note(r"$0.05\times$ the mass, flung apart at 99.5\% of light speed (4-momentum conserved)"),
            note(r"drawn in Kerr--Schild coordinates; dashed: the ergosurface"),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.05).to_corner(DR, buff=0.25)
        t_end = min(float(t1[-1]), float(t2[-1]))
        with self.voiceover(
            "Roger Penrose saw what this allows, in 1969. <bookmark mark='a'/> Send a particle into the ergosphere. "
            "<bookmark mark='b'/> There, let it split in two, throwing one piece backward, against the rotation, fast "
            "enough that its energy is negative. <bookmark mark='c'/> That piece falls into the hole. Energy is "
            "conserved, so the other piece leaves with more energy than the original particle brought in. "
            "<bookmark mark='d'/> In this computed example, almost ten percent more. The extra energy came from the black "
            "hole's rotation: swallowing negative energy and negative angular momentum, the hole gets a little lighter "
            "and spins a little slower."
        ) as vo:
            vo.wait_until("a")
            self.play(FadeIn(hor), Create(ergo), Create(rot), FadeIn(info))
            self.add(TR)
            self.play(k.animate.set_value(0.0), FadeIn(tab[0]), run_time=vo.until("b"), rate_func=linear)
            vo.wait_until("b")
            self.play(k.animate.set_value(0.25 * t_end), run_time=2, rate_func=linear)
            vo.wait_until("c")
            self.play(k.animate.set_value(t_end), FadeIn(tab[1]), FadeIn(tab[2]), run_time=4, rate_func=linear)
            vo.wait_until("d")
            self.play(FadeIn(tab[3]))
        TR.clear_updaters()
        self.clear_scene()

    # ------------------------------------------------------------------
    def limit(self):
        d = self.d
        a = float(d["pp_a"])
        E1, L1 = float(d["pp_E"][1]), float(d["pp_L"][1])
        OmH = st.omega_horizon(a)
        assert E1 - OmH * L1 > 0 and float(d["pp_dA"]) > 0
        rows = [
            mtex(r"-p\cdot\xi", r"\ge", r"0,\qquad \xi = \partial_t + \Omega_H\,\partial_\phi", font_size=40),
            mtex(r"E - \Omega_H L", r"\ge", r"0", font_size=42),
            mtex(r"\delta M", r"\ge", r"\Omega_H\,\delta J", font_size=46),
            mtex(r"\delta A", r"=", r"\frac{8\pi}{\kappa}\big(\delta M - \Omega_H\,\delta J\big) \ge 0", font_size=42),
        ]
        whys = [
            note(r"anything crossing the horizon is future-directed relative to $\xi$, the null generator of the horizon"),
            note(r"for the fragment that falls in"),
            note(r"the hole's mass and spin change by $\delta M = E$, $\delta J = L$"),
            note(r"differentiating Kerr's horizon area $A = 8\pi M r_+$ (checked symbolically)"),
        ]
        rows[2][0].set_color(SPIN)
        rows[3][0].set_color(HOR)
        under(rows, whys, -0.8)
        step = ladder(self, rows, whys, keep=4, top=2.9, x=-0.8, buff=0.62)
        ex = note(rf"in the example: $E_1 - \Omega_H L_1 = {E1 - OmH * L1:.3f} > 0$, and the area grows").to_edge(DOWN, buff=0.5)
        with self.voiceover(
            "Is there a limit? <bookmark mark='a'/> Anything that crosses the horizon must move forward in time "
            "relative to the horizon's own light rays, which rotate with angular velocity Omega H. "
            "<bookmark mark='b'/> For the piece that falls in, that means E minus Omega H times L is at least zero. "
            "<bookmark mark='c'/> So the hole's mass can drop, but only by so much: the change in M is at least Omega H "
            "times the change in J. <bookmark mark='d'/> And here's a surprise. Differentiate the area of Kerr's "
            "horizon, and this inequality says exactly that the area can't decrease. Spin energy can be extracted, but "
            "the horizon's area only grows. We'll meet this again."
        ) as vo:
            vo.wait_until("a")
            step(0)
            vo.wait_until("b")
            step(1)
            vo.wait_until("c")
            step(2)
            vo.wait_until("d")
            step(3)
            self.play(FadeIn(ex))
        self.clear_scene()

    # ------------------------------------------------------------------
    def irreducible(self):
        top = VGroup(
            mtex(r"M^2", r"=", r"M_{\rm irr}^2 + \frac{J^2}{4M_{\rm irr}^2},\qquad M_{\rm irr} = \sqrt{\frac{A}{16\pi}}", font_size=40),
            label(r"Christodoulou (1970): the mass splits into an irreducible part, fixed by the area, plus spin energy",
                  font_size=24, color=GREY_A),
        ).arrange(DOWN, buff=0.15).to_edge(UP, buff=0.4)
        top[0][0].set_color(C.MATTER)
        ax = Axes(x_range=[0, 1.3, 0.25], y_range=[0, 1.3, 0.25], x_length=4.8, y_length=4.4, tips=False,
                  axis_config={"stroke_color": GREY_B, "font_size": 20},
                  x_axis_config={"numbers_to_include": [0.5, 1.0]},
                  y_axis_config={"numbers_to_include": [0.5, 1.0]}).move_to([-3.0, -1.35, 0])
        xl = label(r"$J$", font_size=24, color=SPIN).next_to(ax.x_axis, RIGHT, buff=0.1)
        yl = label(r"$M$", font_size=24, color=C.MATTER).next_to(ax.y_axis, UP, buff=0.1)
        curves = VGroup()
        for Mi in (0.5, 0.6, 0.707, 0.8, 0.9):
            J = np.linspace(0, 2 * Mi * Mi, 200)  # extremal when J = M^2, i.e. J = 2 M_irr^2
            M = np.sqrt(Mi * Mi + J * J / (4 * Mi * Mi))
            ok = (J <= 1.3) & (M <= 1.3)
            curves.add(polyline(ax, J[ok], M[ok], color=HOR, stroke_width=2.2 if Mi != 0.707 else 3.5))
        Jx = np.linspace(0, 1.3, 100)
        ext = polyline(ax, Jx, np.sqrt(Jx), color=GREY_B, stroke_width=2).set_stroke(opacity=0.8)
        extl = label(r"$J = M^2$ (extremal)", font_size=20, color=GREY_B).next_to(ax.c2p(1.2, 1.1), RIGHT, buff=0.05).shift(DOWN * 0.15)
        start = Dot(ax.c2p(1.0, 1.0), radius=0.08, color=WHITE)
        end = Dot(ax.c2p(0.0, 0.7071), radius=0.08, color=WHITE)
        path = polyline(ax, np.linspace(1.0, 0, 100), np.sqrt(0.5 + np.linspace(1.0, 0, 100) ** 2 / 2), color=SPIN,
                        stroke_width=4)
        cl = label(r"curves of constant area", font_size=20, color=HOR).next_to(ax.c2p(0.05, 0.92), UP, buff=0.05).align_to(ax.c2p(0.05, 0), LEFT)
        nums = VGroup(
            label(r"extractable from spin:", font_size=28),
            mtex(r"1 - \frac{M_{\rm irr}}{M} \le 1 - \frac{1}{\sqrt 2} = 29\%", font_size=36, color=SPIN),
            label(r"(for an extremal hole, $J = M^2$)", font_size=22, color=GREY_A),
            label(r"compare: fusion releases $0.7\%$ of hydrogen's mass", font_size=24, color=GREY_A),
            label(r"in nature: magnetic fields threading the ergosphere", font_size=24),
            label(r"(Blandford \& Znajek, 1977) may power the jets of quasars", font_size=24),
        ).arrange(DOWN, buff=0.15).move_to([3.4, -1.2, 0])
        with self.voiceover(
            "Demetrios Christodoulou made this precise in 1970. <bookmark mark='a'/> A Kerr black hole's mass splits "
            "into two parts: an irreducible mass, fixed by the horizon's area, and the energy of its spin. "
            "<bookmark mark='b'/> Here are curves of constant area in the plane of J and M. A Penrose process, done as "
            "gently as possible, moves along one of these curves, removing spin and mass together, until the hole "
            "stops spinning. <bookmark mark='c'/> Starting from a maximally spinning hole, up to twenty-nine percent "
            "of its mass can be extracted. For comparison, nuclear fusion turns seven tenths of a percent of hydrogen's "
            "mass into energy. <bookmark mark='d'/> Nature's version probably uses magnetic fields threading the "
            "ergosphere, which may power the jets of quasars, like the one shooting out of M87."
        ) as vo:
            vo.wait_until("a")
            self.play(FadeIn(top, lag_ratio=0.2))
            vo.wait_until("b")
            self.play(Create(ax), FadeIn(xl), FadeIn(yl), Create(curves), Create(ext), FadeIn(extl), FadeIn(cl))
            self.play(FadeIn(start), Create(path), run_time=2)
            self.play(FadeIn(end))
            vo.wait_until("c")
            self.play(FadeIn(nums[:4], lag_ratio=0.2))
            vo.wait_until("d")
            self.play(FadeIn(nums[4:], lag_ratio=0.2))
        self.clear_scene()
